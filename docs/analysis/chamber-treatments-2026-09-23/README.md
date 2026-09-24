# Chamber treatments, 2026-09-23

First session of point-improvements to the chamber. Every result is an **in/out difference**
between runs of the same 95-tone grid (257 Hz–6.35 kHz at 24/octave, 3–5 kHz omitted because the
sphere is not axisymmetric there), all eleven calibrated capsules at once. The score is
**flatness**: the rms across the arc of each capsule's level relative to the arc mean. With an
axisymmetric source every capsule should read the same, so lower is better.

**Headline: unwrapping the tripod legs flattened the room at 1.6–3 kHz, 0.98 → 0.93 dB.** The
−54° capsule, which sits beside the tripod, was shadowed (−0.79 dB in that band) and filled in
(−0.17 dB). Below 1.6 kHz unwrapping changed the map by only 0.06–0.13 dB and made it slightly
worse (0.01–0.03 dB per band), so the net effect is confined to the high band.
Figure: `tripod-unwrapped.pdf`.

## Geometry

Arc vertical, as remounted 2026-09-17. The 1 l printed sphere is on the tripod, backed 20 cm off
the ring centre **along the arc's symmetry axis**, facing away, driver at 180°. Off-centre along
the axis keeps every capsule equidistant (0.863 m) and at the same angle to the aim, so the test
is still axisymmetric. The source was not moved all session.

## Numbers the method stands on

| | rms, <3 kHz |
|---|---|
| repeat floor, two untouched runs minutes apart (`vertical-2a`/`-2b`) | **0.010 dB** |
| handling: put material in, take it out, compare with before (`foam-out` vs baseline) | **~0.04 dB** |
| six days untouched (`vertical-2a` vs 2026-09-17 `driver-180`) | 0.15–0.25 dB |
| noise floor vs the weakest tone | ≥ 65 dB margin |

A treatment effect clearly above ~0.1 dB is real. Anything compared across days carries ~0.2 dB.

## Runs (`calibrator/sessions/2026-09-23/` and `2026-09-24/`, gitignored; levels+meta mirrored to the data repo)

| run | state | flatness 250–400 / 400–630 / 630–1k / 1–1.6k / 1.6–3k (dB) |
|---|---|---|
| `vertical-2a`, `-2b` | baseline, untouched pair | 2.00 / 1.67 / 1.27 / 0.80 / 0.98 |
| `foam-1` | 30 cm roll of thick Thinsulate on a cardboard core, in a corner, in the arc's plane | 2.04 / 1.67 / 1.24 / 0.81 / 0.98 (avg with foam-2) |
| `foam-2` | same roll, core removed | (see above) |
| `foam-out` | roll removed | 2.01 / 1.67 / 1.27 / 0.80 / 0.98 |
| `tripod-unwrapped` | some Thinsulate wrapping taken off the tripod legs | 2.02 / 1.70 / 1.29 / 0.83 / **0.93** |
| `ring-unwrapped` | + part of the ring's wrapping removed (new physical preset from here) | 2.03 / 1.66 / 1.36 / 0.87 / 0.96 |
| `ring-unwrapped-2` | + more of the ring unwrapped | 2.04 / 1.67 / 1.36 / 0.87 / 0.96 |
| `floor-carpet` | + thick Thinsulate carpet on the floor | **1.74 / 1.51 / 1.30 / 0.81** / 0.95 |
| `ceiling-carpet` | the same carpet moved to the ceiling | 2.29 / 1.54 / 1.28 / 0.81 / 0.95 |
| `2026-09-24/ceiling-carpet-day2` | next day, untouched (preset e3e76875: hub back on USB port 5) | 2.27 / 1.54 / 1.27 / 0.81 / 0.94 |
| `2026-09-24/ceiling1-floor2` | + felt carpet ~2 cm on the floor, Thinsulate still on the ceiling | 2.08 / 1.65 / 1.45 / 1.06 / 0.96 |

Set aside, not data: `noise-floor-CHAMBER-NOT-READY`, `vertical-2a-ABORTED-chamber-not-ready`,
`foam-out-NOISY-above-420Hz` (a loud noise started 1–2 min in; the tone gate rejected 77 of 95
tones on the upper half of the arc, and nothing bad entered the map).

## Findings

1. **The roll changed the room without improving it.** 0.34 dB at 250–630 Hz, falling to 0.05 dB
   at 1.6–3 kHz; flatness unchanged. Removing the core made no difference (r = +0.92, slope 0.95
   between foam-1 and foam-2). Removing the roll returned every band to within 0.03–0.04 dB.
   A 30 cm porous roll behaves at 250–630 Hz as a bulk obstacle, not as an absorber.
2. **The tripod legs matter above ~1.5 kHz,** where they are close to the source and no longer
   small against the wavelength. That is where unwrapping helped.
3. **Locating a reflector from these maps does not work.** The blind single-scatterer fit to the
   roll put it 1.5 m out of the arc's plane; it was in the plane, in a corner. Constrained to the
   plane, the best fit sat at the hub. At 250–630 Hz a corner couples to the room's modes rather
   than sending one echo. `foam-1-reflector.pdf` is kept as the record of that failed guess and
   should not be used to place anything. Improvement is done by **direct search**: material in,
   run, score flatness, material out.
4. **Unwrapping the ring made it worse, and only the first section mattered.** Step 1 changed
   the map 0.18 dB rms, spread over all eleven capsules, and cost flatness at 630 Hz–3 kHz
   (overall 1.387 → 1.406 dB). Step 2 changed it 0.03 dB, the handling level. The top capsule
   (+90°) took a frequency-independent +0.17 dB offset at step 1 that step 2 did not move — either
   that section sat near it or its clamp shifted then. Best state measured: **tripod bare, ring
   wrapped.** Figure: `ring-unwrapping.pdf`.
5. **The floor carpet is the first treatment that works where the error is.** Room error below
   3 kHz 1.408 → **1.277 dB**, the best state measured and better than the untouched baseline
   (1.380): −0.30 dB at 250–400 Hz, −0.16 at 400–630, −0.06 at 630 Hz–1 kHz and 1–1.6 kHz,
   nothing above 1.6 kHz. The change is largest at 257–350 Hz on the middle capsules (0°, −18°,
   −36°), filling the strongest low-frequency holes in the map. Figure: `floor-carpet.pdf`
   (built by `build_step_figure.py`).
6. **The carpet belongs on the floor.** Moved to the ceiling it helped 400 Hz–1.6 kHz about as much
   as on the floor (−0.12 / −0.08 / −0.06 dB) but made 250–400 Hz **worse** (2.04 → 2.29 dB),
   opening a new hole near 270 Hz at −18°/−36°; overall 1.408 → 1.431 dB against 1.277 on the
   floor. Figure: `carpet-floor-vs-ceiling.pdf` (`build_carpet_figure.py`).
7. **Day 2 (2026-09-24).** Overnight, untouched (`2026-09-24/ceiling-carpet-day2` vs
   `ceiling-carpet`): the map moved 0.16 dB rms, spread evenly over the capsules, but flatness only
   1.431 → 1.424. **Compare maps within a day; flatness holds across days to ~0.01 dB.** Adding a
   **felt carpet (~2 cm) on the floor** with the Thinsulate still on the ceiling
   (`2026-09-24/ceiling1-floor2`) changed the map the most of any treatment (1.10 dB rms) but made
   it worse overall, 1.424 → 1.457: 250–400 Hz −0.20, and +0.11 / +0.18 / +0.25 dB at 400 Hz–1.6 kHz.
   The Thinsulate on the floor alone (1.277) remains the best state. Figure: `felt-floor-day2.pdf`.
8. **What remains:** 250–400 Hz is still the worst band, 1.74 dB with the carpet on the floor.

## Files

- `tripod-unwrapped.pdf/.png` — the headline figure (built by `build_tripod_figure.py`)
- `carpet-floor-vs-ceiling.pdf/.png` — no carpet, floor, ceiling side by side
- `felt-floor-day2.pdf/.png` — felt on the floor, day 2
- `grid-95.txt` — the exact 95 frequencies of every treatment run (pass to `--freqs`)
- `floor-carpet.pdf/.png` — the carpet step (`build_step_figure.py <ref> <run> "<what>" <name>`)
- `ring-unwrapping.pdf/.png` — the three ring states and both steps (built by `build_ring_figure.py`)
- `vertical-2-repeat.pdf` — the untouched pair and the 2026-09-17 centred run for reference
- `foam-1-vs-baseline.pdf`, `foam-2-vs-baseline.pdf`, `foam-out-vs-baseline.pdf` — map, map, difference
- `foam-1-reflector.pdf` — the failed localisation (see finding 3)
- `compare_runs.py <run> <ref…>` — band table and flatness; `plot_vs_baseline.py <run>` — three-panel figure;
  `plot_repeat_pair.py` — the repeat figure. Run from the repo root with `.venv/bin/python`.

**Preset change:** every run after `tripod-unwrapped` uses
`setup-presets/1d9a5e2fa2964faf9f10f020edd5a1e9.json`, whose elevations are physical (811-1897 at
−90° = bottom). Every run listed above used `30f35d3f…` and carries `labels_mirrored: true`, which
`read_map()` honours.
