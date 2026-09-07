# docs/analysis — arc validation from the "horizontal prop" runs (Sept 2026)

Setup under test: prop axis horizontal and perpendicular to the arc plane, so all 11 mics sit in the prop plane at the same angle to the axis and an axisymmetric source must give a circle. Data: `dp1-baseline-horizontal-prop7 … prop18`, PWM 1900, from the laptop backup (`../SoundVisualizer-data`). Produced by `scripts/arc_error_map.py`.

- `arc-error-map.png`, `arc-error-map-third-octave.csv` — dB from a circle at each physical elevation per third-octave, with mic offsets removed by a joint fit over 12 runs (mic swap prop10→11; arc rotated 180° in prop11–14 as the data indicate). Run-to-run residual 0.6–2.3 dB per band.
- `mic-offsets-third-octave.csv` — per-mic residual after the UMIK-2 calibration. Serial **811-1892** is the outlier: −2 to −6 dB below 2 kHz, normal above; in raw dBFS it is only ~1 dB low, so most of the offset is its calibration file (Sens Factor −10.63 dB, the least negative of the set) not matching the unit.
- `prop18-pwm1900-*.png` — spectra, floor ripple and per-band directivity for the last run.

Findings (2026-09-08): positions 0°, ±18°, ±90° are within ~1 dB of a circle in every band. Errors of 3–8 dB sit at ±36°, ±54°, ±72° in three bands only — 200–250 Hz (the BPF band), 630–1000 Hz, and 3150 Hz — with opposite signs on the ceiling-side and floor-side halves of the arc (the arc lies in the prop plane). Above 4 kHz the arc is a circle to ±1 dB. Frequency-selective, position-selective, sign-alternating: interference from reflectors of three sizes (λ ≈ 1.5 m: floor/wall/table; ≈ 0.4 m: stand base or arc frame members; ≈ 0.11 m: mic clamps/mounts), consistent with Rajmane & Baumann's rule that a reflector shows up once λ ≤ its size (`papers/small-chamber/`).
