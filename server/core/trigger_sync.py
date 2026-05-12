"""Trigger-onset synchronization for asynchronous USB audio captures.

Each UMIK-2 has its own ADC clock and is opened as a separate PortAudio stream,
so simultaneous "start" calls land within ~ms of each other but not sample-locked.
We use the sound onset itself as a reference: scan each capture for the first
RMS block over a dBFS threshold, then trim everyone so their triggers align,
keeping `preroll_samples` worth of pre-onset audio for attack transients.

Mics that never trigger (silent) are kept but are *not* aligned — they're trimmed
to `min_length` from the start, matching the JS implementation. Throwing them
out would lose information; misaligning them is a smaller cost than dropping a mic.

Port of `src/audio/triggerSync.ts`.
"""

import math

import numpy as np


def block_rms_db(samples: np.ndarray, offset: int, block_size: int) -> float:
    end = min(offset + block_size, len(samples))
    if end <= offset:
        return -math.inf
    block = samples[offset:end].astype(np.float64, copy=False)
    rms = float(np.sqrt(np.mean(block * block)))
    if rms == 0.0:
        return -math.inf
    return 20.0 * math.log10(rms)


def find_trigger_index(samples: np.ndarray, threshold_db: float, block_size: int) -> int:
    for offset in range(0, len(samples), block_size):
        if block_rms_db(samples, offset, block_size) >= threshold_db:
            return offset
    return -1


def align_captures(
    audios: list[np.ndarray],
    *,
    threshold_db: float = -40.0,
    block_size: int = 128,
    preroll_samples: int = 480,
) -> list[np.ndarray]:
    if not audios:
        return audios

    triggers = [find_trigger_index(a, threshold_db, block_size) for a in audios]

    if all(t == -1 for t in triggers):
        return audios

    starts = [max(0, t - preroll_samples) if t != -1 else 0 for t in triggers]
    remaining = [len(a) - s for a, s in zip(audios, starts, strict=True)]
    min_len = min(remaining)
    return [a[s : s + min_len] for a, s in zip(audios, starts, strict=True)]
