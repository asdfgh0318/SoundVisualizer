const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';            // 13.33 x 7.5 in
pres.title = 'Chamber measurements';
const INK = '1F2A44', RED = 'D6336C', BLUE = '2B6CB0', MUTED = '5B6578';

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
  s.addText(String(1), { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
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
  s.addText('7 of 11 factory files were wrong by 0.6–3.6 dB', { x: 8.2, y: 6.35, w: 4.6, h: 0.5, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Calibration session 16 Sep 2026, loudspeaker amplitude 0.03 of full scale. UMIK-2 photo: miniDSP product brief.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('2', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Procedure (calibrator/session.py, 2026-09-16 session): each of the eleven UMIK-2 capsules was plugged in at the same mounting point in front of the loudspeaker and measured over 97 stepped tones, 62 Hz to 16 kHz (about 12 per octave), amplitude 0.03, 48 kHz sampling, 0.7 s settle and 2 s capture per tone (6 s below 250 Hz). Capsule 810-8904 was measured three full times (18:21, 18:30, 20:43) as the reference. The difference of each capsule from the reference was folded into its calibration curve; Sens Factors kept as in the factory files. The datum is the mean of four capsules whose factory files agree with measurement (810-8900, 810-8903, 811-1896, 811-2321). Spread 4.01 to 0.02 dB and 7 of 11 files wrong by 0.6-3.6 dB are from the project notes. Seven capsules had a mean offset beyond 0.6 dB (811-1892 -2.6, 811-1897 -1.4, 811-2310 -0.8, 810-8897 +0.8, 810-8901 +0.8, 810-8904 +0.9, 810-8893 +1.3). Absolute level is not anchored: that needs a 94 dB calibrator.');
}

// Slide 3: the waterfalls of the calibration, before and after
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'fig-mic-slide.png', x: 0.35, y: 0.3, w: 8.2, h: 6.38, altText: 'Maps of each microphone against frequency for two captures: factory files (top), corrected (middle), effect of the correction (bottom)' });
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
  s.addText('range of the microphones’ mean levels, start of day 3 (final state: 4.1 → 1.0 dB)', { x: 8.95, y: 6.25, w: 3.9, h: 0.6, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('Captures from 25 Sep 2026: day3-a (left) and carpet-reordered (right).', { x: 0.6, y: 6.95, w: 8.0, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('3', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Same figure as chapter 1 of the report, redrawn larger. The same two captures were calibrated two ways: with the factory files and with the corrections measured on 16 Sep. The span is the range of the capsules mean levels: 4.3 to 0.8 dB at the start of day 3, 4.1 to 1.0 dB in the final configuration. Room error below 3 kHz: 2.277 to 1.997 dB and 1.736 to 1.387 dB. The change is mainly a per-capsule offset, so it mainly moves whole rows.');
}

// Slide 4: the chamber treatments, day 3 start against the final state
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'fig-wf-slide.png', x: 0.35, y: 0.3, w: 7.61, h: 6.45, altText: 'Maps of each microphone against frequency: start of day 3, final state, and the change between them' });
  s.addText('THE CHAMBER', { x: 8.95, y: 0.5, w: 3.9, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('The treatments flatten the low end', { x: 8.95, y: 0.85, w: 3.9, h: 1.2, fontFace: 'Cambria', fontSize: 28, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addChart(pres.charts.BAR, [
    { name: 'Start of day 3', labels: ['250–400', '400–630', '630–1k', '1k–1.6k', '1.6k–3k', '5k–6.4k'], values: [3.33, 2.57, 1.57, 0.8, 0.87, 1.04] },
    { name: 'Final', labels: ['250–400', '400–630', '630–1k', '1k–1.6k', '1.6k–3k', '5k–6.4k'], values: [1.99, 1.52, 1.47, 0.85, 0.96, 1.17] },
  ], {
    x: 8.85, y: 2.05, w: 4.1, h: 2.75, barDir: 'col', barGrouping: 'clustered', chartColors: ['9AA5B8', '1F2A44'], showLegend: true, legendPos: 'b', legendFontSize: 11, legendColor: INK, legendFontFace: 'Calibri',
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
  s.addText('25 Sep 2026. The loudspeaker was moved during the day and returned to about its starting point; the position was not documented.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('4', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Same pair as page 3 of the report (day3-a at 13:17, carpet-reordered at 19:15, both 25 Sep), read with the corrected microphone files. Room error is the rms deviation of the eleven microphones from their mean, per band. Below 630 Hz the rms room error fell from 2.98 to 1.78 dB (1.2 dB, 40 %); between 1 and 3 kHz it went 0.84 to 0.91 dB. Start of day 3: 3.33, 2.57, 1.57, 0.80, 0.87, 1.04 dB; final: 1.99, 1.52, 1.47, 0.85, 0.96, 1.17 dB for the bands 250-400, 400-630, 630-1000, 1000-1600, 1600-3000 and 5000-6400 Hz. Caveat from the report: the loudspeaker was moved on purpose during the day (20 cm closer, into the ring plane, 5 cm back) and then returned to about its starting mounting point, which was not recorded. The tilt of the map changed from -0.41 to -0.63 and the mean level rose 1.16 dB, so the gain is the treatments plus a small unknown difference in source position, and part of it may be the louder direct sound. The clean pair with an unmoved source is 24 Sep: empty floor 2.054 to carpet 1.317 dB.');
}

// Slide 5: the band table of the evaluation, colour graded
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
  T.rows.forEach((r) => rows.push([C(String(r.band), null, { bold: true }), C(String(r.limit), null), C(String(r.tones), null), C(r.gdev.toFixed(2), r.gdevc, { bold: true, border: [GRID, GRID, GRID, SEP] }), C(r.gcells + ' %', r.gcellsc), C(r.xdev.toFixed(2), r.xdevc, { bold: true, border: [GRID, GRID, GRID, SEP] }), C(r.xcells + ' %', r.xcellsc)]));
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
  s.addText('* Partial bands: only the tones above 5 kHz are measured (4 and 5 tones). 3–5 kHz is left out because of the loudspeaker: its cone rocks near 4.4 kHz. ISO values are an analogue, not a qualification of the room.', { x: 8.95, y: 5.75, w: 3.9, h: 1.15, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('5', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Same table as page 4 of the report. Each one-third-octave band is judged against the anechoic tolerance values of ISO 5305 Table 1 (also ISO 3745 as printed by Cunefare 2003): +-1.5 dB for 125-630 Hz, +-1.0 dB for 800-5000 Hz. The number is the worst microphone band-mean deviation from the arc mean, in dB; the colour is that number as a share of the limit. Cells in limit counts tone x microphone cells inside the limit (3 tones x 11 microphones = 33 cells at 250 Hz, where the grid starts at 257 Hz). This is an analogue: the standards use a traverse and test decay with distance, we use eleven fixed microphones at one radius. The room is treated and not qualified. Within the tolerance values from 1250 Hz at the start of day 3 and from 2000 Hz in the final state, up to 2500 Hz. The rows marked * (5000 and 6300 Hz) are partial: 4 and 5 tones above 5 kHz, the limit is +-1.0 dB at 5000 Hz and +-1.5 dB at 6300 Hz (ISO 5305 Table 1). Both are over the limit in both states (1.24 and 1.23 dB; 1.59 and 1.77 dB). The 3150 and 4000 Hz bands are not shown: no tones between 3 and 5 kHz because of the rocking mode of the sphere at about 4.4 kHz. Caveat: the loudspeaker position was not documented across the day.');
}

// Slide 6: the same polar with the 30 Sep measurement on top
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-both.png', x: 0.6, y: 0.5, w: 5.95, h: 6.34, altText: 'Polar plot of 20 to 560 Hz: the jagged red 31 Aug outline and the smoother blue 30 Sep outline' });
  s.addText('AFTER', { x: 7.4, y: 0.9, w: 5.3, h: 0.4, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('The new polar is rounder', { x: 7.4, y: 1.3, w: 5.3, h: 1.3, fontFace: 'Cambria', fontSize: 34, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText([
    { text: 'Same kind of measurement, same axes, on 30 Sep.', options: { bullet: true, breakLine: true } },
    { text: 'The microphones now carry their measured corrections, and the room has been treated.', options: { bullet: true, breakLine: true } },
    { text: 'The outline is smooth and close to a circle.', options: { bullet: true, bold: true } },
  ], { x: 7.4, y: 2.75, w: 5.3, h: 2.6, fontFace: 'Calibri', fontSize: 16, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 10, isTextBox: true });
  s.addText([
    { text: '6.7', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '4.0 dB', options: { color: BLUE } },
  ], { x: 7.4, y: 5.5, w: 5.3, h: 0.8, fontFace: 'Cambria', fontSize: 48, bold: true, margin: 0, isTextBox: true });
  s.addText('between the loudest and quietest microphone', { x: 7.4, y: 6.3, w: 5.3, h: 0.5, fontFace: 'Calibri', fontSize: 14, color: MUTED, margin: 0, isTextBox: true });
  s.addText('20–560 Hz, motor at 2000 µs. The two runs had different operating points (7.35 V against 11.7 V), which is why the blue is lower.', { x: 0.6, y: 6.95, w: 12.1, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText(String(6), { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Blue: 30 Sep propeller measurement (11.7 V, 7.3 A, thrust -4 N), read with the 16 Sep microphone corrections. Rms spread about the mean 1.45 dB against 2.05 dB for 31 Aug; range 4.0 dB (55.5 to 59.6 dB SPL) against 6.7 dB. The blue is about 11 dB lower because the motor ran at a different operating point. The 4 dB range of the blue is a bottom-louder trend. Honest caveat: with the same calibration applied to the 1-2 Sep runs, those are about as round as 30 Sep, so most of the improvement against the earlier baselines comes from the microphone calibration, not the room.');
}


// Slide 7: the material measurements overlaid
{
  const s = pres.addSlide();
  s.background = { color: 'FFFFFF' };
  s.addImage({ path: 'polar-materials.png', x: 0.45, y: 0.45, w: 6.31, h: 6.35, altText: 'Polar plot of five material set-ups at 2000 microseconds: naked, cork, rubber, felt and felt with rubber' });
  s.addText('THE MATERIALS', { x: 7.6, y: 0.7, w: 5.2, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText('Material measurements at 2000 µs', { x: 7.6, y: 1.05, w: 5.2, h: 1.3, fontFace: 'Cambria', fontSize: 30, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  const items = [
    ['Naked', 74.2, '1F2A44'],
    ['Cork', 78.7, '2F9E44'],
    ['Rubber', 80.6, 'F08C00'],
    ['Felt', 79.5, 'D6336C'],
    ['Felt + rubber', 78.7, '7048E8'],
  ];
  s.addText('Mean level over the eleven microphones', { x: 7.6, y: 2.55, w: 5.2, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
  items.forEach(([name, mean, col], i) => {
    const y = 2.95 + i * 0.5;
    s.addShape(pres.shapes.OVAL, { x: 7.6, y: y + 0.07, w: 0.26, h: 0.26, fill: { color: col }, line: { color: col, width: 0 } });
    s.addText(name, { x: 8.05, y, w: 2.6, h: 0.4, fontFace: 'Calibri', fontSize: 18, bold: true, color: INK, margin: 0, valign: 'middle', isTextBox: true });
    s.addText(mean.toFixed(1) + ' dB', { x: 10.6, y, w: 2.2, h: 0.4, fontFace: 'Calibri', fontSize: 18, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  });
  s.addText('At −90°, in the outflow (off the scale on the plot), all five meet at 94–98 dB. Every lined set-up reads 4.5–6.4 dB higher on average than the naked one.', { x: 7.6, y: 5.6, w: 5.2, h: 1.0, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s.addText('2 Oct 2026, 5-inch 3-blade propeller, total level 100 Hz–10 kHz, motor at 2000 µs, corrected microphone files. Radial axis 69–84 dB.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('7', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Bases of 2 Oct 2026 in the data repo: 2004__5in3b__unset__v1-naked-horizontal, ...cork__v1-cork-horizontal, ...rubber__v1-rubber, ...felt__v1-felt, ...felt-rubber__v1-felt-rubber. Each capture is the PWM 2000 step; level per microphone is the total level 100 Hz to 10 kHz in dB SPL, read with the corrected microphone files (all after 16 Sep). The polar is mirrored to 360 degrees. Mean over the eleven positions: naked 74.2, cork 78.7, rubber 80.6, felt 79.5, felt plus rubber 78.7 dB. At -90 degrees (the outflow) all five are 93.7 to 98.3 dB. The slide shows levels as measured; operating points (voltage, thrust) were not compared here.');
}

pres.writeFile({ fileName: 'chamber-slides.pptx' }).then(() => console.log('written'));
