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
  // diagram: loudspeaker -> microphone, swap with the other capsules
  s.addImage({ path: 'photo-source.jpg', x: 0.6, y: 2.3, w: 1.45, h: 1.65, sizing: { type: 'cover', w: 1.45, h: 1.65 }, altText: 'Our loudspeaker: a printed sphere with an 8 cm driver' });
  // the real UMIK-2 (miniDSP product photo), capsule end towards the loudspeaker
  s.addText('tones\n62 Hz–16 kHz', { x: 2.05, y: 2.75, w: 1.35, h: 0.5, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'center', margin: 0, valign: 'bottom', isTextBox: true });
  s.addShape(pres.shapes.LINE, { x: 2.15, y: 3.35, w: 1.35, h: 0, line: { color: RED, width: 2.5, dashType: 'dash', endArrowType: 'triangle' } });
  s.addText('UMIK-2 microphone', { x: 3.6, y: 2.4, w: 2.5, h: 0.3, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, isTextBox: true });
  s.addImage({ path: 'umik2-photo.png', x: 3.6, y: 2.95, w: 3.0, h: 0.811, altText: 'UMIK-2 measurement microphone at the mounting point, capsule end on the left facing the loudspeaker' });
  s.addText('capsule faces the loudspeaker', { x: 3.6, y: 3.88, w: 3.2, h: 0.28, fontFace: 'Calibri', fontSize: 13, color: BLUE, bold: true, margin: 0, isTextBox: true });
  s.addText('Our loudspeaker', { x: 0.4, y: 4.05, w: 1.85, h: 0.3, fontFace: 'Calibri', fontSize: 14, color: INK, align: 'center', margin: 0, isTextBox: true });
  // settings
  s.addText([
    { text: '97 tones per microphone, 62 Hz to 16 kHz, 12 per octave (a stepped sweep)', options: { bullet: true, breakLine: true } },
    { text: 'One tone at a time: 0.7 s to settle, then 2 s recorded (6 s below 250 Hz)', options: { bullet: true, breakLine: true } },
    { text: 'Microphones swapped in turn: same position, same loudspeaker, same level', options: { bullet: true, breakLine: true } },
    { text: 'One microphone measured three times as the reference', options: { bullet: true } },
  ], { x: 0.6, y: 4.85, w: 6.7, h: 1.95, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 6, isTextBox: true });
  // results
  s.addText([
    { text: '4.01', options: { color: RED } }, { text: ' → ', options: { color: MUTED } }, { text: '0.02 dB', options: { color: BLUE } },
  ], { x: 7.9, y: 1.95, w: 4.9, h: 0.8, fontFace: 'Cambria', fontSize: 44, bold: true, margin: 0, isTextBox: true });
  s.addText('spread across the eleven microphones for the same sound', { x: 7.9, y: 2.75, w: 4.9, h: 0.55, fontFace: 'Calibri', fontSize: 14, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addText('7 of 11 factory files were wrong by 0.6–3.6 dB', { x: 7.9, y: 3.3, w: 4.9, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, isTextBox: true });
  s.addText('Each factory file against the common reference, mean over frequency (dB): below 0 reads too quiet, above 0 too loud', { x: 7.9, y: 3.7, w: 4.9, h: 0.45, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  s.addChart(pres.charts.BAR, [{ name: 'Mean offset (dB)', labels: ['810-8893', '810-8904', '810-8901', '810-8897', '810-8900', '811-1896', '811-2321', '810-8903', '811-2310', '811-1897', '811-1892'], values: [1.25, 0.85, 0.84, 0.76, 0.23, 0.00, -0.09, -0.14, -0.78, -1.39, -2.59] }], {
    x: 7.8, y: 4.1, w: 5.0, h: 2.85, barDir: 'bar', chartColors: [BLUE], showLegend: false, showTitle: false,
    catAxisLabelPos: 'low', catAxisLabelFrequency: 1, catAxisLabelFontSize: 10, catAxisLabelColor: INK, catAxisLabelFontFace: 'Calibri',
    valAxisMinVal: -3, valAxisMaxVal: 2, valAxisMajorUnit: 1, valAxisLabelFontSize: 10, valAxisLabelColor: MUTED, valAxisLabelFontFace: 'Calibri',
    valGridLine: { color: 'E3E7EE', size: 0.5 }, catGridLine: { style: 'none' }, barGapWidthPct: 40,
    showValue: true, dataLabelFontSize: 10, dataLabelColor: INK, dataLabelFontFace: 'Calibri', dataLabelFormatCode: '0.0', dataLabelPosition: 'outEnd',
  });
  s.addText('Calibration session 16 Sep 2026, loudspeaker amplitude 0.03 of full scale. UMIK-2 photo: miniDSP product brief.', { x: 0.6, y: 6.95, w: 11.3, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addText('2', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Procedure (calibrator/session.py, 2026-09-16 session): each of the eleven UMIK-2 capsules was plugged in at the same mounting point in front of the loudspeaker and measured over 97 stepped tones, 62 Hz to 16 kHz (about 12 per octave), amplitude 0.03, 48 kHz sampling, 0.7 s settle and 2 s capture per tone (6 s below 250 Hz). Capsule 810-8904 was measured three full times (18:21, 18:30, 20:43) as the reference. The difference of each capsule from the reference was folded into its calibration curve; Sens Factors kept as in the factory files. The datum is the mean of four capsules whose factory files agree with measurement (810-8900, 810-8903, 811-1896, 811-2321). Bars: mean over frequency of how far each capsule read from that datum with its factory file (calibrator corrections csv). Spread 4.01 to 0.02 dB and 7 of 11 files wrong by 0.6-3.6 dB are from the project notes. Absolute level is not anchored: that needs a 94 dB calibrator.');
}

// Slide 2: the same polar with the 30 Sep measurement on top
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
  s.addText(String(3), { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });
  s.addNotes('Blue: 30 Sep propeller measurement (11.7 V, 7.3 A, thrust -4 N), read with the 16 Sep microphone corrections. Rms spread about the mean 1.45 dB against 2.05 dB for 31 Aug; range 4.0 dB (55.5 to 59.6 dB SPL) against 6.7 dB. The blue is about 11 dB lower because the motor ran at a different operating point. The 4 dB range of the blue is a bottom-louder trend. Honest caveat: with the same calibration applied to the 1-2 Sep runs, those are about as round as 30 Sep, so most of the improvement against the earlier baselines comes from the microphone calibration, not the room.');
}

pres.writeFile({ fileName: 'chamber-slides.pptx' }).then(() => console.log('written'));
