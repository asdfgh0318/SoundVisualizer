"""ThrustStandService — owns the Tyto connection lifetime, runs watchdog + telemetry broadcast.

Single instance lives on the FastAPI app's `lifespan`. On startup:
1. Load `config.toml` and apply calibration to Paweł's vendored module.
2. If `tyto.enabled`, open the serial connection (`open_stand`) and start the
   consumer task that runs the watchdog + broadcasts telemetry.
3. Subscribers (WebSocket clients) get an asyncio.Queue per connection.

The consumer task runs forever (until `stop()`). Each iteration:
- Awaits `stand.next_sample()` — Paweł's poller publishes one Future per ~30ms tick.
- Reads the latest raw `PollResponse`.
- Feeds it through the watchdog (latches trip + slams PWM=1000 if needed).
- Builds a telemetry dict (calibrated thrust/torque, raw V/I/RPM/temps, PWM, trip state).
- Pushes to every subscriber queue, dropping old entries for slow consumers.

Reconnect: the FT231X USB link drops and re-enumerates on its own (observed on
the rig). When it does, the vendored poller dies — either raising out of
`_do_poll` or simply never producing another sample — and with it go telemetry,
PWM transmission (PWM rides on every poll) and, critically, the cutoff
watchdog. The consumer therefore treats "no sample within STALL_TIMEOUT_S" or
any poll exception as a dead link: it tears the old link down, retries
`open_stand(tty)` with backoff (the configured by-id path survives
re-enumeration), and resumes. PWM always comes back at idle — a reconnect never
resumes a live throttle. Tare offsets, cutoff config and the trip latch are
carried across.
"""

import asyncio
import contextlib
import itertools
import logging
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Literal

import serial

from server.api.schemas import CutoffTriggers
from server.core.calibration_override import apply_calibration_config
from server.core.config import Config
from server.core.cutoff_watchdog import CutoffWatchdog
from server.vendor.pawel.async_serial import wrap_serial
from server.vendor.pawel.msp import MSP_TTY_DEF_BAUDRATE, MSPSlave
from server.vendor.pawel.thrust_stand import (
    ThrustStand,
    raw_thrust,
    raw_torque,
)

log = logging.getLogger(__name__)

# Polls arrive every ~30 ms; a whole second of silence means the link is gone.
STALL_TIMEOUT_S = 1.0
# How long to wait for the board's "Ready" banner before calling the open failed.
BANNER_TIMEOUT_S = 10.0
# Paweł's open_connection settles for 5 s after starting the poller; keep parity.
SETTLE_AFTER_OPEN_S = 5.0
# Escalating retry delay, capped — retry forever but never hot-spin.
RECONNECT_BACKOFF_S = (0.5, 1.0, 2.0, 5.0)

LinkState = Literal["absent", "connected", "reconnecting"]


def _open_serial_blocking(tty: str, banner_timeout_s: float) -> serial.Serial:
    """Open the port and wait for the board's `Ready` banner, off the event loop.

    Paweł's `MSPSlave.open_connection` does this inline with `while True:
    s.readline()` on a timeout-less port — against an absent or silent device
    that wedges the whole event loop forever. Same handshake here, but bounded
    and run in a thread.
    """
    ser = serial.Serial(port=tty, baudrate=MSP_TTY_DEF_BAUDRATE, timeout=0.5)
    deadline = time.monotonic() + banner_timeout_s
    try:
        while time.monotonic() < deadline:
            if ser.readline() == b"Ready\r\n":
                return ser
    except Exception:
        ser.close()
        raise
    ser.close()
    raise TimeoutError(f"no MSP 'Ready' banner from {tty} within {banner_timeout_s:.0f}s")


async def open_stand(tty: str) -> tuple[ThrustStand, serial.Serial]:
    """Open a Tyto link and start its poller. Returns the stand plus the raw
    serial handle, which the service needs to tear the link down on reconnect."""
    ser = await asyncio.to_thread(_open_serial_blocking, tty, BANNER_TIMEOUT_S)
    reader, writer = wrap_serial(ser)
    msp = MSPSlave(reader, writer)
    await msp.ensure_reader()
    stand = ThrustStand(msp)
    stand.mot_pwm = 1000
    # Paweł's ThrustStand declares tare_thrust/torque/current but never sets them
    # in __init__; the capture path (finish_meas_series → sample_from_raw) reads
    # them, so a run crashes with AttributeError without this. Zero = no tare;
    # the service's own TareOffsets carry the at-rest baseline.
    stand.tare_thrust = 0.0
    stand.tare_torque = 0.0
    stand.tare_current = 0.0
    await stand.ensure_running()
    await asyncio.sleep(SETTLE_AFTER_OPEN_S)
    return stand, ser


def close_link(stand: Any, ser: Any) -> None:
    """Best-effort teardown of a (usually already dead) link: stop the vendored
    poller/reader tasks and drop the loop's reader on the stale fd, which would
    otherwise keep firing on a vanished device."""
    msp = getattr(stand, "msp", None)
    for task in (getattr(stand, "_poller_task", None), getattr(msp, "_reader_task", None)):
        if task is not None:
            task.cancel()
    if ser is None:
        return
    with contextlib.suppress(Exception):
        fd = ser.fd
        if fd is not None:
            asyncio.get_running_loop().remove_reader(fd)
    with contextlib.suppress(Exception):
        ser.close()


@dataclass
class TareOffsets:
    """At-rest baselines subtracted from thrust/torque/current. The load cell
    reads a non-zero resting value (~4.6 N on our unit); zeroing samples it and
    stores it here so logged + displayed values are referenced to rest."""

    thrust_n: float = 0.0
    torque_nm: float = 0.0
    current_a: float = 0.0


def _build_telemetry(
    stand: ThrustStand, watchdog: CutoffWatchdog, tare: TareOffsets
) -> dict[str, Any]:
    raw = stand.samples_raw[-1]
    return {
        "t": datetime.now(UTC).isoformat(),
        "connected": True,
        "pwm_us": stand.mot_pwm,
        "thrust_n": raw_thrust(raw.load_thrust) - tare.thrust_n,
        "torque_nm": raw_torque(raw.load_left, raw.load_right) - tare.torque_nm,
        "current_a": raw.esc_current - tare.current_a,
        "voltage_v": raw.esc_voltage,
        "rpm": raw.rot_e,
        "temp0_c": raw.temp0,
        "temp1_c": raw.temp1,
        "temp2_c": raw.temp2,
        "vibration": raw.vibration,
        "tripped": watchdog.tripped,
    }


class ThrustStandService:
    def __init__(
        self,
        stand: ThrustStand,
        cutoffs: CutoffTriggers,
        tty: str = "",
        serial_port: serial.Serial | None = None,
        stall_timeout_s: float = STALL_TIMEOUT_S,
    ):
        self.stand = stand
        self.watchdog = CutoffWatchdog(stand, cutoffs)
        self.tare = TareOffsets()
        self.connected = True
        self.link_error: str | None = None
        self._tty = tty
        self._serial = serial_port
        self._stall_timeout_s = stall_timeout_s
        self._subscribers: list[asyncio.Queue[dict[str, Any]]] = []
        self._consumer_task: asyncio.Task[None] | None = None

    @classmethod
    async def start(cls, config: Config) -> "ThrustStandService":
        apply_calibration_config(config.tyto.calibration)
        stand, ser = await open_stand(config.tyto.tty)
        service = cls(stand, CutoffTriggers(), tty=config.tyto.tty, serial_port=ser)
        service._consumer_task = asyncio.create_task(service._consume())
        return service

    async def stop(self) -> None:
        if self._consumer_task:
            self._consumer_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._consumer_task
            self._consumer_task = None
        close_link(self.stand, self._serial)

    @property
    def link_state(self) -> LinkState:
        return "connected" if self.connected else "reconnecting"

    async def _consume(self) -> None:
        while True:
            try:
                async with asyncio.timeout(self._stall_timeout_s):
                    await self.stand.next_sample()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                await self._recover(e)
                continue
            if not self.stand.samples_raw:
                continue
            raw = self.stand.samples_raw[-1]
            self.watchdog.check_and_trip(raw)
            self._publish(_build_telemetry(self.stand, self.watchdog, self.tare))

    def _publish(self, msg: dict[str, Any]) -> None:
        dead: list[asyncio.Queue[dict[str, Any]]] = []
        for q in self._subscribers:
            try:
                if q.full():
                    with contextlib.suppress(asyncio.QueueEmpty):
                        q.get_nowait()
                q.put_nowait(msg)
            except Exception:
                dead.append(q)
        for q in dead:
            self._subscribers.remove(q)

    def link_frame(self) -> dict[str, Any]:
        return {
            "t": datetime.now(UTC).isoformat(),
            "connected": self.connected,
            "link_error": self.link_error,
        }

    async def _recover(self, exc: BaseException) -> None:
        """Mark the link dead, tell everyone, then retry the port until it opens."""
        self.connected = False
        self.link_error = f"{type(exc).__name__}: {exc}".rstrip(": ")
        log.warning("Tyto link lost (%s) — reconnecting on %s", self.link_error, self._tty)
        self._publish(self.link_frame())
        close_link(self.stand, self._serial)
        self._serial = None

        for attempt in itertools.count(1):
            await asyncio.sleep(RECONNECT_BACKOFF_S[min(attempt - 1, len(RECONNECT_BACKOFF_S) - 1)])
            try:
                stand, ser = await open_stand(self._tty)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.link_error = f"{type(e).__name__}: {e}".rstrip(": ")
                log.warning("Tyto reconnect attempt %d failed: %s", attempt, self.link_error)
                continue
            # Safety: a reconnect never resumes a live throttle.
            stand.mot_pwm = 1000
            self.stand = stand
            self._serial = ser
            # The watchdog holds its own reference — repoint it or its PWM slam
            # would land on the dead stand. Cutoff config + trip latch survive.
            self.watchdog.stand = stand
            self.connected = True
            self.link_error = None
            log.info("Tyto link re-established on %s after %d attempt(s)", self._tty, attempt)
            # No "back up" frame — data frames resume within one poll period and
            # carry connected=True themselves.
            return

    def set_pwm(self, pwm_us: int) -> None:
        if not 1000 <= pwm_us <= 2000:
            raise ValueError(f"pwm_us {pwm_us} out of range [1000, 2000]")
        if not self.connected:
            raise RuntimeError("Tyto serial link is down; reconnecting")
        if self.watchdog.tripped:
            raise RuntimeError(f"watchdog tripped on {self.watchdog.tripped}; reset first")
        self.stand.mot_pwm = pwm_us

    def update_cutoffs(self, cutoffs: CutoffTriggers) -> None:
        self.watchdog.cutoffs = cutoffs

    def reset_watchdog(self) -> None:
        self.watchdog.reset()

    def zero(self, n: int = 30) -> TareOffsets:
        """Set tare offsets from the mean of the last `n` at-rest samples.

        Only valid at idle — taring while the motor spins would bake thrust into
        the baseline. Raises if no samples yet or PWM is above idle.
        """
        if not self.connected:
            raise RuntimeError("Tyto serial link is down; reconnecting")
        if self.stand.mot_pwm != 1000:
            raise RuntimeError("zero only at idle (pwm 1000); spool down first")
        window = self.stand.samples_raw[-n:]
        if not window:
            raise RuntimeError("no samples yet")
        k = len(window)
        self.tare = TareOffsets(
            thrust_n=sum(raw_thrust(s.load_thrust) for s in window) / k,
            torque_nm=sum(raw_torque(s.load_left, s.load_right) for s in window) / k,
            current_a=sum(s.esc_current for s in window) / k,
        )
        return self.tare

    def clear_tare(self) -> None:
        self.tare = TareOffsets()

    def subscribe(self) -> asyncio.Queue[dict[str, Any]]:
        q: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=10)
        self._subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue[dict[str, Any]]) -> None:
        if q in self._subscribers:
            self._subscribers.remove(q)
