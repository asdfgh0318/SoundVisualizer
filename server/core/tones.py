"""Blade-passage tones versus broadband, from a capture's own spectrum.

The telemetry carries no RPM, so the blade-passage frequency (BPF) is read from
the audio: the most prominent peak in `lo..hi` whose 2nd and 3rd harmonics are
also present. From it: the level of each BPF harmonic, and third-octave levels
with every shaft harmonic (multiples of BPF/2) notched out. A reflection or a
room mode bends everything at a frequency; a distorted rotor inflow bends the
tones only, so the two views are reported separately (issue #12).

The estimators are the ones validated on the Sept 2026 horizontal runs in
scripts/arc_validation_diagnostics.py; keep them in step.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.signal import find_peaks

THIRD_OCTAVE_CENTRES: tuple[float, ...] = tuple(
    125 * 2 ** (i / 3) for i in range(19)
)  # 125 Hz .. 8 kHz
DEFAULT_HARMONICS = 6


@dataclass(frozen=True)
class ToneLevel:
    harmonic: int
    frequency_hz: float
    level_db: float


@dataclass(frozen=True)
class ToneAnalysis:
    bpf_hz: float | None
    tones: list[ToneLevel]
    band_centres_hz: list[float]
    broadband_bands_db: list[float]  # tones notched; NaN where a band has no clean bins

    @property
    def tone_ok(self) -> bool:
        return self.bpf_hz is not None


def _parabolic_peak(f: np.ndarray, m: np.ndarray, k: int) -> float:
    if not 1 <= k < len(m) - 1:
        return float(f[k])
    y0, y1, y2 = m[k - 1], m[k], m[k + 1]
    denom = y0 - 2 * y1 + y2
    if abs(denom) < 1e-9:
        return float(f[k])
    return float(f[k] + 0.5 * (y0 - y2) / denom * (f[1] - f[0]))


def find_bpf(
    freq: np.ndarray,
    mag_db: np.ndarray,
    *,
    lo_hz: float = 100.0,
    hi_hz: float = 320.0,
    prominence_db: float = 8.0,
) -> float | None:
    """Fundamental of the blade-passage comb, or None if no candidate peak in
    lo..hi has its 2nd and 3rd harmonics standing >= prominence_db above their
    surroundings. `mag_db` may be one spectrum or the mean over several mics."""
    df = float(freq[1] - freq[0])
    # peaks are found on a window twice as wide as lo..hi so that a fundamental near
    # hi_hz keeps its full prominence (a peak at the window edge is otherwise measured
    # against the edge and dropped), then restricted to lo..hi
    wide = (freq > lo_hz / 2) & (freq < 2 * hi_hz)
    idx = np.where(wide)[0]
    if len(idx) < 3:
        return None
    peaks, props = find_peaks(mag_db[wide], prominence=prominence_db)
    keep = [(o, p) for o, p in enumerate(peaks) if lo_hz < freq[idx[p]] < hi_hz]
    for o, _p in sorted(keep, key=lambda t: -props["prominences"][t[0]]):
        k = int(idx[peaks[o]])
        f0 = _parabolic_peak(freq, mag_db, k)
        harmonics_present = 0
        for h in (2, 3):
            win = np.abs(freq - h * f0) <= 2 * df
            near = (np.abs(freq - h * f0) > 4 * df) & (np.abs(freq - h * f0) <= 12 * df)
            if (
                win.any()
                and near.any()
                and mag_db[win].max() - np.median(mag_db[near]) > prominence_db
            ):
                harmonics_present += 1
        if harmonics_present == 2:
            estimates, weights = [], []
            for h in range(1, 5):
                win = np.abs(freq - h * f0) <= 2 * df
                if not win.any():
                    break
                kk = int(np.where(win)[0][np.argmax(mag_db[win])])
                estimates.append(_parabolic_peak(freq, mag_db, kk) / h)
                weights.append(h)
            return float(np.average(estimates, weights=weights))
    return None


def tone_levels(
    freq: np.ndarray, mag_db: np.ndarray, bpf_hz: float, *, harmonics: int = DEFAULT_HARMONICS
) -> list[ToneLevel]:
    """Level of each BPF harmonic: the PSD summed over +-3 bins (the Hann main lobe)."""
    df = float(freq[1] - freq[0])
    lin = 10 ** (mag_db / 10)
    out = []
    for h in range(1, harmonics + 1):
        fh = h * bpf_hz
        if fh >= freq[-1]:
            break
        sel = np.abs(freq - fh) <= 3 * df
        out.append(ToneLevel(h, fh, float(10 * np.log10(lin[sel].sum() * df + 1e-30))))
    return out


def notched_band_levels(
    freq: np.ndarray,
    mag_db: np.ndarray,
    bpf_hz: float | None,
    *,
    centres: tuple[float, ...] = THIRD_OCTAVE_CENTRES,
    notch_bins_bpf: int = 3,
    notch_bins_shaft: int = 2,
) -> list[float]:
    """Third-octave levels with every multiple of BPF/2 notched. The kept bins are
    scaled up by the band's bin count so the result estimates the whole band's
    broadband level. NaN where the notches leave nothing (coarse FFT at low bands)."""
    df = float(freq[1] - freq[0])
    lin = 10 ** (mag_db / 10)
    mask = np.ones_like(freq, dtype=bool)
    if bpf_hz is not None:
        k = 1
        while k * bpf_hz / 2 < centres[-1] * 2 ** (1 / 6) + 4 * df:
            w = notch_bins_bpf if k % 2 == 0 else notch_bins_shaft
            mask &= np.abs(freq - k * bpf_hz / 2) > w * df
            k += 1
    out = []
    for fc in centres:
        band = (freq >= fc / 2 ** (1 / 6)) & (freq < fc * 2 ** (1 / 6))
        kept = band & mask
        if not kept.any():
            out.append(float("nan"))
            continue
        out.append(float(10 * np.log10(lin[kept].sum() * df * band.sum() / kept.sum() + 1e-30)))
    return out


def analyse(
    freq: np.ndarray, mag_db: np.ndarray, *, harmonics: int = DEFAULT_HARMONICS
) -> ToneAnalysis:
    bpf = find_bpf(freq, mag_db)
    tones = tone_levels(freq, mag_db, bpf, harmonics=harmonics) if bpf is not None else []
    return ToneAnalysis(
        bpf_hz=bpf,
        tones=tones,
        band_centres_hz=list(THIRD_OCTAVE_CENTRES),
        broadband_bands_db=notched_band_levels(freq, mag_db, bpf),
    )
