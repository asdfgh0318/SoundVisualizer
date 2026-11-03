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
D = 'axi2217__8in__duct-unlined__r27-duct-unlined'
T = 'axi2217__8in__thinsulate-'
MODES = {   # out file, day, {key: base}, panels, title
    'inlet': ('heatmap-r27-inlet-linings.png', '2026-11-03',
              {'ref': I, 'ref_b': I + '-trial-2026-11-03',
               'thin2': 'axi2217__8in__inlet-thinsulate-2-layers__r27-inlet-thinsulate-2-layers',
               'thin4': 'axi2217__8in__inlet-thinsulate-4-layers__r27-inlet-thinsulate-4-layers',
               'thin4r': 'axi2217__8in__inlet-thinsulate-4-layers-rubber__r27-inlet-thinsulate-4-layers-rubber',
               'felt': 'axi2217__8in__inlet-felt__r27-inlet-felt'},
              [('Thinsulate 2 effect:  [inlet + Thinsulate 2]  minus  [inlet, unlined]', 'thin2'),
               ('Thinsulate 4 effect:  [inlet + Thinsulate 4]  minus  [inlet, unlined]', 'thin4'),
               ('Thinsulate 4 + rubber effect:  [inlet + Thinsulate 4 + rubber]  minus  [inlet, unlined]', 'thin4r'),
               ('Felt effect:  [inlet + felt]  minus  [inlet, unlined]', 'felt'),
               ('Repeat floor:  [inlet, unlined, run 2]  minus  [run 1]  (nothing changed)', 'ref_b')],
              'r27 duct WITH the inlet, 2000 µs, 3 Nov (same day)'),
    'noinlet': ('heatmap-r27-linings-no-inlet.png', '2026-11-02',
                {'ref': D, 'ref_b': D + '-archive-2026-11-02-trial-1751',
                 'thin2': T + '2-layers__r27-thinsulate-2-layers-trial-2026-11-02',
                 'thin4': T + '4-layers__r27-thinsulate-4-layers'},
                [('Thinsulate 2 effect:  [Thinsulate 2]  minus  [unlined]   (no inlet)', 'thin2'),
                 ('Thinsulate 4 effect:  [Thinsulate 4]  minus  [unlined]   (no inlet)', 'thin4'),
                 ('Repeat floor:  [unlined, 17:51 run]  minus  [unlined, 17:35 run]  (nothing changed)', 'ref_b')],
                'r27 duct WITHOUT the inlet, 2000 µs, 2 Nov (same day)'),
}
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])          # 100 Hz .. 20 kHz
LAB = [f'{f/1000:g}k' if f >= 1000 else f'{f:.0f}' for f in [100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000]]


def bands(g):
    f, lin = g['f'], 10 ** (g['mags'] / 10); df = f[1] - f[0]
    return np.array([10 * np.log10(lin[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T   # mics x bands


LIM = 3
for mode, (OUT, DAY, SETS, TITLES, HEAD) in MODES.items():
  R = {}
  for k, base in SETS.items():
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(DAY)]
    assert len(gs) == 3, (k, len(gs))
    el = gs[0]['elev']
    R[k] = np.mean([bands(g) for g in gs], 0)
  PANELS = [(t, R[k] - R['ref']) for t, k in TITLES]
  if True:
    fig, axs = plt.subplots(len(PANELS), 1, figsize=(13, 4.15 * len(PANELS)), dpi=160, gridspec_kw=dict(hspace=.42))
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
        ax.set_title(title, fontsize=11, loc='left', fontweight='bold', pad=20)
        ax.text(0, 1.02, f'front mics −54°…+90°: mean {d[front].mean():+.2f} dB · 100 Hz–2 kHz {d[front][:, FC < 1900].mean():+.2f} · 2–20 kHz {d[front][:, FC >= 1900].mean():+.2f}'.replace('-', '−'), transform=ax.transAxes, fontsize=9, color='#495057', va='bottom')
        ax.set_ylabel('microphone')
    axs[-1].set_xlabel('third-octave band centre, Hz')
    cb = fig.colorbar(im, cax=fig.add_axes([0.93, 0.38, 0.012, 0.25]), label='Δ level, dB (blue = quieter)')
    fig.suptitle(HEAD + ': level change per microphone and third-octave band, mean of 3 repeats\nBelow the dashed line: −72°/−90°, probably in the flow', fontsize=11.5, x=.5, y=.95)
    fig.savefig(os.path.join(HERE, OUT), bbox_inches='tight', facecolor='white')
    for title, d in PANELS:
        front = el >= -54
        print(f'{mode:8} {title[:40]:40} front mean {d[front].mean():+.2f}  <2k {d[front][:, FC < 1900].mean():+.2f}  >=2k {d[front][:, FC >= 1900].mean():+.2f}  |d| max {abs(d[front]).max():.1f}')
    print(OUT, 'written')
