"""Serial-link loss + reconnect for the Tyto stand.

The FT231X drops and re-enumerates on its own; when it does, the vendored poller
either raises or just stops producing samples. Both must be detected, and the
recovered link must come back at idle PWM with tare/cutoffs intact.
"""

import asyncio

import pytest
from fastapi.testclient import TestClient

from server.api.schemas import CutoffChannel, CutoffTriggers
from server.core import thrust_stand_service as svc_mod
from server.core.calibration_override import apply_calibration_config
from server.core.config import TytoCalibrationConfig
from server.core.thrust_stand_service import ThrustStandService
from server.main import app
from server.vendor.pawel.msp import PollResponse


def _poll(**ovr) -> PollResponse:
    d = dict(
        esc_voltage=16.0, esc_current=5.0, esc_power=80.0,
        load_thrust=0.0, load_left=0.0, load_right=0.0,
        rot_e=10000.0, rot_o=10000.0,
        temp0=30.0, temp1=30.0, temp2=30.0,
        basic_data_flag=b"\x00", acc_x=0, acc_y=0, acc_z=0,
        vibration=0, raw_pressure_p=0, raw_pressure_t=0,
        pro_data_flag=b"\x00",
    )
    d.update(ovr)
    return PollResponse(**d)


class FakeStand:
    """Stands in for Paweł's ThrustStand: one future per poll tick — resolved by
    `tick()`, failed by `die()`, or simply left hanging (the stall case)."""

    def __init__(self, pwm: int = 1000, autotick: bool = False):
        self.mot_pwm = pwm
        self.tare_thrust = self.tare_torque = self.tare_current = 0.0
        self.samples_raw = [_poll()]
        self._future: asyncio.Future[None] = asyncio.get_running_loop().create_future()
        self._ticker: asyncio.Task[None] | None = None
        if autotick:
            self._ticker = asyncio.create_task(self._autotick())

    async def _autotick(self) -> None:
        while True:
            await asyncio.sleep(0.005)
            self.tick()

    def next_sample(self):
        return asyncio.shield(self._future)

    def tick(self) -> None:
        self.samples_raw.append(_poll())
        if not self._future.done():
            self._future.set_result(None)
        self._future = asyncio.get_running_loop().create_future()

    def die(self, exc: Exception) -> None:
        self._future.set_exception(exc)

    def close(self) -> None:
        if self._ticker is not None:
            self._ticker.cancel()


@pytest.fixture(autouse=True)
def _fast_backoff(monkeypatch):
    apply_calibration_config(TytoCalibrationConfig())
    monkeypatch.setattr(svc_mod, "RECONNECT_BACKOFF_S", (0.0,))


def _service(stand: FakeStand, stall_timeout_s: float = 0.02) -> ThrustStandService:
    cutoffs = CutoffTriggers(current=CutoffChannel(enabled=True, threshold=42.0))
    s = ThrustStandService(stand, cutoffs, tty="/dev/fake", stall_timeout_s=stall_timeout_s)
    s._consumer_task = asyncio.create_task(s._consume())
    return s


async def _settle(n: int = 5) -> None:
    for _ in range(n):
        await asyncio.sleep(0.03)


async def test_stall_is_detected_and_link_reopened(monkeypatch):
    """No sample within the stall timeout ⇒ dead link ⇒ reopen the same tty."""
    stand = FakeStand(pwm=1600)
    fresh = FakeStand(autotick=True)
    opened: list[str] = []

    async def fake_open(tty: str):
        opened.append(tty)
        return fresh, None

    monkeypatch.setattr(svc_mod, "open_stand", fake_open)
    svc = _service(stand)
    svc.tare.thrust_n = 4.6
    try:
        await _settle()
        assert opened == ["/dev/fake"]
        assert svc.stand is fresh
        assert svc.connected is True
        # Safety: never resume a live throttle across a reconnect.
        assert svc.stand.mot_pwm == 1000
        # Tare + cutoffs survive, and the watchdog now points at the new stand.
        assert svc.tare.thrust_n == 4.6
        assert svc.watchdog.cutoffs.current.threshold == 42.0
        assert svc.watchdog.stand is fresh
    finally:
        await svc.stop()
        fresh.close()


async def test_poll_exception_is_detected(monkeypatch):
    """The raising case: the vendored reader pushes the serial error into the
    pending poll future."""
    stand = FakeStand()
    fresh = FakeStand(autotick=True)
    opened: list[str] = []

    async def fake_open(tty: str):
        opened.append(tty)
        return fresh, None

    monkeypatch.setattr(svc_mod, "open_stand", fake_open)
    svc = _service(stand, stall_timeout_s=5.0)
    try:
        await asyncio.sleep(0.01)
        stand.die(OSError("read failed: device disconnected"))
        await _settle()
        assert opened == ["/dev/fake"]
        assert svc.stand is fresh
        assert svc.connected is True
    finally:
        await svc.stop()
        fresh.close()


async def test_status_is_disconnected_while_retrying(monkeypatch):
    stand = FakeStand()
    fresh = FakeStand(autotick=True)
    release = asyncio.Event()

    async def fake_open(_tty: str):
        await release.wait()
        return fresh, None

    monkeypatch.setattr(svc_mod, "open_stand", fake_open)
    svc = _service(stand)
    try:
        await _settle(2)
        assert svc.connected is False
        assert svc.link_state == "reconnecting"
        assert "Timeout" in (svc.link_error or "")
        # PWM/zero must refuse rather than write into a dead port.
        with pytest.raises(RuntimeError, match="link is down"):
            svc.set_pwm(1200)
        with pytest.raises(RuntimeError, match="link is down"):
            svc.zero()

        release.set()
        await _settle()
        assert svc.connected is True
        assert svc.link_state == "connected"
        assert svc.link_error is None
    finally:
        await svc.stop()
        fresh.close()


async def test_open_failures_are_retried(monkeypatch):
    stand = FakeStand()
    fresh = FakeStand(autotick=True)
    attempts: list[int] = []

    async def fake_open(_tty: str):
        attempts.append(1)
        if len(attempts) < 3:
            raise OSError("no such device")
        return fresh, None

    monkeypatch.setattr(svc_mod, "open_stand", fake_open)
    svc = _service(stand)
    try:
        await _settle(8)
        assert len(attempts) == 3
        assert svc.connected is True
        assert svc.stand is fresh
    finally:
        await svc.stop()
        fresh.close()


async def test_subscribers_get_a_link_down_frame(monkeypatch):
    stand = FakeStand()
    release = asyncio.Event()

    async def fake_open(_tty: str):
        await release.wait()
        return FakeStand(), None

    monkeypatch.setattr(svc_mod, "open_stand", fake_open)
    svc = _service(stand, stall_timeout_s=0.3)
    q = svc.subscribe()
    try:
        await asyncio.sleep(0.01)
        stand.tick()
        first = await asyncio.wait_for(q.get(), 1.0)
        assert first["connected"] is True

        down = await asyncio.wait_for(q.get(), 2.0)
        assert down["connected"] is False
        assert down["link_error"]
    finally:
        release.set()
        await svc.stop()


class _FakeStandStub:
    mot_pwm = 1000


class _FakeWatchdog:
    tripped = None


class _FakeApiService:
    """Minimal shape the /tyto/status route reads."""

    def __init__(self, connected: bool):
        self.connected = connected
        self.link_state = "connected" if connected else "reconnecting"
        self.link_error = None if connected else "OSError: device disconnected"
        self.stand = _FakeStandStub()
        self.watchdog = _FakeWatchdog()
        self.tare = svc_mod.TareOffsets()


def test_status_endpoint_reports_link_state():
    client = TestClient(app)
    try:
        assert client.get("/tyto/status").json()["link_state"] == "absent"

        app.state.thrust_stand = _FakeApiService(connected=False)
        body = client.get("/tyto/status").json()
        assert body["connected"] is False
        assert body["link_state"] == "reconnecting"
        assert "device disconnected" in body["link_error"]

        app.state.thrust_stand = _FakeApiService(connected=True)
        body = client.get("/tyto/status").json()
        assert body["connected"] is True
        assert body["link_state"] == "connected"
        assert body["link_error"] is None
    finally:
        app.state.thrust_stand = None


def test_capture_run_rejected_while_link_down():
    from server.core.capture_orchestrator import CaptureOrchestrator

    client = TestClient(app)
    try:
        app.state.capture_orchestrator = CaptureOrchestrator()
        app.state.thrust_stand = _FakeApiService(connected=False)
        r = client.post(
            "/capture/run",
            json={
                "key": {"motor": "m", "propeller": "p", "shroud": "s", "notes": "n"},
                "pwm_steps": [{"pwm_us": 1100, "recording_ms": 100}],
                "mics": [{"serial": "8100001", "device_index": 0, "elevation_deg": 0.0}],
            },
        )
        assert r.status_code == 503
        assert "link is down" in r.json()["detail"]
    finally:
        app.state.thrust_stand = None
        app.state.capture_orchestrator = None
