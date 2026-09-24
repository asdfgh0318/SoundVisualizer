"""Play one steady tone from the hub speaker and show every capsule's level at that tone, live.

    .venv/bin/python -m calibrator.live_tone 306 --preset <setup-preset.json> [--amplitude 0.03]

Same level formula as `assert_tone_stable` (Hann window, peak within ±3 % of the tone) and the
same per-capsule calibration as `capture_rig`, so a number here matches a number in levels.json.
Walk around the chamber and watch which capsule moves. Ctrl+C stops the tone and the meters.
"""

from __future__ import annotations

import argparse
import sys
import threading
import time
from collections import deque

import numpy as np
import sounddevice as sd

from server.core.calibration import parse_umik_calibration

from . import rig
from .core import SR, acquire_speaker, assert_speaker_ok

WINDOW_S = 0.5
REFRESH_S = 0.2
BAR_DB = 15.0


def tone_dbfs(x: np.ndarray, freq: float) -> tuple[float, float]:
    w = np.hanning(len(x))
    X = np.abs(np.fft.rfft(x * w)) * 2 / w.sum()
    f = np.fft.rfftfreq(len(x), 1 / SR)
    tone = (f >= freq * 0.97) & (f <= freq * 1.03)
    floor = ((f >= freq * 0.85) & (f <= freq * 0.95)) | ((f >= freq * 1.05) & (f <= freq * 1.15))
    lvl = 20 * np.log10(X[tone].max() + 1e-12)
    flr = 20 * np.log10(np.sqrt(np.mean(X[floor] ** 2)) + 1e-12)
    return lvl, lvl - flr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("freq", type=float)
    ap.add_argument("--preset", required=True)
    ap.add_argument("--amplitude", type=float, default=0.03)
    a = ap.parse_args()

    arc = sorted(rig.load_arc(a.preset), key=lambda m: -m.position_deg)
    rig.assert_arc_ok(arc)
    s = acquire_speaker()
    assert_speaker_ok(s)
    corr = {}
    for m in arc:
        p = rig.CAL_DIR / f"{m.serial}.txt"
        c = parse_umik_calibration(p.read_text()) if p.exists() else None
        corr[m.serial] = (-float(np.interp(a.freq, c.freq_hz, c.gain_db)) + 94.0 - (c.sens_factor_db or 0.0)) if c else 0.0

    n = int(WINDOW_S * SR)
    bufs = [deque(maxlen=n) for _ in arc]
    locks = [threading.Lock() for _ in arc]

    def in_cb(i):
        def cb(indata, frames, _t, _s):
            with locks[i]:
                bufs[i].extend(indata[:, 0])
        return cb

    k = [0]

    def out_cb(out, frames, _t, _s):
        t = (k[0] + np.arange(frames)) / SR
        out[:] = (a.amplitude * np.sin(2 * np.pi * a.freq * t))[:, None].astype(np.float32)
        k[0] += frames

    streams = [sd.InputStream(device=m.index, samplerate=SR, channels=1, dtype="float32",
                              callback=in_cb(i)) for i, m in enumerate(arc)]
    out = sd.OutputStream(device=s.index, samplerate=SR, channels=s.channels, dtype="float32",
                          callback=out_cb)
    lo_hold = {m.serial: 1e9 for m in arc}
    hi_hold = {m.serial: -1e9 for m in arc}
    try:
        out.start()
        for st in streams:
            st.start()
        time.sleep(WINDOW_S + 0.2)
        sys.stdout.write("\033[2J")
        while True:
            rows = []
            for i, m in enumerate(arc):
                with locks[i]:
                    x = np.array(bufs[i], dtype=float)
                if len(x) < n // 2:
                    rows.append((m, None, None))
                    continue
                if 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12) > -20:
                    # A capsule whose USB stream went bad after a bus reset delivers full-scale
                    # noise (~-5 dBFS rms in a silent room); its "level" would be meaningless.
                    rows.append((m, "broken", None))
                    continue
                lvl, snr = tone_dbfs(x, a.freq)
                rows.append((m, lvl + corr[m.serial], snr))
            vals = [r[1] for r in rows if isinstance(r[1], float)]
            mean = float(np.mean(vals)) if vals else 0.0
            lines = [f"\033[H\033[1m{a.freq:g} Hz live  —  level at the tone, calibrated (dB SPL)   "
                     f"Ctrl+C to stop\033[0m\033[K",
                     f"arc mean {mean:6.1f} dB   spread {np.ptp(vals) if vals else 0:5.1f} dB   "
                     f"window {WINDOW_S:g} s\033[K", "\033[K",
                     f"  pos    serial     dB SPL   vs mean  {'-15':<15}0{'+15':>15}    SNR   min/max since start\033[K"]
            for m, v, snr in rows:
                if v is None:
                    lines.append(f"  {m.position_deg:+4.0f}°  {m.serial[-7:]:>8}   (filling)\033[K")
                    continue
                if v == "broken":
                    lines.append(f"  {m.position_deg:+4.0f}°  {m.serial[-7:]:>8}   \033[31mBROKEN STREAM - full-scale noise, "
                                 f"replug or re-enumerate this capsule\033[0m\033[K")
                    continue
                d = v - mean
                lo_hold[m.serial] = min(lo_hold[m.serial], d)
                hi_hold[m.serial] = max(hi_hold[m.serial], d)
                half = 15
                pos = int(round(np.clip(d, -BAR_DB, BAR_DB) / BAR_DB * half))
                bar = [" "] * (2 * half + 1)
                bar[half] = "|"
                for j in range(min(half, half + pos), max(half, half + pos) + 1):
                    if j != half:
                        bar[j] = "█"
                col = "\033[34m" if d > 3 else ("\033[33m" if d < -6 else "")
                warn = "  low SNR" if snr < 10 else ""
                lines.append(f"  {m.position_deg:+4.0f}°  {m.serial[-7:]:>8}   {v:6.1f}   {d:+6.1f}  "
                             f"{col}{''.join(bar)}\033[0m  {snr:5.0f}   "
                             f"{lo_hold[m.serial]:+5.1f} / {hi_hold[m.serial]:+5.1f}{warn}\033[K")
            lines.append("\033[K")
            lines.append("+90° = top, −90° = bottom.  Yellow = more than 6 dB below the arc mean, blue = more than 3 dB above.\033[K")
            sys.stdout.write("\n".join(lines) + "\033[J")
            sys.stdout.flush()
            time.sleep(REFRESH_S)
    except KeyboardInterrupt:
        pass
    finally:
        for st in streams:
            st.stop(); st.close()
        out.stop(); out.close()
        print("\nstopped: tone off, meters closed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
