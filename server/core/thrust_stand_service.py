"""ThrustStandService — owns the Tyto connection lifetime, runs watchdog + telemetry broadcast.

Single instance lives on the FastAPI app's `lifespan`. On startup:
1. Load `config.toml` and apply calibration to Paweł's vendored module.
2. If `tyto.enabled`, open the serial connection (Paweł's `ThrustStand.open_connection`)
   and start the consumer task that runs the watchdog + broadcasts telemetry.
3. Subscribers (WebSocket clients) get an asyncio.Queue per connection.

The consumer task runs forever (until `stop()`). Each iteration:
- Awaits `stand.next_sample()` — Paweł's poller publishes one Future per ~30ms tick.
- Reads the latest raw `PollResponse`.
- Feeds it through the watchdog (latches trip + slams PWM=1000 if needed).
- Builds a telemetry dict (calibrated thrust/torque, raw V/I/RPM/temps, PWM, trip state).
- Pushes to every subscriber queue, dropping old entries for slow consumers.
"""

import asyncio
import contextlib
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from server.api.schemas import CutoffTriggers
from server.core.calibration_override import apply_calibration_config
from server.core.config import Config
from server.core.cutoff_watchdog import CutoffWatchdog
from server.vendor.pawel.thrust_stand import (
    ThrustStand,
    raw_thrust,
    raw_torque,
)


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
    def __init__(self, stand: ThrustStand, cutoffs: CutoffTriggers):
        self.stand = stand
        self.watchdog = CutoffWatchdog(stand, cutoffs)
        self.tare = TareOffsets()
        self._subscribers: list[asyncio.Queue[dict[str, Any]]] = []
        self._consumer_task: asyncio.Task[None] | None = None

    @classmethod
    async def start(cls, config: Config) -> "ThrustStandService":
        apply_calibration_config(config.tyto.calibration)
        stand = await ThrustStand.open_connection(config.tyto.tty)
        # Paweł's ThrustStand declares tare_thrust/torque/current but never sets
        # them in __init__; the capture path (finish_meas_series → sample_from_raw)
        # reads them, so a run crashes with AttributeError without this. Zero =
        # no tare; a future "zero stand" step can populate these with the at-rest
        # offsets (the load cell reads a non-zero resting baseline).
        stand.tare_thrust = 0.0
        stand.tare_torque = 0.0
        stand.tare_current = 0.0
        service = cls(stand, CutoffTriggers())
        service._consumer_task = asyncio.create_task(service._consume())
        return service

    async def stop(self) -> None:
        if self._consumer_task:
            self._consumer_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._consumer_task
            self._consumer_task = None

    async def _consume(self) -> None:
        while True:
            await self.stand.next_sample()
            if not self.stand.samples_raw:
                continue
            raw = self.stand.samples_raw[-1]
            self.watchdog.check_and_trip(raw)
            msg = _build_telemetry(self.stand, self.watchdog, self.tare)
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

    def set_pwm(self, pwm_us: int) -> None:
        if not 1000 <= pwm_us <= 2000:
            raise ValueError(f"pwm_us {pwm_us} out of range [1000, 2000]")
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
