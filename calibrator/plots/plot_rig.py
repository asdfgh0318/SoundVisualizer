"""Whole-arc tone grid: what each position reads, relative to the eleven-capsule mean.

Every capsule is equidistant from a hub source with the arc flat, so a perfect rig
would read the same everywhere and this map would be blank. Referencing each column
to its own eleven-capsule mean removes the source and the electronics entirely —
whatever is left belongs to a position: the room, the arc hardware, the neighbouring
capsules, or residual capsule error.
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from calibrator.rig import SOURCE_SUSPECT_HZ, read_map

INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"


def main() -> int:
    run = Path(sys.argv[1])
    out = Path(sys.argv[2])
    meta = json.loads((run / "meta.json").read_text())
    f, posf, L, calibrated = read_map(run)
    pos = [f"{p:+.0f}" for p in sorted(posf, reverse=True)]
    L = L[:, [sorted(posf).index(float(p)) for p in pos]]
    D = (L - np.nanmean(L, axis=1, keepdims=True)).T          # position x frequency
    spread = np.nanmax(L, axis=1) - np.nanmin(L, axis=1)
    lim = float(np.nanmax(np.abs(D)))

    fig, (ax, bx) = plt.subplots(2, 1, figsize=(13, 7.1), dpi=170, sharex=True,
                                 gridspec_kw={"height_ratios": [2.6, 1], "hspace": 0.13})
    fig.patch.set_facecolor("white")

    # cell edges in frequency: geometric midpoints, so a log axis shows equal-width cells
    edges = np.empty(len(f) + 1)
    edges[1:-1] = np.sqrt(f[:-1] * f[1:])
    edges[0] = f[0] ** 2 / edges[1]
    edges[-1] = f[-1] ** 2 / edges[-2]
    im = ax.pcolormesh(edges, np.arange(len(pos) + 1), D,
                       cmap="RdBu_r", vmin=-lim, vmax=lim, shading="flat")
    ax.set_yticks(np.arange(len(pos)) + 0.5)
    ax.set_yticklabels([f"{float(p):+.0f}°" for p in pos], fontsize=9)
    ax.set_ylabel("position on the arc", color=MUTED, fontsize=9.5)
    cb = fig.colorbar(im, ax=ax, pad=0.012)
    cb.set_label("dB re the eleven-capsule mean", color=MUTED, fontsize=9)
    cb.ax.tick_params(colors=MUTED, labelsize=8.5)

    bx.plot(f, spread, color="#2f6f9f", lw=1.7)
    bx.fill_between(f, 0, spread, color="#2f6f9f", alpha=0.12)
    bx.set_ylabel("spread, max−min (dB)", color=MUTED, fontsize=9.5)
    bx.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
    bx.set_ylim(0, max(12.5, spread.max() * 1.1))

    # Third-octave centres: the frequencies these maps are always read in, and dense
    # enough that a cell can be traced to a frequency without counting columns.
    ticks = [t for t in (250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000,
                         2500, 3150, 4000, 5000, 6300) if f.min() <= t <= f.max()]
    fmt = FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}")
    lo, hi = SOURCE_SUSPECT_HZ
    shade = f.min() < hi and f.max() > lo
    if shade:
        # On the map an axvspan hides under the mesh, so mark the band with rules.
        for t in (max(lo, f.min()), min(hi, f.max())):
            ax.axvline(t, color="#b00020", lw=1.2, alpha=0.75, zorder=5)
        bx.axvspan(max(lo, f.min()), min(hi, f.max()), color="#b00020", alpha=0.09, zorder=0)
    for a in (ax, bx):
        a.set_xscale("log")
        a.set_xlim(f.min() * 0.97, f.max() * 1.03)
        a.xaxis.set_major_locator(FixedLocator(ticks))
        a.xaxis.set_minor_locator(FixedLocator([]))
        a.xaxis.set_major_formatter(fmt)
        a.tick_params(colors=MUTED, labelsize=9, length=0)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            a.spines[s].set_color(GRID)
    # the heatmap carries its own frequency scale, on top, so the reader never has to
    # look three inches away to find out which column is which
    ax.tick_params(axis="x", labelbottom=False, labeltop=True, labelsize=8.5)
    ax.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
    ax.xaxis.set_label_position("top")
    for t in ticks:
        ax.axvline(t, color="#ffffff", lw=0.6, alpha=0.45, zorder=4)
    bx.grid(True, color=GRID, lw=0.8)
    for hz in (653, 1958, 3263):
        for a in (ax, bx):
            a.axvline(hz, color="#9aa3ab", lw=1, ls=(0, (4, 3)), zorder=5)

    ax.annotate("every capsule is equidistant from the source, so a perfect rig would be blank · "
                + ("per-capsule calibration applied"
                   if calibrated else "RAW dBFS — capsules NOT calibrated"),
                xy=(0, 1), xycoords="axes fraction", xytext=(0, 30),
                textcoords="offset points", ha="left", va="bottom",
                color=MUTED, fontsize=8.8)
    if shade:
        bx.annotate(f"{lo:.0f}–{hi:.0f} Hz: the sphere's driver rocks here (m = 1, 11 dB at 4362 Hz) "
                    f"— these tones read the loudspeaker, not the rig",
                    xy=(0, 1), xycoords="axes fraction", xytext=(0, 6),
                    textcoords="offset points", ha="left", va="bottom",
                    color="#b00020", fontsize=8.5)
    ax.annotate(f"{len(f)} tones, {f.min():.0f}–{f.max():.0f} Hz",
                xy=(1, 1), xycoords="axes fraction", xytext=(0, 30),
                textcoords="offset points", ha="right", va="bottom",
                color=MUTED, fontsize=8.5)
    fig.suptitle(f"{meta['label']} — whole arc, hub source, amplitude {meta['amplitude']}",
                 color=INK, fontsize=12.5, fontweight="600", x=0.105, ha="left", y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.925))
    fig.savefig(out, facecolor="white")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
