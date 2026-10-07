const pptxgen = require('pptxgenjs');
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.title = 'Hemi-anechoic tolerance';
const INK = '1F2A44', RED = 'D6336C', BLUE = '2B6CB0', MUTED = '5B6578';
const T = JSON.parse(require('fs').readFileSync('hemi.json', 'utf8'));
const s = pres.addSlide(); s.background = { color: 'FFFFFF' };
const GRID = { type: 'solid', pt: 0.75, color: '9AA5B8' }, SEP = { type: 'solid', pt: 2, color: '4A5568' };
const H = (t, o = {}) => ({ text: t, options: Object.assign({ bold: true, fontFace: 'Calibri', fontSize: 12, color: INK, align: 'center', valign: 'middle', border: [GRID, GRID, GRID, GRID] }, o) });
const C = (t, fill, o = {}) => ({ text: t, options: Object.assign({ fontFace: 'Calibri', fontSize: 13, color: INK, align: 'center', valign: 'middle', fill: fill ? { color: fill } : undefined, border: [GRID, GRID, GRID, GRID] }, o) });
const G = (o = {}) => Object.assign({ border: [GRID, GRID, GRID, SEP] }, o);
const rows = [
  [H('Band'), H('Limit'), H('Tones'), H('Bare floor', { colspan: 2, color: RED, border: [GRID, GRID, GRID, SEP] })],
  [H('Hz'), H('± dB'), H('per band'), H('worst mic, dB', G()), H('cells in limit')],
];
T.rows.forEach((r) => rows.push([C(r.band, null, { bold: true }), C(r.limit.toFixed(1), null), C(String(r.tones), null), C(r.bare[0].toFixed(2), r.bare[1], G({ bold: true })), C(r.bare[2] + ' %', r.bare[3])]));
s.addTable(rows, { x: 0.45, y: 0.4, w: 6.6, colW: [0.9, 0.8, 1.0, 2.0, 1.9], rowH: [0.34, 0.5].concat(Array(T.rows.length).fill(0.4)), margin: [0.02, 0.03, 0.02, 0.03] });
s.addText('BARE FLOOR', { x: 7.45, y: 0.45, w: 5.4, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
s.addText('Against the hemi-anechoic ISO values', { x: 7.45, y: 0.8, w: 5.4, h: 1.0, fontFace: 'Cambria', fontSize: 26, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText('Limits: ±2.5 dB up to 630 Hz, ±2.0 dB from 800 to 5000 Hz, ±3.0 dB at 6300 Hz. Colour: worst microphone as a share of the limit (yellow at the limit, red at twice).', { x: 7.45, y: 1.9, w: 5.4, h: 0.9, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
const c = T.card.bare;
s.addText([
  { text: `${c.over} of 13 bands over the limit  ·  ${c.cells} % of cells in limit`, options: { bold: true, breakLine: true } },
  { text: `Room error below 3 kHz: ${c.score.toFixed(2)} dB` },
], { x: 7.45, y: 2.85, w: 5.4, h: 0.8, fontFace: 'Calibri', fontSize: 15, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 4, isTextBox: true });
s.addText('How the floor should look in a hemi-anechoic room', { x: 7.45, y: 3.85, w: 5.4, h: 0.35, fontFace: 'Calibri', fontSize: 15, bold: true, color: INK, margin: 0, isTextBox: true });
s.addText('A hemi-anechoic room has a hard, reflecting floor, for example a concrete slab, with absorbing walls and ceiling. The floor is part of the intended sound field and is not treated. Ours is different: the foam base is still on the floor, so the floor still absorbs and this test is not a true hemi-anechoic one.', { x: 7.45, y: 4.25, w: 5.4, h: 1.9, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText('Bare floor: 24 Sep 14:05, wedges off the floor, flat foam base left. * Partial bands: tones above 5 kHz only; 3–5 kHz left out because of the loudspeaker. ISO values are an analogue, not a qualification. Hemi limits: Winker & Stahnke 2016, Table 1 (quoting ISO 3745:2012). Reflecting floor: Nardari 2019, p. 2.', { x: 0.45, y: 6.95, w: 12.4, h: 0.45, fontFace: 'Calibri', fontSize: 10, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
s.addNotes('Hemi-anechoic tolerance values of ISO 3745:2012 as printed in Winker and Stahnke 2016, Table 1 (and Kayhan 2008 p. 13): +-2.5 dB up to 630 Hz, +-2.0 dB for 800 to 5000 Hz, +-3.0 dB from 6300 Hz. They are looser than the anechoic values (+-1.5 / +-1.0 / +-1.5) used elsewhere. Bare floor = 2026-09-24/floor-no-wedges (14:05): wedges removed from the floor, the flat foam base left. A hemi-anechoic room has a reflecting floor (Nardari 2019, p. 2 describes a hemi-anechoic room whose walls and ceiling are foam-treated while the floor, a thick concrete slab, is left untreated and reflective), so this run is the nearest we have but not a true hemi test: a true one would remove the foam base as well. Method as in the colour table slide: worst microphone band-mean deviation from the arc mean, and the share of tone x microphone cells inside the limit.');
pres.writeFile({ fileName: 'hemi-slide.pptx' }).then(() => console.log('written'));
