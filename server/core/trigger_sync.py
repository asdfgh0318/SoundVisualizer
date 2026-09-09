"""Trigger-onset synchronization for asynchronous USB audio captures.

Each UMIK-2 has its own ADC clock and is opened as a separate PortAudio stream,
so simultaneous "start" calls land within ~ms of each other but not sample-locked.
We use the sound onset itself as a reference: scan each capture for the first
RMS block over a dBFS threshold, then trim everyone so their triggers align,
keeping `preroll_samples` worth of pre-onset audio for attack transients.

Mics that never trigger (silent) are kept but are *not* aligned — they're trimmed
to `min_length` from the start, matching the JS implementation. Throwing them
out would lose information; misaligning them is a smaller cost than dropping a mic.

Alignment is only applied when the triggers describe a real onset inside the
recording: every mic triggered, none already above threshold in its first block,
and all triggers within `max_lag_samples` of each other. A source that is already
running when the recording starts (a stepped PWM run) produces triggers at 0 for
the loud mics and, for a mic hovering just below threshold, a late trigger at some
transient; cropping everyone to that tail silently threw away most of the
PWM-1800 captures of the Sept 2026 runs (issue #13). Such captures are returned
untouched.

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


def is_genuine_onset(triggers: list[int], max_lag_samples: int) -> bool:
    """True when every mic triggered, none was already loud in its first block, and
    the triggers sit within `max_lag_samples` of each other (independent USB clocks
    start within milliseconds; anything wider is not the same onset)."""
    if any(t <= 0 for t in triggers):
        return False
    return max(triggers) - min(triggers) <= max_lag_samples


def align_captures(
    audios: list[np.ndarray],
    *,
    threshold_db: float = -40.0,
    block_size: int = 128,
    preroll_samples: int = 480,
    max_lag_samples: int = 4800,
) -> list[np.ndarray]:
    if not audios:
        return audios

    triggers = [find_trigger_index(a, threshold_db, block_size) for a in audios]

    if all(t == -1 for t in triggers):
        return audios
    if not is_genuine_onset(triggers, max_lag_samples):
        return audios

    starts = [max(0, t - preroll_samples) if t != -1 else 0 for t in triggers]
    remaining = [len(a) - s for a, s in zip(audios, starts, strict=True)]
    min_len = min(remaining)
    return [a[s : s + min_len] for a, s in zip(audios, starts, strict=True)]
