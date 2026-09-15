"""Session bookkeeping: one capsule's full stepped-tone curve per call.

The library contract ends at a WAV plus its tone stats; this module adds
the loop, the labels and the per-frequency levels.json so a real 11-capsule
session is one call per physical swap. Identity stays "the one UMIK plugged
in" — the label is whatever the operator reads off the capsule.
"""

import json
import time
from pathlib import Path

from .core import (
    SR,
    CalibratorError,
    Mic,
    Speaker,
    assert_tone_stable,
    save_wav,
    take_sample_at_frequency,
    third_octave,
)


def capture_capsule(
    m: Mic,
    s: Speaker,
    label: str,
    out_dir: str | Path,
    *,
    freqs: list[float] | None = None,
    amplitude: float = 1.0,
    settle_s: float = 0.7,
    capture_s: float = 2.0,
    lf_capture_s: float = 6.0,
    lf_below_hz: float = 250.0,
) -> Path:
    """Capture a full stepped-tone curve for the capsule currently plugged in.

    Writes <out_dir>/<label>/{meta.json, levels.json, <freq>hz.wav}. A repeated
    label gets an __2 suffix (that is how the reference bracket works: call it
    again with the same label at session end). A frequency that fails the
    stability gate is recorded with its error and the loop continues — a weak
    low-frequency point must not cost the whole capsule.
    """
    base = Path(out_dir)
    out = base / label
    if out.exists():
        k = 2
        while (base / f"{label}__{k}").exists():
            k += 1
        out = base / f"{label}__{k}"
    out.mkdir(parents=True)

    freqs = third_octave() if freqs is None else list(freqs)
    (out / "meta.json").write_text(json.dumps({
        "label": label,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "mic": {"name": m.name, "card_id": m.card_id},
        "speaker": {"name": s.name, "card_id": s.card_id},
        "amplitude": amplitude,
        "sr": SR,
        "freqs": freqs,
    }, indent=2))

    results: list[dict] = []
    for f in freqs:
        cap = lf_capture_s if f < lf_below_hz else capture_s
        try:
            sample, sr = take_sample_at_frequency(
                m, s, f, settle_s=settle_s, capture_s=cap, amplitude=amplitude)
            save_wav(out / f"{f:g}hz.wav", sample, sr)
            stats = assert_tone_stable(sample, f, sr=sr)
            row = {"freq": f, "capture_s": cap, **stats}
        except CalibratorError as e:
            row = {"freq": f, "capture_s": cap, "error": str(e)}
        results.append(row)
        status = f"ok  {stats['level_dbfs']:6.1f} dBFS  SNR {stats['snr_db']:3.0f} dB" \
            if "error" not in row else f"FAILED  {row['error']}"
        print(f"{label:>10}  {f:7g} Hz  {status}", flush=True)
        (out / "levels.json").write_text(json.dumps(results, indent=2))
    return out
