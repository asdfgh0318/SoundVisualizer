# Chamber top-5 vs top performer (2026-09-23–25)

Metric: room-error total <3 kHz (rms across arc vs arc mean, dB, lower = flatter).
Repeat floor 0.01 dB within session, handling ~0.04 dB, overnight map drift 0.1–0.2 dB.
So >0.1 dB = real. Source: `README.md` findings, runs `calibrator/sessions/2026-09-23/` + `2026-09-24/`.
Grid: 95 tones, 257 Hz–6.35 kHz, 3–5 kHz excluded from score (sphere m=1 mode, 11.0 dB at 4362 Hz).

Top performer = `floor-carpet`: wedges + thick Thinsulate carpet on floor. Total **1.277 dB**.
All deltas below are setup minus top performer (negative = better than best in that band).

| # | setup | total | 250–400 / 400–630 / 630–1k / 1–1.6k / 1.6–3k | vs top (+ = worse) |
|---|---|---|---|---|
| 1 | floor-carpet (wedges + Thinsulate on floor, day1) | **1.277** | 1.74 / 1.51 / 1.30 / 0.81 / 0.95 | 0.000 baseline |
| 2 | cleanup-1 / backed-5cm accepted (day3 raised stack, speaker backed 5 cm) | 1.301 / 1.303 | 1.56 / 1.62 / 1.43 / 0.81 / 1.03 | +0.024 / +0.026 |
| 3 | closer-a/-b (speaker ~20 cm closer to ring, day3) | 1.311 | 1.99 / 1.28 / 1.29 / 0.86 / 0.97 | +0.034 |
| 4 | cleanup-2 (more junk out, day3) | 1.314 | 1.61 / 1.72 / 1.40 / 0.79 / 0.98 | +0.037 |
| 5 | chaotic-carpet-1 (wedges OFF + chaotic carpet, day2, best no-wedge) | 1.317 | 1.73 / 1.45 / 1.48 / 0.90 / 0.97 | +0.040 |

Notes:
- #2–#4 are same week/day3 floor stack, not same floor as #1. Tripod stands on the stack, so carpet
  changes move the source (see `carpet-removed`, `cleanup-5` analysis). Cross-day gap #1 vs #2–#4
  carries ~0.1–0.2 dB map drift; #2–#5 differences (0.01–0.04 dB) are at handling level.
- Chaotic-2 / -3 repeat #5 at 1.318 / 1.324 (maps differ 0.12–0.19 dB, r≈0.99): flatness, not arrangement, matters.
- Bare wedges for reference: `bare-day2` 1.400, same state day1 1.408. Floor wedges off: 2.054.
- Worst band everywhere: 250–400 Hz (1.5–2.0 dB even in top-5). Best bands: 1–3 kHz (~0.8–1.0 dB).

## How this maps to literature qualification

- ISO 3745 / ISO 26101 style: deviation from 1/r vs traverse, per 1/3-octave, pass/fail per band.
  We do the in-situ equivalent: per-capsule deviation from arc mean per tone, rms per band.
  du Plessis 2022 precedent (non-conforming fan rig): per-position per-1/3-oct correction,
  residual <0.55 dB above 200 Hz. Our residuals are 2–3× that at 250–630 Hz → correction or geometry, not foam.
- Cutoff by depth (quarter-wave): few-cm porous = 3 kHz treatment, not 250 Hz (needs ~34 cm).
  Matches our data: carpet/thickness moves 1–3 kHz, barely touches 250–400 Hz.
- Time-gate limit: shortest echo 1.98 ms → gated data valid only >~500 Hz. Same reason 250–400 Hz stays bad.
- Sphere limit: avoid 3–5 kHz entirely (non-axisymmetric), 5–6.4 kHz indicative only.

## Which freqs to avoid / trust

- AVOID for directivity: 250–400 Hz (all setups 1.5–3.3 dB, modes + floor reflection, tilt bottom-loud).
  AVOID 3–5 kHz (source defect, not room). CAUTION 5–6.4 kHz (source lobe + unexplained +4 dB boost after 14:10 day3).
- TRUST: 1–3 kHz (0.7–1.1 dB in top-5, tripod-unwrap best 0.93, center-leveled best 0.83).
  USE WITH CORRECTION: 400 Hz–1 kHz (1.3–1.7 dB, reflection-localisation target: extra path 1.5 m at +36°/+54°, 0.7 m at −72°).

## Figures (existing PNGs, arranged)

### 1. Top performer: floor-carpet (1.277)
![floor-carpet](floor-carpet.png)
![floor vs ceiling](carpet-floor-vs-ceiling.png)

### 2. Accepted state backed-5cm (1.303) vs best
![backed-5cm](backed-5cm-day3.png)
![backed-5cm vs best](backed-5cm-vs-best-day3.png)
![cleanup-1 safe](cleanup-1-day3.png)

### 3. Closer (1.311) vs best
![closer](closer-day3.png)
![closer vs best](closer-vs-best-day3.png)
![distance sweep](speaker-distance-day3.png)

### 4. Cleanup-2 (1.314)
![cleanup-2](cleanup-2-day3.png)

### 5. Chaotic-carpet no-wedge best (1.317) vs wedges
![chaotic vs wedges](chaotic-carpet-vs-wedges-day2.png)
![chaotic 1-2-3 repeat](chaotic-1-2-3-day2.png)
![flat vs chaotic](chaotic-vs-flat-carpet-day2.png)

### Reference: bare wedges + wedges-off cliff
![bare](bare-day2.png)
![wedges off](floor-no-wedges-day2.png)
![floor states](floor-states-compare.png)
