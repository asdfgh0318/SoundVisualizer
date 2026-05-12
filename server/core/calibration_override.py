"""Apply per-unit Tyto calibration to Paweł's vendored module.

Paweł's `thrust_stand.py` computes derived constants (`THRUST_CONST`, `TORQUE_CONST`,
`CAL_TORQUE_LEFT`, `CAL_TORQUE_RIGHT`, `CAL_SYNCSPEED`) at import time. To override
calibration, we re-write both the leaf constants AND the derived products on the
module so subsequent calls to `raw_thrust` / `raw_torque` see the updated values.

Idempotent and safe to call multiple times.
"""

import math

from server.core.config import TytoCalibrationConfig
from server.vendor.pawel import thrust_stand as ts


def apply_calibration_config(cfg: TytoCalibrationConfig) -> None:
    ts.HINGE_DISTANCE = cfg.hinge_distance
    ts.CAL_POLES = cfg.cal_poles
    ts.CAL_HINGE_LEFT = cfg.cal_hinge_left
    ts.CAL_HINGE_RIGHT = cfg.cal_hinge_right
    ts.CAL_LEFT = cfg.cal_left
    ts.CAL_RIGHT = cfg.cal_right
    ts.CAL_THRUST = cfg.cal_thrust

    g = ts.GRAVITY_CONST  # gravity stays universal
    ts.THRUST_CONST = 1000 * 5 / 5 * g
    ts.TORQUE_CONST = 1000 * 2 / 5 * g * cfg.hinge_distance / 2
    ts.CAL_TORQUE_LEFT = cfg.cal_left * cfg.cal_hinge_left
    ts.CAL_TORQUE_RIGHT = cfg.cal_right * cfg.cal_hinge_right
    ts.CAL_SYNCSPEED = 2 / cfg.cal_poles * 2 * math.pi
