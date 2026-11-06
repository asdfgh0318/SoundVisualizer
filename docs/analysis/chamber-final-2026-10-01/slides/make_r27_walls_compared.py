"""Transparent wall against the PETG-wall round, same lining behind both, absolute levels (r27 duct with inlet, 2000 us,
mean of 3 repeats per run). Transparent-wall runs are from 6 Nov, PETG-round runs from 3 Nov: every panel crosses days.

  1. bars: transparent - PETG per band group, front mics (-54..+90), for Thinsulate 2 and Thinsulate 4, with the bare walls
           (transparent wall alone - unlined inlet) for context and the same-day repeat floor as grey boxes
  2. map:  [inlet + transparent wall + Thinsulate 2] - [inlet + Thinsulate 2]
  3. map:  [inlet + transparent wall + Thinsulate 4] - [inlet + Thinsulate 4]
  4. map:  repeat floor, unlined inlet run 2 - run 1 (3 Nov)
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
TW = 'axi2217__8in__inlet-transparent-wall__r27-inlet-transparent-wall'
P = lambda n: (f'axi2217__8in__inlet-thinsulate-{n}-layers__r27-inlet-thinsulate-{n}-layers', '2026-11-03')
T = lambda n: (f'axi2217__8in__inlet-transparent-wall-thinsulate-{n}-layers__r27-inlet-transparent-wall-thinsulate-{n}-layers', '2026-11-06')
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])
LAB = ['100', '125', '160', '200', '250', '315', '400', '500', '630', '800', '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k', '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k', '20k']
G = [('100–315 Hz', 100, 355), ('400–800 Hz\n(blade tones)', 355, 890), ('1–2 kHz', 890, 2240), ('2.5–5 kHz', 2240, 5600), ('6.3–10 kHz', 5600, 11200), ('12.5–20 kHz', 11200, 22400)]


def load(base, day):
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(day)]
    assert len(gs) == 3, (base, day, len(gs))
    f = gs[0]['f']; df = f[1] - f[0]
    B = [np.array([10 * np.log10((10 ** (g['mags'] / 10))[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T for g in gs]
    return gs[0]['elev'].astype(int), np.mean(B, 0), np.mean([bf.totals(g, 500, 24000) for g in gs], 0)


el, T2, tT2 = load(*T(2)); _, P2, tP2 = load(*P(2))
_, T4, tT4 = load(*T(4)); _, P4, tP4 = load(*P(4))
_, TB, tTB = load(TW, '2026-11-06'); _, PB, tPB = load(I, '2026-11-03')
_, F2, tF2 = load(I + '-trial-2026-11-03', '2026-11-03')
PAIRS = [('bare walls: transparent − plain inlet', TB - PB, tTB - tPB, '#ced4da'),
         ('Thinsulate 2: transparent − PETG', T2 - P2, tT2 - tP2, '#F08C00'),
         ('Thinsulate 4: transparent − PETG', T4 - P4, tT4 - tP4, '#E03131')]
dF, tF = F2 - PB, tF2 - tPB
fr = el >= -54; side = np.isin(el, (0, 18, -18)); top = np.isin(el, (54, 72, 90))
gm = lambda d, lo, hi: d[fr][:, (FC >= lo) & (FC < hi)].mean()

fig = plt.figure(figsize=(14, 18.5), dpi=140)
gsp = fig.add_gridspec(5, 1, height_ratios=[1.25, 1, 1, 1, .05], hspace=.42)
ax0 = fig.add_subplot(gsp[0])
x = np.arange(len(G)); w = .26
for i, (_, lo, hi) in enumerate(G):
    f_ = abs(gm(dF, lo, hi)); ax0.add_patch(plt.Rectangle((i - .45, -f_), .9, 2 * f_, color='#f1f3f5', zorder=0))
allv = []
for k, (lab, d, t, col) in enumerate(PAIRS):
    v = [gm(d, lo, hi) for _, lo, hi in G]; allv += v
    xs = x + (k - 1) * w
    ax0.bar(xs, v, w, color=col, label=f'{lab}  (total {t[fr].mean():+.2f} dB)', edgecolor='#495057' if k == 0 else 'none', lw=.6)
    for xx, vv in zip(xs, v):
        ax0.text(xx, vv + (.04 if vv >= 0 else -.04), f'{vv:+.2f}', ha='center', va='bottom' if vv >= 0 else 'top', fontsize=7.8)
ax0.axhline(0, color='#495057', lw=1)
ax0.set_xticks(x); ax0.set_xticklabels([g[0] for g in G], fontsize=9.5)
ax0.set_ylabel('transparent wall − PETG round, dB\n(front mics −54…+90°, below 0 = transparent quieter)')
ax0.set_ylim(min(allv) - .45, max(allv) + .5)
ax0.legend(fontsize=8.5, loc='upper left', frameon=False)
ax0.set_title('Same lining behind both walls, absolute level (transparent 6 Nov, PETG round 3 Nov — crosses days; grey box: same-day repeat floor)', fontsize=10, loc='left')
ax0.grid(axis='y', color='#e9ecef')

LIM = 3
for k, (title, d, t) in enumerate([
        ('Thinsulate 2:  [inlet + transparent wall + Thinsulate 2, 6 Nov]  minus  [inlet + Thinsulate 2, PETG round, 3 Nov]', PAIRS[1][1], PAIRS[1][2]),
        ('Thinsulate 4:  [inlet + transparent wall + Thinsulate 4, 6 Nov]  minus  [inlet + Thinsulate 4, PETG round, 3 Nov]', PAIRS[2][1], PAIRS[2][2]),
        ('repeat floor:  [inlet, unlined, run 2]  minus  [run 1]   (3 Nov, nothing changed)', dF, tF)]):
    ax = fig.add_subplot(gsp[k + 1])
    im = ax.imshow(d, cmap='RdBu_r', vmin=-LIM, vmax=LIM, aspect='auto')
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            ax.text(j, i, f'{d[i, j]:+.1f}'.replace('-', '−'), ha='center', va='center', fontsize=6.3, color='white' if abs(d[i, j]) > 1.9 else '#222')
    ax.set_yticks(range(len(el))); ax.set_yticklabels([f'{e:+d}°'.replace('-', '−') if e else '0°' for e in el], fontsize=8)
    ax.set_xticks(range(len(FC))); ax.set_xticklabels(LAB, fontsize=8)
    ax.axhline(8.5, color='#495057', lw=1.3, ls='--')
    ax.set_title(title, fontsize=10, loc='left', pad=18, fontweight='bold' if k < 2 else 'normal')
    ax.text(0, 1.02, f'total 500 Hz–24 kHz: front {t[fr].mean():+.2f} dB · side (0°, ±18°) {t[side].mean():+.2f} · top (+54…+90°) {t[top].mean():+.2f}'.replace('-', '−'),
            transform=ax.transAxes, fontsize=9, color='#495057', va='bottom')
ax.set_xlabel('third-octave band centre, Hz   ·   below the dashed line: −72°/−90°, probably in the flow   ·   400 and 800 Hz: blade tones, ±2 dB run to run')
cax = fig.add_subplot(gsp[4]); fig.colorbar(im, cax=cax, orientation='horizontal', label='Δ dB (blue = transparent-wall set-up quieter)')
fig.suptitle('Transparent wall vs PETG wall, same lining behind both — r27 duct with inlet, 2000 µs', fontsize=13, fontweight='bold', x=.06, ha='left', y=.925)
out = os.path.join(HERE, 'walls-r27-transparent-vs-petg.png')
fig.savefig(out, bbox_inches='tight', facecolor='white')
for lab, d, t, _ in PAIRS + [('repeat floor', dF, tF, None)]:
    print(f'{lab:40} total {t[fr].mean():+.2f} side {t[side].mean():+.2f} top {t[top].mean():+.2f} | ' + ' '.join(f'{gm(d, lo, hi):+.2f}' for _, lo, hi in G))
print(os.path.basename(out), 'written')
