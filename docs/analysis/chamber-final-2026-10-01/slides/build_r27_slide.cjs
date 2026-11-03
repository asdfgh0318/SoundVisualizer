// One-slide deck in the style of slide 9 ("Membranes at 2000 µs"), for the r27 8-inch duct set-ups,
// with thrust and rpm beside each level. Data: r27.json and polar-r27.png from make_r27_fig.py.
//   NODE_PATH=<dir with pptxgenjs> node build_r27_slide.cjs
const pptxgen = require('pptxgenjs');
const R = require('./r27.json');
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';            // 13.33 x 7.5 in
pres.title = 'Duct linings, thrust and rpm';
const INK = '1F2A44', RED = 'D6336C', BLUE = '2B6CB0', MUTED = '5B6578';

const S = R.sets;
const items = Object.entries(S).sort((a, b) => a[1].mean - b[1].mean);
const bare = S['Bare prop, no duct'], duct = S['Duct, no lining'];
const lined = Object.entries(S).filter(([k]) => k.startsWith('Thinsulate'));
const best = lined.reduce((a, b) => (b[1].thrust > a[1].thrust ? b : a));
const loss = bare.thrust - duct.thrust, gain = best[1].thrust - duct.thrust;
const ducted = Object.entries(S).filter(([k]) => !k.startsWith('Bare'));
const dMin = Math.min(...ducted.map(([, v]) => v.mean)), dMax = Math.max(...ducted.map(([, v]) => v.mean));
const rMin = Math.min(...ducted.map(([, v]) => v.rpm)), rMax = Math.max(...ducted.map(([, v]) => v.rpm));
const pct = (x) => (100 * x).toFixed(0);
const front = Object.keys(duct.per_mic).filter((a) => +a >= -54);         // -72/-90 left out: probably in the flow
const dB = front.map((a) => best[1].per_mic[a] - duct.per_mic[a]);
const dMinB = Math.min(...dB), dMaxB = Math.max(...dB), dMeanB = dB.reduce((a, b) => a + b, 0) / dB.length;
const n = (x, d = 0) => x.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });

const s = pres.addSlide();
s.background = { color: 'FFFFFF' };
s.addImage({ path: 'polar-r27-zoom.png', x: 0.45, y: 0.45, w: 6.37, h: 6.35, altText: 'Polar plot of six 8-inch duct set-ups at 2000 microseconds, total level 500 Hz to 24 kHz, radial axis zoomed to the duct levels' });
s.addText('THE DUCT LININGS', { x: 7.2, y: 0.4, w: 5.8, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
s.addText('Duct linings at 2000 µs', { x: 7.2, y: 0.72, w: 5.8, h: 0.8, fontFace: 'Cambria', fontSize: 30, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText('Mean level. Square markers: 2 Nov. Round: 30 Oct. Bare prop off the plot.', { x: 7.2, y: 1.5, w: 5.8, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });

const X = { dot: 7.2, name: 7.47, day: 9.85, db: 10.4, th: 11.32, rpm: 12.12 };
const head = (t, x, w, align = 'right') => s.addText(t, { x, y: 1.83, w, h: 0.26, fontFace: 'Calibri', fontSize: 10, bold: true, color: MUTED, align, margin: 0, valign: 'bottom', isTextBox: true });
head('level', X.db, 0.85); head('thrust', X.th, 0.75); head('rpm', X.rpm, 0.85);
s.addShape(pres.shapes.LINE, { x: 7.2, y: 2.12, w: 5.77, h: 0, line: { color: 'C9CFD8', width: 0.75 } });
items.forEach(([name, v], i) => {
  const y = 2.18 + i * 0.36, col = v.color.replace('#', '');
  const isBare = name.startsWith('Bare');
  s.addShape(pres.shapes.OVAL, { x: X.dot, y: y + 0.08, w: 0.18, h: 0.18, fill: { color: col }, line: { color: col, width: 0 } });
  s.addText(name, { x: X.name, y, w: 2.4, h: 0.34, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, valign: 'middle', isTextBox: true });
  s.addText(v.day, { x: X.day, y, w: 0.6, h: 0.34, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.mean, 1) + ' dB', { x: X.db, y, w: 0.85, h: 0.34, fontFace: 'Calibri', fontSize: 13, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.thrust, 2) + ' N', { x: X.th, y, w: 0.75, h: 0.34, fontFace: 'Calibri', fontSize: 13, bold: true, color: isBare ? INK : (name === best[0] ? RED : INK), align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.rpm), { x: X.rpm, y, w: 0.85, h: 0.34, fontFace: 'Calibri', fontSize: 13, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
});

const yC = 2.18 + items.length * 0.36 + 0.12;
s.addText(`+${n(gain, 2)} N`, { x: 7.2, y: yC, w: 5.8, h: 0.55, fontFace: 'Cambria', fontSize: 28, bold: true, color: RED, margin: 0, isTextBox: true });
s.addText(`${best[0]} against the unlined duct: it wins back ${pct(gain / loss)} % of the ${n(loss, 2)} N the empty duct loses to the bare prop.`,
  { x: 7.2, y: yC + 0.55, w: 5.8, h: 0.42, fontFace: 'Calibri', fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText([
  { text: 'Every duct is louder: ', options: { bold: true } },
  { text: `${n(dMin, 1)}–${n(dMax, 1)} dB against ${n(bare.mean, 1)} dB bare, and spins ${n(rMin)}–${n(rMax)} rpm against ${n(bare.rpm)} rpm bare (+${(100 * (rMin / bare.rpm - 1)).toFixed(1)} to +${(100 * (rMax / bare.rpm - 1)).toFixed(1)} %).` },
], { x: 7.2, y: yC + 1.0, w: 5.8, h: 0.5, fontFace: 'Calibri', fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText([
  { text: `${best[0]} is also the quietest lining: `, options: { bold: true } },
  { text: `${n(-dMaxB, 1)}–${n(-dMinB, 1)} dB below the unlined duct from −54° to +90° (${n(-dMeanB, 1)} dB on average).` },
], { x: 7.2, y: yC + 1.48, w: 5.8, h: 0.45, fontFace: 'Calibri', fontSize: 11, color: INK, margin: 0, valign: 'top', isTextBox: true });

s.addText(`2 Nov 2026 (6 layers: 30 Oct), APC 8x4.5MR, AXI 2217/12, 500 Hz–24 kHz, 2000 µs, mean of 3 repeats. Axis ${R.zoom_axis[0]}–${R.zoom_axis[1]} dB. Grey: −90°/−72°, probably in the flow. rpm = stand × 60/7.`,
  { x: 0.6, y: 6.95, w: 11.6, h: 0.3, fontFace: 'Calibri', fontSize: 10, color: MUTED, margin: 0, isTextBox: true });
s.addText('1', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });

const lines = Object.entries(S).map(([k, v]) => `${k} (${v.day}, base ${v.base}): ${n(v.mean, 1)} dB (repeat-to-repeat spread of the mean ${v.repeat_spread} dB), thrust ${n(v.thrust, 2)} N (repeats ${v.thrust_min_max.join('–')}), ${n(v.rpm)} rpm (${v.rpm_min_max.join('–')}), ${n(v.current, 2)} A; per microphone from +90 to -90: ${Object.values(v.per_mic).join(', ')} dB.`);
s.addNotes(['All set-ups are the 8-inch APC 8x4.5MR on the AXI 2217/12 in the r27 duct, with the lining fitted the new way (from 30 Oct). Thinsulate 6 layers was last captured on 30 Oct; everything else on 2 Nov, so 6 layers is compared across days and is indicative only (on 2 Nov an untouched Thinsulate 8 read 0.08 N above its 30 Oct run, and Thinsulate 2 0.20 N). Each base: the PWM 2000 step of 3 repeats; level per microphone is the total level 500 Hz to 24 kHz in dB SPL with the corrected microphone files, mean over the 3 repeats, and the list gives the mean over the eleven positions. Thrust (the stand reads negative, shown as magnitude), rpm and current are the median of the second half of each step, mean over the 3 repeats; rpm is the stand reading (electrical) times 60/7 for the 14-pole motor. Duct and propeller are one piece on the stand, so the thrust includes the duct.',
  'The bare prop is quieter on average but its -90 degree microphone reads ' + bare.per_mic['-90'] + ' dB, the loudest single reading on the slide; the -72 and -90 positions vary run to run by about 1 dB even without a remount and probably sit in the flow, so their levels are less trustworthy than the rest of the arc.',
  ...lines].join('\n\n'));

pres.writeFile({ fileName: process.env.OUT || '2026-11-03 duct linings thrust rpm.pptx' }).then((f) => console.log('written', f));
