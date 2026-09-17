import json, re, statistics, sys
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

CAL = Path("/home/adam/ŻYCIE/PRACA/SoundVisualizer-data/data/calibrations")
S = Path("calibrator/sessions/2026-09-16")
INK, MUTED, GRID = "#1f2328", "#6b7280", "#e5e7eb"
C_FACT, C_MEAS = "#c25e00", "#2f6f9f"

def sens(ser):
    return float(re.search(r"Sens Factor\s*=\s*(-?[\d.]+)",
                           (CAL/f"{ser}.txt").read_text().splitlines()[0]).group(1))
def lv(n):
    return {r["freq"]: r["level_dbfs"]
            for r in json.load(open(S/n/"levels.json")) if "error" not in r}

ref = lv("m-810-8904__4"); sref = sens("8108904")
CAPS = [("810-8904", "8108904", None), ("810-8903", "8108903", "m-810-8903"),
        ("810-8900", "8108900", "m-810-8900"), ("811-2310", "8112310", "m-811-2310"),
        ("811-1896", "8111896", "m-811-1896")]

rows = []
for lab, ser, run in CAPS:
    pred = sens(ser) - sref
    if run is None:
        meas = 0.0
    else:
        d = lv(run); f = [x for x in sorted(set(d) & set(ref)) if x <= 1000]
        meas = statistics.mean([d[x] - ref[x] for x in f])
    rows.append((lab, pred, meas))

fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=170)
fig.patch.set_facecolor("white"); ax.set_facecolor("white")
y = range(len(rows))
for i, (lab, p, m) in enumerate(rows):
    ax.plot([m, p], [i, i], color=GRID, lw=2.5, zorder=1, solid_capstyle="round")
for i, (lab, p, m) in enumerate(rows):
    ax.plot([p], [i], "o", color=C_FACT, ms=9, mec="white", mew=1.6, zorder=3)
    ax.plot([m], [i], "o", color=C_MEAS, ms=9, mec="white", mew=1.6, zorder=4)
    ax.annotate(f"{m - p:+.2f}", ((m + p)/2, i), textcoords="offset points",
                xytext=(0, 11), ha="center", fontsize=8.5, color=MUTED)

ax.plot([], [], "o", color=C_FACT, ms=9, label="factory Sens Factor predicts")
ax.plot([], [], "o", color=C_MEAS, ms=9, label="we measured")
ax.set_yticks(list(y)); ax.set_yticklabels([r[0] for r in rows], fontsize=10, color=INK)
ax.invert_yaxis()
ax.axvline(0, color="#9aa3ab", lw=1, zorder=2)
ax.set_xlim(-0.6, 2.8); ax.set_xlabel("level relative to 810-8904  (dB)", color=MUTED, fontsize=9.5)
ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
for s_ in ("top", "right", "left"): ax.spines[s_].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(colors=MUTED, labelsize=9, length=0)
leg = ax.legend(frameon=False, loc="lower right", fontsize=9.5)
for t in leg.get_texts(): t.set_color(INK)
ax.set_title("Factory Sens Factors disagree with each other more than the capsules do",
             color=INK, fontsize=12, fontweight="600", loc="left", pad=24)
ax.annotate("measured 63 Hz–1 kHz mean · four of five capsules land within 0.17 dB of each other",
            xy=(0, 1), xycoords="axes fraction", xytext=(0, 8), textcoords="offset points",
            ha="left", va="bottom", color=MUTED, fontsize=8.8)
fig.tight_layout()
out = Path(sys.argv[1]); fig.savefig(out, facecolor="white"); print("wrote", out)
