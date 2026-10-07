"""Polar overlay of the material measurements at 2000 us: 2 Oct set and 7 Oct set, total level 500 Hz-24 kHz, corrected microphone files."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
SETS = [('Bare', '2004__5in3b__unset__v1-naked-horizontal', '#1F2A44', '2 Oct'), ('Cork', '2004__5in3b__cork__v1-cork-horizontal', '#2F9E44', '2 Oct'), ('Rubber', '2004__5in3b__rubber__v1-rubber', '#F08C00', '2 Oct'),
        ('Felt', '2004__5in3b__felt__v1-felt', '#1098AD', '2 Oct'), ('Felt + rubber', '2004__5in3b__felt-rubber__v1-felt-rubber', '#7048E8', '2 Oct'),
        ('Inner felt + outer PU foam', 'axii__5in3b__inner-felt-outer-open-pore-pu-foam__v1-inner-felt-outer-pu', '#C2255C', '7 Oct'), ('PU foam', 'axii__5in3b__open-pore-pu-foam__v1-pu-foam', '#862E9C', '7 Oct'),
        ('PU foam, double layer', 'axii__5in3b__open-pore-pu-foam-double-layer__v1-pu-foam-double', '#5C940D', '7 Oct'), ('Thinsulate, 4 layers', 'axii__5in3b__thinsulate-4-layers__v1-thinsulate-4-layers', '#E03131', '7 Oct'),
        ('Thinsulate, 8 layers', 'axii__5in3b__thinsulate-8-layers__v1-thinsulate-8-layers', '#1864AB', '7 Oct')]
LO, HI = 500, 24000
data = {}
for nm, base, col, day in SETS:
    g = bf.last_at(base, 2000, bf.CORR); data[nm] = (g['elev'], bf.totals(g, LO, HI), col, day)
allv = np.concatenate([v for _, v, _, _ in data.values()]); rmin = float(np.floor(allv.min()) - 2); rmax = float(np.ceil(allv.max()) + 1)
fig = plt.figure(figsize=(6.4, 6.4), dpi=220); ax = fig.add_subplot(111, projection='polar')
for nm, (el, v, col, day) in data.items():
    th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
    ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=col, lw=2.6 if nm == 'Bare' else 2.0, ls='-' if day == '2 Oct' else '--', marker='o', ms=4, mfc=col, mec='white', mew=.8)
ax.set_rlim(rmin, rmax); ticks = [t for t in range(int(rmin), int(rmax) + 1) if t % 5 == 0 and t > rmin]; ax.set_rticks(ticks)
ax.set_yticklabels([f'{t}' if i < len(ticks) - 1 else f'{t} dB' for i, t in enumerate(ticks)], fontsize=10, color='#555'); ax.set_rlabel_position(25)
[(t.set_bbox(dict(facecolor='white', edgecolor='none', alpha=.9, pad=1.5)), t.set_zorder(30)) for t in ax.get_yticklabels()]
ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=12, color='#333'); ax.grid(color='#cfd4dc', lw=1); ax.spines['polar'].set_color('#9aa3b2')
fig.savefig(os.path.join(HERE, 'polar-materials.png'), bbox_inches='tight', pad_inches=.15, facecolor='white')
bare = float(data['Bare'][1].mean())
out = {k: dict(mean=round(float(v.mean()), 1), color=c, day=d, delta=round(float(v.mean()) - bare, 1)) for k, (e, v, c, d) in data.items()}
json.dump(out, open(os.path.join(HERE, 'materials.json'), 'w'), indent=1)
print('rlim', rmin, rmax); print({k: (v['mean'], v['delta']) for k, v in out.items()})
