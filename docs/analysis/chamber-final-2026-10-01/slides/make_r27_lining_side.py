"""Side microphones only (0, +18, -18 deg, looking at the duct wall): Thinsulate 2 and 4 against nothing, for each wall type.
r27 duct with inlet, 2000 us, mean of 3 repeats per run.

  transparent wall: [wall + Thinsulate N] - [wall alone], both 6 Nov, same day
  PETG wall:        [inlet + Thinsulate N, 3 Nov] - [inlet + PETG 1-layer wall, 4 Nov], crosses days
  Diamonds on the PETG bars: "nothing" = the unlined inlet of 3 Nov, same day.
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
TW = 'axi2217__8in__inlet-transparent-wall'
P = lambda n: (f'axi2217__8in__inlet-thinsulate-{n}-layers__r27-inlet-thinsulate-{n}-layers', '2026-11-03')
T = lambda n: (f'{TW}-thinsulate-{n}-layers__r27-inlet-transparent-wall-thinsulate-{n}-layers', '2026-11-06')
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])
LAB = ['100', '125', '160', '200', '250', '315', '400', '500', '630', '800', '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k', '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k', '20k']
G = [('100–315 Hz', 100, 355), ('400–800 Hz\n(blade tones)', 355, 890), ('1–2 kHz', 890, 2240), ('2.5–5 kHz', 2240, 5600), ('6.3–10 kHz', 5600, 11200), ('12.5–20 kHz', 11200, 22400)]
SIDE = (18, 0, -18)


def load(base, day):
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(day)]
    assert len(gs) == 3, (base, day, len(gs))
    f = gs[0]['f']; df = f[1] - f[0]
    el = gs[0]['elev'].astype(int); idx = [int(np.where(el == e)[0][0]) for e in SIDE]
    B = [np.array([10 * np.log10((10 ** (g['mags'] / 10))[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T for g in gs]
    return np.mean(B, 0)[idx], np.mean([bf.totals(g, 500, 24000) for g in gs], 0)[idx]


bP, tbP = load('axi2217__8in__inlet-petg-1-layer__r27-inlet-petg-1-layer', '2026-11-04')
bT, tbT = load(f'{TW}__r27-inlet-transparent-wall', '2026-11-06')
bI, tbI = load(I, '2026-11-03'); bI2, tbI2 = load(I + '-trial-2026-11-03', '2026-11-03')
L = {('PETG', n): load(*P(n)) for n in (2, 4)} | {('transparent', n): load(*T(n)) for n in (2, 4)}
D = {('PETG', n): (L['PETG', n][0] - bP, L['PETG', n][1] - tbP) for n in (2, 4)} | {('transparent', n): (L['transparent', n][0] - bT, L['transparent', n][1] - tbT) for n in (2, 4)}
ALT = {n: (L['PETG', n][0] - bI, L['PETG', n][1] - tbI) for n in (2, 4)}
dF, tF = bI2 - bI, tbI2 - tbI
gm = lambda x, lo, hi: x[:, (FC >= lo) & (FC < hi)].mean()

fig = plt.figure(figsize=(25, 12.5), dpi=120)
gsp = fig.add_gridspec(4, 2, height_ratios=[2.2, 1, 1, .1], hspace=.55, wspace=.08)
ax0 = fig.add_subplot(gsp[0, :])
x = np.arange(len(G)); w = .2
for i, (_, lo, hi) in enumerate(G):
    f_ = abs(gm(dF, lo, hi)); ax0.add_patch(plt.Rectangle((i - .46, -f_), .92, 2 * f_, color='#e9ecef', zorder=0))
S = [(('PETG', 2), '#ffc078', 'PETG wall: Thinsulate 2 − nothing'), (('PETG', 4), '#e8590c', 'PETG wall: Thinsulate 4 − nothing'),
     (('transparent', 2), '#74c0fc', 'transparent wall: Thinsulate 2 − nothing'), (('transparent', 4), '#1864ab', 'transparent wall: Thinsulate 4 − nothing')]
allv = []
for k, (key, col, lab) in enumerate(S):
    v = [gm(D[key][0], lo, hi) for _, lo, hi in G]; allv += v; xs = x + (k - 1.5) * w
    ax0.bar(xs, v, w, color=col, zorder=2, label=f'{lab}  (total {D[key][1].mean():+.2f} dB)')
    for xx, q in zip(xs, v):
        ax0.text(xx, q + (.06 if q >= 0 else -.06), f'{q:+.2f}'.replace('-', '−'), ha='center', va='bottom' if q >= 0 else 'top', fontsize=9.5)
    if key[0] == 'PETG':
        a = [gm(ALT[key[1]][0], lo, hi) for _, lo, hi in G]; allv += a
        ax0.scatter(xs, a, marker='D', s=42, color='white', edgecolor='#212529', zorder=4, label=f'Thinsulate {key[1]}, "nothing" = unlined inlet of 3 Nov (total {ALT[key[1]][1].mean():+.2f} dB)')
ax0.axhline(0, color='#495057', lw=1, zorder=3)
ax0.set_xticks(x); ax0.set_xticklabels([g[0] for g in G], fontsize=12)
ax0.set_ylabel('lining − nothing, dB\n(mean of 0°, ±18°; below 0 = quieter)', fontsize=12)
ax0.set_ylim(min(allv) - .4, max(allv) + 1.1)
ax0.legend(fontsize=11, loc='upper center', ncol=3, frameon=False)
ax0.set_title('Side microphones only (0°, ±18°): each lining against the same wall with nothing behind it (grey box: repeat floor of that group at these mics)', fontsize=13, loc='left')
ax0.grid(axis='y', color='#e9ecef')
for c, (wall, sub) in enumerate((('PETG', 'PETG wall (lining 3 Nov, nothing 4 Nov, crosses days)'), ('transparent', 'transparent wall (both 6 Nov, same day)'))):
    for r, n in enumerate((2, 4)):
        ax = fig.add_subplot(gsp[r + 1, c]); d, t = D[wall, n]
        im = ax.imshow(d, cmap='RdBu_r', vmin=-3, vmax=3, aspect='auto')
        for i in range(d.shape[0]):
            for j in range(d.shape[1]):
                ax.text(j, i, f'{d[i, j]:+.1f}'.replace('-', '−'), ha='center', va='center', fontsize=8.5, color='white' if abs(d[i, j]) > 1.9 else '#222')
        ax.set_yticks(range(3)); ax.set_yticklabels(['+18°', '0°', '−18°'], fontsize=10)
        ax.set_xticks(range(len(FC))); ax.set_xticklabels(LAB, fontsize=9.5)
        ax.set_title(f'Thinsulate {n} minus nothing, {sub}: total {t.mean():+.2f} dB'.replace(' -', ' −'), fontsize=11.5, loc='left', fontweight='bold')
fig.colorbar(im, cax=fig.add_subplot(gsp[3, :]), orientation='horizontal', label='Δ dB (blue = lining quieter than nothing)   ·   third-octave bands, Hz   ·   400 and 800 Hz: blade tones, ±2 dB run to run')
fig.suptitle('Side microphones only: Thinsulate 2 and 4 against nothing, for each wall type. r27 duct with inlet, 2000 µs, mean of 3 repeats per run', fontsize=15, fontweight='bold', x=.125, ha='left', y=.95)
fig.savefig(os.path.join(HERE, 'lining-vs-nothing-r27-side-mics.png'), bbox_inches='tight', facecolor='white')
print(f"{'':44}{'total':>7}" + ''.join(f'{g[0].splitlines()[0]:>13}' for g in G))
def row(lab, d, t):
    print(f'{lab:44}{t.mean():+7.2f}' + ''.join(f'{gm(d, lo, hi):+13.2f}' for _, lo, hi in G))
for key, _, lab in S:
    row(lab, *D[key])
for n in (2, 4):
    row(f'PETG Thinsulate {n} vs unlined inlet 3 Nov', *ALT[n])
row('repeat floor (3 Nov)', dF, tF)
