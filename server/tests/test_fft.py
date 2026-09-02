import numpy as np
import pytest

from server.core.calibration import (
    CALIBRATOR_REFERENCE_SPL_DB,
    UmikCalibration,
    apply_calibration_to_spectrum,
    is_absolute_spl,
)
from server.core.fft import compute_fft


def test_silence_returns_very_low_db():
    audio = np.zeros(4096, dtype=np.float32)
    freq, mag = compute_fft(audio, 48000)
    assert len(freq) == 2049
    assert mag.max() < -150


def test_sine_peaks_near_target_frequency():
    sr = 48000
    n = 16384
    target = 1000.0
    t = np.arange(n) / sr
    audio = (0.5 * np.sin(2 * np.pi * target * t)).astype(np.float32)

    freq, mag = compute_fft(audio, sr, size=4096)
    peak_idx = int(np.argmax(mag))
    peak_freq = freq[peak_idx]
    assert abs(peak_freq - target) < 30


def test_short_audio_returns_stub():
    audio = np.zeros(8, dtype=np.float32)
    freq, mag = compute_fft(audio, 48000)
    assert len(freq) == 1
    assert mag[0] < -100


def test_response_curve_is_subtracted_not_added():
    """The cal file holds the mic's own gain response, so it comes OFF.

    REW, whose format this is: "It should contain the actual gain (and
    optionally phase) response of the meter or microphone at the frequencies
    given, these will then be subtracted from subsequent measurements."
    A mic reading +2 dB hot at 100 Hz must have 2 dB removed, not added.
    """
    freq = np.array([100.0, 1000.0, 10000.0])
    mag_db = np.array([-50.0, -50.0, -50.0])
    cal = UmikCalibration(
        serial="test",
        sens_factor_db=None,
        again_db=None,
        freq_hz=np.array([100.0, 1000.0, 10000.0]),
        gain_db=np.array([2.0, -1.0, 5.0]),
    )
    out = apply_calibration_to_spectrum(freq, mag_db, cal)
    np.testing.assert_array_equal(out, [-52.0, -49.0, -55.0])


def test_calibration_clamps_outside_range():
    freq = np.array([10.0, 100.0, 30000.0])
    mag_db = np.array([-50.0, -50.0, -50.0])
    cal = UmikCalibration(
        serial="t",
        sens_factor_db=None,
        again_db=None,
        freq_hz=np.array([100.0, 10000.0]),
        gain_db=np.array([2.0, 5.0]),
    )
    out = apply_calibration_to_spectrum(freq, mag_db, cal)
    # 10 Hz clamps to gain_db[0]=2.0, 30000 Hz clamps to gain_db[-1]=5.0,
    # and the response is subtracted.
    assert out[0] == -52.0
    assert out[2] == -55.0


def _band_power_db(freq: np.ndarray, mag_db: np.ndarray, low: float, high: float) -> float:
    """Mirror of the frontend `bandPowerDb` — integrate PSD over a band."""
    sel = (freq >= low) & (freq <= high)
    df = np.diff(freq, append=freq[-1] + (freq[-1] - freq[-2]))
    total = float(np.sum(10.0 ** (mag_db[sel] / 10.0) * df[sel]))
    return 10.0 * np.log10(total)


def test_full_scale_sine_integrates_to_minus_3_01_dbfs():
    """REW's convention: a full-scale sine is -3.01 dBFS, not 0 dBFS.

    The Sens Factor is quoted against that convention, so our Welch density +
    band integration must reproduce it with no extra fudge factor.
    """
    sr = 48000
    t = np.arange(sr) / sr
    audio = np.sin(2 * np.pi * 1000.0 * t).astype(np.float64)
    freq, mag_db = compute_fft(audio, sr, size=4096)
    assert _band_power_db(freq, mag_db, 0.0, sr / 2) == pytest.approx(-3.01, abs=0.05)


def test_sens_factor_converts_to_absolute_spl():
    freq = np.array([1000.0])
    mag_db = np.array([-40.0])
    cal = UmikCalibration(
        serial="t",
        sens_factor_db=-12.0,
        again_db=18.0,
        freq_hz=np.array([100.0, 10000.0]),
        gain_db=np.array([0.0, 0.0]),
    )
    # -40 dBFS - (-12) + 94 = 66 dB SPL. AGain must NOT enter the sum.
    out = apply_calibration_to_spectrum(freq, mag_db, cal)
    assert out[0] == pytest.approx(66.0)
    assert is_absolute_spl(cal)


def test_sens_factor_offset_stacks_on_response_curve():
    freq = np.array([100.0, 1000.0, 10000.0])
    mag_db = np.array([-50.0, -50.0, -50.0])
    cal = UmikCalibration(
        serial="t",
        sens_factor_db=-1.724,
        again_db=None,
        freq_hz=np.array([100.0, 1000.0, 10000.0]),
        gain_db=np.array([2.0, -1.0, 5.0]),
    )
    out = apply_calibration_to_spectrum(freq, mag_db, cal)
    offset = CALIBRATOR_REFERENCE_SPL_DB - (-1.724)
    # response subtracted, Sens Factor offset added — opposite signs, on purpose
    np.testing.assert_allclose(out, np.array([-52.0, -49.0, -55.0]) + offset)


def test_missing_sens_factor_applies_response_curve_only():
    freq = np.array([1000.0])
    mag_db = np.array([-40.0])
    cal = UmikCalibration(
        serial="t",
        sens_factor_db=None,
        again_db=18.0,
        freq_hz=np.array([100.0, 10000.0]),
        gain_db=np.array([3.0, 3.0]),
    )
    out = apply_calibration_to_spectrum(freq, mag_db, cal)
    assert out[0] == pytest.approx(-43.0)  # -40 - 3, response removed
    assert not is_absolute_spl(cal)


def test_sens_offset_survives_band_integration():
    """A constant dB offset on a per-Hz density shifts the integrated level 1:1."""
    sr = 48000
    t = np.arange(sr) / sr
    audio = (0.1 * np.sin(2 * np.pi * 1000.0 * t)).astype(np.float64)
    freq, mag_db = compute_fft(audio, sr, size=4096)
    cal = UmikCalibration(
        serial="t",
        sens_factor_db=-12.0,
        again_db=None,
        freq_hz=np.array([20.0, 24000.0]),
        gain_db=np.array([0.0, 0.0]),
    )
    raw = _band_power_db(freq, mag_db, 0.0, sr / 2)
    cald = _band_power_db(freq, apply_calibration_to_spectrum(freq, mag_db, cal), 0.0, sr / 2)
    assert cald - raw == pytest.approx(106.0, abs=1e-6)


def test_curve_and_sens_factor_have_opposite_signs():
    """Guard the one thing that is easy to get backwards and hard to notice.

    The two halves of a cal file are different quantities and move the spectrum
    in opposite directions. A mic that reads hot at some frequency must be
    brought DOWN there (response subtracted), while the Sens Factor lifts dBFS
    up to dB SPL (offset added). Getting the curve's sign wrong doubles its
    error instead of removing it — roughly 3.7 dB of fabricated spread across a
    real 11-mic set, which lands straight on directivity.
    """
    freq = np.array([1000.0])
    mag_db = np.array([-50.0])
    hot = UmikCalibration(  # mic reads 4 dB hot here
        serial="t", sens_factor_db=None, again_db=None,
        freq_hz=np.array([100.0, 10000.0]), gain_db=np.array([4.0, 4.0]),
    )
    quiet = UmikCalibration(  # mic reads 4 dB shy here
        serial="t", sens_factor_db=None, again_db=None,
        freq_hz=np.array([100.0, 10000.0]), gain_db=np.array([-4.0, -4.0]),
    )
    assert apply_calibration_to_spectrum(freq, mag_db, hot)[0] == pytest.approx(-54.0)
    assert apply_calibration_to_spectrum(freq, mag_db, quiet)[0] == pytest.approx(-46.0)

    # ...while the Sens Factor raises the level, on a flat curve.
    flat = UmikCalibration(
        serial="t", sens_factor_db=-12.0, again_db=None,
        freq_hz=np.array([100.0, 10000.0]), gain_db=np.array([0.0, 0.0]),
    )
    assert apply_calibration_to_spectrum(freq, mag_db, flat)[0] == pytest.approx(-50.0 + 12.0 + 94.0)
