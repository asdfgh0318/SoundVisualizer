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

    # Which capsules actually sat at each PHYSICAL spot, over the twelve core runs.
    # Not one capsule per spot: turning the arc for prop11-14 mirrors every capsule to
    # the opposite spot, and 811-1892/810-8901 were swapped outright between prop10 and
    # prop11. The row label has to say so, or the left panel looks like a property of
    # one capsule when it is a property of up to three.
    import collections
    import json
    import re
    pack = json.load(open("docs/analysis/arc-validation-data.json"))
    occ = collections.defaultdict(lambda: collections.defaultdict(list))
    for name in sorted(pack["core_runs"], key=lambda n: int(re.sub(r"\D", "", n))):
        r = pack["runs"][name]
        for e, mi in r["mics"].items():
            occ[-int(e) if r["flipped"] else int(e)][mi["serial"]].append(
                name.replace("prop", ""))
    at = {k: max(v.items(), key=lambda kv: len(kv[1]))[0] for k, v in occ.items()}

    def rowlabel(spot: int) -> str:
        """`+72°  811-1892 · 8901 15-18 · 1896 11-14` — who sat there, and when."""
        runs = occ[spot]
        main = at[spot]
        extra = [f"{s[-4:]} {v[0]}–{v[-1]}" for s, v in
                 sorted(runs.items(), key=lambda kv: -len(kv[1]))[1:]]
        return f"{spot:+.0f}°  {main}" + ("  · " + " · ".join(extra) if extra else "  (never moved)")

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
    fig, axes = plt.subplots(1, 2, figsize=(18.5, 4.8), dpi=110)
    for ax, D, title, labels in (
        (axes[0], M, "What the bench measured and removed, dB — row = the capsule that sat there most",
         [rowlabel(int(float(s))) for s in spots]),
        (axes[1], R, "Room term P, dB from a circle at that spot — no mic term in the fit",
         [f"{float(s):+.0f}°" for s in spots]),
    ):
        ax.imshow(D, cmap="RdBu_r", vmin=-lim, vmax=lim, aspect="auto")
        ax.set_xticks(range(len(THIRD_OCT)))
        ax.set_xticklabels([f"{f:.0f}" for f in THIRD_OCT], rotation=90, fontsize=8)
        ax.set_yticks(range(len(spots))); ax.set_yticklabels(labels, fontsize=7.4)
        ax.set_title(title, fontsize=11)
        for i in range(D.shape[0]):
            for j in range(D.shape[1]):
                v = D[i, j]
                if abs(v) >= 0.05:
                    ax.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=6.0,
                            color="white" if abs(v) > 3.2 else "#222")
    fig.colorbar(axes[1].images[0], ax=axes[1], label="dB")
    fig.text(0.5, 0.055,
             "Fig. 2 · left: the substitution session of 16 Sept 2026, folded into each capsule's "
             "calibration file. Row labels name the capsule that occupied that spot in most runs, "
             "then the others with their run numbers.",
             ha="center", fontsize=8.5, color="#444")
    fig.text(0.5, 0.008,
             "prop11–14 were measured with the arc turned 180°, mirroring every capsule to the "
             "opposite spot; 811-1892 and 810-8901 were swapped outright after prop10, the only "
             "swap in the campaign.\nRight: one fit over prop7…prop18, PWM 1900, no microphone "
             "term · third-octave centre, Hz",
             ha="center", fontsize=8.5, color="#444")
    fig.tight_layout(rect=(0, 0.10, 1, 1))
    fig.savefig(a.out)
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
