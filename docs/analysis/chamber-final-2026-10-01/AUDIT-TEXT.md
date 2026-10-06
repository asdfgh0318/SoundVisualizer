# Text audit: CHAMBER-FINAL.pdf (6 pages)

Audited 2026-10-06 against `build_final.py` (the source of every string quoted here), the rendered PDF
(`pdftotext -layout`, plain `pdftotext`, page images at 70 and 160 dpi), the session data (numbers recomputed
read-only by importing `build_final.py`) and the held text dumps of the cited papers and standard previews.
No repo file other than this one was changed.

**Authority.** This audit is derived from the PDF and `build_final.py` as they stood on 2026-10-06. If either
changes, re-check the affected items. Where this file and the session data disagree, the data govern.

Page numbers below are PDF pages:
p1 microphones (ch. 1) · p2 photo (2.1) · p3 waterfall (2.2) · p4 evaluation (2.3) · p5 polars (ch. 3) · p6 solutions (ch. 4).

## Counts

| Category | Count |
|---|---|
| W: wrong or contradictory (text vs table, figure, data or source) | 12 |
| M: misleading, overclaiming, undefined or unsourced | 24 |
| S: style, terminology, layout | 24 |
| A: meaning-preserving plain-language replacements (section 3) | 44 |
| F: meaning-changing corrections (section 4, each needs Adam's OK) | 16 |

Cross-reference check: every page reference is correct as the PDF now stands. "page 4" (p3) points to the
caveat on p4. "quoted on page 6" (p4) points to the Cunefare quote on p6. "page 1" (p5) points to ch. 1. "the
next page" (p2) points to the waterfall on p3. There is no "previous page" left in the text. Chapter numbers 1-4
have no gaps or repeats.

---

## 1. Findings, by severity

### W: wrong or contradictory

**W1 · p5 · drawn or not drawn.**
Quote (bullet 2): "(The 2 Sep curves are not drawn; the table carries them.)"
Quote (corrections table): "prop11–17 (prop15–17 drawn)".
Problem: the bullet says the 2 Sep curves are not drawn, and the table says prop15–17 are drawn. The bullet is
right: `fig_polar()` draws only 31 Aug and 30 Sep. "The table carries them" is also wrong. No table holds the
prop15/16/17 rms spreads (1.79/1.78/2.25 and 1.18/1.29/1.30 dB). The table holds the cell share of the ten 1–2 Sep runs.
Fix: F1.

**W2 · p5 · "level with 30 Sep" and "little from the room".**
Quote: "the same 1–2 Sep captures re-read with today's corrections give 71 % (65–79), which is level with 30 Sep. The absolute change is real; most of it comes from the calibration, little from the room."
Problem: 30 Sep reads 66.1 %. The corrected 1–2 Sep median is 70.9 %, so 30 Sep sits 4.8 points below it, at the
bottom of the 65–79 range. Read with the same calibration, 30 Sep is *not* rounder. The calibration accounts for
+9.4 points (61.5 → 70.9). The rest of the change between the two sets is −4.8 points, not "little". The project notes
say the same thing ("not rounder than the 2 Sep runs at the same operating point (66 % vs median 71 %, range 65–79)").
Fix: F2.

**W3 · p4 · the box misdescribes the deviation columns.**
Quote: "The deviation columns show the worst microphone's band mean, as a share of the limit."
Problem: the "Day 3 start" and "Final" columns print the worst capsule's band-mean deviation **in dB**
(for example 6.81, 1.88). Only the **colour** is the share of the limit (`grad(G['bm'][fc] / tol(fc))`).
Fix: F3.

**W4 · p4 · "8–9 tones in the band".**
Quote: "Band level = each capsule's mean over the 8–9 tones in the band".
Problem: the table on the same page shows 3 tones in the 250 Hz band, and the box gives the 250 Hz example
with 3 tones. The text takes its range from `F['ntones'][630]`–`F['ntones'][1000]`, which skips the 250 Hz band.
Fix: F4.

**W5 · p4 + p6 · "from the 2000 Hz band up".**
Quotes: "Within the tolerance values from (band) … 2000 Hz" (p4). "within the strict anechoic tolerance values from the 2000 Hz band up" (p6).
Problem: the evaluation stops at the 2500 Hz band (`TOB`). 3–5 kHz is excluded and 5–6.35 kHz is not
evaluated. "From 2000 Hz up" therefore claims bands that were never tested. What the data support is
"the 2000 and 2500 Hz bands pass (the highest bands evaluated)". The same applies to "1250 Hz" for day 3.
Fix: F5.

**W6 · p6 · Orrego cost rule.**
Quote: "cost about ×4 per octave down (Orrego et al. 2018, p. 477)".
Problem: the source (journal p. 477) reads: "frequency is intended, e.g 100 Hz, the cost per square meter would increase in approximately four times." The chamber was designed for 400 Hz, so ×4 is for **two** octaves (400 → 100 Hz), not for one.
Fix: F6.

**W7 · p6 · Ma 2022 paraphrase.**
Quote: "Removing the floor treatment costs ~3 dB broadband and up to 10 dB at the blade tone (Ma et al. 2022, p. 7)."
Problem: in the source the 3 dB is the deviation of the overall level (OASPL) from 1/R decay in the
hemi-anechoic configuration ("the deviations can reach as large as 3 dB"). The 10 dB is the difference between
**two adjacent microphones** at the BPF with the reflecting floor ("At the BPF … the difference in the measured SPL
can be as significant as 10 dB"). Neither is "the cost of removing the floor treatment". Both passages are on PDF
page 8 of the held dump; check that the printed page is 7.
Fix: F7.

**W8 · p6 · gate length against reflector path.**
Quote: "250 Hz needs 1.37 m (gate ≥5 ms, Matelján, ARTA note 4)".
Problem: a 1.37 m extra path is 4.0 ms (1.37/343), and 1/4.0 ms = 250 Hz. The "≥5 ms" is Matelján's general
recommendation ("the gate length should be 5ms or more"), not the gate that 1.37 m gives. Put side by side, the two
numbers disagree.
Fix: F8.

**W9 · p4 vs p6 · two map-change numbers for the same kind of event.**
Quotes: "0.14 for a re-arranged carpet" (p4). "the 24 Sep flip by 0.12" (p6).
Problem: both are re-arrangements of the 24 Sep carpet. Recomputed: chaotic-carpet → chaotic-carpet-2 is 0.143 dB,
and chaotic-carpet-2 → chaotic-carpet-3 is 0.116 dB. The p4 value is hard-coded and does not name its pair, so the
reader sees 0.14 and 0.12 for what looks like the same thing.
Fix: F9.

**W10 · p1 vs p5 · "roughness 3.3 → 1.0 dB".**
Quote (p1): "On the 30 Sep prop-plane polar the corrections cut the roughness from 3.3 to 1.0 dB."
Problem: "roughness" is not defined, and this report does not compute it (it comes from
`baseline-story-2026-09-30`). On p5 the same 30 Sep polar has an rms spread of 1.45 dB and 1.39 dB with the
corrections, which neither 1.0 nor 3.3 matches. A reader will see two contradictory numbers for one polar.
Fix: F10.

**W11 · p1 · "The change is a per-capsule offset".**
Problem: the corrections changed each calibration curve in offset **and** shape (project notes: "Corrections went
entirely into `cal.gain_db` (offset and shape)"). The bottom row of the p1 figure shows changes that vary with
frequency, most clearly at −54°. "Mainly a per-capsule offset" is accurate.
Fix: F11.

**W12 · p5 · "the only propeller capture that has them".**
Problem: the four felt-duct bases of 30 Sep (18:44–19:01) were also taken after 16 Sep, so they carry the
corrections too. The claim holds only for this report.
Fix: F12.

### M: misleading, overclaiming, undefined or unsourced

**M1 · p4 · "tones and noise separately".** The method paragraph lists "tones and noise separately" as taken from the standards. This evaluation has no noise signal: both measures come from the 95 stepped tones, and "band level" (the mean of the tones in a band) stands in for the noise test. Say so (F13).

**M2 · p4 · the 250 Hz band is only partly covered.** The band spans about 223–281 Hz, and the grid starts at 257 Hz, so only 3 tones in its upper part are used. This is the band with the largest failure (6.81 dB), and the table does not mention the partial coverage (F4 adds it).

**M3 · p4 · the critical caveat is in the smallest type.** "Caveat: the source was moved between these runs …" is set in the 6.3 pt grey `tag` style, the least visible text on the page, while the bottom ~40 % of the page is empty. Set it in body type or in a `.box`.

**M4 · p4 · caveat may be incomplete.** The caveat lists two deliberate moves (13:44, 14:03). The project notes say that later on 25 Sep "the speaker's tripod stood on the floor stack, so floor changes moved the source". If that already applied between 14:03 and 19:15 (the floor runs `full-carpet-raised` … `carpet-reordered`), the caveat should say so. Adam to confirm. No text change is proposed until then.

**M5 · p2 · photo labelled as `carpet-reordered`.** The photo was taken on 5 Oct, after the 25 Sep clean-up runs (`cleanup-1…6`) and after the 30 Sep propeller session. It shows the propeller rig at the hub, while `carpet-reordered` was a loudspeaker run. "The chamber in the final configuration (`carpet-reordered`)" needs a qualifier, for example "floor and walls as in `carpet-reordered`". Adam to confirm what changed.

**M6 · p5 · "so 30 Sep is the smoothest".** Only the 30 Sep curve carries the corrections, and p1 and the reference row show that the corrections alone lower the spread. The sentence reads as a chamber result. Add the calibration caveat at that point (F14).

**M7 · p5 · "cell" means two different things.** On p3/p4 a cell is one tone × one capsule. In the p5 table ("cells within ±1.3 dB", "worst cell") a cell is one capsule × one third-octave band, and the bullet then calls the same quantity "the worst capsule". Rename it on p5 (A30, A31).

**M8 · p5 · "worst cell" for the multi-run rows.** For the 10-run and 5-run rows the value is the **median over runs** of each run's worst deviation (`worst=np.median(a[:, 1])`). The header does not say so (F15).

**M9 · p5 · the ±1.3 dB threshold is not explained.** It comes from the arc-validation analysis ("±1.3 dB in 84 % of cells"). The report gives no reason for it. Add a source or a one-line reason.

**M10 · p5 · the operating point of 30 Sep is not in the table.** The 1–2 Sep and 31 Aug rows give V/A/N. The 30 Sep row gives none, so the reader cannot see whether 1–2 Sep is "the same operating point". The project notes give 11.7 V, 5.8 A, −3.4 N for 30 Sep against 11.65 V, 7.3 A, −4.0 N for 1–2 Sep. The currents differ by about 25 %.

**M11 · p5 · the polar figure has no caption.** It is not stated anywhere near the figure that the left half mirrors the right half, that the angle is the capsule elevation, which calibration each curve uses, or that the radial axes differ (30–76 against 50–80 dB SPL). The 31 Aug curve lies about 10 dB above 30 Sep at low frequency because of its other operating point. Without a caption it reads as "30 Sep is quieter". A20 adds the mirroring and PWM explanation.

**M12 · p5 · 31 Aug set.** Five of the six 31 Aug bases are used (`-4` is left out without a reason). The project notes mark the 31 Aug flat-arc captures as orientation unknown ("[H ?]"), so the up/down labelling of the 31 Aug polar is not established. The roundness statistic does not depend on it, but the drawn curve does.

**M13 · p1 · two "spread" numbers.** "The spread across the eleven … fell from 4.01 dB to 0.02 dB" (bench, same sound, one mounting point) and "the span … 4.3 → 0.8 dB" (in the room, includes the room) appear four lines apart with no explanation of why they differ. Add one sentence: the 0.02 dB is at a single mounting point, and the 0.8 dB includes the room (F16).

**M14 · p1 · "room error" is used before it is defined.** It first appears in the p1 caption ("Room error below 3 kHz changes 2.277 → 1.997"). It is defined only implicitly, in the p3 bar-chart axis label. A6 defines it on first use.

**M15 · p6 · row 3, "What the papers give".** "Tones are where a modal room hurts most; a pattern that changes over a 19 % frequency step averages out over a speed ladder" is the project's own reasoning (19 % is 216 → 258 Hz from our runs), but it sits in the literature column with no citation. Move it to "What we already know" or cite it.

**M16 · p6 · "(kr)² ≈ 15 at 250 Hz, above 3".** The arithmetic is right (k = 4.58 m⁻¹, r = 0.84 m, (kr)² = 14.8), but no source is given for the criterion "3".

**M17 · p6 · "Needs a reference run in a chamber (the university's 300 m³)".** No source and no name are given for the 300 m³ chamber.

**M18 · p6 · "Valid for a fixed source and fixed microphones … not for a flying drone".** The project notes attribute this to Rasmussen 2022, but no citation appears in the table.

**M19 · p6 · "the polar shape of 30 Sep depends on speed outside 1.3–2 kHz".** No number or figure in the report supports it. Add a pointer to the baseline-story report or remove it.

**M20 · p6 · "Order", item 4: "the surfaces the sweep names".** No sweep appears anywhere in this report. It is an orphan reference to an earlier plan. Item 3, "Loudspeaker correction", is solution 2 under another name.

**M21 · p6 · Cunefare quote.** The quote is only a table title ("TABLE I. Maximum allowable difference …"). It does not show the ±1.5/±1.0 dB values that p4 cites it for, so it is not evidence for those values. Quote a row of the table, or call it a pointer to the table.

**M22 · p6 · "Yes, the strongest." and "Source position was the largest lever".** These are evaluative claims with no stated basis of comparison. The second compares runs across a source move, which also includes handling (≈0.04 dB, small here). Use "most effective option in the papers" with its residual (<0.55 dB) as the basis.

**M23 · p4 vs p3 · margin against handling.** A band within ±0.03 dB of the limit is "marginal" (largest same-day repeat difference). p3 states that handling costs about 0.04 dB. A band 0.035 dB from the limit is therefore called a clear pass or fail although handling alone could move it. This is a threshold choice; state it, or use the handling figure.

**M24 · whole report · authority statements.** Only p1 has one ("Numbers from the project notes (CLAUDE.md …), which govern"). Pages 2–6 mix computed numbers with hard-coded ones (0.14, 0.80, 20 cm, 13:44, 14:03, 0.68/1.49 m, 215–258 Hz, 713 Hz, 19 %, 8 dB, 1.3–2 kHz, all operating points) and give no statement of which source governs. The chamber-treatment write-up (`docs/analysis/chamber-treatments-2026-09-23/README.md`) is declared governing in the project notes, but the report never mentions it. Pointing a supervisor to "CLAUDE.md" is also odd: call it "the project notes (CLAUDE.md in the repository)".

### S: style, terminology, layout

**S1 · p1 · overlapping figure titles.** The two bottom-row panel titles ("effect of the correction: closer to the arc mean (blue) or further (orange)") run into each other between the columns and cannot be read. The bottom colour-bar label ("change in deviation from the arc mean (dB)") also runs above its axis. Shorten the titles (A42).

**S2 · p1 · caption covers only two of three rows.** It explains "factory files (top) and corrections (middle)" but not the bottom row. A6 fixes this.

**S3 · units and ticks are inconsistent between figures.** p1 ticks are "0.26k … 6k" (kHz). p3 ticks are "257, 397, 1587, 5040, 5993" (Hz, non-nominal). The text mixes "100–10000 Hz", "315 Hz–8 kHz" and "1.3–2 kHz". Pick one convention: Hz below 1 kHz and kHz above, with nominal band labels.

**S4 · decimals for the same quantity differ.** The same quantity is printed as "2.054 → 1.317" on p4 and "2.05 → 1.32" on p6. The other room-error values (1.997, 1.387) use 3 decimals, while p6 also has "1.96 to 1.31". In the p5 table, PWM 2000 has 1 decimal (66.1 %) and PWM 1900 has 0 (72 %). The limit is "±1" in the table and "±1.0 dB" in the text.

**S5 · minus signs.** U+2212 (−) and ASCII hyphen are mixed. The p6 flips print "-4.3", "-4.1" (`{:+.1f}`). The y-axis labels on p1 and p3 print "-18°", "-90°", and also "+0°". The p3 bars print "-1.33". The text uses "−72°".

**S6 · "6.4 kHz" vs "6.35 kHz".** The grid ends at 6.35 kHz (p4 tag). p3 and p6 say "5–6.4 kHz" / "5000–6400 Hz".

**S7 · stale "today".** p5 has "30 Sep, today" and "today's corrections" (twice). The report is dated 5 Oct, and the corrections are from 16 Sep.

**S8 · same thing, different names.**
- Microphone: capsule / microphone / mic / position. p4 says "worst capsule" in the text, "worst microphone's" in the box and "11 microphones" in the example.
- Final run: final / final configuration / accepted configuration / `carpet-reordered` / Final.
- Calibration: corrections / measured corrections / corrected files / corrected microphones / today's corrections.
- Flat arc: horizontal / arc flat.
- 30 Sep geometry: prop plane / prop-plane / propeller plane.
- Loudspeaker: source / speaker / loudspeaker / sphere.
- Limits: ISO limit / tolerance values / anechoic row / anechoic table / limit.
- Spread measures: spread / span / roughness / rms spread / room error.
- Cut-off: "cut-off" (tag) vs "Within the tolerance values from (band)" (row).
- Empty floor: "empty floor" (p4) vs "wedges off" (p6).
- Two-state change: "switch" vs "flip".
- Arc vs ring.
Define each once and use one word (A3, A4, A6 and the A-list do this).

**S9 · undefined abbreviations and symbols.** BPF (p6, used as "2.2 × BPF"), PWM (p5, p6), rms (p1), sd (p1), SPL, λ, k and r in (kr)², D<sub>A</sub>, H<sub>m</sub>, WS2F/WS3F, "prop". The definitions of D<sub>A</sub> and H<sub>m</sub> were checked against the held ISO 5305 preview: D<sub>A</sub> is the UAS diameter, the "diameter of the smallest cylinder that encompasses the projection shape" of the UAS, and H<sub>m</sub> is the distance of each microphone "to the walls, floor, and ceiling (or the wedge tips)".

**S10 · first person.** First person appears in "What we did with the microphones", "Ours, not the standards'", "We have eleven fixed capsules", "our trials", "our arc", "our gate", "We keep the strict row", "What we already know", "Applies to us?". A report would use the impersonal form. The A-list removes these.

**S11 · informal phrases and flourishes.**
- Informal: "Yes, first, free.", "Yes, cheap.", "Sets the ceiling for everything else", "largest lever", "where a modal room hurts most", "Good for naming", "did nothing", "The absolute change is real".
- "not X but Y" constructions: "it moves rows, not the frequency structure", "ranks bands and does not certify". These are acceptable where they carry a caveat; they are kept in the A-list as plain statements.
- Em-dash aside: "— our arc —".
- Rhetorical question as heading: "is the prop-plane polar rounder than before?". It is acceptable, but the answer (no, once calibration is matched) must then be stated plainly (F2).

**S12 · heading hierarchy.**
- Only chapter 2 has numbered sub-sections (2.1–2.3), and they are set in grey, lower-case `tag` type rather than as headings.
- The chapter 2 h1 is repeated on three pages and says "waterfalls" (plural) though there is one waterfall.
- "The method" (p4) is an h2 without the rule line that every other h2 has.
- Chapters 1, 3 and 4 have unnumbered h2s.
- There is no report title, author or date block. The PDF opens on "1 · What we did with the microphones". The only date is in the p1 tag ("chamber report, 2026-10-05").

**S13 · "0: — Hz".** The p4 "Bands marginal" cell for day 3 prints "0: — Hz". `lst()` returns "—" and " Hz" is appended anyway.

**S14 · table units.** The p4 "Limit", "Day 3 start" and "Final" columns have no unit (dB). A13 adds them.

**S15 · p5 table header.** The first header cell is a long upper-case sentence that wraps to two lines and is hard to read. A30 shortens it.

**S16 · citations are inconsistent.**
- Orrego et al. 2018 is cited as "p. 477" (journal page) and "p. 6" (PDF page); in journal pages that is p. 476.
- Nash 2019 and Long 2020 have no page. Kayhan has no year (2008).
- Bellmann & Klippel and Matelján have no year (both undated documents; write "n.d.").
- "Matelján": the held document and file name spell it "Mateljan"; check the accent.
- Cunefare et al. is given in full twice (p4 and p6).

**S17 · internal file names cited as sources.** "Source: chamber-fighting-guide.pdf §03, 29 facilities" (p6) and "CLAUDE.md" (p1) are repository files that the intended reader cannot find without a path. Give `docs/acoustic-speculations/chamber-fighting-guide.pdf`. Note that the project notes warn that documents in `acoustic-speculations/` are not tied to our chamber.

**S18 · p1 "1 l sphere".** "1 l" reads as "11" in this font. Write "1-litre".

**S19 · p1 "seat" and "datum".** Both are jargon. Write "mounting point" and "reference level" (A3, A5).

**S20 · p4 method paragraph.** It runs to 11 lines with stacked clauses, a nested citation in parentheses, and clause numbers dumped mid-sentence. A12 splits it into four short paragraphs.

**S21 · p6 two-state-switch bullet.** It is one 8-line bullet with three "not X (…)" clauses in parentheses. A40 splits it.

**S22 · p6 "63–275 Hz rotor chambers".** The reader is not told that 63–275 Hz are cut-off frequencies (A38).

**S23 · p3 text comes from another script.** The p3 figure title, sub-title ("492 of 946 cells moved >0.05 dB toward flat"), the "repeat floor 0.010, handling ~0.04" and the upper-case "BETTER or WORSE" come from `chamber-treatments-2026-09-23/build_step_figure.py`, not from `build_final.py`. It uses "cell" before p4 defines it, and "(worst)" is unexplained (day3-a 1.997 is the worst of day 3; its repeat day3-b reads 1.996). Fix that script, or define "cell" on p3 (A10 does).

**S24 · documents around the report are out of date** (not report text). The `build_final.py` docstring still says "2-page chamber report", "Page 1 and the page-2 table", and calls chaotic-carpet-2 a "repeat" where the report says "three arrangements". The project notes call the PDF a "Three-page chamber report"; it has 6 pages.

---

## 2. Ten most important findings

1. W1: p5 says the 2 Sep curves are not drawn and that the table carries them. The corrections table says prop15–17 are drawn. Both statements are wrong in some way.
2. W2: p5 calls corrected 1–2 Sep (71 %) "level with" 30 Sep (66 %). With matched calibration, 30 Sep is 4.8 points less round, not "little from the room".
3. W3: the p4 box says the deviation columns are "a share of the limit". They are dB values; only the colour is a share.
4. W5: "within the tolerance values from the 2000 Hz band up" claims bands above 2500 Hz that were never evaluated.
5. W4/M2: "8–9 tones in the band" contradicts the 3-tone 250 Hz band on the same page, and that band is only partly covered (the grid starts at 257 Hz).
6. W10: p1 "roughness 3.3 → 1.0 dB" is undefined and not computed here, and it conflicts with the p5 rms spreads of 1.45/1.39 dB for the same polar.
7. W6/W7: the Orrego "×4 per octave" is ×4 for two octaves, and the Ma 2022 "3 dB / 10 dB from removing the floor treatment" are different quantities in the source.
8. M3/M4: the source-moved caveat on p4 is in the smallest grey type, and it may omit the tripod-on-floor-stack drift (Adam to confirm).
9. M7/M8: "cell" means tone × capsule on p3/p4 and capsule × band on p5, and the p5 "worst cell" is a median over runs without saying so.
10. M24/S12: there is no report title or authority block, and pages 2–6 contain hard-coded numbers with no statement of which source governs.

---

## 3. A-list: plain-language replacements (meaning unchanged)

Apply with exact string replacement in `build_final.py`. Every number, unit, date, run name, citation and f-string
placeholder is kept as in OLD. "Meaning: unchanged" means the same claims, now split into shorter sentences or with
a term defined. Where an entry also adds a definition taken from elsewhere in the report or the project notes, it says
so. Apply the A-list first, then section 4. Where a section-4 fix touches the same text, its OLD is written against
the A-list NEW.

**A1 · p1 · Meaning: unchanged**
OLD: `<h1>1 · What we did with the microphones: substitution calibration</h1>`
NEW: `<h1>1 · Microphone calibration by substitution</h1>`

**A2 · p1 · Meaning: unchanged (defines "hub")**
OLD: `<b>The source</b>: a printed 1 l sphere with an 8 cm driver, at the hub.`
NEW: `<b>The test loudspeaker</b>: a printed 1-litre sphere with an 8 cm driver, placed at the hub (the centre of the ring).`

**A3 · p1 · Meaning: unchanged (defines capsule, ring size from p4, substitution calibration)**
OLD:
```
<p>Eleven UMIK-2 capsules sit on the 1.68 m ring. Their factory calibration files were never checked against each other, so on 16 Sep every capsule was measured against every other at one seat (55 pairs, 12 tones per octave). At one seat the source and the room are the same for both capsules, so their difference is the capsule.</p>
```
NEW:
```
<p>Eleven UMIK-2 measurement microphones, called <i>capsules</i> in this report, sit on a ring of 1.68 m diameter (0.84 m radius). Each came with a factory calibration file, and these files had never been checked against each other. On 16 Sep every capsule was therefore compared with every other capsule in the same mounting point (55 pairs, 12 tones per octave). This is a substitution calibration. In one mounting point the loudspeaker and the room are the same for both capsules, so any difference between the two readings comes from the capsules.</p>
```

**A4 · p1 · Meaning: unchanged**
OLD: `<ul><li><b>Seven of the eleven factory files were wrong by 0.6–3.6 dB</b>, clustered by serial prefix.</li>`
NEW: `<ul><li><b>Seven of the eleven factory files were wrong by 0.6–3.6 dB.</b> The errors are grouped by serial-number prefix.</li>`

**A5 · p1 · Meaning: unchanged (defines "corrections" and "factory files")**
OLD: `<li>The corrections went into each capsule's calibration curve. The spread across the eleven, for the same sound, fell from <b>4.01 dB to 0.02 dB</b>. Repeatability of the method: 0.08 dB sd.</li>`
NEW: `<li>The measured differences were added to each capsule's calibration curve. The updated curves are called the <i>corrections</i>; the original curves are the <i>factory files</i>. For the same sound, the spread of the eleven readings fell from <b>4.01 dB to 0.02 dB</b>. Repeated measurements agreed to 0.08 dB (standard deviation).</li>`

**A6 · p1 · Meaning: unchanged**
OLD: `<li>The datum is the four capsules whose files agree with measurement. Still open: the absolute level, which needs a 94 dB calibrator.</li>`
NEW: `<li>The reference level is set by the four capsules whose factory files agree with the measurement. Still open: the absolute level, which needs a 94 dB sound calibrator.</li>`

**A7 · p1 · Meaning: unchanged (W10 still applies, see F10)**
OLD: `<li>On the 30 Sep prop-plane polar the corrections cut the roughness from 3.3 to 1.0 dB.</li></ul></div></div>`
NEW: `<li>On the 30 Sep propeller-plane polar (chapter 3), the corrections reduced the roughness from 3.3 to 1.0 dB.</li></ul></div></div>`

**A8 · p1 · (OLD contains the literal escapes \u201c / \u201d as in the source) Meaning: unchanged (defines arc mean, span, room error; explains the three rows; W11 still applies, see F11)**
OLD:
```
<p>Same two captures, calibrated two ways: the factory files (top) and the measured corrections (middle); \u201cspan\u201d is the range of the capsules' mean levels. The factory files add a different offset to each capsule, which shows up as horizontal stripes across every frequency; the span of the capsules' mean levels is <b>{R[0][6]:.1f} → {R[0][7]:.1f} dB</b> at the start of day 3 and <b>{R[1][6]:.1f} → {R[1][7]:.1f} dB</b> in the final configuration. Room error below 3 kHz changes <b>{R[0][4]:.3f} → {R[0][5]:.3f} dB</b> and <b>{R[1][4]:.3f} → {R[1][5]:.3f} dB</b>. The change is a per-capsule offset, so it moves rows, not the frequency structure of the room; every room-error number elsewhere in this report uses the corrected files.</p>
```
NEW:
```
<p><b>How to read the figure.</b> Each map is one capture. Rows are capsule positions, columns are tones, and the colour is the capsule's level minus the mean of all eleven (the <i>arc mean</i>). Left: the start of day 3 (<code>day3-a</code>, 25 Sep). Right: the final configuration (<code>carpet-reordered</code>). Top row: read with the factory files. Middle row: read with the corrections. Bottom row: the effect of the correction. The factory files give each capsule a different offset, which shows up as horizontal stripes across every frequency. The <i>span</i> is the range of the capsules' mean levels. It changes from <b>{R[0][6]:.1f} → {R[0][7]:.1f} dB</b> at the start of day 3 and <b>{R[1][6]:.1f} → {R[1][7]:.1f} dB</b> in the final configuration. The <i>room error</i> is the rms deviation of the capsules from the arc mean, below 3 kHz. It changes <b>{R[0][4]:.3f} → {R[0][5]:.3f} dB</b> and <b>{R[1][4]:.3f} → {R[1][5]:.3f} dB</b>. The change is a per-capsule offset. It therefore moves whole rows and leaves the frequency pattern of the room in place. Every room-error number elsewhere in this report uses the corrected files.</p>
```

**A9 · p1 · Meaning: unchanged**
OLD: `<p class="tag">Numbers from the project notes (CLAUDE.md, calibrator session 2026-09-16), which govern where this page and they differ.</p>`
NEW: `<p class="tag">The numbers on this page come from the project notes (CLAUDE.md in the repository) and the calibrator session of 2026-09-16. Where this page and the notes differ, the notes govern.</p>`

**A10 · p2, p3, p4 · Meaning: unchanged (one waterfall). Replace all 3 occurrences.**
OLD: `2 · Main waterfalls and the day 3 evaluation`
NEW: `2 · Main waterfall and the day 3 evaluation`

**A11 · p2 · Meaning: unchanged**
OLD: `<p class="tag" style="margin:0">2.1 the chamber</p>`
NEW: `<p class="tag" style="margin:0">2.1 The chamber</p>`

**A12 · p2 · Meaning: unchanged (M5 still applies)**
OLD:
```
<p style="margin:0"><b>The chamber in the final configuration</b> (<code>carpet-reordered</code>, photographed 5 Oct): the arc ring laid flat around the propeller rig at the hub, the speaker tripod on the left, batting on the floor and ceiling, wedges and lined pillars on the walls. The waterfall on the next page compares the start of day 3 with this state.</p>
```
NEW:
```
<p style="margin:0"><b>The chamber in the final configuration</b> (<code>carpet-reordered</code>, photographed 5 Oct). The microphone ring lies flat around the propeller rig at the hub. The loudspeaker tripod stands on the left. Batting covers the floor and the ceiling; wedges and lined pillars line the walls. The waterfall on the next page compares the start of day 3 with this state.</p>
```

**A13 · p3 · Meaning: unchanged (defines "day 3" from the project notes; defines "cell" for the figure)**
OLD:
```
<h1>2 · Main waterfalls and the day 3 evaluation</h1><p class="tag" style="margin:0 0 2pt">2.2 main waterfall: day 3 start against the final state</p>
<p style="margin:0 0 3pt">Both runs are from 25 Sep with the corrected microphones. The source was moved between them (page 4).</p>
```
(If A10 has already been applied, the h1 reads "Main waterfall".)
NEW:
```
<h1>2 · Main waterfall and the day 3 evaluation</h1><p class="tag" style="margin:0 0 2pt">2.2 Main waterfall: start of day 3 against the final state</p>
<p style="margin:0 0 3pt">Both runs were taken on 25 Sep (day 3 of the chamber treatments, 23–25 Sep) and are read with the corrections. The loudspeaker was moved between the two runs (see the caveat on page 4). A <i>cell</i> in the figure is one tone at one capsule.</p>
```

**A14 · p4 · Meaning: unchanged**
OLD: `<p class="tag" style="margin:0 0 2pt">2.3 evaluation against the ISO anechoic tolerance values (an analogue, not a qualification)</p>`
NEW: `<p class="tag" style="margin:0 0 2pt">2.3 Evaluation against the ISO anechoic tolerance values (an analogue, not a qualification)</p>`

**A15 · p4 · Meaning: unchanged**
OLD: `<p class="tag">11 calibrated capsules on a 0.84 m arc · 95 tones`
NEW: `<p class="tag">11 calibrated capsules on an arc of 0.84 m radius · 95 tones`

**A16 · p4 · Meaning: unchanged (W4 and M1 are fixed separately, in F4 and F13)**
OLD: the whole paragraph that starts `<p><b>Where the method comes from.</b>` and ends `ISO 26101-1 and ISO 5305.</p>`.
NEW:
```
<p><b>Taken from the standards.</b> Each one-third-octave band is judged on its own against the free-field ideal. Tones and noise are judged separately. In each band the worst position is compared with the limit. The limits are the anechoic tolerance values: ±1.5 dB for 125–630 Hz and ±1.0 dB for 800–5000 Hz (ISO 5305:2024 Table 1, p. 8). Cunefare et al. 2003 give the same values (J. Acoust. Soc. Am. 113(2), p. 882; quoted on page 6). ISO 3745:2012 and ISO 26101 are the two qualification procedures; Russo et al. 2018 compare them.</p>
<p><b>Specific to this rig, not taken from the standards.</b> The standards move one microphone along a line away from the source (a traverse) and test how the level falls with distance. Only that test allows a room to be called "qualified" or "in conformity" (ISO 26101-1 p. 3; ISO 3745 §5.1). This rig has eleven fixed capsules at one radius. It tests how uniform the level is around a source that radiates the same way in every direction about its axis. The reference is therefore the arc mean, and the same tolerance values are applied to a different quantity.</p>
<p><b>The two measures.</b> <i>Band level</i>: for each capsule, the mean deviation over the {F['ntones'][630]}–{F['ntones'][1000]} tones in the band; the worst capsule is compared with the limit. <i>Pure tones</i>: the share of tone × capsule cells inside the limit. A band within ±{MARG:.2f} dB of its limit is called <i>marginal</i>. This margin is the largest difference found between two runs of one unchanged state on the same day ({len(REPEATS)} pairs).</p>
<p><b>What the result means.</b> The room is treated, not qualified. The result is a figure of merit that ranks the bands. It claims neither qualification nor conformity. The standards were available as previews only: ISO 3745:2012 (clauses 1–6.1.2, no annexes), ISO 26101-1 and ISO 5305.</p>
```

**A17 · p4 · Meaning: unchanged (W3 is fixed in F3)**
OLD: `<b>Cell = one tone × one microphone.</b> "Cells in limit" counts these, e.g. 250 Hz: 3 tones × 11 microphones = 33 cells, 12 inside ±1.5 dB = 36 %. The deviation columns show the worst microphone's band mean, as a share of the limit.</p>`
NEW: `<b>Cell = one tone at one capsule.</b> "Cells in limit" is the share of cells inside the limit. Example, 250 Hz at the start of day 3: 3 tones × 11 capsules = 33 cells; 12 are inside ±1.5 dB, which is 36 %. The deviation columns show the worst capsule's band mean, as a share of the limit.</p>`

**A18 · p4 · Meaning: unchanged (adds units)**
OLD: `<table><thead><tr><th class="num">Band</th><th class="num">Limit</th><th class="num">Tones (× 11 capsules)</th><th class="num">Day 3 start</th><th class="num">cells in limit</th><th class="num">Final</th><th class="num">cells in limit</th></tr></thead>`
NEW: `<table><thead><tr><th class="num">Band</th><th class="num">Limit (dB)</th><th class="num">Tones (× 11 capsules)</th><th class="num">Day 3 start (dB)</th><th class="num">Cells in limit</th><th class="num">Final (dB)</th><th class="num">Cells in limit</th></tr></thead>`

**A19 · p4 · Meaning: unchanged (W5 is fixed in F5)**
OLD: `names = ['Room error below 3 kHz (dB)', 'Within the tolerance values from (band)', 'Bands clearly over the limit (of 11)', 'Bands marginal', 'Tone × capsule cells inside the limit']`
NEW: `names = ['Room error below 3 kHz (dB)', 'Inside the tolerance values from this band up', 'Bands clearly over the limit (of 11)', 'Bands marginal (of 11)', 'Cells inside the limit, all bands']`

**A20 · p4 · Meaning: unchanged (W9 is fixed in F9; also consider body type for the caveat, M3)**
OLD: the whole `<p class="tag">Colour = worst-capsule deviation … ({C['score']:.3f} / {C2['score']:.3f} / {C3['score']:.3f}).</p>`
NEW:
```
<p class="tag"><b>Colour.</b> Deviation columns: the worst capsule's deviation as a share of the band's limit (green 0, yellow at the limit, red at twice the limit or more). Cells-in-limit columns: green 100 %, yellow 50 %, red 0 %. The "from this band up" row is set by the highest failing band, so read it together with the two lists below it.</p>
<p class="box" style="margin:2pt 0 1pt;padding:2pt 4mm;font-size:7.2pt"><b>Caveat: the source was moved between these two runs.</b> It was moved 20 cm closer at 13:44 and into the ring plane at 14:03. The map changed by {MCg:.2f} dB rms. For comparison, a re-arranged carpet changed it by 0.14 dB and a 5 cm source move by 0.80 dB. The gain therefore combines the treatments and the source positions. The one pair with an unmoved source is from 24 Sep: empty floor {F['score']:.3f} → carpet {C['score']:.3f} (three carpet arrangements: {C['score']:.3f} / {C2['score']:.3f} / {C3['score']:.3f}).</p>
```

**A21 · p5 · Meaning: unchanged. Keep the `mk` prefix "3 · Polars" intact; it is used to split the page.**
OLD: `3 · Polars: is the prop-plane polar rounder than before?</h1>`
NEW: `3 · Polars: is the propeller-plane polar rounder than before?</h1>`

**A22 · p5 · Meaning: unchanged (renames "cell" here to avoid the clash in M7; M8 is fixed in F15)**
OLD: `<th>Tone-notched broadband, 315 Hz–8 kHz, cells within ±1.3 dB of the polar mean</th><th class="num">Runs</th><th class="num">PWM 2000: median (range)</th><th class="num">worst cell</th>`
NEW: `<th>Capsule × band values within ±1.3 dB of the polar mean (broadband, tones removed, 315 Hz–8 kHz)</th><th class="num">Runs</th><th class="num">PWM 2000: median (range)</th><th class="num">Worst deviation</th>`

**A23 · p5 · Meaning: unchanged (stale "today"; the operating point is from bullet 1)**
OLD: `<tr><td><b>30 Sep, today</b></td>`
NEW: `<tr><td><b>30 Sep</b> (11.7 V), corrections</td>`

**A24 · p5 · Meaning: unchanged**
OLD: `<tr><td>1–2 Sep, arc flat (11.65 V, 7.3 A, −4.0 N), factory files as measured</td>`
NEW: `<tr><td>1–2 Sep, arc laid flat (11.65 V, 7.3 A, −4.0 N), factory files</td>`

**A25 · p5 · Meaning: unchanged**
OLD: `<tr><td>31 Aug (7.35 V, 13.8 A, +6 N: other operating point), factory files as measured</td>`
NEW: `<tr><td>31 Aug, arc laid flat (7.35 V, 13.8 A, +6 N: other operating point), factory files</td>`

**A26 · p5 · Meaning: unchanged**
OLD: `<tr><td class="tag">for reference: 1–2 Sep re-read with today's corrections</td>`
NEW: `<tr><td class="tag">for reference: 1–2 Sep re-read with the 16 Sep corrections</td>`

**A27 · p5 · Meaning: unchanged (adds the mirroring and PWM definitions)**
OLD:
```
<li><b>As the app's Polar tab draws it</b> (total level in the band, PWM 2000, recomputed from the data). <b>Each capture is read with the calibration that existed when it was taken</b>: the factory files for 31 Aug and 1–2 Sep, the measured corrections for 30 Sep. The "before" curve is the 31 Aug horizontal baseline, an earlier baseline at another operating point (7.35 V against 11.7 V), not a controlled pair.</li>
```
NEW:
```
<li><b>The figure</b> draws the polars the way the app's Polar tab does. It shows the total level in the band at each capsule, at PWM 2000 (the motor throttle signal, 2000 µs), recomputed from the data. The angle is the capsule's position on the arc; the left half mirrors the right half. <b>Each capture is read with the calibration that existed when it was taken</b>: the factory files for 31 Aug and 1–2 Sep, the corrections for 30 Sep. The "before" curve is the 31 Aug baseline with the arc laid flat. It was taken at another operating point (7.35 V against 11.7 V), so the two curves are not a controlled pair.</li>
```

**A28 · p5 · Meaning: unchanged (W1 is fixed in F1, M6 in F14)**
OLD:
```
<li><b>20–560 Hz</b>, the low end with the blade tone at about 238 Hz: rms spread of the total level {F1['sa']:.2f} dB on 30 Sep, against {F1['sb']:.2f} dB on 31 Aug and {F1['ss'][0]:.2f} / {F1['ss'][1]:.2f} / {F1['ss'][2]:.2f} dB on 2 Sep (prop15 / 16 / 17), so 30 Sep is the smoothest. <b>100–10000 Hz:</b> {F2['sa']:.2f} dB on 30 Sep, {F2['sb']:.2f} dB on 31 Aug, {F2['ss'][0]:.2f} / {F2['ss'][1]:.2f} / {F2['ss'][2]:.2f} dB on 2 Sep: here the 2 Sep runs are slightly smoother than 30 Sep. (The 2 Sep curves are not drawn; the table carries them.)</li>
```
NEW:
```
<li><b>20–560 Hz</b> is the low end; it contains the blade-passing tone at about 238 Hz. The rms spread of the total level across the capsules is {F1['sa']:.2f} dB on 30 Sep, {F1['sb']:.2f} dB on 31 Aug and {F1['ss'][0]:.2f} / {F1['ss'][1]:.2f} / {F1['ss'][2]:.2f} dB on 2 Sep (prop15 / 16 / 17). In this band 30 Sep has the smallest spread. <b>100–10000 Hz:</b> {F2['sa']:.2f} dB on 30 Sep, {F2['sb']:.2f} dB on 31 Aug and {F2['ss'][0]:.2f} / {F2['ss'][1]:.2f} / {F2['ss'][2]:.2f} dB on 2 Sep. In this band the 2 Sep runs have a slightly smaller spread than 30 Sep. (The 2 Sep curves are not drawn; the table carries them.)</li>
```

**A29 · p5 · Meaning: unchanged (W2 is fixed in F2)**
OLD:
```
<li><b>Tone-notched broadband, 315 Hz–8 kHz</b> (table): 30 Sep has {T['med']:.0f} % of cells within ±1.3 dB, against a median of {Sp['med']:.0f} % for 1–2 Sep ({Sp['lo']:.0f}–{Sp['hi']:.0f}) and {Au['med']:.0f} % for 31 Aug ({Au['lo']:.0f}–{Au['hi']:.0f}); the worst capsule is {T['worst']:.1f} dB off the mean against {Sp['worst']:.1f} and {Au['worst']:.1f} dB. Part of this is the microphone correction: the same 1–2 Sep captures re-read with today's corrections give {Sc['med']:.0f} % ({Sc['lo']:.0f}–{Sc['hi']:.0f}), which is level with 30 Sep. The absolute change is real; most of it comes from the calibration, little from the room.</li>
```
NEW:
```
<li><b>Broadband with the tones removed, 315 Hz–8 kHz</b> (table). The level is taken in one-third-octave bands with the propeller tones cut out. On 30 Sep, {T['med']:.0f} % of the capsule × band values lie within ±1.3 dB of the polar mean. The median is {Sp['med']:.0f} % for 1–2 Sep (range {Sp['lo']:.0f}–{Sp['hi']:.0f}) and {Au['med']:.0f} % for 31 Aug (range {Au['lo']:.0f}–{Au['hi']:.0f}). The worst capsule is {T['worst']:.1f} dB off the mean on 30 Sep, against {Sp['worst']:.1f} and {Au['worst']:.1f} dB. Part of this difference is the microphone correction. The same 1–2 Sep captures, re-read with the 16 Sep corrections, give {Sc['med']:.0f} % (range {Sc['lo']:.0f}–{Sc['hi']:.0f}), which is level with 30 Sep. The absolute change is real; most of it comes from the calibration, little from the room.</li>
```

**A30 · p5 · Meaning: unchanged (W12 is fixed in F12)**
OLD: `<tr><td>30 Sep prop-plane baseline</td><td>30 Sep, after the 16 Sep substitution calibration</td><td><b>measured corrections</b> (the only propeller capture that has them)</td></tr></tbody></table>`
NEW: `<tr><td>30 Sep propeller-plane baseline</td><td>30 Sep, after the 16 Sep substitution calibration</td><td><b>corrections</b> (the only propeller capture that has them)</td></tr></tbody></table>`

**A31 · p5 · Meaning: unchanged**
OLD: `<p class="tag">The corrections were measured on 16 Sep (page 1). The earlier captures are shown as they were taken; the reference row in the table above re-reads 1–2 Sep with the corrections to show how much of the gain is calibration.</p>`
NEW: `<p class="tag">The corrections were measured on 16 Sep (page 1). The earlier captures are shown as they were taken. The reference row of the table above re-reads 1–2 Sep with the corrections, to show how much of the gain comes from the calibration.</p>`

**A32 · p6 · Meaning: unchanged (defines BPF; gives the path of the source document)**
OLD: `<p class="tag">What fails (accepted configuration, evaluated on its own): clearly over the ISO limit at {lst(X, 'fail')} Hz, marginal at {lst(X, 'marg')} Hz; the blade tone sits at 215–258 Hz and its third harmonic at 713 Hz. Nearest reflectors measured: extra path 0.68 m at −72° and 1.49 m at +36°/+54°, i.e. 1.98 and 4.34 ms. Source: chamber-fighting-guide.pdf §03, 29 facilities.</p>`
NEW: `<p class="tag"><b>What fails in the final configuration</b> (<code>carpet-reordered</code>, evaluated on its own): clearly over the limit at {lst(X, 'fail')} Hz; marginal at {lst(X, 'marg')} Hz. The blade-passing frequency (BPF, the blade tone) lies at 215–258 Hz; its third harmonic is at 713 Hz. The nearest measured reflections travel 0.68 m further than the direct sound at −72° and 1.49 m further at +36°/+54°, so they arrive 1.98 ms and 4.34 ms after it. Source of the table: docs/acoustic-speculations/chamber-fighting-guide.pdf, §03 (29 facilities).</p>`

**A33 · p6 · Meaning: unchanged**
OLD: `<table><thead><tr><th>Solution</th><th>What the papers give</th><th>Applies to us?</th><th>What we already know</th></tr></thead><tbody>`
NEW: `<table><thead><tr><th>Solution</th><th>What the papers give</th><th>Applies here?</th><th>What the trials show</th></tr></thead><tbody>`

**A34 · p6 · row 1 · Meaning: unchanged (W8 is fixed in F8)**
OLD: `<tr><td><b>1. Move the geometry</b> (source, arc, reflector)</td><td>Sets the ceiling for everything else. Reaching 500 Hz needs every reflector ≥0.69 m of extra path, 250 Hz needs 1.37 m (gate ≥5 ms, Matelján, ARTA note 4).</td><td><b>Yes, first, free.</b> The 0.68 m surface is just short for 500 Hz.</td><td>Source position was the largest lever in our trials: moving the speaker about 20 cm closer took the room error from {B3['score']:.2f} to {CL['score']:.2f} dB within one afternoon (25 Sep).</td></tr>`
NEW: `<tr><td><b>1. Change the geometry</b> (move the source, the arc or the reflecting object)</td><td>Limits what every other measure can reach. To work down to 500 Hz, every reflection must travel at least 0.69 m further than the direct sound; for 250 Hz, 1.37 m (gate ≥5 ms; Matelján, ARTA application note 4).</td><td><b>Yes; first, and at no cost.</b> The 0.68 m reflection is just short of the 500 Hz requirement.</td><td>Source position had the largest effect in the trials: moving the loudspeaker about 20 cm closer reduced the room error from {B3['score']:.2f} to {CL['score']:.2f} dB within one afternoon (25 Sep).</td></tr>`

**A35 · p6 · row 2 · Meaning: unchanged**
OLD: `<tr><td><b>2. Measured room correction</b> per position and tone</td><td>Source measured once in a real chamber and again in the room, band by band: "the uncertainty in measurements is minimal (below 0.55 dB for frequencies above 200 Hz)" (du Plessis et al. 2022, p. 29).</td><td><b>Yes, the strongest.</b> Valid for a fixed source and fixed microphones — our arc — not for a flying drone.</td><td>Needs a reference run in a chamber (the university's 300 m³). Void if a capsule is re-seated: 1 cm moves the response ±6 dB at high frequency (Bellmann &amp; Klippel, p. 7). Must be checked against the prop at 200–250 Hz (Mehrgou 2012, p. 34).</td></tr>`
NEW: `<tr><td><b>2. Measured room correction</b> per position and tone</td><td>The source is measured once in a real anechoic chamber and again in the room, band by band: "the uncertainty in measurements is minimal (below 0.55 dB for frequencies above 200 Hz)" (du Plessis et al. 2022, p. 29).</td><td><b>Yes; the strongest option.</b> Valid for a fixed source and fixed microphones, as on this arc. Not valid for a flying drone.</td><td>Needs a reference run in an anechoic chamber (the university's 300 m³ room). Invalid once a capsule is re-mounted: a 1 cm shift changes the response by ±6 dB at high frequency (Bellmann &amp; Klippel, p. 7). Must be checked against the propeller at 200–250 Hz (Mehrgou 2012, p. 34).</td></tr>`

**A36 · p6 · row 3 · Meaning: unchanged (M15 still applies)**
OLD: `<tr><td><b>3. Average over source speed</b></td><td>Tones are where a modal room hurts most; a pattern that changes over a 19 % frequency step averages out over a speed ladder. No published residual.</td><td><b>Yes, cheap.</b> Hardware exists; 12–15 PWM steps.</td><td>Tone-pattern holes of 8 dB moved with a 19 % frequency step in the flat-arc runs; the polar shape of 30 Sep depends on speed outside 1.3–2 kHz.</td></tr>`
NEW: `<tr><td><b>3. Average over source speed</b></td><td>Room resonances (modes) distort pure tones most. A pattern that changes over a 19 % frequency step averages out over a speed ladder (a series of propeller speeds). No paper gives the remaining error.</td><td><b>Yes; low cost.</b> The hardware exists; 12–15 PWM steps.</td><td>In the flat-arc runs, 8 dB dips in the tone pattern moved with a 19 % frequency step. The 30 Sep polar shape depends on speed outside 1.3–2 kHz.</td></tr>`

**A37 · p6 · row 4 · Meaning: unchanged (defines time gating)**
OLD: `<tr><td><b>4. Time gating</b></td><td>Lowest usable frequency ≈ 1 / gate length: "the time-bandwidth requirement is satisfied on frequencies above 177.9Hz" for a 5.6 ms gate (Matelján, p. 8).</td><td><b>Only above 500 Hz</b>: our gate is 1.98 ms.</td><td>Good for naming the 0.68 m and 1.49 m reflectors; cannot reach the blade tone.</td></tr>`
NEW: `<tr><td><b>4. Time gating</b></td><td>Only the sound that arrives before the first reflection is kept. The lowest usable frequency is about 1 / gate length: "the time-bandwidth requirement is satisfied on frequencies above 177.9Hz" for a 5.6 ms gate (Matelján, p. 8).</td><td><b>Only above 500 Hz</b>: the gate here is 1.98 ms.</td><td>Useful to identify the surfaces behind the 0.68 m and 1.49 m reflections. Cannot reach the blade tone.</td></tr>`

**A38 · p6 · row 5 · Meaning: unchanged (W6 and W7 are fixed in F6 and F7)**
OLD: `<tr><td><b>5. Absorb: foam, wedges</b></td><td>34 cm of depth per 250 Hz; cost about ×4 per octave down (Orrego et al. 2018, p. 477). Removing the floor treatment costs ~3 dB broadband and up to 10 dB at the blade tone (Ma et al. 2022, p. 7).</td><td><b>Not at 250 Hz.</b> Yes at 630–1000 Hz: about 10 cm on the named surface.</td><td>The floor under the arc and source mattered most (wedges off: 2.05 → carpet 1.32, same afternoon); the same material on the walls did nothing.</td></tr>`
NEW: `<tr><td><b>5. Absorb: foam, wedges</b></td><td>An absorber about 34 cm deep is needed for 250 Hz; cost about ×4 per octave down (Orrego et al. 2018, p. 477). Removing the floor treatment costs about 3 dB broadband and up to 10 dB at the blade tone (Ma et al. 2022, p. 7).</td><td><b>Not at 250 Hz.</b> Yes at 630–1000 Hz: about 10 cm on the surface the measurement identifies.</td><td>The floor under the arc and the source mattered most (empty floor 2.05 → carpet 1.32, same afternoon). The same material on the walls had no measurable effect.</td></tr>`

**A39 · p6 · row 6 · Meaning: unchanged (names the absorber type from the cited paper's title)**
OLD: `<tr><td><b>6. Subwavelength absorber</b></td><td>"99.2% absorptance at 239 Hz in experiment" in 100 mm (Long et al. 2020, Sci. Rep. 10:13823).</td><td><b>The one exception</b> for the blade tone, <b>but only if</b> the 238 Hz error is the room, not the stand.</td><td>Decide with the reverse-rotation capture first.</td></tr>`
NEW: `<tr><td><b>6. Subwavelength absorber</b> (thin compared with the wavelength)</td><td>A 100 mm metasurface absorber: "99.2% absorptance at 239 Hz in experiment" (Long et al. 2020, Sci. Rep. 10:13823).</td><td><b>The only option that reaches the blade tone</b>, <b>but only if</b> the 238 Hz error comes from the room and not from the stand.</td><td>Decide this first with the reverse-rotation capture (step 2 below).</td></tr>`

**A40 · p6 · Order list · Meaning: unchanged (M20 is fixed in F16b)**
OLD:
```
<li>Record the room (hub height, dimensions, what stands within 1.5 m of the arc ends) and move the 0.68 m reflector or the arc away from it.</li>
<li>One capture with the propeller turning the other way, everything else identical: separates stand-induced from room-induced asymmetry.</li>
<li>Loudspeaker correction at the blade harmonics (215–258 Hz, 713 Hz) for the eleven positions, then compare with the propeller at the same positions.</li>
<li>Speed ladder to average the tones, then treat only the surfaces the sweep names (about 10 cm of foam at 630–1000 Hz).</li>
```
NEW:
```
<li>Record the room: hub height, room dimensions, and what stands within 1.5 m of the arc ends. Then move the object behind the 0.68 m reflection, or move the arc away from it.</li>
<li>Take one capture with the propeller turning the other way and everything else unchanged. This separates asymmetry caused by the stand from asymmetry caused by the room.</li>
<li>Measure the loudspeaker correction (solution 2) at the blade-tone frequencies (215–258 Hz and 713 Hz) for the eleven positions. Then compare it with the propeller at the same positions.</li>
<li>Run a speed ladder to average the tones. Then treat only the surfaces the sweep names (about 10 cm of foam at 630–1000 Hz).</li>
```

**A41 · p6 · Microphone placement · Meaning: unchanged (defines k, r, D<sub>A</sub> and H<sub>m</sub> from the ISO 5305 preview; M16 still applies)**
OLD:
```
<li><b>Meets:</b> far field ((kr)² ≈ 15 at 250 Hz, above 3); the ring radius 0.84 m is more than λ/4 from 250 Hz up; capsule axis normal to the measurement surface (ISO 3745 §6.1.1); ISO 5305 R ≥ 5·D<sub>A</sub> holds for the 137 mm sphere and one 6-inch propeller, not for larger rotors.</li>
<li><b>Does not meet:</b> UMIK-2 is not a WS2F/WS3F class 1 free-field microphone (ISO 5305 §5.1, ISO 3745 §6.1.1); the ring, clamps and cables are untreated supports; one radius only, so decay with distance is not tested.</li>
<li><b>Not recorded:</b> distance of the ring ends to the walls and floor, hub height, ISO 5305 H<sub>m</sub>.</li></ul>
```
NEW:
```
<li><b>Meets:</b> far field, (kr)² ≈ 15 at 250 Hz, above 3 (k = wavenumber, r = ring radius). The ring radius, 0.84 m, is more than a quarter wavelength (λ/4) from 250 Hz up. The capsule axis is normal to the measurement surface (ISO 3745 §6.1.1). ISO 5305 requires R ≥ 5·D<sub>A</sub> (radius at least five times the diameter of the aircraft). This holds for the 137 mm sphere and for one 6-inch propeller, not for larger rotors.</li>
<li><b>Does not meet:</b> the UMIK-2 is not a class 1 free-field microphone of type WS2F or WS3F (ISO 5305 §5.1, ISO 3745 §6.1.1). The ring, clamps and cables are supports without acoustic treatment. All capsules are at one radius, so the fall of level with distance is not tested.</li>
<li><b>Not recorded:</b> the distance from the ring ends to the walls and the floor, the hub height, and ISO 5305 H<sub>m</sub> (the distance from each microphone to the walls, floor and ceiling, or to the wedge tips).</li></ul>
```

**A42 · p1 figure (`fig_mic`) · Meaning: unchanged (fixes the overlapping titles, S1)**
OLD: `(G, 'effect of the correction: closer to the arc mean (blue) or further (orange)', bw, 3)`
NEW: `(G, 'effect of the correction (blue = closer to arc mean)', bw, 3)`
Also: OLD `f'{nm}\nfactory files: {eb:.3f} dB below 3 kHz, span {sb:.1f} dB'` → NEW `f'{nm}\nfactory files: room error {eb:.3f} dB below 3 kHz, span {sb:.1f} dB'`. And OLD `f'corrected: {ea:.3f} dB, span {sa:.1f} dB'` → NEW `f'corrections: room error {ea:.3f} dB, span {sa:.1f} dB'`.

**A43 · p6 · last section · Meaning: unchanged (W5 is fixed in F5)**
OLD: `<h2>Where the accepted configuration stands, and what the method cannot say</h2>`
NEW: `<h2>Where the final configuration stands, and the limits of the method</h2>`
OLD: the bullet that starts `<li>Evaluated on its own (25 Sep): room error` and ends `across a fixed ring.</li>`
NEW:
```
<li>The final configuration (<code>carpet-reordered</code>, 25 Sep), evaluated on its own: room error {X['score']:.3f} dB; within the strict anechoic tolerance values from the {cutoff(X)} Hz band up; {X['tone_all']:.0f} % of tone cells inside the limit.</li>
<li><b>Comparable rooms in the papers held</b>. This excludes the rotor chambers with cut-off frequencies of 63–275 Hz, which are better rooms. A 6.8 m³ low-cost box conforms to the ISO 3745 anechoic limits from 500 Hz, with one point 1.0 dB over (Orrego et al. 2018, p. 6). A 51 m³ room passes with noise and fails with pure tones (Nash 2019). Amazon Prime Air's rotor room is within ±1 dB only above 2.2 × BPF, and within ±4 dB below (Nardari 2019, p. 2).</li>
<li>Rooms tested against the standard keep the strict limits and publish the range that passes (Russo 2018: "in conformity" for a reduced range). Rooms that cannot meet the limits use their own tolerance. This report keeps the strict limits, as Orrego, Nash and Kayhan did, and reports the failures. No paper held judges a room by the spread of level around a fixed ring.</li>
```
OLD: `<li>Deviation from the arc mean is blind to an error shared by all eleven positions; the ISO traverse has not been run, so this ranks bands and does not certify. The anechoic table is used because the floor under the arc is absorbing.</li>`
NEW: `<li>A deviation from the arc mean cannot show an error that is common to all eleven positions. The ISO traverse has not been run. The evaluation therefore ranks bands; it does not certify the room. The anechoic limits are used because the floor under the arc is absorbing.</li>`

**A44 · p6 · two-state switch and grid · Meaning: unchanged**
OLD: the bullet that starts `<li><b>Open, unexplained: a two-state switch in the source chain.</b>` and ends `while handling each).</li>`
NEW:
```
<li><b>Open, unexplained: a two-state switch in the source chain.</b> Across the arc, the level at 5–6.4 kHz minus the level at 257–400 Hz takes one of two values. Between some neighbouring runs it flips by the same amount: <code>foam-2</code>→<code>foam-out</code> {FL[0]:+.1f}, <code>ceiling-carpet</code>→<code>ceiling-carpet-day2</code> (next morning) {FL[1]:+.1f}, <code>ceiling1-floor2</code>→<code>felt-floor-only</code> {FL[2]:+.1f}, <code>chaotic-carpet-2</code>→<code>chaotic-carpet-3</code> {FL[3]:+.1f}, <code>in-plane-b</code>→<code>curtain</code> {FL[4]:+.1f} dB. At the flips within one day, the loudspeaker device and the amplitude were unchanged. The cause is not a source move: a 5 cm move changes the map by 0.80 dB, the 24 Sep flip by {MC:.2f}. It is not absorber moved around the room: changes to the room alone that afternoon moved the mean level by at most {RO[0]:.2f} dB. It is not a gain or supply-voltage change: that would shift every frequency alike, and 257–400 Hz does not move. The flip cancels in the room error, which is relative to the arc mean. Still to check: the cable near the sphere, the connectors, the amplifier and its supply, by playing 300 Hz and 5 kHz on <code>live_tone</code> while handling each part.</li>
```
OLD: `<li>The grid starts at 257 Hz; 3–5 kHz is excluded (sphere), 5–6.4 kHz indicative.</li>`
NEW: `<li>The tone grid starts at 257 Hz. 3–5 kHz is excluded because the loudspeaker sphere is not axisymmetric there. Results at 5–6.4 kHz are indicative only.</li>`

---

## 4. F-list: corrections that change meaning (apply after the A-list; each needs Adam's OK)

**F1 (W1) · p5**
- In A28 NEW, OLD: `(The 2 Sep curves are not drawn; the table carries them.)` → NEW: `The 2 Sep curves are not drawn; their spreads are given only in this text.`
- In the corrections table, OLD: `<td>prop11–17 (prop15–17 drawn)</td>` → NEW: `<td>prop11–17 (prop15–17 used for the spreads in the text)</td>`

**F2 (W2) · p5 · in A29 NEW**
OLD: `which is level with 30 Sep. The absolute change is real; most of it comes from the calibration, little from the room.`
NEW: `30 Sep ({T['med']:.0f} %) lies inside that range but below its median. Read with the same calibration, the 30 Sep polar is not rounder than the 1–2 Sep polars. The gain over the factory-file readings comes from the calibration, not from the room.`

**F3 (W3) · p4 · in A17 NEW**
OLD: `The deviation columns show the worst capsule's band mean, as a share of the limit.`
NEW: `The deviation columns give the worst capsule's band-mean deviation in dB; their colour shows it as a share of the limit.`

**F4 (W4, M2) · p4 · in A16 NEW**
OLD: `over the {F['ntones'][630]}–{F['ntones'][1000]} tones in the band`
NEW: `over the {min(F['ntones'].values())}–{max(F['ntones'].values())} tones in the band (only {F['ntones'][250]} at 250 Hz, because the grid starts at 257 Hz and covers only the top of that band)`

**F5 (W5) · p4 and p6**
- In A19, OLD: `'Inside the tolerance values from this band up'` → NEW: `'Inside the tolerance values from this band up to 2500 Hz (highest band evaluated)'`
- In A43, OLD: `within the strict anechoic tolerance values from the {cutoff(X)} Hz band up;` → NEW: `within the strict anechoic tolerance values from the {cutoff(X)} Hz band up to the 2500 Hz band, the highest evaluated;`

**F6 (W6) · p6 · in A38 NEW**
OLD: `cost about ×4 per octave down (Orrego et al. 2018, p. 477)`
NEW: `lowering the design frequency from 400 Hz to 100 Hz raises the cost per square metre about four times (Orrego et al. 2018, p. 477)`

**F7 (W7) · p6 · in A38 NEW**
OLD: `Removing the floor treatment costs about 3 dB broadband and up to 10 dB at the blade tone (Ma et al. 2022, p. 7).`
NEW: `With a reflecting floor, the overall level deviates from the inverse-square law by up to 3 dB, and two adjacent microphones differ by up to 10 dB at the BPF (Ma et al. 2022, p. 7).`
Before applying, check the printed page number: the held dump has both passages on PDF page 8.

**F8 (W8) · p6 · in A34 NEW**
OLD: `for 250 Hz, 1.37 m (gate ≥5 ms; Matelján, ARTA application note 4).`
NEW: `for 250 Hz, 1.37 m (a 4 ms gate; Matelján, ARTA application note 4, recommends 5 ms or more).`

**F9 (W9) · p4 · in A20 NEW**
OLD: `a re-arranged carpet changed it by 0.14 dB`
NEW: `re-arranging the 24 Sep carpet (<code>chaotic-carpet</code>→<code>chaotic-carpet-2</code>) changed it by {mapchange(CARPET, CARPET2):.2f} dB`
This prints 0.14, and the number is then computed rather than hard-coded.

**F10 (W10) · p1 · in A7 NEW**
Either name the statistic and its source, for example `… reduced the roughness (statistic defined in docs/analysis/baseline-story-2026-09-30/REPORT.pdf) from 3.3 to 1.0 dB`, or drop the bullet. Adam to choose. It must not be read against the rms spreads on p5.

**F11 (W11) · p1 · in A8 NEW**
OLD: `The change is a per-capsule offset. It therefore moves whole rows`
NEW: `The change is mainly a per-capsule offset. It therefore mainly moves whole rows`

**F12 (W12) · p5 · in A30 NEW**
OLD: `(the only propeller capture that has them)`
NEW: `(the only propeller capture in this report that has them)`

**F13 (M1) · p4 · in A16 NEW**
OLD: `Tones and noise are judged separately.`
NEW: `The standards judge tones and noise separately. Here both measures come from the stepped tones; the band level stands in for the noise test.`

**F14 (M6) · p5 · in A28 NEW**
OLD: `In this band 30 Sep has the smallest spread.`
NEW: `In this band 30 Sep has the smallest spread, but it is the only curve read with the corrections (see the reference row of the table).`

**F15 (M8) · p5 · in A22 NEW**
OLD: `<th class="num">Worst deviation</th>`
NEW: `<th class="num">Worst deviation (median over runs)</th>`

**F16 (M13, M20) · p1 and p6**
- (a) p1, at the end of A5 NEW, add: `This spread is for one mounting point; the span in the figure below also contains the room.`
- (b) p6, in A40 NEW, OLD: `treat only the surfaces the sweep names` → NEW: `treat only the surfaces that the reflection measurements identify`. Adam to confirm that this is what "the sweep" meant.

Open items that need Adam's input before any text is written: M4 (tripod on the floor stack before 19:15?), M5 (what the 5 Oct photo shows), M9 (source of ±1.3 dB), M16 (source of "(kr)² > 3"), M17 (which 300 m³ chamber), M18 (Rasmussen 2022 citation), M19 (pointer for the speed dependence).
