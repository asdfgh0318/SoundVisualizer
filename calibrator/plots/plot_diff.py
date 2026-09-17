import json, sys, statistics
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

S = Path("calibrator/sessions/2026-09-16")
REF, NEW = "m-810-8904__4", "m-811-1896"
INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"
C_REF, C_NEW, C_D = "#2f6f9f", "#c25e00", "#8c5ab8"

def lv(name):
    rows = json.load(open(S/name/"levels.json"))
    return {r["freq"]: r["level_dbfs"] for r in rows if "error" not in r}

a, b = lv(REF), lv(NEW)
f = sorted(set(a) & set(b)); d = [b[x] - a[x] for x in f]
mean = statistics.mean(d)

fig, (ax, bx) = plt.subplots(2, 1, figsize=(11, 7.6), dpi=170,
                             gridspec_kw={"height_ratios": [1.9, 1.3], "hspace": 0.34})
fig.patch.set_facecolor("white")

for name, col, lab in ((REF, C_REF, "810-8904  (reference)"), (NEW, C_NEW, "811-1896")):
    dd = lv(name); x = sorted(dd)
    ax.plot(x, [dd[i] for i in x], color=col, lw=1.6, zorder=3, label=lab)
    ax.plot(x, [dd[i] for i in x], "o", color=col, ms=3.0, mec="white", mew=0.6, zorder=4)

bx.axhline(0, color=GRID, lw=1, zorder=1)
bx.axhline(mean, color=C_D, lw=1.2, ls=(0, (5, 4)), zorder=2)
bx.annotate(f"mean {mean:+.2f} dB", (16000, mean), textcoords="offset points",
            xytext=(-4, 7), ha="right", va="bottom", fontsize=9, color=C_D, fontweight="600")
bx.plot(f, d, color=C_D, lw=1.6, zorder=3)
bx.plot(f, d, "o", color=C_D, ms=3.2, mec="white", mew=0.6, zorder=4)
bx.annotate("+2 dB shelf, 2–8 kHz", (5040, 2.09), textcoords="offset points",
            xytext=(0, -26), ha="center", fontsize=8.8, color=MUTED,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
bx.annotate("scatter grows where\nthe source is weakest", (12699, d[f.index(12699)]),
            textcoords="offset points", xytext=(-8, 26), ha="right", fontsize=8.5,
            color=MUTED, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))

ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
for axis in (ax, bx):
    axis.set_xscale("log"); axis.set_xlim(55, 19000)
    axis.xaxis.set_major_locator(FixedLocator(ticks)); axis.xaxis.set_minor_locator(FixedLocator([]))
    axis.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}"))
    axis.set_facecolor("white"); axis.grid(True, color=GRID, lw=0.8, zorder=0)
    for s_ in ("top", "right"): axis.spines[s_].set_visible(False)
    for s_ in ("left", "bottom"): axis.spines[s_].set_color(GRID)
    axis.tick_params(colors=MUTED, labelsize=9, length=0)

ax.set_ylabel("captured level  (dBFS)", color=MUTED, fontsize=9.5)
bx.set_ylabel("811-1896 − 810-8904  (dB)", color=MUTED, fontsize=9.5)
bx.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
bx.set_ylim(-0.3, 2.7)
leg = ax.legend(frameon=False, loc="lower right", fontsize=9.5)
for t in leg.get_texts(): t.set_color(INK)

ax.set_title("Two capsules at the same seat — the room is still in both curves",
             color=INK, fontsize=12.5, fontweight="600", loc="left", pad=26)
ax.annotate("12 per octave · amplitude 0.03 · every wiggle they share is the room, not the microphone",
            xy=(0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points",
            ha="left", va="bottom", color=MUTED, fontsize=8.8)
bx.set_title("The difference is what the microphone actually is — the room has cancelled out",
             color=INK, fontsize=10.5, fontweight="600", loc="left", pad=10)
fig.tight_layout()
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
