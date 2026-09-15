"""Dead-simple single-mic tone capture for the substitution-calibration session.

    from calibrator import (
        acquire_umik, acquire_speaker, assert_mic_ok, assert_speaker_ok,
        take_sample_at_frequency, save_wav,
    )

    m = acquire_umik()        # the one UMIK-2 plugged in
    s = acquire_speaker()     # our PCM2902 interface (pinned by USB ID)
    sample, sr = take_sample_at_frequency(m, s, 1000)
    save_wav("1000hz.wav", sample, sr)

Two rules the whole module hangs on:

* Identity is the connection. No serials, no stored state — the one UMIK plugged
  in is the mic under test, so 0 or >1 connected is an error.
* Both devices carry a USB feature-unit volume living in their firmware, shared
  state that WirePlumber or a replug can silently change (the interface arrived
  at -23 dB). The gates are therefore re-read before *every* capture, never
  trusted from session start. Nothing here ever writes a control.
"""

import itertools
import operator
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sounddevice as sd
from scipy.io import wavfile

SR = 48000

# Discarded head of every capture; must exceed the ~7 ms stream-open burst.
_LEAD_S = 0.03

# The session interface is the Burr-Brown/TI PCM2902 USB codec ("USB Audio
# CODEC"). Pinned by USB vendor:product ID, not by name or card number: the
# name is a generic chip string many dongles share, and card numbers shift
# with every plug. This keeps working with any other USB audio device
# plugged in; `index=` is the escape hatch for a different interface.
SPEAKER_USB_ID = ("08bb", "2902")


class CalibratorError(RuntimeError):
    """Every failure mode in this module; the message is meant for a human."""


@dataclass(frozen=True)
class Mic:
    index: int
    name: str
    card: int | None
    card_id: str | None


@dataclass(frozen=True)
class Speaker:
    index: int
    name: str
    card: int | None
    card_id: str | None
    channels: int


def _hw_card(name: str) -> int | None:
    m = re.search(r"\(hw:(\d+),", name)
    return int(m.group(1)) if m else None


def _card_id(card: int | None) -> str | None:
    if card is None:
        return None
    try:
        return Path(f"/sys/class/sound/card{card}/id").read_text().strip() or None
    except OSError:
        return None


def _usb_id(card: int | None) -> tuple[str, str] | None:
    """(idVendor, idProduct) of the USB device behind an ALSA card, or None."""
    if card is None:
        return None
    try:
        base = Path(f"/sys/class/sound/card{card}/device").resolve().parent
        return (
            (base / "idVendor").read_text().strip(),
            (base / "idProduct").read_text().strip(),
        )
    except OSError:
        return None


def acquire_umik(index: int | None = None) -> Mic:
    """The one UMIK-2 connected. `index` is the explicit escape hatch."""
    devs = list(sd.query_devices())
    if index is not None:
        d = _device_at(devs, index)
        if "UMIK-2" not in d["name"] or "(hw:" not in d["name"] or d["max_input_channels"] < 1:
            raise CalibratorError(f"device {index} is '{d['name']}', not a UMIK-2 input")
    else:
        found = [(i, d) for i, d in enumerate(devs)
                 if "UMIK-2" in d["name"] and "(hw:" in d["name"] and d["max_input_channels"] > 0]
        if len(found) != 1:
            raise CalibratorError(
                f"expected exactly one UMIK-2, found {len(found)}: "
                + (_device_list(found) or "none visible to PortAudio — if it is plugged in, "
                   "PipeWire is probably holding it; wpctl set-profile <dev> off")
            )
        i, d = found[0]
    card = _hw_card(d["name"])
    return Mic(index=i, name=d["name"], card=card, card_id=_card_id(card))


def acquire_speaker(index: int | None = None) -> Speaker:
    """Our PCM2902 interface (SPEAKER_USB_ID), wherever it is plugged.

    Other USB audio devices (the UMIK, headsets, another interface) do not
    interfere. A second PCM2902 would be an ambiguity and errors out; use
    `index=` for any deliberate different output.
    """
    devs = list(sd.query_devices())
    if index is not None:
        d = _device_at(devs, index)
        if "(hw:" not in d["name"] or d["max_output_channels"] < 1:
            raise CalibratorError(f"device {index} is '{d['name']}', not a hardware output")
    else:
        found = [(i, d) for i, d in enumerate(devs)
                 if "(hw:" in d["name"] and d["max_output_channels"] > 0
                 and _usb_id(_hw_card(d["name"])) == SPEAKER_USB_ID]
        if len(found) != 1:
            raise CalibratorError(
                f"expected exactly one speaker interface {SPEAKER_USB_ID[0]}:{SPEAKER_USB_ID[1]}, "
                f"found {len(found)}: "
                + (_device_list(found) or "none visible to PortAudio — if it is plugged in, "
                   "PipeWire is probably holding it; wpctl set-profile <dev> off")
            )
        i, d = found[0]
    card = _hw_card(d["name"])
    return Speaker(index=i, name=d["name"], card=card, card_id=_card_id(card),
                   channels=min(2, d["max_output_channels"]))


def _device_at(devs: list, index: int) -> dict:
    if index < 0:
        raise CalibratorError("device index must be >= 0")
    try:
        return devs[index]
    except IndexError as e:
        raise CalibratorError(f"no sounddevice index {index}") from e


def _device_list(found) -> str:
    return "; ".join(f"[{i}] {d['name']}" for i, d in found)


# ---------------------------------------------------------------- mixer gates

@dataclass(frozen=True)
class _Control:
    numid: int
    iface: str
    name: str
    idx: int
    type: str
    values: list
    min: int | None
    max: int | None
    db_min: float | None
    db_max: float | None


_HDR = re.compile(r"numid=(\d+),iface=(\w+),name='([^']+)'(?:,index=(\d+))?")
_TYPE = re.compile(r";\s*type=(\w+),access=[\w-]+,values=\d+(?:,min=(-?\d+),max=(-?\d+))?")
_VALS = re.compile(r":\s*values=(.+)")
_DBMM = re.compile(r"dBminmax-min=(-?[\d.]+)dB,max=(-?[\d.]+)dB")

_BOOL_TYPES = ("BOOLEAN", "INV_BOOLEAN")


def _read_controls(card: int | None) -> list[_Control]:
    """Parse `amixer -c N contents` into typed controls."""
    if card is None:
        raise CalibratorError("device has no ALSA card number — cannot read its mixer")
    try:
        proc = subprocess.run(
            ["amixer", "-c", str(card), "contents"],
            capture_output=True, text=True, check=True,
        )
    except FileNotFoundError as e:
        raise CalibratorError("amixer not found (install alsa-utils)") from e
    except subprocess.CalledProcessError as e:
        raise CalibratorError(f"amixer failed on card {card}: {(e.stderr or '').strip()}") from e

    out: list[_Control] = []
    cur: dict | None = None
    for raw in proc.stdout.splitlines():
        line = raw.strip()
        if line.startswith("numid="):
            _flush(cur, out)
            cur = None
            m = _HDR.match(line)
            if m:
                cur = {
                    "numid": int(m.group(1)),
                    "iface": m.group(2),
                    "name": m.group(3),
                    "idx": int(m.group(4) or 0),
                    "type": "",
                    "values": [],
                    "min": None,
                    "max": None,
                    "db_min": None,
                    "db_max": None,
                }
            continue
        if cur is None:
            continue
        if line.startswith(";"):
            m = _TYPE.search(line)
            if m:
                cur["type"] = m.group(1)
                if m.group(2) is not None:
                    cur["min"], cur["max"] = int(m.group(2)), int(m.group(3))
        elif line.startswith(":"):
            m = _VALS.search(line)
            if not m:
                continue
            raw_values = [v.strip() for v in m.group(1).split(",")]
            if cur["type"] in _BOOL_TYPES:
                cur["values"] = [v == "on" for v in raw_values]
            elif cur["type"] == "INTEGER":
                try:
                    cur["values"] = [int(v) for v in raw_values]
                except ValueError:
                    cur["values"] = []
        elif line.startswith("|"):
            m = _DBMM.search(line)
            if m:
                cur["db_min"], cur["db_max"] = float(m.group(1)), float(m.group(2))
    _flush(cur, out)
    return out


def _flush(cur: dict | None, out: list) -> None:
    if cur is not None and cur["type"] in ("INTEGER", *_BOOL_TYPES):
        out.append(_Control(**cur))


def _db_of(c: _Control, v: int) -> str:
    if c.db_min is None or c.min is None or c.max is None or c.max == c.min:
        return "? dB"
    db = c.db_min + (v - c.min) * (c.db_max - c.db_min) / (c.max - c.min)
    return f"{db:+.2f} dB"


def _assert_mixer_gates(handle: Mic | Speaker, prefix: str) -> None:
    """Every MIXER control named `<prefix> Volume` must sit at max (0 dB
    firmware attenuation) and every `<prefix> Switch` must be on. On both
    devices 'on' is the unmuted state. Missing controls fail too."""
    controls = [c for c in _read_controls(handle.card)
                if c.iface == "MIXER" and c.name.startswith(prefix)]
    vols = [c for c in controls if c.type == "INTEGER"]
    switches = [c for c in controls if c.type in _BOOL_TYPES]
    problems: list[str] = []
    if not vols:
        problems.append(f"no '{prefix} Volume' control found")
    if not switches:
        problems.append(f"no '{prefix} Switch' control found")
    for c in vols:
        if not c.values:
            problems.append(f"{c.name}: could not read values")
            continue
        bad = [v for v in c.values if v != c.max]
        if bad:
            problems.append(
                f"{c.name} = {c.values} of max {c.max} "
                f"({', '.join(_db_of(c, v) for v in bad)}), expected 0 dB"
            )
    for c in switches:
        if not all(c.values):
            problems.append(f"{c.name} = off, expected on")
    if problems:
        raise CalibratorError(
            f"{handle.name}: digital state not at unity — " + "; ".join(problems)
        )


def assert_mic_ok(m: Mic) -> Mic:
    """UMIK mixer at unity + the input opens at 48 kHz. Returns m for chaining."""
    _assert_mixer_gates(m, "Mic Capture")
    try:
        with sd.InputStream(device=m.index, channels=1, samplerate=SR, dtype="float32") as stream:
            stream.start()
            stream.stop()
    except Exception as e:
        raise CalibratorError(f"cannot open '{m.name}' for capture at {SR} Hz: {e}") from e
    return m


def assert_speaker_ok(s: Speaker) -> Speaker:
    """Interface mixer at unity + the output opens at 48 kHz. Returns s for chaining."""
    _assert_mixer_gates(s, "PCM Playback")
    try:
        with sd.OutputStream(device=s.index, channels=s.channels, samplerate=SR,
                             dtype="float32") as stream:
            stream.start()
            stream.stop()
    except Exception as e:
        raise CalibratorError(f"cannot open '{s.name}' for playback at {SR} Hz: {e}") from e
    return s


# ------------------------------------------------------------------ capture

def take_sample_at_frequency(
    m: Mic,
    s: Speaker,
    freq: float,
    *,
    settle_s: float = 0.5,
    capture_s: float = 1.0,
    amplitude: float = 0.25,
) -> tuple[np.ndarray, int]:
    """Play a steady tone at `freq` on `s` and record `m` while it plays.

    Both gates re-run here, so every capture is independently verified: a
    control moved since the last capture fails loudly instead of shifting
    this capture by an unknown number of dB.

    The tone is generated *inside* the PortAudio callback — there is no
    buffer to feed and nothing to starve. sd.play(loop=True) with its
    ring-buffer thread produced 20+ ms-scale dropouts per capture behind
    the dock's full-speed hub; the inline generator measured 0 underflows.

    The first _LEAD_S seconds are discarded: opening the capture stream
    re-reserves USB isochronous bandwidth and the full-speed CODEC drops
    ~7 ms of tone right there, once, every time.
    """
    assert_mic_ok(m)
    assert_speaker_ok(s)
    if not 0.0 < freq < SR / 2:
        raise CalibratorError(f"freq {freq} outside (0, {SR / 2}) Hz")
    if not 0.0 < amplitude <= 1.0:
        raise CalibratorError(f"amplitude {amplitude} outside (0, 1]")
    if settle_s < 0.0:
        raise CalibratorError(f"settle_s {settle_s} must be >= 0")
    if capture_s <= 0.0:
        raise CalibratorError(f"capture_s {capture_s} must be > 0")

    n = [0]

    def tone_cb(outdata, frames, _time, _status):
        t = (n[0] + np.arange(frames)) / SR
        outdata[:] = (amplitude * np.sin(2.0 * np.pi * freq * t))[:, None].astype(np.float32)
        n[0] += frames

    with sd.OutputStream(device=s.index, samplerate=SR, channels=s.channels,
                         dtype="float32", callback=tone_cb):
        time.sleep(settle_s)
        rec = sd.rec(
            round((capture_s + _LEAD_S) * SR),
            samplerate=SR,
            device=m.index,
            channels=1,
            dtype="float32",
            blocking=True,
        )
    out = rec.reshape(-1)
    return out[len(out) - round(capture_s * SR):], SR


def octave_series(f0: float = 200.0, fmax: float = 15000.0) -> list[float]:
    """f0, 2*f0, 4*f0, ... stopping at or below fmax: 200...12800 Hz by default."""
    return list(itertools.takewhile(lambda f: f <= fmax,
                                    itertools.accumulate(itertools.repeat(2), operator.mul,
                                                         initial=f0)))


# Preferred 1/3-octave band centers (IEC 61260 rounded series).
THIRD_OCTAVE_HZ = (50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
                   1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000,
                   10000, 12500, 16000)


def third_octave(fmin: float = 63.0, fmax: float = 16000.0) -> list[float]:
    """Preferred 1/3-octave centers within [fmin, fmax]: 63...16000 Hz by default."""
    return [float(f) for f in THIRD_OCTAVE_HZ if fmin <= f <= fmax]


def log_series(fmin: float = 60.0, fmax: float = 16000.0, per_octave: int = 6) -> list[float]:
    """Log-spaced tone grid anchored at 1 kHz (base-2, IEC 61260 convention),
    rounded to whole Hz: per_octave=6 gives 62, 70, 79 ... 15844 (49 points).
    One grid per session: relative_curves matches exact frequency keys, and
    this grid does not repeat THIRD_OCTAVE_HZ's preferred roundings.
    """
    if per_octave < 1:
        raise CalibratorError(f"per_octave {per_octave} must be >= 1")
    k_lo = int(np.ceil(per_octave * np.log2(fmin / 1000)))
    k_hi = int(np.floor(per_octave * np.log2(fmax / 1000)))
    return [float(round(1000 * 2 ** (k / per_octave))) for k in range(k_lo, k_hi + 1)]


def take_octave_series(
    m: Mic,
    s: Speaker,
    f0: float = 200.0,
    fmax: float = 15000.0,
    **kwargs,
) -> dict[float, np.ndarray]:
    """One capture per octave step, {freq: samples}; SR is the module constant.

    kwargs pass straight through to take_sample_at_frequency
    (settle_s, capture_s, amplitude).
    """
    results: dict[float, np.ndarray] = {}
    for freq in octave_series(f0, fmax):
        print(f"{freq:g} Hz", flush=True)
        results[freq] = take_sample_at_frequency(m, s, freq, **kwargs)[0]
    return results


def assert_tone_stable(
    sample: np.ndarray,
    freq: float,
    *,
    sr: int = SR,
    chunk_s: float = 0.25,
    level_tol_db: float = 6.0,
    freq_tol: float = 0.01,
    snr_min_db: float = 10.0,
) -> dict:
    """Verify the tone at `freq` is present and stable across the whole window.

    Three checks on a capture: the tone stands above the adjacent-band floor
    by `snr_min_db` (a dead mic or silent speaker must not pass as perfectly
    stable silence); every chunk's tone level stays within `level_tol_db` of
    the median chunk (dropouts, clicks); every chunk's peak stays within
    `freq_tol` of the nominal (clock or underrun wander). Raises with the
    offending chunks; returns the stats on success.
    """
    x = np.asarray(sample, dtype=np.float64).reshape(-1)
    if not 0.0 < freq < sr / 2:
        raise CalibratorError(f"freq {freq} outside (0, {sr / 2}) Hz")
    n_chunk = round(chunk_s * sr)
    if len(x) < 2 * n_chunk:
        raise CalibratorError(
            f"need at least 2 chunks of {chunk_s} s, capture is {len(x) / sr:.2f} s"
        )

    w = np.hanning(len(x))
    X = np.abs(np.fft.rfft(x * w)) * 2 / w.sum()
    f = np.fft.rfftfreq(len(x), 1 / sr)
    tone_band = (f >= freq * 0.97) & (f <= freq * 1.03)
    floor_band = (f > 0) & (
        ((f >= freq * 0.85) & (f <= freq * 0.95))
        | ((f >= freq * 1.05) & (f <= freq * 1.15))
    )
    if not tone_band.any() or not floor_band.any():
        raise CalibratorError(f"no FFT bins inside the bands around {freq} Hz — longer capture")

    level_full = 20 * np.log10(X[tone_band].max() + 1e-12)
    floor_full = 20 * np.log10(np.sqrt(np.mean(X[floor_band] ** 2)) + 1e-12)
    if level_full - floor_full < snr_min_db:
        raise CalibratorError(
            f"no tone at {freq} Hz: peak {level_full:.1f} dBFS vs adjacent floor "
            f"{floor_full:.1f} dBFS = {level_full - floor_full:.1f} dB SNR, need {snr_min_db} dB"
        )

    n = len(x) // n_chunk
    xc = x[: n * n_chunk].reshape(n, n_chunk)
    wc = np.hanning(n_chunk)
    Xc = np.abs(np.fft.rfft(xc * wc, axis=1)) * 2 / wc.sum()
    fc = np.fft.rfftfreq(n_chunk, 1 / sr)
    cb = (fc >= freq * 0.97) & (fc <= freq * 1.03)
    levels = 20 * np.log10(Xc[:, cb].max(axis=1) + 1e-12)
    peaks = fc[cb][Xc[:, cb].argmax(axis=1)]
    med = np.median(levels)
    # The chunk FFT quantizes the peak to 1/chunk_s bins: at low frequencies
    # that alone exceeds a 1% tolerance (63 Hz lands on a 4 Hz bin grid), so
    # the tolerance has a floor of 1.5 bin widths.
    tol_hz = max(freq_tol * freq, 1.5 * sr / n_chunk)
    bad_level = [i for i in range(n) if abs(levels[i] - med) > level_tol_db]
    bad_freq = [i for i in range(n) if abs(peaks[i] - freq) > tol_hz]
    if bad_level or bad_freq:
        parts = []
        if bad_level:
            parts.append("level: " + ", ".join(
                f"chunk {i} {levels[i]:.1f} dBFS (median {med:.1f})" for i in bad_level))
        if bad_freq:
            parts.append("frequency: " + ", ".join(
                f"chunk {i} {peaks[i]:.1f} Hz" for i in bad_freq))
        raise CalibratorError(f"tone at {freq} Hz not stable — " + "; ".join(parts))

    return {
        "chunks": int(n),
        "level_dbfs": float(med),
        "worst_level_dev_db": float(np.abs(levels - med).max()),
        "peak_hz": [float(p) for p in peaks],
        "worst_freq_dev_hz": float(np.abs(peaks - freq).max()),
        "snr_db": float(level_full - floor_full),
    }


def save_wav(path: str | Path, audio: np.ndarray, sr: int = SR) -> Path:
    """Write float32 mono WAV (IEEE float, the same convention as the server's store)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(path, sr, np.asarray(audio, dtype=np.float32))
    return path
