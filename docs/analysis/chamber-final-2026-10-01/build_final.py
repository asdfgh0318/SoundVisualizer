"""build_final.py — 2-page chamber report: waterfall comparison (same day, same source) + evaluation by the chamber-qualification method.

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
def fig_polar():
    cur = {'today': last_at(TODAY, 2000), 'aug': last_at(AUG[0], 2000), 'sept': last_at('2004__6in__unset__dp1-baseline-horizontal-prop9', 2000)}
    lev = {k: totals(v) for k, v in cur.items()}; allv = np.concatenate(list(lev.values())); lo, hi = np.floor(allv.min()) - 2, np.ceil(allv.max()) + 1
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.45), subplot_kw=dict(projection='polar'), gridspec_kw=dict(wspace=.28))
    spread = lambda v: float(np.sqrt(np.mean((v - v.mean()) ** 2)))
    for ax, other, ttl, col in ((axs[0], 'aug', 'vs 31 Aug · 7.35 V, 13.8 A (your screenshot)', '#e0679c'), (axs[1], 'sept', 'vs 2 Sep · 11.65 V, 7.3 A (same operating point)', '#c05621')):
        for key, c, lw in (('today', '#2b6cb0', 1.6), (other, col, 1.3)):
            el = cur[key]['elev']; v = lev[key]; th = np.radians(np.r_[el, 180 - el[::-1]]); r = np.r_[v, v[::-1]]
            ax.plot(np.r_[th, th[0]], np.r_[r, r[0]], color=c, lw=lw, marker='o', ms=2.6)
        ax.set_rlim(0, 80); ax.set_rticks([20, 40, 60, 80]); ax.set_yticklabels(['20', '40', '60', '80 dB SPL']); ax.set_rlabel_position(22); ax.tick_params(axis='y', labelsize=5.5); ax.set_thetagrids([90, 0, 270], ['+90°', '0°', '−90°'], fontsize=6); ax.grid(alpha=.3)
        ax.set_title(ttl, fontsize=7, pad=11)
        ax.text(0.5, -.12, f'spread (rms about the mean): today {spread(lev["today"]):.2f} dB · other {spread(lev[other]):.2f} dB', ha='center', fontsize=6.5, transform=ax.transAxes)
    from matplotlib.lines import Line2D
    fig.legend([Line2D([0], [0], color='#2b6cb0', lw=1.6), Line2D([0], [0], color='#e0679c', lw=1.3), Line2D([0], [0], color='#c05621', lw=1.3)],
               ['30 Sep, PWM 2000', '31 Aug horizontal, PWM 2000', '2 Sep prop9 (median-spread run), PWM 2000'], fontsize=6.3, frameon=False, loc='lower center', ncol=3, bbox_to_anchor=(.5, -.04))
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
td{padding:2pt 3pt;border-bottom:.5pt solid #e0e6e9;vertical-align:top} td.num,th.num{font-family:"DejaVu Sans Mono",monospace;font-size:7pt;white-space:nowrap;text-align:right}
td.lst{font-family:"DejaVu Sans Mono",monospace;font-size:6.6pt;text-align:right;white-space:normal;width:26%}
img{width:100%;max-height:6.3cm;object-fit:contain;display:block;margin:2pt auto}
.tag{font-family:"DejaVu Sans Mono",monospace;font-size:6.3pt;color:#74828a} .box{background:#f1f4f6;border-left:2pt solid #17566e;padding:4pt 4mm;margin:4pt 0 5pt}
.q{border-left:1.5pt solid #17566e;padding:1pt 0 1pt 3mm;margin:2pt 0;font-size:7.4pt} .q span{display:block;font-family:"DejaVu Sans Mono",monospace;font-size:6pt;color:#74828a}
.pass{background:#cfe0f3}.marg{background:#f3e6b3}.fail{background:#f0c4a8}'''

def chromium(name):
    subprocess.run(['/snap/bin/chromium', '--headless', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={HERE}/{name}.pdf', f'file://{HERE}/{name}.html'], check=True, stderr=subprocess.DEVNULL)

def page2(PS):
    rows = ''.join(f"<tr><td class='num'>{fc} Hz</td><td class='num'>±{tol(fc):g}</td><td class='num'>{F['ntones'][fc]}</td>"
                   f"<td class='num {verdict(G, fc)}'>{G['bm'][fc]:.2f}</td><td class='num'>{G['tr'][fc]:.0f} %</td>"
                   f"<td class='num {verdict(X, fc)}'>{X['bm'][fc]:.2f}</td><td class='num'>{X['tr'][fc]:.0f} %</td></tr>" for fc in TOB)
    sc = lambda st: [f"{st['score']:.3f}", f"{cutoff(st)} Hz" if cutoff(st) else 'none', f"{count(st, 'fail')}: {lst(st, 'fail')} Hz", f"{count(st, 'marg')}: {lst(st, 'marg')} Hz", f"{st['tone_all']:.0f} %"]
    sf, sc_ = sc(G), sc(X)
    names = ['Room error below 3 kHz (dB)', 'Band-level qualified from', 'Bands clearly over the limit (of 11)', 'Bands marginal', 'Pure-tone cells inside the limit']
    cl = lambda i: 'lst' if i in (2, 3) else 'num'
    card = ''.join(f"<tr><td>{n}</td><td class='{cl(i)}'>{sf[i]}</td><td class='{cl(i)}'><b>{sc_[i]}</b></td></tr>" for i, n in enumerate(names))
    s3 = srcstep(C3)
    MCg = mapchange(DAY3A, FINAL)
    T, Sp, Au = PS['today', 2000], PS['sept', 2000], PS['aug', 2000]
    T9, Sp9, Au9 = PS['today', 1900], PS['sept', 1900], PS['aug', 1900]; AX = PS['axis']
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Chamber evaluation</title><style>{CSS}</style></head><body>
<h1>Evaluation and the prop-plane check</h1>
<p class="tag">SoundVisualizer · 2026-10-01 · 11 calibrated capsules on a 0.84 m arc · 95 tones, 257 Hz–6.35 kHz · page 1: waterfall, 25 Sep, <code>day3-a</code> (13:17, worst of the day) → <code>carpet-reordered</code> (19:15, final)</p>
<h2 style="border:0;margin-top:2pt">The method</h2>
<p>Chambers are qualified one one-third-octave band at a time against the free-field ideal: reported as qualified between two bands, the cut-off the lowest band above which everything passes, noise and pure tones separately. Limits: ±1.5 dB to 630 Hz, ±1.0 dB from 800 Hz (Cunefare et al. 2003, J. Acoust. Soc. Am. 113(2), p. 882, quoted on page 3). <b>Our adaptation:</b> eleven fixed positions around an axisymmetric source, so the reference is the arc mean; <b>band level</b> = each capsule's mean over the {F['ntones'][630]}–{F['ntones'][1000]} tones in the band, worst capsule against the limit; <b>pure tones</b> = share of single tone × capsule cells inside. Within ±{MARG:.2f} dB of a limit is marginal (the largest difference between two same-day runs of one unchanged state, {len(REPEATS)} pairs).</p>
<table><thead><tr><th class="num">Band</th><th class="num">Limit</th><th class="num">Tones</th><th class="num">Day 3 start</th><th class="num">tones in limit</th><th class="num">Final</th><th class="num">tones in limit</th></tr></thead><tbody>{rows}</tbody></table>
<table><thead><tr><th>Measure</th><th class="num">Day 3 start</th><th class="num">Final</th></tr></thead><tbody>{card}</tbody></table>
<p class="tag">Blue = inside, yellow = marginal, orange = over. The cut-off is set by the highest failing band, so read it with the lists. <b>Caveat:</b> the source was deliberately moved between these two runs (20 cm closer at 13:44, into the ring plane at 14:03) and the arc-relative map changed by {MCg:.2f} dB rms, against 0.14 dB for a re-arranged carpet and 0.80 dB for a 5 cm move; so the improvement is the day's treatments <i>and</i> source positions together, not treatments alone. The only pair with a source known to be unmoved is 24 Sep, floor without wedges {F['score']:.3f} → carpet {C['score']:.3f} (three carpet arrangements {C['score']:.3f} / {C2['score']:.3f} / {C3['score']:.3f}), tilt change {C['tilt'] - F['tilt']:+.2f} dB per unit sin(el).</p>
<h2>The prop-plane check: is the polar rounder than before?</h2>
<img src="fig-polar.png">
<table><thead><tr><th>Tone-notched broadband, 315 Hz–8 kHz, cells within ±1.3 dB of the polar mean</th><th class="num">Runs</th><th class="num">PWM 2000: median (range)</th><th class="num">worst cell</th><th class="num">PWM 1900: median (range)</th></tr></thead><tbody>
<tr><td><b>30 Sep, today</b></td><td class="num">1</td><td class="num"><b>{T['med']:.0f} %</b></td><td class="num">{T['worst']:.1f} dB</td><td class="num">{T9['med']:.0f} %</td></tr>
<tr><td>2 Sep, same operating point (11.65 V, 7.3 A, −4.0 N)</td><td class="num">{Sp['n']}</td><td class="num">{Sp['med']:.0f} % ({Sp['lo']:.0f}–{Sp['hi']:.0f})</td><td class="num">{Sp['worst']:.1f} dB</td><td class="num">{Sp9['med']:.0f} % ({Sp9['lo']:.0f}–{Sp9['hi']:.0f})</td></tr>
<tr><td>31 Aug (7.35 V, 13.8 A, +6 N: a different operating point)</td><td class="num">{Au['n']}</td><td class="num">{Au['med']:.0f} % ({Au['lo']:.0f}–{Au['hi']:.0f})</td><td class="num">{Au['worst']:.1f} dB</td><td class="num">{Au9['med']:.0f} % ({Au9['lo']:.0f}–{Au9['hi']:.0f})</td></tr></tbody></table>
<ul>
<li><b>Against 31 Aug the polar is clearly rounder where it counts</b>: the worst capsule is {T['worst']:.1f} dB off the mean instead of {Au['worst']:.1f} dB, and the 31 Aug runs range down to {Au['lo']:.0f} % of cells in tolerance. That run is the one in the screenshot.</li>
<li><b>Against 2 Sep, which had the same voltage, current and thrust, it is not rounder</b>: {T['med']:.0f} % against a median of {Sp['med']:.0f} % ({Sp['lo']:.0f}–{Sp['hi']:.0f}), inside the scatter of the 2 Sep runs. Between 31 Aug and 2 Sep the supply went from 7.35 to 11.65 V.</li>
<li><b>It is a prop-plane measurement.</b> The ends of the arc read louder than its centre at 2 and 4 kHz by {AX['2 kHz'][0]:+.1f} and {AX['4 kHz'][0]:+.1f} dB today; the flat-arc runs, where the true difference is zero, show the same ({AX['2 kHz'][1]:+.1f} and {AX['4 kHz'][1]:+.1f} dB median). So that structure is position-fixed error, not directivity.</li>
</ul></body></html>"""
    open(HERE + '/_p2.html', 'w').write(h); chromium('_p2')

def page3():
    B3, CL = stats('2026-09-25/blue-carpet'), stats('2026-09-25/closer-a'); s3 = srcstep(C3); RO = roomonly(); FL = flips(); MC = mapchange(CARPET2, CARPET3)
    h = f"""<!doctype html><html><head><meta charset="utf-8"><title>Semi-anechoic solutions</title><style>{CSS}</style></head><body>
<h1>Semi-anechoic room solutions that apply to this chamber</h1>
<p class="tag">What fails (accepted configuration, evaluated on its own): clearly over the ISO limit at {lst(X, 'fail')} Hz, marginal at {lst(X, 'marg')} Hz; the blade tone sits at 215–258 Hz and its third harmonic at 713 Hz. Nearest reflectors measured: extra path 0.68 m at −72° and 1.49 m at +36°/+54°, i.e. 1.98 and 4.34 ms. Source: chamber-fighting-guide.pdf §03, 29 facilities.</p>
<table><thead><tr><th>Solution</th><th>What the papers give</th><th>Applies to us?</th><th>What we already know</th></tr></thead><tbody>
<tr><td><b>1. Move the geometry</b> (source, arc, reflector)</td><td>Sets the ceiling for everything else. Reaching 500 Hz needs every reflector ≥0.69 m of extra path, 250 Hz needs 1.37 m (gate ≥5 ms, Matelján, ARTA note 4).</td><td><b>Yes, first, free.</b> The 0.68 m surface is just short for 500 Hz.</td><td>Source position was the largest lever in our trials: moving the speaker about 20 cm closer took the room error from {B3['score']:.2f} to {CL['score']:.2f} dB within one afternoon (25 Sep).</td></tr>
<tr><td><b>2. Measured room correction</b> per position and tone</td><td>Source measured once in a real chamber and again in the room, band by band: "the uncertainty in measurements is minimal (below 0.55 dB for frequencies above 200 Hz)" (du Plessis et al. 2022, p. 29).</td><td><b>Yes, the strongest.</b> Valid for a fixed source and fixed microphones — our arc — not for a flying drone.</td><td>Needs a reference run in a chamber (the university's 300 m³). Void if a capsule is re-seated: 1 cm moves the response ±6 dB at high frequency (Bellmann &amp; Klippel, p. 7). Must be checked against the prop at 200–250 Hz (Mehrgou 2012, p. 34).</td></tr>
<tr><td><b>3. Average over source speed</b></td><td>Tones are where a modal room hurts most; a pattern that changes over a 19 % frequency step averages out over a speed ladder. No published residual.</td><td><b>Yes, cheap.</b> Hardware exists; 12–15 PWM steps.</td><td>Tone-pattern holes of 8 dB moved with a 19 % frequency step in the flat-arc runs; the polar shape of 30 Sep depends on speed outside 1.3–2 kHz.</td></tr>
<tr><td><b>4. Time gating</b></td><td>Lowest usable frequency ≈ 1 / gate length: "the time-bandwidth requirement is satisfied on frequencies above 177.9Hz" for a 5.6 ms gate (Matelján, p. 8).</td><td><b>Only above 500 Hz</b>: our gate is 1.98 ms.</td><td>Good for naming the 0.68 m and 1.49 m reflectors; cannot reach the blade tone.</td></tr>
<tr><td><b>5. Absorb: foam, wedges</b></td><td>34 cm of depth per 250 Hz; cost about ×4 per octave down (Orrego et al. 2018, p. 477).</td><td><b>Not at 250 Hz.</b> Yes at 630–1000 Hz: about 10 cm on the named surface.</td><td>The floor under the arc and source mattered most (wedges off: 2.05 → carpet 1.32, same afternoon); the same material on the walls did nothing.</td></tr>
<tr><td><b>6. Subwavelength absorber</b></td><td>"99.2% absorptance at 239 Hz in experiment" in 100 mm (Long et al. 2020, Sci. Rep. 10:13823).</td><td><b>The one exception</b> for the blade tone, <b>but only if</b> the 238 Hz error is the room, not the stand.</td><td>Decide with the reverse-rotation capture first.</td></tr>
<tr><td><b>7. Hemi-anechoic floor</b></td><td>Removing the floor treatment costs ~3 dB broadband and up to 10 dB at the blade tone, repeatability 0.5 dB (Ma et al. 2022, p. 7).</td><td>Already in play: our floor is treated.</td><td>Floor changes moved the score; the same material on the walls did nothing.</td></tr>
<tr><td>Active absorption, intensity or holography, outdoors</td><td>9.6 dB up to ~600 Hz (Haasjes 2025); 1–3 dB (ISO 9614-1); outdoors agreed to 0.1 dB at ≥20 dB signal-to-noise (Kim et al. 2022).</td><td>Not now.</td><td>Outdoors only for an absolute-level check.</td></tr>
</tbody></table>
<h2>Order for this chamber</h2>
<ol style="margin:0 0 3pt;padding-left:5mm">
<li>Record the room (hub height, dimensions, what stands within 1.5 m of the arc ends) and move the 0.68 m reflector or the arc away from it.</li>
<li>One capture with the propeller turning the other way, everything else identical: separates stand-induced from room-induced asymmetry.</li>
<li>Loudspeaker correction at the blade harmonics (215–258 Hz, 713 Hz) for the eleven positions, then compare with the propeller at the same positions.</li>
<li>Speed ladder to average the tones.</li>
<li>Treat only the surfaces the sweep names (about 10 cm of foam at 630–1000 Hz).</li>
</ol>
<div class="q">"TABLE I. Maximum allowable difference in anechoic rooms between measured and theoretical free-field levels per ISO 3745 and ANSI S12.35." <span>Cunefare et al. 2003, J. Acoust. Soc. Am. 113(2), p. 882</span></div>
<h2>Where the accepted configuration stands, and what the method cannot say</h2>
<ul>
<li>Evaluated on its own (25 Sep): room error {X['score']:.3f} dB, qualified from the {cutoff(X)} Hz band, {X['tone_all']:.0f} % of tone cells inside the limit. Published small rotor chambers report cut-offs of 63–275 Hz (29 facilities; METU's semi-anechoic room, 160 Hz, Kayhan 2008 p. 63); ours is {cutoff(X) / 275:.0f}–{cutoff(X) / 63:.0f} times higher, by a test easier in one respect (the arc mean, not the ideal, is the reference) and harder in another (the worst of eleven capsules).</li>
<li>Deviation from the arc mean is blind to an error shared by all eleven positions; the ISO traverse has not been run, so this ranks bands and does not certify. The anechoic table is used because the floor under the arc is absorbing.</li>
<li><b>Open, unexplained: a two-state switch in the source chain.</b> The arc-wide balance of 5–6.4 kHz against 257–400 Hz sits on two levels and flips by the same amount between neighbouring runs: <code>foam-2</code>→<code>foam-out</code> {FL[0]:+.1f}, <code>ceiling-carpet</code>→<code>ceiling-carpet-day2</code> (next morning) {FL[1]:+.1f}, <code>ceiling1-floor2</code>→<code>felt-floor-only</code> {FL[2]:+.1f}, <code>chaotic-carpet-2</code>→<code>-3</code> {FL[3]:+.1f}, <code>in-plane-b</code>→<code>curtain</code> {FL[4]:+.1f} dB. Speaker device and amplitude were unchanged at the same-day flips. Not a source move (a 5 cm move changes the map by 0.80 dB; the 24 Sep flip by {MC:.2f}), not redistributed absorber (room-only changes that afternoon moved the mean level by at most {RO[0]:.2f} dB), not a gain or supply-voltage change (that would shift every frequency alike; 257–400 Hz does not move). It cancels in the arc-relative score. To check: the speaker cable's position near the sphere, connectors, the amplifier and its supply; test with 300 Hz and 5 kHz tones on <code>live_tone</code> while handling each.</li>
<li>Only same-day pairs with an unmoved source are compared. The grid starts at 257 Hz, above the blade tone; 3–5 kHz is excluded (sphere), 5–6.4 kHz indicative.</li>
</ul></body></html>"""
    open(HERE + '/_p3.html', 'w').write(h); chromium('_p3')

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
    subprocess.run([sys.executable, STEP, DAY3A, FINAL, 'Start of day 3 (worst run) vs the final configuration · same day, source moved in between (see page 2)', 'floor-vs-carpet'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    D = ROOT + '/docs/analysis/chamber-treatments-2026-09-23/'
    a4(D + 'floor-vs-carpet.pdf', HERE + '/_p1.pdf'); page2(PS); page3()
    subprocess.run(['pdfunite', HERE + '/_p1.pdf', HERE + '/_p2.pdf', HERE + '/_p3.pdf', HERE + '/CHAMBER-FINAL.pdf'], check=True)
    for x in ('_p1.pdf', '_p2.pdf', '_p3.pdf', '_p2.html', '_p3.html'): os.remove(HERE + '/' + x)
    for g in ('floor-vs-carpet.pdf', 'floor-vs-carpet.png'): os.remove(D + g)
    print('floor', round(F['score'], 3), cutoff(F), count(F, 'fail'), round(F['tone_all']), '| carpet', round(C['score'], 3), cutoff(C), count(C, 'fail'), count(C, 'marg'), round(C['tone_all']),
          '| final', round(X['score'], 3), cutoff(X), '| MARG', MARG)
