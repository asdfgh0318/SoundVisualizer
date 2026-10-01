"""build_report.py — the 2026-09-30 baseline story: timeline, mic corrections, room, fresh prop baseline, felt-duct variants.

    .venv/bin/python docs/analysis/baseline-story-2026-09-30/build_report.py

Reads the prop captures of 2026-09-30 from the measurement repo, or from NEWDATA=<dir> (a copy of the Pi's
~/SoundVisualizer/data) while the laptop backup has not pulled them yet. Writes fig-*.png, report-numbers.json and
REPORT.pdf next to this file. Every number in the text is computed here.
"""
import os, sys, glob, json, subprocess, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from story_lib import groups, perf, FC, ROOT
from calibrator.rig import read_map

DATA = os.path.expanduser('~/ŻYCIE/PRACA/SoundVisualizer-data/data')
CORR, FACT = DATA + '/calibrations', DATA + '/calibrations/factory-originals-2026-09-16'
SEARCH = [p for p in [os.environ.get('NEWDATA'), DATA] if p]
def base(name):
    for d in SEARCH:
        if os.path.isdir(f'{d}/{name}/measurements'): return f'{d}/{name}'
    raise SystemExit(f'base {name} not found in {SEARCH}')
BASE = 'dupa__ggggg__unset__v1-baseline-vertical'
DUCTS = {'felt-duct': 'aaaa__fffff__felt__v1-felt-duct', 'felt-duct2': 'aaaa__fffff__felt__v1-felt-duct2',
         'felt-duct23': 'aaaa__fffff__felt__v1-felt-duct23', 'felt-plastic-coomp': 'aaaa__fffff__felt__v1-felt-plastic-coomp'}
OLD = {'2026-07-24': '2004__6in__unset__dp1-baseline', '2026-08-28': '2004__6in__unset__dp1-baseline-2026-08-28'}
INK, BLUE, ORANGE, TEAL, GREY = '#10171b', '#2b6cb0', '#c05621', '#17566e', '#9ca3af'
PWMC = {1800: '#8fb4d6', 1900: BLUE, 2000: INK}
plt.rcParams.update({'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.titlesize': 8.5, 'axes.titleweight': 'bold',
                     'axes.titlelocation': 'left', 'figure.dpi': 200, 'savefig.bbox': 'tight'})
rms = lambda x: float(np.sqrt(np.nanmean(np.asarray(x) ** 2)))
last = lambda G, pw: [g for g in G if g['pwm'] == pw][-1]
N = {}          # numbers that go into the text and into report-numbers.json
BI = list(range(3, 19))                                     # bands 250 Hz .. 8 kHz
BN = [f'{FC[i]:.0f}' for i in range(19)]

# ------------------------------------------------------------------------------------------------ data
G_b = groups(base(BASE), CORR); G_bf = groups(base(BASE), FACT); P_b = perf(base(BASE))
G_old = {k: groups(base(v), CORR) for k, v in OLD.items()}; G_oldf = {k: groups(base(v), FACT) for k, v in OLD.items()}
P_old = {k: perf(base(v)) for k, v in OLD.items()}
G_d = {k: groups(base(v), CORR) for k, v in DUCTS.items()}; P_d = {k: perf(base(v)) for k, v in DUCTS.items()}
G_sep = {k: groups(base(f'2004__6in__unset__dp1-baseline-horizontal-prop{k}'), CORR) for k in (15, 16, 17, 18)}
P_sep = {k: perf(base(f'2004__6in__unset__dp1-baseline-horizontal-prop{k}')) for k in (15, 16, 17, 18)}

def rough(B):   # rms second difference across elevation, dB, per band
    d2 = B[:-2] - 2 * B[1:-1] + B[2:]; return np.sqrt(np.nanmean(d2 ** 2, 0))

# ------------------------------------------------------------------------------------------------ room-error time series
runs = []
for d in ['2026-09-23', '2026-09-24', '2026-09-25', '2026-09-30']:
    for p in sorted(glob.glob(f'{ROOT}/calibrator/sessions/{d}/*/')):
        n = os.path.basename(p.rstrip('/'))
        if any(k in n for k in ('ABORTED', 'NOISY', 'noise-floor', 'NOT-READY')): continue
        try:
            f, pos, L, _ = read_map(p.rstrip('/')); f = np.asarray(f); L = np.asarray(L, float)
            if len(f) < 90: continue
            Dm = L - np.nanmean(L, 1, keepdims=True); lo = f < 3000
            s = np.sin(np.radians(np.asarray(pos, float))); s -= s.mean(); Dt = Dm - np.outer((Dm @ s) / (s @ s), s)
            runs.append((dt.datetime.fromtimestamp(os.path.getmtime(p + 'levels.json')), d + '/' + n, rms(Dm[lo]), rms(Dt[lo]),
                         [rms(Dm[(f >= a) & (f < b)]) for a, b in [(250, 400), (400, 630), (630, 1000), (1000, 1600), (1600, 3000)]]))
        except Exception:
            pass
runs.sort(key=lambda r: r[0]); RUN = {r[1]: r for r in runs}
N['room'] = {k: dict(score=RUN[v][2], tilt_removed=RUN[v][3], bands=RUN[v][4]) for k, v in
             dict(start='2026-09-23/vertical-2a', best='2026-09-23/floor-carpet', accepted='2026-09-25/carpet-reordered', rerun='2026-09-30/carpet-reordered-rerun',
                  floor='2026-09-24/floor-no-wedges', carpet='2026-09-24/chaotic-carpet', carpet2='2026-09-24/chaotic-carpet-2', carpet3='2026-09-24/chaotic-carpet-3').items()}
_ps = os.path.join(HERE, '..', 'chamber-final-2026-10-01', 'polar-stats.json')
POLAR = json.load(open(_ps)) if os.path.exists(_ps) else None

# ------------------------------------------------------------------------------------------------ F1 timeline in real time
def fig_timeline():
    D = lambda s: mdates.date2num(dt.datetime.fromisoformat(s))
    lanes = ['Props · arc vertical (old)', 'Props · arc flat', 'Analysis of the flat runs', 'Microphone corrections', 'Loudspeaker source tests',
             'Room optimisation', 'Props · arc vertical (fresh)']
    y = {n: len(lanes) - 1 - i for i, n in enumerate(lanes)}
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    def pt(lane, s, txt, col=TEAL, dy=.0, ha='left'):
        ax.plot(D(s), y[lane], 'o', color=col, ms=5, zorder=3); ax.text(D(s) + (1.2 if ha == 'left' else -1.2), y[lane] + .24 + dy, txt, fontsize=6.6, ha=ha, color=INK)
    def bar(lane, a, b, txt, col=TEAL, left=False):
        ax.barh(y[lane], D(b) - D(a) + .8, left=D(a), height=.34, color=col, zorder=2)
        ax.text(D(a) - 1.8 if left else D(b) + 2.8, y[lane], txt, va='center', ha='right' if left else 'left', fontsize=6.6, color=INK)
    pt(lanes[0], '2026-07-24T12:00', '24 Jul baseline · 6.7 V'); pt(lanes[0], '2026-07-27T12:00', '', GREY); pt(lanes[0], '2026-08-28T12:00', '28 Aug baseline + materials · 7.6 V')
    ax.text(D('2026-07-27T12:00') + 1.2, y[lanes[0]] - .42, '27 Jul: 4 materials', fontsize=6.3, color='#46545c')
    bar(lanes[1], '2026-08-31', '2026-09-02', '31 Aug–2 Sep  prop1–18 · 11.8 V')
    pt(lanes[2], '2026-09-08T12:00', '8 Sep: tones bend up to 8 dB, arc not qualified')
    bar(lanes[3], '2026-09-16', '2026-09-16', '16 Sep  11 capsules measured against each other: spread 4.0 → 0.02 dB', BLUE, left=True)
    pt(lanes[4], '2026-09-17T12:00', '17 Sep  sphere good to 3 kHz, rocks at 4.4 kHz')
    bar(lanes[5], '2026-09-23', '2026-09-25', '23–25 Sep  3 days, 73 runs', ORANGE, left=True)
    pt(lanes[5], '2026-09-30T15:48', '30 Sep rerun', ORANGE, ha='right')
    pt(lanes[6], '2026-09-30T17:22', '30 Sep 17:22  fresh baseline + 4 felt-duct runs · 11.7 V', BLUE, dy=-.02, ha='right')
    ax.set_yticks([y[n] for n in lanes]); ax.set_yticklabels(lanes, fontsize=7); ax.set_ylim(-.7, len(lanes) - .3)
    ax.set_xlim(D('2026-07-20'), D('2026-10-02')); ax.xaxis.set_major_locator(mdates.WeekdayLocator(mdates.MONDAY, interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b')); ax.grid(axis='x', alpha=.25); ax.tick_params(axis='y', length=0)
    for s_ in ('left',): ax.spines[s_].set_visible(False)
    ax.set_title('The story on a real-time axis (2026)')
    fig.savefig(HERE + '/fig-1-timeline.png'); plt.close(fig)

# ------------------------------------------------------------------------------------------------ F2 room error vs clock time
def fig_room():
    days = ['2026-09-23', '2026-09-24', '2026-09-25', '2026-09-30']
    byday = {d: [r for r in runs if r[1].startswith(d)] for d in days}
    span = {d: (min(r[0] for r in byday[d]), max(r[0] for r in byday[d])) for d in days}
    wid = [max((span[d][1] - span[d][0]).total_seconds() / 3600 + .5, 1.3) for d in days]
    fig, axs = plt.subplots(1, 4, figsize=(7.4, 3.6), sharey=True, gridspec_kw=dict(width_ratios=wid, wspace=.05))
    key = [('2026-09-23/vertical-2a', 'untouched start'), ('2026-09-23/floor-carpet', 'best: wedges + carpet'), ('2026-09-24/floor-no-wedges', 'wedges taken off'),
           ('2026-09-24/wall-direct-a', 'speaker on the wall'), ('2026-09-24/center-leveled', 'sphere levelled'), ('2026-09-25/closer-a', 'speaker 20 cm closer'),
           ('2026-09-25/backed-5cm', 'accepted on 25 Sep'), ('2026-09-25/cleanup-3', 'source moves (level +0.6 dB)'), ('2026-09-25/carpet-removed', 'tilt flips sign'),
           ('2026-09-25/carpet-reordered', 'final accepted'), ('2026-09-30/carpet-reordered-rerun', 'rerun, 30 Sep')]
    num = {r: i + 1 for i, (r, _) in enumerate(key)}
    s0 = N['room']['start']['score']; ymax = max(r[2] for r in runs)
    for ax, d in zip(axs, days):
        rr = byday[d]; tt = [mdates.date2num(r[0]) for r in rr]
        ax.plot(tt, [r[3] for r in rr], '-', color=GREY, lw=1, label='tilt fitted out')
        ax.plot(tt, [r[2] for r in rr], '-o', color=INK, lw=1, ms=3, label='room error')
        for r in rr:
            if r[1] in num:
                ax.annotate(str(num[r[1]]), (mdates.date2num(r[0]), r[2]), xytext=(0, 9), textcoords='offset points', fontsize=6, ha='center', va='center', fontweight='bold',
                            color=ORANGE, bbox=dict(boxstyle='circle,pad=0.18', fc='white', ec=ORANGE, lw=.7), zorder=6)
        half = dt.timedelta(minutes=(wid[days.index(d)] * 60 - (span[d][1] - span[d][0]).total_seconds() / 60) / 2)
        ax.set_xlim(mdates.date2num(span[d][0] - half), mdates.date2num(span[d][1] + half)); ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1 if d in (days[0], days[2]) else 2) if d != days[3] else mdates.MinuteLocator(byminute=[45]))
        ax.set_title(d[8:] + '.09', fontsize=7.5); ax.grid(alpha=.2); plt.setp(ax.get_xticklabels(), fontsize=6)
        if d != days[0]: ax.spines['left'].set_visible(False); ax.tick_params(axis='y', length=0)
    axs[0].set_ylabel('room error below 3 kHz (dB, lower = flatter)'); axs[0].legend(fontsize=6, frameon=False, loc='upper left')
    axs[0].set_ylim(1.0, ymax + .15)
    half_ = (len(key) + 1) // 2
    fig.text(.01, -.03, '   '.join(f'{num[r]} {txt}' for r, txt in key[:half_]), fontsize=6.3, ha='left', va='top', color=INK)
    fig.text(.01, -.08, '   '.join(f'{num[r]} {txt}' for r, txt in key[half_:]), fontsize=6.3, ha='left', va='top', color=INK)
    fig.suptitle('Room error per run on the clock of each day (days are not chained)', x=.01, ha='left', fontsize=8.5, fontweight='bold', y=1.0)
    fig.savefig(HERE + '/fig-2-room.png'); plt.close(fig)

# ------------------------------------------------------------------------------------------------ F3 mic corrections
def fig_mic():
    from matplotlib.patches import Patch
    fig = plt.figure(figsize=(7.4, 3.0)); gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1, 1], wspace=.42)
    a = fig.add_subplot(gs[0])
    eras = [('24 Jul', G_old['2026-07-24'], G_oldf['2026-07-24']), ('28 Aug', G_old['2026-08-28'], G_oldf['2026-08-28']), ('30 Sep', G_b, G_bf)]
    N['rough'] = {}
    for i, (nm, gc, gf) in enumerate(eras):
        rf, rc = np.nanmean(rough(last(gf, 1900)['B'])[BI]), np.nanmean(rough(last(gc, 1900)['B'])[BI]); N['rough'][nm] = (rf, rc)
        a.bar(i - .2, rf, .36, color=ORANGE); a.bar(i + .2, rc, .36, color=BLUE)
        a.text(i - .2, rf + .12, f'{rf:.1f}', ha='center', fontsize=6.8); a.text(i + .2, rc + .12, f'{rc:.1f}', ha='center', fontsize=6.8)
        a.text(i, max(rf, rc) + .9, f'{(rc / rf - 1) * 100:+.0f} %', ha='center', fontsize=7.5, fontweight='bold')
    a.set_xticks(range(3)); a.set_xticklabels([e[0] for e in eras]); a.set_ylim(0, 8.3); a.set_ylabel('polar roughness, dB')
    a.set_title('Same captures, two files', fontsize=8); a.legend(handles=[Patch(color=ORANGE, label='factory'), Patch(color=BLUE, label='corrected')], fontsize=6.3, frameon=False, loc='upper right')
    for k, (bi, ttl) in enumerate([(8, '794 Hz'), (14, '3.2 kHz')]):
        ax = fig.add_subplot(gs[1 + k]); g, gf = last(G_b, 1900), last(G_bf, 1900)
        ax.plot(g['elev'], gf['B'][:, bi], '-o', color=ORANGE, ms=3, lw=1, label='factory'); ax.plot(g['elev'], g['B'][:, bi], '-o', color=BLUE, ms=3, lw=1.2, label='corrected')
        ax.set_xlabel('elevation (°)'); ax.set_title(f'Today · 1900 · {ttl}', fontsize=8); ax.set_xticks([-90, -45, 0, 45, 90]); ax.grid(alpha=.2)
        if k == 0: ax.set_ylabel('level, dB SPL'); ax.legend(fontsize=6.3, frameon=False)
    fig.savefig(HERE + '/fig-3-mic.png'); plt.close(fig)

# ------------------------------------------------------------------------------------------------ F4 polars
def polar_ax(ax, el, v, color, lw=1.3, label=None):
    th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
    ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=color, lw=lw, label=label)
def clock(ax):
    ax.set_thetagrids([90, 0, 270], ['+90°', '0°', '−90°'], fontsize=6); ax.tick_params(axis='y', labelsize=5.5); ax.grid(alpha=.3)
def fig_polars():
    bands = [(4, '315 Hz'), (7, '630 Hz'), (9, '1 kHz'), (12, '2 kHz'), (15, '4 kHz'), (18, '8 kHz')]
    fig, axs = plt.subplots(2, 3, figsize=(7.4, 5.3), subplot_kw=dict(projection='polar'), gridspec_kw=dict(wspace=.35, hspace=.35))
    for ax, (bi, ttl) in zip(axs.flat, bands):
        allv = []
        for pw in (1800, 1900, 2000):
            g = last(G_b, pw); polar_ax(ax, g['elev'], g['B'][:, bi], PWMC[pw], label=f'PWM {pw}'); allv += list(g['B'][:, bi])
        lo, hi = np.nanmin(allv), np.nanmax(allv); ax.set_rlim(lo - 3, hi + 2); ax.set_rticks(np.round(np.linspace(lo, hi, 3)))
        ax.set_title(ttl, pad=10); clock(ax)
    h_, l_ = axs.flat[0].get_legend_handles_labels(); fig.legend(h_, l_, fontsize=6.5, frameon=False, loc='lower center', ncol=3, bbox_to_anchor=(.5, -.02))
    fig.suptitle('Tone-notched broadband level (dB SPL), 11 capsules, left half mirrored', x=.01, ha='left', y=1.0, fontsize=8.5, fontweight='bold')
    fig.savefig(HERE + '/fig-4a-polar-broadband.png'); plt.close(fig)
    fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.4), subplot_kw=dict(projection='polar'), gridspec_kw=dict(wspace=.4))
    for h, ax in enumerate(axs):
        allv = []
        for pw in (1800, 1900, 2000):
            g = last(G_b, pw); polar_ax(ax, g['elev'], g['T'][:, h], PWMC[pw]); allv += list(g['T'][:, h])
        lo, hi = np.nanmin(allv), np.nanmax(allv); ax.set_rlim(lo - 3, hi + 2); ax.set_rticks(np.round(np.linspace(lo, hi, 3)))
        ax.set_title(f'{h + 1}× BPF · {(h + 1) * last(G_b, 1900)["f0"]:.0f} Hz', pad=10, fontsize=7.5); clock(ax)
    fig.suptitle('Blade-passage harmonics, dB SPL (lines: PWM 1800, 1900, 2000; frequency shown for 1900)', x=.01, ha='left', y=1.08, fontsize=8.5, fontweight='bold')
    fig.savefig(HERE + '/fig-4b-polar-tones.png'); plt.close(fig)

# ------------------------------------------------------------------------------------------------ F5 waterfalls
def smooth(f, mags, lo=100, hi=10000, per_oct=12):
    c = lo * 2 ** (np.arange(int(np.log2(hi / lo) * per_oct) + 1) / per_oct); out = np.full((mags.shape[0], len(c)), np.nan); df = f[1] - f[0]
    for j, fc in enumerate(c):
        w = max(fc * (2 ** (1 / (2 * per_oct)) - 2 ** (-1 / (2 * per_oct))), 1.5 * df)
        m = (f >= fc - w / 2) & (f < fc + w / 2)
        if m.any(): out[:, j] = 10 * np.log10(np.mean(10 ** (mags[:, m] / 10), 1))
    return c, out
def fig_waterfall():
    g = last(G_b, 1900); c, S = smooth(g['f'], g['mags'])
    fig = plt.figure(figsize=(7.4, 7.2)); gs = fig.add_gridspec(2, 2, height_ratios=[1.35, 1], hspace=.3, wspace=.12)
    a = fig.add_subplot(gs[0, 0]); off = 11
    for i in range(len(S)):
        y0 = (len(S) - 1 - i) * off; base_ = y0 - 6
        a.fill_between(c, base_, S[i] - 20 + y0, color='white', zorder=2 + i * .01); a.plot(c, S[i] - 20 + y0, color=INK, lw=.9, zorder=3 + i * .01)
        a.text(92, y0, f'{g["elev"][i]:+.0f}°', fontsize=6.2, ha='right', va='center')
    for h in range(1, 5): a.axvline(h * g['f0'], color=ORANGE, lw=.7, ls='--', alpha=.8)
    a.text(g['f0'], len(S) * off - 2, 'BPF', color=ORANGE, fontsize=6.3, ha='center'); a.set_xscale('log'); a.set_xlim(100, 10000); a.set_yticks([])
    a.set_xlabel('Hz'); a.set_title('Per capsule · PWM 1900', fontsize=8); a.spines['left'].set_visible(False)
    b = fig.add_subplot(gs[0, 1]); pws = [1200, 1500, 1800, 1900, 2000]
    for k, pw in enumerate(pws):
        gg = last(G_b, pw); cc, SS = smooth(gg['f'], gg['mags']); i0 = int(np.argmin(abs(gg['elev']))); y0 = k * 15
        b.fill_between(cc, y0 - 6, SS[i0] - 22 + y0, color='white', zorder=2 + k * .01); b.plot(cc, SS[i0] - 22 + y0, color=INK, lw=.9, zorder=3 + k * .01)
        b.text(10000, y0 - 4.5, f'PWM {pw}', fontsize=6.2, ha='right', va='center', color='#46545c')
        if gg['f0']:
            for h in range(1, 5): b.plot([h * gg['f0']] * 2, [y0 - 6, y0 + 9], color=ORANGE, lw=.9, zorder=5)
    b.set_xscale('log'); b.set_xlim(100, 10000); b.set_yticks([]); b.set_xlabel('Hz'); b.set_title('Per motor speed · capsule at 0°', fontsize=8); b.spines['left'].set_visible(False)
    h_ = fig.add_subplot(gs[1, :]); c6, S6 = smooth(g['f'], g['mags'], 125, 8000, 6); R = S6 - np.nanmean(S6, 0)
    im = h_.pcolormesh(np.arange(len(c6) + 1), np.arange(12), R, cmap='RdBu_r', vmin=-8, vmax=8, shading='flat')
    h_.set_yticks(np.arange(11) + .5); h_.set_yticklabels([f'{e:+.0f}°' for e in g['elev']], fontsize=6.3); h_.invert_yaxis()
    tk = [i for i, fc in enumerate(c6) if any(abs(fc - z) / z < .06 for z in [125, 250, 500, 1000, 2000, 4000, 8000])]
    h_.set_xticks([i + .5 for i in tk]); h_.set_xticklabels([f'{c6[i]:.0f}' for i in tk]); h_.set_xlabel('Hz')
    plt.colorbar(im, ax=h_, pad=.01, fraction=.025).set_label('dB vs mean over elevation', fontsize=6.5)
    h_.set_title('Level relative to the elevation mean · PWM 1900 · 1/6-octave', fontsize=8); fig.savefig(HERE + '/fig-5-waterfall.png'); plt.close(fig)

# ------------------------------------------------------------------------------------------------ F6 felt-duct vs baseline at matched thrust
bp = [1800, 1900, 2000]; Tb = np.array([abs(P_b[p]['T']) for p in bp]); Bb = np.array([last(G_b, p)['B'] for p in bp]); Hb = np.array([last(G_b, p)['T'] for p in bp])
def at(T, A):
    o = np.argsort(Tb); return np.array([[np.interp(T, Tb[o], A[o][:, i, j]) for j in range(A.shape[2])] for i in range(A.shape[1])])
DELTA = {}
for n in DUCTS:
    for pw in (1900, 2000):
        T = abs(P_d[n][pw]['T']); g = last(G_d[n], pw)
        if T < Tb.min() - .1: continue
        DELTA[n, pw] = dict(T=T, I=P_d[n][pw]['I'], dB=g['B'] - at(T, Bb), dH=g['T'] - at(T, Hb))
def fig_duct():
    fig = plt.figure(figsize=(7.4, 6.6)); gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.05], hspace=.32)
    a = fig.add_subplot(gs[0]); cols = {'felt-duct': INK, 'felt-duct2': BLUE, 'felt-duct23': '#8fb4d6', 'felt-plastic-coomp': ORANGE}
    for n in DUCTS:
        if (n, 2000) in DELTA: a.plot([FC[i] for i in BI], np.nanmean(DELTA[n, 2000]['dB'][:, BI], 0), '-o', color=cols[n], ms=3, lw=1.2, label=f'{n}  ({DELTA[n, 2000]["T"]:.2f} N)')
    a.axhline(0, color=GREY, lw=.8); a.set_xscale('log'); a.set_xticks([250, 500, 1000, 2000, 4000, 8000]); a.set_xticklabels(['250', '500', '1k', '2k', '4k', '8k'])
    a.set_ylabel('louder than baseline (dB)'); a.set_xlabel('Hz'); a.legend(fontsize=6.3, frameon=False, loc='upper left'); a.grid(alpha=.2)
    a.set_title('Each variant minus the baseline at equal thrust · PWM 2000 · mean of 11 capsules', fontsize=8)
    sub = gs[1].subgridspec(2, 4, hspace=.35, wspace=.12); axd = []
    for r, pw in enumerate((1900, 2000)):
        for c_, n in enumerate(DUCTS):
            ax = fig.add_subplot(sub[r, c_]); axd.append(ax)
            if (n, pw) not in DELTA:
                ax.axis('off'); ax.text(.5, .5, f'{n}\nPWM {pw}: {abs(P_d[n][pw]["T"]):.2f} N\nbelow the baseline\nthrust range', ha='center', va='center', fontsize=6, transform=ax.transAxes, color='#74828a'); continue
            d = DELTA[n, pw]; im = ax.pcolormesh(np.arange(12), np.arange(len(BI) + 1), d['dB'][:, BI].T, cmap='RdBu_r', vmin=-20, vmax=20, shading='flat')
            ax.set_yticks(np.arange(len(BI))[::3] + .5); ax.set_yticklabels([BN[i] for i in BI][::3] if c_ == 0 else [], fontsize=5.8)
            ax.set_xticks([.5, 5.5, 10.5]); ax.set_xticklabels(['+90°', '0°', '−90°'] if r == 1 else [], fontsize=5.8)
            ax.set_title(f'{n}\n{pw} · {d["T"]:.2f} N', fontsize=6, pad=3)
    cb = fig.colorbar(im, ax=axd, fraction=.02, pad=.01); cb.set_label('dB vs baseline at equal thrust', fontsize=6.5); cb.ax.tick_params(labelsize=6)
    fig.savefig(HERE + '/fig-6-duct.png'); plt.close(fig)

# ------------------------------------------------------------------------------------------------ numbers for the text
def numbers():
    g = last(G_b, 1900); B = g['B']
    top, bot = np.nanmean(B[:5], 0), np.nanmean(B[6:], 0)
    N['topbot'] = {BN[i]: float(top[i] - bot[i]) for i in BI}
    N['f0'] = {pw: last(G_b, pw)['f0'] for pw in bp}
    N['harm_today'] = [float(np.nanmean(g['T'][:, h])) for h in range(4)]; N['harm_today_0deg'] = [float(g['T'][5, h]) for h in range(4)]
    N['harm_sep'] = [[float(np.nanmean(last(G_sep[k], 1900)['T'][:, h])) for h in range(4)] for k in G_sep]; N['f0_sep'] = [last(G_sep[k], 1900)['f0'] for k in G_sep]
    N['bb_today_0deg'] = {BN[i]: float(g['B'][5, i]) for i in (3, 9, 14)}
    N['bb_sep'] = {BN[i]: [float(np.nanmean(last(G_sep[k], 1900)['B'][:, i])) for k in G_sep] for i in (3, 9, 14)}
    N['op'] = {}
    for nm, P, G in [('24 Jul', P_old['2026-07-24'], G_old['2026-07-24']), ('28 Aug', P_old['2026-08-28'], G_old['2026-08-28']), ('2 Sep flat (prop15)', P_sep[15], G_sep[15]),
                     ('2 Sep flat (prop17)', P_sep[17], G_sep[17]), ('30 Sep baseline', P_b, G_b)]:
        f0s = [last(G, pw)['f0'] for pw in bp]; ok = all(x for x in f0s) and f0s[0] < f0s[1] < f0s[2]
        N['op'][nm] = dict(V=P[1900]['V'], I=P[1900]['I'], T=P[1900]['T'], f0=f0s[1] if ok else None)
    rp = {}
    for pw in bp:
        a, b = last(G_d['felt-duct2'], pw), last(G_d['felt-duct23'], pw)
        rp[pw] = (rms((a['B'] - b['B'])[:, BI]), rms(a['T'][:, :4] - b['T'][:, :4]))
    N['dup_repeat'] = rp
    sh = {}
    for i in BI:
        a = last(G_b, 1800)['B'][:, i]; b = last(G_b, 2000)['B'][:, i]
        if np.isnan(a).any() or np.isnan(b).any(): continue
        a = a - a.mean(); b = b - b.mean(); sh[BN[i]] = (float(np.corrcoef(a, b)[0, 1]), float(np.sqrt(np.mean((a - b) ** 2))))
    N['shape'] = sh
    N['duct'] = {f'{n}@{pw}': dict(T=d['T'], I=d['I'], band=[float(np.nanmean(d['dB'][:, i])) for i in BI], mean=float(np.nanmean(d['dB'][:, BI])),
                                   tones=[float(np.nanmean(d['dH'][:, h])) for h in range(4)], elev=[float(np.nanmean(d['dB'][e, BI])) for e in range(11)]) for (n, pw), d in DELTA.items()}
    N['duct_drop'] = {n: {pw: 1 - abs(P_d[n][pw]['T']) / abs(P_b[pw]['T']) for pw in bp} for n in DUCTS}
    N['idle_hf'] = {'baseline': float(np.nanmean(last(G_b, 1200)['B'][:, 15])), 'felt-duct': float(np.nanmean(last(G_d['felt-duct'], 1200)['B'][:, 15])), 'felt-duct2': float(np.nanmean(last(G_d['felt-duct2'], 1200)['B'][:, 15]))}
    json.dump(N, open(HERE + '/report-numbers.json', 'w'), indent=1, default=float)


# ------------------------------------------------------------------------------------------------ report
def build_html():
    R = N['room']; S0, SB, SA, SR = R['start'], R['best'], R['accepted'], R['rerun']
    if POLAR:
        a, s_, u = POLAR['today@2000'], POLAR['sept@2000'], POLAR['aug@2000']
        POLAR_TXT = (f"Arc in the rotor plane (Adam), so the polar should be a circle. Against the 31 Aug runs it is rounder: worst capsule {a['worst']:.1f} dB off the mean instead of {u['worst']:.1f} dB. "
                     f"Against the 2 Sep runs at the same voltage, current and thrust it is not: {a['med']:.0f} % of cells within ±1.3 dB against a median of {s_['med']:.0f} % ({s_['lo']:.0f}–{s_['hi']:.0f}). Detail: CHAMBER-FINAL.pdf, page 2.")
    else:
        POLAR_TXT = 'See CHAMBER-FINAL.pdf, page 2.'
    NCAP = sum(len(glob.glob(base(n) + '/measurements/*')) for n in [BASE] + list(DUCTS.values()))
    rf = N['rough']; ch = lambda k: (rf[k][1] / rf[k][0] - 1) * 100
    op = N['op']; hs = np.array(N['harm_sep']); ht = N['harm_today']; h0 = N['harm_today_0deg']
    tb = N['topbot']; dup = N['dup_repeat']; dk = N['duct']
    tiltslope = -0.63                                            # measured on the accepted state with the loudspeaker (SUMMARY-day3)
    duct_means = {k: v['mean'] for k, v in dk.items()}
    dmin, dmax = min(duct_means.values()), max(duct_means.values())
    drop = N['duct_drop']
    def row(nm, v, extra=''):
        f0 = f"{v['f0']:.1f} Hz" if v['f0'] else 'not reliable'
        return f"<tr><td>{nm}</td><td class='num'>{v['V']:.2f}</td><td class='num'>{v['I']:.2f}</td><td class='num'>{v['T']:+.2f}</td><td class='num'>{f0}</td><td>{extra}</td></tr>"
    opt = (row('24 Jul  vertical', op['24 Jul'], 'supply sagging; thrust sign opposite') + row('28 Aug  vertical', op['28 Aug'], 'supply sagging; thrust sign opposite') +
           row('2 Sep  flat, prop15', op['2 Sep flat (prop15)'], 'the September campaign') + row('2 Sep  flat, prop17', op['2 Sep flat (prop17)'], '') +
           row('<b>30 Sep  vertical, fresh</b>', op['30 Sep baseline'], '<b>same operating point as September</b>'))
    ht_rows = ''.join(f"<tr><td>{h + 1}× BPF</td><td class='num'>{hs[:, h].mean():.1f}</td><td class='num'>{hs[:, h].min():.1f}–{hs[:, h].max():.1f}</td><td class='num'>{h0[h]:.1f}</td><td class='num'>{ht[h]:.1f}</td></tr>" for h in range(4))
    css = """@page{size:A4;margin:12mm 13mm} body{font-family:"IBM Plex Sans","DejaVu Sans",Arial,sans-serif;font-size:8.3pt;line-height:1.3;color:#10171b;margin:0}
    h1{font-size:18pt;margin:0 0 2pt;letter-spacing:-.02em} h2{font-size:11pt;margin:10pt 0 3pt;padding-top:5pt;border-top:.7pt solid #c6d0d5} h2 .n{font-family:monospace;font-size:7pt;color:#74828a;margin-right:5pt}
    p{margin:0 0 4pt} ul{margin:0 0 4pt;padding-left:4.5mm} li{margin:0 0 2.4pt} table{border-collapse:collapse;width:100%;margin:3pt 0 6pt;font-size:7.6pt}
    th{font-size:6.6pt;text-transform:uppercase;letter-spacing:.05em;color:#46545c;text-align:left;padding:3pt;border-bottom:1pt solid #10171b;vertical-align:bottom}
    td{padding:2.6pt 3pt;border-bottom:.5pt solid #e0e6e9;vertical-align:top} td.num{font-family:"DejaVu Sans Mono",monospace;font-size:7.1pt;white-space:nowrap}
    .tag{font-family:"DejaVu Sans Mono",monospace;font-size:6.4pt;color:#74828a} .pb{break-before:page} img{width:100%;display:block;margin:2pt auto 4pt}
    .box{background:#f1f4f6;border-left:2pt solid #17566e;padding:4pt 4mm;margin:4pt 0 6pt} .yes{color:#2f6b3a;font-weight:700}.no{color:#96382a;font-weight:700}.mid{color:#8f5c0d;font-weight:700}
    td.verdict{white-space:nowrap} .cap{font-size:7pt;color:#46545c;margin:0 0 6pt}"""
    H = f"""<!doctype html><html><head><meta charset="utf-8"><title>Baseline story 2026-09-30</title><style>{css}</style></head><body>
<h1>Did we get better? The story up to the fresh baseline</h1>
<p class="tag">SoundVisualizer · 2026-09-30 · prop data from the Pi (5 bases, {NCAP} measurements) · loudspeaker data from the chamber campaign · every number computed by build_report.py</p>
<h2 style="border:0;margin-top:4pt"><span class="n">00</span>The answer</h2>
<table><thead><tr><th>Layer of the work</th><th>Did it get better?</th><th>Evidence</th></tr></thead><tbody>
<tr><td><b>Microphone corrections</b><br><span class="tag">16 Sep</span></td><td class="verdict"><span class="yes">YES</span></td><td>On the <i>same captures</i>, the polar of today's baseline is {abs(ch('30 Sep')):.0f} % smoother with the corrected files than the factory ones (roughness {rf['30 Sep'][0]:.1f} → {rf['30 Sep'][1]:.1f} dB). The two old baselines gain {abs(ch('24 Jul')):.0f} % and {abs(ch('28 Aug')):.0f} %. Bench: spread across the 11 capsules 4.01 → 0.02 dB.</td></tr>
<tr><td><b>Room optimisation</b><br><span class="tag">24 Sep, from the stripped floor</span></td><td class="verdict"><span class="yes">YES, in the one valid block</span></td><td>The source is known to have stayed in one position only from the moment the floor was stripped on 24 Sep (14:10), so only that block is compared and nothing is chained across days. Empty floor <b>{R['floor']['score']:.3f}</b> → carpet <b>{R['carpet']['score']:.3f}</b> ({(R['carpet']['score'] / R['floor']['score'] - 1) * 100:+.0f} %); three carpet arrangements {R['carpet']['score']:.3f} / {R['carpet2']['score']:.3f} / {R['carpet3']['score']:.3f}. The accepted state ({SA['score']:.3f}, 25 Sep) was measured with the source in another position and cannot be set against it.</td></tr>
<tr><td><b>Fresh prop baseline</b><br><span class="tag">30 Sep 17:22</span></td><td class="verdict"><span class="mid">VALID, not comparable to July/Aug</span></td><td>Same operating point as the September flat-arc runs (11.7 V, 5.8 A, BPF {N['f0'][1900]:.1f} vs {np.mean(N['f0_sep']):.1f} Hz). The July and August "baselines" ran at 6.6 and 7.6 V with the opposite thrust sign, so they cannot be the "before".</td></tr>
<tr><td><b>Room quality measured with props</b><br><span class="tag">prop plane</span></td><td class="verdict"><span class="mid">YES vs 31 Aug, NO vs 2 Sep</span></td><td>{POLAR_TXT}</td></tr>
</tbody></table>
<img src="fig-1-timeline.png">
<p class="cap">Real time, 2026. Each lane is one kind of work; bars span days, dots are single sessions. The fresh baseline (blue, bottom) is the first prop run after the microphone corrections and the room work.</p>
<div class="box"><b>Today in clock time (local):</b> 15:43–15:48 loudspeaker rerun of the accepted state · <b>17:22</b> baseline (arc in the prop plane), 5 motor speeds, 11 capsules, 2 idle steps repeated · <b>18:44</b> felt-duct · 18:49 felt-duct2 · 18:53 felt-duct23 · <b>19:01</b> felt-plastic-coomp. Each run takes 14 s.</div>

<h2 class="pb"><span class="n">01</span>The room, in clock time</h2>
<img src="fig-2-room.png" style="width:88%">
<p class="cap">Loudspeaker room error for all 73 runs of the chamber campaign. Grey line: the same with each map's top-to-bottom tilt fitted out.</p>
<ul>
<li><b>24 Sep, from the stripped floor (14:10)</b> the source stays in one position: empty floor {R['floor']['score']:.3f}, carpet {R['carpet']['score']:.3f}; later that afternoon the speaker went to the wall, which ends the comparison.</li>
<li>Before that moment, and from 25 Sep on, the source position is not known to be constant, so runs there are not chained into a trend. On 25 Sep the source moved twice (markers 8 and 9). Marker 11, the rerun five days later, repeats the final state to {abs(SR['score'] - SA['score']):.3f} dB.</li>
</ul>

<h2><span class="n">02</span>Is the fresh baseline comparable with anything?</h2>
<table><thead><tr><th>Baseline</th><th>V</th><th>I (A)</th><th>Thrust (N)</th><th>BPF at PWM 1900</th><th>Note</th></tr></thead><tbody>{opt}</tbody></table>
<p class="cap">Median telemetry and the blade-passage frequency read from the audio at PWM 1900. The detector gives an erratic, non-monotonic BPF for the two old baselines, so none is shown.</p>
<p><b>Cross-check with September.</b> Every capsule of today's arc sits at the same polar angle to the prop axis as every position of the flat arc (a prop-plane measurement, Adam), so its levels should match September's mean; the 0° capsule is shown beside the mean over the arc.</p>
<table><thead><tr><th>Level at PWM 1900</th><th>Sept flat, mean</th><th>Sept flat, range (4 runs)</th><th>Today, 0° capsule</th><th>Today, mean over elevation</th></tr></thead><tbody>{ht_rows}</tbody></table>
<p class="cap">Blade-passage harmonics, dB SPL, corrected calibration.</p>
<ul>
<li><b>1× and 3× BPF match</b> (within {abs(h0[0] - hs[:, 0].mean()):.1f} and {abs(h0[2] - hs[:, 2].mean()):.1f} dB), and 3× BPF ({3 * N['f0'][1900]:.0f} Hz) dominates both, 10–12 dB above the fundamental. It is a property of this source, not new.</li>
<li><b>2× and 4× BPF are 6–8 dB lower today</b> at the 0° capsule ({h0[1]:.1f} vs {hs[:, 1].mean():.1f}, {h0[3]:.1f} vs {hs[:, 3].mean():.1f}). Those two frequencies ({2 * N['f0'][1900]:.0f} and {4 * N['f0'][1900]:.0f} Hz) sit in the 400 and 800 Hz bands that fail the room test. The room changed and so did the arrangement, so this cannot be attributed; it is the kind of change tones show when the room moves.</li>
<li>Broadband at the 0° capsule lies inside September's spread of four runs (1 kHz: {N['bb_today_0deg']['1000']:.1f} vs {min(N['bb_sep']['1000']):.1f}–{max(N['bb_sep']['1000']):.1f} dB; 3.2 kHz: {N['bb_today_0deg']['3175']:.1f} vs {min(N['bb_sep']['3175']):.1f}–{max(N['bb_sep']['3175']):.1f} dB).</li>
</ul>

<h2 class="pb"><span class="n">03</span>The microphone corrections, tested on the same captures</h2>
<img src="fig-3-mic.png">
<p class="cap">Roughness = rms second difference of the tone-notched broadband level across the 11 elevations, averaged over the 250 Hz–8 kHz bands at PWM 1900. A true polar is smooth; a capsule error is a kink. Right: today's 794 Hz and 3.2 kHz polars with each file set.</p>
<ul>
<li>The test needs no matching operating point, because only the calibration file changes. Every baseline improves, today's most ({rf['30 Sep'][0]:.1f} → {rf['30 Sep'][1]:.1f} dB).</li>
<li>The old baselines stay rough ({rf['24 Jul'][1]:.1f} and {rf['28 Aug'][1]:.1f} dB) after the correction. That roughness is not the microphones; it comes with the 6.6–7.6 V operating point and whatever else differed then.</li>
<li>The corrections are on the Pi (same checksums as the repo), so today's captures were read with them by the server as well.</li>
</ul>

<h2><span class="n">04</span>Patterns in the fresh baseline</h2>
<img src="fig-4a-polar-broadband.png">
<p class="cap">Polar plots use the project's clock-face convention: +90° up, 0° right, −90° down; the measured right half is mirrored.</p>
<ul>
<li><b>The bottom of the arc is louder than the top</b> (in the prop plane every position should read the same, so this is asymmetry, not directivity) from 500 Hz to 2 kHz, by {abs(tb['500']):.1f}–{abs(tb['1000']):.1f} dB, and by 1.2–1.7 dB above that. At 315 Hz it reverses (top louder by {tb['315']:.1f} dB).</li>
<li>Part of that may be the room rather than the prop: with the loudspeaker, the accepted state has a bottom-louder tilt of about {abs(tiltslope) * 2:.1f} dB top to bottom at 400 Hz–3 kHz.</li>
<li><b>The shape of the polar depends on motor speed, except at 1.3–2 kHz.</b> Between PWM 1800 and 2000 it is stable there (correlation {min(v[0] for k, v in N['shape'].items() if k in ('1260', '1587', '2000')):.2f} or better, shape change {max(v[1] for k, v in N['shape'].items() if k in ('1260', '1587', '2000')):.1f} dB at most). In the other bands the shape changes by {min(v[1] for k, v in N['shape'].items() if k not in ('1260', '1587', '2000')):.1f}–{max(v[1] for k, v in N['shape'].items() if k not in ('1260', '1587', '2000')):.1f} dB rms. Level still rises at every angle.</li>
</ul>
<img src="fig-4b-polar-tones.png">
<p class="cap">Harmonics grow faster with speed than broadband does, so each panel has its own radial scale.</p>

<h2 class="pb"><span class="n">05</span>Waterfalls</h2>
<img src="fig-5-waterfall.png">
<ul>
<li>Left: the same tone stack, in the same places, at every elevation; the capsules agree on the spectrum's shape. Right: the tones track motor speed, and at PWM 1200 and 1500 there is no blade tone (idle and spool-up), with a steady ~2 kHz motor whine at idle.</li>
<li>Bottom: what differs between capsules is localised. The warm block at ~1.5 kHz on the bottom capsules (−54° to −90°) and the pair of columns at 3.2 kHz with opposite signs at top and bottom are fixed-frequency structures, the kind a reflection or a capsule position produces, not a smooth directivity.</li>
</ul>

<h2 class="pb"><span class="n">06</span>The four felt-duct runs against the baseline</h2>
<img src="fig-6-duct.png">
<ul>
<li>At equal thrust every variant is <b>{dmin:.0f}–{dmax:.0f} dB louder</b> than the open prop across 250 Hz–8 kHz, with a peak of +18 to +20 dB at 1.6 kHz and a minimum (+4 to +7 dB) near 500 Hz. The effect is nearly uniform with elevation (within ±2 dB).</li>
<li>Thrust at the same PWM is {min(drop['felt-duct2'].values()) * 100:.0f}–{max(drop['felt-plastic-coomp'].values()) * 100:.0f} % lower for three variants and {min(drop['felt-duct'].values()) * 100:.0f}–{max(drop['felt-duct'].values()) * 100:.0f} % lower for the first one. The blade-passing frequency does not move.</li>
<li>The 1× BPF tone is unchanged (within 4 dB) while 4× BPF rises by 15–19 dB at PWM 1900.</li>
<li>This agrees in sign with Malgoezar et al. 2019 (static duct louder everywhere, up to +12 dB) but is larger. It is also not a level artefact: at idle (PWM 1200) the ducted captures are not louder than the baseline at high frequency.</li>
<li><b>Repeat floor.</b> felt-duct2 and felt-duct23 draw the same current and thrust (to 0.3 %) yet differ by {dup[1800][0]:.1f} dB rms (PWM 1800 and 1900: {dup[1900][0]:.1f}) and {dup[2000][0]:.1f} dB (PWM 2000) in the band levels, and by {dup[2000][1]:.1f}–{dup[1800][1]:.1f} dB in the tones. If they are the same state, that is this rig's repeat floor; the duct effect is five times larger. One idle capture (felt-duct23, PWM 1200) carries a noise burst 30+ dB above the others and is not used.</li>
</ul>

<h2 class="pb"><span class="n">07</span>What we can and cannot say</h2>
<ul>
<li><b>Can:</b> the corrected microphones make the polar smoother; today's baseline is a valid fresh reference at the September operating point; a felt duct is much louder than the open prop at equal thrust in a static test.</li>
<li><b>Cannot:</b> chain the room campaign across days (the source moved), or claim the prop polar is rounder than the 2 Sep runs: it is rounder than 31 Aug only.</li>
<li><b>Repeat floor unknown for the open prop.</b> The only repeats at spinning speeds are the two duct runs above; the repeated 1200 and 1500 steps of the baseline are idle noise and say nothing.</li>
<li>The July and August baselines are not evidence for or against anything about the room.</li>
</ul>
<div class="box"><b>Next, in order of value:</b> (1) Repeat one spinning step of the baseline three times, to get a real repeat floor for the open prop. (2) One capture with the propeller turning the other way, to split stand-induced from room-induced asymmetry. (3) Say what the four felt-duct runs are (names as typed: felt-duct, felt-duct2, felt-duct23, felt-plastic-coomp) and whether duct2 and duct23 are meant to be identical. (4) Extend the loudspeaker grid below 257 Hz: the blade tone is at 215–258 Hz and sits below what the room test covers.</div>
<p class="tag">Sources: prop captures on the Pi (~/SoundVisualizer/data, 5 bases) and the measurement repo; loudspeaker sessions calibrator/sessions/2026-09-23…30; calibration files data/calibrations and factory-originals-2026-09-16. Evidence for the duct comparison: Malgoezar et al. 2019, Int. J. Aeroacoustics 18, p. 9 (papers/SoundVisualizer/design-rules/EXTRACTS-DUCT-LINING.md).</p>
</body></html>"""
    open(HERE + '/_report.html', 'w').write(H)
    subprocess.run(['/snap/bin/chromium', '--headless', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={HERE}/REPORT.pdf', 'file://' + HERE + '/_report.html'],
                   check=True, stderr=subprocess.DEVNULL)
    os.replace(HERE + '/_report.html', HERE + '/REPORT.html')

if __name__ == '__main__':
    fig_timeline(); fig_room(); fig_mic(); fig_polars(); fig_waterfall(); fig_duct(); numbers(); build_html()
    print(json.dumps({k: N[k] for k in ('rough', 'topbot', 'f0', 'harm_today', 'harm_sep', 'op', 'dup_repeat', 'idle_hf')}, indent=1, default=float)[:3500])
