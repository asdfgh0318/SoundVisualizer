"""Split the arc's position map into what travels with the rig and what stays in the room.

The arc was measured, physically flipped, and measured again with nothing else
touched. Both runs are indexed by LABEL, and a capsule keeps its label through the
flip, so with m = mirror about the equator

    A_p = X_p + Y_p        before
    C_p = X_p + Y_m(p)     after: same capsule, the room swapped underneath it

X travels with the capsule (its clamp, its cable, its place on the frame), Y stays
in the room. Un-flipping the second run, C'_q = C_m(q), gives the two useful views:

    rig  = (A + C ) / 2 = X + Y_sym
    room = (A + C') / 2 = Y + X_sym

Each panel shows its own subject WHOLE -- all of the room's asymmetry is in the
room panel -- contaminated only by the other's mirror-symmetric part. Do not plot
(A - C)/2 and call it the room: that is only Y's antisymmetric half, and it looks
antisymmetric because the arithmetic made it so, not because the room is.

Two runs cannot go further than this. Of the four unknowns X_sym, X_anti, Y_sym,
Y_anti the flip determines three: X_anti = 0.21 dB rms is provably the rig,
Y_anti = 1.04 dB is provably the room, and X_sym + Y_sym = 0.84 dB is shared
between them with no way to divide it. Breaking that last tie needs a different
move on the room (move the source, or move the arc off the symmetry plane), not
another flip.
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
    X, Y = (A + C) / 2, (A + C[::-1]) / 2
    anti = lambda D: (D - D[::-1]) / 2
    rms = lambda D: float(np.sqrt((D ** 2).mean()))
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
            (X, "the rig — capsule, clamp, cable, place on the frame  (+ the room's mirror-symmetric part)"),
            (Y, "the room — whole, asymmetry and all  (+ the rig's mirror-symmetric part)"))):
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
    for D, col, lab in ((X, "#c25e00", "the rig"), (Y, "#2f6f9f", "the room")):
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

    fig.suptitle("The arc was flipped: the rig against the room",
                 color=INK, fontsize=13, fontweight="600", x=0.085, ha="left", y=0.985)
    fig.text(0.085, 0.938,
             ("per-capsule calibration applied · " if calA and calC else "RAW dBFS · ")
             + "same room, same source, arc physically inverted · rig = (before + after)/2, "
             "room = (before + after un-flipped)/2\n"
             f"whole panels, {rms(X):.2f} and {rms(Y):.2f} dB rms — but only their antisymmetric parts are "
             f"attributable: {rms(anti(X)):.2f} dB provably rig, {rms(anti(Y)):.2f} dB provably room, "
             f"{rms((X + X[::-1]) / 2):.2f} dB shared and undividable",
             color=MUTED, fontsize=9, ha="left", linespacing=1.5)
    fig.tight_layout(rect=(0, 0, 1, 0.915))
    out = Path(sys.argv[1])
    fig.savefig(out, facecolor="white")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
