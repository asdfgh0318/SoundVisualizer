from dataclasses import dataclass

from server.api.schemas import CutoffChannel, CutoffTriggers
from server.core.calibration_override import apply_calibration_config
from server.core.config import TytoCalibrationConfig
from server.core.cutoff_watchdog import CutoffWatchdog
from server.vendor.pawel.msp import PollResponse


@dataclass
class FakeStand:
    mot_pwm: int = 1500


def make_poll(**overrides) -> PollResponse:
    defaults = dict(
        esc_voltage=16.0,
        esc_current=5.0,
        esc_power=80.0,
        load_thrust=0.0,
        load_left=0.0,
        rot_e=10000.0,
        rot_o=10000.0,
        temp0=30.0,
        temp1=30.0,
        temp2=30.0,
        basic_data_flag=b"\x00",
        acc_x=0,
        acc_y=0,
        acc_z=0,
        vibration=0,
        raw_pressure_p=0,
        raw_pressure_t=0,
        load_right=0.0,
        pro_data_flag=b"\x00",
    )
    defaults.update(overrides)
    return PollResponse(**defaults)


def setup_module():
    apply_calibration_config(TytoCalibrationConfig())


def test_no_trip_when_all_disabled():
    stand = FakeStand(mot_pwm=1500)
    wd = CutoffWatchdog(stand, CutoffTriggers())
    assert wd.check_and_trip(make_poll(esc_current=999.0)) is None
    assert stand.mot_pwm == 1500
    assert wd.tripped is None


def test_trips_on_overcurrent():
    stand = FakeStand(mot_pwm=1500)
    wd = CutoffWatchdog(
        stand,
        CutoffTriggers(current=CutoffChannel(enabled=True, threshold=10.0, direction="above")),
    )
    assert wd.check_and_trip(make_poll(esc_current=5.0)) is None
    assert stand.mot_pwm == 1500

    assert wd.check_and_trip(make_poll(esc_current=15.0)) == "current"
    assert stand.mot_pwm == 1000
    assert wd.tripped == "current"


def test_trips_on_undervoltage():
    stand = FakeStand(mot_pwm=1500)
    wd = CutoffWatchdog(
        stand,
        CutoffTriggers(voltage=CutoffChannel(enabled=True, threshold=14.0, direction="below")),
    )
    assert wd.check_and_trip(make_poll(esc_voltage=16.0)) is None
    assert wd.check_and_trip(make_poll(esc_voltage=13.5)) == "voltage"
    assert stand.mot_pwm == 1000


def test_latches_after_first_trip():
    stand = FakeStand(mot_pwm=1500)
    wd = CutoffWatchdog(
        stand,
        CutoffTriggers(current=CutoffChannel(enabled=True, threshold=10.0)),
    )
    wd.check_and_trip(make_poll(esc_current=15.0))
    assert wd.tripped == "current"

    # user manually re-arms PWM (shouldn't matter — watchdog stays tripped)
    stand.mot_pwm = 1500
    # next sample is fine but trip is latched
    result = wd.check_and_trip(make_poll(esc_current=5.0))
    assert result == "current"


def test_reset_clears_trip():
    stand = FakeStand(mot_pwm=1500)
    wd = CutoffWatchdog(
        stand,
        CutoffTriggers(current=CutoffChannel(enabled=True, threshold=10.0)),
    )
    wd.check_and_trip(make_poll(esc_current=15.0))
    wd.reset()
    assert wd.tripped is None
    assert wd.check_and_trip(make_poll(esc_current=5.0)) is None


def test_first_check_decides_channel_when_multiple_trip():
    """If two channels trip on the same sample, the first one in the check order wins.
    The order is documented in CutoffWatchdog: current, voltage, rpm, temp0/1/2, thrust, torque."""
    stand = FakeStand(mot_pwm=1500)
    wd = CutoffWatchdog(
        stand,
        CutoffTriggers(
            current=CutoffChannel(enabled=True, threshold=10.0),
            rpm=CutoffChannel(enabled=True, threshold=15000.0),
        ),
    )
    result = wd.check_and_trip(make_poll(esc_current=15.0, rot_e=20000.0))
    assert result == "current"


def test_thrust_cutoff_uses_calibrated_value():
    """Thrust cutoff threshold is in Newtons. The watchdog must apply Paweł's calibration."""
    stand = FakeStand(mot_pwm=1500)
    wd = CutoffWatchdog(
        stand,
        CutoffTriggers(thrust=CutoffChannel(enabled=True, threshold=50.0, direction="above")),
    )
    # raw load_thrust=0 → calibrated thrust=0 → no trip
    assert wd.check_and_trip(make_poll(load_thrust=0.0)) is None
    # large positive raw load — calibrated value depends on CAL_THRUST sign
    # we just verify a really big magnitude trips
    assert wd.check_and_trip(make_poll(load_thrust=-1.0)) == "thrust"
