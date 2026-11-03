"""Polar: the r27 duct with the inlet (3 Nov, run and repeat, and with Thinsulate 2) against the unlined duct without it (2 Nov), 2000 us,
total level 500 Hz-24 kHz, mean of the 3 repeats, corrected microphone files. Different days: indicative.
Prints thrust/rpm/current per set-up and the inlet's repeat-to-repeat check.
"""
import sys, os, json, glob, csv, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
SETS = [  # label, base, day, colour, line style
    ('Duct + inlet, run 1 (3 Nov)', I, '2026-11-03', '#D6336C', '-'),
    ('Duct + inlet, run 2 (3 Nov)', I + '-trial-2026-11-03', '2026-11-03', '#F08C00', '--'),
    ('Inlet + Thinsulate, 2 layers (3 Nov)', 'axi2217__8in__inlet-thinsulate-2-layers__r27-inlet-thinsulate-2-layers', '2026-11-03', '#1098AD', '-'),
    ('Inlet + Thinsulate, 4 layers (3 Nov)', 'axi2217__8in__inlet-thinsulate-4-layers__r27-inlet-thinsulate-4-layers', '2026-11-03', '#7048E8', '-'),
    ('Inlet + Thinsulate 4 + rubber (3 Nov)', 'axi2217__8in__inlet-thinsulate-4-layers-rubber__r27-inlet-thinsulate-4-layers-rubber', '2026-11-03', '#2F9E44', '-'),
    ('Inlet + felt (3 Nov)', 'axi2217__8in__inlet-felt__r27-inlet-felt', '2026-11-03', '#A0522D', '-'),
    ('Duct, no lining, no inlet (2 Nov)', 'axi2217__8in__duct-unlined__r27-duct-unlined', '2026-11-02', '#495057', '-'),
]
PWM, LO, HI = 2000, 500, 24000


def perf(base, day):
    th, rpm, cur = [], [], []
    for p in sorted(glob.glob(bf.DATA + '/' + base + '/measurements/' + day + '*performance*')):
        if json.load(open(p + '/meta.json')).get('pwm_setpoint') != PWM: continue
        half = list(csv.DictReader(open(p + '/telemetry.csv')))
        half = half[len(half) // 2:]
        th.append(abs(st.median(float(r['thrust_n']) for r in half)))
        rpm.append(st.median(float(r['rpm']) for r in half) * 60 / 7)
        cur.append(st.median(float(r['current_a']) for r in half))
    assert len(th) == 3, (base, day, len(th))
    return th, rpm, cur


data = {}
for nm, base, day, col, ls in SETS:
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == PWM and g['cid'].startswith(day)]
    assert len(gs) == 3, (nm, len(gs))
    lv = np.array([bf.totals(g, LO, HI) for g in gs])
    th, rpm, cur = perf(base, day)
    data[nm] = (gs[0]['elev'], lv, col, ls)
    print(f'{nm:36} {lv.mean():5.1f} dB (repeat means {np.round(lv.mean(1), 2)})  thrust {np.mean(th):.2f} N {np.round(th, 2)}  '
          f'{np.mean(rpm):.0f} rpm  {np.mean(cur):.2f} A')

el = SETS and data[SETS[0][0]][0]
print('elev            ' + ' '.join(f'{int(e):>6}' for e in el))
for nm, (e, lv, _, _) in data.items():
    assert (e == el).all()
    print(f'{nm[:15]:15} ' + ' '.join(f'{x:6.1f}' for x in lv.mean(0)))
a, b, t, t4, t4r, fe, c = (data[s[0]][1].mean(0) for s in SETS)
print('felt - run1     ' + ' '.join(f'{x:+6.1f}' for x in fe - a))
print('thin4r - run1   ' + ' '.join(f'{x:+6.1f}' for x in t4r - a))
print('thin4 - run1    ' + ' '.join(f'{x:+6.1f}' for x in t4 - a))
print('run2 - run1     ' + ' '.join(f'{x:+6.1f}' for x in b - a))
print('thin2 - run1    ' + ' '.join(f'{x:+6.1f}' for x in t - a))
print('run1 - no inlet ' + ' '.join(f'{x:+6.1f}' for x in a - c))

allv = np.concatenate([lv.mean(0) for _, lv, _, _ in data.values()])
zmin, zmax = float(np.floor(allv.min()) - 1), float(np.ceil(allv.max()) + .5)
fig = plt.figure(figsize=(7.2, 7.6), dpi=200); ax = fig.add_subplot(111, projection='polar')
ax.bar(np.radians(270), zmax - zmin, width=np.radians(54), bottom=zmin, color='#eceff3', zorder=0)
for nm, (e, lv, col, ls) in data.items():
    v = lv.mean(0); th = np.radians(np.r_[e, 180 - e[::-1]]); r = np.r_[v, v[::-1]]
    ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=col, lw=2.4, ls=ls, marker='o', ms=4.5, mfc=col, mec='white', mew=.8, zorder=3, label=nm)
ax.set_rlim(zmin, zmax); zt = [t for t in range(int(zmin) + 1, int(zmax) + 1) if t % 2 == 0]; ax.set_rticks(zt)
ax.set_yticklabels([f'{t}' if i < len(zt) - 1 else f'{t} dB' for i, t in enumerate(zt)], fontsize=10, color='#555'); ax.set_rlabel_position(25)
[(t.set_bbox(dict(facecolor='white', edgecolor='none', alpha=.9, pad=1.5)), t.set_zorder(30)) for t in ax.get_yticklabels()]
ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=12, color='#333')
ax.grid(color='#cfd4dc', lw=1); ax.spines['polar'].set_color('#9aa3b2')
ax.legend(loc='upper center', bbox_to_anchor=(.5, -.06), fontsize=10, frameon=False, ncol=1)
ax.set_title('r27 duct at 2000 µs, 500 Hz–24 kHz, mean of 3 repeats\n(grey: −90°/−72°, probably in the flow; the no-inlet duct is from another day)', fontsize=10, color='#333', pad=18)
fig.savefig(os.path.join(HERE, 'polar-r27-inlet.png'), bbox_inches='tight', pad_inches=.15, facecolor='white')
print('polar-r27-inlet.png written, axis', zmin, zmax)
