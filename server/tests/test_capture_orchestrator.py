"""Orchestrator tests with a fully faked stand + mic capture (no hardware).

The orchestrator is glue code; we exercise its state machine, error handling,
and persistence rather than the actual capture/PWM control."""

import asyncio
from typing import Any

import numpy as np
import pytest

from server.api.schemas import (
    CaptureRunPhase,
    CutoffTriggers,
    KeyFields,
    MeasurementHalf,
    PWMStep,
)
from server.core.calibration_override import apply_calibration_config
from server.core.capture_orchestrator import (
    CaptureHalfRunRequest,
    CaptureOrchestrator,
    MicSpecRun,
    TriggerSyncRun,
)
from server.core.config import TytoCalibrationConfig
from server.core.cutoff_watchdog import CutoffWatchdog
from server.core.thrust_stand_service import TareOffsets
from server.vendor.pawel.msp import PollResponse


def _make_poll(**ovr: Any) -> PollResponse:
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
    def __init__(self):
        self.mot_pwm = 1000
        self.samples_raw: list[PollResponse] = [_make_poll() for _ in range(20)]
        self.sample_number = len(self.samples_raw)

    async def stabilize_rpm(self, _window: int, _tolerance: float) -> None:
        # immediate return — pretend stable
        await asyncio.sleep(0)

    def start_meas_series(self):
        from server.vendor.pawel.thrust_stand import PendingMeasurementSeries
        return PendingMeasurementSeries(self.sample_number)

    def finish_meas_series(self, p):
        return list(self.samples_raw[-3:])  # 3 samples in the window


class FakeService:
    def __init__(self):
        self.stand = FakeStand()
        self.watchdog = CutoffWatchdog(self.stand, CutoffTriggers())
        self.tare = TareOffsets()

    def set_pwm(self, pwm_us: int) -> None:
        if self.watchdog.tripped:
            raise RuntimeError(f"watchdog tripped on {self.watchdog.tripped}")
        self.stand.mot_pwm = pwm_us


@pytest.fixture(autouse=True)
def _setup(tmp_path, monkeypatch):
    monkeypatch.setenv("SOUNDVIS_DATA", str(tmp_path))
    apply_calibration_config(TytoCalibrationConfig())
    return tmp_path


@pytest.fixture
def fake_capture(monkeypatch):
    """Replace `capture_simultaneous` with a stub that returns silent buffers."""
    from server.core import capture_orchestrator as orch_mod
    from server.core.capture import CaptureResult

    def fake(specs, _duration):
        return [
            CaptureResult(
                serial=s.serial, sample_rate=s.sample_rate,
                audio=np.zeros(int(s.sample_rate * 0.1), dtype=np.float32),
            )
            for s in specs
        ]

    monkeypatch.setattr(orch_mod, "capture_simultaneous", fake)


@pytest.fixture
def request_body() -> CaptureHalfRunRequest:
    return CaptureHalfRunRequest(
        key=KeyFields(motor="M", propeller="P", shroud="S", notes="N"),
        half=MeasurementHalf.TOP,
        pwm_steps=[PWMStep(pwm_us=1100, recording_ms=100), PWMStep(pwm_us=1200, recording_ms=100)],
        mics=[
            MicSpecRun(serial="8100001", device_index=0, elevation_deg=0.0),
            MicSpecRun(serial="8100002", device_index=1, elevation_deg=45.0),
        ],
        sample_rate=48000,
        stabilize_timeout_seconds=2.0,
        trigger=TriggerSyncRun(enabled=False),
    )


async def _wait_until_done(orch: CaptureOrchestrator, timeout: float = 5.0):
    """Poll the task until it completes."""
    if orch._task is None:
        return
    await asyncio.wait_for(orch._task, timeout)


async def test_run_completes_and_writes_measurements(fake_capture, request_body):
    orch = CaptureOrchestrator()
    svc = FakeService()
    status = await orch.start_run(svc, request_body)
    assert status.state == "running"

    await _wait_until_done(orch)

    final = orch.get_status()
    assert final.state == "completed"
    assert final.phase == CaptureRunPhase.COMPLETED
    # 2 PWM steps * (1 perf + 2 acoustic) = 6 measurements
    assert len(final.measurement_ids) == 6
    # spool-down brought PWM to 1000
    assert svc.stand.mot_pwm == 1000


async def test_concurrent_run_rejected(fake_capture, request_body):
    orch = CaptureOrchestrator()
    svc = FakeService()
    await orch.start_run(svc, request_body)
    with pytest.raises(RuntimeError, match="already in progress"):
        await orch.start_run(svc, request_body)
    await _wait_until_done(orch)


async def test_empty_pwm_steps_rejected(fake_capture, request_body):
    request_body.pwm_steps = []
    orch = CaptureOrchestrator()
    svc = FakeService()
    with pytest.raises(ValueError, match="pwm_steps"):
        await orch.start_run(svc, request_body)


async def test_abort_stops_run_and_slams_pwm(fake_capture, request_body):
    request_body.pwm_steps = [PWMStep(pwm_us=1500, recording_ms=5000)]  # long step so we can abort mid-run
    orch = CaptureOrchestrator()
    svc = FakeService()
    await orch.start_run(svc, request_body)
    await asyncio.sleep(0.1)  # let it advance to capturing
    await orch.abort()
    final = orch.get_status()
    assert final.state == "aborted"
    assert svc.stand.mot_pwm == 1000


async def test_subscribe_receives_status_updates(fake_capture, request_body):
    orch = CaptureOrchestrator()
    svc = FakeService()
    queue = orch.subscribe()
    await orch.start_run(svc, request_body)
    await _wait_until_done(orch)

    statuses = []
    while not queue.empty():
        statuses.append(queue.get_nowait())
    states = {s.phase for s in statuses}
    assert CaptureRunPhase.STARTING in states or CaptureRunPhase.SETTING_PWM in states
    assert CaptureRunPhase.COMPLETED in states
