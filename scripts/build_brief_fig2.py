#!/usr/bin/env python3
"""Fig. 2 of the one-pager: what the bench took out, and what the room leaves behind.

Until 2026-09-16 the left panel was the microphone term M *estimated by the arc fit*
alongside the room term P — which is exactly the pair the five-cluster degeneracy
could not separate. The capsules have since been measured against each other on a
bench, so the left panel is now the correction that measurement put into each cal
file, and the right panel is the room term from a fit with no microphone term at all.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from server.core.calibration import parse_umik_calibration  # noqa: E402

THIRD_OCT = [125 * 2 ** (i / 3) for i in range(19)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cal", default="../SoundVisualizer-data/data/calibrations")
    ap.add_argument("--backup", default="factory-originals-2026-09-16")
    ap.add_argument("--map", default="docs/analysis/arc-error-map-third-octave.csv")
    ap.add_argument("--out", default="docs/analysis/brief-fig2-errormap.png")
    a = ap.parse_args()

    rows = list(csv.reader(open(a.map)))
    P = {r[0]: np.array([float(x) for x in r[1:]]) for r in rows[1:] if r and r[0].strip()}
    spots = sorted(P, key=float, reverse=True)

    # which capsule sits at which spot, from the data pack's arc_map
    import json
    pack = json.load(open("docs/analysis/arc-validation-data.json"))
    at = {int(k): v for k, v in pack["arc_map"].items()}

    delta = {}
    for ser in set(at.values()):
        new = parse_umik_calibration(open(os.path.join(a.cal, f"{ser}.txt")).read())
        old = parse_umik_calibration(open(os.path.join(a.cal, a.backup, f"{ser}.txt")).read())
        delta[ser] = np.array([
            np.interp(f, new.freq_hz, new.gain_db) - np.interp(f, old.freq_hz, old.gain_db)
            for f in THIRD_OCT])

    M = np.array([delta[at[int(float(s))]] for s in spots])
    R = np.array([P[s] for s in spots])
    lim = 6.0
    fig, axes = plt.subplots(1, 2, figsize=(19, 4.6), dpi=110)
    for ax, D, title, labels in (
        (axes[0], M, "What the bench measured and removed, dB (row = its spot)",
         [f"{float(s):+.0f}°  {at[int(float(s))]}" for s in spots]),
        (axes[1], R, "Room term P, dB from a circle at that spot — no mic term in the fit",
         [f"{float(s):+.0f}°" for s in spots]),
    ):
        ax.imshow(D, cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto")
        ax.set_xticks(range(len(THIRD_OCT)))
        ax.set_xticklabels([f"{f:.0f}" for f in THIRD_OCT], rotation=90, fontsize=8)
        ax.set_yticks(range(len(spots))); ax.set_yticklabels(labels, fontsize=8)
        ax.set_title(title, fontsize=11)
        for i in range(D.shape[0]):
            for j in range(D.shape[1]):
                v = D[i, j]
                if abs(v) >= 0.05:
                    ax.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=6.0,
                            color="white" if abs(v) > 3.2 else "#222")
    fig.colorbar(axes[1].images[0], ax=axes[1], label="dB")
    fig.text(0.5, 0.005,
             "Fig. 2 · left: the substitution session of 16 Sept 2026, folded into each "
             "capsule's calibration file · right: one fit over keys "
             "dp1-baseline-horizontal-prop7…prop18, PWM 1900, prop11–14 mirrored, "
             "no microphone term · third-octave centre, Hz",
             ha="center", fontsize=9, color="#444")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(a.out)
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
