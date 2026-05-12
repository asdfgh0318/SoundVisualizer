import numpy as np

from server.core.wav import read_wav_float32, write_wav_float32


def test_wav_roundtrip_float32(tmp_path):
    sr = 48000
    n = 4096
    t = np.arange(n) / sr
    audio = (0.5 * np.sin(2 * np.pi * 1000 * t)).astype(np.float32)

    path = tmp_path / "test.wav"
    write_wav_float32(path, audio, sr)

    sr_back, audio_back = read_wav_float32(path)
    assert sr_back == sr
    assert audio_back.dtype == np.float32
    assert len(audio_back) == n
    np.testing.assert_allclose(audio_back, audio, atol=1e-6)


def test_wav_rejects_stereo(tmp_path):
    import pytest
    audio = np.zeros((100, 2), dtype=np.float32)
    with pytest.raises(ValueError, match="mono"):
        write_wav_float32(tmp_path / "stereo.wav", audio, 48000)
