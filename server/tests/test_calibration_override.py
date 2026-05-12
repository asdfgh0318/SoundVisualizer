import math

from server.core.calibration_override import apply_calibration_config
from server.core.config import TytoCalibrationConfig
from server.vendor.pawel import thrust_stand as ts


def test_apply_overrides_leaf_constants():
    apply_calibration_config(TytoCalibrationConfig(hinge_distance=0.1, cal_thrust=-2.0))
    assert ts.HINGE_DISTANCE == 0.1
    assert ts.CAL_THRUST == -2.0


def test_apply_recomputes_derived_constants():
    apply_calibration_config(TytoCalibrationConfig(hinge_distance=0.1, cal_left=2.0, cal_right=-3.0,
                                                   cal_hinge_left=1.5, cal_hinge_right=2.5))
    assert ts.CAL_TORQUE_LEFT == 2.0 * 1.5
    assert ts.CAL_TORQUE_RIGHT == -3.0 * 2.5
    expected_torque_const = 1000 * 2 / 5 * ts.GRAVITY_CONST * 0.1 / 2
    assert expected_torque_const == ts.TORQUE_CONST


def test_apply_idempotent_with_defaults():
    apply_calibration_config(TytoCalibrationConfig())
    assert ts.HINGE_DISTANCE == 0.07492
    assert ts.CAL_POLES == 14
    assert 2 / 14 * 2 * math.pi == ts.CAL_SYNCSPEED


def test_raw_thrust_responds_to_override():
    from server.vendor.pawel.thrust_stand import raw_thrust

    apply_calibration_config(TytoCalibrationConfig(cal_thrust=-1.0))
    base = raw_thrust(1.0)
    apply_calibration_config(TytoCalibrationConfig(cal_thrust=-2.0))
    doubled = raw_thrust(1.0)
    assert abs(doubled / base - 2.0) < 1e-9


def test_raw_torque_responds_to_hinge_override():
    from server.vendor.pawel.thrust_stand import raw_torque

    apply_calibration_config(TytoCalibrationConfig(hinge_distance=0.05))
    base = raw_torque(1.0, 1.0)
    apply_calibration_config(TytoCalibrationConfig(hinge_distance=0.10))
    doubled = raw_torque(1.0, 1.0)
    # raw_torque is linear in HINGE_DISTANCE (via TORQUE_CONST)
    assert abs(doubled / base - 2.0) < 1e-9


def teardown_module():
    """Restore Paweł's defaults after this test module so other tests aren't affected."""
    apply_calibration_config(TytoCalibrationConfig())
