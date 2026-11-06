"""Is the duct wall acoustically transparent? A directional test from the arc we already have.

The duct axis is vertical: +90 deg looks into the inlet, -90 deg into the jet (in the flow), 0 deg looks at the side
wall. Sound reaches the side mics (0, +-18) either through the wall (breakout) or by diffracting round the open ends;
the top mics (+54..+90) hear the inlet opening. Per third-octave band:

  side-minus-top  S(f) = mean L(0, +-18) - mean L(+54, +72, +90)          (dB, per set-up)

For the bare prop S(f) is the propeller's own directivity. A duct with an OPAQUE wall should push S(f) down (the side
is shielded, the noise comes out of the ends); a TRANSPARENT wall leaves S(f) near the bare-prop value. A lining that
only absorbs inside the duct lowers both groups alike (S unchanged); one that cuts breakout lowers S.

Also prints, per set-up, the lining effect split into side and top (Δside, Δtop vs the unlined inlet duct).
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
SETS = [  # key, label, base, day, colour, style
    ('bare', 'bare prop (2 Nov)', 'axi2217__8in__none__r27-8x45mr-bare-prop', '2026-11-02', '#000000', '-'),
    ('duct', 'duct, no inlet (2 Nov)', 'axi2217__8in__duct-unlined__r27-duct-unlined', '2026-11-02', '#868E96', '-'),
    ('inlet', 'duct + inlet, unlined (3 Nov, run 1)', I, '2026-11-03', '#0B7285', '-'),
    ('inlet_b', 'duct + inlet, unlined (3 Nov, run 2)', I + '-trial-2026-11-03', '2026-11-03', '#0B7285', '--'),
    ('thin2', 'inlet + Thinsulate 2 (3 Nov)', 'axi2217__8in__inlet-thinsulate-2-layers__r27-inlet-thinsulate-2-layers', '2026-11-03', '#F08C00', '-'),
    ('thin4', 'inlet + Thinsulate 4 (3 Nov)', 'axi2217__8in__inlet-thinsulate-4-layers__r27-inlet-thinsulate-4-layers', '2026-11-03', '#E03131', '-'),
    ('thin4r', 'inlet + Thinsulate 4 + rubber (3 Nov)', 'axi2217__8in__inlet-thinsulate-4-layers-rubber__r27-inlet-thinsulate-4-layers-rubber', '2026-11-03', '#9C36B5', '-'),
    ('felt', 'inlet + felt (3 Nov)', 'axi2217__8in__inlet-felt__r27-inlet-felt', '2026-11-03', '#2F9E44', '-'),
    ('petg', 'inlet + PETG 1-layer wall (4 Nov)', 'axi2217__8in__inlet-petg-1-layer__r27-inlet-petg-1-layer', '2026-11-04', '#A0522D', '-'),
]
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])
SIDE, TOP = (0, 18, -18), (54, 72, 90)


def bands(g):
    f, lin = g['f'], 10 ** (g['mags'] / 10); df = f[1] - f[0]
    return np.array([10 * np.log10(lin[:, (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))].sum(1) * df) for fc in FC]).T


R = {}
for k, lab, base, day, col, ls in SETS:
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(day)]
    assert len(gs) == 3, (k, len(gs))
    el = gs[0]['elev'].astype(int)
    B = np.mean([bands(g) for g in gs], 0)
    side, top = B[np.isin(el, SIDE)].mean(0), B[np.isin(el, TOP)].mean(0)
    R[k] = dict(side=side, top=top, S=side - top)

GRP = [('100–315', 100, 355), ('400–800', 355, 890), ('1–2k', 890, 2240), ('2.5–5k', 2240, 5600), ('6.3–10k', 5600, 11200), ('12.5–20k', 11200, 22400)]
g = lambda v, lo, hi: v[(FC >= lo) & (FC < hi)].mean()
print('side-minus-top S (dB), band-group means of the per-band values')
print(f"{'':40}" + ''.join(f'{n:>10}' for n, _, _ in GRP))
for k, lab, *_ in SETS:
    print(f'{lab:40}' + ''.join(f'{g(R[k]["S"], lo, hi):+10.1f}' for _, lo, hi in GRP))
print('\nshielding = S(set-up) - S(bare prop): how much the duct pushes the side down relative to the top')
for k, lab, *_ in SETS[1:]:
    print(f'{lab:40}' + ''.join(f'{g(R[k]["S"] - R["bare"]["S"], lo, hi):+10.1f}' for _, lo, hi in GRP))
print('\nlining effect vs unlined inlet (run 1): Δside / Δtop per group')
for k, lab, *_ in SETS[3:]:
    print(f'{lab:40}' + ''.join(f'{g(R[k]["side"] - R["inlet"]["side"], lo, hi):+5.1f}/{g(R[k]["top"] - R["inlet"]["top"], lo, hi):+4.1f}' for _, lo, hi in GRP))

fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 9), dpi=160, sharex=True, gridspec_kw=dict(hspace=.14))
for k, lab, base, day, col, ls in SETS:
    a1.semilogx(FC, R[k]['S'], color=col, ls=ls, lw=2.6 if k in ('bare', 'duct', 'inlet') else 1.7, marker='o', ms=3, label=lab)
    if k not in ('bare', 'duct', 'inlet'):
        a2.semilogx(FC, R[k]['S'] - R['inlet']['S'], color=col, ls=ls, lw=1.8, marker='o', ms=3, label=lab)
a1.axhline(0, color='#adb5bd', lw=1)
a1.set_ylabel('side − top, dB\n(0°,±18° minus +54…+90°)')
a1.set_title('How much quieter the side of the duct is than its inlet, per third-octave band (2000 µs)', fontsize=10.5, loc='left')
a1.legend(fontsize=7.5, ncol=2, frameon=False, loc='lower left')
a2.axhline(0, color='#0B7285', lw=1.2)
a2.axhspan(-.3, .3, color='#e9ecef', zorder=0)
a2.set_ylabel('change of side − top\nvs unlined inlet duct, dB')
a2.set_title('Below zero: the lining/wall cuts the side more than the inlet → it acts on what leaves sideways (breakout or near-wall field)', fontsize=9.5, loc='left')
a2.legend(fontsize=7.5, ncol=2, frameon=False, loc='lower left')
for a in (a1, a2):
    a.grid(color='#e9ecef', which='both')
a2.set_xticks([100, 200, 500, 1000, 2000, 5000, 10000, 20000]); a2.set_xticklabels(['100', '200', '500', '1k', '2k', '5k', '10k', '20k'])
a2.set_xlabel('third-octave band centre, Hz (grey band: ±0.3 dB, the repeat floor of a group mean)')
fig.savefig(os.path.join(HERE, 'wall-side-vs-top-r27.png'), bbox_inches='tight', facecolor='white')
print('wall-side-vs-top-r27.png written')
