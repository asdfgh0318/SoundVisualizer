"""Polar overlay of the 2 Oct material measurements at 2000 us (total level 100 Hz-10 kHz, corrected microphone files)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
SETS = [('Naked', '2004__5in3b__unset__v1-naked-horizontal', '#1F2A44'), ('Cork', '2004__5in3b__cork__v1-cork-horizontal', '#2F9E44'), ('Rubber', '2004__5in3b__rubber__v1-rubber', '#F08C00'),
        ('Felt', '2004__5in3b__felt__v1-felt', '#D6336C'), ('Felt + rubber', '2004__5in3b__felt-rubber__v1-felt-rubber', '#7048E8')]
LO, HI = 100, 10000
data = {}
for nm, base, col in SETS:
    g = bf.last_at(base, 2000, bf.CORR)
    data[nm] = (g['elev'], bf.totals(g, LO, HI), col)
allv = np.concatenate([v for _, v, _ in data.values()]); print({k: (round(float(v.mean()), 1), round(float(np.ptp(v)), 1), round(float(v.min()), 1), round(float(v.max()), 1)) for k, (e, v, c) in data.items()})
rmin = float(np.floor(allv.min()) - 1); rmax = float(np.ceil(allv.max()) + 1)
fig = plt.figure(figsize=(6.4, 6.4), dpi=220); ax = fig.add_subplot(111, projection='polar')
for nm, (el, v, col) in data.items():
    th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
    ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=col, lw=2.8, marker='o', ms=5.5, mfc=col, mec='white', mew=1, label=nm)
ax.set_rlim(rmin, rmax); ticks = [t for t in range(int(rmin), int(rmax) + 1) if t % 5 == 0 and t > rmin]; ax.set_rticks(ticks); ax.set_yticklabels([f'{t}' if i < len(ticks) - 1 else f'{t} dB' for i, t in enumerate(ticks)], fontsize=10, color='#555'); ax.set_rlabel_position(25); [t.set_bbox(dict(facecolor='white', edgecolor='none', alpha=.85, pad=1.5)) for t in ax.get_yticklabels()]
ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=12, color='#333'); ax.grid(color='#cfd4dc', lw=1); ax.spines['polar'].set_color('#9aa3b2')
fig.savefig(os.path.join(HERE, 'polar-materials.png'), bbox_inches='tight', pad_inches=.15, facecolor='white')
json.dump({k: dict(mean=round(float(v.mean()), 1), rng=round(float(np.ptp(v)), 1), color=c) for k, (e, v, c) in data.items()}, open(os.path.join(HERE, 'materials.json'), 'w'), indent=1)
print('rlim', rmin, rmax)
