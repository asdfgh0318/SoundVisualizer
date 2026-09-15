"""Dead-simple single-mic tone capture — usage sketch in calibrator/core.py."""

from .core import (
    SPEAKER_USB_ID,
    SR,
    THIRD_OCTAVE_HZ,
    CalibratorError,
    Mic,
    Speaker,
    acquire_speaker,
    acquire_umik,
    assert_mic_ok,
    assert_speaker_ok,
    assert_tone_stable,
    log_series,
    octave_series,
    save_wav,
    take_octave_series,
    take_sample_at_frequency,
    third_octave,
)
from .postprocess import merge_curve, relative_curves, write_rew_curve
from .session import capture_capsule

__all__ = [
    "SPEAKER_USB_ID",
    "SR",
    "THIRD_OCTAVE_HZ",
    "CalibratorError",
    "Mic",
    "Speaker",
    "acquire_speaker",
    "acquire_umik",
    "assert_mic_ok",
    "assert_speaker_ok",
    "assert_tone_stable",
    "capture_capsule",
    "log_series",
    "merge_curve",
    "octave_series",
    "relative_curves",
    "save_wav",
    "take_octave_series",
    "take_sample_at_frequency",
    "third_octave",
    "write_rew_curve",
]
