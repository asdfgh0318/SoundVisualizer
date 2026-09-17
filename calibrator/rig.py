"""Stepped tones through the WHOLE arc at once: one speaker at the hub, eleven mics.

The single-mic library answers "what is this capsule's own response". This module
answers a different question: what does a capsule read *when the rig is around it*.
Those are not the same measurement, and the difference is the point. The 2026-09-16
substitution session was run with the chamber cleared — one capsule, one speaker,
nothing else — so it cannot see anything the array does to itself: eleven bodies on a
1.68 m ring sit 26.3 cm apart, and half a wavelength equals that spacing at 653 Hz,
right where the capsule-swap audit leaves its largest unexplained residual (-2.6 dB
at 630 Hz). Running the same kind of tone grid with the rig assembled, and again with
a capsule's neighbours removed, is what separates the room from the array.

Reuses both halves rather than reimplementing either:
  * playback  — the inline PortAudio callback from calibrator.core, the path that
    measures 0 underflows behind the dock's hub
  * capture   — server.core.capture.capture_simultaneous, the eleven-stream recorder
    the rig already uses, called as a library so nothing is written to the
    measurement store

Identity comes from a Setup preset: it holds serial, elevation and `alsa_card_id`
(the udev port-path name), which is stable across reboots where the PortAudio device
index is not.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sounddevice as sd

from server.core.capture import MicCaptureSpec, capture_simultaneous

from .core import (
    SR,
    CalibratorError,
    Mic,
    Speaker,
    _assert_mixer_gates,
    _card_id,
    _hw_card,
    assert_speaker_ok,
    assert_tone_stable,
    save_wav,
)

_LEAD_S = 0.25  # longer than the single-mic path: eleven streams take longer to settle


@dataclass(frozen=True)
class ArcMic:
    position_deg: float
    serial: str          # calibration_file_id — the real capsule serial
    card_id: str         # udev name, e.g. umik_1_1_4_1
    index: int           # PortAudio device index, resolved at run time
    card: int            # ALSA card number, for the mixer gate
    name: str            # PortAudio device name, for error messages

    def as_mic(self) -> Mic:
        return Mic(index=self.index, name=self.name, card=self.card, card_id=self.card_id)


def assert_arc_ok(arc: list[ArcMic]) -> None:
    """Every capsule's own mixer at unity, checked before a single tone is played.

    Each UMIK carries its own `Mic Capture Volume`, it is device-firmware state that
    WirePlumber rewrites, and these eleven get replugged constantly. One capsule left
    at -6 dB would read as a -6 dB error at its POSITION, which is exactly the kind of
    thing this measurement exists to detect — so it has to be impossible, not unlikely.
    Every capsule is reported, not just the first bad one.
    """
    problems = []
    for m in arc:
        try:
            _assert_mixer_gates(m.as_mic(), "Mic Capture")
        except CalibratorError as e:
            problems.append(f"{m.position_deg:+.0f}° {m.serial}: {e}")
    if problems:
        raise CalibratorError(f"{len(problems)} of {len(arc)} capsules not at unity — "
                              + " | ".join(problems))


def load_arc(preset: str | Path) -> list[ArcMic]:
    """Resolve a Setup preset against the devices PortAudio can see right now.

    Raises with the full picture rather than a partial list: a rig sweep with a
    silently missing capsule is worse than no sweep, because the gap only shows up
    in analysis days later.
    """
    entries = json.loads(Path(preset).read_text())["mics"]
    devs = list(sd.query_devices())
    by_card: dict[str, int] = {}
    for i, d in enumerate(devs):
        if "UMIK-2" in d["name"] and "(hw:" in d["name"] and d["max_input_channels"] > 0:
            cid = _card_id(_hw_card(d["name"]))
            if cid:
                by_card[cid] = i

    out, missing = [], []
    for e in entries:
        cid = e.get("alsa_card_id")
        if cid in by_card:
            i = by_card[cid]
            out.append(ArcMic(float(e["elevation_deg"]), e["calibration_file_id"], cid, i,
                              _hw_card(devs[i]["name"]), devs[i]["name"]))
        else:
            missing.append(f"{e['calibration_file_id']} at {e['elevation_deg']:+.0f}° ({cid})")
    if missing:
        seen = ", ".join(sorted(by_card)) or (
            "none — PipeWire may be holding them; wpctl set-profile <dev> off")
        raise CalibratorError(
            f"{len(missing)} of {len(entries)} preset mics are not visible to PortAudio: "
            + "; ".join(missing) + f"  |  visible: {seen}"
        )
    return sorted(out, key=lambda m: -m.position_deg)


def take_rig_sample(
    arc: list[ArcMic],
    s: Speaker,
    freq: float,
    *,
    settle_s: float = 0.7,
    capture_s: float = 2.0,
    amplitude: float = 0.03,
) -> list[np.ndarray]:
    """Play a steady tone and record every capsule on the arc at once.

    The tone runs for settle_s before the capture opens and for the whole capture,
    so every capsule hears the identical signal — which is what makes the levels
    comparable between positions without knowing anything about the source.
    """
    assert_speaker_ok(s)
    assert_arc_ok(arc)
    if not 0.0 < freq < SR / 2:
        raise CalibratorError(f"freq {freq} outside (0, {SR / 2}) Hz")
    if not 0.0 < amplitude <= 1.0:
        raise CalibratorError(f"amplitude {amplitude} outside (0, 1]")

    n = [0]

    def tone_cb(outdata, frames, _time, _status):
        t = (n[0] + np.arange(frames)) / SR
        outdata[:] = (amplitude * np.sin(2.0 * np.pi * freq * t))[:, None].astype(np.float32)
        n[0] += frames

    specs = [MicCaptureSpec(serial=m.serial, device_index=m.index, sample_rate=SR) for m in arc]
    with sd.OutputStream(device=s.index, samplerate=SR, channels=s.channels,
                         dtype="float32", callback=tone_cb):
        time.sleep(settle_s)
        results = capture_simultaneous(specs, capture_s + _LEAD_S)
    keep = round(capture_s * SR)
    return [np.asarray(r.audio, dtype=np.float64).reshape(-1)[-keep:] for r in results]


def capture_rig(
    arc: list[ArcMic],
    s: Speaker,
    label: str,
    out_dir: str | Path,
    freqs: list[float],
    *,
    amplitude: float = 0.03,
    settle_s: float = 0.7,
    capture_s: float = 2.0,
    save_wavs: bool = False,
) -> Path:
    """One tone grid over the whole arc. Writes levels.json keyed by position.

    A frequency that fails the stability gate on one capsule is recorded as failed
    for THAT capsule only and the rest are kept — with eleven microphones, treating
    one bad channel as fatal for the frequency would throw away ten good readings.
    """
    base = Path(out_dir)
    out = base / label
    k = 2
    while out.exists():
        out = base / f"{label}__{k}"
        k += 1
    out.mkdir(parents=True)

    (out / "meta.json").write_text(json.dumps({
        "label": label,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "kind": "rig-stepped-tones",
        "speaker": {"name": s.name, "card_id": s.card_id},
        "arc": [{"position_deg": m.position_deg, "serial": m.serial, "card_id": m.card_id}
                for m in arc],
        "amplitude": amplitude, "sr": SR, "capture_s": capture_s, "freqs": freqs,
    }, indent=2))

    rows: list[dict] = []
    for f in freqs:
        samples = take_rig_sample(arc, s, f, settle_s=settle_s,
                                  capture_s=capture_s, amplitude=amplitude)
        per: dict[str, dict] = {}
        for m, x in zip(arc, samples, strict=True):
            key = f"{m.position_deg:+.0f}"
            try:
                per[key] = {"serial": m.serial, **assert_tone_stable(x, f, sr=SR)}
            except CalibratorError as e:
                per[key] = {"serial": m.serial, "error": str(e)}
            if save_wavs:
                save_wav(out / f"{f:g}hz_{key}.wav", x, SR)
        rows.append({"freq": f, **{k2: v for k2, v in per.items()}})
        (out / "levels.json").write_text(json.dumps(rows, indent=2))
        ok = [v["level_dbfs"] for v in per.values() if "error" not in v]
        bad = [k2 for k2, v in per.items() if "error" in v]
        print(f"{label:>12}  {f:7g} Hz  {len(ok):2d}/{len(arc)} ok  "
              + (f"{min(ok):6.1f}..{max(ok):6.1f} dBFS" if ok else "  no level ")
              + (f"   failed: {','.join(bad)}" if bad else ""), flush=True)
    return out
