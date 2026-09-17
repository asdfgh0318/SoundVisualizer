import json, sys, statistics
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

S = Path("calibrator/sessions/2026-09-16")
REF = "m-810-8904__4"
CAPS = [("811-1896", "m-811-1896", "#c25e00"),
        ("810-8903", "m-810-8903", "#8c5ab8"),
        ("810-8900", "m-810-8900", "#4b8b3b")]
INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"

def lv(n):
    return {r["freq"]: r["level_dbfs"]
            for r in json.load(open(S/n/"levels.json")) if "error" not in r}

ref = lv(REF)
fig, ax = plt.subplots(figsize=(11, 5.2), dpi=170)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")
ax.axhspan(-0.5, 0.5, color="#f2f4f6", zorder=0)
ax.axhline(0, color="#9aa3ab", lw=1.2, zorder=2)
ax.annotate("810-8904 = reference, 0 dB by definition", (58, 0), textcoords="offset points",
            xytext=(4, 5), ha="left", va="bottom", fontsize=8.5, color=MUTED)

for lab, name, col in CAPS:
    d = lv(name); f = sorted(set(ref) & set(d)); y = [d[x] - ref[x] for x in f]
    m = statistics.mean(y)
    ax.plot(f, y, color=col, lw=1.7, zorder=3, label=f"{lab}   (mean {m:+.2f} dB)")
    ax.plot(f, y, "o", color=col, ms=3.2, mec="white", mew=0.6, zorder=4)
    ax.annotate(lab, (f[-1], y[-1]), textcoords="offset points", xytext=(7, 0),
                ha="left", va="center", fontsize=9, color=col, fontweight="600")

ax.annotate("all three rise together into 4–8 kHz\nand fall together above it — a shared\nshape belongs to the reference, not\nto three independent capsules",
            (5040, 1.74), textcoords="offset points", xytext=(-40, -74), ha="right",
            fontsize=8.5, color=MUTED, linespacing=1.4,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))

ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
ax.set_xscale("log"); ax.set_xlim(55, 21000); ax.set_ylim(-2.2, 2.6)
ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(FixedLocator([]))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}"))
ax.grid(True, color=GRID, lw=0.8, zorder=1)
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
for s_ in ("left", "bottom"): ax.spines[s_].set_color(GRID)
ax.tick_params(colors=MUTED, labelsize=9, length=0)
ax.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
ax.set_ylabel("level relative to 810-8904  (dB)", color=MUTED, fontsize=9.5)
leg = ax.legend(frameon=False, loc="lower left", fontsize=9.5)
for t in leg.get_texts(): t.set_color(INK)
ax.set_title("Relative capsule response — four of eleven",
             color=INK, fontsize=12.5, fontweight="600", loc="left", pad=26)
ax.annotate("12 per octave · amplitude 0.03 · the room has cancelled; this is microphone only",
            xy=(0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points",
            ha="left", va="bottom", color=MUTED, fontsize=8.8)
fig.tight_layout()
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
