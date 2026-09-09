import numpy as np

from server.core.trigger_sync import (
    align_captures,
    is_genuine_onset,
    block_rms_db,
    find_trigger_index,
)


def test_block_rms_db_silence_is_neg_inf():
    samples = np.zeros(1024, dtype=np.float32)
    assert block_rms_db(samples, 0, 128) == float("-inf")


def test_block_rms_db_full_scale_sine_is_near_minus_3():
    sr = 48000
    n = 4096
    t = np.arange(n) / sr
    samples = np.sin(2 * np.pi * 1000 * t).astype(np.float32)
    db = block_rms_db(samples, 0, n)
    assert -3.5 < db < -2.5


def test_find_trigger_returns_minus_one_when_below_threshold():
    samples = np.full(2048, 0.001, dtype=np.float32)  # ~ -60 dBFS
    assert find_trigger_index(samples, threshold_db=-40, block_size=128) == -1


def test_find_trigger_locates_first_block_above_threshold():
    samples = np.zeros(2048, dtype=np.float32)
    samples[1024:] = 0.5  # second half is loud
    idx = find_trigger_index(samples, threshold_db=-10, block_size=128)
    assert idx == 1024


def test_align_captures_aligns_two_offset_signals():
    n = 24000  # 0.5 s @ 48 kHz
    a = np.zeros(n, dtype=np.float32)
    b = np.zeros(n, dtype=np.float32)
    a[5000:5500] = 0.5
    b[8000:8500] = 0.5

    aligned = align_captures(
        [a, b], threshold_db=-10, block_size=128, preroll_samples=128
    )

    assert len(aligned) == 2
    assert len(aligned[0]) == len(aligned[1])
    a_idx = find_trigger_index(aligned[0], -10, 128)
    b_idx = find_trigger_index(aligned[1], -10, 128)
    assert a_idx >= 0 and b_idx >= 0
    assert abs(a_idx - b_idx) <= 128


def test_align_captures_passthrough_when_disabled():
    a = np.zeros(100, dtype=np.float32)
    b = np.ones(100, dtype=np.float32)
    out = align_captures([a, b], threshold_db=-10, block_size=128, preroll_samples=128)
    assert len(out[0]) == 100
    assert len(out[1]) == 100


def test_align_captures_no_trigger_returns_originals():
    a = np.zeros(1024, dtype=np.float32)
    b = np.zeros(1024, dtype=np.float32)
    out = align_captures([a, b], threshold_db=-10, block_size=128, preroll_samples=128)
    assert out[0] is a
    assert out[1] is b


def test_align_captures_preserves_preroll():
    n = 24000
    a = np.zeros(n, dtype=np.float32)
    a[12000:12500] = 0.5
    aligned = align_captures(
        [a, a.copy()], threshold_db=-10, block_size=128, preroll_samples=512
    )
    idx = find_trigger_index(aligned[0], -10, 128)
    assert idx >= 384  # roughly preroll_samples (within block rounding)


def test_align_captures_leaves_running_source_untouched():
    # Issue #13: the motor is already running. Loud mics are above threshold in
    # block 0; one quiet mic crosses only at a late transient. Nothing may be cropped.
    n = 96000  # 2 s @ 48 kHz
    loud = np.full(n, 0.2, dtype=np.float32)
    quiet = np.full(n, 0.005, dtype=np.float32)  # -46 dBFS, under the -40 dBFS threshold
    quiet[80000:80500] = 0.3  # a transient 1.67 s in
    out = align_captures([loud, loud.copy(), quiet], threshold_db=-40, block_size=128, preroll_samples=480)
    assert all(len(o) == n for o in out)


def test_align_captures_rejects_triggers_too_far_apart():
    n = 96000
    a = np.zeros(n, dtype=np.float32)
    b = np.zeros(n, dtype=np.float32)
    a[5000:5500] = 0.5
    b[60000:60500] = 0.5  # 1.15 s later: not the same onset
    out = align_captures([a, b], threshold_db=-10, block_size=128, preroll_samples=128)
    assert len(out[0]) == n and len(out[1]) == n


def test_is_genuine_onset():
    assert is_genuine_onset([5000, 5200, 4900], 4800)
    assert not is_genuine_onset([0, 5000], 4800)
    assert not is_genuine_onset([5000, 60000], 4800)
    assert not is_genuine_onset([-1, 5000], 4800)
