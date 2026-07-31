"""Sound Quality Metrics (SQM) and Psychoacoustic Annoyance (PA).

Formulas: see docs/psychoacoustics_report.pdf (Vaiuso et al., arXiv:2410.22208).

Pipeline:
  - Loudness (sone): ISO 532-1 Zwicker stationary, via `mosqito.loudness_zwst`.
  - Sharpness (acum): DIN 45692, via `mosqito.sharpness_din_from_loudness`.
  - Roughness (asper): Daniel-Weber, via `mosqito.roughness_dw`; we take the mean
    across the time-series frames it returns.
  - Fluctuation strength (vacil): NOT computed — set to 0.0. Per the reference
    paper drone hover fluctuation is ~0.01 vacil which is essentially noise
    floor and contributes <0.1% to PA. Revisit once NOR-145 lands and we can
    sanity-check against its built-in reading.
  - PA: Zwicker formula, computed manually from L/S/R/F.

`mosqito` expects acoustic pressure in Pa, so callers pass the UMIK Sens Factor
derived scalar (`calibration.pascals_per_full_scale`) and we scale the float32
[-1, 1] samples by it — loudness and sharpness are level-dependent, so without
it the numbers are not ISO-comparable. `pa_per_full_scale=None` is the explicit
opt-out (no cal file, or a cal file without a Sens Factor); the resulting metrics
carry `absolute=False` and are only good for relative comparison — the error is
nonlinear, not an offset you can subtract afterwards.

Only the scalar is applied. The mic's per-frequency response curve — which the
FFT path does interpolate — is NOT applied here: correcting a time signal means
FIR-filtering it, which is separate work. UMIK-2 curves are within ~±2 dB over
the drone band, so this is an approximation, not an exact ISO 532-1 input.
"""

import math

import numpy as np
from mosqito.sq_metrics import (
    loudness_zwst,
    roughness_dw,
    sharpness_din_from_loudness,
)
from pydantic import BaseModel


class PsychoacousticMetrics(BaseModel):
    loudness_sone: float
    sharpness_acum: float
    roughness_asper: float
    fluctuation_vacil: float
    annoyance: float
    # Carried through so the UI can flag the F=0 caveat.
    fluctuation_assumed_zero: bool = True
    # Whether the audio was scaled to Pa — i.e. whether sone/acum/PA mean anything
    # in ISO terms. Mirrors FFTResponse.absolute_spl.
    absolute: bool


def psychoacoustic_annoyance(
    loudness_sone: float,
    sharpness_acum: float,
    roughness_asper: float,
    fluctuation_vacil: float,
) -> float:
    """Zwicker PA = N5 * (1 + sqrt(wS^2 + wFR^2)).

    Stationary loudness substituted for N5 — acceptable for our short clips.
    """
    N = loudness_sone
    S = sharpness_acum
    R = roughness_asper
    F = fluctuation_vacil
    if N <= 0:
        return 0.0
    w_S = (S - 1.75) * 0.25 * math.log10(N + 10) if S > 1.75 else 0.0
    w_FR = (2.18 / (N ** 0.4)) * (0.4 * F + 0.6 * R)
    return float(N * (1.0 + math.sqrt(w_S ** 2 + w_FR ** 2)))


def compute_metrics(
    audio: np.ndarray,
    sample_rate: int,
    *,
    pa_per_full_scale: float | None,
) -> PsychoacousticMetrics:
    """Compute all five metrics for a mono audio buffer.

    `pa_per_full_scale` is keyword-only and has no default so no caller can
    silently end up with arbitrary-scale loudness; pass None to opt out.
    """
    absolute = pa_per_full_scale is not None
    if audio.ndim > 1:
        audio = audio[:, 0]
    if audio.size < int(sample_rate * 0.2):
        # Too short for stable loudness — return zeros rather than crash.
        return PsychoacousticMetrics(
            loudness_sone=0.0, sharpness_acum=0.0,
            roughness_asper=0.0, fluctuation_vacil=0.0,
            annoyance=0.0, absolute=absolute,
        )

    audio64 = audio.astype(np.float64)
    if pa_per_full_scale is not None:
        audio64 = audio64 * pa_per_full_scale
    N, N_spec, _bark = loudness_zwst(audio64, sample_rate)
    L = float(N)
    S = float(sharpness_din_from_loudness(N, N_spec))

    # roughness_dw returns (R_time, R_specific, bark, time_axis)
    R_time, _, _, _ = roughness_dw(audio64, sample_rate)
    R = float(np.mean(R_time))

    F = 0.0  # see module docstring
    PA = psychoacoustic_annoyance(L, S, R, F)

    return PsychoacousticMetrics(
        loudness_sone=L,
        sharpness_acum=S,
        roughness_asper=R,
        fluctuation_vacil=F,
        annoyance=PA,
        fluctuation_assumed_zero=True,
        absolute=absolute,
    )
