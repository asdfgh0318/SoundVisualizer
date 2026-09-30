"""build_summary.py — day-3 chamber summary: top-5 table, ISO-3745-analogue qualification, one A4 waterfall page per setup.

Run from the repo root:  .venv/bin/python docs/analysis/chamber-treatments-2026-09-23/build_summary.py
Writes SUMMARY-day3.{md,pdf} next to this file. Every number in them is computed here.
"""
import sys, os, subprocess, html
sys.path.insert(0, '.')
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from calibrator.rig import read_map

OUT = 'docs/analysis/chamber-treatments-2026-09-23/'
S = 'calibrator/sessions/'
BEST = '2026-09-25/cleanup-1'
# (short name, run, what it is — only what README.md states)
SETUPS = [
    ('last config', '2026-09-25/carpet-reordered',
     'Last configuration of day 3 (19:20): the full carpet on standoffs, layer order changed (bottom layer moved to the top).'),
    ('cleanup-1', '2026-09-25/cleanup-1',
     'BEST. The accepted state (speaker backed off 5 cm from the ring plane, raised thick carpet) with the loose felt sheets removed.'),
    ('backed-5cm', '2026-09-25/backed-5cm',
     'The accepted state: speaker backed off 5 cm from the ring plane, raised thick carpet.'),
    ('closer', '2026-09-25/closer-a',
     'Speaker moved ~20 cm closer to the ring, still on the axis; morning floor stack of day 3 (after the blue absorbing carpet was added). Repeat `closer-b` agrees to 0.006 dB.'),
    ('cleanup-2', '2026-09-25/cleanup-2',
     'The accepted state after more junk was removed (what, not stated).'),
]
RERUN = '2026-09-30/carpet-reordered-rerun'
BANDS6 = [(250, 400), (400, 630), (630, 1000), (1000, 1600), (1600, 3000)]
TOB = [250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500]
tol = lambda fc: 1.5 if fc <= 630 else 1.0            # ISO 3745 anechoic table, one-third-octave centres
rms = lambda x: float(np.sqrt(np.nanmean(np.asarray(x) ** 2)))
BETTER, WORSE, MUTED = '#2b6cb0', '#c05621', '#4b5563'


def load(run):
    f, pos, L, _ = read_map(S + run)
    f = np.asarray(f); L = np.asarray(L, float)
    return f, L - np.nanmean(L, 1, keepdims=True), pos


def sel(f, fc):
    return (f >= fc / 2 ** (1 / 6)) & (f < fc * 2 ** (1 / 6))


data = {n: load(r) for n, r, _ in SETUPS}
f0 = data['last config'][0]
rerun = load(RERUN)

# ---- coefficient: room error below 3 kHz, total and per band
score = {n: rms(D[f < 3000]) for n, (f, D, _) in data.items()}
perband = {n: [rms(D[(f >= a) & (f < b)]) for a, b in BANDS6] for n, (f, D, _) in data.items()}
def tilt_removed(D, pos):                      # remove each tone's best-fit top-to-bottom slope (linear in sin(elevation))
    s = np.sin(np.radians(np.asarray(pos, float))); s = s - s.mean()
    return D - np.outer((D @ s) / (s @ s), s)
def src(run):                                   # mean level <3 kHz (dB SPL) and mean tilt 400 Hz-3 kHz (+ = top louder)
    f, pos, L, _ = read_map(S + run); f = np.asarray(f); L = np.asarray(L, float)
    D = L - L.mean(1, keepdims=True); s = np.sin(np.radians(np.asarray(pos, float))); s = s - s.mean(); m = (f >= 400) & (f < 3000)
    return float(L[f < 3000].mean()), float(np.mean((D[m] @ s) / (s @ s)))
score_t = {n: rms(tilt_removed(D, pos)[f < 3000]) for n, (f, D, pos) in data.items()}
SRC = {k: src('2026-09-25/' + k) for k in ['cleanup-1', 'cleanup-2', 'cleanup-3', 'cleanup-6', 'carpet-removed', 'carpet-reordered']}
best_name = min(score, key=score.get)
assert best_name == 'cleanup-1', best_name

# ---- ISO 3745 analogue, per one-third-octave band
band_max, tone_rate = {}, {}
for n, (f, D, _) in data.items():
    for fc in TOB:
        m = sel(f, fc)
        band_max[n, fc] = float(np.nanmax(abs(np.nanmean(D[m], 0))))      # band level per capsule, worst capsule
        tone_rate[n, fc] = float(100 * np.mean(abs(D[m]) <= tol(fc)))     # share of tone x capsule cells in tolerance
ntones = {fc: int(sel(f0, fc).sum()) for fc in TOB}
# across-day scatter of the band statistic: last config vs its rerun 5 days later
fr, Dr, _ = rerun
scatter = max(abs(float(np.nanmax(abs(np.nanmean(Dr[sel(fr, fc)], 0)))) - band_max['last config', fc]) for fc in TOB)
MARG = round(scatter + 0.005, 2)


def verdict(n, fc):
    v = band_max[n, fc]
    if abs(v - tol(fc)) <= MARG: return 'marg'
    return 'pass' if v < tol(fc) else 'fail'


def cutoff(n):
    lo = None
    for fc in sorted(TOB, reverse=True):
        if verdict(n, fc) == 'fail': break
        lo = fc
    return lo


nfail = {fc: sum(verdict(n, fc) == 'fail' for n, _, _ in SETUPS) for fc in TOB}
fails_by_setup = {n: sum(verdict(n, fc) == 'fail' for fc in TOB) for n, _, _ in SETUPS}
tone_med = {fc: float(np.median([tone_rate[n, fc] for n, _, _ in SETUPS])) for fc in TOB}
nmarg = {fc: sum(verdict(n, fc) == 'marg' for n, _, _ in SETUPS) for fc in TOB}
tier = {fc: ('avoid' if nfail[fc] >= 3 else 'setup-dependent' if nfail[fc] >= 1 else 'borderline' if nmarg[fc] else 'holds') for fc in TOB}

# ---- figures --------------------------------------------------------------------------------
# 1. waterfall pages: the repo's step figure, each setup against the best one
for n, run, _ in SETUPS:
    if n == best_name: continue
    name = 'top5-' + n.replace(' ', '-')
    subprocess.run([sys.executable, OUT + 'build_step_figure.py', BEST, run, f'{n} vs best (cleanup-1)', name], check=True,
                   stdout=subprocess.DEVNULL)

# 2. the best one on its own (nothing to compare it with)
f, D, pos = data[best_name]; o = np.argsort(pos)[::-1]; Dp = D[:, o]; ps = [pos[i] for i in o]
fig = plt.figure(figsize=(12.5, 16.5), dpi=150)
gs = fig.add_gridspec(3, 3, height_ratios=[.75, 1, 1.1], width_ratios=[1, .018, .14], hspace=.45, wspace=.12, top=.92)
ax = fig.add_subplot(gs[0, 0])
BANDS7 = BANDS6 + [(5000, 6400)]
pb7 = perband[best_name] + [rms(D[(f >= 5000) & (f < 6400)])]
lab = [f'{a}–{b} Hz' for a, b in BANDS7]
ax.bar(range(len(BANDS7)), pb7, .5, color='#1f2328')
for i, v in enumerate(pb7): ax.text(i, v + .03, f'{v:.2f}', ha='center', fontsize=9)
ax.set_xticks(range(len(BANDS7))); ax.set_xticklabels(lab); ax.set_ylim(0, 2.2); ax.grid(axis='y', alpha=.3)
ax.set_ylabel('room error, rms dB across the arc\n(lower = flatter = better)')
ax.set_title('Room error per band', loc='left', fontsize=10)
a2 = fig.add_subplot(gs[1, 0]); lim = float(np.nanmax(abs(Dp)))
im = a2.pcolormesh(np.arange(len(f) + 1), np.arange(len(ps) + 1), Dp.T, cmap='RdBu_r', vmin=-lim, vmax=lim)
a2.set_yticks(np.arange(len(ps)) + .5); a2.set_yticklabels([f'{p:+.0f}°' for p in ps], fontsize=7); a2.invert_yaxis()
a2.axvline(np.searchsorted(f, 4000), color='k', lw=1.5)
tk = [i for i, q in enumerate(f) if any(abs(q - z) / z < .02 for z in [257, 400, 630, 1000, 1600, 2500, 5000, 6000])]
a2.set_xticks([i + .5 for i in tk]); a2.set_xticklabels([f'{f[i]:.0f}' for i in tk], fontsize=8)
a2.set_title(f'cleanup-1 — {score[best_name]:.3f} dB below 3 kHz', loc='left', fontsize=10)
a2.set_xlabel('Hz (3–5 kHz omitted: the sphere is not axisymmetric there). +90° = top, −90° = bottom')
plt.colorbar(im, cax=fig.add_subplot(gs[1, 1])).set_label('dB vs arc mean', fontsize=8)
m = fig.add_subplot(gs[1, 2]); m.barh(np.arange(len(ps)) + .5, [rms(D[f < 3000][:, o][:, j]) for j in range(len(ps))], .75, color='#9ca3af')
m.set_ylim(len(ps), 0); m.set_yticks([]); m.set_title('rms per capsule\n<3 kHz (dB)', fontsize=7.5); m.tick_params(labelsize=7); m.grid(axis='x', alpha=.3)
fig.suptitle(f'Best of day 3: cleanup-1 — room error below 3 kHz {score[best_name]:.3f} dB (reference for the other pages)',
             x=.01, y=.975, ha='left', fontsize=12, fontweight='bold')
fig.text(.01, .95, '2026-09-25/cleanup-1 · 95 tones · 11 calibrated capsules · the four pages that follow it are drawn against this map',
         fontsize=8.5, color=MUTED)
fig.savefig(OUT + 'top5-cleanup-1.pdf'); plt.close(fig)

# 3. qualification matrix
names = [n for n, _, _ in SETUPS]
fig, (a, b) = plt.subplots(1, 2, figsize=(8.27, 5.4), dpi=170, gridspec_kw=dict(wspace=.08))
cm = {'pass': '#cfe0f3', 'marg': '#f3e6b3', 'fail': '#f0c4a8'}
for j, n in enumerate(names):
    for i, fc in enumerate(TOB):
        a.add_patch(plt.Rectangle((j, i), 1, 1, color=cm[verdict(n, fc)], ec='w', lw=1.5))
        a.text(j + .5, i + .5, f'{band_max[n, fc]:.2f}', ha='center', va='center', fontsize=8)
        v = tone_rate[n, fc]
        b.add_patch(plt.Rectangle((j, i), 1, 1, color=plt.cm.Blues(.08 + .55 * v / 100), ec='w', lw=1.5))
        b.text(j + .5, i + .5, f'{v:.0f}', ha='center', va='center', fontsize=8)
for ax_ in (a, b):
    ax_.set_xlim(0, len(names)); ax_.set_ylim(len(TOB), 0)
    ax_.set_xticks(np.arange(len(names)) + .5); ax_.set_xticklabels(names, fontsize=7.5, rotation=25, ha='right')
    for s_ in ax_.spines.values(): s_.set_visible(False)
    ax_.tick_params(length=0)
a.set_yticks(np.arange(len(TOB)) + .5)
a.set_yticklabels([f'{fc} Hz  ±{tol(fc):g}  ({ntones[fc]} tones)' for fc in TOB], fontsize=7.5)
b.set_yticks([])
a.set_title('Band level: worst capsule vs arc mean (dB)\norange = over the ISO 3745 limit, yellow = within ±%.2f of it' % MARG, fontsize=8, loc='left')
b.set_title('Pure tones: % of tone×capsule cells\ninside the limit', fontsize=8, loc='left')
fig.savefig(OUT + 'top5-qualification.png', bbox_inches='tight'); plt.close(fig)

# ---- A4 scaling of the figure pages -----------------------------------------------------------
def a4(src, dst):
    subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=pdfwrite', '-sPAPERSIZE=a4', '-dFIXEDMEDIA', '-dPDFFitPage',
                    f'-sOutputFile={dst}', src], check=True)

pages = []
for n, _, _ in SETUPS:
    src = OUT + ('top5-cleanup-1.pdf' if n == best_name else 'top5-' + n.replace(' ', '-') + '.pdf')
    dst = OUT + '_a4-' + os.path.basename(src)
    a4(src, dst); pages.append(dst)

# ---- text pages -------------------------------------------------------------------------------
E = html.escape
rows = ''
for n, run, what in SETUPS:
    pb = ''.join(f'<td class="num">{v:.2f}</td>' for v in perband[n])
    d = score[n] - score[best_name]
    co = cutoff(n); co_txt = f'{co} Hz' + ('*' if verdict(n, co) == 'marg' else '')
    rows += (f'<tr><td><b>{E(n)}</b><br><span class="tag">{E(run)}</span></td><td class="num big">{score[n]:.3f}</td>'
             f'<td class="num">{"—" if n == best_name else f"{d:+.3f}"}</td><td class="num">{score_t[n]:.3f}</td>{pb}'
             f'<td class="num">{co_txt}</td><td class="num">{fails_by_setup[n]}</td></tr>'
             f'<tr class="desc"><td colspan="11">{E(what)}</td></tr>')
tiers = ''
for fc in TOB:
    tiers += (f'<tr><td class="num">{fc} Hz</td><td class="num">±{tol(fc):g}</td><td class="num">{ntones[fc]}</td>'
              f'<td class="num">{nfail[fc]} clear + {nmarg[fc]} marginal</td><td class="num">{tone_med[fc]:.0f} %</td><td><b class="{tier[fc].split("-")[0]}">{tier[fc]}</b></td></tr>')
top4 = [score[n] for n in names if n != 'last config']
spread4 = max(top4) - min(top4)
avoid = [fc for fc in TOB if tier[fc] == 'avoid']
holds = [fc for fc in TOB if tier[fc] == 'holds']
border = [fc for fc in TOB if tier[fc] == 'borderline']
dep = [fc for fc in TOB if tier[fc] == 'setup-dependent']
worst_tone = min(TOB, key=lambda fc: tone_med[fc])
LAB6 = [f'{a}–{b}' for a, b in BANDS6]
def grp(fn):
    g = {}
    for n in names: g.setdefault(LAB6[fn(perband[n])], []).append(n)
    return '; '.join(f"{k} Hz: {', '.join(v)}" for k, v in g.items())
worst_txt, best_txt = grp(lambda v: int(np.argmax(v))), grp(lambda v: int(np.argmin(v)))
fails_txt = ', '.join(f'{n} {fails_by_setup[n]}' for n in names)
dep_txt = '; '.join(f"{fc} Hz fails only in {', '.join(n for n in names if verdict(n, fc) == 'fail')}" for fc in dep)
marg_txt = ', '.join(f'{n} at {fc} Hz' for n in names for fc in TOB if verdict(n, fc) == 'marg')
rr = rms(rerun[1][rerun[0] < 3000])

CSS = '''
@page { size:A4; margin:12mm 13mm; }
body{font-family:"IBM Plex Sans","DejaVu Sans",Arial,sans-serif;font-size:8.2pt;line-height:1.27;color:#10171b;margin:0}
h1{font-size:16pt;margin:0 0 2pt;letter-spacing:-.02em} h2{font-size:10.5pt;margin:9pt 0 3pt;border-top:.7pt solid #c6d0d5;padding-top:5pt}
p{margin:0 0 4pt} table{border-collapse:collapse;width:100%;margin:3pt 0 6pt;font-size:7.6pt}
th{font-size:6.6pt;text-transform:uppercase;letter-spacing:.05em;color:#46545c;text-align:left;padding:3pt 3pt;border-bottom:1pt solid #10171b;vertical-align:bottom}
td{padding:2.4pt 3pt;border-bottom:.5pt solid #e0e6e9;vertical-align:top} td.num{font-family:"IBM Plex Mono","DejaVu Sans Mono",monospace;font-size:7.2pt;white-space:nowrap}
td.big{font-size:9pt;font-weight:700} tr.desc td{font-size:7pt;color:#46545c;padding-top:0;border-bottom:.5pt solid #c6d0d5}
.tag{font-family:"DejaVu Sans Mono",monospace;font-size:6.3pt;color:#74828a} ul{margin:0 0 4pt;padding-left:4.5mm} li{margin:0 0 2.2pt}
.avoid{color:#96382a}.holds{color:#2f6b3a}.borderline{color:#4b6a2f}.setup{color:#8f5c0d} .pb{break-before:page} img{width:84%;display:block;margin:0 auto}
.box{background:#f1f4f6;border-left:2pt solid #17566e;padding:4pt 4mm;margin:4pt 0 6pt}
'''
html_doc = f'''<!doctype html><html><head><meta charset="utf-8"><title>Chamber summary day 3</title><style>{CSS}</style></head><body>
<h1>Chamber findings — day 3, top 5 setups</h1>
<p class="tag">2026-09-25 (+ rerun 2026-09-30) · 95 tones 257 Hz–6.35 kHz, 3–5 kHz omitted · 11 calibrated capsules · sphere on the axis, arc vertical</p>
<div class="box"><b>Coefficient</b> = room error below 3 kHz: rms over all tones and capsules of each capsule's level relative to the arc mean, dB, lower is flatter.
Repeat floor 0.01 dB, handling ~0.04 dB, so <b>the top four are tied</b> (span {spread4:.3f} dB). The last config is {score['last config']-score[best_name]:.3f} dB behind, <b>but that is the source, not the carpet</b>: fitting out each map's top-to-bottom slope†, it scores {score_t['last config']:.3f} against {score_t[best_name]:.3f} for cleanup-1.
Today's rerun of the last config scored {rr:.3f} ({rr-score['last config']:+.3f}): consistent with the chamber still being in that state at 15:48.</div>
<table><thead><tr><th>Setup</th><th>Room error<br>&lt;3 kHz</th><th>vs best</th><th>Tilt<br>removed†</th><th>250–400</th><th>400–630</th><th>630–1k</th><th>1–1.6k</th><th>1.6–3k</th><th>Qualified<br>from*</th><th>Bands<br>failed*</th></tr></thead><tbody>{rows}</tbody></table>
<p class="tag">†Per tone, the best-fit line in sin(elevation) across the eleven capsules is subtracted before scoring; this removes a tilted or shifted source, not a room effect. *ISO 3745 analogue on band levels, section 2. "Qualified from" = the lowest one-third-octave band from which no band up to 2.5 kHz is clearly over the limit (the way METU and others state a cut-off); * = that band is marginal. "Bands failed" is out of 11.</p>
<ul>
<li>The single coefficient ranks cleanup-1 first, but it hides <i>where</i> the error is. Bands clearly over the limit, of 11: {fails_txt}. Closer and cleanup-2 are the cleanest by that count although they score 0.01 dB behind.</li>
<li>Worst band: {worst_txt}. Best band: {best_txt}.</li>
<li><b>The source moved between cleanup-1 and the last config, in two steps.</b> At cleanup-3 (16:20, some junk put back) the mean level rose {SRC['cleanup-3'][0]-SRC['cleanup-1'][0]:+.2f} dB and never came back (cleanup-6: {SRC['cleanup-6'][0]-SRC['cleanup-1'][0]:+.2f}). At carpet-removed (17:23) the level fell to {SRC['carpet-removed'][0]-SRC['cleanup-1'][0]:+.2f} dB and the tilt at 400 Hz–3 kHz flipped from top-louder ({SRC['cleanup-6'][1]:+.2f} dB per unit sin(el) at cleanup-6; cleanup-1 {SRC['cleanup-1'][1]:+.2f}) to bottom-louder ({SRC['carpet-removed'][1]:+.2f}); the last config sits at {SRC['carpet-reordered'][1]:+.2f}. The likely cause is the tripod standing on the floor stack (README, day 3): the sphere itself was not measured.</li>
<li>Different floors: closer was measured on the morning stack of day 3, the rest on later stacks. Across days the map drifts 0.1–0.2 dB even when the score does not.</li>
</ul>
<h2 class="pb" style="border:0;margin-top:0">2. Which frequencies to avoid</h2>
<p><b>Rule, taken from how chambers are qualified.</b> ISO 3745 compares the level at each one-third-octave band with the ideal and allows ±1.5 dB up to 630 Hz and ±1.0 dB from 800 Hz to 5 kHz (the same table in six independent papers). A chamber is then reported as qualified between two bands, with the lowest one its cut-off. Nash 2019 found a chamber that passed with random noise and failed with pure tones, so both are reported here.</p>
<p><b>What we changed.</b> ISO compares a microphone traverse with the inverse-square law. We have eleven fixed positions and an axisymmetric source, so the reference is the arc mean. Two tests per band: <b>band level</b> (each capsule's mean over the ~8 tones in the band; worst capsule against the limit) and <b>pure tones</b> (share of individual tone×capsule cells inside the limit). Band verdicts within ±{MARG:.2f} dB of the limit are marked marginal: that is how far the same statistic moved between the last config and its rerun.</p>
<img src="top5-qualification.png">
<table><thead><tr><th>Band</th><th>Limit dB</th><th>Tones</th><th>Setups over the limit (band level), of 5</th><th>Pure tones in limit, median</th><th>Verdict</th></tr></thead><tbody>{tiers}</tbody></table>
<p class="tag">avoid = clearly over the limit in 3 or more of the 5 setups; marginal cases are {marg_txt}.<br> setup-dependent = 1–2; borderline = none clearly over but some marginal; holds = neither. These cut-offs are ours, not from a standard.</p>
<ul>
<li><b>Avoid:</b> {", ".join(str(x) for x in avoid)} Hz. <b>Clean in all five:</b> {", ".join(str(x) for x in holds)} Hz. <b>Borderline</b> (no clear failure, but at least one setup within the scatter of the limit): {", ".join(str(x) for x in border)} Hz. <b>Depends on the setup:</b> {", ".join(str(x) for x in dep)} Hz ({dep_txt}).</li>
<li><b>Pure tones are not qualified anywhere.</b> No band has all cells inside the limit; the median is {min(tone_med.values()):.0f}–{max(tone_med[fc] for fc in TOB if ntones[fc] > 3):.0f} %, lowest at {worst_tone} Hz.</li>
<li><b>Never usable:</b> 3–5 kHz (the sphere's rocking mode, a source fault). <b>Indicative only:</b> 5–6.4 kHz. <b>Not measured:</b> below 257 Hz, where blade tones sat at 216 and 238 Hz (and 258 Hz) in the September runs, and the 250 Hz band has only {ntones[250]} tones.</li>
</ul>
<p><b>Limits of this rule.</b> Deviation from the arc mean cannot see an error shared by all eleven positions, such as a uniform reflection. Band verdicts hinge on the single worst of eleven capsules. The tolerance table belongs to a traverse test we never ran; treat the verdicts as a ranking of bands, not a certificate.</p>
</body></html>'''
open(OUT + '_summary.html', 'w').write(html_doc)
subprocess.run(['/snap/bin/chromium', '--headless', '--disable-gpu', '--no-pdf-header-footer',
                f'--print-to-pdf={os.path.abspath(OUT)}/_summary.pdf', 'file://' + os.path.abspath(OUT) + '/_summary.html'],
               check=True, stderr=subprocess.DEVNULL)
subprocess.run(['pdfunite', OUT + '_summary.pdf'] + pages + [OUT + 'SUMMARY-day3.pdf'], check=True)

# ---- markdown list ---------------------------------------------------------------------------
md = ['# Chamber findings, day 3 — top 5 setups', '',
      'Coefficient = room error below 3 kHz (rms dB across the arc vs arc mean; lower = flatter). Repeat 0.01 dB, handling ~0.04 dB. '
      f'Rerun of the last config on 2026-09-30: {rr:.3f}.', '',
      '| # | setup | run | room error | vs best | tilt removed | ' + ' | '.join(f'{a}–{b}' for a, b in BANDS6) + ' | qualified from | bands failed /11 |',
      '|---|---|---|---|---|---|' + '---|' * (len(BANDS6) + 2)]
for i, (n, run, what) in enumerate(SETUPS, 1):
    md.append(f'| {i} | {n} | `{run}` | **{score[n]:.3f}** | {"—" if n == best_name else f"{score[n]-score[best_name]:+.3f}"} | {score_t[n]:.3f} | '
              + ' | '.join(f'{v:.2f}' for v in perband[n]) + f" | {cutoff(n)} Hz{'*' if verdict(n, cutoff(n)) == 'marg' else ''} | {fails_by_setup[n]} |")
md += ['', *[f'- **{n}** — {what}' for n, _, what in SETUPS], '',
       '`*` = the cut-off band is marginal (within the day-to-day scatter of the limit).', '',
       f'**The last config\'s deficit is the source, not the carpet:** with each map\'s top-to-bottom tilt fitted out it scores {score_t["last config"]:.3f} vs {score_t[best_name]:.3f} for cleanup-1. The source moved at cleanup-3 (level {SRC["cleanup-3"][0]-SRC["cleanup-1"][0]:+.2f} dB, 16:20) and at carpet-removed (tilt {SRC["cleanup-6"][1]:+.2f} → {SRC["carpet-removed"][1]:+.2f}, 17:23); it was not put back.', '',
       f'Top four are tied (span {spread4:.3f} dB). Setup 1 is the last config of the day; the waterfall page for each is in `SUMMARY-day3.pdf` (A4), drawn against cleanup-1.', '',
       '## Bands (ISO 3745 analogue: ±1.5 dB to 630 Hz, ±1.0 dB from 800 Hz; reference = arc mean)', '',
       '| band | limit | tones | setups over the limit, of 5 | pure tones in limit, median | verdict |', '|---|---|---|---|---|---|']
md += [f'| {fc} Hz | ±{tol(fc):g} | {ntones[fc]} | {nfail[fc]} clear + {nmarg[fc]} marginal | {tone_med[fc]:.0f} % | {tier[fc]} |' for fc in TOB]
md += ['', f'- Avoid: {", ".join(map(str, avoid))} Hz. Clean in all five: {", ".join(map(str, holds))} Hz. Borderline: {", ".join(map(str, border))} Hz. Setup-dependent: {", ".join(map(str, dep))} Hz.',
       '- Pure tones are not qualified in any band. 3–5 kHz never usable (sphere); 5–6.4 kHz indicative; below 257 Hz not measured.',
       f'- Marginal = within ±{MARG:.2f} dB of the limit (the last config vs its rerun scatter). "avoid/depends/holds" thresholds are ours, not from a standard.']
open(OUT + 'SUMMARY-day3.md', 'w').write('\n'.join(md) + '\n')
for p in pages + [OUT + '_summary.pdf', OUT + '_summary.html']: os.remove(p)
print('score', {k: round(v, 3) for k, v in score.items()}, 'MARG', MARG)
print('cutoffs', {n: cutoff(n) for n in names}, 'fails', fails_by_setup)
print('tiers', tier)
for g in ['top5-*.pdf', 'top5-*.png']:
    import glob
    for x in glob.glob(OUT + g): os.remove(x)
