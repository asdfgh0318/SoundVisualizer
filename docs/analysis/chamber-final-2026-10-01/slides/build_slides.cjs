const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';            // 13.33 x 7.5 in
pres.title = 'Chamber measurements';
const INK = '1F2A44', RED = 'D6336C', BLUE = '2B6CB0', MUTED = '5B6578';

// Slide 1: intro, the chamber as it is now
{
  const s = pres.addSlide();
  s.background = { color: '1F2A44' };
  s.addImage({ path: 'photo-chamber.jpg', x: 0, y: 0, w: 5.65, h: 7.5, sizing: { type: 'cover', w: 5.65, h: 7.5 }, altText: 'The chamber in its current set-up: the microphone ring laid flat around the propeller rig, speaker tripod on the left, absorbing material on floor, ceiling and walls' });
  s.addText('Chasing a round polar', { x: 6.3, y: 2.9, w: 6.8, h: 1.4, fontFace: 'Cambria', fontSize: 40, bold: true, color: 'FFFFFF', margin: 0, valign: 'middle', isTextBox: true });
  s.addText('Our chamber in its current set-up (5 Oct 2026): eleven microphones on a ring around the source, absorbing material on floor, ceiling and walls.', { x: 6.3, y: 6.3, w: 6.3, h: 0.8, fontFace: 'Calibri', fontSize: 14, color: 'AFC3E3', margin: 0, valign: 'top', isTextBox: true });
  s.addNotes('Intro slide. The photo (komora_05_10_26.jpg) shows the chamber in the final configuration (carpet-reordered): the microphone ring laid flat around the propeller rig at the hub, the loudspeaker tripod on the left, batting on the floor and ceiling, wedges and lined pillars on the walls. Ring diameter 1.68 m (radius 0.84 m), eleven UMIK-2 microphones.');
}

// Slide 1: the problem
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-red.png', x: 0.6, y: 0.65, w: 6.2, h: 6.2, altText: 'Polar plot of the 31 Aug propeller measurement, 20 to 560 Hz, with a jagged outline' });
  s.addText('THE PROBLEM', { x: 7.4, y: 0.9, w: 5.3, h: 0.4, fontFace: 'Calibri', fontSize: 14, bold: true, color: RED, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Our polar plot is jagged', { x: 7.4, y: 1.3, w: 5.3, h: 1.3, fontFace: 'Cambria', fontSize: 34, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'We measured a propeller with the microphone arc in a plane parallel to the propeller disc.', options: { bullet: true, breakLine: true } },
    { text: 'A propeller is symmetric around its axis, so every microphone should read about the same.', options: { bullet: true, breakLine: true } },
    { text: 'We expected a smooth, nearly round polar. We observed a jagged outline.', options: { bullet: true, bold: true } },
  ], { x: 7.4, y: 2.75, w: 5.3, h: 2.6, fontFace: 'Calibri', fontSize: 16, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 10, isTextBox: true });
  s.addText('6.7 dB', { x: 7.4, y: 5.5, w: 5.3, h: 0.8, fontFace: 'Cambria', fontSize: 48, bold: true, color: RED, margin: 0, isTextBox: true });
  s.addText('between the loudest and quietest of the eleven microphones', { x: 7.4, y: 6.3, w: 5.3, h: 0.5, fontFace: 'Calibri', fontSize: 14, color: MUTED, margin: 0, isTextBox: true });
  s.addText('31 Aug 2026, 20–560 Hz, motor at 2000 µs. Radial axis 30–76 dB, the same as in the report.', { x: 0.6, y: 6.95, w: 12.1, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText(String(2), { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Data: the 31 Aug 2026 horizontal baseline (arc laid flat, propeller axis vertical), propeller at PWM 2000, total level 20-560 Hz per microphone, read with the factory calibration files as it was measured. Rms spread about the mean 2.05 dB, range 6.7 dB (63.9 to 70.6 dB SPL). The radial axis is 30-76 dB, the same as the report polars, so the same red curve can be shown against the 30 Sep measurement on a later slide. On a 0-80 dB axis the same curve looks rounder.');
}



// Slide 2: what we did to fix it
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addText('THE FIX', { x: 0.6, y: 0.5, w: 6, h: 0.4, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('What we did: every microphone, one loudspeaker', { x: 0.6, y: 0.9, w: 12.1, h: 0.8, fontFace: 'Cambria', fontSize: 32, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  // set-up: loudspeaker -> UMIK-2, capsule end towards the loudspeaker
  s.addImage({ path: 'photo-source.jpg', x: 0.9, y: 2.0, w: 2.1, h: 2.45, sizing: { type: 'cover', w: 2.1, h: 2.45 }, altText: 'Our loudspeaker: a printed sphere with an 8 cm driver' });
  s.addText('Our loudspeaker', { x: 0.6, y: 4.55, w: 2.7, h: 0.35, fontFace: 'Calibri', fontSize: 16, color: INK, align: 'center', margin: 0, isTextBox: true });
  s.addText('tones, 62 Hz–16 kHz', { x: 3.35, y: 2.55, w: 2.4, h: 0.35, fontFace: 'Calibri', fontSize: 14, color: MUTED, align: 'center', margin: 0, isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: 3.45, y: 3.25, w: 2.2, h: 0, line: { color: RED, width: 3, dashType: 'dash', endArrowType: 'triangle' } });
  s.addImage({ path: 'umik2-photo.png', x: 5.9, y: 2.75, w: 5.2, h: 1.405, altText: 'UMIK-2 measurement microphone, capsule end on the left facing the loudspeaker' });
  s.addText('UMIK-2 microphone, capsule faces the loudspeaker', { x: 5.9, y: 4.3, w: 6.8, h: 0.35, fontFace: 'Calibri', fontSize: 16, bold: true, color: BLUE, margin: 0, isTextBox: true });
  // settings
  s.addText([
    { text: '97 tones per microphone, 62 Hz to 16 kHz, 12 per octave (a stepped sweep)', options: { bullet: true, breakLine: true } },
    { text: 'One tone at a time: 0.7 s to settle, then 2 s recorded (6 s below 250 Hz)', options: { bullet: true, breakLine: true } },
    { text: 'Microphones swapped in turn: same position, same loudspeaker, same level', options: { bullet: true, breakLine: true } },
    { text: 'One microphone measured three times as the reference', options: { bullet: true } },
  ], { x: 0.6, y: 5.2, w: 7.0, h: 1.65, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 5, isTextBox: true });
  // result
  s.addText([
    { text: '4.01', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '0.02 dB', options: { color: BLUE } },
  ], { x: 8.2, y: 5.05, w: 4.6, h: 0.75, fontFace: 'Cambria', fontSize: 40, bold: true, margin: 0, isTextBox: true });
  s.addText('spread across the eleven microphones for the same sound', { x: 8.2, y: 5.8, w: 4.6, h: 0.5, fontFace: 'Calibri', fontSize: 14, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('7 of 11 factory files were off by 0.8–2.6 dB on average', { x: 8.2, y: 6.35, w: 4.6, h: 0.5, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Calibration session 16 Sep 2026, loudspeaker amplitude 0.03 of full scale. UMIK-2 photo: miniDSP product brief.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('3', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Procedure (calibrator/session.py, 2026-09-16 session): each of the eleven UMIK-2 capsules was plugged in at the same mounting point in front of the loudspeaker and measured over 97 stepped tones, 62 Hz to 16 kHz (about 12 per octave), amplitude 0.03, 48 kHz sampling, 0.7 s settle and 2 s capture per tone (6 s below 250 Hz). Capsule 810-8904 was measured three full times (18:21, 18:30, 20:43) as the reference. The difference of each capsule from the reference was folded into its calibration curve; Sens Factors kept as in the factory files. The datum is the mean of four capsules whose factory files agree with measurement (810-8900, 810-8903, 811-1896, 811-2321). Spread 4.01 to 0.02 dB is from the project notes: a same-session check, since the corrections come from this session, and the absolute level is not anchored (that needs a 94 dB calibrator). Seven capsules have a mean offset beyond 0.6 dB over frequency, between 0.76 and 2.59 dB; the worst single frequency is 3.48 dB (811-1892), from CORRECTIONS-2026-09-16.csv. Seven capsules had a mean offset beyond 0.6 dB (811-1892 -2.6, 811-1897 -1.4, 811-2310 -0.8, 810-8897 +0.8, 810-8901 +0.8, 810-8904 +0.9, 810-8893 +1.3). Absolute level is not anchored: that needs a 94 dB calibrator.');
}

// Slide 3: the waterfalls of the calibration, before and after
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'fig-mic-slide.png', x: 0.3, y: 0.3, w: 8.06, h: 6.4, altText: 'Maps of each microphone against frequency for two captures: factory files (top), corrected (middle), effect of the correction (bottom)' });
  s.addText('THE RESULT', { x: 8.95, y: 0.7, w: 3.9, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('The correction removes the microphone offsets', { x: 8.95, y: 1.05, w: 3.9, h: 1.7, fontFace: 'Cambria', fontSize: 28, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'Top', options: { bold: true } }, { text: ': factory files. ' }, { text: 'Middle', options: { bold: true } }, { text: ': corrected. ' }, { text: 'Bottom', options: { bold: true } }, { text: ': what the correction changed.', options: { breakLine: true } },
    { text: 'A stripe across all frequencies is one microphone reading too loud or too quiet. The middle row has none.', options: { bullet: true, breakLine: true } },
    { text: 'The room pattern stays: whole rows move, not the frequency structure.', options: { bullet: true } },
  ], { x: 8.95, y: 2.85, w: 3.9, h: 2.7, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 8, isTextBox: true });
  s.addText([
    { text: '4.3', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '0.8 dB', options: { color: BLUE } },
  ], { x: 8.95, y: 5.55, w: 3.9, h: 0.7, fontFace: 'Cambria', fontSize: 36, bold: true, margin: 0, isTextBox: true });
  s.addText('gap between the loudest and quietest microphone for the same sound: factory files → corrected (start of day 3; final state 4.1 → 1.0 dB)', { x: 8.95, y: 6.25, w: 3.9, h: 0.6, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Two captures from 25 Sep 2026: the start of day 3 (left) and the final configuration (right).', { x: 0.6, y: 6.95, w: 8.0, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('4', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Same figure as chapter 1 of the report, redrawn larger. The same two captures were calibrated two ways: with the factory files and with the corrections measured on 16 Sep. The span is the range of the capsules mean levels: 4.3 to 0.8 dB at the start of day 3, 4.1 to 1.0 dB in the final configuration. Room error below 3 kHz: 2.277 to 1.997 dB and 1.736 to 1.387 dB. The change is mainly a per-capsule offset, so it mainly moves whole rows.');
}

// Slide 4: the chamber treatments, day 3 start against the final state
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'fig-wf-slide.png', x: 0.3, y: 0.3, w: 7.59, h: 6.45, altText: 'Maps of each microphone against frequency: start of day 3, final state, and the change between them' });
  s.addText('THE CHAMBER', { x: 8.95, y: 0.5, w: 3.9, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('The treatments flatten the low end', { x: 8.95, y: 0.85, w: 3.9, h: 1.2, fontFace: 'Cambria', fontSize: 28, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addChart(pres.charts.BAR, [
    { name: 'Start of day 3', labels: ['250–400', '400–630', '630–1000', '1000–1600', '1600–3000', '5000–6400'], values: [3.33, 2.57, 1.57, 0.8, 0.87, 1.04] },
    { name: 'Final', labels: ['250–400', '400–630', '630–1000', '1000–1600', '1600–3000', '5000–6400'], values: [1.99, 1.52, 1.47, 0.85, 0.96, 1.17] },
  ], {
    x: 8.85, y: 2.05, w: 4.1, h: 2.75, barDir: 'col', barGrouping: 'clustered', chartColors: ['D6336C', '2B6CB0'], showLegend: true, legendPos: 'b', legendFontSize: 11, legendColor: INK, legendFontFace: 'Calibri',
    showTitle: true, title: 'Room error per band (dB, band in Hz)', titleFontSize: 12, titleColor: INK, titleFontFace: 'Calibri',
    catAxisLabelFontSize: 10, catAxisLabelColor: INK, catAxisLabelFontFace: 'Calibri', valAxisLabelFontSize: 10, valAxisLabelColor: MUTED, valAxisLabelFontFace: 'Calibri', valAxisMinVal: 0, valAxisMaxVal: 4, valAxisMajorUnit: 1,
    valGridLine: { color: 'E3E7EE', size: 0.5 }, catGridLine: { style: 'none' }, barGapWidthPct: 50,
    showValue: true, dataLabelFontSize: 9, dataLabelColor: INK, dataLabelFontFace: 'Calibri', dataLabelFormatCode: '0.0', dataLabelPosition: 'outEnd',
  });
  s.addText([
    { text: '2.00', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '1.39 dB', options: { color: BLUE } },
  ], { x: 8.95, y: 4.85, w: 3.9, h: 0.65, fontFace: 'Cambria', fontSize: 34, bold: true, margin: 0, isTextBox: true });
  s.addText('room error below 3 kHz', { x: 8.95, y: 5.5, w: 3.9, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
  s.addText('We improved the low end (below 630 Hz) by 1.2 dB: the error fell from 3.0 to 1.8 dB, 40 % lower. Above 1 kHz only marginal changes.', { x: 8.95, y: 5.85, w: 3.9, h: 0.95, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText('25 Sep 2026. The loudspeaker was moved during the day and returned to about its starting point; the position was not documented. Room error: rms difference of the eleven microphones from their average.', { x: 0.6, y: 6.85, w: 11.4, h: 0.45, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('5', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Same pair as page 3 of the report (day3-a at 13:17, carpet-reordered at 19:15, both 25 Sep), read with the corrected microphone files. Room error is the rms deviation of the eleven microphones from their mean, per band. Below 630 Hz the rms room error fell from 2.98 to 1.78 dB (1.2 dB, 40 %); between 1 and 3 kHz it went 0.84 to 0.91 dB. Start of day 3: 3.33, 2.57, 1.57, 0.80, 0.87, 1.04 dB; final: 1.99, 1.52, 1.47, 0.85, 0.96, 1.17 dB for the bands 250-400, 400-630, 630-1000, 1000-1600, 1600-3000 and 5000-6400 Hz. Caveat from the report: the loudspeaker was moved on purpose during the day (20 cm closer, into the ring plane, 5 cm back) and then returned to about its starting mounting point, which was not recorded. The tilt of the map changed from -0.41 to -0.63 and the mean level rose 1.16 dB, so the gain is the treatments plus a small unknown difference in source position, and part of it may be the louder direct sound. The clean pair with an unmoved source is 24 Sep: empty floor 2.054 to carpet 1.317 dB.');
}

// Thinsulate ring wrap slide: left out of the deck on request; build it with WRAP_SLIDE=1
if (process.env.WRAP_SLIDE) {
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addText('THE RING WRAP', { x: 0.6, y: 0.5, w: 6, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Thinsulate on the ring hardly matters', { x: 0.6, y: 0.85, w: 12.1, h: 0.8, fontFace: 'Cambria', fontSize: 32, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Size of the change in room error (dB)', { x: 0.6, y: 1.9, w: 7.2, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addChart(pres.charts.BAR, [{ name: 'Change in room error (dB)', labels: ['Tripod wrap partly off (23 Sep)', 'Ring wrap, first part off (23 Sep)', 'Ring wrap, more off (23 Sep)', 'Rest of ring wrap off (24 Sep)', 'Handling alone (typical)', 'Carpet on the empty floor (24 Sep)'], values: [0.004, 0.018, 0.002, 0.014, 0.04, 0.737] }], {
    x: 0.5, y: 2.25, w: 7.7, h: 4.55, barDir: 'bar', chartColors: ['9AA5B8', '9AA5B8', '9AA5B8', '9AA5B8', 'C9CFDA', BLUE], catAxisOrientation: 'maxMin', catAxisLabelPos: 'low', catAxisLabelFrequency: 1,
    showLegend: false, showTitle: false, catAxisLabelFontSize: 13, catAxisLabelColor: INK, catAxisLabelFontFace: 'Calibri',
    valAxisMinVal: 0, valAxisMaxVal: 0.9, valAxisMajorUnit: 0.3, valAxisLabelFontSize: 12, valAxisLabelColor: MUTED, valAxisLabelFontFace: 'Calibri', valAxisLabelFormatCode: '0.0',
    valGridLine: { color: 'E3E7EE', size: 0.5 }, catGridLine: { style: 'none' }, barGapWidthPct: 45,
    showValue: true, dataLabelFontSize: 13, dataLabelColor: INK, dataLabelFontFace: 'Calibri', dataLabelFormatCode: '0.000', dataLabelPosition: 'outEnd',
  });
  s.addText('0.02 dB', { x: 8.6, y: 1.95, w: 4.2, h: 0.9, fontFace: 'Cambria', fontSize: 48, bold: true, color: RED, margin: 0, isTextBox: true });
  s.addText('at most: the largest change in room error from taking any Thinsulate wrap off the ring or the tripod, in four cases.', { x: 8.6, y: 2.9, w: 4.2, h: 1.0, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'Three cases got slightly worse, one slightly better: no clear effect.', options: { bullet: true, breakLine: true } },
    { text: 'The same state measured twice differs by 0.006–0.015 dB, and handling by about 0.04 dB.', options: { bullet: true, breakLine: true } },
    { text: 'The carpet on the empty floor changed the error 40 times more.', options: { bullet: true } },
  ], { x: 8.6, y: 4.1, w: 4.2, h: 2.6, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 8, isTextBox: true });
  s.addText('Runs: foam-out → tripod-unwrapped → ring-unwrapped → -2 (23 Sep); wall-direct-absorber → ring-bare (24 Sep). Carpet: 2.054 → 1.317 dB.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('6', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Source: README of the chamber trials (docs/analysis/chamber-treatments-2026-09-23) and the loudspeaker sessions, room error below 3 kHz. 23 Sep: foam-out 1.3837 to tripod-unwrapped 1.3874 (+0.004, some wrapping off the tripod legs); to ring-unwrapped 1.4057 (+0.018, part of the ring wrapping removed; a new hub mounting preset from there); to ring-unwrapped-2 1.4076 (+0.002, more of the ring unwrapped). 24 Sep, speaker on the wall (a different geometry): wall-direct-absorber 2.2193 to ring-bare 2.2054 (-0.014), the rest of the ring wrap removed, 10 minutes apart; map change 0.36 dB spread over all capsules. Three of the four changes are slightly worse, one slightly better. The README concludes the ring wrap is worth a little only at the high end, and that the best state measured was tripod bare and ring wrapped. Repeat floor 0.006-0.015 dB, handling about 0.04 dB (README). Carpet on the empty floor: 24 Sep floor-no-wedges 2.054 to chaotic-carpet 1.317 dB (-0.737), source unmoved. 0.737 / 0.018 = 40.');
}

// Slide 6: the band table of the evaluation, colour graded
{
  const T = JSON.parse(require('fs').readFileSync('table.json', 'utf8'));
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addText('THE EVALUATION', { x: 8.95, y: 0.5, w: 3.9, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Band by band against the ISO tolerance', { x: 8.95, y: 0.85, w: 3.9, h: 1.3, fontFace: 'Cambria', fontSize: 26, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  const GRID = { type: 'solid', pt: 0.75, color: '9AA5B8' }, SEP = { type: 'solid', pt: 2, color: '4A5568' };
  const H = (t, extra = {}) => ({ text: t, options: Object.assign({ bold: true, fontFace: 'Calibri', fontSize: 12, color: INK, align: 'center', valign: 'middle', border: [GRID, GRID, GRID, GRID] }, extra) });
  const C = (t, fill, o = {}) => ({ text: t, options: Object.assign({ fontFace: 'Calibri', fontSize: 14, color: INK, align: 'center', valign: 'middle', fill: fill ? { color: fill } : undefined, border: [GRID, GRID, GRID, GRID] }, o) });
  const rows = [
    [H('Band'), H('Limit'), H('Tones'), H('Start of day 3', { colspan: 2, color: RED, border: [GRID, GRID, GRID, SEP] }), H('Final', { colspan: 2, color: BLUE, border: [GRID, GRID, GRID, SEP] })],
    [H('Hz'), H('± dB'), H('per band'), H('worst mic, dB', { border: [GRID, GRID, GRID, SEP] }), H('cells in limit'), H('worst mic, dB', { border: [GRID, GRID, GRID, SEP] }), H('cells in limit')],
  ];
  T.rows.forEach((r) => rows.push([C(String(r.band), null, { bold: true }), C(r.limit.toFixed(1), null), C(String(r.tones), null), C(r.gdev.toFixed(2), r.gdevc, { bold: true, border: [GRID, GRID, GRID, SEP] }), C(r.gcells + ' %', r.gcellsc), C(r.xdev.toFixed(2), r.xdevc, { bold: true, border: [GRID, GRID, GRID, SEP] }), C(r.xcells + ' %', r.xcellsc)]));
  s.addTable(rows, { x: 0.6, y: 0.5, w: 7.9, colW: [0.85, 0.8, 0.85, 1.4, 1.3, 1.4, 1.3], rowH: [0.36, 0.32].concat(Array(T.rows.length).fill(0.43)), margin: [0.02, 0.04, 0.02, 0.04] });
  // colour key
  s.addText('Colour key', { x: 8.95, y: 2.35, w: 3.9, h: 0.3, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, isTextBox: true });
  T.scale.forEach((c, i) => s.addShape(pres.shapes.RECTANGLE, { x: 8.95 + i * 0.78, y: 2.7, w: 0.78, h: 0.3, fill: { color: c }, line: { color: 'FFFFFF', width: 1 } }));
  s.addText('0', { x: 8.95, y: 3.03, w: 0.78, h: 0.25, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'center', margin: 0, isTextBox: true });
  s.addText('at the limit', { x: 8.95 + 2 * 0.78 - 0.1, y: 3.03, w: 0.98, h: 0.25, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'center', margin: 0, isTextBox: true });
  s.addText('2× or more', { x: 8.95 + 4 * 0.78 - 0.1, y: 3.03, w: 0.98, h: 0.25, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'center', margin: 0, isTextBox: true });
  s.addText('Worst microphone as a share of the limit. Cells: green 100 %, yellow 50 %, red 0 %.', { x: 8.95, y: 3.35, w: 3.9, h: 0.55, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  // scorecard
  const g = T.card.g, x = T.card.x;
  s.addText([
    { text: 'Bands clearly over (of 13): ' }, { text: `${g.over13} → ${x.over13}`, options: { bold: true, breakLine: true } },
    { text: 'Cells in limit (13 bands): ' }, { text: `${g.cells13} % → ${x.cells13} %`, options: { bold: true } },
  ], { x: 8.95, y: 4.1, w: 3.9, h: 1.5, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 6, isTextBox: true });
  s.addText('* Partial bands: only the tones above 5 kHz are measured (4 and 5 tones). 3–5 kHz is left out because of the loudspeaker: its cone has a rocking mode near 4.4 kHz. ISO values are an analogue, not a qualification of the room.', { x: 8.95, y: 5.75, w: 3.9, h: 1.15, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('6', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Same table as page 4 of the report. Each one-third-octave band is judged against the anechoic tolerance values of ISO 5305 Table 1 (also ISO 3745 as printed by Cunefare 2003): +-1.5 dB for 125-630 Hz, +-1.0 dB for 800-5000 Hz. The number is the worst microphone band-mean deviation from the arc mean, in dB; the colour is that number as a share of the limit. Cells in limit counts tone x microphone cells inside the limit (3 tones x 11 microphones = 33 cells at 250 Hz, where the grid starts at 257 Hz). This is an analogue: the standards use a traverse and test decay with distance, we use eleven fixed microphones at one radius. The room is treated and not qualified. Within the tolerance values from 1250 Hz at the start of day 3 and from 2000 Hz in the final state, up to 2500 Hz. The rows marked * (5000 and 6300 Hz) are partial: 4 and 5 tones above 5 kHz, the limit is +-1.0 dB at 5000 Hz and +-1.5 dB at 6300 Hz (ISO 5305 Table 1). Both are over the limit in both states (1.24 and 1.23 dB; 1.59 and 1.77 dB). The 3150 and 4000 Hz bands are not shown: no tones between 3 and 5 kHz because of the rocking mode of the sphere at about 4.4 kHz. Caveat: the loudspeaker position was not documented across the day.');
}

// Slide 7: the same polar with the 30 Sep measurement on top
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-both.png', x: 0.6, y: 0.5, w: 5.95, h: 6.34, altText: 'Polar plot of 20 to 560 Hz: the jagged red 31 Aug outline and the smoother blue 30 Sep outline' });
  s.addText('COMPARISON', { x: 7.4, y: 0.9, w: 5.3, h: 0.4, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('31 Aug and 30 Sep on the same axes', { x: 7.4, y: 1.3, w: 5.3, h: 1.3, fontFace: 'Cambria', fontSize: 34, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'Red: 31 Aug, factory microphone files. Blue: 30 Sep, corrected files. Two different propellers.', options: { bullet: true, breakLine: true } },
    { text: 'The propeller was mounted the other way round between the two, so the thrust points the other way. We do not expect this to change the sound.', options: { bullet: true, breakLine: true } },
    { text: 'The 30 Sep outline is smoother.', options: { bullet: true, bold: true } },
  ], { x: 7.4, y: 2.75, w: 5.3, h: 2.6, fontFace: 'Calibri', fontSize: 16, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 10, isTextBox: true });
  s.addText([
    { text: '6.7', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '4.0 dB', options: { color: BLUE } },
  ], { x: 7.4, y: 5.5, w: 5.3, h: 0.8, fontFace: 'Cambria', fontSize: 48, bold: true, margin: 0, isTextBox: true });
  s.addText('between the loudest and quietest microphone', { x: 7.4, y: 6.3, w: 5.3, h: 0.5, fontFace: 'Calibri', fontSize: 14, color: MUTED, margin: 0, isTextBox: true });
  s.addText('20–560 Hz, motor at 2000 µs. Different propellers and run conditions, so the levels are not comparable; compare the shapes.', { x: 0.6, y: 6.95, w: 12.1, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText(String(7), { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Blue: 30 Sep propeller measurement (11.7 V, 7.3 A, thrust -4 N), read with the 16 Sep microphone corrections. Rms spread about the mean 1.45 dB against 2.05 dB for 31 Aug; range 4.0 dB (55.5 to 59.6 dB SPL) against 6.7 dB. The blue is about 11 dB lower, but this cannot be attributed to the supply voltage (the blue run had the higher voltage): the two runs used different propellers, and the thrust direction was reversed, so the levels are not comparable. The 4 dB range of the blue is a bottom-louder trend. Honest caveat: with the same calibration applied to the 1-2 Sep runs, those are about as round as 30 Sep, so most of the improvement against the earlier baselines comes from the microphone calibration, not the room.');
}


// Slide 8: the material measurements overlaid
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-materials.png', x: 0.45, y: 0.45, w: 6.37, h: 6.35, altText: 'Polar plot of ten material set-ups at 2000 microseconds, total level 500 Hz to 24 kHz: bare, cork, rubber, felt, felt with rubber, felt with PU foam, PU foam, double PU foam, 4 and 8 layers of Thinsulate' });
  s.addText('THE MATERIALS', { x: 7.2, y: 0.4, w: 5.6, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Materials at 2000 µs', { x: 7.2, y: 0.72, w: 5.6, h: 0.9, fontFace: 'Cambria', fontSize: 30, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  const items = [
    ['Bare', 74.2, '1F2A44', '2 Oct', 0.0],
    ['PU foam', 77.6, '862E9C', '7 Oct', 3.4],
    ['Felt + rubber', 78.2, '7048E8', '2 Oct', 4.1],
    ['PU foam, double layer', 78.2, '5C940D', '7 Oct', 4.1],
    ['Cork', 78.6, '2F9E44', '2 Oct', 4.4],
    ['Inner felt + outer PU foam', 78.8, 'C2255C', '7 Oct', 4.6],
    ['Thinsulate, 8 layers', 79.2, '1864AB', '7 Oct', 5.0],
    ['Felt', 79.3, '1098AD', '2 Oct', 5.2],
    ['Thinsulate, 4 layers', 79.4, 'E03131', '7 Oct', 5.2],
    ['Rubber', 80.3, 'F08C00', '2 Oct', 6.2],
  ];
  s.addText('Mean level. Round markers: 2 Oct. Square: 7 Oct.', { x: 7.2, y: 1.65, w: 5.6, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
  items.forEach(([name, mean, col, day, delta], i) => {
    const y = 2.05 + i * 0.37;
    s.addShape(pres.shapes.OVAL, { x: 7.2, y: y + 0.07, w: 0.2, h: 0.2, fill: { color: col }, line: { color: col, width: 0 } });
    s.addText(name, { x: 7.5, y, w: 3.0, h: 0.34, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, valign: 'middle', isTextBox: true });
    s.addText(day, { x: 10.55, y, w: 0.7, h: 0.34, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'middle', isTextBox: true });
    s.addText(mean.toFixed(1) + ' dB', { x: 11.2, y, w: 1.6, h: 0.34, fontFace: 'Calibri', fontSize: 14, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  });
  s.addText('+3.4 to +6.2 dB', { x: 7.2, y: 5.85, w: 5.6, h: 0.7, fontFace: 'Cambria', fontSize: 36, bold: true, color: RED, margin: 0, isTextBox: true });
  s.addText('louder than bare, on average (bare measured 2 Oct)', { x: 7.2, y: 6.5, w: 5.6, h: 0.3, fontFace: 'Calibri', fontSize: 13, color: INK, margin: 0, isTextBox: true });
  s.addText('2 and 7 Oct 2026, 5-inch 3-blade propeller, total level 500 Hz–24 kHz, motor at 2000 µs, corrected microphone files. Radial axis 68–89 dB.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('8', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Bases in the data repo. 2 Oct 2026: 2004__5in3b__unset__v1-naked-horizontal (bare), ...cork__v1-cork-horizontal, ...rubber__v1-rubber, ...felt__v1-felt, ...felt-rubber__v1-felt-rubber. 7 Oct 2026 (axii__5in3b__...): inner-felt-outer-open-pore-pu-foam, open-pore-pu-foam, open-pore-pu-foam-double-layer, thinsulate-4-layers, thinsulate-8-layers. Each capture is the PWM 2000 step; level per microphone is the total level 500 Hz to 24 kHz in dB SPL (was 100 Hz to 10 kHz on the earlier version of this slide), read with the corrected microphone files (all after 16 Sep). The polar is mirrored to 360 degrees. Mean over the eleven positions. The bare reference is from 2 Oct, so the 7 Oct materials are compared across days: the differences from bare are indicative, not a controlled comparison. The earlier 100 Hz-10 kHz version had a strong lobe at -90 degrees (94-98 dB); with the band from 500 Hz it is 78-87 dB and fits on the plot. Operating points (voltage, thrust) were not compared here.');
}

// Slide 9: the membrane measurements overlaid
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-membranes.png', x: 0.45, y: 0.45, w: 6.37, h: 6.35, altText: 'Polar plot of ten membrane set-ups at 2000 microseconds, total level 500 Hz to 24 kHz' });
  s.addText('THE MEMBRANES', { x: 7.2, y: 0.4, w: 5.6, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Membranes at 2000 µs', { x: 7.2, y: 0.72, w: 5.6, h: 0.9, fontFace: 'Cambria', fontSize: 30, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  const items = [
    ['Thinsulate, 4 layers', 82.8, 'E03131', '9 Oct'],
    ['Thinsulate, 2 layers', 84.0, 'F08C00', '9 Oct'],
    ['Thinsulate, 8 layers', 85.0, 'C2255C', '9 Oct'],
    ['Felt + rubber', 86.0, '7048E8', '9 Oct'],
    ['Felt', 86.3, '1098AD', '9 Oct'],
    ['Felt, double layer', 86.4, '1864AB', '9 Oct'],
    ['Duct + PU foam, double', 87.5, '5C940D', '9 Oct'],
    ['PU foam', 87.9, '862E9C', '8 Oct'],
    ['Cork', 88.5, '2F9E44', '9 Oct'],
    ['Duct, small', 89.5, '1F2A44', '8 Oct'],
  ];
  s.addText('Mean level. Round markers: 8 Oct. Square: 9 Oct.', { x: 7.2, y: 1.65, w: 5.6, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
  items.forEach(([name, mean, col, day], i) => {
    const y = 2.05 + i * 0.37;
    s.addShape(pres.shapes.OVAL, { x: 7.2, y: y + 0.07, w: 0.2, h: 0.2, fill: { color: col }, line: { color: col, width: 0 } });
    s.addText(name, { x: 7.5, y, w: 3.1, h: 0.34, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, valign: 'middle', isTextBox: true });
    s.addText(day, { x: 10.6, y, w: 0.7, h: 0.34, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'middle', isTextBox: true });
    s.addText(mean.toFixed(1) + ' dB', { x: 11.2, y, w: 1.6, h: 0.34, fontFace: 'Calibri', fontSize: 14, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  });
  s.addText('6.7 dB', { x: 7.2, y: 5.85, w: 5.6, h: 0.7, fontFace: 'Cambria', fontSize: 36, bold: true, color: RED, margin: 0, isTextBox: true });
  s.addText('between the quietest and loudest set-up, on average', { x: 7.2, y: 6.5, w: 5.6, h: 0.3, fontFace: 'Calibri', fontSize: 13, color: INK, margin: 0, isTextBox: true });
  s.addText('8 and 9 Oct 2026, 5-inch 3-blade propeller, 500 Hz–24 kHz, 2000 µs, mean of 3 repeats, corrected files. Axis 76–94 dB. Not comparable with slide 8.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('9', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Bases in the data repo (f30__5in3b__membrane-...): 8 Oct 2026: membrane-duct-small, membrane-open-pore-pu-foam. 9 Oct 2026: membrane-duct-open-pore-pu-foam-double-layer, membrane-felt, membrane-felt-double-layer, membrane-cork, membrane-felt-rubber, membrane-thinsulate-8-layers, -4-layers, -2-layers. Each base was captured with 3 repeats of the ramp; the plot uses the PWM 2000 step and the mean over the 3 repeats of the total level 500 Hz to 24 kHz per microphone, in dB SPL, read with the corrected microphone files. The repeat-to-repeat scatter of the mean level is 0.02-0.11 dB. There is no bare reference measured with this set-up (the base names carry a different motor field, f30, from the 2 and 7 Oct materials), so levels here are not comparable with slide 8 and no louder-than-bare figure is given; the callout is the spread between the quietest (Thinsulate 4 layers) and loudest (small membrane duct) set-up. Two of the bases are ducts. The polar is mirrored to 360 degrees.');
}

pres.writeFile({ fileName: 'chamber-slides-final.pptx' }).then(() => console.log('written'));
