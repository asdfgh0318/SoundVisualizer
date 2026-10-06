# Review of chamber-slides.pptx (8 slides), 2026-10-06

Reviewed: `chamber-slides.pptx` (text and speaker notes, via `build_slides.cjs`), the PDF render
(`chamber-slides.pdf`, rendered at 100 dpi), `CHAMBER-FINAL.pdf` / `build_final.py`, the helper
scripts and JSON files in this folder, the data repo (`SoundVisualizer-data/data`), and
`calibrator/sessions/2026-09-16`. Numbers were recomputed by importing `build_final.py` as a module
(as `make_*.py` do), without writing anything into the repo. **The report and the data govern
wherever this review and they disagree.**

## 0. Numbers checked

| Slide | Number on the slide | Recomputed | Verdict |
|---|---|---|---|
| 2 | 6.7 dB range, 31 Aug, 20–560 Hz | 6.69 dB (63.9–70.6), rms 2.05 | OK |
| 3 | 97 tones, 62 Hz–16 kHz, 0.7 s settle, 2 s / 6 s below 250 Hz, amplitude 0.03 | `levels.json` 97 tones 62–16000 Hz; `session.py` settle 0.7, lf 6.0 s below 250 Hz; meta amplitude 0.03 | OK |
| 3 | reference measured three times | full 97-tone runs `m-810-8904__3/__4/__5` (18:15, 18:24, 20:37 starts); `m-810-8904` (25 tones) and `__2` (aborted) are extra | OK, three full runs |
| 3 | "7 of 11 factory files were wrong by 0.6–3.6 dB" | corrected minus factory curve, 90 Hz–16 kHz: the seven are 0.76 to 2.59 dB on average (811-1892 −2.59 mean, −3.47 worst single frequency); the notes list the same seven at 0.8–2.6 dB | **Mismatch** (see A5) |
| 3 | 4.01 → 0.02 dB | from project notes; not recomputable from what is in the folder | not checked; see B3 |
| 4 | 4.3 → 0.8 dB span (final 4.1 → 1.0) | 4.32 → 0.80; 4.06 → 1.02 | OK |
| 4 notes | room error 2.277 → 1.997, 1.736 → 1.387 | 2.277 → 1.997; 1.736 → 1.387 | OK |
| 5 | 2.00 → 1.39 dB | 1.997 → 1.387 | OK |
| 5 | bands 3.33/2.57/1.57/0.80/0.87/1.04 → 1.99/1.52/1.47/0.85/0.96/1.17 | identical | OK |
| 5 | below 630 Hz 3.0 → 1.8 dB, 1.2 dB, 40 % | 2.984 → 1.780, 1.20 dB, 40.4 % | OK |
| 5 notes | 1–3 kHz 0.84 → 0.91; mean level +1.16 dB; tilt −0.41 → −0.63 | 0.838 → 0.912; +1.156; −0.413 → −0.630 | OK |
| 6 | table values | identical to `table.json` and to `bf.stats()`; rows 250–2500 match report page 4 | OK |
| 6 | "Bands clearly over (of 13): 7 → 6", "Cells in limit (13 bands): 60 % → 66 %" | correct for 13 rows, but **the report's card is "of 11": 5 → 4 bands, 58 % → 65 %** | **Mismatch with report** (A4) |
| 7 | 6.7 → 4.0 dB | 6.69 → 4.04; rms 2.05 → 1.45 | OK |
| 7 notes | 30 Sep 11.7 V, 7.3 A, −4 N; blue ~11 dB lower | telemetry PWM 2000: 11.64 V, 7.43 A, −4.09 N; means 68.1 vs 57.1 dB | OK |
| 7 footer | 7.35 V against 11.7 V | 31 Aug: 7.35 V, **13.9 A, +6.2 N** (thrust of the opposite sign) | OK, but incomplete (A2) |
| 8 | means 74.2 / 78.7 / 80.6 / 79.5 / 78.7 dB; +4.5 to +6.4 dB | identical (arithmetic mean of dB **including −90°**) | Arithmetic OK, definition misleading (B1) |
| 8 | −90° at 94–98 dB | 93.7–98.3 dB | OK |

Extra numbers computed for this review (they are not on the slides):
- 31 Aug re-read with the corrected files: range **6.2 dB** (rms 1.84). So the calibration explains only about 0.5 dB of the 6.7 → 4.0 dB on slide 7.
- 2 Sep prop15/16/17 (same operating point as 30 Sep), 20–560 Hz range: factory files 5.7 / 5.3 / 7.3 dB, corrected files **4.8 / 4.0 / 5.9 dB** (rms 1.31 / 1.29 / 2.05 against 1.45 on 30 Sep).
- Material means **without the −90° point**: open 71.8, cork 76.8, rubber 78.9, felt 77.7, felt + rubber 77.2 dB → **+5.0 to +7.2 dB**. Energy (power) mean over all eleven, dominated by −90°: open 88.0, the shrouds 84.5–87.5 dB, i.e. the shrouds come out 0.5–3.5 dB *quieter*.
- Material operating points at PWM 2000 (2 Oct): all 11.64–11.65 V, 7.24–7.36 A; thrust open −3.60 N, cork −3.49, rubber −3.36, felt −3.39, felt + rubber −3.23 N.

---

## (A) Wrong or contradictory

**A1. Slide 7 contradicts the report and breaks the team's own rule.**
- Quote: title "The new polar is rounder"; bullet "The microphones now carry their measured corrections, and the room has been treated."
- Problem: (i) It compares 31 Aug with 30 Sep, which the rule "results of different days are not compared" forbids. (ii) The report (p. 5) concludes the opposite: "Read with the same calibration, the 30 Sep polar is not rounder than the 1–2 Sep polars. The gain over the factory-file readings comes from the calibration, not from the room." (iii) The bullet presents the room treatment as a cause, but no same-source evidence links the treatment to the propeller polar. (iv) For this statistic (20–560 Hz range) even the calibration explains little: 31 Aug re-read with the corrections still spans 6.2 dB. Most of the 6.7 → 4.0 cannot be attributed to anything we did. The likeliest cause is the different operating point (see A2), but that has not been tested.
- Fix: retitle and reword:
  - Title: "A month later: a smoother polar, but not a controlled comparison"
  - Bullets: "30 Sep, read with the corrected microphone files. 31 Aug, read with the factory files." / "The two runs differ in supply voltage, current and thrust direction, so this pair cannot show what caused the change." / "Re-read with the same corrected files, the 2 Sep runs at the 30 Sep operating point span 4.0–5.9 dB. 30 Sep (4.0 dB) is at the low end of that range, not outside it."
  - Label "AFTER" → "COMPARISON". Alternatively drop the slide and end the polar story on slides 5–6, which are same-day.

**A2. Slide 7: "Same kind of measurement, same axes, on 30 Sep."**
- Problem: the operating points differ by more than voltage. 31 Aug ran at 7.35 V, 13.9 A, **+6.2 N**; 30 Sep at 11.6 V, 7.4 A, **−4.1 N**. The thrust sign is reversed, so the flow went the other way past the stand. The report calls the pair "not a controlled pair", and its legend calls one run "horizontal" and the other "prop plane".
- Fix: "Same analysis and same axes. Different day, operating point (7.35 V / 13.9 A / +6 N against 11.6 V / 7.4 A / −4 N) and calibration files." Footer: replace "which is why the blue is lower" with "which is the most likely reason the blue is about 11 dB lower".

**A3. Slide 5 says the treatments helped; slide 6 shows that the upper bands got worse.**
- Quote (slide 5): "The treatments flatten the low end" … "Above 1 kHz only marginal changes."
- Problem: (i) The title gives the treatments as the cause. The footer and the notes say the loudspeaker was moved and not returned to a documented position. The notes add that the tilt changed (−0.41 → −0.63) and the mean level rose 1.16 dB, "so the gain is the treatments plus a small unknown difference in source position". (ii) On slide 6 the worst-microphone deviation rises at 1250 Hz (0.54 → 1.02) and 1600 Hz (0.69 → 1.15). 800 Hz goes from 0.87 to 1.12, so 800 and 1600 Hz cross the limit. The rms by band also rises above 1 kHz (0.80 → 0.85, 0.87 → 0.96, 1.04 → 1.17). The report's own cutoff falls from "from 1250 Hz" to "from 2000 Hz". "Only marginal changes" hides that the upper bands got worse.
- Fix: title "From start to end of day 3, the low frequencies flattened". Body: "Below 630 Hz the room error fell from 3.0 to 1.8 dB (40 %). Above 1 kHz it rose slightly (0.84 → 0.91 dB), and the 1250 and 1600 Hz bands moved to or over the limit (slide 6). The loudspeaker was moved in between, so part of the change may come from its position." Add the clean pair on the slide (see B2).

**A4. Slide 6 summary does not match the report it claims to reproduce.**
- Quote: "Bands clearly over (of 13): 7 → 6" / "Cells in limit (13 bands): 60 % → 66 %"; notes: "Same table as page 4 of the report."
- Problem: report page 4 counts 11 bands: 5 → 4 over, 58 % → 65 % of cells. The slide adds the two partial bands (5000*/6300*), which the report treats as "indicative", and counts them as failures. Someone holding both documents will see two different scorecards.
- Fix: use the report's numbers: "Bands clearly over the limit (of 11, 250–2500 Hz): 5 → 4" and "Cells inside the limit: 58 % → 65 %". Keep the starred rows only as information, and change the notes to "Same table as page 4 of the report, plus the two partial bands."

**A5. Slide 3: "7 of 11 factory files were wrong by 0.6–3.6 dB".**
- Problem: the corrections actually applied (`data/calibrations` minus `factory-originals-2026-09-16`, averaged over 90 Hz–16 kHz) range from 0.76 dB (810-8897) to 2.59 dB (811-1892). Their single-frequency worst is 3.47 dB. The slide's own notes list the same seven at 0.8–2.6 dB. "0.6–3.6" comes from CLAUDE.md, where 3.6 is 811-1892 measured against the group mean, a different datum. The report repeats the CLAUDE.md figure, so the report needs the same correction.
- Fix: "7 of 11 factory files differed from our measurement by 0.8–2.6 dB on average (up to 3.5 dB at single frequencies)". Or keep 0.6–3.6 and say in the notes which datum it uses. The slide, the notes and the report must agree.

## (B) Misleading, or caveat missing from the slide

**B1. Slide 8: the average includes a point that is off the plot.**
- Quote: "Mean level over the eleven microphones" … "+4.5 to +6.4 dB louder than naked, on average".
- Problem: the mean includes the −90° microphone, which reads 94–98 dB in the outflow and is cut off the plot. It is probably airflow on the capsule rather than sound. The result depends on how the average is taken. Without −90° the shrouds are +5.0 to +7.2 dB louder. With an energy mean they come out 0.5–3.5 dB quieter. Also, nothing on the slide says what "cork/rubber/felt" are. They are shrouds (the `shroud` field of each base).
- Fix: compute the average over the ten microphones outside the outflow and say so: "Mean over the ten microphones outside the outflow: open 71.8, cork 76.8, rubber 78.9, felt 77.7, felt + rubber 77.2 dB" → "+5.0 to +7.2 dB louder than the open propeller". Last line: "At −90° the microphone sits in the propeller outflow (94–98 dB, probably airflow on the capsule); it is left out of the average." Title: "Shroud materials at 2000 µs".

**B2. Slide 5: the one clean comparison is only in the notes.**
- Problem: the notes give the pair with a documented, unmoved source (24 Sep: empty floor 2.054 → carpet 1.317 dB; three arrangements 1.317 / 1.318 / 1.324). That is the strongest evidence that the treatment works, and it is not on any slide.
- Fix: add under the big number: "Same source, not moved (24 Sep): empty floor 2.05 → carpet 1.32 dB."

**B3. Slide 3: "4.01 → 0.02 dB spread … for the same sound" looks like an accuracy figure.**
- Problem: the corrections were derived from this same session, so applying them back to it gives about 0 by construction. 0.02 dB is smaller than the session's own repeatability (0.08 dB sd, report p. 1). The absolute level is also not anchored (needs a 94 dB calibrator). That is in the notes and the report but not on the slide, and the corrections are relative to a datum the team chose (four consistent capsules).
- Fix: replace the caption with "spread across the eleven microphones for the same sound, before and after correction (same session; repeatability 0.08 dB)". Add a line in small type: "Relative calibration only: the absolute level still needs a 94 dB calibrator."

**B4. Slide 4: "The correction removes the microphone offsets".**
- Problem: a range of 0.8 dB (1.0 dB in the final state) remains, and it mixes any remaining capsule error with room error. The report's wording is "mainly moves whole rows".
- Fix: "The correction removes most of the microphone offsets". Bullet 2: "The middle row has no clear stripes left."

**B5. Slide 2: the calibration state is not on the slide.**
- Problem: the whole story turns on factory against corrected files, but slide 2 says nothing about which files were used (only the notes do). The operating point (7.35 V, current-limited supply, 13.9 A) is also not shown, though it matters for slide 7.
- Fix: footer: "31 Aug 2026, 20–560 Hz, motor at 2000 µs (7.35 V), read with the factory microphone files. Radial axis 30–76 dB, as in the report."

**B6. Slide 6: the main caveat is in the smallest grey type.**
- Quote: "ISO values are an analogue, not a qualification of the room." (12 pt, muted, bottom right). The title "Band by band against the ISO tolerance" reads like a pass/fail test.
- Fix: subtitle under the title, in INK: "Same limits as an anechoic-room test (ISO 3745 / ISO 5305), applied to a different quantity: a comparison, not a qualification." Also add the message the table shows: "End of day 3: still over the limit at 250, 500, 800 and 1600 Hz; inside from 2000 to 2500 Hz."

**B7. Slide 8: no operating point and no repeat.**
- Problem: the notes say "operating points … were not compared here". They were in fact the same (11.65 V, 7.2–7.4 A), and the shrouds gave 3–10 % less thrust (−3.2 to −3.5 N against −3.6 N). That is worth stating, because they are louder at lower thrust. No set-up was repeated, so the run-to-run spread of the open propeller is unknown. The project notes give 1–2 dB between nominally identical duct runs.
- Fix, footer: "Same supply for all five (11.65 V, 7.2–7.4 A); the shrouds gave 3–10 % less thrust. One capture each; repeatability not measured (1–2 dB between repeated shroud runs on 30 Sep)."

**B8. Slide 7 notes: the "honest caveat" uses the wrong statistic.**
- Quote: "with the same calibration applied to the 1-2 Sep runs, those are about as round as 30 Sep, so most of the improvement … comes from the microphone calibration, not the room."
- Problem: the report's statement is about the tone-notched 315 Hz–8 kHz cell statistic. For the 20–560 Hz range on the slide, the calibration takes 31 Aug only from 6.7 to 6.2 dB. The remainder is between days and operating points and cannot be attributed.
- Fix (notes): "For the 20–560 Hz range shown, the corrections take 31 Aug from 6.7 to 6.2 dB; 2 Sep at the 30 Sep operating point spans 4.0–5.9 dB when corrected. The rest of the difference is between days and operating points and is not attributed." Drop "Honest caveat:", which is not the requested tone.

**B9. Slide 8 belongs to a different geometry, and the slide does not say so.**
- Problem: after slides 2 and 7 have taught that "round = good", the audience sees a strongly non-round polar. On 2 Oct the outflow hits the −90° microphone, so the propeller axis lies in the plane of the ring and real directivity is expected. Without one sentence, slide 8 looks like a failure.
- Fix: add a first line: "Here the ring is turned so that it measures the propeller's real directivity: a non-round polar is expected."

## (C) Story, flow, visuals, language

**Story and flow**
- C1. Slide 4 uses `day3-a` and `carpet-reordered` before slide 5 introduces them, and the audience does not yet know these are loudspeaker captures. Fix: footer "Loudspeaker at the hub, 25 Sep 2026: start of day 3 (left) and end of day 3 (right), the two runs of the next slide."
- C2. "Room error" is used on slides 4–5 and never defined on a slide. Fix (slide 5, under "room error below 3 kHz"): "rms difference of each microphone from the average of all eleven, loudspeaker at the hub; 0 = perfectly even".
- C3. No closing slide. The deck ends on a new topic (shrouds). Suggest a slide 9 "What we know, what is open": calibration fixed (relative, 7 of 11 files corrected); floor treatment helps (24 Sep, same source, 2.05 → 1.32 dB); still open: source position on 25 Sep, the 250–500 Hz bands, absolute level (94 dB calibrator), repeatability of propeller runs.
- C4. Slide 3's label "THE FIX" suggests that calibration fixed slide 2's polar. Re-read with the corrected files, slide 2's polar still spans 6.2 dB. Fix: "STEP 1: THE MICROPHONES"; slide 5 "STEP 2: THE ROOM".
- C5. Slides 5 and 6 cover the same pair. That is fine, but slide 6 needs a message title (see B6) so that each slide has one message.

**Visual QA (PDF at 100 dpi)**
- C6. Slide numbers: slide 1 is unnumbered and slides 2–8 show 2…8. OK. The comments in `build_slides.cjs` are stale ("Slide 1: the problem", "Slide 2: what we did" …); renumber them so they match.
- C7. Slide 5 chart: data labels are rendered with **decimal commas** ("3,3", "2,0") while every other number in the deck uses points. This is the locale of the PDF converter, and PowerPoint may do the same on a Polish system. Fix: format code `'0.0'` is ignored by LibreOffice's locale. Put the values in as text labels, or set the chart language to en-GB. Data labels are 9 pt; raise to 11.
- C8. Slide 5 chart colours are grey/navy while the big number beside it is red → blue. Use the red/blue convention: start of day 3 `D6336C`, final `2B6CB0`.
- C9. Slides 4 and 5 heat maps: tick labels and colourbar text come out at about 6–7 pt on the slide, which is unreadable when projected. Fix: re-export with `fs` ≈ 1.8–2.0, or crop to fewer rows (slide 4 could show only the left column).
- C10. Heat-map colours clash with the deck convention: in the maps red = louder and blue = quieter, while everywhere else red = before and blue = after. The slide 4 colourbar label also says "capsule". At least add "red/blue here = louder/quieter, not before/after" to the slide 4 bullet, or use a different diverging map (purple–green) for level.
- C11. Slide 8: radial tick labels "70" and "75" are hidden under the curves (open-propeller and purple lines). Move `set_rlabel_position` to about 100° (the top-left quadrant has the most free space) or give the labels white boxes on top (`zorder`).
- C12. Slide 8: "Felt" uses `D6336C`, the same red as "31 Aug / before" and as the "+4.5 to +6.4 dB" callout. Give felt another colour (e.g. brown `8B5A2B` or teal `0CA678`) and set the callout in INK.
- C13. Slide 3: the red dashed arrow uses the "before" red; use MUTED. The UMIK-2 product photo shows the capsule unscrewed from the body, which suggests a detached capsule. Crop it or caption "(capsule shown unscrewed)".
- C14. Slide 6: Limit column shows "1" and "1.5". Write "1.0" for consistency. The table header "worst mic, dB" → "worst microphone (dB)".
- C15. Slide 2/7 polar: fine. No overflow or overlap found on slides 1, 2, 3, 6, 7. Body text is 14–16 pt and footers 11 pt.

**Language**
- C16. Inconsistent terms: "microphone" on the slides but "capsule" in the slide 4/5 figure labels ("capsule level minus arc mean"); "arc" (slides 2, 4, 5) against "ring" (slide 1); "Final" / "final state" / "carpet-reordered (final)" / "Final (carpet-reordered)". Pick "microphone", define "ring (arc)" once on slide 2, and use "end of day 3" (with `carpet-reordered` only in footers). "Final" also suggests the chamber is finished.
- C17. Informal or unexplained words. "Chasing a round polar" (slide 1, mildly idiomatic; alternative "Towards a round polar plot"). "Naked" (slide 8) → "Open propeller (no shroud)". "flatten the low end" → "even out the low frequencies". "its cone rocks near 4.4 kHz" → "its cone has a rocking resonance near 4.4 kHz". "polar" as a noun → "polar plot" at first use, with "(level at each microphone angle)" on slide 2. "motor at 2000 µs" → "throttle signal 2000 µs" at first use.
- C18. Spelling is consistently British (colour, analogue, set-up). OK; keep it that way.
- C19. Slide 1 notes say the photo shows the "final configuration (carpet-reordered)". The photo is from 5 Oct, after the 30 Sep and 2 Oct propeller runs. Say "photographed 5 Oct; set-up as accepted on 25 Sep", and only if that is confirmed.
- C20. Bases `…naked-horizontal` and `…cork-horizontal` carry "horizontal" in their names, but the other three bases do not. The −90° readings agree, so the geometry is probably the same, but confirm it before presenting.

---

## The 8 most important fixes

1. Slide 7: drop "rounder" and "the room has been treated". This is a cross-day pair with different operating points and thrust direction. The report says the 30 Sep polar is not rounder at equal calibration.
2. Slide 7: replace "Same kind of measurement" with the real differences (7.35 V / 13.9 A / +6 N against 11.6 V / 7.4 A / −4 N; factory against corrected files).
3. Slide 5: change the causal title and replace "Above 1 kHz only marginal changes" with what slide 6 shows: 1250 and 1600 Hz moved to or over the limit, and the source moved.
4. Slide 5: put the clean same-source pair on the slide (24 Sep, empty floor 2.05 → carpet 1.32 dB).
5. Slide 6: use the report's scorecard (of 11 bands: 5 → 4 over, 58 → 65 %) and lift "analogue, not a qualification" into the subtitle.
6. Slide 8: average without the −90° outflow microphone (+5.0 to +7.2 dB), say what the materials are (shrouds), and give the same operating point plus the missing repeat.
7. Slide 3: reconcile "0.6–3.6 dB" with the applied corrections (0.8–2.6 dB mean, 3.5 dB worst). Present 0.02 dB as a same-session check and note that the absolute level is not anchored.
8. Visuals: decimal commas and grey/navy colours in the slide 5 chart, 6–7 pt heat-map text on slides 4–5, hidden radial labels and the felt/red colour clash on slide 8.
