#!/usr/bin/env python3
"""Rebuild docs/analysis/arc-validation-data.json — the one-pager's data pack.

The pack existed before this script did; it was produced ad hoc. So the script
carries a `--verify-against` mode that regenerates the pack under the OLD
conventions (mic term estimated, factory calibration files) and diffs it against
a committed copy. Only once that reproduces the committed numbers is the
regenerated pack under new conventions worth trusting.

    # prove the generator reproduces what is committed
    scripts/build_arc_data_pack.py --data ../SoundVisualizer-data/data \
        --cal-dir ../SoundVisualizer-data/data/calibrations/factory-originals-2026-09-16 \
        --verify-against docs/analysis/arc-validation-data.json

    # regenerate with the corrected cal files and no mic term
    scripts/build_arc_data_pack.py --data ../SoundVisualizer-data/data \
        --no-mic-term --out docs/analysis/arc-validation-data.json
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from server.core import calibration as C  # noqa: E402

from arc_error_map import THIRD_OCT, fit  # noqa: E402
from server.core.fft import compute_fft  # noqa: E402
from scipy.io import wavfile  # noqa: E402

WIDE = ["100-10000", "500-2000"]
WIDE_EDGES = [(100.0, 10000.0), (500.0, 2000.0)]
CORE = [f"prop{i}" for i in range(7, 19)]
FLIPPED = [f"prop{i}" for i in (11, 12, 13, 14)]


def levels21(path: str, cal) -> np.ndarray:
    """Nineteen thirds from 125 Hz, then the two wide summary bands.

    The wide columns are an energy integration over the stated edges straight off
    the spectrum — NOT a sum or mean of the third-octaves, whose outer edges do not
    line up with 100 Hz / 10 kHz / 500 Hz / 2 kHz. Getting this wrong moves the
    overall level by ~20 dB, which is how it was caught.
    """
    fs, x = wavfile.read(path)
    x = x.astype(float)
    if x.ndim > 1:
        x = x[:, 0]
    f, mag = compute_fft(x, fs, size=4096)
    if cal is not None:
        mag = C.apply_calibration_to_spectrum(f, mag, cal)
    df = f[1] - f[0]

    def integrate(lo, hi):
        sel = (f >= lo) & (f < hi)
        return 10 * np.log10((10 ** (mag[sel] / 10)).sum() * df)

    out = [integrate(fc / 2 ** (1 / 6), fc * 2 ** (1 / 6)) for fc in THIRD_OCT]
    out += [integrate(lo, hi) for lo, hi in WIDE_EDGES]
    return np.array(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--cal-dir", default=None, help="override the calibrations dir (for --verify-against)")
    ap.add_argument("--pwm", type=int, default=1900)
    ap.add_argument("--no-mic-term", action="store_true")
    ap.add_argument("--out", default="docs/analysis/arc-validation-data.json")
    ap.add_argument("--verify-against", default=None)
    a = ap.parse_args()

    cal_dir = a.cal_dir or os.path.join(a.data, "calibrations")
    cals = {}
    for t in glob.glob(os.path.join(cal_dir, "*.txt")):
        with open(t) as fh:
            cals[os.path.basename(t)[:-4]] = C.parse_umik_calibration(fh.read())

    runs: dict[str, dict] = {}
    obs = []
    for key in sorted(glob.glob(os.path.join(a.data, "2004__6in__unset__dp1-baseline-horizontal*"))):
        name = os.path.basename(key).split("__")[-1].replace("dp1-baseline-horizontal-", "")
        metas = []
        for m in glob.glob(os.path.join(key, "measurements", "*acoustic*", "meta.json")):
            with open(m) as fh:
                metas.append((json.load(fh), os.path.dirname(m)))
        stamps = sorted({os.path.basename(d).split("__")[0] for m, d in metas if m["pwm_setpoint"] == a.pwm})
        if not stamps:
            continue
        stamp = stamps[-1]
        mics: dict[str, dict] = {}
        for m, d in metas:
            if m["pwm_setpoint"] != a.pwm or not os.path.basename(d).startswith(stamp):
                continue
            ser = m["calibration_file_id"]
            wav = os.path.join(d, "audio.wav")
            cal = levels21(wav, cals.get(ser))
            raw = levels21(wav, None)
            mics[str(int(float(m["elevation_deg"])))] = {
                "serial": ser,
                "cal": [round(float(v), 2) for v in cal],
                "raw": [round(float(v), 2) for v in raw],
            }
            if name in CORE:
                obs.append((name, float(m["elevation_deg"]), ser, cal))
        runs[name] = {
            "time": m["t_start"].replace("T", " ")[:16],
            "flipped": name in FLIPPED,
            "coherent": name in CORE,
            "capture": stamp,
            "key": os.path.basename(key),
            "mics": mics,
        }

    _, poss, sers, P, M, R = fit(obs, set(FLIPPED), mic_term=not a.no_mic_term)
    res = np.sqrt((R ** 2).mean(axis=0))

    def row(v):
        return [round(float(x), 2) for x in v]

    pack = {
        "bands": [round(f, 1) for f in THIRD_OCT] + WIDE,
        "positions": [int(p) for p in poss],
        "serials": sers,
        "position_pattern": {str(int(p)): row(P[i]) for i, p in enumerate(poss)},
        "mic_offsets": {s: row(M[i]) for i, s in enumerate(sers)},
        "residual": row(res),
        "flipped": FLIPPED,
        "core_runs": CORE,
        "runs": runs,
        "sens_factor": {s: cals[s].sens_factor_db for s in sers},
        "arc_map": {
            ("+" if p > 0 else "") + str(int(p)): next(
                mi["serial"] for r in runs.values() if r["coherent"]
                for e, mi in r["mics"].items() if int(e) == int(p))
            for p in poss
        },
    }

    if a.verify_against:
        old = json.load(open(a.verify_against))
        worst = 0.0
        for field in ("position_pattern", "mic_offsets"):
            for k, v in pack[field].items():
                if k in old[field]:
                    d = np.abs(np.array(v) - np.array(old[field][k]))
                    worst = max(worst, float(d.max()))
        lev = 0.0
        for rk, rv in pack["runs"].items():
            for pk, mv in rv["mics"].items():
                o = old["runs"].get(rk, {}).get("mics", {}).get(pk)
                if o:
                    for col in ("cal", "raw"):
                        lev = max(lev, float(np.abs(np.array(mv[col]) - np.array(o[col])).max()))
        print(f"verify: worst per-run level difference {lev:.3f} dB (all 21 columns)")
        rd = float(np.abs(np.array(pack["residual"]) - np.array(old["residual"])).max())
        print(f"verify: worst fit difference {worst:.3f} dB, worst residual difference {rd:.3f} dB")
        ok = sorted(pack) == sorted(old)
        print("top-level keys match:", ok)
        rk = sorted(pack["runs"]) == sorted(old["runs"])
        print(f"run set matches: {rk}  ({len(pack['runs'])} vs {len(old['runs'])})")
        ra, rb = next(iter(pack["runs"].values())), next(iter(old["runs"].values()))
        print("run entry fields match:", sorted(ra) == sorted(rb), sorted(ra))
        ma = next(iter(ra["mics"].values())); mb = next(iter(rb["mics"].values()))
        print("mic entry fields match:", sorted(ma) == sorted(mb))
        same = sum(1 for k in pack["runs"] if k in old["runs"]
                   and pack["runs"][k].get("key") == old["runs"][k].get("key"))
        print(f"run 'key' field agrees on {same}/{len(old['runs'])} runs")
        return 0

    with open(a.out, "w") as fh:
        json.dump(pack, fh, indent=1)
    print(f"wrote {a.out}  (mic term: {'estimated' if not a.no_mic_term else 'DROPPED'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
