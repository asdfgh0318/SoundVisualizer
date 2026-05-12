from pathlib import Path

import numpy as np
from scipy.io import wavfile


def write_wav_float32(path: Path, audio: np.ndarray, sample_rate: int) -> None:
    """Write float32 IEEE_FLOAT WAV. Preserves precision for downstream FFT/calibration."""
    if audio.ndim != 1:
        raise ValueError(f"expected mono audio, got shape {audio.shape}")
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32)
    wavfile.write(str(path), sample_rate, audio)


def read_wav_float32(path: Path) -> tuple[int, np.ndarray]:
    """Returns (sample_rate, mono float32 audio). Converts integer PCM to float [-1, 1]."""
    sr, data = wavfile.read(str(path))
    if data.ndim > 1:
        data = data[:, 0]
    if data.dtype == np.float32:
        return sr, data
    if data.dtype == np.float64:
        return sr, data.astype(np.float32)
    if np.issubdtype(data.dtype, np.integer):
        max_val = float(np.iinfo(data.dtype).max)
        return sr, (data.astype(np.float32) / max_val)
    raise ValueError(f"unsupported WAV dtype: {data.dtype}")
