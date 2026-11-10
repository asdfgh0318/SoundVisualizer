"""timeline-fig.png: every run of the six steps in time order, thrust above and level below.

Read from levels.csv (2000 us) and, for the 9 Nov step, levels-1900.csv (most 2000 us steps of that day have a fault).
One mark per run. Level = total 500 Hz-20 kHz, microphones -54..+90 deg.
"""
import csv, os, textwrap
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = list(csv.DictReader(open(HERE + '/levels.csv')))
R19 = [r for r in csv.DictReader(open(HERE + '/levels-1900.csv')) if r['notes'].startswith('g5-')]
INK, MUTED, GRID, SURF = '#0b0b0b', '#52514e', '#e6e5e0', '#fcfcfb'
KIND = {'bare': ('Bare propeller', '#2a78d6', 'o'), 'unlined': ('Empty cage or unlined duct', '#eb6834', 's'), 'lined': ('With material or lining', '#1baf7a', 'D')}
STATUS = {'Fault': '#c92a2a', 'Not a win': '#c92a2a', 'Gain': '#e8590c', 'Win on thrust': '#2f9e44'}


def kind(n):
    if 'bare-prop' in n or n == 'v1-naked-horizontal':
        return 'bare'
    if n.startswith(('v1-naked-cage', 'v1-membrane-duct-small', 'r27-duct-unlined', 'g5-duct-unlined')) or n == 'r27-inlet-transparent-wall':
        return 'unlined'
    return 'lined'


def pick(rows, f):
    return [r for r in rows if f(r)]


v1 = lambda r: r['notes'].startswith('v1-')
STEPS = [  # title, dates, outcome, rows, what the data show
    ('Materials around\nthe 5 in propeller', '2 and 7 Oct', 'Fault', pick(R, lambda r: v1(r) and r['propeller'] == '5in3b' and 'membrane' not in r['notes'] and r['motor'] != 'f30' and float(r['thrust_n']) > 0.1),
     'Materials: 76.5–79.7 dB against 72–73 dB bare'),
    ('8x4.5 propeller\nin the cage', '7 Oct', 'Fault', pick(R, lambda r: r['notes'].endswith('-bp')), '82–87 dB against 75.6 dB'),
    ('Small duct with\na membrane wall', '8–9 Oct', 'Fault', pick(R, lambda r: r['motor'] == 'f30'), 'Thrust 3.76 → 0.4–1.2 N, 8.5–15.7 dB louder'),
    ('8 in duct with linings, no inlet', '27 Oct – 2 Nov', 'Not a win', pick(R, lambda r: r['notes'].startswith('r27-') and 'inlet' not in r['notes']),
     'Thrust 5.7–9.2 N depending on lining and mount; Thinsulate 4 looked best on 2 Nov, but the gain came with the thrust; duct about 13 dB louder than the bare propeller'),
    ('Inlet added', '3–6 Nov', 'Win on thrust', pick(R, lambda r: 'inlet' in r['notes']), 'Every set-up at 10.0–10.3 N; level unchanged'),
    ('5 in propeller in\nthe 8 in duct', '9 Nov, 1900 µs', 'Gain', R19, 'Linings −0.7 / −0.9 dB'),
]

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.edgecolor': GRID, 'text.color': INK, 'axes.labelcolor': MUTED,
                     'xtick.color': MUTED, 'ytick.color': MUTED})
fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 4.9), dpi=200, sharex=True, gridspec_kw=dict(hspace=.09, left=.055, right=.995, top=.775, bottom=.145))
fig.patch.set_facecolor(SURF)
x, GAP, seen = 0, 2.2, set()
for i, (title, dates, outcome, rows, note) in enumerate(STEPS):
    rows = sorted(rows, key=lambda r: (r['date'], r['time'])); x0 = x
    for r in rows:
        k = kind(r['notes']); lab, col, mk = KIND[k]; odd = float(r['level_front']) < 76 and r['notes'].startswith('r27-petg')
        for ax, v in ((a1, float(r['thrust_n'])), (a2, float(r['level_front']))):
            ax.plot(x, v, mk, ms=5.6 if mk == 'D' else 6.2, mfc=SURF if (odd and ax is a2) else col, mec=col if (odd and ax is a2) else SURF, mew=1.1 if (odd and ax is a2) else .9,
                    zorder=3, clip_on=False)
        if odd:
            a2.annotate('unexplained', (x, float(r['level_front'])), xytext=(7, -2), textcoords='offset points', fontsize=6.5, color=MUTED, va='center')
        seen.add(k); x += 1
    x1 = x - 1; mid = (x0 + x1) / 2; w = x1 - x0 + 1
    for ax in (a1, a2):
        ax.axvspan(x0 - .8, x1 + .8, color='#f1f0ec' if i % 2 == 0 else SURF, zorder=0, lw=0)
    tr = a1.get_xaxis_transform()
    a1.text(mid, 1.36, dates, transform=tr, ha='center', va='bottom', fontsize=7.4, color=MUTED)
    a1.text(mid, 1.33, title if w < 14 else title.replace('\n', ' '), transform=tr, ha='center', va='top', fontsize=8.6, fontweight='bold', linespacing=1.15)
    a1.plot([mid - .042 * len(outcome) * 6 - 1.1], [1.065], 'o', ms=4.5, color=STATUS[outcome], transform=tr, clip_on=False)
    a1.text(mid + .5, 1.065, outcome, transform=tr, ha='center', va='center', fontsize=7.6, fontweight='bold')
    a2.text(mid, -.07, '\n'.join(textwrap.wrap(note, max(14, int(w * 1.95)))), transform=a2.get_xaxis_transform(), ha='center', va='top', fontsize=7, color=INK, linespacing=1.2)
    x += GAP

for ax, lab, lim, ticks in ((a1, 'Thrust, N', (0, 11.5), range(0, 12, 2)), (a2, 'Level, dB', (68, 94), range(70, 95, 5))):
    ax.set_facecolor(SURF); ax.set_ylim(*lim); ax.set_yticks(list(ticks)); ax.set_ylabel(lab); ax.set_xlim(-1.2, x - GAP + 1.6)
    ax.grid(axis='y', color=GRID, lw=.7, zorder=1); ax.tick_params(length=0); ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
from matplotlib.lines import Line2D
a1.legend(handles=[Line2D([], [], marker=m, ls='', ms=6, mfc=c, mec=SURF, label=l) for l, c, m in KIND.values()], loc='lower left', bbox_to_anchor=(0, 1.44), ncol=3, frameon=False, fontsize=7.8, handletextpad=.3, columnspacing=1.6, borderaxespad=0)
fig.text(.995, .975, 'One mark per run, in time order within each step', ha='right', va='top', fontsize=7.4, color=MUTED)
fig.savefig(HERE + '/timeline-fig.png', facecolor=SURF)
print({t.split(chr(10))[0]: len(r) for t, _, _, r, _ in STEPS})
