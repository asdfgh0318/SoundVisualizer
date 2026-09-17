"""Split the arc's position map into what travels with the rig and what stays in the room.

The arc was measured, physically flipped, and measured again with nothing else
touched. A component fixed to the capsule (its clamp, its cable, its place on the
frame) reads the same at the same label before and after; a component fixed to the
room swaps between mirrored labels. So with A = before and C = after,

    X = (A + C) / 2   travels with the arc
    Y = (A - C) / 2   stays in the room

and the model is testable rather than assumed: C - A has to come out antisymmetric,
which it does to 2.07 dB of 2.10.

What the split can and cannot prove. Y is purely the room, but only its
ANTISYMMETRIC half: any part of the room that is already mirror-symmetric about
the equator cancels out of A - C and lands in X. So X is the arc plus the
symmetric part of the room, and only X's own antisymmetric part is provably the
arc. Calibrated budget: 0.21 dB rms provably rig, 1.05 dB rms provably room,
0.84 dB rms ambiguous. The antisymmetry of A - C is forced by the arithmetic and
is a consistency check, not evidence.
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from calibrator.rig import read_map

INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"
S = Path("calibrator/sessions/2026-09-17")


def dev(run):
    f, pos, L, calibrated = read_map(S / run)
    return f, pos, (L - L.mean(axis=1, keepdims=True)).T, calibrated


def main() -> int:
    f, pos, A, calA = dev("full-rig")
    _, _, C, calC = dev("flipped")
    X, Y = (A + C) / 2, (A - C) / 2
    lim = float(max(np.abs(X).max(), np.abs(Y).max()))

    fig = plt.figure(figsize=(13.5, 8.6), dpi=170)
    fig.patch.set_facecolor("white")
    gs = fig.add_gridspec(3, 2, height_ratios=[2.2, 2.2, 1.25], width_ratios=[1, 0.02],
                          hspace=0.42, wspace=0.03)
    edges = np.empty(len(f) + 1)
    edges[1:-1] = np.sqrt(f[:-1] * f[1:])
    edges[0] = f[0] ** 2 / edges[1]
    edges[-1] = f[-1] ** 2 / edges[-2]
    ticks = [t for t in (315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500,
                         3150, 4000, 5000, 6300) if f.min() <= t <= f.max()]
    fmt = FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}")

    axes = []
    for row, (D, title) in enumerate((
            (X, "X — the arc (capsule, clamp, cable, place on the frame) PLUS the mirror-symmetric part of the room"),
            (Y, "Y — the room, but only its mirror-antisymmetric part"))):
        ax = fig.add_subplot(gs[row, 0])
        im = ax.pcolormesh(edges, np.arange(len(pos) + 1), D, cmap="RdBu_r",
                           vmin=-lim, vmax=lim, shading="flat")
        ax.set_yticks(np.arange(len(pos)) + 0.5)
        ax.set_yticklabels([f"{p:+.0f}°" for p in pos], fontsize=8.5)
        ax.set_title(title, color=INK, fontsize=10.5, fontweight="600", loc="left", pad=7)
        cax = fig.add_subplot(gs[row, 1])
        cb = fig.colorbar(im, cax=cax)
        cb.set_label("dB", color=MUTED, fontsize=8.5)
        cb.ax.tick_params(colors=MUTED, labelsize=8)
        axes.append(ax)

    bx = fig.add_subplot(gs[2, 0])
    for D, col, lab in ((X, "#c25e00", "X — arc + symmetric room"), (Y, "#2f6f9f", "Y — antisymmetric room")):
        bx.plot(f, np.sqrt((D ** 2).mean(axis=0)), color=col, lw=1.8, label=lab)
    bx.axhline(0.026, color="#9aa3ab", lw=1.2, ls=(0, (4, 3)))
    bx.annotate("run-to-run noise, 0.03 dB", (f[0], 0.026), textcoords="offset points",
                xytext=(6, 7), ha="left", fontsize=8.5, color=MUTED)
    bx.set_ylabel("rms over the\neleven positions (dB)", color=MUTED, fontsize=9)
    bx.set_ylim(0, None)
    leg = bx.legend(frameon=False, loc="upper right", fontsize=9.5)
    for t in leg.get_texts():
        t.set_color(INK)
    axes.append(bx)

    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlim(f.min() * 0.97, f.max() * 1.03)
        ax.xaxis.set_major_locator(FixedLocator(ticks))
        ax.xaxis.set_minor_locator(FixedLocator([]))
        ax.xaxis.set_major_formatter(fmt)
        ax.tick_params(colors=MUTED, labelsize=8.5, length=0)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(GRID)
    for ax in axes[:2]:
        for t in ticks:
            ax.axvline(t, color="#ffffff", lw=0.6, alpha=0.45, zorder=4)
    bx.grid(True, color=GRID, lw=0.8)
    bx.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)

    fig.suptitle("The arc was flipped: what that can and cannot separate",
                 color=INK, fontsize=13, fontweight="600", x=0.085, ha="left", y=0.985)
    fig.text(0.085, 0.938,
             ("per-capsule calibration applied · " if calA and calC else "RAW dBFS · ")
             + "same room, same source, arc physically inverted · X = (before+after)/2, "
             "Y = (before−after)/2\nonly the antisymmetric parts are attributable: 0.21 dB rms "
             "provably rig, 1.05 dB provably room, 0.84 dB ambiguous",
             color=MUTED, fontsize=9, ha="left", linespacing=1.5)
    fig.tight_layout(rect=(0, 0, 1, 0.915))
    out = Path(sys.argv[1])
    fig.savefig(out, facecolor="white")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
