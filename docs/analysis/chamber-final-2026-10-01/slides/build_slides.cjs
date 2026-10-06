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
