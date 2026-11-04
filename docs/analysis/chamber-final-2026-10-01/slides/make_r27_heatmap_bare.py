"""Heatmaps, microphone x third-octave band, of what the duct and the inlet do to the bare prop (2000 us, total level per
band, mean of the 3 repeats):
  1. duct, no inlet, unlined   minus  bare prop            (both 2 Nov, same day)
  2. duct + inlet, unlined     minus  bare prop            (3 Nov vs 2 Nov, crosses days)
  3. duct + inlet, unlined     minus  duct, no inlet       (3 Nov vs 2 Nov, crosses days)
  4. repeat floor: duct + inlet run 2 minus run 1          (3 Nov)
Red = louder than the reference.
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
SETS = {'bare': ('axi2217__8in__none__r27-8x45mr-bare-prop', '2026-11-02'),
        'duct': ('axi2217__8in__duct-unlined__r27-duct-unlined', '2026-11-02'),
        'inlet': (I, '2026-11-03'),
        'inlet_b': (I + '-trial-2026-11-03', '2026-11-03')}
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])
LAB = ['100', '125', '160', '200', '250', '315', '400', '500', '630', '800', '1k', '1.25k', '1.6k', '2k', '2.5k', '3.15k', '4k', '5k', '6.3k', '8k', '10k', '12.5k', '16k', '20k']


def bands(g):
    f, lin = g['f'], 10 ** (g['mags'] / 10); df = f[1] - f[0]
    return np.array([10 * np.log10(lin[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T


R = {}
for k, (base, day) in SETS.items():
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(day)]
    assert len(gs) == 3, (k, len(gs))
    el = gs[0]['elev']
    R[k] = np.mean([bands(g) for g in gs], 0)

PANELS = [  # title, data, colour limit
    ('Duct effect:  [duct, no inlet, unlined]  minus  [bare prop]   (both 2 Nov)', R['duct'] - R['bare'], 18),
    ('Duct + inlet effect:  [duct + inlet, unlined]  minus  [bare prop]   (3 Nov − 2 Nov, crosses days)', R['inlet'] - R['bare'], 18),
    ('Inlet effect:  [duct + inlet, unlined]  minus  [duct, no inlet, unlined]   (3 Nov − 2 Nov, crosses days)', R['inlet'] - R['duct'], 6),
    ('Repeat floor:  [duct + inlet, unlined, run 2]  minus  [run 1]   (3 Nov, nothing changed)', R['inlet_b'] - R['inlet'], 6),
]
front = el >= -54
fig, axs = plt.subplots(len(PANELS), 1, figsize=(13.5, 4.15 * len(PANELS)), dpi=160, gridspec_kw=dict(hspace=.42))
for ax, (title, d, lim) in zip(axs, PANELS):
    im = ax.imshow(d, cmap='RdBu_r', vmin=-lim, vmax=lim, aspect='auto')
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            v = d[i, j]
            ax.text(j, i, f'{v:+.1f}'.replace('-', '−'), ha='center', va='center', fontsize=6.6, color='white' if abs(v) > .63 * lim else '#222')
    ax.set_yticks(range(len(el))); ax.set_yticklabels([f'{int(e):+d}°'.replace('-', '−') if e else '0°' for e in el], fontsize=8.5)
    ax.set_xticks(range(len(FC))); ax.set_xticklabels(LAB, fontsize=8.5)
    ax.axhline(8.5, color='#495057', lw=1.4, ls='--')
    ax.set_title(title, fontsize=11, loc='left', fontweight='bold', pad=20)
    ax.text(0, 1.02, f'front mics −54°…+90°: mean {d[front].mean():+.1f} dB · 100–315 Hz {d[front][:, FC < 355].mean():+.1f} · 400 Hz–2 kHz {d[front][:, (FC >= 355) & (FC < 2240)].mean():+.1f} · 2.5–5 kHz {d[front][:, (FC >= 2240) & (FC < 5600)].mean():+.1f} · 6.3–20 kHz {d[front][:, FC >= 5600].mean():+.1f}'.replace('-', '−'),
            transform=ax.transAxes, fontsize=9, color='#495057', va='bottom')
    ax.set_ylabel('microphone')
    fig.colorbar(im, ax=ax, pad=.012, fraction=.025, label='Δ dB (red = louder)')
axs[-1].set_xlabel('third-octave band centre, Hz')
fig.suptitle('r27 8-inch duct vs the bare APC 8x4.5MR, 2000 µs: level change per microphone and third-octave band, mean of 3 repeats\n'
             'Note the colour scales: ±18 dB for the top two panels, ±6 dB for the bottom two. Below the dashed line: −72°/−90°, probably in the flow',
             fontsize=11.5, y=.95)
fig.savefig(os.path.join(HERE, 'heatmap-r27-bare-duct-inlet.png'), bbox_inches='tight', facecolor='white')
for title, d, _ in PANELS:
    print(f'{title[:60]:60} front mean {d[front].mean():+.1f}  <315 {d[front][:, FC < 355].mean():+.1f}  400-2k {d[front][:, (FC >= 355) & (FC < 2240)].mean():+.1f}  2.5-5k {d[front][:, (FC >= 2240) & (FC < 5600)].mean():+.1f}  >6.3k {d[front][:, FC >= 5600].mean():+.1f}')
print('heatmap-r27-bare-duct-inlet.png written')
