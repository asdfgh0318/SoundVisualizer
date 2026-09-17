#!/usr/bin/env python3
"""Fig. 1 of the one-pager: the room error as a polar, at four bands.

Reads the position map that arc_error_map.py writes, so it always matches whatever
fit produced that map (since 2026-09-17 that is the fit with no microphone term).
"""

from __future__ import annotations

import argparse
import csv
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

BANDS = [(250, "250 Hz"), (794, "800 Hz"), (3175, "3.15 kHz"), (6350, "6.3 kHz (clean)")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", default="docs/analysis/arc-error-map-third-octave.csv")
    ap.add_argument("--out", default="docs/analysis/brief-fig1-polars.png")
    a = ap.parse_args()

    rows = list(csv.reader(open(a.map)))
    freqs = [float(h.replace("Hz", "")) for h in rows[0][1:]]
    P = {float(r[0]): np.array([float(x) for x in r[1:]]) for r in rows[1:] if r and r[0].strip()}
    spots = sorted(P)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4.3), dpi=110,
                             subplot_kw={"projection": "polar"})
    for ax, (fc, label) in zip(axes, BANDS):
        i = int(np.argmin([abs(f - fc) for f in freqs]))
        th = np.radians(spots)
        r = np.array([P[s][i] for s in spots])
        ax.set_theta_zero_location("E")
        ax.set_thetamin(-90); ax.set_thetamax(90)
        ax.plot(th, r, "-o", color="#a33", ms=4.5, lw=1.6)
        ax.plot(np.radians(np.linspace(-90, 90, 181)), np.zeros(181), "--", color="#333", lw=1)
        ax.set_ylim(-10.5, 8)
        ax.set_yticks([-9, -6, -3, 0, 3, 6])
        ax.set_yticklabels(["−9", "−6", "−3", "0", "+3", "+6"], fontsize=9)
        ax.set_thetagrids(spots, [f"{s:+.0f}°" for s in spots], fontsize=9)
        ax.set_title(label, fontsize=13, pad=14)
        ax.grid(color="#ccc", lw=0.7)
        for s, v in zip(spots, r):
            if abs(v) >= 3.4:
                ax.annotate(f"{v:+.1f}", (np.radians(s), v), textcoords="offset points",
                            xytext=(4, 4), fontsize=9, color="#a33")
    fig.text(0.5, 0.005,
             "Fig. 1 · room error P(position), dB from a circle, capsule corrections measured on a "
             "bench and removed before the fit · 12 captures: keys "
             "dp1-baseline-horizontal-prop7…prop18, PWM 1900 step (ids in the table below)",
             ha="center", fontsize=10, color="#444")
    fig.tight_layout(rect=(0, 0.085, 1, 0.94))
    fig.savefig(a.out)
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
