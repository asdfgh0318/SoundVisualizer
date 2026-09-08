# docs/analysis — arc validation from the "horizontal prop" runs (Sept 2026)

Setup under test: the arc laid flat (horizontal) with the prop axis vertical, so all 11 mics sit at one height in the prop plane at the same angle to the axis, and an axisymmetric source must give a circle. Data: `dp1-baseline-horizontal-prop7 … prop18`, PWM 1900, from the laptop backup (`../SoundVisualizer-data`). Produced by `scripts/arc_error_map.py`.

- `arc-error-map.png`, `arc-error-map-third-octave.csv` — dB from a circle at each physical elevation per third-octave, with mic offsets removed by a joint fit over 12 runs (mic swap prop10→11; arc rotated 180° in prop11–14 as the data indicate). Run-to-run residual 0.6–2.3 dB per band.
- `mic-offsets-third-octave.csv` — per-mic residual after the UMIK-2 calibration. Serial **811-1892** is the outlier: −2 to −6 dB below 2 kHz, normal above; in raw dBFS it is only ~1 dB low, so most of the offset is its calibration file (Sens Factor −10.63 dB, the least negative of the set) not matching the unit.
- `prop18-pwm1900-*.png` — spectra, floor ripple and per-band directivity for the last run. **The cepstrum in `prop18-pwm1900-floor-ripple.png` is not showing reflections**: its peaks at 1.4, 2.8, 4.2 and 8.4 ms are 1/(3·BPF), 2/(3·BPF), 1/BPF and the shaft period, and they move with 1/BPF between motor speeds (`remedies-diagnostics.txt`). Kept for the record; do not read echoes from it.

Findings (2026-09-08): positions 0°, ±18°, ±90° are within ~1 dB of a circle in every band. Errors of 3–8 dB sit at ±36°, ±54°, ±72° in three bands only — 200–250 Hz (the BPF band), 630–1000 Hz, and 3150 Hz — with opposite signs on the negative-angle and positive-angle halves of the arc (the arc was laid horizontal for these runs, so this is a one-sided surface in the horizontal plane, wall/corner side, not floor or ceiling). Above 4 kHz the arc is a circle to ±1 dB. Frequency-selective, position-selective, sign-alternating: interference from reflectors of three sizes (λ ≈ 1.5 m: floor/wall/table; ≈ 0.4 m: stand base or arc frame members; ≈ 0.11 m: mic clamps/mounts), consistent with Rajmane & Baumann's rule that a reflector shows up once λ ≤ its size (`papers/small-chamber/`).

- `brief-fig4-mic-vs-room.png`: microphone error map (serial × band) beside the room error map (position × band), same fit, same scale. The 0° mic (810-8897) never moved, so its cell and the 0° room cell are only known as a sum.

## Remedies diagnostics (2026-09-08, `scripts/arc_validation_diagnostics.py`)

Same twelve runs, all five PWM steps, tones and broadband separated. Behind `docs/arc-validation-remedies.html/pdf`.

- `remedies-diagnostics.txt`, `remedies-diagnostics.json` — the full printout and the numbers: BPF per run and step (prop7 spun at 164 Hz at PWM 1900, the others at 238–239 Hz; PWM 1200 never makes a tone; PWM 1800 WAVs are cut short in nine runs), standard errors, comb fits, correlations, cepstral peaks by speed.
- `remedies-tone-probe-map.csv` — the room term per position at each BPF harmonic (3 speeds × 6 harmonics = 18 probe frequencies, 216 Hz–1.55 kHz), with mean s.e. and residual rows.
- `remedies-broadband-position-map-allpwm.csv` (+ `-se-`) — tone-notched third-octave room term over all usable captures at all speeds: within ±1.3 dB in 92 % of cells, worst ±2.7 dB. Fine 16384-point notching below 1.1 kHz.
- `remedies-thirdoct-position-map-allpwm.csv`, `remedies-thirdoct-position-se-pwm1900.csv`, `remedies-mic-offsets-pwm1900.csv`, `remedies-mic-offsets-se-pwm1900.csv` — the one-pager's quantities with their standard errors (position term median 0.34 dB, mic term median 0.24 dB).
- `remedies-fig-three-speeds.png` — the blade tone polar at BPF 216/238/258 Hz beside the broadband floor 7–15 Hz from the tone: the tones are bent by ±8 dB, the floor is not.
- `remedies-fig-tones-vs-broadband.png` — tone probe map beside the tone-notched broadband map.
- `remedies-fig-probe-comb.png` — per position, the room term vs probe frequency with the best single-echo comb (+36°/+54°: extra path 1.5 m; −72°: 0.7 m; nothing fits −36° at 238 Hz).
- `remedies-fig-cepstrum.png`, `remedies-fig-bpf-tone-vs-broadband.png` — cepstrum of the tone-notched ripple (peaks are harmonic residue, common to all mics) and tone-vs-broadband per speed.
