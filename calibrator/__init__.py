"""Dead-simple single-mic tone capture — usage sketch in calibrator/core.py."""

from .core import (
    SPEAKER_USB_ID,
    SR,
    CalibratorError,
    Mic,
    Speaker,
    acquire_speaker,
    acquire_umik,
    assert_mic_ok,
    assert_speaker_ok,
    assert_tone_stable,
    octave_series,
    save_wav,
    take_octave_series,
    take_sample_at_frequency,
)

__all__ = [
    "SPEAKER_USB_ID",
    "SR",
    "CalibratorError",
    "Mic",
    "Speaker",
    "acquire_speaker",
    "acquire_umik",
    "assert_mic_ok",
    "assert_speaker_ok",
    "assert_tone_stable",
    "octave_series",
    "save_wav",
    "take_octave_series",
    "take_sample_at_frequency",
]
