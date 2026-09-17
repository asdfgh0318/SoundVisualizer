import json, sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

S = Path("calibrator/sessions/2026-09-16")
runs = [("1/3-octave, 25 tones", S/"m-810-8904",    "#2f6f9f"),
        ("12 per octave, 97 tones", S/"m-810-8904__3", "#c25e00")]

INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"
fig, ax = plt.subplots(figsize=(10.5, 5.0), dpi=170)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")

for label, run, color in runs:
    rows = json.load(open(run/"levels.json"))
    ok = [r for r in rows if "error" not in r]
    f = [r["freq"] for r in ok]; L = [r["level_dbfs"] for r in ok]
    dense = len(ok) > 40
    ax.plot(f, L, color=color, lw=2 if not dense else 1.6,
            alpha=1.0 if not dense else 0.9, zorder=3, label=label)
    ax.plot(f, L, "o", color=color, ms=5.5 if not dense else 3.4,
            mec="white", mew=1.2 if not dense else 0.7, zorder=4)
    bad = [r for r in rows if "error" in r]
    for r in bad:   # the coarse grid's two gate failures
        ax.plot([r["freq"]], [-70], marker="x", color=color, ms=8, mew=2, zorder=5)
    if bad:
        ax.annotate("gate fail on the coarse grid", (bad[0]["freq"], -70),
                    textcoords="offset points", xytext=(10, -2), ha="left", va="center",
                    fontsize=8.5, color=color)

ax.annotate("14.25 kHz notch —\ninvisible at 1/3 octave", (14254, -36.9),
            textcoords="offset points", xytext=(-16, -30), ha="right", va="top",
            fontsize=8.5, color=MUTED,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))

ax.set_xscale("log")
ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(FixedLocator([]))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_: f"{v/1000:g}k" if v>=1000 else f"{v:g}"))
ax.set_xlim(55, 19000); ax.set_ylim(-74, -16)
ax.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
ax.set_ylabel("captured level  (dBFS)", color=MUTED, fontsize=9.5)
ax.grid(True, color=GRID, lw=0.8, zorder=0)
for s_ in ("top","right"): ax.spines[s_].set_visible(False)
for s_ in ("left","bottom"): ax.spines[s_].set_color(GRID)
ax.tick_params(colors=MUTED, labelsize=9, length=0)
leg = ax.legend(frameon=False, loc="lower right", fontsize=9.5)
for t in leg.get_texts(): t.set_color(INK)

ax.set_title("m-810-8904, same capsule and seat — two frequency grids",
             color=INK, fontsize=12.5, fontweight="600", loc="left", pad=26)
ax.annotate("amplitude 0.03  ·  six minutes apart  ·  the dense grid resolves structure the coarse one aliases",
            xy=(0,1), xycoords="axes fraction", xytext=(0,8), textcoords="offset points",
            ha="left", va="bottom", color=MUTED, fontsize=8.8)
fig.tight_layout()
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
