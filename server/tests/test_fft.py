import numpy as np

from server.core.calibration import UmikCalibration, apply_calibration_to_spectrum
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


def test_calibration_correction_added_to_spectrum():
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
    np.testing.assert_array_equal(out, [-48.0, -51.0, -45.0])


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
    # 10 Hz clamps to gain_db[0]=2.0, 30000 Hz clamps to gain_db[-1]=5.0
    assert out[0] == -48.0
    assert out[2] == -45.0
