import json, re, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

CAL = Path("/home/adam/ŻYCIE/PRACA/SoundVisualizer-data/data/calibrations")
S = Path("calibrator/sessions/2026-09-16")
INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"
C_MEAS, C_FACT = "#2f6f9f", "#c25e00"

def factory(ser):
    lines = (CAL / f"{ser}.txt").read_text().splitlines()
    f, g = [], []
    for ln in lines[1:]:
        p = ln.split()
        if len(p) >= 2:
            try: f.append(float(p[0])); g.append(float(p[1]))
            except ValueError: pass
    return np.array(f), np.array(g)

def meas(n):
    return {r["freq"]: r["level_dbfs"]
            for r in json.load(open(S / n / "levels.json")) if "error" not in r}

REF = meas("m-810-8904__4"); fref, gref = factory("8108904")
CAPS = [("811-1896", "8111896", "m-811-1896"),
        ("810-8903", "8108903", "m-810-8903"),
        ("810-8900", "8108900", "m-810-8900")]

fig, axes = plt.subplots(3, 1, figsize=(10.5, 9.4), dpi=170, sharex=True)
fig.patch.set_facecolor("white")

for ax, (lab, ser, run) in zip(axes, CAPS):
    d = meas(run); fs = sorted(set(d) & set(REF))
    ff, gg = factory(ser)
    i1k = int(np.argmin([abs(x - 1000) for x in fs]))
    fac = np.interp(fs, ff, gg) - np.interp(fs, fref, gref); fac -= fac[i1k]
    mm = np.array([d[x] - REF[x] for x in fs]); mm -= mm[i1k]
    ax.axhspan(-0.3, 0.3, color="#f2f4f6", zorder=0)
    ax.axhline(0, color="#9aa3ab", lw=1, zorder=1)
    ax.plot(fs, fac, color=C_FACT, lw=1.8, ls=(0, (5, 3)), zorder=3, label="factory cal file")
    ax.plot(fs, mm, color=C_MEAS, lw=1.8, zorder=4, label="our measurement")
    ax.plot(fs, mm, "o", color=C_MEAS, ms=2.8, mec="white", mew=0.5, zorder=5)
    ax.set_facecolor("white"); ax.grid(True, color=GRID, lw=0.8, zorder=2)
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    for s_ in ("left", "bottom"): ax.spines[s_].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.set_ylim(-2.4, 2.4); ax.set_ylabel("dB re 1 kHz", color=MUTED, fontsize=9)
    ax.set_title(f"{lab}  vs  810-8904", color=INK, fontsize=10.5, fontweight="600",
                 loc="left", pad=8)

axes[0].annotate("agreement within ~0.2 dB", (300, -0.1), textcoords="offset points",
                 xytext=(0, -34), ha="center", fontsize=8.8, color=MUTED,
                 arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
axes[0].annotate("measured runs high here in all three —\ncommon-mode, so it is the reference run,\nnot the capsules", (5040, 0.6),
                 textcoords="offset points", xytext=(-24, 36), ha="right", fontsize=8.5,
                 color=MUTED, linespacing=1.4,
                 arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
leg = axes[0].legend(frameon=False, loc="lower left", fontsize=9)
for t in leg.get_texts(): t.set_color(INK)

ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
for ax in axes:
    ax.set_xscale("log"); ax.set_xlim(55, 19000)
    ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(FixedLocator([]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}"))
axes[-1].set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)

fig.suptitle("Our substitution measurement against miniDSP's factory calibration",
             color=INK, fontsize=12.5, fontweight="600", x=0.055, ha="left", y=0.985)
fig.text(0.055, 0.958, "both curves normalised at 1 kHz, so this compares SHAPE only — "
         "the absolute offsets are in the Sens Factor table",
         color=MUTED, fontsize=8.8, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.945))
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
