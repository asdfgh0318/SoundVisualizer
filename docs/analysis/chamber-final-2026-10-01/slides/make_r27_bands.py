"""Where in frequency the inlet and the linings act: r27 duct set-ups at 2000 us, per third-octave band (100 Hz-20 kHz),
total, tone-notched broadband, and the blade-passage tones (BPF found per capture near 400 Hz). Level per set-up is the
dB mean over the front microphones (-54 to +90; -72/-90 probably sit in the flow), mean of the 3 repeats.

Prints a table of differences and draws bands-r27-inlet.png. The repeat floor is the bare-inlet run 2 minus run 1 (same day).
"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = ['x']
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sp = importlib.util.spec_from_file_location('bf', os.path.join(HERE, '..', 'build_final.py')); bf = importlib.util.module_from_spec(sp); sp.loader.exec_module(bf)

T = 'axi2217__8in__thinsulate-'
I = 'axi2217__8in__duct-unlined-inlet__r27-duct-unlined-inlet'
SETS = {
    'bare':    ('axi2217__8in__none__r27-8x45mr-bare-prop', '2026-11-02'),
    'duct':    ('axi2217__8in__duct-unlined__r27-duct-unlined', '2026-11-02'),
    'thin2':   (T + '2-layers__r27-thinsulate-2-layers-trial-2026-11-02', '2026-11-02'),
    'thin4':   (T + '4-layers__r27-thinsulate-4-layers', '2026-11-02'),
    'inlet':   (I, '2026-11-03'),
    'inlet_b': (I + '-trial-2026-11-03', '2026-11-03'),
    'i_thin2': ('axi2217__8in__inlet-thinsulate-2-layers__r27-inlet-thinsulate-2-layers', '2026-11-03'),
    'i_thin4': ('axi2217__8in__inlet-thinsulate-4-layers__r27-inlet-thinsulate-4-layers', '2026-11-03'),
}
FC = np.array([100 * 2 ** (i / 3) for i in range(24)])          # 100 Hz .. 20 kHz
NH = 10


def bpf(f, mags):
    m = mags.mean(0); sel = (f > 300) & (f < 500); k = np.where(sel)[0][np.argmax(m[sel])]
    y0, y1, y2 = m[k - 1], m[k], m[k + 1]; d = y0 - 2 * y1 + y2
    return f[k] + (0.5 * (y0 - y2) / d * (f[1] - f[0]) if abs(d) > 1e-9 else 0)


def analyse(g):
    f, mags = g['f'], g['mags']; df = f[1] - f[0]; lin = 10 ** (mags / 10); f0 = bpf(f, mags)
    tone = np.array([10 * np.log10(lin[:, np.abs(f - h * f0) <= 3 * df].sum(1) * df) for h in range(1, NH + 1)]).T
    mask = np.ones_like(f, bool)
    for k in range(1, int(21000 / (f0 / 2)) + 1):
        mask &= np.abs(f - k * f0 / 2) > (3 if k % 2 == 0 else 2) * df
    tot, bb = [], []
    for fc in FC:
        band = (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6)); kept = band & mask
        tot.append(10 * np.log10(lin[:, band].sum(1) * df))
        bb.append(10 * np.log10(lin[:, kept].sum(1) * df * band.sum() / kept.sum()))
    return f0, np.array(tot).T, np.array(bb).T, tone


R = {}
for k, (base, day) in SETS.items():
    gs = [g for g in bf.groups(bf.base(base), bf.CORR) if g['pwm'] == 2000 and g['cid'].startswith(day)]
    assert len(gs) == 3, (k, len(gs))
    front = gs[0]['elev'] >= -54
    a = [analyse(g) for g in gs]
    R[k] = dict(f0=np.mean([x[0] for x in a]),
                tot=np.mean([x[1][front].mean(0) for x in a], 0), bb=np.mean([x[2][front].mean(0) for x in a], 0),
                tone=np.mean([x[3][front].mean(0) for x in a], 0),
                rep_tot=np.ptp([x[1][front].mean(0) for x in a], 0))
    print(f"{k:8} BPF {R[k]['f0']:.1f} Hz")

PAIRS = [  # label, a, b (b minus a), same day?
    ('repeat floor: inlet run 2 − run 1', 'inlet', 'inlet_b', True),
    ('inlet − no inlet (unlined)', 'duct', 'inlet', False),
    ('Thinsulate 2 − unlined, no inlet', 'duct', 'thin2', True),
    ('Thinsulate 4 − unlined, no inlet', 'duct', 'thin4', True),
    ('Thinsulate 2 − unlined, with inlet', 'inlet', 'i_thin2', True),
    ('Thinsulate 4 − unlined, with inlet', 'inlet', 'i_thin4', True),
]
GROUPS = [('100–315 Hz', 100, 355), ('400–800 Hz', 355, 890), ('1–2 kHz', 890, 2240), ('2.5–5 kHz', 2240, 5600), ('6.3–10 kHz', 5600, 11200), ('12.5–20 kHz', 11200, 22400)]


def grp(v, lo, hi):
    sel = (FC >= lo) & (FC < hi); return 10 * np.log10((10 ** (v[sel] / 10)).sum())


print('\nTOTAL level per band group, front mics, b − a (dB); then broadband (tones notched)')
print(f"{'':38}" + ''.join(f'{g[0]:>13}' for g in GROUPS) + f"{'BPF':>7}{'2xBPF':>7}{'3xBPF':>7}")
for lab, a, b, same in PAIRS:
    t = [grp(R[b]['tot'], lo, hi) - grp(R[a]['tot'], lo, hi) for _, lo, hi in GROUPS]
    bb = [grp(R[b]['bb'], lo, hi) - grp(R[a]['bb'], lo, hi) for _, lo, hi in GROUPS]
    tn = R[b]['tone'][:3] - R[a]['tone'][:3]
    print(f"{lab + ('' if same else ' *'):38}" + ''.join(f'{x:+13.1f}' for x in t) + ''.join(f'{x:+7.1f}' for x in tn))
    print(f"{'   broadband':38}" + ''.join(f'{x:+13.1f}' for x in bb))
print('\nabsolute, total per group (dB):')
for k in ('bare', 'duct', 'inlet', 'thin4', 'i_thin4'):
    print(f"{k:38}" + ''.join(f'{grp(R[k]["tot"], lo, hi):13.1f}' for _, lo, hi in GROUPS) + ''.join(f'{x:7.1f}' for x in R[k]['tone'][:3]))
print('\ntones, front-mic mean (dB), harmonics 1..10:')
for k in ('duct', 'inlet', 'thin2', 'i_thin2', 'thin4', 'i_thin4'):
    print(f"{k:10}" + ''.join(f'{x:7.1f}' for x in R[k]['tone']))

# ---- figure: b - a per third-octave band, total and broadband, with the repeat floor shaded ----
fl = np.abs(R['inlet_b']['tot'] - R['inlet']['tot'])
fig, axs = plt.subplots(3, 1, figsize=(9, 10), dpi=170, sharex=True, gridspec_kw=dict(hspace=.12))
panels = [('Inlet vs no inlet (unlined; 3 Nov − 2 Nov, crosses days)', [('inlet − no inlet', 'duct', 'inlet', '#0B7285')]),
          ('Linings, no inlet (2 Nov, same day)', [('Thinsulate 2 − unlined', 'duct', 'thin2', '#F08C00'), ('Thinsulate 4 − unlined', 'duct', 'thin4', '#E03131')]),
          ('Linings, with inlet (3 Nov, same day)', [('Thinsulate 2 − unlined', 'inlet', 'i_thin2', '#F08C00'), ('Thinsulate 4 − unlined', 'inlet', 'i_thin4', '#E03131')])]
for ax, (title, lines) in zip(axs, panels):
    ax.fill_between(FC, -fl, fl, color='#dee2e6', step='mid', label='repeat floor (inlet run 2 vs run 1)')
    ax.axhline(0, color='#868E96', lw=1)
    for lab, a, b, col in lines:
        ax.semilogx(FC, R[b]['tot'] - R[a]['tot'], color=col, lw=2.2, marker='o', ms=3.5, label=lab + ', total')
        ax.semilogx(FC, R[b]['bb'] - R[a]['bb'], color=col, lw=1.3, ls='--', label=lab + ', tones notched')
    f0 = R['inlet']['f0']
    for h in range(1, 6):
        ax.axvline(h * f0, color='#adb5bd', lw=.7, ls=':')
    ax.set_title(title, fontsize=10, loc='left'); ax.set_ylabel('Δ level, dB'); ax.grid(color='#e9ecef', lw=.8, which='both')
    ax.legend(fontsize=7.5, loc='lower right', ncol=2, frameon=False); ax.set_ylim(-7.5, 3)
axs[-1].set_xlabel('third-octave band centre, Hz (dotted: BPF harmonics 1–5)')
axs[-1].set_xticks([100, 200, 500, 1000, 2000, 5000, 10000, 20000]); axs[-1].set_xticklabels(['100', '200', '500', '1k', '2k', '5k', '10k', '20k'])
fig.suptitle('r27 duct, 2000 µs: level difference per third-octave band, front microphones (−54° to +90°), mean of 3 repeats', fontsize=10.5)
fig.savefig(os.path.join(HERE, 'bands-r27-inlet.png'), bbox_inches='tight', facecolor='white')
print('bands-r27-inlet.png written')
