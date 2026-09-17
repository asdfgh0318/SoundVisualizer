import json, sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

S = Path("calibrator/sessions/2026-09-16")
CAPS = [("810-8904  (reference)", "m-810-8904__4", "#2f6f9f"),
        ("811-1896",              "m-811-1896",    "#c25e00"),
        ("810-8903",              "m-810-8903",    "#8c5ab8"),
        ("810-8900",              "m-810-8900",    "#4b8b3b")]
INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"

def lv(n):
    return {r["freq"]: r["level_dbfs"]
            for r in json.load(open(S/n/"levels.json")) if "error" not in r}

fig, ax = plt.subplots(figsize=(11.5, 5.8), dpi=170)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")

for lab, name, col in CAPS:
    d = lv(name); f = sorted(d)
    ax.plot(f, [d[x] for x in f], color=col, lw=1.7, zorder=3, label=lab)
    ax.plot(f, [d[x] for x in f], "o", color=col, ms=3.0, mec="white", mew=0.6, zorder=4)

ax.annotate("all three trace the same room —\nthe comb, the 250 Hz dip, the 14 kHz notch",
            (330, -36.4), textcoords="offset points", xytext=(6, -46), ha="left",
            fontsize=8.8, color=MUTED, linespacing=1.4,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
ax.annotate("811-1896 rides ~1.4 dB above\nthe other three throughout",
            (900, -33.0), textcoords="offset points", xytext=(10, 44), ha="left",
            fontsize=8.8, color="#c25e00", linespacing=1.4,
            arrowprops=dict(arrowstyle="-", color="#c25e00", lw=0.9))

ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
ax.set_xscale("log"); ax.set_xlim(55, 19000); ax.set_ylim(-70, -17)
ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(FixedLocator([]))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}"))
ax.grid(True, color=GRID, lw=0.8, zorder=0)
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
for s_ in ("left", "bottom"): ax.spines[s_].set_color(GRID)
ax.tick_params(colors=MUTED, labelsize=9, length=0)
ax.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
ax.set_ylabel("captured level  (dBFS)", color=MUTED, fontsize=9.5)
leg = ax.legend(frameon=False, loc="lower right", fontsize=9.5)
for t in leg.get_texts(): t.set_color(INK)
ax.set_title("Four capsules, same seat, same source — raw captures",
             color=INK, fontsize=12.5, fontweight="600", loc="left", pad=26)
ax.annotate("12 per octave · amplitude 0.03 · source + room + capsule, nothing removed",
            xy=(0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points",
            ha="left", va="bottom", color=MUTED, fontsize=8.8)
fig.tight_layout()
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
