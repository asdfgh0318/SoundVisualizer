"""Tare/zero logic for the Tyto stand: zero() captures the at-rest baseline and
_build_telemetry subtracts it."""

from dataclasses import dataclass

from server.api.schemas import CutoffTriggers
from server.core.calibration_override import apply_calibration_config
from server.core.config import TytoCalibrationConfig
from server.core.cutoff_watchdog import CutoffWatchdog
from server.core.thrust_stand_service import (
    TareOffsets,
    ThrustStandService,
    _build_telemetry,
)
from server.vendor.pawel.msp import PollResponse
from server.vendor.pawel.thrust_stand import raw_thrust


def _poll(load_thrust: float) -> PollResponse:
    return PollResponse(
        esc_voltage=0.0, esc_current=0.5, esc_power=0.0,
        load_thrust=load_thrust, load_left=0.0, load_right=0.0,
        rot_e=0.0, rot_o=0.0, temp0=0.0, temp1=0.0, temp2=0.0,
        basic_data_flag=b"\x00", acc_x=0, acc_y=0, acc_z=0, vibration=0,
        raw_pressure_p=0, raw_pressure_t=0, pro_data_flag=b"\x00",
    )


@dataclass
class _Stand:
    mot_pwm: int = 1000
    samples_raw: list = None

    def __post_init__(self):
        if self.samples_raw is None:
            self.samples_raw = []


def _service() -> ThrustStandService:
    apply_calibration_config(TytoCalibrationConfig())
    stand = _Stand(samples_raw=[_poll(1234.0) for _ in range(30)])
    return ThrustStandService(stand, CutoffTriggers())


def test_zero_captures_resting_baseline():
    svc = _service()
    resting = raw_thrust(1234.0)
    assert svc.tare.thrust_n == 0.0  # untared by default

    tare = svc.zero()
    # tare equals the mean resting thrust (all samples identical here)
    assert abs(tare.thrust_n - resting) < 1e-6
    assert abs(tare.current_a - 0.5) < 1e-6


def test_zero_refuses_above_idle():
    svc = _service()
    svc.stand.mot_pwm = 1200
    try:
        svc.zero()
        raise AssertionError("expected RuntimeError when not idle")
    except RuntimeError as e:
        assert "idle" in str(e)


def test_build_telemetry_subtracts_tare():
    svc = _service()
    svc.zero()
    frame = _build_telemetry(svc.stand, CutoffWatchdog(svc.stand, CutoffTriggers()), svc.tare)
    # resting thrust minus its own tare ≈ 0
    assert abs(frame["thrust_n"]) < 1e-6
    assert abs(frame["current_a"]) < 1e-6


def test_clear_tare_restores_raw():
    svc = _service()
    svc.zero()
    assert svc.tare.thrust_n != 0.0
    svc.clear_tare()
    assert svc.tare == TareOffsets()
