"""Multi-stream simultaneous audio capture.

Opens N independent PortAudio InputStreams, starts them tightly, captures for
`duration_seconds`, stops them. Each stream's callback appends frames to a
per-stream buffer. UMIK-2s have independent ADC clocks → simultaneous starts
land within ~ms of each other; trigger-onset sync afterwards aligns them.
"""

import contextlib
import time
from dataclasses import dataclass
from threading import Lock
from typing import Any

import numpy as np
import sounddevice as sd


@dataclass
class MicCaptureSpec:
    serial: str
    device_index: int
    sample_rate: int = 48000
    channels: int = 1


@dataclass
class CaptureResult:
    serial: str
    sample_rate: int
    audio: np.ndarray  # float32 mono


def capture_simultaneous(
    specs: list[MicCaptureSpec],
    duration_seconds: float,
) -> list[CaptureResult]:
    if not specs:
        return []

    buffers: list[list[np.ndarray]] = [[] for _ in specs]
    locks = [Lock() for _ in specs]

    def make_callback(i: int):
        def cb(indata: np.ndarray, frames: int, _time: Any, status: sd.CallbackFlags) -> None:
            if status:
                # input overflow / underflow — log and continue. Trigger sync is robust to gaps.
                pass
            with locks[i]:
                buffers[i].append(indata[:, 0].copy())

        return cb

    # Open inside the try: if one device is unavailable, the ones already opened
    # must still be closed. Constructing the whole list first leaks every stream
    # opened before the failure, and those handles keep holding the ALSA devices
    # — so the next capture fails with the same "Device unavailable" on mics that
    # are physically fine, until the service is restarted.
    streams: list[sd.InputStream] = []
    try:
        for i, spec in enumerate(specs):
            streams.append(
                sd.InputStream(
                    device=spec.device_index,
                    channels=spec.channels,
                    samplerate=spec.sample_rate,
                    dtype="float32",
                    callback=make_callback(i),
                )
            )
        for s in streams:
            s.start()
        time.sleep(duration_seconds)
    finally:
        for s in streams:
            # A stream that failed to start must not block closing the rest.
            with contextlib.suppress(Exception):
                s.stop()
            with contextlib.suppress(Exception):
                s.close()

    out: list[CaptureResult] = []
    for i, spec in enumerate(specs):
        with locks[i]:
            chunks = list(buffers[i])
        audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.float32)
        out.append(CaptureResult(serial=spec.serial, sample_rate=spec.sample_rate, audio=audio))
    return out
