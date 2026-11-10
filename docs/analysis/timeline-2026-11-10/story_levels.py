"""Thrust, electrical power and sound level of every prop run from 2 Oct 2026 on, at 2000 us.

Writes levels.csv next to this file (PWM=1900 START=2026-11-03 in the environment writes levels-1900.csv
for the runs from that day on). One row per run (recordings stored under two base names are
merged, shortest name kept). Level = total 500 Hz-20 kHz per microphone (measured capsule
corrections applied), dB-mean over the microphones, mean over the run's repeats at 2000 us:
  level_front  microphones -54..+90 deg (the two lowest sit in the flow of the ducted set-ups)
  level_all    all eleven
Telemetry is the mean of the 2000 us steps; power = V x A; rpm is electrical as logged.
"""
import csv, glob, json, os, sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, ROOT); sys.path.insert(0, ROOT + '/docs/analysis/baseline-story-2026-09-30')
from story_lib import groups
DATA = os.path.expanduser('~/ŻYCIE/PRACA/SoundVisualizer-data/data'); CORR = DATA + '/calibrations'
TZ = ZoneInfo('Europe/Warsaw'); START = os.environ.get('START', '2026-10-02'); PWM = int(os.environ.get('PWM', 2000)); LO, HI = 500, 20000


def ts(cid):
    return datetime.strptime(cid, '%Y-%m-%dT%H-%M-%S-%f').replace(tzinfo=timezone.utc)


def tel(path):
    rows = list(csv.DictReader(open(path)))
    return {k: float(np.mean([float(r[k]) for r in rows])) for k in ('thrust_n', 'current_a', 'voltage_v', 'rpm', 'torque_nm')}


def total(g):
    f = g['f']; df = f[1] - f[0]; m = (f >= LO) & (f < HI)
    return 10 * np.log10((10 ** (g['mags'][:, m] / 10)).sum(1) * df)


runs = []
for bdir in sorted(glob.glob(DATA + '/*/measurements')):
    base = bdir.split('/')[-2]
    cids = sorted({os.path.basename(p).split('__')[0] for p in glob.glob(bdir + '/*__performance')})
    if not cids or cids[-1][:10] < START:
        continue
    split, cur = [], []
    for c in cids:
        if cur and (ts(c) - ts(cur[-1])).total_seconds() > 120:
            split.append(cur); cur = []
        cur.append(c)
    split.append(cur)
    split = [r for r in split if r[0][:10] >= START]
    if not split:
        continue
    gs = {g['cid']: g for g in groups(os.path.dirname(bdir), CORR) if g['pwm'] == PWM}
    for r in split:
        top = [c for c in r if json.load(open(f'{bdir}/{c}__performance/meta.json'))['pwm_setpoint'] == PWM]
        runs.append(dict(base=base, cids=frozenset(r), top=top, gs=[gs[c] for c in top if c in gs], bdir=bdir))
    print(base, len(split), file=sys.stderr)

seen, out = {}, []
for r in sorted(runs, key=lambda r: len(r['base'])):
    key = min(r['cids'])
    if key in seen:
        seen[key]['also'].append(r['base'].split('__')[-1]); continue
    seen[key] = r; r['also'] = []; out.append(r)

rows = []
for r in sorted(out, key=lambda r: min(r['cids'])):
    t = [tel(f"{r['bdir']}/{c}__performance/telemetry.csv") for c in r['top']]
    if not t:
        continue
    m = {k: float(np.mean([x[k] for x in t])) for k in t[0]}
    thr = [abs(x['thrust_n']) for x in t]
    p = m['voltage_v'] * m['current_a']
    start = ts(min(r['cids'])).astimezone(TZ)
    motor, prop, shroud, notes = r['base'].split('__')
    row = dict(date=start.strftime('%Y-%m-%d'), time=start.strftime('%H:%M'), notes=notes, motor=motor, propeller=prop, shroud=shroud,
               repeats=len(t), thrust_n=round(abs(m['thrust_n']), 2), thrust_min=round(min(thr), 2), thrust_max=round(max(thr), 2),
               voltage_v=round(m['voltage_v'], 2), current_a=round(m['current_a'], 2), power_w=round(p, 1),
               n_per_w=round(abs(m['thrust_n']) / p, 4) if p > 1 else '', rpm_electrical=round(m['rpm'], 0),
               also_stored_as='; '.join(r['also']))
    if r['gs']:
        front = r['gs'][0]['elev'] >= -54
        lv = [total(g) for g in r['gs']]
        lf = [float(x[front].mean()) for x in lv]
        row.update(level_front=round(float(np.mean(lf)), 2), level_front_spread=round(float(np.ptp(lf)), 2),
                   level_all=round(float(np.mean([x.mean() for x in lv])), 2), level_repeats=len(lv))
    rows.append(row)

fields = ['date', 'time', 'notes', 'motor', 'propeller', 'shroud', 'repeats', 'thrust_n', 'thrust_min', 'thrust_max', 'voltage_v', 'current_a',
          'power_w', 'n_per_w', 'rpm_electrical', 'level_front', 'level_front_spread', 'level_all', 'level_repeats', 'also_stored_as']
with open(HERE + ('/levels.csv' if PWM == 2000 else f'/levels-{PWM}.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, restval=''); w.writeheader(); w.writerows(rows)
print(len(rows), 'runs written')
