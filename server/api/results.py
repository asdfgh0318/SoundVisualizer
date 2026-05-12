"""Results endpoints — group measurements into PWM points, compute FFTs, summarize telemetry."""

import csv
from io import StringIO
from typing import Annotated, Any

import numpy as np
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from server.api.schemas import (
    AcousticMeasurementMeta,
    MeasurementHalf,
    PerformanceMeasurementMeta,
)
from server.core.calibration import apply_calibration_to_spectrum
from server.core.fft import compute_fft
from server.core.wav import read_wav_float32
from server.store import calibration as cal_store
from server.store import keys as keys_store
from server.store import measurements as meas_store
from server.store.paths import measurement_dir

router = APIRouter(prefix="/keys/{slug}", tags=["results"])


def _require_key(slug: str) -> None:
    if not keys_store.get_key(slug):
        raise HTTPException(404, f"Key {slug!r} not found")


class AcousticInPoint(BaseModel):
    id: str
    mic_serial: str
    elevation_deg: float
    half: MeasurementHalf
    calibration_file_id: str | None


class PWMPoint(BaseModel):
    t_start: str
    half: MeasurementHalf | None
    pwm_us: int | None
    performance_id: str | None
    acoustic: list[AcousticInPoint]


@router.get("/pwm_points", response_model=list[PWMPoint])
def list_pwm_points(slug: str) -> list[PWMPoint]:
    _require_key(slug)

    by_t: dict[str, dict[str, Any]] = {}
    for m in meas_store.list_measurements(slug):
        key = m.t_start.isoformat()
        bucket = by_t.setdefault(
            key,
            {
                "performance_id": None,
                "acoustic": [],
                "half": None,
                "pwm_us": None,
            },
        )
        if isinstance(m, PerformanceMeasurementMeta):
            bucket["performance_id"] = m.id
            bucket["pwm_us"] = m.pwm_setpoint
        elif isinstance(m, AcousticMeasurementMeta):
            bucket["acoustic"].append(
                AcousticInPoint(
                    id=m.id,
                    mic_serial=m.mic_serial,
                    elevation_deg=m.elevation_deg,
                    half=m.half,
                    calibration_file_id=m.calibration_file_id,
                )
            )
            if bucket["half"] is None:
                bucket["half"] = m.half
            if bucket["pwm_us"] is None:
                bucket["pwm_us"] = m.pwm_setpoint

    return [
        PWMPoint(
            t_start=k,
            half=v["half"],
            pwm_us=v["pwm_us"],
            performance_id=v["performance_id"],
            acoustic=sorted(v["acoustic"], key=lambda x: -x.elevation_deg),
        )
        for k, v in sorted(by_t.items())
    ]


class FFTResponse(BaseModel):
    frequencies: list[float]
    magnitudes_db: list[float]
    sample_rate: int
    calibrated: bool
    window: str
    size: int


@router.get("/measurements/{meas_id}/fft", response_model=FFTResponse)
def get_fft(
    slug: str,
    meas_id: str,
    window: Annotated[str, Query()] = "hann",
    size: Annotated[int, Query(ge=64, le=131072)] = 4096,
    overlap: Annotated[float, Query(ge=0.0, lt=1.0)] = 0.5,
) -> FFTResponse:
    _require_key(slug)
    meta = meas_store.get_measurement(slug, meas_id)
    if meta is None:
        raise HTTPException(404, f"measurement {meas_id!r} not found")
    if not isinstance(meta, AcousticMeasurementMeta):
        raise HTTPException(400, "FFT is only available for acoustic measurements")

    audio_path = measurement_dir(slug, meas_id) / "audio.wav"
    if not audio_path.exists():
        raise HTTPException(404, "audio.wav missing")

    sr, audio = read_wav_float32(audio_path)
    freq, mag_db = compute_fft(audio, sr, window=window, size=size, overlap=overlap)

    calibrated = False
    if meta.calibration_file_id:
        cal = cal_store.get_calibration(meta.calibration_file_id)
        if cal is not None:
            mag_db = apply_calibration_to_spectrum(freq, mag_db, cal)
            calibrated = True

    return FFTResponse(
        frequencies=freq.tolist(),
        magnitudes_db=mag_db.tolist(),
        sample_rate=sr,
        calibrated=calibrated,
        window=window,
        size=size,
    )


class PerformanceSummary(BaseModel):
    n_samples: int
    duration_s: float
    thrust_n_mean: float
    thrust_n_max: float
    torque_nm_mean: float
    current_a_mean: float
    voltage_v_mean: float
    rpm_mean: float
    temp0_c_max: float
    temp1_c_max: float
    temp2_c_max: float


def _empty_summary() -> PerformanceSummary:
    return PerformanceSummary(
        n_samples=0,
        duration_s=0.0,
        thrust_n_mean=0.0,
        thrust_n_max=0.0,
        torque_nm_mean=0.0,
        current_a_mean=0.0,
        voltage_v_mean=0.0,
        rpm_mean=0.0,
        temp0_c_max=0.0,
        temp1_c_max=0.0,
        temp2_c_max=0.0,
    )


@router.get(
    "/measurements/{meas_id}/performance_summary",
    response_model=PerformanceSummary,
)
def get_performance_summary(slug: str, meas_id: str) -> PerformanceSummary:
    _require_key(slug)
    meta = meas_store.get_measurement(slug, meas_id)
    if meta is None or not isinstance(meta, PerformanceMeasurementMeta):
        raise HTTPException(404, "performance measurement not found")

    csv_path = measurement_dir(slug, meas_id) / "telemetry.csv"
    if not csv_path.exists():
        raise HTTPException(404, "telemetry.csv missing")

    rows = list(csv.DictReader(StringIO(csv_path.read_text())))
    if not rows:
        return _empty_summary()

    def col(name: str) -> np.ndarray:
        return np.array([float(r[name]) for r in rows])

    t = col("t_offset_s")
    duration = float(t[-1] - t[0]) if len(t) > 1 else 0.0

    return PerformanceSummary(
        n_samples=len(rows),
        duration_s=duration,
        thrust_n_mean=float(col("thrust_n").mean()),
        thrust_n_max=float(col("thrust_n").max()),
        torque_nm_mean=float(col("torque_nm").mean()),
        current_a_mean=float(col("current_a").mean()),
        voltage_v_mean=float(col("voltage_v").mean()),
        rpm_mean=float(col("rpm").mean()),
        temp0_c_max=float(col("temp0_c").max()),
        temp1_c_max=float(col("temp1_c").max()),
        temp2_c_max=float(col("temp2_c").max()),
    )
