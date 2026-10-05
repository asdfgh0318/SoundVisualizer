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
SEPT = [f'2004__6in__unset__dp1-baseline-horizontal-prop{k}' for k in range(8, 18)]          # 2 Sep, 11.65 V / 7.3 A / -4.0 N, the operating point of 30 Sep
AUG = [f'2004__6in__unset__dp1-baseline-horizontal-{k}' for k in ('2026-08-31', '2', '3', '5', '6')]      # 31 Aug, 7.35 V / 13.8 A / +6 N
def totals(g, lo=100, hi=10000):
    f = g['f']; df = f[1] - f[0]; m = (f >= lo) & (f < hi); return 10 * np.log10((10 ** (g['mags'][:, m] / 10)).sum(1) * df)
def cells(g):                                           # tone-notched broadband 315 Hz-8 kHz, deviation of each capsule from the polar mean
    B = g['B'][:, 4:19]; B = B[:, ~np.isnan(B).any(0)]; d = B - B.mean(0); return float((abs(d) <= 1.3).mean() * 100), float(abs(d).max())
def last_at(b, pw):
    gs = [g for g in groups(base(b), CORR) if g['pwm'] == pw]; return gs[-1] if gs else None
def polar_stats():
    out = {}
    for name, bs in (('today', [TODAY]), ('sept', SEPT), ('aug', AUG)):
        for pw in (2000, 1900):
            rows = [cells(g) for g in (last_at(b, pw) for b in bs) if g is not None]
            a = np.array(rows); out[name, pw] = dict(n=len(a), med=float(np.median(a[:, 0])), lo=float(a[:, 0].min()), hi=float(a[:, 0].max()), worst=float(np.median(a[:, 1])))
    return out
def ends_centre(g, bi):                                  # ends (|pos| >= 72) minus centre (|pos| <= 18), dB
    B = g['B'][:, bi]; e = np.abs(g['elev']); return float(np.nanmean(B[e >= 72]) - np.nanmean(B[e <= 18]))
def axis_check():
    t0 = last_at(TODAY, 2000); fl = [last_at(f'2004__6in__unset__dp1-baseline-horizontal-prop{k}', 2000) for k in (9, 10, 12, 13, 14, 15, 16, 17)]
    return {n: (ends_centre(t0, i), float(np.median([ends_centre(g, i) for g in fl]))) for i, n in ((12, '2 kHz'), (15, '4 kHz'))}
def bbl(g, lo=4, hi=10):                              # tone-notched broadband 315 Hz-1 kHz (bands 4..9), dB per capsule
    B = g['B'][:, lo:hi]; B = B[:, ~np.isnan(B).any(0)]; return 10 * np.log10((10 ** (B / 10)).sum(1))
def fig_polar():
    cur = {'today': last_at(TODAY, 2000), 'aug': last_at(AUG[0], 2000), 'sept': last_at('2004__6in__unset__dp1-baseline-horizontal-prop9', 2000)}
    dv = {k: bbl(v) - bbl(v).mean() for k, v in cur.items()}
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.6), subplot_kw=dict(projection='polar'), gridspec_kw=dict(wspace=.12))
    for ax, other, ttl, col in ((axs[0], 'aug', 'vs 31 Aug · 7.35 V, 13.8 A (your screenshot)', '#e0679c'), (axs[1], 'sept', 'vs 2 Sep · 11.65 V, 7.3 A (same operating point)', '#c05621')):
        for key, c, lw in (('today', '#2b6cb0', 1.6), (other, col, 1.3)):
            el = cur[key]['elev']; v = dv[key] + 8; th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
            ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=c, lw=lw, marker='o', ms=2.6)
        ax.set_rlim(0, 16); ax.set_rticks([4, 8, 12]); ax.set_yticklabels(['−4', '0', '+4 dB']); ax.set_rlabel_position(22); ax.tick_params(axis='y', labelsize=5.5)
        ax.set_thetagrids([90, 0, 270], ['+90°', '0°', '−90°'], fontsize=6); ax.grid(alpha=.3); ax.set_title(ttl, fontsize=7, pad=11)
        ax.text(0.5, -.17, f'rms spread: 30 Sep {np.std(dv["today"]):.2f} dB · other {np.std(dv[other]):.2f} dB\npeak-to-peak: {np.ptp(dv["today"]):.1f} dB · {np.ptp(dv[other]):.1f} dB', ha='center', fontsize=6.3, transform=ax.transAxes)
    from matplotlib.lines import Line2D
    fig.legend([Line2D([0], [0], color='#2b6cb0', lw=1.6), Line2D([0], [0], color='#e0679c', lw=1.3), Line2D([0], [0], color='#c05621', lw=1.3)],
               ['30 Sep, PWM 2000', '31 Aug horizontal, PWM 2000', '2 Sep prop9 (median-spread run), PWM 2000'], fontsize=6.3, frameon=False, loc='lower center', ncol=3, bbox_to_anchor=(.5, -.1))
    fig.suptitle('Tone-notched broadband 315 Hz–1 kHz, relative to each curve\'s own mean, zoomed to ±8 dB (on the full 0–80 dB SPL scale all three are near-round)', fontsize=6.6, y=1.04)
    fig.savefig(HERE + '/fig-polar.png', dpi=200, bbox_inches='tight'); plt.close(fig)

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
img{width:100%;max-height:5.9cm;object-fit:contain;display:block;margin:2pt auto}
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
    names = ['Room error below 3 kHz (dB)', 'Within the tolerance values from (band)', 'Bands clearly over the limit (of 11)', 'Bands marginal', 'Tone × capsule cells inside the limit']
    cl = lambda i: 'lst' if i in (2, 3) else 'num'
    card = ''.join(f"<tr><td>{n}</td><td class='{cl(i)}'>{sf[i]}</td><td class='{cl(i)}'><b>{sc_[i]}</b></td></tr>" for i, n in enumerate(names))
    s3 = srcstep(C3)
    MCg = mapchange(DAY3A, FINAL)
    T, Sp, Au = PS['today', 2000], PS['sept', 2000], PS['aug', 2000]
    T9, Sp9, Au9 = PS['today', 1900], PS['sept', 1900], PS['aug', 1900]; AX = PS['axis']
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Chamber evaluation</title><style>{CSS}</style></head><body>
<h1>2 · Main waterfalls and the day 3 evaluation</h1><p class="tag" style="margin:0 0 2pt">2.3 evaluation against the ISO anechoic tolerance values (an analogue, not a qualification)</p>
<p class="tag">11 calibrated capsules on a 0.84 m arc · 95 tones, 257 Hz–6.35 kHz · runs: 25 Sep, <code>day3-a</code> (13:17) → <code>carpet-reordered</code> (19:15)</p>
<h2 style="border:0;margin-top:2pt">The method</h2>
<p><b>Where the method comes from.</b> <u>Taken from the standards:</u> each one-third-octave band judged on its own against the free-field ideal, tones and noise separately, the worst position against the limit, and the anechoic tolerances ±1.5 dB for 125–630 Hz and ±1.0 dB for 800–5000 Hz (ISO 5305:2024 Table 1, p. 8; the same values in Cunefare et al. 2003, J. Acoust. Soc. Am. 113(2), p. 882, quoted on page 5; ISO 3745:2012 and ISO 26101 are the two procedures, compared by Russo et al. 2018). <u>Ours, not the standards':</u> they move one microphone along a traverse and test the decay of level with distance, and only that test earns the words "qualified" or "in conformity" (ISO 26101-1 p. 3; ISO 3745 §5.1). We have eleven fixed capsules at one radius and test uniformity around an axisymmetric source, so the reference is the arc mean and the same values are applied to a different quantity. <b>Band level</b> = each capsule's mean over the {F['ntones'][630]}–{F['ntones'][1000]} tones in the band, worst capsule against the value; <b>pure tones</b> = share of tone × capsule cells inside; within ±{MARG:.2f} dB is marginal (largest difference between two same-day runs of one unchanged state, {len(REPEATS)} pairs). The room is treated and not qualified, so this is a figure of merit that ranks bands; it claims neither qualification nor conformity. Held: previews of ISO 3745:2012 (clauses 1–6.1.2, no annexes), ISO 26101-1 and ISO 5305.</p>
<table><thead><tr><th class="num">Band</th><th class="num">Limit</th><th class="num">Tones (× 11 capsules)</th><th class="num">Day 3 start</th><th class="num">cells in limit</th><th class="num">Final</th><th class="num">cells in limit</th></tr></thead><tbody>{rows}</tbody></table>
<table><thead><tr><th>Measure</th><th class="num">Day 3 start</th><th class="num">Final</th></tr></thead><tbody>{card}</tbody></table>
<p class="tag">Colour = worst-capsule deviation as a share of the band's limit: green 0, yellow at the limit, red at twice the limit or more (cells in limit: green 100 %, yellow 50 %, red 0 %). A cell is one tone at one capsule (3 tones × 11 capsules = 33 cells at 250 Hz, where the grid starts at 257 Hz). The cut-off is set by the highest failing band, so read it with the lists. <b>Caveat:</b> the source was moved between these runs (20 cm closer at 13:44, into the ring plane at 14:03): the map changed by {MCg:.2f} dB rms, against 0.14 for a re-arranged carpet and 0.80 for a 5 cm move, so the gain is treatments and source positions together. The one pair with an unmoved source is 24 Sep, empty floor {F['score']:.3f} → carpet {C['score']:.3f} (three arrangements {C['score']:.3f} / {C2['score']:.3f} / {C3['score']:.3f}).</p>
<h1 style="font-size:15pt;margin:8pt 0 2pt;padding-top:4pt;border-top:.7pt solid #c6d0d5">3 · Polars: is the prop-plane polar rounder than before?</h1>
<img src="fig-polar.png">
<table><thead><tr><th>Tone-notched broadband, 315 Hz–8 kHz, cells within ±1.3 dB of the polar mean</th><th class="num">Runs</th><th class="num">PWM 2000: median (range)</th><th class="num">worst cell</th><th class="num">PWM 1900: median (range)</th></tr></thead><tbody>
<tr><td><b>30 Sep, today</b></td><td class="num">1</td><td class="num"><b>{T['med']:.0f} %</b></td><td class="num">{T['worst']:.1f} dB</td><td class="num">{T9['med']:.0f} %</td></tr>
<tr><td>2 Sep, same operating point (11.65 V, 7.3 A, −4.0 N)</td><td class="num">{Sp['n']}</td><td class="num">{Sp['med']:.0f} % ({Sp['lo']:.0f}–{Sp['hi']:.0f})</td><td class="num">{Sp['worst']:.1f} dB</td><td class="num">{Sp9['med']:.0f} % ({Sp9['lo']:.0f}–{Sp9['hi']:.0f})</td></tr>
<tr><td>31 Aug (7.35 V, 13.8 A, +6 N: other operating point)</td><td class="num">{Au['n']}</td><td class="num">{Au['med']:.0f} % ({Au['lo']:.0f}–{Au['hi']:.0f})</td><td class="num">{Au['worst']:.1f} dB</td><td class="num">{Au9['med']:.0f} % ({Au9['lo']:.0f}–{Au9['hi']:.0f})</td></tr></tbody></table>
<ul>
<li><b>Rounder than 31 Aug where it counts</b>: worst capsule {T['worst']:.1f} dB off the mean instead of {Au['worst']:.1f} dB; the 31 Aug runs go down to {Au['lo']:.0f} % of cells in tolerance. That run is the one in the screenshot, whose total level (tones included) is equally spread, 1.39 vs 1.41 dB; the gain is in the broadband.</li>
<li><b>Not rounder than 2 Sep</b> (same voltage, current, thrust): {T['med']:.0f} % against a median of {Sp['med']:.0f} % ({Sp['lo']:.0f}–{Sp['hi']:.0f}), inside the scatter of the 2 Sep runs.</li>
<li><b>Prop-plane measurement</b>: ends of the arc read louder than the centre at 2 and 4 kHz by {AX['2 kHz'][0]:+.1f} and {AX['4 kHz'][0]:+.1f} dB today, and by {AX['2 kHz'][1]:+.1f} and {AX['4 kHz'][1]:+.1f} dB (median) in the flat-arc runs where the true difference is zero: position-fixed error, not directivity.</li>
</ul></body></html>"""
    open(HERE + '/_p2.html', 'w').write(h); chromium('_p2')

def page3():
    B3, CL = stats('2026-09-25/blue-carpet'), stats('2026-09-25/closer-a'); s3 = srcstep(C3); RO = roomonly(); FL = flips(); MC = mapchange(CARPET2, CARPET3)
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Semi-anechoic solutions</title><style>{CSS}</style></head><body>
<h1>4 · Semi-anechoic room solutions that apply to this chamber</h1>
<p class="tag">What fails (accepted configuration, evaluated on its own): clearly over the ISO limit at {lst(X, 'fail')} Hz, marginal at {lst(X, 'marg')} Hz; the blade tone sits at 215–258 Hz and its third harmonic at 713 Hz. Nearest reflectors measured: extra path 0.68 m at −72° and 1.49 m at +36°/+54°, i.e. 1.98 and 4.34 ms. Source: chamber-fighting-guide.pdf §03, 29 facilities.</p>
<table><thead><tr><th>Solution</th><th>What the papers give</th><th>Applies to us?</th><th>What we already know</th></tr></thead><tbody>
<tr><td><b>1. Move the geometry</b> (source, arc, reflector)</td><td>Sets the ceiling for everything else. Reaching 500 Hz needs every reflector ≥0.69 m of extra path, 250 Hz needs 1.37 m (gate ≥5 ms, Matelján, ARTA note 4).</td><td><b>Yes, first, free.</b> The 0.68 m surface is just short for 500 Hz.</td><td>Source position was the largest lever in our trials: moving the speaker about 20 cm closer took the room error from {B3['score']:.2f} to {CL['score']:.2f} dB within one afternoon (25 Sep).</td></tr>
<tr><td><b>2. Measured room correction</b> per position and tone</td><td>Source measured once in a real chamber and again in the room, band by band: "the uncertainty in measurements is minimal (below 0.55 dB for frequencies above 200 Hz)" (du Plessis et al. 2022, p. 29).</td><td><b>Yes, the strongest.</b> Valid for a fixed source and fixed microphones — our arc — not for a flying drone.</td><td>Needs a reference run in a chamber (the university's 300 m³). Void if a capsule is re-seated: 1 cm moves the response ±6 dB at high frequency (Bellmann &amp; Klippel, p. 7). Must be checked against the prop at 200–250 Hz (Mehrgou 2012, p. 34).</td></tr>
<tr><td><b>3. Average over source speed</b></td><td>Tones are where a modal room hurts most; a pattern that changes over a 19 % frequency step averages out over a speed ladder. No published residual.</td><td><b>Yes, cheap.</b> Hardware exists; 12–15 PWM steps.</td><td>Tone-pattern holes of 8 dB moved with a 19 % frequency step in the flat-arc runs; the polar shape of 30 Sep depends on speed outside 1.3–2 kHz.</td></tr>
<tr><td><b>4. Time gating</b></td><td>Lowest usable frequency ≈ 1 / gate length: "the time-bandwidth requirement is satisfied on frequencies above 177.9Hz" for a 5.6 ms gate (Matelján, p. 8).</td><td><b>Only above 500 Hz</b>: our gate is 1.98 ms.</td><td>Good for naming the 0.68 m and 1.49 m reflectors; cannot reach the blade tone.</td></tr>
<tr><td><b>5. Absorb: foam, wedges</b></td><td>34 cm of depth per 250 Hz; cost about ×4 per octave down (Orrego et al. 2018, p. 477). Removing the floor treatment costs ~3 dB broadband and up to 10 dB at the blade tone (Ma et al. 2022, p. 7).</td><td><b>Not at 250 Hz.</b> Yes at 630–1000 Hz: about 10 cm on the named surface.</td><td>The floor under the arc and source mattered most (wedges off: 2.05 → carpet 1.32, same afternoon); the same material on the walls did nothing.</td></tr>
<tr><td><b>6. Subwavelength absorber</b></td><td>"99.2% absorptance at 239 Hz in experiment" in 100 mm (Long et al. 2020, Sci. Rep. 10:13823).</td><td><b>The one exception</b> for the blade tone, <b>but only if</b> the 238 Hz error is the room, not the stand.</td><td>Decide with the reverse-rotation capture first.</td></tr>
</tbody></table>
<h2>Order for this chamber</h2>
<ol style="margin:0 0 3pt;padding-left:5mm">
<li>Record the room (hub height, dimensions, what stands within 1.5 m of the arc ends) and move the 0.68 m reflector or the arc away from it.</li>
<li>One capture with the propeller turning the other way, everything else identical: separates stand-induced from room-induced asymmetry.</li>
<li>Loudspeaker correction at the blade harmonics (215–258 Hz, 713 Hz) for the eleven positions, then compare with the propeller at the same positions.</li>
<li>Speed ladder to average the tones, then treat only the surfaces the sweep names (about 10 cm of foam at 630–1000 Hz).</li>
</ol>
<h2>Microphone placement against the standards</h2>
<ul style="margin:0 0 3pt">
<li><b>Meets:</b> far field ((kr)² ≈ 15 at 250 Hz, above 3); the ring radius 0.84 m is more than λ/4 from 250 Hz up; capsule axis normal to the measurement surface (ISO 3745 §6.1.1); ISO 5305 R ≥ 5·D<sub>A</sub> holds for the 137 mm sphere and one 6-inch propeller, not for larger rotors.</li>
<li><b>Does not meet:</b> UMIK-2 is not a WS2F/WS3F class 1 free-field microphone (ISO 5305 §5.1, ISO 3745 §6.1.1); the ring, clamps and cables are untreated supports; one radius only, so decay with distance is not tested.</li>
<li><b>Not recorded:</b> distance of the ring ends to the walls and floor, hub height, ISO 5305 H<sub>m</sub>.</li></ul>
<div class="q">"TABLE I. Maximum allowable difference in anechoic rooms between measured and theoretical free-field levels per ISO 3745 and ANSI S12.35." <span>Cunefare et al. 2003, J. Acoust. Soc. Am. 113(2), p. 882</span></div>
<h2>Where the accepted configuration stands, and what the method cannot say</h2>
<ul>
<li>Evaluated on its own (25 Sep): room error {X['score']:.3f} dB, within the strict anechoic tolerance values from the {cutoff(X)} Hz band up, {X['tone_all']:.0f} % of tone cells inside. <b>Comparable rooms in the held papers</b> (not the 63–275 Hz rotor chambers, which are better rooms): a 6.8 m³ low-cost box conforming to the ISO 3745 anechoic row from 500 Hz with one point 1.0 dB over (Orrego et al. 2018, p. 6); a 51 m³ room that passes with noise and fails with pure tones (Nash 2019); Amazon Prime Air's rotor room, ±1 dB only above 2.2 × BPF and ±4 dB below (Nardari 2019, p. 2). Rooms tested against the standard keep the strict row and publish the range that passes (Russo 2018: "in conformity" for a reduced range); rooms that cannot meet it use their own tolerance. We keep the strict row, as Orrego, Nash and Kayhan did, and report the failures. No held paper judges a room by the angular spread across a fixed ring.</li>
<li>Deviation from the arc mean is blind to an error shared by all eleven positions; the ISO traverse has not been run, so this ranks bands and does not certify. The anechoic table is used because the floor under the arc is absorbing.</li>
<li><b>Open, unexplained: a two-state switch in the source chain.</b> The arc-wide balance of 5–6.4 kHz against 257–400 Hz sits on two levels and flips by the same amount between neighbouring runs: <code>foam-2</code>→<code>foam-out</code> {FL[0]:+.1f}, <code>ceiling-carpet</code>→<code>ceiling-carpet-day2</code> (next morning) {FL[1]:+.1f}, <code>ceiling1-floor2</code>→<code>felt-floor-only</code> {FL[2]:+.1f}, <code>chaotic-carpet-2</code>→<code>-3</code> {FL[3]:+.1f}, <code>in-plane-b</code>→<code>curtain</code> {FL[4]:+.1f} dB. Speaker device and amplitude were unchanged at the same-day flips. Not a source move (a 5 cm move changes the map by 0.80 dB; the 24 Sep flip by {MC:.2f}), not redistributed absorber (room-only changes that afternoon moved the mean level by at most {RO[0]:.2f} dB), not a gain or supply-voltage change (that would shift every frequency alike; 257–400 Hz does not move). It cancels in the arc-relative score. To check: cable near the sphere, connectors, amplifier and supply (300 Hz and 5 kHz on <code>live_tone</code> while handling each).</li>
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

def fig_mic():
    from matplotlib.colors import LinearSegmentedColormap
    runs = [(DAY3A, 'day3-a (start of day 3)'), (FINAL, 'carpet-reordered (final)')]; res = [mic_before_after(r) for r, _ in runs]
    bw = LinearSegmentedColormap.from_list('bw', ['#c05621', '#f6d7c3', '#ffffff', '#cfe0f3', '#2b6cb0'])
    fig, axs = plt.subplots(3, 2, figsize=(7.4, 6.4), gridspec_kw=dict(hspace=.5, wspace=.12))
    f = res[0][0]; pos = res[0][1][::-1]; xx = np.arange(len(f) + 1); yy = np.arange(len(pos) + 1)
    tk = [i for i, q in enumerate(f) if any(abs(q - z) / z < 0.02 for z in [257, 400, 630, 1000, 1600, 2500, 5000, 6000])]
    for c, ((run, nm), (f, p, nb, na, eb, ea, sb, sa)) in enumerate(zip(runs, res)):
        G = np.abs(nb) - np.abs(na)
        for r, (M, ttl, cm, v) in enumerate(((nb, f'{nm}\nfactory files: {eb:.3f} dB below 3 kHz, span {sb:.1f} dB', 'RdBu_r', 12), (na, f'corrected: {ea:.3f} dB, span {sa:.1f} dB', 'RdBu_r', 12),
                                           (G, 'closer to flat (blue) or further (orange)', bw, 3))):
            a = axs[r, c]; a.pcolormesh(xx, yy, M.T, cmap=cm, vmin=-v, vmax=v); a.axvline(np.searchsorted(f, 4000), color='k', lw=1.2); a.invert_yaxis()
            a.set_yticks(np.arange(len(pos)) + .5); a.set_yticklabels([f'{q:+.0f}°' for q in pos] if c == 0 else [], fontsize=5.5)
            a.set_xticks([i + .5 for i in tk]); a.set_xticklabels([f'{f[i]:.0f}' for i in tk], fontsize=5.5); a.set_title(ttl, fontsize=6.4, loc='left')
    fig.text(.5, .015, 'Hz (3–5 kHz omitted). Rows: level of each capsule relative to the arc mean (±12 dB); bottom row ±3 dB. Top of each map = +90°.', ha='center', fontsize=6)
    fig.savefig(HERE + '/fig-mic.png', dpi=200, bbox_inches='tight'); plt.close(fig)
    return res

def page1():
    R = fig_mic()
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Microphones</title><style>{CSS}
.top{{display:flex;gap:4mm;align-items:flex-start;margin:3pt 0 4pt}} .top img{{width:4.6cm;height:auto;max-height:none;margin:0;flex:none}} .cap{{font-size:6.8pt;color:#46545c;margin:1pt 0 0}} .fig{{width:100%;max-height:15cm;object-fit:contain}}</style></head><body>
<h1>1 · What we did with the microphones: substitution calibration</h1>
<p class="tag">SoundVisualizer · chamber report, 2026-10-05 · calibrator session 2026-09-16</p>
<div class="top"><div><img src="photo-source.jpg"><p class="cap"><b>The source</b>: a printed 1 l sphere with an 8 cm driver, at the hub.</p></div>
<div><p>Eleven UMIK-2 capsules sit on the 1.68 m ring. Their factory calibration files were never checked against each other, so on 16 Sep every capsule was measured against every other at one seat (55 pairs, 12 tones per octave). At one seat the source and the room are the same for both capsules, so their difference is the capsule.</p>
<ul><li><b>Seven of the eleven factory files were wrong by 0.6–3.6 dB</b>, clustered by serial prefix.</li>
<li>The corrections went into each capsule's calibration curve. The spread across the eleven, for the same sound, fell from <b>4.01 dB to 0.02 dB</b>. Repeatability of the method: 0.08 dB sd.</li>
<li>The datum is the four capsules whose files agree with measurement. Still open: the absolute level, which needs a 94 dB calibrator.</li>
<li>On the 30 Sep prop-plane polar the corrections cut the roughness from 3.3 to 1.0 dB.</li></ul></div></div>
<h2>Before and after, on two captures from this report</h2>
<img class="fig" src="fig-mic.png">
<p>Same two captures, calibrated two ways: the factory files (top) and the measured corrections (middle); \u201cspan\u201d is the range of the capsules' mean levels. The factory files add a different offset to each capsule, which shows up as horizontal stripes across every frequency; the span of the capsules' mean levels is <b>{R[0][6]:.1f} → {R[0][7]:.1f} dB</b> at the start of day 3 and <b>{R[1][6]:.1f} → {R[1][7]:.1f} dB</b> in the final configuration. Room error below 3 kHz changes <b>{R[0][4]:.3f} → {R[0][5]:.3f} dB</b> and <b>{R[1][4]:.3f} → {R[1][5]:.3f} dB</b>. The change is a per-capsule offset, so it moves rows, not the frequency structure of the room; every room-error number elsewhere in this report uses the corrected files.</p>
<p class="tag">Numbers from the project notes (CLAUDE.md, calibrator session 2026-09-16), which govern where this page and they differ.</p>
</body></html>"""
    open(HERE + '/_p0.html', 'w').write(h); chromium('_p0')

def pagewf(png):
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Chamber</title><style>{CSS}
.big{{display:block;width:100%;height:auto;max-height:none;margin:3pt 0 3pt}}</style></head><body>
<h1>2 · Main waterfalls and the day 3 evaluation</h1><p class="tag" style="margin:0">2.1 the chamber</p>
<img class="big" src="photo-chamber.jpg">
<p style="margin:0"><b>The chamber in the final configuration</b> (<code>carpet-reordered</code>, photographed 5 Oct): the arc ring laid flat around the propeller rig at the hub, the speaker tripod on the left, batting on the floor and ceiling, wedges and lined pillars on the walls. The waterfall on the next page compares the start of day 3 with this state.</p></body></html>"""
    open(HERE + '/_p1a.html', 'w').write(h); chromium('_p1a')
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Waterfall</title><style>{CSS}
.fig{{display:block;margin:0 auto;max-height:24.5cm;width:auto}}</style></head><body>
<h1>2 · Main waterfalls and the day 3 evaluation</h1><p class="tag" style="margin:0 0 2pt">2.2 main waterfall: day 3 start against the final state</p>
<p style="margin:0 0 3pt">Both runs are from 25 Sep with the corrected microphones. The source was moved between them (page 4).</p>
<img class="fig" src="{png}"></body></html>"""
    open(HERE + '/_p1.html', 'w').write(h); chromium('_p1')

if __name__ == '__main__':
    print(f'source check carpet vs floor: level {C["level"] - F["level"]:+.2f} dB, tilt {C["tilt"] - F["tilt"]:+.2f}; repeat: {C2["level"] - F["level"]:+.2f}, {C2["tilt"] - F["tilt"]:+.2f}')
    import json
    try:
        PS = polar_stats(); PS['axis'] = axis_check(); fig_polar()
        json.dump({f'{k[0]}@{k[1]}' if isinstance(k, tuple) else k: v for k, v in PS.items()}, open(HERE + '/polar-stats.json', 'w'), indent=1)
    except SystemExit:                  # 30 Sep bases not on this machine: reuse the saved polar figure and statistics
        PS = {(k.split('@')[0], int(k.split('@')[1])) if '@' in k else k: v for k, v in json.load(open(HERE + '/polar-stats.json')).items()}
    for kk, v in PS.items():
        if kk != 'axis': print(kk, {a: round(b, 1) for a, b in v.items()})
    subprocess.run([sys.executable, STEP, DAY3A, FINAL, 'Day 3 start (worst) vs final · source moved in between', 'floor-vs-carpet'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    D = ROOT + '/docs/analysis/chamber-treatments-2026-09-23/'
    import shutil; shutil.copy(D + 'floor-vs-carpet.png', HERE + '/_wf.png'); from PIL import Image, ImageChops; _im = Image.open(HERE + '/_wf.png').convert('RGB'); _im.crop(ImageChops.difference(_im, Image.new('RGB', _im.size, (255, 255, 255))).getbbox()).save(HERE + '/_wf.png'); pagewf('_wf.png'); page1(); page2(PS); page3()
    subprocess.run(['pdfunite', HERE + '/_p0.pdf', HERE + '/_p1a.pdf', HERE + '/_p1.pdf', HERE + '/_p2.pdf', HERE + '/_p3.pdf', HERE + '/CHAMBER-FINAL.pdf'], check=True)
    for x in ('_wf.png', '_p1a.pdf', '_p1a.html', '_p1.html', '_p0.pdf', '_p0.html', '_p1.pdf', '_p2.pdf', '_p3.pdf', '_p2.html', '_p3.html'): os.remove(HERE + '/' + x)
    for g in ('floor-vs-carpet.pdf', 'floor-vs-carpet.png'): os.remove(D + g)
    print('floor', round(F['score'], 3), cutoff(F), count(F, 'fail'), round(F['tone_all']), '| carpet', round(C['score'], 3), cutoff(C), count(C, 'fail'), count(C, 'marg'), round(C['tone_all']),
          '| final', round(X['score'], 3), cutoff(X), '| MARG', MARG)
