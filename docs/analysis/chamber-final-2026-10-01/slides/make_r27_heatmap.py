"""Heatmaps, microphone x third-octave band, of the linings inside the inlet duct (3 Nov, same day):
Inlet + Thinsulate 2 minus inlet, Inlet + Thinsulate 4 minus inlet, and the repeat floor (inlet run 2 minus run 1).
2000 us, total level per band, mean of the 3 repeats. Blue = quieter with the lining.
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
DAY = '2026-11-03'
SETS = {'inlet': I, 'inlet_b': I + '-trial-2026-11-03',
        'i_thin2': 'axi2217__8in__inlet-thinsulate-2-layers__r27-inlet-thinsulate-2-layers',
        'i_thin4': 'axi2217__8in__inlet-thinsulate-4-layers__r27-inlet-thinsulate-4-layers'}
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])          # 100 Hz .. 20 kHz
LAB = [f'{f/1000:g}k' if f >= 1000 else f'{f:.0f}' for f in [100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]]


def bands(g):
    f, lin = g['f'], 10 ** (g['mags'] / 10); df = f[1] - f[0]
    return np.array([10 * np.log10(lin[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T   # mics x bands


R = {}
for k, base in SETS.items():
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(DAY)]
    assert len(gs) == 3, (k, len(gs))
    el = gs[0]['elev']
    R[k] = np.mean([bands(g) for g in gs], 0)

PANELS = [('Inlet + Thinsulate 2 − inlet, no lining', R['i_thin2'] - R['inlet']),
          ('Inlet + Thinsulate 4 − inlet, no lining', R['i_thin4'] - R['inlet']),
          ('Repeat floor: inlet run 2 − run 1 (nothing changed)', R['inlet_b'] - R['inlet'])]
LIM = 3
fig, axs = plt.subplots(3, 1, figsize=(13, 12.5), dpi=160, gridspec_kw=dict(hspace=.32))
for ax, (title, d) in zip(axs, PANELS):
    im = ax.imshow(d, cmap='RdBu_r', vmin=-LIM, vmax=LIM, aspect='auto')
    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            v = d[i, j]
            ax.text(j, i, f'{v:+.1f}'.replace('-', '−'), ha='center', va='center', fontsize=6.6, color='white' if abs(v) > 1.9 else '#222')
    ax.set_yticks(range(len(el))); ax.set_yticklabels([f'{int(e):+d}°'.replace('-', '−') if e else '0°' for e in el], fontsize=8.5)
    ax.set_xticks(range(len(FC))); ax.set_xticklabels(LAB, fontsize=8.5)
    ax.axhline(8.5, color='#495057', lw=1.4, ls='--')          # below: -72 / -90, probably in the flow
    front = el >= -54
    ax.set_title(title, fontsize=11, loc='left', fontweight='bold')
    ax.set_title(f'front mics −54°…+90°: mean {d[front].mean():+.2f} dB · 100 Hz–2 kHz {d[front][:, FC < 1900].mean():+.2f} · 2–20 kHz {d[front][:, FC >= 1900].mean():+.2f}'.replace('-', '−'), fontsize=9, loc='right', color='#495057')
    ax.set_ylabel('microphone')
axs[-1].set_xlabel('third-octave band centre, Hz')
cb = fig.colorbar(im, cax=fig.add_axes([0.93, 0.38, 0.012, 0.25]), label='Δ level, dB (blue = quieter)')
fig.suptitle('r27 duct with the inlet, 2000 µs, 3 Nov (same day): level change per microphone and third-octave band, mean of 3 repeats\nBelow the dashed line: −72°/−90°, probably in the flow', fontsize=11.5, x=.5, y=.95)
fig.savefig(os.path.join(HERE, 'heatmap-r27-inlet-linings.png'), bbox_inches='tight', facecolor='white')
for title, d in PANELS:
    front = el >= -54
    print(f'{title:55} front mean {d[front].mean():+.2f}  <2k {d[front][:, FC < 1900].mean():+.2f}  >=2k {d[front][:, FC >= 1900].mean():+.2f}  |d| max {abs(d[front]).max():.1f}')
print('heatmap-r27-inlet-linings.png written')
