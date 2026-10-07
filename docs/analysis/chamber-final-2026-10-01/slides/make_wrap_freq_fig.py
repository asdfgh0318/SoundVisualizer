"""Per-tone change of the arc-relative map when Thinsulate wrap came off the ring/tripod, against the repeat floor."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
def get(r):
    f, L, pos = bf.load(S + r); return f, L - np.nanmean(L, 1, keepdims=True)
S = ''
def mapchange(a, b):
    fa, Na = get(a); fb, Nb = get(b); return fa, np.sqrt(((Nb - Na) ** 2).mean(1))
bf.S = bf.S
pairs = [('Tripod wrap partly off (23 Sep)', '2026-09-23/foam-out', '2026-09-23/tripod-unwrapped', '#9AA5B8'), ('Ring wrap, first part off (23 Sep)', '2026-09-23/tripod-unwrapped', '2026-09-23/ring-unwrapped', '#2F9E44'),
         ('Ring wrap, more off (23 Sep)', '2026-09-23/ring-unwrapped', '2026-09-23/ring-unwrapped-2', '#F08C00'), ('Rest of ring wrap off (24 Sep)', '2026-09-24/wall-direct-absorber', '2026-09-24/ring-bare', '#D6336C')]
fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
for nm, a, b, c in pairs:
    f, d = mapchange(a, b); m = f < 3000; ax.plot(f[m], d[m], color=c, lw=2.4 if '24' in nm else 1.6, label=nm, marker='o' if '24' in nm else None, ms=3)
f, d = mapchange('2026-09-24/wall-direct-a', '2026-09-24/wall-direct-b'); m = f < 3000
ax.fill_between(f[m], 0, d[m], color='#C9CFDA', alpha=.9, label='Repeat of one state (noise floor)')
ax.set_xscale('log'); ax.set_xlim(257, 3000); ax.set_ylim(0, 1.6); ax.set_xticks([300, 400, 500, 630, 800, 1000, 1600, 2500]); ax.set_xticklabels(['300', '400', '500', '630', '800', '1k', '1.6k', '2.5k'])
ax.set_xlabel('Frequency (Hz)'); ax.set_ylabel('Change of the microphone pattern (dB rms)'); ax.grid(alpha=.3); ax.legend(fontsize=8, frameon=False, loc='upper right')
ax.annotate('1.5 dB at 545 Hz', xy=(545, 1.49), xytext=(700, 1.45), fontsize=9, arrowprops=dict(arrowstyle='->', lw=1))
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'wrap-frequency.png'), facecolor='white')
