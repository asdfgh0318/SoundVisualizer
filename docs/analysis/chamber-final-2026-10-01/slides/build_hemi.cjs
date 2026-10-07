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
  [H('Band'), H('Limit'), H('Tones'), H('Bare floor', { colspan: 2, color: RED, border: [GRID, GRID, GRID, SEP] }), H('Carpet on it', { colspan: 2, color: INK, border: [GRID, GRID, GRID, SEP] }), H('Final state', { colspan: 2, color: BLUE, border: [GRID, GRID, GRID, SEP] })],
  [H('Hz'), H('± dB'), H('per band'), H('worst mic, dB', G()), H('cells in limit'), H('worst mic, dB', G()), H('cells in limit'), H('worst mic, dB', G()), H('cells in limit')],
];
T.rows.forEach((r) => rows.push([C(r.band, null, { bold: true }), C(r.limit.toFixed(1), null), C(String(r.tones), null)].concat(['bare', 'carpet', 'final'].flatMap((k) => [C(r[k][0].toFixed(2), r[k][1], G({ bold: true })), C(r[k][2] + ' %', r[k][3])]))));
s.addTable(rows, { x: 0.45, y: 0.4, w: 8.6, colW: [0.8, 0.65, 0.8, 1.15, 1.0, 1.15, 1.0, 1.15, 0.9], rowH: [0.34, 0.5].concat(Array(T.rows.length).fill(0.4)), margin: [0.02, 0.03, 0.02, 0.03] });
s.addText('WHERE WE STAND', { x: 9.4, y: 0.45, w: 3.6, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
s.addText('Against the hemi-anechoic ISO values', { x: 9.4, y: 0.8, w: 3.6, h: 1.4, fontFace: 'Cambria', fontSize: 24, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText('Limits: ±2.5 dB up to 630 Hz, ±2.0 dB from 800 to 5000 Hz, ±3.0 dB at 6300 Hz. Colour: worst microphone as a share of the limit (yellow at the limit, red at twice).', { x: 9.4, y: 2.25, w: 3.6, h: 1.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
const c = T.card;
s.addText([
  { text: 'Bands over the limit (of 13)', options: { bold: true, breakLine: true } },
  { text: `Bare floor ${c.bare.over}  →  carpet ${c.carpet.over}  →  final ${c.final.over}`, options: { breakLine: true } },
  { text: 'Cells in limit (13 bands)', options: { bold: true, breakLine: true } },
  { text: `${c.bare.cells} %  →  ${c.carpet.cells} %  →  ${c.final.cells} %`, options: { breakLine: true } },
  { text: 'Room error below 3 kHz', options: { bold: true, breakLine: true } },
  { text: `${c.bare.score.toFixed(2)}  →  ${c.carpet.score.toFixed(2)}  →  ${c.final.score.toFixed(2)} dB` },
], { x: 9.4, y: 3.6, w: 3.6, h: 2.3, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', paraSpaceAfter: 3, isTextBox: true });
s.addText('Bare floor: 24 Sep, wedges off the floor, flat foam base only. Carpet: same afternoon, source unmoved. Final: 25 Sep (other day, source position not documented). * Partial bands: tones above 5 kHz only; 3–5 kHz left out because of the loudspeaker. ISO values are an analogue, not a qualification. Hemi limits: Winker & Stahnke 2016, Table 1 (quoting ISO 3745:2012).', { x: 0.45, y: 6.95, w: 12.5, h: 0.45, fontFace: 'Calibri', fontSize: 10, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
s.addNotes('Hemi-anechoic tolerance values of ISO 3745:2012 as printed in Winker and Stahnke 2016, Table 1 (and Kayhan 2008 p. 13): +-2.5 dB up to 630 Hz, +-2.0 dB for 800 to 5000 Hz, +-3.0 dB from 6300 Hz. They are looser than the anechoic values (+-1.5 / +-1.0 / +-1.5) used elsewhere in this deck. Our floor is treated, so the anechoic row remains the stricter and primary reading; this slide shows where the room stands if judged as a hemi-anechoic one. Bare floor = 2026-09-24/floor-no-wedges (14:05, flat foam base, wedges off), carpet = 2026-09-24/chaotic-carpet (14:32), final = 2026-09-25/carpet-reordered. Bare floor and carpet are the same-source pair; the final state is another day. Same method as the colour table slide: worst microphone band-mean deviation from the arc mean, and the share of tone x microphone cells inside the limit.');
pres.writeFile({ fileName: 'hemi-slide.pptx' }).then(() => console.log('written'));
