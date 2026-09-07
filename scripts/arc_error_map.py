#!/usr/bin/env python3
"""Arc error map from "horizontal prop" validation runs.

With the prop axis horizontal and perpendicular to the arc plane every mic sits
in the prop plane at the same angle to the axis, so an axisymmetric source must
read the same level at every elevation. Whatever is not a circle is the arc, the
room or the mics. This script separates those with a joint least-squares fit
over many runs:

    L(run, position, mic, band) = g(run) + P(position, band) + M(mic, band)

P is the "arc error map" (directivity error fixed to a physical position, i.e.
room + fixtures), M is the per-mic residual after the UMIK-2 calibration. Runs
where the arc was turned 180 deg (label +e physically at -e) are given with
--rotated; --detect-rotated guesses them from the data (greedy on the 500-2 kHz
residual), which worked for the Sept-2026 prop7-18 set but is fragile when
setups differ between runs, so prefer the lab notes.

    scripts/arc_error_map.py --data ../SoundVisualizer-data/data \
        --glob '2004__6in__unset__dp1-baseline-horizontal-prop*' --pwm 1900 \
        --exclude dp1-baseline-horizontal-prop{1,2,3,4,5,6} \
        --rotated dp1-baseline-horizontal-prop1{1,2,3,4} --out docs/analysis

Requires the repo venv (numpy, scipy, matplotlib) and the calibrations dir
inside --data.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys

import numpy as np
from scipy.io import wavfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from server.core import calibration as C
from server.core.fft import compute_fft

THIRD_OCT = [125 * 2 ** (i / 3) for i in range(0, 19)]  # 125 Hz .. 8 kHz


def band_levels(path: str, cal) -> np.ndarray:
    fs, x = wavfile.read(path)
    x = x.astype(float)
    if x.ndim > 1:
        x = x[:, 0]
    f, mag = compute_fft(x, fs, size=4096)
    if cal is not None:
        mag = C.apply_calibration_to_spectrum(f, mag, cal)
    df = f[1] - f[0]
    out = []
    for fc in THIRD_OCT:
        sel = (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))
        out.append(10 * np.log10((10 ** (mag[sel] / 10)).sum() * df))
    return np.array(out)


def load_runs(data: str, pattern: str, pwm: int, exclude: set[str]):
    cals = {}
    for t in glob.glob(os.path.join(data, "calibrations", "*.txt")):
        with open(t) as fh:
            cals[os.path.basename(t)[:-4]] = C.parse_umik_calibration(fh.read())
    obs = []
    for key in sorted(glob.glob(os.path.join(data, pattern)), key=os.path.getmtime):
        name = os.path.basename(key).split("__")[-1]
        if name in exclude:
            continue
        metas = []
        for m in glob.glob(os.path.join(key, "measurements", "*acoustic*", "meta.json")):
            with open(m) as fh:
                metas.append((json.load(fh), os.path.dirname(m)))
        runs = sorted({d.split("/")[-1].split("__")[0] for m, d in metas if m["pwm_setpoint"] == pwm})
        if not runs:
            continue
        run = runs[-1]
        for m, d in metas:
            if m["pwm_setpoint"] != pwm or not d.split("/")[-1].startswith(run):
                continue
            L = band_levels(os.path.join(d, "audio.wav"), cals.get(m["calibration_file_id"]))
            obs.append((name, float(m["elevation_deg"]), m["calibration_file_id"], L))
    return obs


def fit(obs, rotated: set[str]):
    runs = sorted({o[0] for o in obs})
    poss = sorted({o[1] for o in obs})
    sers = sorted({o[2] for o in obs})
    n = len(runs) + len(poss) + len(sers)
    A = np.zeros((len(obs), n))
    Y = np.array([o[3] for o in obs])
    for i, (r, e, s, _) in enumerate(obs):
        p = -e if r in rotated else e
        A[i, runs.index(r)] = 1
        A[i, len(runs) + poss.index(p)] = 1
        A[i, len(runs) + len(poss) + sers.index(s)] = 1
    c1 = np.zeros(n)
    c1[len(runs) : len(runs) + len(poss)] = 10
    c2 = np.zeros(n)
    c2[len(runs) + len(poss) :] = 10
    X = np.linalg.lstsq(np.vstack([A, c1, c2]), np.vstack([Y, np.zeros((2, Y.shape[1]))]), rcond=None)[0]
    R = Y - A @ X
    return runs, poss, sers, X[len(runs) : len(runs) + len(poss)], X[len(runs) + len(poss) :], R


def detect_rotated(obs) -> set[str]:
    band = [i for i, f in enumerate(THIRD_OCT) if 500 <= f <= 2000]
    runs = sorted({o[0] for o in obs})
    rot: set[str] = set()

    def rms(r):
        return np.sqrt(np.mean(fit(obs, r)[5][:, band] ** 2))

    best = rms(rot)
    improved = True
    while improved:
        improved = False
        for r in runs:
            trial = rot ^ {r}
            v = rms(trial)
            if v < best - 0.05:
                rot, best, improved = trial, v, True
    return rot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--glob", required=True)
    ap.add_argument("--pwm", type=int, default=1900)
    ap.add_argument("--rotated", nargs="*", default=None, help="run names (the key's notes field) measured with the arc turned 180 deg")
    ap.add_argument("--detect-rotated", action="store_true", help="guess rotated runs from the data (greedy on the 500-2 kHz residual; fragile with mixed setups)")
    ap.add_argument("--exclude", nargs="*", default=[], help="run names to leave out")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    obs = load_runs(a.data, a.glob, a.pwm, set(a.exclude))
    if not obs:
        sys.exit("no runs matched")
    rot = set(a.rotated or [])
    if a.detect_rotated:
        rot = detect_rotated(obs)
        print("WARNING: rotated runs guessed from the data; confirm against the lab notes")
    runs, poss, sers, P, M, R = fit(obs, rot)
    hdr = " ".join(f"{f:6.0f}" for f in THIRD_OCT)
    print(f"runs: {runs}\nrotated: {sorted(rot)}\n")
    print("ARC ERROR MAP, dB from a circle per physical position (mic offsets removed)")
    print(f"{'pos':>5} {hdr}   RMS")
    for i, p in enumerate(poss):
        print(f"{p:>+5.0f} " + " ".join(f"{v:+6.1f}" for v in P[i]) + f"  {np.sqrt(np.mean(P[i] ** 2)):4.1f}")
    print(f"{'res':>5} " + " ".join(f"{np.sqrt(np.mean(R[:, j] ** 2)):6.1f}" for j in range(len(THIRD_OCT))) + "   (run-to-run residual)")
    print("\nMIC OFFSETS after calibration, dB")
    for i, s in enumerate(sers):
        print(f"{s:>8} " + " ".join(f"{v:+6.1f}" for v in M[i]) + f"  {np.sqrt(np.mean(M[i] ** 2)):4.1f}")
    os.makedirs(a.out, exist_ok=True)
    head = "," + ",".join(f"{f:.0f}Hz" for f in THIRD_OCT)
    np.savetxt(os.path.join(a.out, "arc-error-map-third-octave.csv"), np.column_stack([poss, P]), delimiter=",", header="position_deg" + head, comments="", fmt="%.2f")
    np.savetxt(os.path.join(a.out, "mic-offsets-third-octave.csv"), np.column_stack([[int(s) for s in sers], M]), delimiter=",", header="serial" + head, comments="", fmt="%.2f")
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        _fig, ax = plt.subplots(1, 2, figsize=(14, 5.5))
        for k, (Z, ylab, title) in enumerate(
            [(P, [f"{p:+.0f}°" for p in poss], "Arc error map: dB from a circle (mic offsets removed)"), (M, sers, "Mic offsets after calibration")]
        ):
            im = ax[k].imshow(Z, aspect="auto", cmap="RdBu_r", vmin=-5, vmax=5, origin="lower")
            ax[k].set_yticks(range(len(ylab)))
            ax[k].set_yticklabels(ylab)
            ax[k].set_xticks(range(len(THIRD_OCT)))
            ax[k].set_xticklabels([f"{f:.0f}" for f in THIRD_OCT], rotation=90)
            ax[k].set_title(title)
            plt.colorbar(im, ax=ax[k], label="dB")
        plt.tight_layout()
        plt.savefig(os.path.join(a.out, "arc-error-map.png"), dpi=110)
    except ImportError:
        pass


if __name__ == "__main__":
    main()
