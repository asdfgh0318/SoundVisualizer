import json, sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

S = Path("calibrator/sessions/2026-09-16")
RUNS = [("1/3-octave · 23/25",  S/"m-810-8904",    "#2f6f9f"),
        ("12/oct run 1 · 97/97", S/"m-810-8904__3", "#c25e00"),
        ("12/oct run 2 · 96/97", S/"m-810-8904__4", "#8c5ab8")]
INK, MUTED, GRID, FAIL = "#1f2328", "#6b7280", "#e5e7eb", "#b3341f"

def lv(run):
    rows = json.load(open(run/"levels.json"))
    ok = [r for r in rows if "error" not in r]
    return {r["freq"]: r["level_dbfs"] for r in ok}, [r for r in rows if "error" in r]

fig, (ax, bx) = plt.subplots(2, 1, figsize=(11, 7.4), dpi=170,
                             gridspec_kw={"height_ratios": [2.5, 1], "hspace": 0.30})
fig.patch.set_facecolor("white")

for label, run, color in RUNS:
    d, bad = lv(run)
    f = sorted(d); L = [d[x] for x in f]
    dense = len(f) > 40
    ax.plot(f, L, color=color, lw=1.7, zorder=3, label=label)
    ax.plot(f, L, "o", color=color, ms=5.2 if not dense else 3.0,
            mec="white", mew=1.1 if not dense else 0.6, zorder=4)
    for r in bad:
        ax.plot([r["freq"]], [-71], marker="x", color=color, ms=8, mew=2, zorder=5)

ax.annotate("gate failures", (63, -71), textcoords="offset points", xytext=(26, 0),
            ha="left", va="center", fontsize=8.5, color=FAIL)

a, _ = lv(S/"m-810-8904__3"); b, _ = lv(S/"m-810-8904__4")
f = sorted(set(a) & set(b)); diff = [b[x] - a[x] for x in f]
bx.axhspan(-0.1, 0.1, color="#eef3f7", zorder=0)
bx.axhline(0, color=GRID, lw=1, zorder=1)
bx.plot(f, diff, color="#8c5ab8", lw=1.5, zorder=3)
bx.plot(f, diff, "o", color="#8c5ab8", ms=3.0, mec="white", mew=0.6, zorder=4)
bx.annotate("±0.1 dB", (58, 0.1), textcoords="offset points", xytext=(2, 3),
            fontsize=8, color=MUTED, ha="left", va="bottom")
bx.annotate("62 Hz, −66 dBFS\nthe noise floor, not the mic", (62, -0.73),
            textcoords="offset points", xytext=(30, -2), fontsize=8.5,
            color=MUTED, ha="left", va="center",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))

ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
for axis in (ax, bx):
    axis.set_xscale("log"); axis.set_xlim(55, 19000)
    axis.xaxis.set_major_locator(FixedLocator(ticks)); axis.xaxis.set_minor_locator(FixedLocator([]))
    axis.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}"))
    axis.set_facecolor("white"); axis.grid(True, color=GRID, lw=0.8, zorder=0)
    for s_ in ("top", "right"): axis.spines[s_].set_visible(False)
    for s_ in ("left", "bottom"): axis.spines[s_].set_color(GRID)
    axis.tick_params(colors=MUTED, labelsize=9, length=0)

ax.set_ylim(-75, -16); ax.set_ylabel("captured level  (dBFS)", color=MUTED, fontsize=9.5)
bx.set_ylim(-0.95, 0.55); bx.set_ylabel("run 2 − run 1  (dB)", color=MUTED, fontsize=9.5)
bx.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)

leg = ax.legend(frameon=False, loc="lower right", fontsize=9.5)
for t in leg.get_texts(): t.set_color(INK)
ax.set_title("m-810-8904 — three captures, same capsule, same seat",
             color=INK, fontsize=12.5, fontweight="600", loc="left", pad=26)
ax.annotate("amplitude 0.03 throughout  ·  the two dense runs sit on top of each other",
            xy=(0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points",
            ha="left", va="bottom", color=MUTED, fontsize=8.8)
bx.set_title("repeatability residual: sd 0.082 dB, 94 of 96 points inside ±0.1 dB",
             color=INK, fontsize=10, fontweight="600", loc="left", pad=10)
fig.tight_layout()
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
