// One-slide deck in the style of slide 9 ("Membranes at 2000 µs"), for the r27 8-inch duct set-ups,
// with thrust and rpm beside each level. Data: r27.json and polar-r27-zoom.png from make_r27_fig.py.
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
// headline numbers only from the same day as the bare prop and the unlined duct (Adam's rule: days are not compared)
const sameDay = Object.entries(S).filter(([k, v]) => v.day === duct.day && !k.startsWith('Bare') && k !== 'Duct, no lining');
const best = sameDay.reduce((a, b) => (b[1].thrust > a[1].thrust ? b : a));
const loss = bare.thrust - duct.thrust, gain = best[1].thrust - duct.thrust;
const front = Object.keys(duct.per_mic).filter((a) => +a >= -54);         // -72/-90 left out: probably in the flow
const dB = front.map((a) => best[1].per_mic[a] - duct.per_mic[a]);
const dMeanB = dB.reduce((a, b) => a + b, 0) / dB.length;
const ducted = Object.entries(S).filter(([k]) => !k.startsWith('Bare'));
const dMin = Math.min(...ducted.map(([, v]) => v.mean)), dMax = Math.max(...ducted.map(([, v]) => v.mean));
const n = (x, d = 0) => x.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
const MARK = { '2 Nov': '■', '30 Oct': '●', '29 Oct': '◆', '28 Oct': '▲' };

const s = pres.addSlide();
s.background = { color: 'FFFFFF' };
s.addImage({ path: 'polar-r27-zoom.png', x: 0.45, y: 0.45, w: 6.37, h: 6.35, altText: 'Polar plot of ten 8-inch duct set-ups at 2000 microseconds, total level 500 Hz to 24 kHz, radial axis zoomed to the duct levels' });
s.addText('THE DUCT LININGS', { x: 7.2, y: 0.35, w: 5.8, h: 0.35, fontFace: 'Calibri', fontSize: 14, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
s.addText('Duct linings at 2000 µs', { x: 7.2, y: 0.67, w: 5.8, h: 0.75, fontFace: 'Cambria', fontSize: 30, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText('Mean level. Markers: ■ 2 Nov, ● 30 Oct, ◆ 29 Oct, ▲ 28 Oct. † lining fitted the old way (before 30 Oct). Bare prop off the plot.',
  { x: 7.2, y: 1.38, w: 5.8, h: 0.45, fontFace: 'Calibri', fontSize: 11, color: MUTED, margin: 0, valign: 'top', isTextBox: true });

const X = { dot: 7.2, name: 7.43, day: 9.72, db: 10.38, th: 11.3, rpm: 12.12 };
const RH = 0.29, Y0 = 2.12;
const head = (t, x, w) => s.addText(t, { x, y: 1.83, w, h: 0.24, fontFace: 'Calibri', fontSize: 10, bold: true, color: MUTED, align: 'right', margin: 0, valign: 'bottom', isTextBox: true });
head('level', X.db, 0.85); head('thrust', X.th, 0.75); head('rpm', X.rpm, 0.85);
s.addShape(pres.shapes.LINE, { x: 7.2, y: 2.08, w: 5.77, h: 0, line: { color: 'C9CFD8', width: 0.75 } });
items.forEach(([name, v], i) => {
  const y = Y0 + i * RH, col = v.color.replace('#', '');
  s.addShape(pres.shapes.OVAL, { x: X.dot, y: y + 0.065, w: 0.16, h: 0.16, fill: { color: col }, line: { color: col, width: 0 } });
  s.addText(name + (v.old_fit ? ' †' : ''), { x: X.name, y, w: 2.3, h: RH, fontFace: 'Calibri', fontSize: 12.5, bold: true, color: INK, margin: 0, valign: 'middle', isTextBox: true });
  s.addText(`${MARK[v.day] || ''} ${v.day}`, { x: X.day, y, w: 0.7, h: RH, fontFace: 'Calibri', fontSize: 10, color: v.old_fit ? '8A94A6' : MUTED, margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.mean, 1) + ' dB', { x: X.db, y, w: 0.85, h: RH, fontFace: 'Calibri', fontSize: 12, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.thrust, 2) + ' N', { x: X.th, y, w: 0.75, h: RH, fontFace: 'Calibri', fontSize: 12, bold: true, color: name === best[0] ? RED : INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.rpm), { x: X.rpm, y, w: 0.85, h: RH, fontFace: 'Calibri', fontSize: 12, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
});

const yC = Y0 + items.length * RH + 0.08;
s.addText(`+${n(gain, 2)} N`, { x: 7.2, y: yC, w: 1.9, h: 0.5, fontFace: 'Cambria', fontSize: 26, bold: true, color: RED, margin: 0, valign: 'middle', isTextBox: true });
s.addText(`${best[0]} against the unlined duct, both ${duct.day}: wins back ${(100 * gain / loss).toFixed(0)} % of the ${n(loss, 2)} N the empty duct loses to the bare prop, and is ${n(-dMeanB, 1)} dB quieter from −54° to +90°.`,
  { x: 9.1, y: yC, w: 3.9, h: 0.55, fontFace: 'Calibri', fontSize: 10.5, color: INK, margin: 0, valign: 'middle', isTextBox: true });
s.addText([
  { text: 'Every duct is louder than the bare prop: ', options: { bold: true } },
  { text: `${n(dMin, 1)}–${n(dMax, 1)} dB against ${n(bare.mean, 1)} dB. Set-ups marked † are from other days and the old fit: indicative only.` },
], { x: 7.2, y: yC + 0.6, w: 5.8, h: 0.45, fontFace: 'Calibri', fontSize: 10.5, color: INK, margin: 0, valign: 'top', isTextBox: true });

s.addText(`28 Oct–2 Nov 2026, APC 8x4.5MR, AXI 2217/12, 500 Hz–24 kHz, 2000 µs, mean of 3 repeats. Axis ${R.zoom_axis[0]}–${R.zoom_axis[1]} dB. Grey: −90°/−72°, probably in the flow. rpm = stand × 60/7.`,
  { x: 0.6, y: 6.95, w: 11.6, h: 0.3, fontFace: 'Calibri', fontSize: 10, color: MUTED, margin: 0, isTextBox: true });
s.addText('1', { x: 12.2, y: 6.95, w: 0.5, h: 0.3, fontFace: 'Calibri', fontSize: 12, color: MUTED, align: 'right', margin: 0, isTextBox: true });

const lines = Object.entries(S).map(([k, v]) => `${k} (${v.day}${v.old_fit ? ', old fit' : ''}, base ${v.base}): ${n(v.mean, 1)} dB (repeat-to-repeat spread of the mean ${v.repeat_spread} dB), thrust ${n(v.thrust, 2)} N (repeats ${v.thrust_min_max.join('–')}), ${n(v.rpm)} rpm (${v.rpm_min_max.join('–')}), ${n(v.current, 2)} A; per microphone from +90 to -90: ${Object.values(v.per_mic).join(', ')} dB.`);
s.addNotes(['All set-ups are the 8-inch APC 8x4.5MR on the AXI 2217/12 in the r27 duct. The bare prop, the unlined duct and Thinsulate 2/4/8/10 are from 2 Nov; Thinsulate 6 from 30 Oct; felt from 28 Oct; felt double, felt double + rubber and rubber from 29 Oct. The linings from 28-29 Oct were fitted the old way: with the new fit (from 30 Oct) the Thinsulates gave 8-26 % more thrust than their old-fit runs, so the felt and rubber values are probably low and are not comparable with the rest. Only the 2 Nov set-ups are compared with each other (the headline numbers). Each base: the PWM 2000 step of 3 repeats; level per microphone is the total level 500 Hz to 24 kHz in dB SPL with the corrected microphone files, mean over the 3 repeats, and the list gives the mean over the eleven positions. Thrust (the stand reads negative, shown as magnitude), rpm and current are the median of the second half of each step, mean over the 3 repeats; rpm is the stand reading (electrical) times 60/7 for the 14-pole motor. Duct and propeller are one piece on the stand, so the thrust includes the duct.',
  'The radial axis is zoomed to the ducted set-ups, so the bare prop (74-80 dB at most positions, 96.1 dB at -90 degrees) is not drawn. The -90 and -72 degree positions vary run to run by about 1 dB even without a remount and probably sit in the flow, so their levels are less trustworthy than the rest of the arc.',
  ...lines].join('\n\n'));

pres.writeFile({ fileName: process.env.OUT || '2026-11-03 duct linings thrust rpm.pptx' }).then((f) => console.log('written', f));
