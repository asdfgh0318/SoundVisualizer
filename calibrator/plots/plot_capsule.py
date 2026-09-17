import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

run = Path(sys.argv[1]); out = Path(sys.argv[2])
rows = json.load(open(run / "levels.json"))
ok = [r for r in rows if "error" not in r]
bad = [r for r in rows if "error" in r]

INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"
SERIES, FAIL = "#2f6f9f", "#b3341f"

fig, ax = plt.subplots(figsize=(9.5, 4.6), dpi=170)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")

f = [r["freq"] for r in ok]; L = [r["level_dbfs"] for r in ok]
ax.plot(f, L, color=SERIES, lw=2, zorder=3)
ax.plot(f, L, "o", color=SERIES, ms=5.5, mec="white", mew=1.4, zorder=4)

lo = min(L) - 9
for r in bad:
    ax.plot([r["freq"]], [lo], marker="x", color=FAIL, ms=9, mew=2.2, zorder=5)
if bad:
    ax.annotate(" , ".join(f"{r['freq']:g}" for r in bad) + " Hz — gate fail",
                (bad[0]["freq"], lo), textcoords="offset points", xytext=(6, -12),
                ha="left", va="top", fontsize=8.5, color=FAIL)

# label only the extremes and the two LF dips, never every point
notable = {max(ok, key=lambda r: r["level_dbfs"])["freq"],
           min(ok, key=lambda r: r["level_dbfs"])["freq"], 100.0, 250.0}
for r in ok:
    if r["freq"] in notable:
        below = r["freq"] in (125.0, 250.0)          # dips: label under the point
        ax.annotate(f"{r['level_dbfs']:.1f}", (r["freq"], r["level_dbfs"]),
                    textcoords="offset points", xytext=(0, -15 if below else 10),
                    ha="center", fontsize=8.5, color=MUTED)

ax.set_xscale("log")
ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
ax.xaxis.set_major_locator(FixedLocator(ticks))
ax.xaxis.set_minor_locator(FixedLocator([]))
ax.xaxis.set_major_formatter(FuncFormatter(
    lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}"))
ax.set_xlim(55, 19000); ax.set_ylim(lo - 7, max(L) + 7)

ax.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
ax.set_ylabel("captured level  (dBFS)", color=MUTED, fontsize=9.5)
ax.grid(True, which="major", color=GRID, lw=0.8, zorder=0)
for side in ("top", "right"): ax.spines[side].set_visible(False)
for side in ("left", "bottom"): ax.spines[side].set_color(GRID)
ax.tick_params(colors=MUTED, labelsize=9, length=0)

meta = json.load(open(run / "meta.json"))
ax.set_title(f"{meta['label']}  —  source + room + capsule, amplitude {meta['amplitude']}",
             color=INK, fontsize=12, fontweight="600", loc="left", pad=26)
ax.annotate(f"{len(ok)}/{len(rows)} tones passed the stability gate  ·  "
            f"{meta['timestamp'].replace('T', ' ')}",
            xy=(0, 1), xycoords="axes fraction", xytext=(0, 8),
            textcoords="offset points", ha="left", va="bottom",
            color=MUTED, fontsize=8.8)
fig.tight_layout()
fig.savefig(out, facecolor="white")
print("wrote", out)
