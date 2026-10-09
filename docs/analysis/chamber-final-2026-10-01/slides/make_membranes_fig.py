"""Polar overlay of the membrane measurements (8-9 Oct), 2000 us, total level 500 Hz-24 kHz, mean of the 3 repeats, corrected microphone files."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
P = 'f30__5in3b__membrane-'
SETS = [('Membrane + cork', P + 'cork__v1-membrane-cork', '#2F9E44'), ('Membrane + felt', P + 'felt__v1-membrane-felt', '#1098AD'), ('Membrane + felt, double layer', P + 'felt-double-layer__v1-membrane-felt-double', '#1864AB'),
        ('Membrane + felt + rubber', P + 'felt-rubber__v1-membrane-felt-rubber', '#7048E8'), ('Membrane + PU foam', P + 'open-pore-pu-foam__v1-membrane-pu-foam', '#862E9C'),
        ('Membrane + Thinsulate, 2 layers', P + 'thinsulate-2-layers__v1-membrane-thinsulate-2-layers', '#F08C00'), ('Membrane + Thinsulate, 4 layers', P + 'thinsulate-4-layers__v1-membrane-thinsulate-4-layers', '#E03131'),
        ('Membrane + Thinsulate, 8 layers', P + 'thinsulate-8-layers__v1-membrane-thinsulate-8-layers', '#C2255C'), ('Membrane duct, small', P + 'duct-small__v1-membrane-duct-small', '#1F2A44'),
        ('Membrane duct + PU foam, double', P + 'duct-open-pore-pu-foam-double-layer__v1-membrane-duct-pu-foam-double', '#5C940D')]
DAY = lambda b: '8 Oct' if 'duct-small' in b or 'open-pore-pu-foam__' in b else '9 Oct'
LO, HI = 500, 24000
data = {}
for nm, base, col in SETS:
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000]; assert len(gs) == 3, (nm, len(gs))
    data[nm] = (gs[0]['elev'], np.mean([bf.totals(g, LO, HI) for g in gs], 0), col, DAY(base))
allv = np.concatenate([v for _, v, _, _ in data.values()]); rmin = float(np.floor(allv.min()) - 2); rmax = float(np.ceil(allv.max()) + 1)
fig = plt.figure(figsize=(6.4, 6.4), dpi=220); ax = fig.add_subplot(111, projection='polar')
for nm, (el, v, col, day) in data.items():
    th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
    ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=col, lw=2.0, ls='-', marker='o' if day == '8 Oct' else 's', ms=4, mfc=col, mec='white', mew=.8)
ax.set_rlim(rmin, rmax); ticks = [t for t in range(int(rmin), int(rmax) + 1) if t % 5 == 0 and t > rmin]; ax.set_rticks(ticks)
ax.set_yticklabels([f'{t}' if i < len(ticks) - 1 else f'{t} dB' for i, t in enumerate(ticks)], fontsize=10, color='#555'); ax.set_rlabel_position(25)
[(t.set_bbox(dict(facecolor='white', edgecolor='none', alpha=.9, pad=1.5)), t.set_zorder(30)) for t in ax.get_yticklabels()]
ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=12, color='#333'); ax.grid(color='#cfd4dc', lw=1); ax.spines['polar'].set_color('#9aa3b2')
fig.savefig(os.path.join(HERE, 'polar-membranes.png'), bbox_inches='tight', pad_inches=.15, facecolor='white')
out = {k: dict(mean=round(float(v.mean()), 1), color=c, day=d) for k, (e, v, c, d) in data.items()}
json.dump(out, open(os.path.join(HERE, 'membranes.json'), 'w'), indent=1); print('rlim', rmin, rmax); print({k: v['mean'] for k, v in out.items()})
