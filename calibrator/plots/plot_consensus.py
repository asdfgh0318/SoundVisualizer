import json, re, itertools, statistics, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter

CAL = Path("/home/adam/ŻYCIE/PRACA/SoundVisualizer-data/data/calibrations")
S = Path("calibrator/sessions/2026-09-16")
INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"
CAPS = [("810-8904", "8108904", "m-810-8904__4", "#2f6f9f"),
        ("811-1896", "8111896", "m-811-1896",    "#c25e00"),
        ("810-8903", "8108903", "m-810-8903",    "#8c5ab8"),
        ("810-8900", "8108900", "m-810-8900",    "#4b8b3b"),
        ("811-2310", "8112310", "m-811-2310",    "#9c2f6f"),
        ("810-8897", "8108897", "m-810-8897",    "#4a5560")]

def sens(ser):
    return float(re.search(r"Sens Factor\s*=\s*(-?[\d.]+)",
                           (CAL/f"{ser}.txt").read_text().splitlines()[0]).group(1))
def lv(n):
    return {r["freq"]: r["level_dbfs"]
            for r in json.load(open(S/n/"levels.json")) if "error" not in r}

L = {c[0]: lv(c[2]) for c in CAPS}
SF = {c[0]: sens(c[1]) for c in CAPS}
common = sorted(set.intersection(*[set(v) for v in L.values()]))

# Consensus datum: at each frequency the mean across capsules. No capsule is privileged.
meas = {k: np.array([L[k][f] for f in common]) for k in L}
mbar = np.mean([meas[k] for k in L], axis=0)
meas = {k: meas[k] - mbar for k in L}
sbar = statistics.mean(SF.values())
pred = {k: SF[k] - sbar for k in L}

fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=170)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")
ax.axhline(0, color="#9aa3ab", lw=1.1, zorder=2)

for lab, ser, run, col in CAPS:
    ax.plot(common, meas[lab], color=col, lw=1.8, zorder=4)
    ax.plot([55, 21000], [pred[lab]]*2, color=col, lw=1.6, ls=(0, (5, 3)), alpha=0.8, zorder=3)
    bias = float(np.mean([meas[lab][i] for i, f in enumerate(common) if f <= 1000])) - pred[lab]
    ax.annotate(f"{lab}   {bias:+.2f}", (common[-1], meas[lab][-1]),
                textcoords="offset points", xytext=(8, 0), ha="left", va="center",
                fontsize=8.8, color=col, fontweight="600")

ax.annotate("dashed = where the factory Sens Factor says the capsule sits\n"
            "solid = where it actually sits",
            xy=(70, 1.9), fontsize=8.8, color=MUTED, linespacing=1.5)
for lab, y in (("811-2310", None), ("810-8897", None)):
    pass
ax.annotate("these three are a dB away from their files", (150, 0.95),
            textcoords="offset points", xytext=(10, 26), ha="left", fontsize=8.8,
            color=MUTED, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))

ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
ax.set_xscale("log"); ax.set_xlim(55, 24000); ax.set_ylim(-2.6, 2.6)
ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(FixedLocator([]))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}"))
ax.grid(True, color=GRID, lw=0.8, zorder=0)
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
for s_ in ("left", "bottom"): ax.spines[s_].set_color(GRID)
ax.tick_params(colors=MUTED, labelsize=9, length=0)
ax.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
ax.set_ylabel("level relative to the six-capsule mean  (dB)", color=MUTED, fontsize=9.5)
ax.set_title("Six capsules against the group consensus — no reference privileged",
             color=INK, fontsize=12.5, fontweight="600", loc="left", pad=26)
ax.annotate("number beside each label is the 63 Hz–1 kHz gap between measurement and factory Sens Factor",
            xy=(0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points",
            ha="left", va="bottom", color=MUTED, fontsize=8.8)
fig.tight_layout()
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
