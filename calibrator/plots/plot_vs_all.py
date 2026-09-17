import json, re, sys
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter

CAL = Path("/home/adam/ŻYCIE/PRACA/SoundVisualizer-data/data/calibrations")
S = Path("calibrator/sessions/2026-09-16")
INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"

def factory(ser):
    lines = (CAL/f"{ser}.txt").read_text().splitlines()
    sens = float(re.search(r"Sens Factor\s*=\s*(-?[\d.]+)", lines[0]).group(1))
    f, g = [], []
    for ln in lines[1:]:
        p = ln.split()
        if len(p) >= 2:
            try: f.append(float(p[0])); g.append(float(p[1]))
            except ValueError: pass
    return sens, np.array(f), np.array(g)

def lv(n):
    return {r["freq"]: r["level_dbfs"]
            for r in json.load(open(S/n/"levels.json")) if "error" not in r}

ref = lv("m-810-8904__4"); sref, fref, gref = factory("8108904")
CAPS = [("811-1896", "8111896", "m-811-1896", "#c25e00"),
        ("810-8903", "8108903", "m-810-8903", "#8c5ab8"),
        ("810-8900", "8108900", "m-810-8900", "#4b8b3b"),
        ("811-2310", "8112310", "m-811-2310", "#2f6f9f")]

fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=170)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")
ax.axhline(0, color="#9aa3ab", lw=1.1, zorder=2)
ax.annotate("810-8904 — the reference, 0 dB by definition", (58, 0),
            textcoords="offset points", xytext=(4, 5), ha="left", va="bottom",
            fontsize=8.5, color=MUTED)

for lab, ser, run, col in CAPS:
    s, ff, gg = factory(ser)
    d = lv(run); fs = sorted(set(d) & set(ref))
    pred = (s - sref) + (np.interp(fs, ff, gg) - np.interp(fs, fref, gref))
    meas = np.array([d[x] - ref[x] for x in fs])
    ax.plot(fs, pred, color=col, lw=1.8, ls=(0, (5, 3)), alpha=0.85, zorder=3)
    ax.plot(fs, meas, color=col, lw=1.9, zorder=4)
    ax.annotate(lab, (fs[-1], meas[-1]), textcoords="offset points", xytext=(7, 0),
                ha="left", va="center", fontsize=9, color=col, fontweight="600")

ax.annotate("factory says these four span 1.8 dB here …", (150, 1.1),
            textcoords="offset points", xytext=(0, 28), ha="left", fontsize=8.8, color=MUTED,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))
ax.annotate("… we measure them inside 0.2 dB", (150, -0.1),
            textcoords="offset points", xytext=(0, -34), ha="left", fontsize=8.8, color=MUTED,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9))

ticks = [63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
ax.set_xscale("log"); ax.set_xlim(55, 21000); ax.set_ylim(-2.6, 3.6)
ax.xaxis.set_major_locator(FixedLocator(ticks)); ax.xaxis.set_minor_locator(FixedLocator([]))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}"))
ax.grid(True, color=GRID, lw=0.8, zorder=0)
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
for s_ in ("left", "bottom"): ax.spines[s_].set_color(GRID)
ax.tick_params(colors=MUTED, labelsize=9, length=0)
ax.set_xlabel("frequency  (Hz)", color=MUTED, fontsize=9.5)
ax.set_ylabel("level relative to 810-8904  (dB)", color=MUTED, fontsize=9.5)

style = [Line2D([], [], color="#4a5560", lw=1.9, label="measured (this session)"),
         Line2D([], [], color="#4a5560", lw=1.8, ls=(0, (5, 3)), label="predicted by factory cal file")]
leg = ax.legend(handles=style, frameon=False, loc="upper left", fontsize=9.5)
for t in leg.get_texts(): t.set_color(INK)
ax.set_title("What the factory files predict, against what the capsules actually do",
             color=INK, fontsize=12.5, fontweight="600", loc="left", pad=26)
ax.annotate("prediction = Sens-Factor difference + response-curve difference · colour identifies the capsule, line style the source",
            xy=(0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points",
            ha="left", va="bottom", color=MUTED, fontsize=8.8)
fig.tight_layout()
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
