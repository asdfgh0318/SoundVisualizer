from pathlib import Path

from pydantic import BaseModel

from server.core.calibration import UmikCalibration, parse_umik_calibration
from server.store.paths import data_root


def calibrations_dir() -> Path:
    return data_root() / "calibrations"


class CalibrationSummary(BaseModel):
    id: str
    serial: str | None
    sens_factor_db: float | None
    again_db: float | None
    n_points: int
    freq_min_hz: float
    freq_max_hz: float


def save_calibration(serial: str, raw_text: str, parsed: UmikCalibration) -> CalibrationSummary:
    d = calibrations_dir()
    d.mkdir(parents=True, exist_ok=True)
    cal_id = serial
    (d / f"{cal_id}.txt").write_text(raw_text)
    summary = CalibrationSummary(
        id=cal_id,
        serial=parsed.serial,
        sens_factor_db=parsed.sens_factor_db,
        again_db=parsed.again_db,
        n_points=len(parsed.freq_hz),
        freq_min_hz=float(parsed.freq_hz[0]),
        freq_max_hz=float(parsed.freq_hz[-1]),
    )
    (d / f"{cal_id}.json").write_text(summary.model_dump_json(indent=2))
    return summary


def list_calibrations() -> list[CalibrationSummary]:
    d = calibrations_dir()
    if not d.exists():
        return []
    return [
        CalibrationSummary.model_validate_json(f.read_text())
        for f in sorted(d.glob("*.json"))
    ]


def get_calibration(cal_id: str) -> UmikCalibration | None:
    p = calibrations_dir() / f"{cal_id}.txt"
    if not p.exists():
        return None
    return parse_umik_calibration(p.read_text())
