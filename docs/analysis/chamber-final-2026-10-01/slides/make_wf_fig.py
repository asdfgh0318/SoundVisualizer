"""Slide figure for the chamber-treatment waterfall (day3-a -> carpet-reordered): three wide maps + band numbers for the native chart."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
def maps(run):
    f, L, pos = bf.load(run); lo = f < 3000; N = L - np.nanmean(L, 1, keepdims=True); return f, pos, N
f, pos, B = maps(bf.DAY3A); _, _, A = maps(bf.FINAL); lo = f < 3000
rms = lambda x: float(np.sqrt(np.nanmean(x ** 2)))
bands = [(250, 400), (400, 630), (630, 1000), (1000, 1600), (1600, 3000), (5000, 6400)]
bb = [rms(B[(f >= a) & (f < b)]) for a, b in bands]; ba = [rms(A[(f >= a) & (f < b)]) for a, b in bands]
json.dump(dict(labels=[f'{a}–{b}' for a, b in bands], before=bb, after=ba, eb=rms(B[lo]), ea=rms(A[lo])), open(os.path.join(HERE, 'wf-bands.json'), 'w'))
G = np.abs(B) - np.abs(A)
bw = LinearSegmentedColormap.from_list('bw', ['#c05621', '#f6d7c3', '#ffffff', '#cfe0f3', '#2b6cb0'])
fs = 1.3
fig, axs = plt.subplots(3, 1, figsize=(10.0, 7.2), gridspec_kw=dict(hspace=.55))
xx = np.arange(len(f) + 1); yy = np.arange(len(pos) + 1)
nom = {257: '0.26k', 400: '0.4k', 630: '0.63k', 1000: '1k', 1600: '1.6k', 2500: '2.5k', 6000: '6k'}
tk, tl = [], []
for z, lab in nom.items():
    i = int(np.argmin(abs(f - z)))
    if abs(f[i] - z) / z < 0.02: tk.append(i); tl.append(lab)
rows = [(B, f'Start of day 3 (day3-a): room error {rms(B[lo]):.3f} dB below 3 kHz', 'RdBu_r', 12), (A, f'Final (carpet-reordered): room error {rms(A[lo]):.3f} dB', 'RdBu_r', 12),
        (G, 'Change: blue = closer to the arc mean, orange = further', bw, 6)]
ims = []
for ax, (M, t, cm, v) in zip(axs, rows):
    ims.append(ax.pcolormesh(xx, yy, M.T, cmap=cm, vmin=-v, vmax=v)); ax.axvline(np.searchsorted(f, 4000), color='k', lw=1.2); ax.invert_yaxis()
    ax.set_yticks(np.arange(len(pos)) + .5); ax.set_yticklabels([f'{q:+.0f}°'.replace('-', '−') for q in pos], fontsize=6 * fs)
    ax.set_xticks([i + .5 for i in tk]); ax.set_xticklabels(tl, fontsize=6.5 * fs); ax.set_title(t, fontsize=8 * fs, loc='left')
cb = fig.colorbar(ims[0], ax=axs[:2], shrink=.85, pad=.015, aspect=22); cb.set_label('capsule level minus arc mean (dB)', fontsize=7 * fs); cb.ax.tick_params(labelsize=6 * fs)
cb2 = fig.colorbar(ims[2], ax=axs[2], shrink=.9, pad=.015, aspect=10); cb2.set_ticks([-6, 0, 6]); cb2.set_ticklabels(['−6', '0', '+6 dB']); cb2.ax.tick_params(labelsize=6 * fs)
fig.text(.42, .02, 'Frequency in kHz (black line: omitted 3–5 kHz). Top of each map = +90°.', ha='center', fontsize=6.5 * fs)
fig.savefig(os.path.join(HERE, 'fig-wf-slide.png'), dpi=200, bbox_inches='tight'); plt.close(fig)
print('room error', rms(B[lo]), rms(A[lo])); print(list(zip(bands, np.round(bb, 2), np.round(ba, 2))))
