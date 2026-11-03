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
    ('Duct + inlet, no lining', 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet', '2026-11-03', '#0B7285'),   # run 1; the repeat (trial base) agrees to 0.04 N
    ('Inlet + Thinsulate, 2 layers', 'axi2217__8in__inlet-thinsulate-2-layers__r27-inlet-thinsulate-2-layers', '2026-11-03', '#F08C00'),
    ('Inlet + Thinsulate, 4 layers', 'axi2217__8in__inlet-thinsulate-4-layers__r27-inlet-thinsulate-4-layers', '2026-11-03', '#E03131'),
    ('Thinsulate, 2 layers', T + '2-layers__r27-thinsulate-2-layers-trial-2026-11-02', '2026-11-02', '#F08C00'),
    ('Thinsulate, 4 layers', T + '4-layers__r27-thinsulate-4-layers', '2026-11-02', '#E03131'),
    ('Thinsulate, 6 layers', T + '6-layers__r27-thinsulate-6-layers', '2026-10-30', '#1098AD'),
    ('Thinsulate, 8 layers', T + '8-layers__r27-thinsulate-8-layers-archive-2026-11-02-trial-1619', '2026-11-02', '#C2255C'),
    ('Thinsulate, 10 layers', T + '10-layers__r27-thinsulate-10-layers', '2026-11-02', '#7048E8'),
    # fitted the old way, before the new lining fit of 30 Oct, and on other days: indicative only
    ('Felt', 'axi2217__8in__felt__r27-felt', '2026-10-28', '#2F9E44'),
    ('Felt, double layer', 'axi2217__8in__felt-2-layers__r27-felt-2-layers', '2026-10-29', '#5C940D'),
    ('Felt, double + rubber', 'axi2217__8in__felt-2-layers-rubber__r27-felt-2-layers-rubber', '2026-10-29', '#862E9C'),
    ('Rubber', 'axi2217__8in__rubber__r27-rubber', '2026-10-29', '#1864AB'),
    ('PU foam', 'axi2217__8in__pu-foam__r27-pu-foam', '2026-10-28', '#A0522D'),          # base also holds the deleted 27 Oct run
    ('PU foam + rubber', 'axi2217__8in__pu-foam-rubber__r27-pu-foam-rubber', '2026-10-29', '#FCC419'),
]
MARK = {'2026-11-03': '*', '2026-11-02': 's', '2026-10-30': 'o', '2026-10-29': 'D', '2026-10-28': '^'}
OLD_FIT = {'2026-10-28', '2026-10-29'}
LO, HI, PWM = 500, 24000, 2000
LS = {k: (0, (5, 1.6)) for k in ('Duct + inlet, no lining', 'Inlet + Thinsulate, 2 layers', 'Inlet + Thinsulate, 4 layers')}   # dashed: the duct with the inlet
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
                   old_fit=day in OLD_FIT, thrust=round(p['thrust'], 2), thrust_min_max=[round(x, 2) for x in sorted(p['thrust_rng'])], rpm=round(p['rpm']),
                   rpm_min_max=[round(x) for x in p['rpm_rng']], current=round(p['current'], 2),
                   per_mic=dict(zip([int(e) for e in gs[0]['elev']], [round(float(x), 1) for x in lv.mean(0)])))

allv = np.concatenate([v for _, v, _, _ in data.values()]); rmin = float(np.floor(allv.min()) - 2); rmax = float(np.ceil(allv.max()) + 1)
fig = plt.figure(figsize=(6.4, 6.4), dpi=220); ax = fig.add_subplot(111, projection='polar')
for nm, (el, v, col, day) in data.items():
    th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
    ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=col, lw=3.4 if nm.startswith('Bare') else 2.0, ls=LS.get(nm, '-'),
            marker=MARK[day], ms=4, mfc=col, mec='white', mew=.8)
ax.set_rlim(rmin, rmax); ticks = [t for t in range(int(rmin), int(rmax) + 1) if t % 5 == 0 and t > rmin]; ax.set_rticks(ticks)
ax.set_yticklabels([f'{t}' if i < len(ticks) - 1 else f'{t} dB' for i, t in enumerate(ticks)], fontsize=10, color='#555'); ax.set_rlabel_position(25)
[(t.set_bbox(dict(facecolor='white', edgecolor='none', alpha=.9, pad=1.5)), t.set_zorder(30)) for t in ax.get_yticklabels()]
ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=12, color='#333'); ax.grid(color='#cfd4dc', lw=1); ax.spines['polar'].set_color('#9aa3b2')
fig.savefig(os.path.join(HERE, 'polar-r27.png'), bbox_inches='tight', pad_inches=.15, facecolor='white')
json.dump(dict(axis=[rmin, rmax], sets=out), open(os.path.join(HERE, 'r27.json'), 'w'), indent=1, ensure_ascii=False)
print('rlim', rmin, rmax)
for k, v in out.items():
    print(f"{k:24} {v['day']:7} {v['mean']:5.1f} dB (rep spread {v['repeat_spread']}) {v['thrust']:6.2f} N {v['thrust_min_max']} {v['rpm']:6d} rpm {v['rpm_min_max']} {v['current']:.2f} A")


# ---- line version: level against microphone angle, one line per set-up next to each other ----
# The polar hides the 0.1-1 dB differences between linings under the 11 dB gap to the bare prop, so the bare prop
# stays in the slide's list but not in this chart, and the lower panel shows each set-up minus the unlined duct.
REF = 'Duct, no lining'
el = data[REF][0]
order = np.argsort(el)
x = el[order]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 6.4), dpi=220, sharex=True, gridspec_kw=dict(height_ratios=[1.15, 1], hspace=.08))
for a in (a1, a2):
    a.axvspan(-99, -63, color='#eceff3', zorder=0)
    a.grid(color='#dde1e7', lw=.8); a.set_axisbelow(True)
    for sp_ in ('top', 'right'): a.spines[sp_].set_visible(False)
for nm, (e, v, col, day) in data.items():
    if nm.startswith('Bare'): continue
    y = v[order]; ref = data[REF][1][order]
    mk = MARK[day]
    lw = 2.6 if nm == REF else 2.0
    a1.plot(x, y, color=col, lw=lw, marker=mk, ms=5, mfc=col, mec='white', mew=.8, zorder=3)
    a2.plot(x, y - ref, color=col, lw=lw, marker=mk, ms=5, mfc=col, mec='white', mew=.8, zorder=3)
a1.set_ylabel('level, dB SPL', fontsize=11, color='#333')
a2.set_ylabel('minus unlined duct, dB', fontsize=11, color='#333')
a2.axhline(0, color='#868E96', lw=1.2)
a2.set_xticks(x); a2.set_xticklabels([f'{int(t):+d}°'.replace('-', '−') if t else '0°' for t in x], fontsize=10)
a2.set_xlabel('microphone elevation', fontsize=11, color='#333')
a2.set_xlim(-95, 95)
a1.text(-79, a1.get_ylim()[1] - .3, 'in the flow?\nvaries ~1 dB\nrun to run', fontsize=7.5, color='#6b7280', ha='center', va='top')
for a in (a1, a2): a.tick_params(labelsize=10, colors='#444')
fig.savefig(os.path.join(HERE, 'lines-r27.png'), bbox_inches='tight', pad_inches=.12, facecolor='white')
print('lines-r27.png written')


# ---- zoomed polar: the same plot, radial axis on the duct set-ups only, so each lining is its own line ----
duct_v = np.concatenate([v for nm, (_, v, _, _) in data.items() if not nm.startswith('Bare')])
zmin, zmax = float(np.floor(duct_v.min()) - 1), float(np.ceil(duct_v.max()) + .5)
fig = plt.figure(figsize=(6.4, 6.4), dpi=220); ax = fig.add_subplot(111, projection='polar')
ax.bar(np.radians(270), zmax - zmin, width=np.radians(54), bottom=zmin, color='#eceff3', zorder=0)   # -90/-72 region, probably in the flow
for nm, (el, v, col, day) in data.items():
    if nm.startswith('Bare'): continue
    th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
    ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=col, lw=2.6 if nm in ('Duct, no lining', 'Duct + inlet, no lining') else 2.0, ls=LS.get(nm, '-'),
            marker=MARK[day], ms=4.5, mfc=col, mec='white', mew=.8, zorder=3)
ax.set_rlim(zmin, zmax); zt = [t for t in range(int(zmin) + 1, int(zmax) + 1) if t % 2 == 0]; ax.set_rticks(zt)
ax.set_yticklabels([f'{t}' if i < len(zt) - 1 else f'{t} dB' for i, t in enumerate(zt)], fontsize=10, color='#555'); ax.set_rlabel_position(25)
[(t.set_bbox(dict(facecolor='white', edgecolor='none', alpha=.9, pad=1.5)), t.set_zorder(30)) for t in ax.get_yticklabels()]
ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=12, color='#333'); ax.grid(color='#cfd4dc', lw=1); ax.spines['polar'].set_color('#9aa3b2')
fig.savefig(os.path.join(HERE, 'polar-r27-zoom.png'), bbox_inches='tight', pad_inches=.15, facecolor='white')
R = json.load(open(os.path.join(HERE, 'r27.json'))); R['zoom_axis'] = [zmin, zmax]; json.dump(R, open(os.path.join(HERE, 'r27.json'), 'w'), indent=1, ensure_ascii=False)
print('polar-r27-zoom.png written, axis', zmin, zmax)
