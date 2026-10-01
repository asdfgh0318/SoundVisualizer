"""build_final.py — 3-page chamber report: final configuration, empty-room worst case, evaluation by the chamber-qualification method.

    .venv/bin/python docs/analysis/chamber-final-2026-10-01/build_final.py

Runs: FINAL = the accepted state (carpet-reordered), WORST = the bare floor with the wedges off (floor-no-wedges, the nearest thing to an
empty room that was measured), START = the untouched chamber of 2026-09-23. Change WORST to compare against another state.
Every number in the report is computed here.
"""
import os, sys, subprocess, html
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..')); sys.path.insert(0, ROOT)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from calibrator.rig import read_map
S = ROOT + '/calibrator/sessions/'
FINAL, RERUN, WORST, START = '2026-09-25/carpet-reordered', '2026-09-30/carpet-reordered-rerun', '2026-09-24/floor-no-wedges', '2026-09-23/vertical-2a'
STEP = ROOT + '/docs/analysis/chamber-treatments-2026-09-23/build_step_figure.py'
TOB = [250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500]
tol = lambda fc: 1.5 if fc <= 630 else 1.0                       # ISO 3745 anechoic table
rms = lambda x: float(np.sqrt(np.nanmean(np.asarray(x) ** 2)))
sel = lambda f, fc: (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))
BETTER, WORSE, MARGC, INK = '#2b6cb0', '#c05621', '#d9b44a', '#10171b'

def load(run):
    f, pos, L, _ = read_map(S + run); f = np.asarray(f); L = np.asarray(L, float)
    o = np.argsort(pos)[::-1]; D = (L - np.nanmean(L, 1, keepdims=True))[:, o]
    return f, D, [pos[i] for i in o]
def stats(run):
    f, D, pos = load(run); lo = f < 3000
    bm = {fc: float(np.nanmax(abs(np.nanmean(D[sel(f, fc)], 0)))) for fc in TOB}
    tr = {fc: float(100 * np.mean(abs(D[sel(f, fc)]) <= tol(fc))) for fc in TOB}
    cells = np.concatenate([abs(D[sel(f, fc)]).ravel() <= tol(fc) for fc in TOB]); 
    return dict(f=f, D=D, pos=pos, score=rms(D[lo]), bm=bm, tr=tr, tone_all=float(100 * cells.mean()), bands=[rms(D[(f >= a) & (f < b)]) for a, b in [(250, 400), (400, 630), (630, 1000), (1000, 1600), (1600, 3000)]],
                ntones={fc: int(sel(f, fc).sum()) for fc in TOB})
A, W, T0, RR = stats(FINAL), stats(WORST), stats(START), stats(RERUN)
MARG = round(max(abs(RR['bm'][fc] - A['bm'][fc]) for fc in TOB) + .005, 2)     # day-to-day scatter of the band statistic
def verdict(st, fc):
    v = st['bm'][fc]; return 'marg' if abs(v - tol(fc)) <= MARG else ('pass' if v < tol(fc) else 'fail')
def cutoff(st):
    lo = None
    for fc in sorted(TOB, reverse=True):
        if verdict(st, fc) == 'fail': break
        lo = fc
    return lo
def count(st, k): return sum(verdict(st, fc) == k for fc in TOB)
CELL = {'pass': '#cfe0f3', 'marg': '#f3e6b3', 'fail': '#f0c4a8'}

# ---- figure A: the final configuration as a waterfall (position x tone map) with the band verdict strip
def fig_final():
    f, D, pos = A['f'], A['D'], A['pos']; lim = float(np.nanmax(abs(D)))
    fig = plt.figure(figsize=(7.2, 6.5)); gs = fig.add_gridspec(3, 3, height_ratios=[.55, 1, .05], width_ratios=[1, .018, .13], hspace=.5, wspace=.05, top=.94)
    ax = fig.add_subplot(gs[0, 0]); xs = np.arange(len(TOB))
    for i, fc in enumerate(TOB):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=CELL[verdict(A, fc)], ec='w', lw=1.5))
        ax.text(i + .5, .66, f'{A["bm"][fc]:.2f}', ha='center', va='center', fontsize=8, fontweight='bold')
        ax.text(i + .5, .30, f'±{tol(fc):g}', ha='center', va='center', fontsize=6.5, color='#46545c')
    ax.set_xlim(0, len(TOB)); ax.set_ylim(0, 1); ax.set_yticks([]); ax.set_xticks(xs + .5); ax.set_xticklabels([f'{fc}' for fc in TOB], fontsize=7)
    for s_ in ax.spines.values(): s_.set_visible(False)
    ax.tick_params(length=0); ax.set_xlabel('one-third-octave band centre (Hz)', fontsize=7)
    ax.set_title('Worst capsule vs arc mean per band (dB), against the ISO 3745 limit · orange = over, yellow = within ±%.2f of it' % MARG, fontsize=7.5, loc='left')
    a2 = fig.add_subplot(gs[1, 0]); xx = np.arange(len(f) + 1)
    im = a2.pcolormesh(xx, np.arange(len(pos) + 1), D.T, cmap='RdBu_r', vmin=-lim, vmax=lim)
    a2.set_yticks(np.arange(len(pos)) + .5); a2.set_yticklabels([f'{p:+.0f}°' for p in pos], fontsize=7); a2.invert_yaxis(); a2.axvline(np.searchsorted(f, 4000), color='k', lw=1.5)
    edges = [np.searchsorted(f, fc / 2 ** (1 / 6)) for fc in TOB if fc / 2 ** (1 / 6) > f[0]]
    for e in edges: a2.axvline(e, color='w', lw=.5, alpha=.7)
    tk = [i for i, q in enumerate(f) if any(abs(q - z) / z < .02 for z in [257, 400, 630, 1000, 1600, 2500, 6000])]
    a2.set_xticks([i + .5 for i in tk]); a2.set_xticklabels([f'{f[i]:.0f}' for i in tk], fontsize=7)
    a2.set_xlabel('Hz (95 tones; 3–5 kHz omitted, the sphere is not axisymmetric there) · +90° = top, −90° = bottom', fontsize=7)
    a2.set_title(f'Final configuration: level of each capsule vs the arc mean · room error below 3 kHz {A["score"]:.3f} dB', fontsize=7.5, loc='left')
    plt.colorbar(im, cax=fig.add_subplot(gs[1, 1])).set_label('dB vs arc mean', fontsize=7)
    m = fig.add_subplot(gs[1, 2]); lo = f < 3000
    m.barh(np.arange(len(pos)) + .5, [rms(D[lo][:, j]) for j in range(len(pos))], .75, color='#9ca3af'); m.set_ylim(len(pos), 0); m.set_yticks([])
    m.set_title('rms per capsule\n<3 kHz (dB)', fontsize=6.5); m.tick_params(labelsize=6.5); m.grid(axis='x', alpha=.3)
    fig.savefig(HERE + '/fig-final.png', dpi=200, bbox_inches='tight'); plt.close(fig)

def a4(src, dst):
    subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=pdfwrite', '-sPAPERSIZE=a4', '-dFIXEDMEDIA', '-dPDFFitPage', f'-sOutputFile={dst}', src], check=True)

def chromium(htmlfile, pdf):
    subprocess.run(['/snap/bin/chromium', '--headless', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', 'file://' + htmlfile], check=True, stderr=subprocess.DEVNULL)

CSS = '''@page{size:A4;margin:9mm 13mm} body{font-family:"IBM Plex Sans","DejaVu Sans",Arial,sans-serif;font-size:7.9pt;line-height:1.24;color:#10171b;margin:0}
h1{font-size:15pt;margin:0 0 1pt;letter-spacing:-.02em} h2{font-size:10pt;margin:7pt 0 3pt;padding-top:4pt;border-top:.7pt solid #c6d0d5} p{margin:0 0 3.5pt} ul{margin:0 0 3pt;padding-left:4.5mm} li{margin:0 0 2pt}
table{border-collapse:collapse;width:100%;margin:2pt 0 5pt;font-size:7.4pt} th{font-size:6.4pt;text-transform:uppercase;letter-spacing:.05em;color:#46545c;text-align:left;padding:2.5pt 3pt;border-bottom:1pt solid #10171b;vertical-align:bottom}
td{padding:2pt 3pt;border-bottom:.5pt solid #e0e6e9;vertical-align:top} td.num,th.num{font-family:"DejaVu Sans Mono",monospace;font-size:7pt;white-space:nowrap;text-align:right}
.tag{font-family:"DejaVu Sans Mono",monospace;font-size:6.3pt;color:#74828a} img{width:100%;display:block;margin:2pt auto} .box{background:#f1f4f6;border-left:2pt solid #17566e;padding:4pt 4mm;margin:4pt 0 5pt}
.q{border-left:1.5pt solid #17566e;padding:1pt 0 1pt 3mm;margin:2pt 0;font-size:7.4pt} .q span{display:block;font-family:"DejaVu Sans Mono",monospace;font-size:6pt;color:#74828a}
td.lst{font-family:"DejaVu Sans Mono",monospace;font-size:6.6pt;text-align:right;white-space:normal;width:22%}
.pass{background:#cfe0f3}.marg{background:#f3e6b3}.fail{background:#f0c4a8} b.w{color:#96382a}'''

def page1():
    d = A['score'] - W['score']
    box = (f"<b>Final configuration</b> (carpet-reordered, accepted by Adam): room error <b>{A['score']:.3f} dB</b> against <b>{W['score']:.3f} dB</b> for the worst bare room "
           f"({(A['score'] / W['score'] - 1) * 100:+.0f} %) and {T0['score']:.3f} for the untouched start. By the ISO 3745 test applied band by band it is "
           f"<b>qualified from the {cutoff(A)} Hz band up</b>; below that, {count(A, 'fail')} of 11 bands are clearly over the limit and {count(A, 'marg')} are marginal. "
           f"<b>Pure tones are qualified in no band</b>: {A['tone_all']:.0f} % of tone × capsule cells are inside the limit.")
    h = f'''<!doctype html><html><head><meta charset="utf-8"><title>Chamber final 1</title><style>{CSS}</style></head><body>
<h1>Chamber report — final configuration</h1><p class="tag">SoundVisualizer · 2026-10-01 · 11 calibrated UMIK-2 capsules on a 0.84 m arc · loudspeaker sphere on the axis · 95 tones, 257 Hz–6.35 kHz</p>
<div class="box">{box}</div>
<img src="fig-final.png">
<p class="tag">How to read: each cell of the map is one capsule at one tone; blue = quieter than the arc mean, red = louder. In an ideal free field every capsule would read the same, so the map would be white. The strip above gives, per band, the worst capsule's band-averaged deviation; the limits are the ISO 3745 anechoic ones (±1.5 dB to 630 Hz, ±1.0 dB from 800 Hz).</p>
<ul>
<li>Worst bands by room error: 250–400 Hz ({A['bands'][0]:.2f} dB) and 400–630 Hz ({A['bands'][1]:.2f}); best: 1–1.6 kHz ({A['bands'][3]:.2f}).</li>
<li>Reproducibility: the same configuration, re-measured on 2026-09-30, scores {RR['score']:.3f} (map differs by {rms(RR['D'][RR['f'] < 3000] - A['D'][A['f'] < 3000]):.2f} dB rms).</li>
</ul></body></html>'''
    open(HERE + '/_p1.html', 'w').write(h); chromium(HERE + '/_p1.html', HERE + '/_p1.pdf')

def page3():
    rows = ''
    for fc in TOB:
        rows += (f"<tr><td class='num'>{fc} Hz</td><td class='num'>±{tol(fc):g}</td><td class='num'>{A['ntones'][fc]}</td>"
                 f"<td class='num {verdict(W, fc)}'>{W['bm'][fc]:.2f}</td><td class='num'>{W['tr'][fc]:.0f} %</td>"
                 f"<td class='num {verdict(A, fc)}'>{A['bm'][fc]:.2f}</td><td class='num'>{A['tr'][fc]:.0f} %</td></tr>")
    lst = lambda st, k: ', '.join(str(fc) for fc in TOB if verdict(st, fc) == k) or '—'
    sc = lambda st: [f"{st['score']:.3f}", f"{cutoff(st)} Hz" if cutoff(st) else 'none', f"{count(st, 'fail')}: {lst(st, 'fail')} Hz", f"{count(st, 'marg')}: {lst(st, 'marg')} Hz", f"{st['tone_all']:.0f} %"]
    sw, sf, s0 = sc(W), sc(A), sc(T0)
    worse = [fc for fc in TOB if verdict(W, fc) != 'fail' and W['bm'][fc] < A['bm'][fc]] or [fc for fc in TOB if W['bm'][fc] < A['bm'][fc]]
    fixed = ', '.join(str(fc) for fc in TOB if verdict(T0, fc) == 'fail' and verdict(A, fc) != 'fail')
    broke = ', '.join(str(fc) for fc in TOB if verdict(A, fc) == 'fail' and verdict(T0, fc) != 'fail')
    names = ['Room error below 3 kHz (dB)', 'Band-level qualified from', 'Bands clearly over the limit (of 11)', 'Bands marginal', 'Pure-tone cells inside the limit']
    cl = lambda i: 'lst' if i in (2, 3) else 'num'
    card = ''.join(f"<tr><td>{n}</td><td class='{cl(i)}'>{sw[i]}</td><td class='{cl(i)}'>{s0[i]}</td><td class='{cl(i)}'><b>{sf[i]}</b></td></tr>" for i, n in enumerate(names))
    h = f'''<!doctype html><html><head><meta charset="utf-8"><title>Chamber final 3</title><style>{CSS}</style></head><body>
<h1>Evaluation by the method of the chamber papers</h1>
<p class="tag">SoundVisualizer · 2026-10-01 · 11 calibrated capsules on a 0.84 m arc · sphere on the axis · 95 tones, 257 Hz–6.35 kHz · page 1: waterfall comparison</p>
<div class="box"><b>Final configuration</b> (carpet-reordered, accepted): room error <b>{A['score']:.3f} dB</b> vs <b>{W['score']:.3f}</b> for the worst bare room ({(A['score'] / W['score'] - 1) * 100:+.0f} %) and {T0['score']:.3f} for the untouched start. Qualified (band level) from the <b>{cutoff(A)} Hz</b> band up; {count(A, 'fail')} of 11 bands over the limit, {count(A, 'marg')} marginal. <b>Pure tones qualified in no band.</b> Re-measured 2026-09-30: {RR['score']:.3f}.</div>
<h2 style="border:0;margin-top:3pt">The method</h2>
<p>Chambers are qualified one one-third-octave band at a time against the free-field ideal; the chamber is reported as qualified between two bands, its cut-off the lowest band above which everything passes, and noise and pure tones are reported separately.</p>
<div class="q">"TABLE I. Maximum allowable difference in anechoic rooms between measured and theoretical free-field levels per ISO 3745 and ANSI S12.35." <span>Cunefare et al. 2003, J. Acoust. Soc. Am. 113(2), p. 882 — ±1.5 dB up to 630 Hz, ±1.0 dB from 800 to 5000 Hz</span></div>
<div class="q">"semi-anechoic chamber is qualified with ISO 3745 on the 1/3 frequency band between 160 Hz- 4000 Hz. Cut-off frequency of the chamber is 160 Hz." <span>Kayhan 2008, METU thesis, p. 63</span></div>
<div class="q">"The chamber could satisfy the ISO tolerances when using random noise but failed to qualify when using pure tones." <span>Nash 2019, Proc. 23rd ICA, p. 1343</span></div>
<p><b>Our adaptation.</b> The standard compares a traversed microphone with 1/r; we have eleven fixed positions around an axisymmetric source, so the reference is the arc mean. <b>Band level:</b> each capsule's mean over the {A['ntones'][630]}–{A['ntones'][1000]} tones in the band; the worst capsule must be inside the limit. <b>Pure tones:</b> the share of single tone × capsule cells inside the limit. Within ±{MARG:.2f} dB of a limit is marginal: how far the statistic moved between the final configuration and its rerun five days later.</p>
<h2>Result, band by band (worst capsule, dB)</h2>
<table><thead><tr><th class="num">Band</th><th class="num">Limit</th><th class="num">Tones</th><th class="num">Worst bare room</th><th class="num">tones in limit</th><th class="num">Final configuration</th><th class="num">tones in limit</th></tr></thead><tbody>{rows}</tbody></table>
<p class="tag">The cut-off is set by the highest failing band, so one band can move it; read it together with the lists. Shading: blue = inside the limit, yellow = marginal, orange = over. Worst bare room = {WORST.split('/')[1]}: the wedges off, the flat foam base left — the nearest measured state to an empty room.</p>
<h2>Scorecard</h2>
<table><thead><tr><th>Measure</th><th class="num">Worst bare room</th><th class="num">Untouched start</th><th class="num">Final configuration</th></tr></thead><tbody>{card}</tbody></table>
<h2>Where that puts the chamber</h2>
<ul>
<li><b>Against the worst case:</b> room error {(1 - A['score'] / W['score']) * 100:.0f} % lower, bands clearly over the limit {count(W, 'fail')} → {count(A, 'fail')}, pure-tone cells inside the limit {W['tone_all']:.0f} → {A['tone_all']:.0f} %. The cut-off is the same, {cutoff(A)} Hz. Not better everywhere: at {', '.join(str(fc) for fc in worse)} Hz the bare room is the better one ({', '.join(f"{W['bm'][fc]:.2f} vs {A['bm'][fc]:.2f}" for fc in worse)}).</li>
<li><b>Against the untouched start:</b> no gain in the headline ({T0['score']:.3f} → {A['score']:.3f}) and the same number of failing bands ({count(T0, 'fail')}), in different places: the work fixed {fixed} Hz and broke {broke} Hz.</li>
<li><b>Against other chambers:</b> published small rotor chambers report cut-offs of 63–275 Hz (29 facilities, chamber-fighting-guide.pdf §01); METU, in the quote above, 160 Hz. Ours is the {cutoff(A)} Hz band, {cutoff(A) / 275:.0f}–{cutoff(A) / 63:.0f} times higher, by a test that is easier in one respect (a reference that is the arc mean, not the ideal) and harder in another (single worst capsule of eleven).</li>
</ul>
<h2>What the method cannot say</h2>
<ul>
<li>Deviation from the arc mean is blind to an error shared by all eleven positions; the ISO traverse has not been run here, so this ranks bands, it does not certify.</li>
<li>The grid starts at 257 Hz, above the 215–258 Hz blade tone, and the 250 Hz band has only {A['ntones'][250]} tones; 3–5 kHz is excluded (sphere), 5–6.4 kHz indicative. The scorecard compares whole setups: the source sits in a different position than at the start (tilt flipped on 25 Sep).</li>
</ul></body></html>'''
    open(HERE + '/_p3.html', 'w').write(h); chromium(HERE + '/_p3.html', HERE + '/_p3.pdf')

if __name__ == '__main__':
    subprocess.run([sys.executable, STEP, WORST, FINAL, 'Final configuration vs the empty floor (wedges off)', 'final-vs-worst'], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    a4(ROOT + '/docs/analysis/chamber-treatments-2026-09-23/final-vs-worst.pdf', HERE + '/_p2.pdf'); page3()
    subprocess.run(['pdfunite', HERE + '/_p2.pdf', HERE + '/_p3.pdf', HERE + '/CHAMBER-FINAL.pdf'], check=True)
    for x in ('_p3.html', '_p2.pdf', '_p3.pdf'): os.remove(HERE + '/' + x)
    for g in ('final-vs-worst.pdf', 'final-vs-worst.png'): os.remove(ROOT + '/docs/analysis/chamber-treatments-2026-09-23/' + g)
    print('final', A['score'], cutoff(A), count(A, 'fail'), count(A, 'marg'), round(A['tone_all']), '| worst', W['score'], cutoff(W), count(W, 'fail'), count(W, 'marg'), round(W['tone_all']), '| start', T0['score'], cutoff(T0), '| MARG', MARG)
