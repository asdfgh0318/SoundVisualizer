import math
from datetime import UTC, datetime, timedelta

import numpy as np
from fastapi import APIRouter, Request

from server.api.schemas import (
    AcousticMeasurementMeta,
    Key,
    MeasurementHalf,
    PerformanceMeasurementMeta,
)
from server.core.capture_orchestrator import CaptureRunRequest
from server.core.wav import write_wav_float32
from server.store import keys as keys_store
from server.store import measurements as meas_store
from server.store.paths import measurement_dir

router = APIRouter(prefix="/dev", tags=["dev"])


_PERF_CSV_HEADER = (
    b"t_offset_s,thrust_n,torque_nm,current_a,voltage_v,rpm,"
    b"temp0_c,temp1_c,temp2_c,vibration\n"
)


# ---- Drone-noise synthesis -------------------------------------------------
# Models propeller aerodynamic noise per the standard breakdown:
#   - tonal BPF (blade-pass frequency) and its harmonics (highly directional;
#     max in the rotor plane, ~0° elevation; null on the axis ±90°)
#   - "spreaded continuous noise" — low-frequency hump around BPF
#   - high-frequency broadband — gradually decaying noise band 1.5-5 kHz,
#     weakly directional
# Reference: classic prop-noise textbook spectrum (BPF tone + harmonics +
# broadband HF).


def _drone_directivity(elevation_deg: float, strength: float) -> float:
    """Per-component directivity factor.

    strength=1.0 → fully cosine-shaped (max at 0° equator, min at ±90° pole).
    strength=0.0 → isotropic.
    Intermediate values blend.
    """
    base = abs(math.cos(math.radians(elevation_deg)))
    return (1.0 - strength) + strength * base


def _pink_noise(rng: np.random.Generator, n: int) -> np.ndarray:
    """Pink (1/f) noise, normalized to unit RMS."""
    white = rng.standard_normal(n).astype(np.float64)
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n)
    freqs[0] = 1e-6
    fft = fft / np.sqrt(freqs)
    out = np.fft.irfft(fft, n)
    rms = float(np.sqrt(np.mean(out * out)))
    return out / max(rms, 1e-12)


def _gaussian_band_noise(
    rng: np.random.Generator,
    n: int,
    sr: int,
    center_hz: float,
    width_hz: float,
) -> np.ndarray:
    """White noise FFT-shaped by a Gaussian bandpass centered at `center_hz`,
    half-width `width_hz`. Returns unit-RMS array."""
    white = rng.standard_normal(n).astype(np.float64)
    fft = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(n, d=1.0 / sr)
    shape = np.exp(-((freqs - center_hz) / max(width_hz, 1.0)) ** 2)
    fft = fft * shape
    out = np.fft.irfft(fft, n)
    rms = float(np.sqrt(np.mean(out * out)))
    return out / max(rms, 1e-12)


def _synth_drone_wav(
    rpm: float,
    elevation_deg: float,
    sr: int = 48000,
    duration_s: float = 1.0,
    n_blades: int = 2,
) -> np.ndarray:
    """Synthesize a propeller-noise-like signal at the given operating point."""
    n = max(int(sr * duration_s), 16)
    seed = int(abs(rpm) * 100 + (elevation_deg + 90) * 13) % (2**31)
    rng = np.random.default_rng(seed)
    t = np.arange(n) / sr

    bpf = rpm * n_blades / 60.0  # blade-pass fundamental in Hz
    nyq = sr / 2.0

    # Directivity factors per component
    dir_tonal = _drone_directivity(elevation_deg, strength=0.85)  # strong
    dir_lf = _drone_directivity(elevation_deg, strength=0.55)     # medium
    dir_hf = _drone_directivity(elevation_deg, strength=0.30)     # weak

    # 1) Low background pink noise (the always-on broadband floor)
    audio = 0.025 * dir_lf * _pink_noise(rng, n)

    # 2) Tonal BPF + harmonics — each is a sine with random phase so adjacent
    # captures don't beat suspiciously identically. Amplitude decays per harmonic.
    if 20.0 < bpf < nyq - 20:
        for h in range(1, 12):
            f = bpf * h
            if f > nyq - 50:
                break
            amp = 0.35 * (0.55 ** (h - 1)) * dir_tonal
            phase = float(rng.uniform(0, 2 * math.pi))
            audio += amp * np.sin(2 * math.pi * f * t + phase)

    # 3) Low-frequency continuous noise hump around BPF (the "spreaded" bump)
    if bpf > 20:
        audio += 0.07 * dir_lf * _gaussian_band_noise(
            rng, n, sr, center_hz=bpf * 0.8, width_hz=max(bpf * 0.6, 80.0)
        )

    # 4) High-frequency broadband bump (2-5 kHz centered, wide)
    audio += 0.045 * dir_hf * _gaussian_band_noise(
        rng, n, sr, center_hz=3000.0, width_hz=1800.0
    )

    # Prevent clipping
    peak = float(np.max(np.abs(audio)))
    if peak > 0.95:
        audio *= 0.95 / peak

    return audio.astype(np.float32)


# ---- Performance telemetry CSV --------------------------------------------


def _synth_perf_csv(
    thrust_n: float,
    torque_nm: float,
    current_a: float,
    rpm: float,
    duration_s: float = 1.0,
) -> bytes:
    n = max(int(duration_s * 33), 1)
    rows = [_PERF_CSV_HEADER.decode()]
    for i in range(n):
        t = i * 0.03
        jitter = (i % 5) * 0.01
        rows.append(
            f"{t:.3f},{thrust_n + jitter:.4f},{torque_nm:.4f},"
            f"{current_a + jitter * 0.5:.4f},16.05,{rpm:.1f},"
            f"35.0,32.0,30.0,40\n"
        )
    return ("".join(rows)).encode()


def _synth_for_pwm(pwm_us: int) -> tuple[float, float, float, float]:
    """Map PWM (1000..2000) → (thrust_N, torque_Nm, current_A, rpm)."""
    p = max(0.0, min(1.0, (pwm_us - 1000) / 1000.0))
    thrust = 0.5 + 19.5 * (p ** 1.4)
    torque = 0.05 + 0.95 * (p ** 1.3)
    current = 0.3 + 14.7 * (p ** 1.5)
    rpm = 1500 + 18500 * p
    return thrust, torque, current, rpm


# ---- Endpoints -------------------------------------------------------------


@router.post("/seed")
def seed() -> dict[str, list[str] | str]:
    """Create a demo key with two PWM steps x top+bottom, four mics each."""
    key = Key(motor="T-Motor F60", propeller="HQProp 5x4", shroud="none", notes="seed")
    if not keys_store.get_key(key.slug):
        keys_store.create_key(key)

    base = datetime.now(UTC).replace(microsecond=0)
    elevations = [0.0, 30.0, 60.0, 90.0]
    serials = [f"81000{i:02d}" for i in range(1, 5)]
    sample_rate = 48000

    pwm_steps = [(1200, 1000), (1800, 1000)]
    halves: list[MeasurementHalf] = [MeasurementHalf.TOP, MeasurementHalf.BOTTOM]

    perf_ids: list[str] = []
    acoustic_ids: list[str] = []

    for half_idx, half in enumerate(halves):
        for step_idx, (pwm, rec_ms) in enumerate(pwm_steps):
            t_start = base + timedelta(seconds=10 * (half_idx * len(pwm_steps) + step_idx))
            t_end = t_start + timedelta(milliseconds=rec_ms)
            thrust, torque, current, rpm = _synth_for_pwm(pwm)
            duration_s = rec_ms / 1000.0

            perf_meta = PerformanceMeasurementMeta(
                t_start=t_start, t_end=t_end, pwm_setpoint=pwm
            )
            perf_saved = meas_store.create_measurement(
                key.slug,
                perf_meta,
                telemetry_csv=_synth_perf_csv(thrust, torque, current, rpm, duration_s),
            )
            perf_ids.append(perf_saved.id)

            for elev, serial in zip(elevations, serials, strict=True):
                signed_elev = elev if half == MeasurementHalf.TOP else -elev
                meta = AcousticMeasurementMeta(
                    t_start=t_start, t_end=t_end, pwm_setpoint=pwm,
                    mic_serial=serial, elevation_deg=signed_elev, half=half,
                    sample_rate=sample_rate,
                )
                saved = meas_store.create_measurement(key.slug, meta)
                wav = _synth_drone_wav(rpm, signed_elev, sr=sample_rate, duration_s=duration_s)
                write_wav_float32(
                    measurement_dir(key.slug, saved.id) / "audio.wav", wav, sample_rate
                )
                acoustic_ids.append(saved.id)

    return {"key": key.slug, "performance": perf_ids, "acoustic": acoustic_ids}


@router.post("/fake_capture", status_code=201)
def fake_capture(
    body: CaptureRunRequest, request: Request
) -> dict[str, str | list[str]]:
    """Take a real CaptureRunRequest body but skip Tyto + mic acquisition.

    Synthesizes plausible drone-noise WAVs + telemetry CSV per PWM step.
    Also fires the research-tree push if the request carries a node id —
    fake-mode bypasses the orchestrator so the on_completed hook there never
    runs, and we want the same UX (linked node updated) for fake captures.
    """
    key = Key(**body.key.model_dump())
    if not keys_store.get_key(key.slug):
        keys_store.create_key(key)

    base = datetime.now(UTC)
    measurement_ids: list[str] = []

    for step_idx, step in enumerate(body.pwm_steps):
        t_start = base + timedelta(seconds=5 * step_idx)
        t_end = t_start + timedelta(milliseconds=step.recording_ms)
        duration_s = step.recording_ms / 1000.0
        thrust, torque, current, rpm = _synth_for_pwm(step.pwm_us)

        perf_meta = PerformanceMeasurementMeta(
            t_start=t_start, t_end=t_end, pwm_setpoint=step.pwm_us
        )
        perf_saved = meas_store.create_measurement(
            key.slug,
            perf_meta,
            telemetry_csv=_synth_perf_csv(thrust, torque, current, rpm, duration_s),
        )
        measurement_ids.append(perf_saved.id)

        for mic in body.mics:
            meta = AcousticMeasurementMeta(
                t_start=t_start, t_end=t_end, pwm_setpoint=step.pwm_us,
                mic_serial=mic.serial, elevation_deg=mic.elevation_deg,
                half=body.half, sample_rate=body.sample_rate,
                calibration_file_id=mic.calibration_file_id,
            )
            saved = meas_store.create_measurement(key.slug, meta)
            wav = _synth_drone_wav(
                rpm, mic.elevation_deg, sr=body.sample_rate, duration_s=duration_s
            )
            write_wav_float32(
                measurement_dir(key.slug, saved.id) / "audio.wav", wav, body.sample_rate
            )
            measurement_ids.append(saved.id)

    # Mirror the orchestrator's on_completed hook for the fake-capture path.
    if body.research_tree_node_id:
        cfg = getattr(request.app.state, "config", None)
        trees = [t for t in cfg.research_trees if t.enabled] if cfg is not None else []
        if trees:
            from server.api.research_tree import push_node_update

            base = trees[0].public_url.rstrip("/")
            results_url = (
                f"{base}/results#key={key.slug}" if base else f"/results#key={key.slug}"
            )
            push_node_update(
                cfg.research_trees,
                body.research_tree_node_id,
                {"soundVisualizerLink": results_url, "status": "in-progress"},
            )

    return {"key": key.slug, "measurement_ids": measurement_ids}
