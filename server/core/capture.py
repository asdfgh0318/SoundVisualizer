"""Multi-stream simultaneous audio capture.

Opens N independent PortAudio InputStreams, starts them tightly, captures for
`duration_seconds`, stops them. Each stream's callback appends frames to a
per-stream buffer. UMIK-2s have independent ADC clocks → simultaneous starts
land within ~ms of each other; trigger-onset sync afterwards aligns them.
"""

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

    streams = [
        sd.InputStream(
            device=spec.device_index,
            channels=spec.channels,
            samplerate=spec.sample_rate,
            dtype="float32",
            callback=make_callback(i),
        )
        for i, spec in enumerate(specs)
    ]

    try:
        for s in streams:
            s.start()
        time.sleep(duration_seconds)
    finally:
        for s in streams:
            try:
                s.stop()
            finally:
                s.close()

    out: list[CaptureResult] = []
    for i, spec in enumerate(specs):
        with locks[i]:
            chunks = list(buffers[i])
        audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.float32)
        out.append(CaptureResult(serial=spec.serial, sample_rate=spec.sample_rate, audio=audio))
    return out
