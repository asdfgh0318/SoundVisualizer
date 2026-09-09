import numpy as np

from server.core.fft import compute_fft
from server.core.tones import (
    THIRD_OCTAVE_CENTRES,
    analyse,
    find_bpf,
    notched_band_levels,
    tone_levels,
)

FS = 48000


def _rotor_like(
    bpf: float,
    seconds: float = 2.0,
    tone_amp: float = 0.05,
    noise_rms: float = 0.002,
    harmonics: int = 6,
    seed: int = 0,
):
    rng = np.random.default_rng(seed)
    t = np.arange(int(seconds * FS)) / FS
    x = noise_rms * rng.standard_normal(len(t))
    for h in range(1, harmonics + 1):
        x += tone_amp / h * np.sin(2 * np.pi * h * bpf * t + rng.uniform(0, 2 * np.pi))
    # shaft harmonics at half the BPF, weaker
    for k in (1, 3, 5):
        x += 0.1 * tone_amp * np.sin(2 * np.pi * k * bpf / 2 * t)
    return x.astype(np.float32)


def test_find_bpf_recovers_fundamental_within_1_hz():
    for bpf in (150.0, 216.0, 238.0, 258.0, 300.0):
        f, m = compute_fft(_rotor_like(bpf), FS, size=4096)
        est = find_bpf(f, m)
        assert est is not None
        assert abs(est - bpf) < 1.0, (bpf, est)


def test_find_bpf_returns_none_on_noise():
    rng = np.random.default_rng(1)
    x = (0.01 * rng.standard_normal(2 * FS)).astype(np.float32)
    f, m = compute_fft(x, FS, size=4096)
    assert find_bpf(f, m) is None


def test_tone_level_matches_sine_power():
    bpf = 238.0
    f, m = compute_fft(_rotor_like(bpf, noise_rms=1e-5), FS, size=4096)
    tones = tone_levels(f, m, bpf, harmonics=3)
    # a sine of amplitude A has mean-square A^2/2; the fundamental has A = 0.05
    expected = 10 * np.log10(0.05**2 / 2)
    assert abs(tones[0].level_db - expected) < 0.2
    assert abs(tones[1].level_db - (expected - 20 * np.log10(2))) < 0.2


def test_notched_bands_ignore_a_strong_tone():
    bpf = 238.0
    rng = np.random.default_rng(2)
    # floor chosen so the BPF stands ~35 dB above the per-bin floor, as in the real captures
    noise = (0.03 * rng.standard_normal(2 * FS)).astype(np.float32)
    f, m_noise = compute_fft(noise, FS, size=16384)
    f, m_tone = compute_fft(noise + _rotor_like(bpf, noise_rms=0.0), FS, size=16384)
    plain = notched_band_levels(f, m_noise, None)
    notched = notched_band_levels(f, m_tone, bpf)
    # the 250 Hz band holds the BPF; notched it must match the tone-free floor
    i250 = int(np.argmin([abs(c - 250) for c in THIRD_OCTAVE_CENTRES]))
    assert abs(notched[i250] - plain[i250]) < 0.5
    # and a band with no tone is untouched
    i2000 = int(np.argmin([abs(c - 2000) for c in THIRD_OCTAVE_CENTRES]))
    assert abs(notched[i2000] - plain[i2000]) < 0.3


def test_analyse_bundle():
    f, m = compute_fft(_rotor_like(238.0), FS, size=4096)
    a = analyse(f, m)
    assert a.tone_ok and abs(a.bpf_hz - 238.0) < 1.0
    assert [t.harmonic for t in a.tones] == [1, 2, 3, 4, 5, 6]
    assert len(a.broadband_bands_db) == len(THIRD_OCTAVE_CENTRES)
