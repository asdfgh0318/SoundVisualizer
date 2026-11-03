// One A3-landscape slide in the style of slide 9 ("Membranes at 2000 µs"), for the r27 8-inch duct set-ups,
// with thrust and rpm beside each level. Data: r27.json and polar-r27-zoom.png from make_r27_fig.py.
//   NODE_PATH=<dir with pptxgenjs> node build_r27_slide.cjs
const pptxgen = require('pptxgenjs');
const R = require('./r27.json');
const pres = new pptxgen();
pres.defineLayout({ name: 'A3_LANDSCAPE', width: 16.54, height: 11.69 });   // 420 x 297 mm, so all thirteen set-ups fit
pres.layout = 'A3_LANDSCAPE';
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
const inlet = S['Duct + inlet, no lining'];
const iDelta = Object.keys(duct.per_mic).map((a) => inlet.per_mic[a] - duct.per_mic[a]);
const frontMean = (a, b) => { const k = Object.keys(b.per_mic).filter((x) => +x >= -54); return k.reduce((t, x) => t + a.per_mic[x] - b.per_mic[x], 0) / k.length; };
const iLined = Object.entries(S).filter(([k]) => k.startsWith('Inlet + '));
const ducted = Object.entries(S).filter(([k]) => !k.startsWith('Bare'));
const dMin = Math.min(...ducted.map(([, v]) => v.mean)), dMax = Math.max(...ducted.map(([, v]) => v.mean));
const n = (x, d = 0) => x.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }).replace('-', '−');
const MARK = { '3 Nov': '★', '2 Nov': '■', '30 Oct': '●', '29 Oct': '◆', '28 Oct': '▲' };

const s = pres.addSlide();
s.background = { color: 'FFFFFF' };
s.addImage({ path: 'polar-r27-zoom.png', x: 0.35, y: 1.2, w: 8.7, h: 8.67, altText: 'Polar plot of thirteen 8-inch duct set-ups at 2000 microseconds, total level 500 Hz to 24 kHz, radial axis zoomed to the duct levels' });
const L = 9.3, W = 6.75;                                                    // right column
s.addText('THE DUCT LININGS', { x: L, y: 0.6, w: W, h: 0.4, fontFace: 'Calibri', fontSize: 16, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
s.addText('Duct linings at 2000 µs', { x: L, y: 0.98, w: W, h: 0.85, fontFace: 'Cambria', fontSize: 38, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText('Mean level over the arc. Markers: ★ 3 Nov, ■ 2 Nov, ● 30 Oct, ◆ 29 Oct, ▲ 28 Oct. † lining fitted the old way (before 30 Oct). The bare prop is off the plot.',
  { x: L, y: 1.9, w: W, h: 0.6, fontFace: 'Calibri', fontSize: 13, color: MUTED, margin: 0, valign: 'top', isTextBox: true });

const X = { dot: L, name: L + 0.3, day: L + 3.1, db: L + 3.9, th: L + 4.95, rpm: L + 5.9 };
const RH = 0.285, Y0 = 2.9;
const head = (t, x, w) => s.addText(t, { x, y: 2.52, w, h: 0.3, fontFace: 'Calibri', fontSize: 12, bold: true, color: MUTED, align: 'right', margin: 0, valign: 'bottom', isTextBox: true });
head('level', X.db, 0.95); head('thrust', X.th, 0.85); head('rpm', X.rpm, 0.85);
s.addShape(pres.shapes.LINE, { x: L, y: 2.85, w: W, h: 0, line: { color: 'C9CFD8', width: 1 } });
items.forEach(([name, v], i) => {
  const y = Y0 + i * RH, col = v.color.replace('#', '');
  s.addShape(pres.shapes.OVAL, { x: X.dot, y: y + 0.06, w: 0.18, h: 0.18, fill: { color: col }, line: { color: col, width: 0 } });
  s.addText(name + (v.old_fit ? ' †' : ''), { x: X.name, y, w: 2.85, h: RH, fontFace: 'Calibri', fontSize: 14, bold: true, color: INK, margin: 0, valign: 'middle', isTextBox: true });
  s.addText(`${MARK[v.day] || ''} ${v.day}`, { x: X.day, y, w: 0.8, h: RH, fontFace: 'Calibri', fontSize: 12, color: v.old_fit ? '8A94A6' : MUTED, margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.mean, 1) + ' dB', { x: X.db, y, w: 0.95, h: RH, fontFace: 'Calibri', fontSize: 15, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.thrust, 2) + ' N', { x: X.th, y, w: 0.85, h: RH, fontFace: 'Calibri', fontSize: 15, bold: true, color: name === best[0] ? RED : name === 'Duct + inlet, no lining' ? '0B7285' : INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
  s.addText(n(v.rpm), { x: X.rpm, y, w: 0.85, h: RH, fontFace: 'Calibri', fontSize: 15, color: INK, align: 'right', margin: 0, valign: 'middle', isTextBox: true });
});

const yC = Y0 + items.length * RH + 0.12;
s.addText(`+${n(gain, 2)} N`, { x: L, y: yC, w: W, h: 0.7, fontFace: 'Cambria', fontSize: 40, bold: true, color: RED, margin: 0, isTextBox: true });
s.addText(`${best[0]} against the unlined duct, both ${duct.day}: it wins back ${(100 * gain / loss).toFixed(0)} % of the ${n(loss, 2)} N the empty duct loses to the bare prop, and is ${n(-dMeanB, 1)} dB quieter from −54° to +90°.`,
  { x: L, y: yC + 0.72, w: W, h: 0.66, fontFace: 'Calibri', fontSize: 13, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText([
  { text: 'Every duct is louder than the bare prop: ', options: { bold: true } },
  { text: `${n(dMin, 1)}–${n(dMax, 1)} dB against ${n(bare.mean, 1)} dB, at ${n(bare.thrust, 2)} N and ${n(bare.rpm)} rpm bare. Set-ups marked † are from other days and the old fit: indicative only.` },
], { x: L, y: yC + 1.42, w: W, h: 0.66, fontFace: 'Calibri', fontSize: 13, color: INK, margin: 0, valign: 'top', isTextBox: true });
s.addText([
  { text: `Inlet (dashed, ${inlet.day}): `, options: { bold: true, color: '0B7285' } },
  { text: `${n(inlet.thrust, 2)} N, +${n(inlet.thrust - duct.thrust, 2)} N over the unlined duct of 2 Nov at the same level (${n(frontMean(inlet, duct), 1)} dB from −54° to +90°). Same day with the inlet: ` +
    iLined.map(([k, v]) => `${k.replace('Inlet + Thinsulate, ', 'Thinsulate ').replace('Inlet + Thinsulate ', 'Thinsulate ').replace(' layers', '')} ${n(v.thrust - inlet.thrust, 2).replace(/^(?!−)/, '+')} N, ${n(frontMean(v, inlet), 1).replace(/^(?!−)/, '+')} dB`).join('; ') +
    '. A repeat of the bare inlet agreed to 0.04 N.' },
], { x: L, y: yC + 2.12, w: W, h: 0.85, fontFace: 'Calibri', fontSize: 13, color: INK, margin: 0, valign: 'top', isTextBox: true });

s.addText(`28 Oct–3 Nov 2026, APC 8x4.5MR, AXI 2217/12, 500 Hz–24 kHz, 2000 µs, mean of 3 repeats, corrected files. Axis ${R.zoom_axis[0]}–${R.zoom_axis[1]} dB. Grey: −90°/−72°, probably in the flow. rpm = stand × 60/7.`,
  { x: 0.6, y: 11.0, w: 15.0, h: 0.35, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
s.addText('1', { x: 15.6, y: 11.0, w: 0.45, h: 0.35, fontFace: 'Calibri', fontSize: 13, color: MUTED, align: 'right', margin: 0, isTextBox: true });

const lines = Object.entries(S).map(([k, v]) => `${k} (${v.day}${v.old_fit ? ', old fit' : ''}, base ${v.base}): ${n(v.mean, 1)} dB (repeat-to-repeat spread of the mean ${v.repeat_spread} dB), thrust ${n(v.thrust, 2)} N (repeats ${v.thrust_min_max.join('–')}), ${n(v.rpm)} rpm (${v.rpm_min_max.join('–')}), ${n(v.current, 2)} A; per microphone from +90 to -90: ${Object.values(v.per_mic).join(', ')} dB.`);
s.addNotes(['All set-ups are the 8-inch APC 8x4.5MR on the AXI 2217/12 in the r27 duct. The bare prop, the unlined duct and Thinsulate 2/4/8/10 are from 2 Nov; the duct with the inlet (no lining), and with Thinsulate 2, Thinsulate 4 and Thinsulate 4 + rubber inside it, from 3 Nov; the bare-inlet value is run 1, whose repeat (base r27-duct-unlined-inlet-trial-2026-11-03) gave 10.08 N and 0.0-0.2 dB from -54 to +90 degrees; Thinsulate 6 from 30 Oct; felt and PU foam from 28 Oct; felt double, felt double + rubber, rubber and PU foam + rubber from 29 Oct. The linings from 28-29 Oct were fitted the old way: with the new fit (from 30 Oct) the Thinsulates gave 8-26 % more thrust than their old-fit runs, so the old-fit values are probably low and are not comparable with the rest. The PU foam base also holds a 27 Oct run that was deleted on the Pi; only the 28 Oct run is used. Only the 2 Nov set-ups are compared with each other (the headline numbers). Each base: the PWM 2000 step of 3 repeats; level per microphone is the total level 500 Hz to 24 kHz in dB SPL with the corrected microphone files, mean over the 3 repeats, and the list gives the mean over the eleven positions. Thrust (the stand reads negative, shown as magnitude), rpm and current are the median of the second half of each step, mean over the 3 repeats; rpm is the stand reading (electrical) times 60/7 for the 14-pole motor. Duct and propeller are one piece on the stand, so the thrust includes the duct.',
  'The radial axis is zoomed to the ducted set-ups, so the bare prop (74-80 dB at most positions, 96.1 dB at -90 degrees) is not drawn. The -90 and -72 degree positions vary run to run by about 1 dB even without a remount and probably sit in the flow, so their levels are less trustworthy than the rest of the arc.',
  ...lines].join('\n\n'));

// ---- page 2: each set-up with and without the inlet ----
{
  const s2 = pres.addSlide();
  s2.background = { color: 'FFFFFF' };
  s2.addImage({ path: 'polar-r27-inlet.png', x: 0.3, y: 1.4, w: 6.8, h: 8.63, altText: 'Polar plot of the duct with the inlet (two runs, with Thinsulate 2 and 4) and the unlined duct without it, 2000 microseconds' });
  const L2 = 7.35, W2 = 8.85;
  s2.addText('THE INLET', { x: L2, y: 0.6, w: W2, h: 0.4, fontFace: 'Calibri', fontSize: 16, bold: true, color: BLUE, charSpacing: 3, margin: 0, isTextBox: true });
  s2.addText('With and without the inlet', { x: L2, y: 0.98, w: W2, h: 0.85, fontFace: 'Cambria', fontSize: 38, bold: true, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s2.addText(`2000 µs, mean of 3 repeats. Without the inlet: ${duct.day}; with it: ${inlet.day}, so every row crosses days. Level is the mean over −54° to +90°.`,
    { x: L2, y: 1.9, w: W2, h: 0.6, fontFace: 'Calibri', fontSize: 13, color: MUTED, margin: 0, valign: 'top', isTextBox: true });
  const PAIRS = [['None', 'Duct, no lining', 'Duct + inlet, no lining'], ['Thinsulate 2', 'Thinsulate, 2 layers', 'Inlet + Thinsulate, 2 layers'], ['Thinsulate 4', 'Thinsulate, 4 layers', 'Inlet + Thinsulate, 4 layers']];
  const sg = (x, d) => (x >= 0 ? '+' : '') + n(x, d);
  const hdr = { fontFace: 'Calibri', fontSize: 12, bold: true, color: MUTED, align: 'center', valign: 'middle', fill: { color: 'F1F3F5' } };
  const c = (t, o = {}) => ({ text: t, options: { fontFace: 'Calibri', fontSize: 14, color: INK, align: 'right', valign: 'middle', ...o } });
  const rows = [[
    { text: 'lining', options: { ...hdr, align: 'left' } }, { text: 'thrust\nno inlet', options: hdr }, { text: 'thrust\ninlet', options: hdr }, { text: 'Δ thrust', options: hdr },
    { text: 'rpm\nno inlet → inlet', options: hdr }, { text: 'level\nno inlet → inlet', options: hdr }, { text: 'Δ level', options: hdr }, { text: '0°\nno inlet → inlet', options: hdr }]];
  PAIRS.forEach(([lab, a, b]) => {
    const A = S[a], B = S[b];
    rows.push([c(lab, { align: 'left', bold: true }), c(n(A.thrust, 2) + ' N'), c(n(B.thrust, 2) + ' N'), c(sg(B.thrust - A.thrust, 2) + ' N', { bold: true, color: '0B7285' }),
      c(`${n(A.rpm)} → ${n(B.rpm)}`, { fontSize: 13 }), c(`${n(frontMean(A, { per_mic: Object.fromEntries(Object.keys(A.per_mic).map((k) => [k, 0])) }), 1)} → ${n(frontMean(B, { per_mic: Object.fromEntries(Object.keys(B.per_mic).map((k) => [k, 0])) }), 1)}`, { fontSize: 13 }),
      c(sg(frontMean(B, A), 1) + ' dB', { bold: true }), c(`${n(A.per_mic['0'], 1)} → ${n(B.per_mic['0'], 1)}`, { fontSize: 13 })]);
  });
  s2.addTable(rows, { x: L2, y: 2.65, w: W2, colW: [1.3, 0.9, 0.9, 0.95, 1.5, 1.15, 0.85, 1.3], rowH: [0.6, 0.45, 0.45, 0.45], border: { type: 'solid', pt: 0.75, color: 'C9CFD8' }, margin: 0.05 });
  const npa = PAIRS.map(([, a, b]) => [S[a].thrust / S[a].current, S[b].thrust / S[b].current]);
  s2.addText([
    { text: 'Thrust: ', options: { bold: true } },
    { text: `with the inlet all three land at ${n(Math.min(...PAIRS.map(([, , b]) => S[b].thrust)), 2)}–${n(Math.max(...PAIRS.map(([, , b]) => S[b].thrust)), 2)} N. The weaker the set-up without it, the more the inlet adds, so the linings and the inlet fix the same loss. Per amp: ${npa.map((x) => n(x[0], 3)).join(' / ')} N/A without, ${npa.map((x) => n(x[1], 3)).join(' / ')} N/A with.`, options: { breakLine: true } },
    { text: ' ', options: { breakLine: true, fontSize: 6 } },
    { text: 'Noise: ', options: { bold: true } },
    { text: 'without the inlet the linings were 0.6–0.9 dB quieter than the empty duct; with it the three are within 0.3 dB, and the 0° microphone is quieter in every case. The inlet slows the prop by 80–190 rpm at the same ESC signal.', options: { breakLine: true } },
    { text: ' ', options: { breakLine: true, fontSize: 6 } },
    { text: 'Caution: ', options: { bold: true, color: RED } },
    { text: 'day to day the rig moves up to ~0.2 N and a few tenths of a dB, so the thrust gains are real and the level differences of 0.3 dB or less are not settled. Thinsulate 4 without the inlet, re-run on the inlet day, would make its row same-day.' },
  ], { x: L2, y: 5.05, w: W2, h: 3.4, fontFace: 'Calibri', fontSize: 14, color: INK, margin: 0, valign: 'top', isTextBox: true });
  s2.addText(`2–3 Nov 2026, APC 8x4.5MR, AXI 2217/12, 500 Hz–24 kHz, 2000 µs, mean of 3 repeats, corrected files. Inlet set-ups from 3 Nov; plain inlet value is run 1 (repeat: 10.08 N). rpm = stand × 60/7.`,
    { x: 0.6, y: 11.0, w: 15.0, h: 0.35, fontFace: 'Calibri', fontSize: 12, color: MUTED, margin: 0, isTextBox: true });
  s2.addText('2', { x: 15.6, y: 11.0, w: 0.45, h: 0.35, fontFace: 'Calibri', fontSize: 13, color: MUTED, align: 'right', margin: 0, isTextBox: true });
}

pres.writeFile({ fileName: process.env.OUT || '2026-11-03 duct linings thrust rpm.pptx' }).then((f) => console.log('written', f));
