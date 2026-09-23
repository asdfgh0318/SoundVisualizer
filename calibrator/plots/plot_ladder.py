"""Four interventions, one thing changed each time. The whole one-pager in one figure."""
import sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter
sys.path.insert(0, "/home/adam/ŻYCIE/PRACA/SoundVisualizer")
from calibrator.rig import SOURCE_SUSPECT_HZ, read_map

INK, MID, MUT, GRID = "#14181d", "#4b5563", "#6b7280", "#e3e7ec"
OK, BAD = "#2f7d32", "#b00020"
S = Path("calibrator/sessions/2026-09-17")

def dev(r):
    f, pos, L, _ = read_map(S / r)
    return f, pos, (L - L.mean(axis=1, keepdims=True)).T

f, pos, A = dev("full-rig")
_, _, A2 = dev("full-rig-2")
_, _, C  = dev("flipped")
_, _, V  = dev("vertical")
_, _, B  = dev("roll-B")
_, _, D  = dev("driver-180")

rms = lambda X: float(np.sqrt((X**2).mean()))
def r_of(X, Y): return float(np.corrcoef(X.ravel(), Y.ravel())[0, 1])


rows = [
    ("1", "Nothing changed", "the same capture twice, 20 min apart",
     A, "arc flat · sphere at the centre, firing up", A2, "same rig, 20 min later",
     f"{rms(A-A2):.2f} dB", f"r = {r_of(A,A2):+.2f}", OK,
     "the instrument is silent when nothing moves"),
    ("2", "The arc flipped 180°", "second run re-indexed by physical position",
     A, "arc flat · +90° end to the left", C[::-1], "arc turned 180°, read by physical position",
     f"{rms(A-C[::-1]):.2f} dB", f"r = {r_of(A,C[::-1]):+.2f}", OK,
     "the pattern stayed with the room, not with the arc"),
    ("3", "The arc stood vertical", "same capsules and cables, different room",
     A, "arc flat · sphere firing up", V, "arc standing · sphere firing sideways",
     f"{rms(A-V):.2f} dB", f"r = {r_of(A,V):+.2f}", BAD,
     "change the room and the map is unrecognisable"),
    ("4", "Only the driver turned 180°", "in a sphere that never moved",
     B, "arc standing · driver at 0°", D, "same rig · driver remounted 180°",
     "0.20 dB", "below 3 kHz", OK,
     "and 11.0 dB at 4362 Hz — the source's own rocking mode"),
]

lim = 5.0
lo, hi = SOURCE_SUSPECT_HZ
fig = plt.figure(figsize=(8.0, 9.28), dpi=300)
fig.patch.set_facecolor("white")
gs = fig.add_gridspec(len(rows), 3, width_ratios=[1, 1, 0.022],
                      hspace=0.72, wspace=0.045,
                      left=0.075, right=0.945, top=0.845, bottom=0.046)
edges = np.empty(len(f) + 1)
edges[1:-1] = np.sqrt(f[:-1]*f[1:]); edges[0] = f[0]**2/edges[1]; edges[-1] = f[-1]**2/edges[-2]
ticks = [315, 500, 800, 1250, 2000, 3150, 5000]
fmt = FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}")


for i, (num, title, sub, M1, l1, M2, l2, big, small, col, verdict) in enumerate(rows):
    axes = []
    for j, (M, lab) in enumerate(((M1, l1), (M2, l2))):
        ax = fig.add_subplot(gs[i, j])
        im = ax.pcolormesh(edges, np.arange(len(pos)+1), M, cmap="RdBu_r", vmin=-lim, vmax=lim)
        ax.set_title(lab, color=MID, fontsize=6.8, loc="left", pad=2.8)
        ax.set_yticks([0.5, 5.5, 10.5])
        ax.set_yticklabels(["−90°", "0°", "+90°"] if j == 0 else [], fontsize=5.4)
        for x in (lo, hi):
            ax.axvline(x, color=BAD, lw=0.5, alpha=0.55, zorder=5)
        ax.set_xscale("log"); ax.set_xlim(f.min()*0.98, f.max()*1.02)
        ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(FixedLocator([]))
        ax.xaxis.set_major_formatter(fmt)
        ax.tick_params(colors=MUT, labelsize=5.4, length=0, pad=1.6)
        if i < len(rows) - 1: ax.set_xticklabels([])
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        for s in ("left", "bottom"): ax.spines[s].set_color(GRID); ax.spines[s].set_linewidth(0.4)
        axes.append(ax)
    cax = fig.add_subplot(gs[i, 2]); cb = fig.colorbar(im, cax=cax)
    cb.set_ticks([-5, 0, 5]); cb.ax.tick_params(colors=MUT, labelsize=4.8, length=0, pad=1)
    cb.outline.set_visible(False)

    y = axes[0].get_position().y1
    fig.text(0.075, y + 0.0385, f"{num}", color=col, fontsize=11, fontweight="700", va="bottom")
    fig.text(0.098, y + 0.0385, title, color=INK, fontsize=9.2, fontweight="700", va="bottom")
    fig.text(0.098, y + 0.0275, sub, color=MUT, fontsize=6.6, va="bottom")
    fig.text(0.945, y + 0.0385, big, color=col, fontsize=11, fontweight="700", va="bottom", ha="right")
    fig.text(0.945, y + 0.0275, small, color=MUT, fontsize=6.6, va="bottom", ha="right")
    yb = axes[0].get_position().y0
    fig.text(0.075, yb - 0.021, verdict, color=MID, fontsize=7.1, style="italic", va="top")

fig.text(0.075, 0.962, "Change one thing at a time", color=INK, fontsize=14.5, fontweight="700")
fig.text(0.075, 0.9455,
         "Eleven UMIK-2 capsules on a 1.68 m arc · 112 tones, 257–6350 Hz · each cell is one capsule at "
         "one tone, dB re the eleven-capsule mean",
         color=MUT, fontsize=6.8)
fig.text(0.075, 0.9295,
         "per-capsule calibration applied · red rules mark 3–5 kHz, where the source is not axisymmetric",
         color=MUT, fontsize=6.8)
fig.text(0.075, 0.9135,
         "the sphere sits on a tripod at the centre of the arc and fires along its axis, so every capsule "
         "is the same distance away and at the same angle to it",
         color=MUT, fontsize=6.8)
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
