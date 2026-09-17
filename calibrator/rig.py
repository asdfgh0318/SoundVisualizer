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
from threading import Lock

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
    position_deg: float | None
    serial: str          # calibration_file_id — the real capsule serial
    card_id: str         # udev name, e.g. umik_1_1_4_1
    index: int           # PortAudio device index, resolved at run time
    card: int            # ALSA card number, for the mixer gate
    name: str            # PortAudio device name, for error messages

    def as_mic(self) -> Mic:
        return Mic(index=self.index, name=self.name, card=self.card, card_id=self.card_id)


def _usb_port(card: int | None) -> str | None:
    """`3-6.4.1` for the physical USB port an ALSA card sits on."""
    if card is None:
        return None
    try:
        return Path(f"/sys/class/sound/card{card}/device").resolve().parent.name
    except OSError:
        return None


def _port_id(card: int | None) -> str | None:
    """The udev name generate_udev.py would give this port: `3-6.4.1` -> `umik_3_6_4_1`.

    Derived from sysfs rather than read from the card id, so it works on a machine
    where the udev rules were never installed — which is the normal case for a laptop
    that is not the Pi.
    """
    port = _usb_port(card)
    return f"umik_{port.replace('-', '_').replace('.', '_')}"[:15] if port else None


def discover_umiks() -> list[ArcMic]:
    """Every UMIK PortAudio can see, ordered by USB port. Position unknown.

    For when there is no usable preset — which includes the normal case of moving the
    rig to a different machine, since the preset's identity is a USB PORT PATH and
    those do not travel. Use it with `identify` to build the map by tapping.
    """
    out = []
    for i, d in enumerate(sd.query_devices()):
        if "UMIK-2" in d["name"] and "(hw:" in d["name"] and d["max_input_channels"] > 0:
            card = _hw_card(d["name"])
            out.append(ArcMic(None, "?", _port_id(card) or _card_id(card) or "?",
                              i, card, d["name"]))
    return sorted(out, key=lambda m: m.card_id)


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
            card = _hw_card(d["name"])
            for cid in (_card_id(card), _port_id(card)):
                if cid:
                    by_card[cid] = i

    out, missing = [], []
    for e in entries:
        cid = e.get("alsa_card_id")
        if cid not in by_card:
            cid = next((k for k in by_card if k == e.get("alsa_card_id")), cid)
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


def identify_live(arc: list[ArcMic], *, refresh_hz: float = 12.0, peak_hold_s: float = 2.0,
                   tap_over_db: float = 12.0) -> None:
    """Live per-capsule meter, so YOU identify the mics rather than trusting a detector.

    Tap a capsule and watch which row jumps. Nothing is inferred and nothing is
    written: the tool only shows what each stream is hearing, right now.

    This exists because the software cannot check the two links that matter. A UMIK-2
    reports USB serial `00000`, so the capsule on a given cable is unverifiable
    electronically, and nothing anywhere knows which arc position a cable ends at —
    `load_arc` only proves which USB PORT each stream comes from. With the source at
    the hub every capsule is equidistant, so the measurement itself carries no
    positional information either. A tap is the only signal that does.
    """
    n = len(arc)
    rms = [1e-9] * n
    peak = [(-120.0, 0.0)] * n            # (dBFS, when)
    locks = [Lock() for _ in arc]

    def make_cb(i: int):
        def cb(indata, frames, _t, _status):
            v = float(np.sqrt(np.mean(np.square(indata[:, 0].astype(np.float64)))) + 1e-12)
            with locks[i]:
                rms[i] = v
        return cb

    streams = []
    try:
        for i, m in enumerate(arc):
            st = sd.InputStream(device=m.index, channels=1, samplerate=SR,
                                dtype="float32", blocksize=1024, callback=make_cb(i))
            st.start()
            streams.append(st)

        base = [-120.0] * n
        print(f"\nLive meter on {n} capsules — tap one and watch its row. Ctrl-C to stop.\n")
        print("\n" * (n + 2), end="")
        t0 = time.time()
        while True:
            now = time.time()
            db = []
            for i in range(n):
                with locks[i]:
                    db.append(20.0 * np.log10(rms[i] + 1e-12))
            for i, v in enumerate(db):
                # Quiet baseline: follow a falling level quickly, rise only by a crawl,
                # so a tap raises the level far above the baseline instead of dragging
                # the baseline up with it.
                base[i] = v if base[i] < -119 else (
                    base[i] * 0.9 + v * 0.1 if v < base[i] else base[i] + 0.02)
                if v > peak[i][0] or now - peak[i][1] > peak_hold_s:
                    peak[i] = (v, now)
            loud = int(np.argmax(db))
            print(f"\033[{n + 2}A", end="")
            print(f"  {'position':>9} {'capsule':>9} {'port':>14} {'now':>8} {'peak':>8}   level"
                  + " " * 12)
            for i, m in enumerate(arc):
                v, pk = db[i], peak[i][0]
                bar = "#" * max(0, min(40, int((v + 80) / 2)))
                tag = " <<< TAP" if v - base[i] > tap_over_db else ("  <- loudest" if i == loud else "")
                pos = f"{m.position_deg:+8.0f}°" if m.position_deg is not None else "   slot " + f"{i + 1:<2d}"
                print(f"  {pos:>9} {m.serial[-7:]:>9} {m.card_id:>14} "
                      f"{v:8.1f} {pk:8.1f}   {bar:<40}{tag}   ")
            print(f"  {time.strftime('%H:%M:%S')}   elapsed {now - t0:5.1f} s"
                  + " " * 40)
            time.sleep(1.0 / refresh_hz)
    except KeyboardInterrupt:
        print("\nstopped.")
    finally:
        for st in streams:
            try:
                st.stop()
                st.close()
            except Exception:
                pass


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
