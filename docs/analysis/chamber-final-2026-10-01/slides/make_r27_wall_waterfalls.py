"""Wall-difference waterfalls: the transparent wall (6 Nov) against the PETG wall, same thing behind both, one figure per case
(r27 duct with inlet, 2000 us, mean of 3 repeats per run). Every figure crosses days.

  bare          [inlet + transparent wall] vs [inlet + PETG 1-layer wall, 4 Nov]
  thin2, thin4  [inlet + transparent wall + Thinsulate N] vs [inlet + Thinsulate N, PETG round, 3 Nov]

Stack, top to bottom: difference per band group; PETG level map; transparent level map; transparent minus PETG, with the
net per microphone. Level maps are absolute third-octave dB SPL.
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
TW = 'axi2217__8in__inlet-transparent-wall'
CASES = [  # file tag, title, PETG label, (PETG base, day), transparent label, (transparent base, day)
    ('bare', 'No lining', 'inlet + PETG 1-layer wall (4 Nov)', ('axi2217__8in__inlet-petg-1-layer__r27-inlet-petg-1-layer', '2026-11-04'),
     'inlet + transparent wall (6 Nov)', (f'{TW}__r27-inlet-transparent-wall', '2026-11-06')),
    ('thin2', 'Thinsulate 2', 'inlet + Thinsulate 2, PETG round (3 Nov)', ('axi2217__8in__inlet-thinsulate-2-layers__r27-inlet-thinsulate-2-layers', '2026-11-03'),
     'inlet + transparent wall + Thinsulate 2 (6 Nov)', (f'{TW}-thinsulate-2-layers__r27-inlet-transparent-wall-thinsulate-2-layers', '2026-11-06')),
    ('thin4', 'Thinsulate 4', 'inlet + Thinsulate 4, PETG round (3 Nov)', ('axi2217__8in__inlet-thinsulate-4-layers__r27-inlet-thinsulate-4-layers', '2026-11-03'),
     'inlet + transparent wall + Thinsulate 4 (6 Nov)', (f'{TW}-thinsulate-4-layers__r27-inlet-transparent-wall-thinsulate-4-layers', '2026-11-06')),
]
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])
LAB = ['100', '125', '160', '200', '250', '315', '400', '500', '630', '800', '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k', '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k', '20k']
G = [('100–315 Hz', 100, 355), ('400–800 Hz\n(blade tones)', 355, 890), ('1–2 kHz', 890, 2240), ('2.5–5 kHz', 2240, 5600), ('6.3–10 kHz', 5600, 11200), ('12.5–20 kHz', 11200, 22400)]


def load(base, day):
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(day)]
    assert len(gs) == 3, (base, day, len(gs))
    f = gs[0]['f']; df = f[1] - f[0]
    B = [np.array([10 * np.log10((10 ** (g['mags'] / 10))[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T for g in gs]
    return gs[0]['elev'].astype(int), np.mean(B, 0), np.mean([bf.totals(g, 500, 24000) for g in gs], 0)


el, F1, _ = load(I, '2026-11-03'); _, F2, _ = load(I + '-trial-2026-11-03', '2026-11-03')
dF = F2 - F1
fr = el >= -54; side = np.isin(el, (0, 18, -18)); top = np.isin(el, (54, 72, 90))
tick = [f'{e:+d}°'.replace('-', '−') if e else '0°' for e in el]


def cells(ax, d, white):
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            ax.text(j, i, white[1](d[i, j]), ha='center', va='center', fontsize=6.3, color='white' if white[0](d[i, j]) else '#222')
    ax.set_yticks(range(len(el))); ax.set_yticklabels(tick, fontsize=8)
    ax.set_xticks(range(len(FC))); ax.set_xticklabels(LAB, fontsize=8)
    ax.axhline(8.5, color='#ffffff' if white[2] else '#495057', lw=1.3, ls='--')


for tag, name, lp, bp, lt, bt in CASES:
    _, P, tP = load(*bp); _, T, tT = load(*bt)
    d, t = T - P, tT - tP
    gm = lambda x, lo, hi: x[fr][:, (FC >= lo) & (FC < hi)].mean()
    fig = plt.figure(figsize=(14, 18.5), dpi=140)
    gsp = fig.add_gridspec(5, 2, height_ratios=[1, 1, 1, 1, .05], width_ratios=[1, .09], hspace=.42, wspace=.04)
    ax0 = fig.add_subplot(gsp[0, 0])
    v = [gm(d, lo, hi) for _, lo, hi in G]; vf = [abs(gm(dF, lo, hi)) for _, lo, hi in G]
    x = np.arange(len(G))
    for i, f_ in enumerate(vf):
        ax0.add_patch(plt.Rectangle((i - .45, -f_), .9, 2 * f_, color='#e9ecef', zorder=0))
    ax0.bar(x, v, .5, color=['#1971C2' if q < 0 else '#d9480f' for q in v], zorder=2)
    for xx, q in zip(x, v):
        ax0.text(xx, q + (.05 if q >= 0 else -.05), f'{q:+.2f}'.replace('-', '−'), ha='center', va='bottom' if q >= 0 else 'top', fontsize=10, fontweight='bold')
    ax0.axhline(0, color='#495057', lw=1, zorder=3)
    ax0.set_xticks(x); ax0.set_xticklabels([g[0] for g in G], fontsize=9.5)
    ax0.set_ylim(min(v + [-.3]) - .35, max(v + [.3]) + .35)
    ax0.set_ylabel('transparent − PETG, dB\n(front mics, below 0 = transparent quieter)')
    ax0.set_title('Difference per band group (grey box: same-day repeat floor of that band group)', fontsize=10.5, loc='left')
    ax0.grid(axis='y', color='#e9ecef')
    vmin, vmax = float(np.floor(min(P.min(), T.min()))), float(np.ceil(max(P.max(), T.max())))
    mid = (vmin + vmax) / 2
    for k, (lab, m) in enumerate(((lp, P), (lt, T))):
        ax = fig.add_subplot(gsp[k + 1, 0])
        im = ax.imshow(m, cmap='viridis', vmin=vmin, vmax=vmax, aspect='auto')
        cells(ax, m, (lambda q: q < mid, lambda q: f'{q:.0f}', True))
        ax.set_title(f'{lab}: level per microphone and band', fontsize=10, loc='left')
        holder = fig.add_subplot(gsp[k + 1, 1]); holder.axis('off')
        fig.colorbar(im, cax=holder.inset_axes([.05, 0, .25, 1]), label='dB SPL')
    ax = fig.add_subplot(gsp[3, 0])
    im = ax.imshow(d, cmap='RdBu_r', vmin=-3, vmax=3, aspect='auto')
    cells(ax, d, (lambda q: abs(q) > 1.9, lambda q: f'{q:+.1f}'.replace('-', '−'), False))
    ax.set_title(f'DIFFERENCE: transparent minus PETG (blue = transparent quieter), total 500 Hz–24 kHz, front mics {t[fr].mean():+.2f} dB'.replace('-', '−').replace('500 Hz−24', '500 Hz–24'), fontsize=10, loc='left', fontweight='bold')
    ax.set_xlabel('third-octave band centre, Hz   ·   below the dashed line: −72°/−90°, probably in the flow   ·   400 and 800 Hz: blade tones, ±2 dB run to run')
    axn = fig.add_subplot(gsp[3, 1], sharey=ax)
    net = d[:, FC >= 890].mean(1)
    axn.barh(range(len(el)), net, color=['#1971C2' if q < 0 else '#d9480f' for q in net])
    axn.axvline(0, color='#495057', lw=.8); axn.tick_params(labelleft=False, labelsize=7.5); axn.set_title('net per mic\n1–20 kHz, dB', fontsize=8)
    fig.colorbar(im, cax=fig.add_subplot(gsp[4, 0]), orientation='horizontal', label='Δ dB')
    fig.suptitle(f'{name}: transparent wall vs PETG wall, r27 duct with inlet, 2000 µs, mean of 3 repeats per run', fontsize=13, fontweight='bold', x=.06, ha='left', y=.93)
    fig.text(.06, .914, f'total 500 Hz–24 kHz: front {t[fr].mean():+.2f} dB, side (0°, ±18°) {t[side].mean():+.2f}, top (+54…+90°) {t[top].mean():+.2f}.  The runs are from different days, so drift between days is included.'.replace('-', '−').replace('500 Hz−24', '500 Hz–24'), fontsize=9.5, color='#495057')
    out = os.path.join(HERE, f'waterfall-r27-walls-{tag}.png')
    fig.savefig(out, bbox_inches='tight', facecolor='white'); plt.close(fig)
    print(f'{name:13} total {t[fr].mean():+.2f} side {t[side].mean():+.2f} top {t[top].mean():+.2f} | ' + ' '.join(f'{q:+.2f}' for q in v) + f' | {os.path.basename(out)}')
