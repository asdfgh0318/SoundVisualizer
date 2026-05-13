"""Results endpoints — group measurements into merged PWM points, compute FFTs, summarize telemetry.

A "merged PWM point" combines all captures at the same PWM setpoint that are
compatible with each other on the configured performance tolerances. Top + bottom
captures at the same PWM usually merge into one point; incompatible captures
split into separate sibling points so the user can still see them.
"""

import csv
from io import StringIO
from typing import Annotated, Any

import numpy as np
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from server.api.schemas import (
    AcousticMeasurementMeta,
    CompatibilityTolerances,
    MeasurementHalf,
    PerformanceMeasurementMeta,
)
from server.core.calibration import apply_calibration_to_spectrum
from server.core.fft import compute_fft
from server.core.wav import read_wav_float32
from server.store import calibration as cal_store
from server.store import compat_tolerances as tolerances_store
from server.store import keys as keys_store
from server.store import measurements as meas_store
from server.store.paths import measurement_dir

router = APIRouter(prefix="/keys/{slug}", tags=["results"])


def _require_key(slug: str) -> None:
    if not keys_store.get_key(slug):
        raise HTTPException(404, f"Key {slug!r} not found")


# ----- Performance summary ------------------------------------------------


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
        n_samples=0, duration_s=0.0,
        thrust_n_mean=0.0, thrust_n_max=0.0, torque_nm_mean=0.0,
        current_a_mean=0.0, voltage_v_mean=0.0, rpm_mean=0.0,
        temp0_c_max=0.0, temp1_c_max=0.0, temp2_c_max=0.0,
    )


def _load_performance_summary(slug: str, meas_id: str) -> PerformanceSummary | None:
    meta = meas_store.get_measurement(slug, meas_id)
    if meta is None or not isinstance(meta, PerformanceMeasurementMeta):
        return None
    csv_path = measurement_dir(slug, meas_id) / "telemetry.csv"
    if not csv_path.exists():
        return None
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


@router.get(
    "/measurements/{meas_id}/performance_summary",
    response_model=PerformanceSummary,
)
def get_performance_summary(slug: str, meas_id: str) -> PerformanceSummary:
    _require_key(slug)
    summary = _load_performance_summary(slug, meas_id)
    if summary is None:
        raise HTTPException(404, "performance measurement not found")
    return summary


# ----- Compatibility check -----------------------------------------------


def _compatible(
    a: PerformanceSummary, b: PerformanceSummary, tol: CompatibilityTolerances
) -> bool:
    pairs = [
        (a.thrust_n_mean, b.thrust_n_mean, tol.thrust_n),
        (a.torque_nm_mean, b.torque_nm_mean, tol.torque_nm),
        (a.current_a_mean, b.current_a_mean, tol.current_a),
        (a.voltage_v_mean, b.voltage_v_mean, tol.voltage_v),
        (a.rpm_mean, b.rpm_mean, tol.rpm_mean),
    ]
    for va, vb, t in pairs:
        diff = abs(va - vb)
        rel_ref = (abs(va) + abs(vb)) / 2.0
        threshold = max(t.abs, t.rel * rel_ref)
        if diff > threshold:
            return False
    return True


def _avg_perf(summaries: list[PerformanceSummary]) -> PerformanceSummary:
    n = len(summaries)
    if n == 0:
        return _empty_summary()
    return PerformanceSummary(
        n_samples=sum(s.n_samples for s in summaries) // n,
        duration_s=sum(s.duration_s for s in summaries) / n,
        thrust_n_mean=sum(s.thrust_n_mean for s in summaries) / n,
        thrust_n_max=max(s.thrust_n_max for s in summaries),
        torque_nm_mean=sum(s.torque_nm_mean for s in summaries) / n,
        current_a_mean=sum(s.current_a_mean for s in summaries) / n,
        voltage_v_mean=sum(s.voltage_v_mean for s in summaries) / n,
        rpm_mean=sum(s.rpm_mean for s in summaries) / n,
        temp0_c_max=max(s.temp0_c_max for s in summaries),
        temp1_c_max=max(s.temp1_c_max for s in summaries),
        temp2_c_max=max(s.temp2_c_max for s in summaries),
    )


# ----- Merged PWM points -------------------------------------------------


class AcousticInPoint(BaseModel):
    id: str
    mic_serial: str
    elevation_deg: float
    half: MeasurementHalf
    calibration_file_id: str | None


class UnderlyingCapture(BaseModel):
    t_start: str
    half: MeasurementHalf
    performance_id: str | None
    acoustic: list[AcousticInPoint]
    performance_summary: PerformanceSummary | None


class MergedPWMPoint(BaseModel):
    id: str  # "<pwm_us>-<group_index>"
    pwm_us: int
    composition: dict[str, int]  # e.g. {"top": 2, "bottom": 1}
    underlying: list[UnderlyingCapture]
    acoustic: list[AcousticInPoint]  # combined from all underlying, sorted by elev desc
    avg_performance: PerformanceSummary | None


@router.get("/pwm_points", response_model=list[MergedPWMPoint])
def list_pwm_points(slug: str) -> list[MergedPWMPoint]:
    _require_key(slug)
    tolerances = tolerances_store.load_tolerances()

    # 1. Group raw measurements by t_start. Each bucket = one "capture" (one PWM step on one half).
    by_t: dict[str, dict[str, Any]] = {}
    for m in meas_store.list_measurements(slug):
        key = m.t_start.isoformat()
        bucket = by_t.setdefault(
            key,
            {"t_start": m.t_start, "performance_id": None, "acoustic": [],
             "half": None, "pwm_us": None},
        )
        if isinstance(m, PerformanceMeasurementMeta):
            bucket["performance_id"] = m.id
            bucket["pwm_us"] = m.pwm_setpoint
        elif isinstance(m, AcousticMeasurementMeta):
            bucket["acoustic"].append(
                AcousticInPoint(
                    id=m.id, mic_serial=m.mic_serial,
                    elevation_deg=m.elevation_deg, half=m.half,
                    calibration_file_id=m.calibration_file_id,
                )
            )
            if bucket["half"] is None:
                bucket["half"] = m.half
            if bucket["pwm_us"] is None:
                bucket["pwm_us"] = m.pwm_setpoint

    captures = [c for c in by_t.values() if c["pwm_us"] is not None and c["half"] is not None]

    # 2. Group captures by pwm_us
    by_pwm: dict[int, list[dict]] = {}
    for c in captures:
        by_pwm.setdefault(c["pwm_us"], []).append(c)

    # 3. Within each pwm bucket, greedy-group by compatibility
    out: list[MergedPWMPoint] = []
    for pwm_us in sorted(by_pwm):
        captures_at_pwm = sorted(by_pwm[pwm_us], key=lambda c: c["t_start"])

        # Pre-load perf summaries (None if missing)
        perfs: list[PerformanceSummary | None] = [
            _load_performance_summary(slug, c["performance_id"]) if c["performance_id"] else None
            for c in captures_at_pwm
        ]

        # Greedy first-match grouping
        groups: list[list[int]] = []
        for i in range(len(captures_at_pwm)):
            placed = False
            for g in groups:
                seed = g[0]
                # Captures with no perf can't be compatibility-checked — keep them in singletons.
                if perfs[seed] is None or perfs[i] is None:
                    continue
                if _compatible(perfs[seed], perfs[i], tolerances):
                    g.append(i)
                    placed = True
                    break
            if not placed:
                groups.append([i])

        # 4. Build merged points
        for gi, group in enumerate(groups):
            underlying: list[UnderlyingCapture] = []
            composition: dict[str, int] = {}
            combined_acoustic: list[AcousticInPoint] = []
            group_perfs: list[PerformanceSummary] = []
            for idx in group:
                c = captures_at_pwm[idx]
                half = c["half"]
                composition[half.value] = composition.get(half.value, 0) + 1
                underlying.append(
                    UnderlyingCapture(
                        t_start=c["t_start"].isoformat(),
                        half=half,
                        performance_id=c["performance_id"],
                        acoustic=c["acoustic"],
                        performance_summary=perfs[idx],
                    )
                )
                combined_acoustic.extend(c["acoustic"])
                if perfs[idx] is not None:
                    group_perfs.append(perfs[idx])

            # Dedup by elevation_deg — a mic at 0° in both top and bottom captures
            # records the same operating condition, so we show it once. Drill-down
            # into a specific underlying capture keeps the full per-capture mic list.
            seen_elevs: set[float] = set()
            deduped: list[AcousticInPoint] = []
            for a in combined_acoustic:
                if a.elevation_deg in seen_elevs:
                    continue
                seen_elevs.add(a.elevation_deg)
                deduped.append(a)
            deduped.sort(key=lambda a: -a.elevation_deg)
            combined_acoustic = deduped
            avg_performance = _avg_perf(group_perfs) if group_perfs else None
            out.append(
                MergedPWMPoint(
                    id=f"{pwm_us}-{gi}",
                    pwm_us=pwm_us,
                    composition=composition,
                    underlying=underlying,
                    acoustic=combined_acoustic,
                    avg_performance=avg_performance,
                )
            )

    return out


# ----- FFT ----------------------------------------------------------------


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
