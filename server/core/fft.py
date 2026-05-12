"""Welch power spectral density → magnitude dB.

Uses scipy.signal.welch which averages overlapping windowed segments. For drone
noise (broadband, periodic blade-pass tones) Welch gives much cleaner spectra
than a single windowed FFT.

Output is `10 * log10(psd + epsilon)` — power spectral density in dB/Hz reference.
For float32 audio in [-1, 1] this is dBFS/Hz; downstream calibration adds the
UMIK-2 correction curve to convert toward dBSPL.
"""

import numpy as np
from scipy.signal import welch


def compute_fft(
    audio: np.ndarray,
    sample_rate: int,
    *,
    window: str = "hann",
    size: int = 4096,
    overlap: float = 0.5,
) -> tuple[np.ndarray, np.ndarray]:
    if len(audio) < 16:
        return np.array([0.0]), np.array([-200.0])

    nperseg = min(size, len(audio))
    noverlap = int(nperseg * overlap)

    freq, psd = welch(
        audio,
        fs=sample_rate,
        window=window,
        nperseg=nperseg,
        noverlap=noverlap,
        scaling="density",
    )
    mag_db = 10.0 * np.log10(psd + 1e-20)
    return freq, mag_db
