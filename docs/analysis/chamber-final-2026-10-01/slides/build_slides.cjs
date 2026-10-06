const pptxgen = require('pptxgenjs');
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';            // 13.33 x 7.5 in
pres.title = 'Chamber measurements';
const INK = '1F2A44', RED = 'D6336C', MUTED = '5B6578';

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
  s.addText('31 Aug 2026, 20–560 Hz, motor at 2000 µs. Radial axis zoomed to 56–72 dB.', { x: 0.6, y: 6.95, w: 12.1, h: 0.3, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, isTextBox: true });
  s.addNotes('Data: the 31 Aug 2026 horizontal baseline (arc laid flat, propeller axis vertical), propeller at PWM 2000, total level 20-560 Hz per microphone, read with the factory calibration files as it was measured. Rms spread about the mean 2.05 dB, range 6.7 dB (63.9 to 70.6 dB SPL). The radial axis is zoomed to 56-72 dB so the outline is visible; on a 0-80 dB axis the same curve looks much rounder.');
}

pres.writeFile({ fileName: 'chamber-slides.pptx' }).then(() => console.log('written'));
