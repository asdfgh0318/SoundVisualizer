"""build_final.py — 2-page chamber report: waterfall comparison (same day, same source) + evaluation against the ISO anechoic tolerance values.

    .venv/bin/python docs/analysis/chamber-final-2026-10-01/build_final.py

Only runs from one day with the source not moved are compared (Adam's rule: results of different days are not compared). Page 1 and the page-2 table: 2026-09-25/day3-a (worst of day 3) vs carpet-reordered (final), same day but the source was moved in between and the page says so. The clean unmoved-source pair is cited in the page-2 caveat:
  FLOOR  = 2026-09-24/floor-no-wedges   the empty floor, wedges off (14:10)
  CARPET = 2026-09-24/chaotic-carpet    carpet laid on that floor (14:37); chaotic-carpet-2 (14:48) is its repeat
The accepted configuration (2026-09-25/carpet-reordered) is evaluated on its own, never against another day.
The script prints the source check (level shift, tilt change) that justifies the pair. Every number in the report is computed here.
"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..')); sys.path.insert(0, ROOT)
import numpy as np
from calibrator.rig import read_map
S = ROOT + '/calibrator/sessions/'
sys.path.insert(0, ROOT + '/docs/analysis/baseline-story-2026-09-30')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from story_lib import groups
DATA = os.path.expanduser('~/ŻYCIE/PRACA/SoundVisualizer-data/data'); CORR = DATA + '/calibrations'
TODAY = 'dupa__ggggg__unset__v1-baseline-vertical'
def base(name):                       # NEWDATA=<copy of the Pi's data> while the laptop backup has not pulled 30 Sep
    for d in [os.environ.get('NEWDATA'), DATA]:
        if d and os.path.isdir(f'{d}/{name}/measurements'): return f'{d}/{name}'
    raise SystemExit('base not found: ' + name)
FLOOR, CARPET, CARPET2, FINAL = '2026-09-24/floor-no-wedges', '2026-09-24/chaotic-carpet', '2026-09-24/chaotic-carpet-2', '2026-09-25/carpet-reordered'
STEP = ROOT + '/docs/analysis/chamber-treatments-2026-09-23/build_step_figure.py'
TOB = [250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500]
tol = lambda fc: 1.5 if fc <= 630 else 1.0                       # ISO 3745 anechoic table
rms = lambda x: float(np.sqrt(np.nanmean(np.asarray(x) ** 2)))
sel = lambda f, fc: (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))

def load(run):
    f, pos, L, _ = read_map(S + run); f = np.asarray(f); L = np.asarray(L, float)
    o = np.argsort(pos)[::-1]; return f, L[:, o], np.asarray(pos, float)[o]
def stats(run):
    f, L, pos = load(run); D = L - np.nanmean(L, 1, keepdims=True); lo = f < 3000
    bm = {fc: float(np.nanmax(abs(np.nanmean(D[sel(f, fc)], 0)))) for fc in TOB}
    tr = {fc: float(100 * np.mean(abs(D[sel(f, fc)]) <= tol(fc))) for fc in TOB}
    cells = np.concatenate([abs(D[sel(f, fc)]).ravel() <= tol(fc) for fc in TOB])
    s = np.sin(np.radians(pos)); s = s - s.mean(); m = (f >= 400) & (f < 3000)
    return dict(f=f, D=D, L=L, score=rms(D[lo]), bm=bm, tr=tr, tone_all=float(100 * cells.mean()), ntones={fc: int(sel(f, fc).sum()) for fc in TOB},
                level=float(L[lo].mean()), tilt=float(np.mean((D[m] @ s) / (s @ s))), bands=[rms(D[(f >= a) & (f < b)]) for a, b in [(250, 400), (400, 630), (630, 1000), (1000, 1600), (1600, 3000)]])
CARPET3 = '2026-09-24/chaotic-carpet-3'
DAY3A = '2026-09-25/day3-a'
F, C, C2, C3, X, G = stats(FLOOR), stats(CARPET), stats(CARPET2), stats(CARPET3), stats(FINAL), stats(DAY3A)
REPEATS = [('2026-09-23/vertical-2a', '2026-09-23/vertical-2b'), ('2026-09-24/wall-mount-a', '2026-09-24/wall-mount-b'), ('2026-09-24/wall-direct-a', '2026-09-24/wall-direct-b'),
           ('2026-09-24/center-new-a', '2026-09-24/center-new-b'), ('2026-09-25/closer-a', '2026-09-25/closer-b')]       # same state measured twice, same day
_r = [(stats(a), stats(b)) for a, b in REPEATS]
MARG = round(max(abs(x['bm'][fc] - y['bm'][fc]) for x, y in _r for fc in TOB) + .005, 2)     # largest same-day repeat difference of the band statistic
def verdict(st, fc):
    v = st['bm'][fc]; return 'marg' if abs(v - tol(fc)) <= MARG else ('pass' if v < tol(fc) else 'fail')
def cutoff(st):
    lo = None
    for fc in sorted(TOB, reverse=True):
        if verdict(st, fc) == 'fail': break
        lo = fc
    return lo
lst = lambda st, k: ', '.join(str(fc) for fc in TOB if verdict(st, fc) == k) or '—'
count = lambda st, k: sum(verdict(st, fc) == k for fc in TOB)


# ---- prop-plane roundness: the same statistic for today and for every earlier flat-arc run
SEPT = [f'2004__6in__unset__dp1-baseline-horizontal-prop{k}' for k in range(8, 18)]          # 1-2 Sep (prop8-10 on 1 Sep 16:44-16:55, prop11-17 on 2 Sep), arc flat, 11.65 V / 7.3 A / -4.0 N, the operating point of 30 Sep
AUG = [f'2004__6in__unset__dp1-baseline-horizontal-{k}' for k in ('2026-08-31', '2', '3', '5', '6')]      # 31 Aug, 7.35 V / 13.8 A / +6 N
def totals(g, lo=100, hi=10000):
    f = g['f']; df = f[1] - f[0]; m = (f >= lo) & (f < hi); return 10 * np.log10((10 ** (g['mags'][:, m] / 10)).sum(1) * df)
def cells(g):                                           # tone-notched broadband 315 Hz-8 kHz, deviation of each capsule from the polar mean
    B = g['B'][:, 4:19]; B = B[:, ~np.isnan(B).any(0)]; d = B - B.mean(0); return float((abs(d) <= 1.3).mean() * 100), float(abs(d).max())
FACT = DATA + '/calibrations/factory-originals-2026-09-16'
def last_at(b, pw, cal=None):                                     # a capture is read with the calibration that existed when it was taken: factory files before 16 Sep, the measured corrections after
    gs = [g for g in groups(base(b), cal or (CORR if b == TODAY else FACT)) if g['pwm'] == pw]; return gs[-1] if gs else None
def polar_stats():
    out = {}
    for name, bs, cal in (('today', [TODAY], None), ('sept', SEPT, None), ('aug', AUG, None), ('sept_c', SEPT, CORR)):
        for pw in (2000, 1900):
            rows = [cells(g) for g in (last_at(b, pw, cal) for b in bs) if g is not None]
            a = np.array(rows); out[name, pw] = dict(n=len(a), med=float(np.median(a[:, 0])), lo=float(a[:, 0].min()), hi=float(a[:, 0].max()), worst=float(np.median(a[:, 1])))
    return out
def ends_centre(g, bi):                                  # ends (|pos| >= 72) minus centre (|pos| <= 18), dB
    B = g['B'][:, bi]; e = np.abs(g['elev']); return float(np.nanmean(B[e >= 72]) - np.nanmean(B[e <= 18]))
def axis_check():
    t0 = last_at(TODAY, 2000); fl = [last_at(f'2004__6in__unset__dp1-baseline-horizontal-prop{k}', 2000) for k in (9, 10, 12, 13, 14, 15, 16, 17)]
    return {n: (ends_centre(t0, i), float(np.median([ends_centre(g, i) for g in fl]))) for i, n in ((12, '2 kHz'), (15, '4 kHz'))}
def bbl(g, lo=4, hi=10):                              # tone-notched broadband 315 Hz-1 kHz (bands 4..9), dB per capsule
    B = g['B'][:, lo:hi]; B = B[:, ~np.isnan(B).any(0)]; return 10 * np.log10((10 ** (B / 10)).sum(1))
def fig_polar():                                       # the app's Polar tab: total level in a band per capsule, mirrored to 360 deg, PWM 2000, dB SPL
    cur = {'today': last_at(TODAY, 2000), 'aug': last_at(AUG[0], 2000)}; FIG = {}
    sep = [last_at(f'2004__6in__unset__dp1-baseline-horizontal-prop{k}', 2000) for k in (15, 16, 17)]       # 2 Sep, arc in the normal orientation, factory files as measured
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 4.1), subplot_kw=dict(projection='polar'), gridspec_kw=dict(wspace=.22))
    sp = lambda v: float(np.sqrt(np.mean((v - v.mean()) ** 2)))
    def draw(ax, g, lo, hi, **kw):
        el = g['elev']; v = totals(g, lo, hi); th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
        ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], marker='o', **kw); return v
    for ax, (lo, hi, rmin, rmax) in zip(axs, ((20, 560, 30, 76), (100, 10000, 50, 80))):
        va = draw(ax, cur['aug'], lo, hi, color='#e0679c', lw=1.5, ms=3, label='31 Aug horizontal, factory files')
        vs = [totals(g, lo, hi) for g in sep]                  # 2 Sep: statistics only, not drawn
        vt = draw(ax, cur['today'], lo, hi, color='#2b6cb0', lw=2.0, ms=3, label='30 Sep prop plane, corrected files')
        FIG[f'{lo}-{hi}'] = dict(sb=sp(va), sa=sp(vt), pb=float(np.ptp(va)), pa=float(np.ptp(vt)), ss=[sp(v) for v in vs], ps=[float(np.ptp(v)) for v in vs])
        ax.set_rlim(rmin, rmax); ticks = list(range(40, rmax, 10)) if rmax < 80 else [60, 80]
        ax.set_rticks(ticks); ax.set_yticklabels([f'{t:g}' for t in ticks]); ax.set_rlabel_position(22); ax.tick_params(axis='y', labelsize=6)
        ax.set_thetagrids([90, 45, 0, 315, 270, 225, 180, 135], ['+90°', '+45°', '0°', '−45°', '−90°', '−45°', '0°', '+45°'], fontsize=6); ax.grid(alpha=.3)
        ax.set_title(f'{lo}–{hi} Hz, dB SPL (radial {rmin}–{rmax})', fontsize=7.5, pad=10)
        f = FIG[f'{lo}-{hi}']
        ax.text(0.5, -.17, f'rms spread (peak-to-peak)\n31 Aug {f["sb"]:.2f} dB ({f["pb"]:.1f}) · 30 Sep {f["sa"]:.2f} dB ({f["pa"]:.1f})', ha='center', fontsize=6.5, transform=ax.transAxes)
    h, l = axs[0].get_legend_handles_labels(); fig.legend(h, l, fontsize=6.8, frameon=False, loc='lower center', ncol=2, bbox_to_anchor=(.5, -.1))
    fig.savefig(HERE + '/fig-polar.png', dpi=200, bbox_inches='tight'); plt.close(fig)
    return FIG

def srcstep(st):                                     # level change vs the empty floor, per capsule, in two bands
    d = st['L'] - F['L']; f = st['f']; r = {}
    for k, (a, b) in {'mid': (1000, 3000), 'hf': (5000, 6400)}.items():
        v = d[(f >= a) & (f < b)].mean(0); r[k] = (float(v.mean()), float(v.std()))
    return r
def hfmlf(run):                                       # arc-wide level at 5-6.4 kHz minus level at 257-400 Hz, dB
    st = stats(run); f, L = st['f'], st['L']; return float(L[(f >= 5000) & (f < 6400)].mean() - L[(f >= 257) & (f < 400)].mean())
def flips():
    pairs = [('2026-09-23/foam-2', '2026-09-23/foam-out'), ('2026-09-23/ceiling-carpet', '2026-09-24/ceiling-carpet-day2'), ('2026-09-24/ceiling1-floor2', '2026-09-24/felt-floor-only'),
             ('2026-09-24/chaotic-carpet-2', '2026-09-24/chaotic-carpet-3'), ('2026-09-25/in-plane-b', '2026-09-25/curtain')]
    return [hfmlf(b) - hfmlf(a) for a, b in pairs]
def mapchange(a, b):                                  # change of the arc-relative map below 3 kHz, dB rms
    x, y = stats(a), stats(b); lo = x['f'] < 3000; return rms((y['D'] - x['D'])[lo])
def roomonly():                                       # same-source, room-only changes that afternoon: largest mean change in any band, and capsule spread at 1-3 kHz
    A_ = stats('2026-09-24/carpet-added'); worst = 0.0; spread = []
    for a, b in ((F, A_), (F, C), (C, C2)):
        d = b['L'] - a['L']; f = a['f']
        for lo, hi in ((257, 400), (400, 630), (630, 1000), (1000, 1600), (1600, 3000), (5000, 6400)):
            v = d[(f >= lo) & (f < hi)].mean(0); worst = max(worst, abs(float(v.mean())))
        v = d[(f >= 1000) & (f < 3000)].mean(0); spread.append(float(v.std()))
    return worst, max(spread)
def a4(src, dst):
    subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=pdfwrite', '-sPAPERSIZE=a4', '-dFIXEDMEDIA', '-dPDFFitPage', f'-sOutputFile={dst}', src], check=True)

CSS = '''@page{size:A4;margin:9mm 13mm} body{font-family:"IBM Plex Sans","DejaVu Sans",Arial,sans-serif;font-size:7.9pt;line-height:1.24;color:#10171b;margin:0}
h1{font-size:15pt;margin:0 0 1pt;letter-spacing:-.02em} h2{font-size:10pt;margin:7pt 0 3pt;padding-top:4pt;border-top:.7pt solid #c6d0d5} p{margin:0 0 3.5pt} ul{margin:0 0 3pt;padding-left:4.5mm} li{margin:0 0 2pt}
table{border-collapse:collapse;width:100%;margin:2pt 0 5pt;font-size:7.4pt} th{font-size:6.4pt;text-transform:uppercase;letter-spacing:.05em;color:#46545c;text-align:left;padding:2.5pt 3pt;border-bottom:1pt solid #10171b;vertical-align:bottom}
td{padding:1.2pt 3pt;border-bottom:.5pt solid #e0e6e9;vertical-align:top} td.num,th.num{font-family:"DejaVu Sans Mono",monospace;font-size:7pt;white-space:nowrap;text-align:right}
td.lst{font-family:"DejaVu Sans Mono",monospace;font-size:6.6pt;text-align:right;white-space:normal;width:26%}
img{width:100%;max-height:9.6cm;object-fit:contain;display:block;margin:2pt auto}
.tag{font-family:"DejaVu Sans Mono",monospace;font-size:6.3pt;color:#74828a} .box{background:#f1f4f6;border-left:2pt solid #17566e;padding:4pt 4mm;margin:4pt 0 5pt}
.q{border-left:1.5pt solid #17566e;padding:1pt 0 1pt 3mm;margin:2pt 0;font-size:7.4pt} .q span{display:block;font-family:"DejaVu Sans Mono",monospace;font-size:6pt;color:#74828a}
.pass{background:#cfe0f3}.marg{background:#f3e6b3}.fail{background:#f0c4a8}'''

def chromium(name):
    subprocess.run(['/snap/bin/chromium', '--headless', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={HERE}/{name}.pdf', f'file://{HERE}/{name}.html'], check=True, stderr=subprocess.DEVNULL)


def grad(t):                                           # t: 0 = green, 1 = yellow, >=2 = red (continuous)
    t = max(0.0, min(2.0, t)); a, b, c = (120, 190, 130), (245, 220, 110), (225, 100, 80)
    lo, hi, u = (a, b, t) if t <= 1 else (b, c, t - 1)
    return 'rgb(%d,%d,%d)' % tuple(round(x + (y - x) * u) for x, y in zip(lo, hi))

def page2(PS):
    rows = ''.join(f"<tr><td class='num'>{fc} Hz</td><td class='num'>±{tol(fc):g}</td><td class='num'>{F['ntones'][fc]}</td>"
                   f"<td class='num' style='background:{grad(G['bm'][fc] / tol(fc))}'>{G['bm'][fc]:.2f}</td><td class='num' style='background:{grad((100 - G['tr'][fc]) / 50)}'>{G['tr'][fc]:.0f} %</td>"
                   f"<td class='num' style='background:{grad(X['bm'][fc] / tol(fc))}'>{X['bm'][fc]:.2f}</td><td class='num' style='background:{grad((100 - X['tr'][fc]) / 50)}'>{X['tr'][fc]:.0f} %</td></tr>" for fc in TOB)
    sc = lambda st: [f"{st['score']:.3f}", f"{cutoff(st)} Hz" if cutoff(st) else 'none', f"{count(st, 'fail')}: {lst(st, 'fail')} Hz", f"{count(st, 'marg')}: {lst(st, 'marg')} Hz", f"{st['tone_all']:.0f} %"]
    sf, sc_ = sc(G), sc(X)
    names = ['Room error below 3 kHz (dB)', 'Inside the tolerance values from this band up to 2500 Hz (highest band evaluated)', 'Bands clearly over the limit (of 11)', 'Bands marginal (of 11)', 'Cells inside the limit, all bands']
    cl = lambda i: 'lst' if i in (2, 3) else 'num'
    card = ''.join(f"<tr><td>{n}</td><td class='{cl(i)}'>{sf[i]}</td><td class='{cl(i)}'><b>{sc_[i]}</b></td></tr>" for i, n in enumerate(names))
    s3 = srcstep(C3)
    MCg = mapchange(DAY3A, FINAL)
    T, Sp, Au, Sc = PS['today', 2000], PS['sept', 2000], PS['aug', 2000], PS['sept_c', 2000]; F1, F2 = PS['fig']['20-560'], PS['fig']['100-10000']
    T9, Sp9, Au9 = PS['today', 1900], PS['sept', 1900], PS['aug', 1900]; AX = PS['axis']
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Chamber evaluation</title><style>{CSS}</style></head><body>
<h1>2 · Main waterfall and the day 3 evaluation</h1><p class="tag" style="margin:0 0 2pt">2.3 Evaluation against the ISO anechoic tolerance values (an analogue, not a qualification)</p>
<p class="tag">11 calibrated capsules on an arc of 0.84 m radius · 95 tones, 257 Hz–6.35 kHz · runs: 25 Sep, <code>day3-a</code> (13:17) → <code>carpet-reordered</code> (19:15)</p>
<h2 style="border:0;margin-top:2pt">The method</h2>
<p><b>Taken from the standards.</b> Each one-third-octave band is judged on its own against the free-field ideal. The standards judge tones and noise separately. Here both measures come from the stepped tones; the band level stands in for the noise test. In each band the worst position is compared with the limit. The limits are the anechoic tolerance values: ±1.5 dB for 125–630 Hz and ±1.0 dB for 800–5000 Hz (ISO 5305:2024 Table 1, p. 8). Cunefare et al. 2003 give the same values (J. Acoust. Soc. Am. 113(2), p. 882; quoted on page 6). ISO 3745:2012 and ISO 26101 are the two qualification procedures; Russo et al. 2018 compare them.</p>
<p><b>Specific to this rig, not taken from the standards.</b> The standards move one microphone along a line away from the source (a traverse) and test how the level falls with distance. Only that test allows a room to be called "qualified" or "in conformity" (ISO 26101-1 p. 3; ISO 3745 §5.1). This rig has eleven fixed capsules at one radius. It tests how uniform the level is around a source that radiates the same way in every direction about its axis. The reference is therefore the arc mean, and the same tolerance values are applied to a different quantity.</p>
<p><b>The two measures.</b> <i>Band level</i>: for each capsule, the mean deviation over the {min(F['ntones'].values())}–{max(F['ntones'].values())} tones in the band (only {F['ntones'][250]} at 250 Hz, because the grid starts at 257 Hz and covers only the top of that band); the worst capsule is compared with the limit. <i>Pure tones</i>: the share of tone × capsule cells inside the limit. A band within ±{MARG:.2f} dB of its limit is called <i>marginal</i>. This margin is the largest difference found between two runs of one unchanged state on the same day ({len(REPEATS)} pairs).</p>
<p><b>What the result means.</b> The room is treated, not qualified. The result is a figure of merit that ranks the bands. It claims neither qualification nor conformity. The standards were available as previews only: ISO 3745:2012 (clauses 1–6.1.2, no annexes), ISO 26101-1 and ISO 5305.</p>
<p class="box" style="margin:2pt 0 1pt;padding:2pt 4mm;font-size:7.2pt"><b>Cell = one tone at one capsule.</b> "Cells in limit" is the share of cells inside the limit. Example, 250 Hz at the start of day 3: 3 tones × 11 capsules = 33 cells; 12 are inside ±1.5 dB, which is 36 %. The deviation columns give the worst capsule's band-mean deviation in dB; their colour shows it as a share of the limit.</p>
<table><thead><tr><th class="num">Band</th><th class="num">Limit (dB)</th><th class="num">Tones (× 11 capsules)</th><th class="num">Day 3 start (dB)</th><th class="num">Cells in limit</th><th class="num">Final (dB)</th><th class="num">Cells in limit</th></tr></thead><tbody>{rows}</tbody></table>
<table><thead><tr><th>Measure</th><th class="num">Day 3 start</th><th class="num">Final</th></tr></thead><tbody>{card}</tbody></table>
<p class="tag"><b>Colour.</b> Deviation columns: the number is the worst capsule's band-mean deviation in dB; the colour shows it as a share of the band's limit (green 0, yellow at the limit, red at twice the limit or more). Cells-in-limit columns: green 100 %, yellow 50 %, red 0 %. The "from this band up" row is set by the highest failing band, so read it together with the two lists below it.</p>
<p class="box" style="margin:2pt 0 3pt"><b>Caveat: the loudspeaker position is not documented for these two runs.</b> During day 3 the loudspeaker was moved on purpose (20 cm closer at 13:44, into the ring plane at 14:03, 5 cm back at 15:29) and then returned to about its starting mounting point. The final point was meant to repeat the starting one, but this was not recorded. The data show the match is not exact: the top-to-bottom tilt of the map went from {G['tilt']:+.2f} to {X['tilt']:+.2f} (a 5 cm move changes it by about 0.25) and the mean level rose by {X['level'] - G['level']:.2f} dB. The map changed by {MCg:.2f} dB rms; for comparison, re-arranging the 24 Sep carpet (<code>chaotic-carpet</code>→<code>chaotic-carpet-2</code>) changed it by {mapchange(CARPET, CARPET2):.2f} dB and a 5 cm source move by 0.80 dB. The gain is therefore the treatments plus a small, unknown difference in source position. The final tilt is closer to the 24 Sep afternoon runs ({F['tilt']:+.2f} to {C3['tilt']:+.2f}). The one pair with a documented, unmoved source is from 24 Sep: empty floor {F['score']:.3f} → carpet {C['score']:.3f} (three carpet arrangements: {C['score']:.3f} / {C2['score']:.3f} / {C3['score']:.3f}).</p>
<h1 style="font-size:15pt;margin:8pt 0 2pt;padding-top:4pt;border-top:.7pt solid #c6d0d5">3 · Polars: is the propeller-plane polar rounder than before?</h1>
<img src="fig-polar.png">
<table><thead><tr><th>Capsule × band values within ±1.3 dB of the polar mean (broadband, tones removed, 315 Hz–8 kHz)</th><th class="num">Runs</th><th class="num">PWM 2000: median (range)</th><th class="num">Worst deviation (median over runs)</th><th class="num">PWM 1900: median (range)</th></tr></thead><tbody>
<tr><td><b>30 Sep</b> (11.7 V), corrections</td><td class="num">1</td><td class="num"><b>{T['med']:.1f} %</b></td><td class="num">{T['worst']:.1f} dB</td><td class="num">{T9['med']:.0f} %</td></tr>
<tr><td>1–2 Sep, arc laid flat (11.65 V, 7.3 A, −4.0 N), factory files</td><td class="num">{Sp['n']}</td><td class="num">{Sp['med']:.1f} % ({Sp['lo']:.0f}–{Sp['hi']:.0f})</td><td class="num">{Sp['worst']:.1f} dB</td><td class="num">{PS['sept', 1900]['med']:.0f} % ({PS['sept', 1900]['lo']:.0f}–{PS['sept', 1900]['hi']:.0f})</td></tr>
<tr><td>31 Aug, arc laid flat (7.35 V, 13.8 A, +6 N: other operating point), factory files</td><td class="num">{Au['n']}</td><td class="num">{Au['med']:.1f} % ({Au['lo']:.0f}–{Au['hi']:.0f})</td><td class="num">{Au['worst']:.1f} dB</td><td class="num">{PS['aug', 1900]['med']:.0f} % ({PS['aug', 1900]['lo']:.0f}–{PS['aug', 1900]['hi']:.0f})</td></tr>
<tr><td class="tag">for reference: 1–2 Sep re-read with the 16 Sep corrections</td><td class="num">{Sc['n']}</td><td class="num">{Sc['med']:.1f} % ({Sc['lo']:.0f}–{Sc['hi']:.0f})</td><td class="num">{Sc['worst']:.1f} dB</td><td class="num">{PS['sept_c', 1900]['med']:.0f} % ({PS['sept_c', 1900]['lo']:.0f}–{PS['sept_c', 1900]['hi']:.0f})</td></tr></tbody></table>
<ul>
<li><b>The figure</b> draws the polars the way the app's Polar tab does. It shows the total level in the band at each capsule, at PWM 2000 (the motor throttle signal, 2000 µs), recomputed from the data. The angle is the capsule's position on the arc; the left half mirrors the right half. <b>Each capture is read with the calibration that existed when it was taken</b>: the factory files for 31 Aug and 1–2 Sep, the corrections for 30 Sep. The "before" curve is the 31 Aug baseline with the arc laid flat. It was taken with a different propeller and at another operating point (7.35 V against 11.7 V), so the two curves are not a controlled pair.</li>
<li><b>20–560 Hz</b> is the low end; it contains the blade-passing tone at about 238 Hz. The rms spread of the total level across the capsules is {F1['sa']:.2f} dB on 30 Sep, {F1['sb']:.2f} dB on 31 Aug and {F1['ss'][0]:.2f} / {F1['ss'][1]:.2f} / {F1['ss'][2]:.2f} dB on 2 Sep (prop15 / 16 / 17). In this band 30 Sep has the smallest spread, but it is the only curve read with the corrections (see the reference row of the table). <b>100–10000 Hz:</b> {F2['sa']:.2f} dB on 30 Sep, {F2['sb']:.2f} dB on 31 Aug and {F2['ss'][0]:.2f} / {F2['ss'][1]:.2f} / {F2['ss'][2]:.2f} dB on 2 Sep. In this band the 2 Sep runs have a slightly smaller spread than 30 Sep. The 2 Sep curves are not drawn; their spreads are given only in this text.</li>
<li><b>Broadband with the tones removed, 315 Hz–8 kHz</b> (table). The level is taken in one-third-octave bands with the propeller tones cut out. On 30 Sep, {T['med']:.0f} % of the capsule × band values lie within ±1.3 dB of the polar mean. The median is {Sp['med']:.0f} % for 1–2 Sep (range {Sp['lo']:.0f}–{Sp['hi']:.0f}) and {Au['med']:.0f} % for 31 Aug (range {Au['lo']:.0f}–{Au['hi']:.0f}). The worst capsule is {T['worst']:.1f} dB off the mean on 30 Sep, against {Sp['worst']:.1f} and {Au['worst']:.1f} dB. Part of this difference is the microphone correction. The same 1–2 Sep captures, re-read with the 16 Sep corrections, give {Sc['med']:.0f} % (range {Sc['lo']:.0f}–{Sc['hi']:.0f}), 30 Sep ({T['med']:.0f} %) lies inside that range but below its median. Read with the same calibration, the 30 Sep polar is not rounder than the 1–2 Sep polars. The gain over the factory-file readings comes from the calibration, not from the room.</li>
</ul>
<h2>Which captures carry the microphone corrections</h2>
<table><thead><tr><th>Capture set</th><th>Date</th><th>Calibration it is read with</th></tr></thead><tbody>
<tr><td>31 Aug horizontal baseline</td><td>31 Aug, before the corrections</td><td><b>factory files</b></td></tr>
<tr><td>prop8–10</td><td>1 Sep, before the corrections</td><td><b>factory files</b></td></tr>
<tr><td>prop11–17 (prop15–17 used for the spreads in the text)</td><td>2 Sep, before the corrections</td><td><b>factory files</b></td></tr>
<tr><td>30 Sep propeller-plane baseline</td><td>30 Sep, after the 16 Sep microphone calibration</td><td><b>corrections</b> (the only propeller capture in this report that has them)</td></tr></tbody></table>
<p class="tag">The corrections were measured on 16 Sep (page 1). The earlier captures are shown as they were taken. The reference row of the table above re-reads 1–2 Sep with the corrections, to show how much of the gain comes from the calibration.</p>
</body></html>"""
    mk = '<h1 style="font-size:15pt;margin:8pt 0 2pt;padding-top:4pt;border-top:.7pt solid #c6d0d5">3 · Polars'
    i = h.index(mk); head = h[:h.index('<body>') + 6]
    open(HERE + '/_p2.html', 'w').write(h[:i] + '</body></html>'); chromium('_p2')
    open(HERE + '/_p2b.html', 'w').write(head + h[i:].replace(mk, '<h1>3 · Polars', 1)); chromium('_p2b')

def page3():
    B3, CL = stats('2026-09-25/blue-carpet'), stats('2026-09-25/closer-a'); s3 = srcstep(C3); RO = roomonly(); FL = flips(); MC = mapchange(CARPET2, CARPET3)
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Semi-anechoic solutions</title><style>{CSS} body{{font-size:7.0pt;line-height:1.2}} td{{padding:1pt 3pt;font-size:7pt}} li{{margin:0 0 1pt}} h2{{margin:5pt 0 2pt}}</style></head><body>
<h1>4 · Semi-anechoic room solutions that apply to this chamber</h1>
<p class="tag"><b>What fails in the final configuration</b> (<code>carpet-reordered</code>, evaluated on its own): clearly over the limit at {lst(X, 'fail')} Hz; marginal at {lst(X, 'marg')} Hz. The blade-passing frequency (BPF, the blade tone) lies at 215–258 Hz; its third harmonic is at 713 Hz. The nearest measured reflections travel 0.68 m further than the direct sound at −72° and 1.49 m further at +36°/+54°, so they arrive 1.98 ms and 4.34 ms after it. Source of the table: docs/acoustic-speculations/chamber-fighting-guide.pdf, §03 (29 facilities).</p>
<table><thead><tr><th>Solution</th><th>What the papers give</th><th>Applies here?</th><th>What the trials show</th></tr></thead><tbody>
<tr><td><b>1. Change the geometry</b> (move the source, the arc or the reflecting object)</td><td>Limits what every other measure can reach. To work down to 500 Hz, every reflection must travel at least 0.69 m further than the direct sound; for 250 Hz, 1.37 m (a 4 ms gate; Matelján, ARTA application note 4, recommends 5 ms or more).</td><td><b>Yes; first, and at no cost.</b> The 0.68 m reflection is just short of the 500 Hz requirement.</td><td>Source position had the largest effect in the trials: moving the loudspeaker about 20 cm closer reduced the room error from {B3['score']:.2f} to {CL['score']:.2f} dB within one afternoon (25 Sep).</td></tr>
<tr><td><b>2. Measured room correction</b> per position and tone</td><td>The source is measured once in a real anechoic chamber and again in the room, band by band: "the uncertainty in measurements is minimal (below 0.55 dB for frequencies above 200 Hz)" (du Plessis et al. 2022, p. 29).</td><td><b>Yes; the strongest option.</b> Valid for a fixed source and fixed microphones, as on this arc. Not valid for a flying drone.</td><td>Needs a reference run in an anechoic chamber (the university's 300 m³ room). Invalid once a capsule is re-mounted: a 1 cm shift changes the response by ±6 dB at high frequency (Bellmann &amp; Klippel, p. 7). Must be checked against the propeller at 200–250 Hz (Mehrgou 2012, p. 34).</td></tr>
<tr><td><b>3. Average over source speed</b></td><td>Room resonances (modes) distort pure tones most. A pattern that changes over a 19 % frequency step averages out over a speed ladder (a series of propeller speeds). No paper gives the remaining error.</td><td><b>Yes; low cost.</b> The hardware exists; 12–15 PWM steps.</td><td>In the flat-arc runs, 8 dB dips in the tone pattern moved with a 19 % frequency step. The 30 Sep polar shape depends on speed outside 1.3–2 kHz.</td></tr>
<tr><td><b>4. Time gating</b></td><td>Only the sound that arrives before the first reflection is kept. The lowest usable frequency is about 1 / gate length: "the time-bandwidth requirement is satisfied on frequencies above 177.9Hz" for a 5.6 ms gate (Matelján, p. 8).</td><td><b>Only above 500 Hz</b>: the gate here is 1.98 ms.</td><td>Useful to identify the surfaces behind the 0.68 m and 1.49 m reflections. Cannot reach the blade tone.</td></tr>
<tr><td><b>5. Absorb: foam, wedges</b></td><td>An absorber about 34 cm deep is needed for 250 Hz; lowering the design frequency from 400 Hz to 100 Hz raises the cost per square metre about four times (Orrego et al. 2018, p. 477). With a reflecting floor the overall level deviates from the inverse-square law by up to 3 dB, and two adjacent microphones differ by up to 10 dB at the blade-passing frequency (Ma et al. 2022, p. 7).</td><td><b>Not at 250 Hz.</b> Yes at 630–1000 Hz: about 10 cm on the surface the measurement identifies.</td><td>The floor under the arc and the source mattered most (empty floor 2.05 → carpet 1.32, same afternoon). The same material on the walls had no measurable effect.</td></tr>
<tr><td><b>6. Subwavelength absorber</b> (thin compared with the wavelength)</td><td>A 100 mm metasurface absorber: "99.2% absorptance at 239 Hz in experiment" (Long et al. 2020, Sci. Rep. 10:13823).</td><td><b>The only option that reaches the blade tone</b>, <b>but only if</b> the 238 Hz error comes from the room and not from the stand.</td><td>Decide this first with the reverse-rotation capture (step 2 below).</td></tr>
</tbody></table>
<h2>Order for this chamber</h2>
<ol style="margin:0 0 3pt;padding-left:5mm">
<li>Record the room: hub height, room dimensions, and what stands within 1.5 m of the arc ends. Then move the object behind the 0.68 m reflection, or move the arc away from it.</li>
<li>Take one capture with the propeller turning the other way and everything else unchanged. This separates asymmetry caused by the stand from asymmetry caused by the room.</li>
<li>Measure the loudspeaker correction (solution 2) at the blade-tone frequencies (215–258 Hz and 713 Hz) for the eleven positions. Then compare it with the propeller at the same positions.</li>
<li>Run a speed ladder to average the tones. Then treat only the surfaces the sweep names (about 10 cm of foam at 630–1000 Hz).</li>
</ol>
<h2>Microphone placement against the standards</h2>
<ul style="margin:0 0 3pt">
<li><b>Meets:</b> far field, (kr)² ≈ 15 at 250 Hz, above 3 (k = wavenumber, r = ring radius). The ring radius, 0.84 m, is more than a quarter wavelength (λ/4) from 250 Hz up. The capsule axis is normal to the measurement surface (ISO 3745 §6.1.1). ISO 5305 requires R ≥ 5·D<sub>A</sub> (radius at least five times the diameter of the aircraft). This holds for the 137 mm sphere and for one 6-inch propeller, not for larger rotors.</li>
<li><b>Does not meet:</b> the UMIK-2 is not a class 1 free-field microphone of type WS2F or WS3F (ISO 5305 §5.1, ISO 3745 §6.1.1). The ring, clamps and cables are supports without acoustic treatment. All capsules are at one radius, so the fall of level with distance is not tested.</li>
<li><b>Not recorded:</b> the distance from the ring ends to the walls and the floor, the hub height, and ISO 5305 H<sub>m</sub> (the distance from each microphone to the walls, floor and ceiling, or to the wedge tips).</li></ul>
<div class="q">"TABLE I. Maximum allowable difference in anechoic rooms between measured and theoretical free-field levels per ISO 3745 and ANSI S12.35." <span>Cunefare et al. 2003, J. Acoust. Soc. Am. 113(2), p. 882</span></div>
<h2>Where the accepted configuration stands, and what the method cannot say</h2>
<ul>
<li>Evaluated on its own (25 Sep): room error {X['score']:.3f} dB, within the strict anechoic tolerance values from the {cutoff(X)} Hz band up to the 2500 Hz band (the highest evaluated), {X['tone_all']:.0f} % of tone cells inside. <b>Comparable rooms in the held papers</b> (not the 63–275 Hz rotor chambers, which are better rooms): a 6.8 m³ low-cost box conforming to the ISO 3745 anechoic row from 500 Hz with one point 1.0 dB over (Orrego et al. 2018, p. 6); a 51 m³ room that passes with noise and fails with pure tones (Nash 2019); Amazon Prime Air's rotor room, ±1 dB only above 2.2 × BPF and ±4 dB below (Nardari 2019, p. 2). Rooms tested against the standard keep the strict row and publish the range that passes (Russo 2018: "in conformity" for a reduced range); rooms that cannot meet it use their own tolerance. We keep the strict row, as Orrego, Nash and Kayhan did, and report the failures. No held paper judges a room by the angular spread across a fixed ring.</li>
<li>Deviation from the arc mean is blind to an error shared by all eleven positions; the ISO traverse has not been run, so this ranks bands and does not certify. The anechoic table is used because the floor under the arc is absorbing.</li>
<li><b>Open, unexplained: a two-state switch in the source chain.</b> The level at 5–6.35 kHz minus the level at 257–400 Hz takes one of two values and jumps by the same amount between some neighbouring runs: <code>foam-2</code>→<code>foam-out</code> {FL[0]:+.1f}, <code>ceiling-carpet</code>→<code>ceiling-carpet-day2</code> (next morning) {FL[1]:+.1f}, <code>ceiling1-floor2</code>→<code>felt-floor-only</code> {FL[2]:+.1f}, <code>chaotic-carpet-2</code>→<code>chaotic-carpet-3</code> {FL[3]:+.1f}, <code>in-plane-b</code>→<code>curtain</code> {FL[4]:+.1f} dB. Within a day the loudspeaker device and amplitude did not change. It is not a source move (a 5 cm move changes the map by 0.80 dB, the 24 Sep flip by {MC:.2f} dB), not moved absorber (room-only changes that afternoon moved the mean level by at most {RO[0]:.2f} dB), and not a gain or supply-voltage change (that would shift every frequency alike, and 257–400 Hz does not move). It cancels in the room error, which is relative to the arc mean. Still to check: cable, connectors, amplifier and supply (300 Hz and 5 kHz on <code>live_tone</code> while handling each).</li>
<li>The grid starts at 257 Hz; 3–5 kHz is excluded (sphere), 5–6.4 kHz indicative.</li>
</ul></body></html>"""
    open(HERE + '/_p3.html', 'w').write(h); chromium('_p3')



FO = os.path.expanduser('~/ŻYCIE/PRACA/SoundVisualizer-data/data/calibrations/factory-originals-2026-09-16')
def mic_before_after(run):                              # same capture, factory calibration files vs the measured (16 Sep) corrections
    from calibrator.rig import parse_umik_calibration
    import json
    rows = json.load(open(S + run + '/levels.json')); meta = json.load(open(S + run + '/meta.json'))
    ser = {f"{m['position_deg']:+.0f}": m['serial'] for m in meta['arc']}
    pos = sorted(float(k) for k in rows[0] if k != 'freq'); f = np.array([r['freq'] for r in rows]); B = np.full((len(f), len(pos)), np.nan)
    for j, q in enumerate(pos):
        k = f'{q:+.0f}'; c = parse_umik_calibration(open(f'{FO}/{ser[k]}.txt').read())
        for i, r in enumerate(rows): B[i, j] = r[k]['level_dbfs'] - np.interp(f[i], c.freq_hz, c.gain_db) + 94 - c.sens_factor_db
    f2, p2, A, _ = read_map(S + run)
    nb, na = B - B.mean(1, keepdims=True), A - A.mean(1, keepdims=True); lo = f < 3000
    return f, np.asarray(p2), nb[:, ::-1], na[:, ::-1], rms(nb[lo]), rms(na[lo]), float(np.ptp(B[lo].mean(0))), float(np.ptp(A[lo].mean(0)))

def fig_mic(figsize=(7.4, 6.4), fs=1.0, out='/fig-mic.png', short=False, lang='en'):
    PL = lang == 'pl'; dc = (lambda t: t.replace('.', ',')) if PL else (lambda t: t)
    from matplotlib.colors import LinearSegmentedColormap
    runs = [(DAY3A, 'day3-a (początek dnia 3)' if PL else 'day3-a (start of day 3)'), (FINAL, 'carpet-reordered (stan końcowy)' if PL else 'carpet-reordered (final)')]; res = [mic_before_after(r) for r, _ in runs]
    bw = LinearSegmentedColormap.from_list('bw', ['#c05621', '#f6d7c3', '#ffffff', '#cfe0f3', '#2b6cb0'])
    fig, axs = plt.subplots(3, 2, figsize=figsize, gridspec_kw=dict(hspace=.5, wspace=.12))
    f = res[0][0]; pos = res[0][1][::-1]; xx = np.arange(len(f) + 1); yy = np.arange(len(pos) + 1)
    nom = {257: '260', 400: '400', 630: '630', 1000: '1k', 1600: dc('1.6k'), 2500: dc('2.5k'), 6000: '6k'}
    tk = []; tl = []
    for z, lab in nom.items():
        i = int(np.argmin(abs(f - z)))
        if abs(f[i] - z) / z < 0.02: tk.append(i); tl.append(lab)
    ims = {}
    for c, ((run, nm), (f, p, nb, na, eb, ea, sb, sa)) in enumerate(zip(runs, res)):
        G = np.abs(nb) - np.abs(na)
        for r, (M, ttl, cm, v) in enumerate(((nb, (dc(f'{nm}\npliki fabryczne: {eb:.3f} dB poniżej 3 kHz, rozstęp {sb:.1f} dB') if PL else f'{nm}\nfactory files: {eb:.3f} dB below 3 kHz, span {sb:.1f} dB'), 'RdBu_r', 12), (na, (dc(f'z poprawkami: {ea:.3f} dB, rozstęp {sa:.1f} dB') if PL else f'corrected: {ea:.3f} dB, span {sa:.1f} dB'), 'RdBu_r', 12),
                                           (G, ('efekt poprawki (niebieski = bliżej średniej łuku)' if PL else 'effect of the correction (blue = closer to arc mean)'), bw, 3))):
            a = axs[r, c]; ims[r] = a.pcolormesh(xx, yy, M.T, cmap=cm, vmin=-v, vmax=v); a.axvline(np.searchsorted(f, 4000), color='k', lw=1.2); a.invert_yaxis()
            a.set_yticks(np.arange(len(pos)) + .5); a.set_yticklabels([f'{q:+.0f}°'.replace('-', '−') for q in pos] if c == 0 else [], fontsize=5.5 * fs)
            a.set_xticks([i + .5 for i in tk]); a.set_xticklabels(tl, fontsize=5.5 * fs); a.set_title(ttl, fontsize=6.4 * fs, loc='left')
    cb = fig.colorbar(ims[0], ax=axs[:2, :], shrink=.85, pad=.02, aspect=28); cb.set_label(('poziom minus średnia łuku (dB)' if PL else 'level minus arc mean (dB)') if short else 'capsule level minus arc mean (dB): blue = quieter, red = louder', fontsize=6 * fs); cb.ax.tick_params(labelsize=5.5 * fs)
    cb2 = fig.colorbar(ims[2], ax=axs[2, :], shrink=.85, pad=.02, aspect=14); cb2.set_ticks([-3, 0, 3]); cb2.set_ticklabels(['−3 dB\ndalej', '0', '+3 dB\nbliżej'] if PL else ['−3 dB\nfurther', '0', '+3 dB\ncloser']); cb2.set_label(('zmiana (dB)' if PL else 'change (dB)') if short else 'change in deviation from the arc mean (dB)', fontsize=6 * fs); cb2.ax.tick_params(labelsize=5.5 * fs)
    fig.text(.45, .015, 'Częstotliwość w Hz (k = kHz; czarna linia: pominięty zakres 3–5 kHz). Góra każdej mapy = +90°.' if PL else 'Frequency in Hz (k = kHz; the black line marks the omitted 3–5 kHz). Top of each map = +90°.', ha='center', fontsize=6 * fs)
    fig.savefig(HERE + out, dpi=200, bbox_inches='tight'); plt.close(fig)
    return res

def page1():
    R = fig_mic()
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Microphones</title><style>{CSS}
.top{{display:flex;gap:4mm;align-items:flex-start;margin:3pt 0 4pt}} .top img{{width:4.6cm;height:auto;max-height:none;margin:0;flex:none}} .cap{{font-size:6.8pt;color:#46545c;margin:1pt 0 0}} .fig{{width:100%;max-height:15cm;object-fit:contain}}</style></head><body>
<h1>1 · Microphone calibration</h1>
<p class="tag">SoundVisualizer · chamber report, 2026-10-05 · calibrator session 2026-09-16 (97 tones per capsule, amplitude 0.03)</p>
<div class="top"><div><img src="photo-source.jpg"><p class="cap"><b>The test loudspeaker</b>: a printed 1-litre sphere with an 8 cm driver, placed at the hub (the centre of the ring).</p></div>
<div><p>Eleven UMIK-2 measurement microphones, called <i>capsules</i> in this report, sit on a ring of 1.68 m diameter (0.84 m radius). Each came with a factory calibration file, and nobody had checked these files against each other. On 16 Sep we measured every capsule in turn, one at a time, at the same mounting point in front of our loudspeaker, over a stepped frequency sweep: 97 tones from 62 Hz to 16 kHz, 12 per octave. One capsule (810-8904) was measured three full times (18:21, 18:30 and 20:43) as the reference. The loudspeaker, the room and the mounting point were the same for every capsule, so a difference between two curves comes from the capsules.</p>
<ul><li><b>Seven of the eleven factory files were off by 0.8–2.6 dB on average</b> (3.5 dB at the worst single frequency). The errors are grouped by serial-number prefix.</li>
<li>Each capsule's difference from the reference was added to its calibration curve. The updated curves are called the <i>corrections</i>; the original curves are the <i>factory files</i>. For the same sound, the spread of the eleven readings fell from <b>4.01 dB to 0.02 dB</b>. Repeated measurements agreed to 0.08 dB (standard deviation).</li>
<li>The reference level is set by the four capsules whose factory files agree with the measurement. Still open: the absolute level, which needs a 94 dB sound calibrator.</li>
<li>On the 30 Sep propeller-plane polar (chapter 3), the corrections reduced the roughness from 3.3 to 1.0 dB (a different statistic from the rms spread on page 5, defined in <code>docs/analysis/baseline-story-2026-09-30/REPORT.pdf</code>).</li></ul></div></div>
<h2>Before and after, on two captures from this report</h2>
<img class="fig" src="fig-mic.png">
<p><b>How to read the figure.</b> Each map is one capture. Rows are capsule positions, columns are tones, and the colour is the capsule's level minus the mean of all eleven (the <i>arc mean</i>). Left: the start of day 3 (<code>day3-a</code>, 25 Sep). Right: the final configuration (<code>carpet-reordered</code>). Top row: read with the factory files. Middle row: read with the corrections. Bottom row: the effect of the correction. The factory files give each capsule a different offset, which shows up as horizontal stripes across every frequency. The <i>span</i> is the range of the capsules' mean levels. It changes from <b>{R[0][6]:.1f} → {R[0][7]:.1f} dB</b> at the start of day 3 and <b>{R[1][6]:.1f} → {R[1][7]:.1f} dB</b> in the final configuration. The <i>room error</i> is the rms deviation of the capsules from the arc mean, below 3 kHz. It changes <b>{R[0][4]:.3f} → {R[0][5]:.3f} dB</b> and <b>{R[1][4]:.3f} → {R[1][5]:.3f} dB</b>. The change is mainly a per-capsule offset. It therefore mainly moves whole rows and leaves the frequency pattern of the room in place. Every room-error number elsewhere in this report uses the corrected files.</p>
<p class="tag">The numbers on this page come from the project notes (CLAUDE.md in the repository) and the calibrator session of 2026-09-16. Where this page and the notes differ, the notes govern.</p>
</body></html>"""
    open(HERE + '/_p0.html', 'w').write(h); chromium('_p0')

def pagewf(png):
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Chamber</title><style>{CSS}
.big{{display:block;width:100%;height:auto;max-height:none;margin:3pt 0 3pt}}</style></head><body>
<h1>2 · Main waterfall and the day 3 evaluation</h1><p class="tag" style="margin:0">2.1 The chamber</p>
<img class="big" src="photo-chamber.jpg">
<p style="margin:0"><b>The chamber in the final configuration</b> (<code>carpet-reordered</code>, photographed 5 Oct). The microphone ring lies flat around the propeller rig at the hub. The loudspeaker tripod stands on the left. Batting covers the floor and the ceiling; wedges and lined pillars line the walls. The waterfall on the next page compares the start of day 3 with this state.</p></body></html>"""
    open(HERE + '/_p1a.html', 'w').write(h); chromium('_p1a')
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Waterfall</title><style>{CSS}
.fig{{display:block;margin:0 auto;max-height:24.5cm;width:auto}}</style></head><body>
<h1>2 · Main waterfall and the day 3 evaluation</h1><p class="tag" style="margin:0 0 2pt">2.2 Main waterfall: start of day 3 against the final state</p>
<p style="margin:0 0 3pt">Both runs were taken on 25 Sep (day 3 of the chamber treatments, 23–25 Sep) and are read with the corrections. The loudspeaker was moved during the day and returned to about its starting mounting point; the position is not documented (see the caveat on page 4). A <i>cell</i> in the figure is one tone at one capsule.</p>
<img class="fig" src="{png}"></body></html>"""
    open(HERE + '/_p1.html', 'w').write(h); chromium('_p1')

if __name__ == '__main__':
    print(f'source check carpet vs floor: level {C["level"] - F["level"]:+.2f} dB, tilt {C["tilt"] - F["tilt"]:+.2f}; repeat: {C2["level"] - F["level"]:+.2f}, {C2["tilt"] - F["tilt"]:+.2f}')
    import json
    try:
        PS = polar_stats(); PS['axis'] = axis_check(); PS['fig'] = fig_polar()
        json.dump({f'{k[0]}@{k[1]}' if isinstance(k, tuple) else k: v for k, v in PS.items()}, open(HERE + '/polar-stats.json', 'w'), indent=1)
    except SystemExit:                  # 30 Sep bases not on this machine: reuse the saved polar figure and statistics
        PS = {(k.split('@')[0], int(k.split('@')[1])) if '@' in k else k: v for k, v in json.load(open(HERE + '/polar-stats.json')).items()}
    for kk, v in PS.items():
        if kk not in ('axis', 'fig'): print(kk, {a: round(b, 1) for a, b in v.items()})
    subprocess.run([sys.executable, STEP, DAY3A, FINAL, 'Day 3 start (worst) vs final · source position not documented', 'floor-vs-carpet'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    D = ROOT + '/docs/analysis/chamber-treatments-2026-09-23/'
    import shutil; shutil.copy(D + 'floor-vs-carpet.png', HERE + '/_wf.png'); from PIL import Image, ImageChops; _im = Image.open(HERE + '/_wf.png').convert('RGB'); _im.crop(ImageChops.difference(_im, Image.new('RGB', _im.size, (255, 255, 255))).getbbox()).save(HERE + '/_wf.png'); pagewf('_wf.png'); page1(); page2(PS); page3()
    subprocess.run(['pdfunite', HERE + '/_p0.pdf', HERE + '/_p1a.pdf', HERE + '/_p1.pdf', HERE + '/_p2.pdf', HERE + '/_p2b.pdf', HERE + '/_p3.pdf', HERE + '/CHAMBER-FINAL.pdf'], check=True)
    for x in ('_wf.png', '_p1a.pdf', '_p1a.html', '_p1.html', '_p0.pdf', '_p0.html', '_p1.pdf', '_p2.pdf', '_p2b.pdf', '_p2b.html', '_p3.pdf', '_p2.html', '_p3.html'): os.remove(HERE + '/' + x)
    for g in ('floor-vs-carpet.pdf', 'floor-vs-carpet.png'): os.remove(D + g)
    print('floor', round(F['score'], 3), cutoff(F), count(F, 'fail'), round(F['tone_all']), '| carpet', round(C['score'], 3), cutoff(C), count(C, 'fail'), count(C, 'marg'), round(C['tone_all']),
          '| final', round(X['score'], 3), cutoff(X), '| MARG', MARG)
