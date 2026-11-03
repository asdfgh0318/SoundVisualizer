"""Polar overlay of the r27 duct set-ups (8in APC 8x4.5MR, AXI 2217/12), 2000 us, total level 500 Hz-24 kHz, mean of the 3 repeats, corrected microphone files; plus thrust and rpm per set-up.

Only the captures taken with the new lining fit (from 30 Oct) are used, and each base is read on one day only: the
data repo is an additive backup, so a base that was re-measured still holds the old day's captures under the same name.
"""
import sys, os, json, glob, csv, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import importlib.util, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

MECH_PER_ELEC = 60 / 7          # the stand's rpm is electrical; AXI 2217/12 has 14 poles
T = 'axi2217__8in__thinsulate-'
SETS = [  # label, base, day (YYYY-MM-DD, the only day read from that base), colour
    ('Bare prop, no duct', 'axi2217__8in__none__r27-8x45mr-bare-prop', '2026-11-02', '#000000'),
    ('Duct, no lining', 'axi2217__8in__duct-unlined__r27-duct-unlined', '2026-11-02', '#868E96'),
    ('Thinsulate, 2 layers', T + '2-layers__r27-thinsulate-2-layers-trial-2026-11-02', '2026-11-02', '#F08C00'),
    ('Thinsulate, 4 layers', T + '4-layers__r27-thinsulate-4-layers', '2026-11-02', '#E03131'),
    ('Thinsulate, 6 layers', T + '6-layers__r27-thinsulate-6-layers', '2026-10-30', '#1098AD'),
    ('Thinsulate, 8 layers', T + '8-layers__r27-thinsulate-8-layers-archive-2026-11-02-trial-1619', '2026-11-02', '#C2255C'),
    ('Thinsulate, 10 layers', T + '10-layers__r27-thinsulate-10-layers', '2026-11-02', '#7048E8'),
]
LO, HI, PWM = 500, 24000, 2000
DAYLABEL = lambda d: f'{int(d[8:])} {["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(d[5:7])]}'


def perf(base, day):
    """thrust (N, magnitude), mechanical rpm and current at PWM: median of the second half of each step, mean over the repeats"""
    th, rpm, cur = [], [], []
    for p in sorted(glob.glob(bf.DATA + '/' + base + '/measurements/' + day + '*performance*')):
        if json.load(open(p + '/meta.json')).get('pwm_setpoint') != PWM: continue
        rows = list(csv.DictReader(open(p + '/telemetry.csv')))[0:]
        half = rows[len(rows) // 2:]
        th.append(st.median(float(r['thrust_n']) for r in half))
        rpm.append(st.median(float(r['rpm']) for r in half) * MECH_PER_ELEC)
        cur.append(st.median(float(r['current_a']) for r in half))
    assert len(th) == 3, (base, day, len(th))
    return dict(thrust=abs(float(np.mean(th))), thrust_rng=[abs(max(th)), abs(min(th))], rpm=float(np.mean(rpm)),
                rpm_rng=[min(rpm), max(rpm)], current=float(np.mean(cur)))


data, out = {}, {}
for nm, base, day, col in SETS:
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == PWM and g['cid'].startswith(day)]
    assert len(gs) == 3, (nm, len(gs))
    lv = np.array([bf.totals(g, LO, HI) for g in gs])
    data[nm] = (gs[0]['elev'], lv.mean(0), col, day)
    p = perf(base, day)
    out[nm] = dict(mean=round(float(lv.mean()), 1), repeat_spread=round(float(np.ptp(lv.mean(1))), 2), color=col, day=DAYLABEL(day), base=base,
                   thrust=round(p['thrust'], 2), thrust_min_max=[round(x, 2) for x in sorted(p['thrust_rng'])], rpm=round(p['rpm']),
                   rpm_min_max=[round(x) for x in p['rpm_rng']], current=round(p['current'], 2),
                   per_mic=dict(zip([int(e) for e in gs[0]['elev']], [round(float(x), 1) for x in lv.mean(0)])))

allv = np.concatenate([v for _, v, _, _ in data.values()]); rmin = float(np.floor(allv.min()) - 2); rmax = float(np.ceil(allv.max()) + 1)
fig = plt.figure(figsize=(6.4, 6.4), dpi=220); ax = fig.add_subplot(111, projection='polar')
for nm, (el, v, col, day) in data.items():
    th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
    ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=col, lw=3.4 if nm.startswith('Bare') else 2.0, ls='-',
            marker='o' if day == '2026-10-30' else 's', ms=4, mfc=col, mec='white', mew=.8)
ax.set_rlim(rmin, rmax); ticks = [t for t in range(int(rmin), int(rmax) + 1) if t % 5 == 0 and t > rmin]; ax.set_rticks(ticks)
ax.set_yticklabels([f'{t}' if i < len(ticks) - 1 else f'{t} dB' for i, t in enumerate(ticks)], fontsize=10, color='#555'); ax.set_rlabel_position(25)
[(t.set_bbox(dict(facecolor='white', edgecolor='none', alpha=.9, pad=1.5)), t.set_zorder(30)) for t in ax.get_yticklabels()]
ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=12, color='#333'); ax.grid(color='#cfd4dc', lw=1); ax.spines['polar'].set_color('#9aa3b2')
fig.savefig(os.path.join(HERE, 'polar-r27.png'), bbox_inches='tight', pad_inches=.15, facecolor='white')
json.dump(dict(axis=[rmin, rmax], sets=out), open(os.path.join(HERE, 'r27.json'), 'w'), indent=1, ensure_ascii=False)
print('rlim', rmin, rmax)
for k, v in out.items():
    print(f"{k:24} {v['day']:7} {v['mean']:5.1f} dB (rep spread {v['repeat_spread']}) {v['thrust']:6.2f} N {v['thrust_min_max']} {v['rpm']:6d} rpm {v['rpm_min_max']} {v['current']:.2f} A")
