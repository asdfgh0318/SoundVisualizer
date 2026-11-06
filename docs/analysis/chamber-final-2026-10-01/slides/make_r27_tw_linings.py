"""Do the linings work better behind an acoustically transparent wall? (r27, inlet fitted, 2000 us)

Round 1 (3 Nov): lining straight in the inlet duct, against the unlined inlet duct, same day.
Round 2 (6 Nov): lining behind the transparent wall, against the transparent wall alone, same day.
For each: total level 500 Hz-24 kHz (the slide's metric) and band groups, front mics (-54..+90), and the side
(0, +-18) / top (+54..+90) split. Levels are the mean of the 3 repeats. Missing bases are skipped.
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import numpy as np
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)
sys.path.insert(0, HERE)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
TW = 'axi2217__8in__inlet-transparent-wall__r27-inlet-transparent-wall'
ROUNDS = [  # label, lined base, day, reference base, reference day
    ('Thinsulate 2, plain inlet duct (3 Nov)', 'axi2217__8in__inlet-thinsulate-2-layers__r27-inlet-thinsulate-2-layers', '2026-11-03', I, '2026-11-03'),
    ('Thinsulate 4, plain inlet duct (3 Nov)', 'axi2217__8in__inlet-thinsulate-4-layers__r27-inlet-thinsulate-4-layers', '2026-11-03', I, '2026-11-03'),
    ('Thinsulate 2, behind transparent wall (6 Nov)', 'axi2217__8in__inlet-transparent-wall-thinsulate-2-layers__r27-inlet-transparent-wall-thinsulate-2-layers', '2026-11-06', TW, '2026-11-06'),
    ('Thinsulate 4, behind transparent wall (6 Nov)', 'axi2217__8in__inlet-transparent-wall-thinsulate-4-layers__r27-inlet-transparent-wall-thinsulate-4-layers', '2026-11-06', TW, '2026-11-06'),
    ('repeat floor: unlined inlet run 2 vs run 1 (3 Nov)', I + '-trial-2026-11-03', '2026-11-03', I, '2026-11-03'),
]
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])
G = [('100–315', 100, 355), ('400–800', 355, 890), ('1–2k', 890, 2240), ('2.5–5k', 2240, 5600), ('6.3–20k', 5600, 22400)]


def load(base, day):
    try:
        bd = bf.base(base)
    except BaseException:
        return None
    gs = [g for g in bf.groups(bd, bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(day)]
    if len(gs) != 3:
        return None
    f = gs[0]['f']; df = f[1] - f[0]
    def bands(g):
        lin = 10 ** (g['mags'] / 10)
        return np.array([10 * np.log10(lin[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T
    return dict(el=gs[0]['elev'].astype(int), tot=np.mean([bf.totals(g, 500, 24000) for g in gs], 0), B=np.mean([bands(g) for g in gs], 0))


print(f"{'':52}{'total':>7}{'side':>7}{'top':>7}" + ''.join(f'{n:>9}' for n, *_ in G) + '   (dB, lined − reference, front mics)')
for lab, b, d, rb, rd in ROUNDS:
    A, R = load(b, d), load(rb, rd)
    if A is None or R is None:
        print(f'{lab:52}  (not captured yet)'); continue
    el = A['el']; fr = el >= -54; side = np.isin(el, (0, 18, -18)); top = np.isin(el, (54, 72, 90))
    dt = A['tot'] - R['tot']; dB = A['B'] - R['B']
    print(f'{lab:52}{dt[fr].mean():+7.2f}{dt[side].mean():+7.2f}{dt[top].mean():+7.2f}' + ''.join(f'{dB[fr][:, (FC >= lo) & (FC < hi)].mean():+9.2f}' for _, lo, hi in G))
