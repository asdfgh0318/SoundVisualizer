"""Waterfall, in the style of the chamber-treatment step figures: does a lining attenuate more behind the transparent wall
than in the PETG-wall round? Each round is the lining's effect against its own same-day reference, so the two effects
are comparable even though the rounds are on different days.

    make_r27_waterfall.py [2|4]      (Thinsulate layers; default 2)

  1. bars: lining effect per band group, front mics (-54..+90), PETG round vs transparent round, with the repeat floor
  2. map: PETG round effect      [inlet + Thinsulate N] - [inlet, unlined]                  (3 Nov)
  3. map: transparent round      [inlet + transp. wall + Thinsulate N] - [inlet + transp. wall]  (6 Nov)
  4. map: transparent effect - PETG effect   (blue = attenuates more behind the transparent wall), per-mic net on the right
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2
sys.argv = ['x']
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
TW = 'axi2217__8in__inlet-transparent-wall__r27-inlet-transparent-wall'
PETG = (f'axi2217__8in__inlet-thinsulate-{N}-layers__r27-inlet-thinsulate-{N}-layers', '2026-11-03', I, '2026-11-03')
TRAN = (f'axi2217__8in__inlet-transparent-wall-thinsulate-{N}-layers__r27-inlet-transparent-wall-thinsulate-{N}-layers', '2026-11-06', TW, '2026-11-06')
FLOOR = (I + '-trial-2026-11-03', '2026-11-03', I, '2026-11-03')
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])
LAB = ['100', '125', '160', '200', '250', '315', '400', '500', '630', '800', '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k', '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k', '20k']
G = [('100–315 Hz', 100, 355), ('400–800 Hz\n(blade tones)', 355, 890), ('1–2 kHz', 890, 2240), ('2.5–5 kHz', 2240, 5600), ('6.3–10 kHz', 5600, 11200), ('12.5–20 kHz', 11200, 22400)]


def bands(base, day):
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(day)]
    assert len(gs) == 3, (base, day, len(gs))
    f = gs[0]['f']; df = f[1] - f[0]
    B = [np.array([10 * np.log10((10 ** (g['mags'] / 10))[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T for g in gs]
    return gs[0]['elev'].astype(int), np.mean(B, 0), np.mean([bf.totals(g, 500, 24000) for g in gs], 0)


def effect(lb, ld, rb, rd):
    el, A, ta = bands(lb, ld); _, R, tr = bands(rb, rd)
    return el, A - R, ta - tr


el, dP, tP = effect(*PETG)
_, dT, tT = effect(*TRAN)
_, dF, tF = effect(*FLOOR)
fr = el >= -54
gm = lambda d, lo, hi: d[fr][:, (FC >= lo) & (FC < hi)].mean()
DD = dT - dP

fig = plt.figure(figsize=(14, 19), dpi=140)
gsp = fig.add_gridspec(5, 2, height_ratios=[1.25, 1, 1, 1, .05], width_ratios=[1, .09], hspace=.42, wspace=.04)
ax0 = fig.add_subplot(gsp[0, 0])
x = np.arange(len(G)); w = .36
vp = [gm(dP, lo, hi) for _, lo, hi in G]; vt = [gm(dT, lo, hi) for _, lo, hi in G]; vf = [abs(gm(dF, lo, hi)) for _, lo, hi in G]
ax0.bar(x - w / 2, vp, w, color='#9aa0a8', label=f'PETG round: [inlet + Thinsulate {N}] − [inlet, unlined]  (3 Nov)')
ax0.bar(x + w / 2, vt, w, color='#1971C2', label=f'transparent round: [inlet + transparent wall + Thinsulate {N}] − [inlet + transparent wall]  (6 Nov)')
for i, f_ in enumerate(vf):
    ax0.add_patch(plt.Rectangle((i - .45, -f_), .9, 2 * f_, color='#f1f3f5', zorder=0))
for i, (a, b) in enumerate(zip(vp, vt)):
    d = b - a; c = '#1971C2' if d < -.1 else '#d9480f' if d > .1 else '#495057'
    word = 'more attenuation' if d < -.1 else 'less attenuation' if d > .1 else 'same'
    ax0.text(i + w / 2, min(b, 0) - .07, f'{d:+.2f}\n{word}', ha='center', va='top', fontsize=8.5, color=c, fontweight='bold')
ax0.axhline(0, color='#495057', lw=1)
ax0.set_xticks(x); ax0.set_xticklabels([g[0] for g in G], fontsize=9.5)
ax0.set_ylabel('lining effect, dB\n(front mics −54…+90°, below 0 = quieter)')
lo_ = min(min(vp), min(vt)) - .55; ax0.set_ylim(lo_, max(.4, max(vp + vt) + .25))
ax0.legend(fontsize=8.5, loc='upper right', frameon=False)
ax0.set_title(f'Thinsulate {N} effect per band group, each against its own same-day reference (grey box: repeat floor of the band group)', fontsize=10.5, loc='left')
ax0.grid(axis='y', color='#e9ecef')

LIM = 3
for k, (title, d, cmap) in enumerate([
        (f'PETG round:  [inlet + Thinsulate {N}]  minus  [inlet, unlined]   (3 Nov, same day) — total 500 Hz–24 kHz, front mics {tP[fr].mean():+.2f} dB', dP, 'RdBu_r'),
        (f'transparent round:  [inlet + transparent wall + Thinsulate {N}]  minus  [inlet + transparent wall]   (6 Nov, same day) — total {tT[fr].mean():+.2f} dB', dT, 'RdBu_r'),
        (f'DIFFERENCE:  transparent-round effect  minus  PETG-round effect  (blue = more attenuation behind the transparent wall) — total {tT[fr].mean() - tP[fr].mean():+.2f} dB', DD, 'PuOr_r')]):
    ax = fig.add_subplot(gsp[k + 1, 0])
    im = ax.imshow(d, cmap=cmap if k < 2 else 'RdBu_r', vmin=-LIM, vmax=LIM, aspect='auto')
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            ax.text(j, i, f'{d[i, j]:+.1f}'.replace('-', '−'), ha='center', va='center', fontsize=6.3, color='white' if abs(d[i, j]) > 1.9 else '#222')
    ax.set_yticks(range(len(el))); ax.set_yticklabels([f'{e:+d}°'.replace('-', '−') if e else '0°' for e in el], fontsize=8)
    ax.set_xticks(range(len(FC))); ax.set_xticklabels(LAB, fontsize=8)
    ax.axhline(8.5, color='#495057', lw=1.3, ls='--')
    ax.set_title(title, fontsize=9.5, loc='left', fontweight='bold' if k == 2 else 'normal')
    if k == 2:
        ax.set_xlabel('third-octave band centre, Hz   ·   below the dashed line: −72°/−90°, probably in the flow   ·   400 and 800 Hz columns: blade tones, ±2 dB run to run')
        axn = fig.add_subplot(gsp[3, 1], sharey=ax)
        net = DD[:, FC >= 890].mean(1)
        axn.barh(range(len(el)), net, color=['#1971C2' if v < 0 else '#d9480f' for v in net])
        axn.axvline(0, color='#495057', lw=.8); axn.tick_params(labelleft=False, labelsize=7.5)
        axn.set_xlabel('net per mic,\n1–20 kHz (dB)', fontsize=8)
cax = fig.add_subplot(gsp[4, 0]); fig.colorbar(im, cax=cax, orientation='horizontal', label='Δ dB (blue = quieter / more attenuation)')
fig.suptitle(f'Thinsulate {N}: transparent wall vs PETG wall — r27 duct with inlet, 2000 µs, mean of 3 repeats per run', fontsize=13, fontweight='bold', x=.06, ha='left', y=.93)
fig.text(.06, .912, f'transparent round {tT[fr].mean():+.2f} dB vs PETG round {tP[fr].mean():+.2f} dB (total 500 Hz–24 kHz, front mics); side (0°, ±18°) {tT[np.isin(el, (0, 18, -18))].mean():+.2f} vs {tP[np.isin(el, (0, 18, -18))].mean():+.2f} dB; '
         f'repeat floor {tF[fr].mean():+.2f} dB. Effects are same-day; the two rounds are 3 days apart.', fontsize=9.5, color='#495057')
out = os.path.join(HERE, f'waterfall-r27-thin{N}-petg-vs-transparent.png')
fig.savefig(out, bbox_inches='tight', facecolor='white')
print(f'PETG {tP[fr].mean():+.2f}  transparent {tT[fr].mean():+.2f}  floor {tF[fr].mean():+.2f}')
for (n, *_), a, b in zip(G, vp, vt):
    print(f'{n.splitlines()[0]:12} PETG {a:+.2f}  transparent {b:+.2f}  diff {b - a:+.2f}')
print(os.path.basename(out), 'written')
