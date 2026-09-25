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
| `2026-09-24/felt-floor-only` | Thinsulate off the ceiling, felt left on the floor | 2.06 / 1.77 / 1.57 / 1.12 / 0.98 |
| `2026-09-24/bare-day2` | all carpets removed = same state as `ring-unwrapped-2` | 2.00 / 1.67 / 1.36 / 0.87 / 0.97 |
| `2026-09-24/floor-no-wedges` | + absorbing wedges taken off the floor, flat foam base left | **3.29 / 2.17 / 1.84 / 1.32 / 1.26** |
| `2026-09-24/carpet-added` | wedges still off, a carpet laid on the flat foam (material not stated) | 2.60 / 1.74 / 1.61 / 0.94 / 0.98 |
| `2026-09-24/chaotic-carpet` | the carpet made "chaotic" (uneven) instead of flat; wedges presumed still off — both unconfirmed | **1.73 / 1.45** / 1.48 / 0.90 / 0.97 |
| `2026-09-24/chaotic-carpet-2` | a second, different chaotic arrangement | 1.71 / 1.46 / 1.48 / 0.91 / 0.98 |
| `2026-09-24/chaotic-carpet-3` | a third chaotic arrangement | 1.76 / 1.45 / 1.48 / 0.89 / 0.98 |
| `2026-09-24/wall-direct-a`, `-b` | sphere on the wall itself, further out (~2.5 m by level, unconfirmed) | 2.12 / **3.58** / 2.13 / 1.54 / 1.13 |
| `2026-09-25/material-roll` | curtain replaced by a roll of material | 1.60 / 2.01 / 1.40 / 0.87 / 1.03 (5–6.4 kHz 1.10) |
| `2026-09-25/curtain` | + curtain on the wall the speaker fires toward (sphere confirmed unmoved) | 1.98 / 1.85 / 1.57 / 1.36 / 2.01 (5–6.4 kHz 2.31) |
| `2026-09-25/in-plane-a`, `-b` | speaker moved on into the ring plane, on the axis | 1.94 / 1.87 / 1.39 / 0.98 / 1.10 |
| `2026-09-25/closer-a`, `-b` | **speaker moved ~20 cm closer to the ring**, still on the axis | **1.99 / 1.28 / 1.29** / 0.86 / 0.97 |
| `2026-09-25/blue-carpet` | + a blue absorbing carpet on top of the floor stack-up, ~0.5 cm, no backing | 3.22 / 2.49 / 1.53 / 0.83 / 1.00 (5–6.4 kHz 1.11) |
| `2026-09-25/day3-a`, `-b` | day 3, nothing changed since `floor-raised-3` (hub back on USB port 4: preset 1d9a5e2f) | 3.33 / 2.57 / 1.57 / 0.80 / 0.87 |
| `2026-09-24/floor-raised-3` | floor layer raised further (height not stated) | 3.32 / 2.56 / 1.57 / 0.80 / 0.86 (5–6.4 kHz 1.02) |
| `2026-09-24/felt-bare` | the glue layer left by the foil also removed: bare felt | 3.39 / 2.53 / 1.55 / **0.74** / 0.84 (5–6.4 kHz 1.03) |
| `2026-09-24/felt-foil-free-inverted` | the foil-free felt flipped over | 3.38 / 2.40 / 1.62 / 0.95 / 0.95 (5–6.4 kHz 1.17) |
| `2026-09-24/felt-foil-removed` | felt stays on the floor, **foil backing stripped off** | 3.47 / 2.55 / 1.85 / 1.31 / 1.10 (5–6.4 kHz 1.43) |
| `2026-09-24/felt-foil-in` | felt turned FOIL SIDE INTO the chamber (it has a foil backing, until now always facing away) | **4.32** / 2.86 / 2.37 / 2.01 / 1.81 (5–6.4 kHz **1.71**) |
| `2026-09-24/ceiling-felt-to-floor` | the ceiling felt laid on the floor (second felt layer on the floor) | 3.69 / 2.64 / **2.53 / 1.75 / 1.76** (5–6.4 kHz 1.12) |
| `2026-09-24/ceiling-felt-removed` | the ceiling felt taken down (carpet still raised, felt still on the floor) | 3.68 / 2.67 / 1.55 / **0.71 / 0.72** (5–6.4 kHz 0.88) |
| `2026-09-24/shield-removed` | the felt shield taken out again (carpet stays raised) | 3.07 / 2.64 / 1.91 / 1.06 / 0.97 (5–6.4 kHz 0.96) |
| `2026-09-24/carpet-raised-2` | carpet raised further + felt shield under some electronics (two changes at once) | 3.07 / 2.59 / 1.96 / 1.06 / 0.96 (5–6.4 kHz 1.03) |
| `2026-09-24/carpet-raised` | carpet less even and lifted on spacers (gap height not stated) | 3.04 / 2.59 / 1.92 / 1.08 / 0.95 (5–6.4 kHz 0.93) |
| `2026-09-24/rod-removed` | the same with the metal rod taken out | 3.06 / 2.66 / 1.95 / 1.15 / 1.04 (5–6.4 kHz 1.10) |
| `2026-09-24/felt-ceiling` | + a second piece of felt on the ceiling (floor felt stays), rod still in | 3.05 / 2.66 / 1.96 / 1.14 / 1.03 |
| `2026-09-24/metal-rod` | + a metal rod placed in the chamber (position, size not stated) | 3.69 / 3.09 / 2.26 / 1.74 / 1.43 (5–6.4 kHz 1.31) |
| `2026-09-24/carpet-plus-felt` | + the felt added to the even thick carpet | 3.69 / 3.12 / 2.27 / 1.73 / 1.42 |
| `2026-09-24/floor-even-carpet` | floor cleaned up, thick carpet laid mostly evenly (was heaped) | **4.86 / 2.72** / 1.61 / **0.77 / 0.79** |
| `2026-09-24/center-leveled` | the same, sphere levelled | 2.20 / 1.81 / 1.26 / **0.84 / 0.83** |
| `2026-09-24/center-new-a`, `-b` | **sphere back at the ring centre on a new tripod mount**, ring bare | 2.21 / 1.97 / 1.80 / 1.39 / 1.57 |
| `2026-09-24/ring-bare` | + the rest of the Thinsulate wrap removed from the ring | 1.79 / 4.04 / 1.84 / 1.46 / 1.20 |
| `2026-09-24/wall-direct-absorber` | + felt and foam behind the speaker, against the wall | 1.89 / **4.04** / 1.85 / 1.47 / 1.16 (quarter-octave peak still 555 Hz) |
| `2026-09-24/wall-mount-decoupled` | same, Thinsulate between speaker and wall | 3.97 / 2.05 / 1.52 / 0.80 / 0.94 |
| `2026-09-24/wall-mount-a`, `-b` | **new geometry**: sphere on the wall reinforcement ~1.5 m out along the axis, facing the ring; tripod and clutter removed; chaotic carpet unchanged | **4.18** / 2.06 / 1.49 / **0.80 / 0.92** |

Set aside, not data: `noise-floor-CHAMBER-NOT-READY`, `vertical-2a-ABORTED-chamber-not-ready`,
`foam-out-NOISY-above-420Hz` (a loud noise started 1–2 min in; the tone gate rejected 77 of 95
tones on the upper half of the arc, and nothing bad entered the map).

## Findings

0. **Repeatability, day 3 (2026-09-25).** Nothing touched overnight. Two back-to-back runs agree to
   **0.009 dB** rms below 3 kHz (worst cell 0.06 dB). Against yesterday's last run the map moved
   **0.10 dB** (worst cell 0.65), every capsule's offset stayed within ±0.04 dB, the overall level
   within 0.00 dB, and the room-error score reproduced to **0.005 dB** (1.992 → 1.997 / 1.996) with every
   band within 0.02 dB. Across three days the pattern holds: within a session ~0.01 dB, overnight
   ~0.1–0.2 dB on the map and ~0.01 dB on the score.
   **Blue absorbing carpet** added to the floor stack (`blue-carpet`): map moved 0.53 dB; small gain at
   250–630 Hz (3.33 → 3.22, 2.57 → 2.49), small loss at 1.6–3 kHz (0.87 → 1.00); total 1.996 → 1.961.
   Figure: `blue-carpet-day3.pdf`.
   **Moving the speaker closer to the ring** (`closer-a/-b`, repeat 0.006 dB) is the largest gain
   since the wedges came out: room error **1.961 → 1.311**, 250–400 Hz 3.22 → 1.99, 400–630 Hz 2.49 →
   **1.28 (best ever)**, 630 Hz–1 kHz 1.53 → 1.29 (best ever). Level +0.5 dB (+0.8 below 1 kHz). A
   top-to-bottom tilt remains (+0.59 dB, bottom louder); fitted out, the score would be 1.183.
   Within 0.03 dB of the best state (1.277) without the wedges. Figures: `closer-day3.pdf`,
   `closer-vs-best-day3.pdf`.
   **Moving it on into the ring plane** (`in-plane-a/-b`, repeat 0.010 dB) went too far: 1.311 →
   **1.473**, with 400–630 Hz 1.28 → 1.87 and 1–3 kHz slightly worse; only 250–400 Hz held (1.94). The
   tilt is gone (−0.12 dB) but the arc now reads low at both ends (+90° −0.22, −90° −0.34 dB) and the
   level fell 0.35 dB although the sphere came closer — every capsule now sits at 90° to the aim, off
   the sphere's main lobe. **Best position so far: ~10 cm off the ring plane.** Figures:
   `in-plane-day3.pdf`, `speaker-distance-day3.pdf`.
   **Curtain on the wall the speaker faces** (`curtain`): room error 1.473 → 1.783, worst at 1.6–3 kHz
   (1.10 → 2.01) and 5–6.4 kHz (1.04 → 2.31). The overall level rose 0.92 dB, rising with frequency to +4.25 dB at
   5–6.4 kHz. I first read that as the sphere's aim having changed; **Adam confirms the sphere did not
   move**, so the curtain itself did it: hung on an absorbing wall straight in the speaker's main beam,
   it replaced absorption with a strong reflection back toward the arc, strongest where the wall had
   absorbed best. A reflective covering over an absorber is the foil lesson again. Figure:
   `curtain-day3.pdf`.
   **Replacing the curtain with a roll of material** (`material-roll`) gives 1.403, better than the curtain
   (1.783) mainly above 1 kHz. **But the curtain and roll runs carry the same level boost against the
   bare-wall runs** — +0.9 dB at 1–1.6 kHz, +2.0 at 1.6–3 kHz, +4.2 at 5–6.4 kHz, matching each other
   to 0.1 dB — so the boost is not the curtain. Something changed between 14:08 (`in-plane-b`) and 14:18
   (`curtain`) and stayed changed; unexplained so far (sphere reported unmoved). Curtain vs roll compares
   fairly; neither compares cleanly with the bare-wall pair. Figure: `material-roll-day3.pdf`.

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
   Taking the Thinsulate off the ceiling and leaving only the felt (`felt-floor-only`) gives the
   **worst state measured, 1.512 dB** — worse than the bare room (1.408) in every band from
   400 Hz to 3 kHz. **Felt on the floor harms 400 Hz–1.6 kHz; the Thinsulate on the ceiling had
   been masking part of that.** Figure: `felt-floor-only-day2.pdf`.
   With every carpet removed (`bare-day2`) the room returns to **1.400 dB against 1.408 for the
   same state the day before** — every band within 0.04 dB. The room-error score reproduces across
   days, so yesterday's 1.277 for the Thinsulate floor stands as a valid comparison.
   **The floor wedges are the most important treatment in the room.** Taking them off, leaving the
   flat foam base (`floor-no-wedges`), took room error from 1.400 to **2.054 dB** — worse in every
   band below 3 kHz, 250–400 Hz from 2.00 to 3.29 — and tilted the arc: the bottom capsule reads
   +0.47 dB and the top −0.31 dB relative to the mean, the signature of a stronger floor reflection
   reaching the capsules nearest the floor. Only 5–6.4 kHz improved (1.14 → 0.98). Figure:
   `floor-no-wedges-day2.pdf`.
   **A carpet on the flat foam recovers ~63 % of that loss but does not replace the wedges**
   (`carpet-added`): 2.054 → 1.642 dB, against 1.400 with the wedges and 1.277 with wedges +
   Thinsulate; 250–400 Hz 3.29 → 2.60. The top-to-bottom tilt stays (−0.51 dB top, +0.52 bottom),
   so the floor reflection is still strong. Figure: `carpet-on-flat-foam-day2.pdf`; against wedges
   only: `carpet-vs-wedges-day2.pdf` (worse at 250 Hz–1 kHz, equal 1–3 kHz, better 5–6.4 kHz).
   **Making the carpet chaotic instead of flat** (`chaotic-carpet`, state unconfirmed) took room
   error from 1.642 to **1.317 dB — better than the wedges alone (1.400)** and the best result
   without the Thinsulate-on-wedges combination. It gives the lowest 250–400 Hz (1.73) and 400–630 Hz
   (1.45) of any state, but is worse than the wedges at 630 Hz–1 kHz (1.48 vs 1.36) and keeps the
   top-to-bottom tilt (−0.64 .. +0.53 dB). Figures: `chaotic-vs-flat-carpet-day2.pdf`,
   `chaotic-carpet-vs-wedges-day2.pdf`. **A second, different chaotic arrangement gave the same
   result** (`chaotic-carpet-2`, 1.318 vs 1.317; the two maps differ by 0.14 dB rms, r = +0.99): what
   matters is that the carpet is not flat, not the particular arrangement. Figures:
   `chaotic-carpet-2-vs-wedges-day2.pdf`, `chaotic-2-vs-1-day2.pdf`. **A third arrangement agrees
   too** (`chaotic-carpet-3`, 1.324): the three score 1.317 / 1.318 / 1.324 and their maps differ
   pairwise by 0.12–0.19 dB (r = +0.99…+1.00). Figures: `chaotic-carpet-3-vs-wedges-day2.pdf`,
   `chaotic-3-vs-2-day2.pdf`; all three together: `chaotic-1-2-3-day2.pdf` (`build_chaotic_figure.py`).
8. **Moving the speaker to the wall (new geometry, `wall-mount-a/-b`).** Repeat pair agrees to
   0.026 dB (0.056 at 250–400 Hz, 0.006–0.011 above). Room error below 3 kHz **2.180 dB** against
   1.324 in the old position: better from 1 kHz up (1–1.6 k 0.80, 1.6–3 k 0.92, 5–6.4 k 0.87 — the
   best of any state there) but far worse at 250–400 Hz (**4.18**) and 400–630 Hz (2.06), with deep
   single-capsule nulls (306 Hz at +54° −23.6 dB, 297 Hz at −18° −16.9 dB) — two nearly equal
   coherent paths cancelling, i.e. a strong reflection that is not on the axis. Structure-borne
   radiation from the wall mount is the other candidate; a decoupled mount would separate them.
   The top-to-bottom tilt is gone. Level fell only 2.5 dB (6 dB expected from distance alone), but
   the aim also changed (now facing the ring), so that does not check the distance. Figure:
   `wall-mount-day2.pdf` (cell maps across a geometry change compare distance-from-flat only).
   **Decoupling the mount with Thinsulate barely helps** (`wall-mount-decoupled`): 250–400 Hz
   4.18 → 3.97, other bands within ±0.06, overall 2.180 → 2.109; level unchanged (−0.01 dB), so the
   speaker was not displaced. The deep holes stay (306 Hz at +54° −23.9 → −16.3, 297 Hz at −18°
   −16.8 → −20.1, 364 Hz at +90° unchanged). Structure-borne sound is at most a small part; **the
   low-end damage comes from the position.** Figure: `wall-mount-decoupled-day2.pdf`.
   **On the wall itself, further out** (`wall-direct-a/-b`, repeat 0.015 dB): 250–400 Hz recovers
   (3.97 → 2.12) but the damage moves up — 400–630 Hz 3.58, 630 Hz–1 kHz 2.13, 1–1.6 kHz 1.54 — and the
   total is unchanged (2.170 vs 2.109). Level fell 3.9 dB, which puts the sphere roughly 1 m further out
   (distance not stated). Each position outside the ring swaps which band is ruined; none approaches
   the in-ring 1.32. Figure: `wall-direct-day2.pdf`. **Felt and foam behind the speaker did not touch
   the 555 Hz peak** (`wall-direct-absorber`: 4.11 → 4.19 dB in that quarter-octave; total 2.170 →
   2.219). The map moved 1.67 dB and the level rose 0.44 dB, so the speaker was probably nudged while
   the absorber went in. The wall directly behind is therefore not what makes the peak — consistent
   with an on-axis reflection reaching every capsule equally and cancelling in the map. Figure:
   `wall-direct-absorber-day2.pdf`. **Stripping the rest of the ring's wrap** (`ring-bare`) moved the map
   0.36 dB, spread over every capsule with no clamp-like offset (all ≤ 0.08 dB), but left the score
   unchanged (2.219 → 2.205): 250–400 Hz −0.10, 1.6–3 kHz +0.04, 5–6.4 kHz +0.09. As on day 1, the
   ring wrap is worth a little only at the high end. Figure: `ring-bare-day2.pdf`.
   **Back at the ring centre on a new tripod mount** (`center-new-a/-b`, repeat 0.015 dB): 1.786 dB —
   better than any wall position (~2.2), worse than the old in-ring mount (1.324). The wall-position
   peaks are gone, but the arc is **tilted top to bottom by 3.2 dB** (bottom louder), growing with
   frequency (1.6 dB at 250–400 Hz, 3.2 at 0.6–3 kHz, 4.5 at 5–6.4 kHz): the sphere is probably
   sitting below the ring centre (≈15 cm would give 3.1 dB) and/or aimed slightly down. With that
   tilt fitted out the score is 1.241 (old mount, treated the same: 1.105). Level −0.3 dB vs the old
   mount. Figure: `center-new-day2.pdf`. **Levelling the sphere** (`center-leveled`) took the tilt below
   0.5 dB under 3 kHz (1.2 dB at 5–6.4 kHz) and the score from 1.786 to **1.443**. It is the best state
   measured at 1.6–3 kHz (0.83) and 5–6.4 kHz (0.82) and ties the best at 630 Hz–1.6 kHz (1.26 / 0.84
   against 1.30 / 0.81 for Thinsulate-on-wedges and 0.80 on the wall reinforcement); below 630 Hz it is worse
   than the old tripod on the same floor (2.20 / 1.81 against 1.76 / 1.45). The remaining per-capsule
   pattern is a shallow U (0° −0.33 dB, ends +0.16 / +0.51), consistent with the sphere sitting a few
   cm off-centre horizontally, away from the 0° capsule. Figure: `center-leveled-day2.pdf`; against the
   previous cleanest (`floor-carpet`, 1.277): `center-leveled-vs-best-day2.pdf` — 428 cells better,
   467 worse; it loses at 250–630 Hz (+0.46 / +0.31) and wins at 1.6–3 kHz (−0.12) and 5–6.4 kHz (−0.26).
   **An even carpet undoes the floor** (`floor-even-carpet`): 1.443 → **2.540 dB**, 250–400 Hz 2.20 → 4.86
   and 400–630 Hz 1.81 → 2.72, while 1–3 kHz reach their best yet (0.77 / 0.79). The same lesson as the
   flat-vs-heaped carpet test: laid flat, the carpet is a mirror for the low end. Figure:
   `floor-even-carpet-day2.pdf`; every floor state side by side: `floor-states-compare.pdf`
   (`build_compare_figure.py`). **Adding the felt** (`carpet-plus-felt`) trades bands instead of fixing
   them: 250–400 Hz 4.86 → 3.69, but 400 Hz–3 kHz all worse (2.72 → 3.12, 1.61 → 2.27, 0.77 → 1.73,
   0.79 → 1.42); total 2.540 → 2.509. Felt hurts 400 Hz–1.6 kHz here exactly as it did on the
   wedges. Figure: `carpet-plus-felt-day2.pdf`. **A metal rod** (`metal-rod`) changes the map in
   proportion to frequency — 0.12 dB at 250–400 Hz, 0.31 at 1.6–3 kHz, 0.79 at 5–6.4 kHz — spread
   evenly over the capsules; the score below 3 kHz is unchanged (2.509 → 2.506) and 5–6.4 kHz gets
   worse (1.07 → 1.31). A thin hard object is invisible at long wavelengths and scatters at short
   ones. Figure: `metal-rod-day2.pdf`. **Felt on the ceiling** (`felt-ceiling`) is the largest single
   change measured (map moved 2.41 dB rms, spread over every capsule) and improves every band below
   3 kHz: 250–400 Hz 3.69 → 3.05, 1–1.6 kHz 1.74 → 1.14, total 2.506 → **2.051**; 5–6.4 kHz slightly
   worse (1.31 → 1.42). Unlike the Thinsulate on the ceiling on day 1, which hurt 250–400 Hz. It was
   a second piece (the floor felt stayed), so the gain is the ceiling felt alone. Figure:
   `felt-ceiling-day2.pdf`. **Taking the rod out again** (`rod-removed`) confirms the rod result:
   5–6.4 kHz returns 1.42 → 1.10, below 1 kHz the map moves only 0.03–0.05 dB (handling level), and
   at 5–6.4 kHz the removal undoes the insertion (r = −0.87 between the two changes). Score below
   3 kHz unchanged (2.051 → 2.054). Figure: `rod-removed-day2.pdf`. **Raising the carpet on spacers
   and making it less even** (`carpet-raised`, restarted after a disrupted first attempt) moved the map
   0.66 dB and helped every band a little — 2.054 → 2.011, most above 1 kHz (1.6–3 kHz 1.04 → 0.95,
   5–6.4 kHz 1.10 → 0.93) — but left 250–400 Hz where it was (3.06 → 3.04). Figure:
   `carpet-raised-day2.pdf`. Raising it further and adding a felt shield under the electronics
   (`carpet-raised-2`) moved the map 0.48 dB but not the score (2.011 → 2.027; every band within
   ±0.04 below 3 kHz, 5–6.4 kHz 0.93 → 1.03). Figure: `carpet-raised-2-day2.pdf`. Removing the shield
   again (`shield-removed`) separates the two: **the shield alone** moved the map 0.42 dB, most at −18°
   and −36° (0.75 / 0.58 dB — the capsules nearest the electronics), with score 2.027 → 2.028; **the
   extra carpet height alone** moved it 0.31 dB, score 2.011 → 2.028. Neither changes room error.
   Figure: `shield-removed-day2.pdf`. **Taking the ceiling felt down again** (`ceiling-felt-removed`)
   did not simply undo putting it up: the change correlates only −0.60 with the earlier one (slope
   −0.43), and the score moved 2.028 → 2.107 rather than back by 0.46. Now the felt's absence hurts
   250–400 Hz (3.07 → 3.68) but *helps* 630 Hz–3 kHz (1.91 → 1.55, 1.06 → 0.71, 0.97 → 0.72 — the best
   1–3 kHz values measured). The carpet was raised in between, so the ceiling felt's effect depends
   on the floor: it is not a fixed, additive improvement. Figure: `ceiling-felt-removed-day2.pdf`.
   **Laying that felt on the floor instead** (`ceiling-felt-to-floor`) is the third time felt on the
   floor has damaged the mid and high bands: 630 Hz–1 kHz 1.55 → 2.53, 1–1.6 kHz 0.71 → 1.75,
   1.6–3 kHz 0.72 → 1.76, total 2.107 → 2.517; 250–630 Hz unchanged. Figure:
   `ceiling-felt-to-floor-day2.pdf`. **The felt has a foil backing.** Turned foil side inward
   (`felt-foil-in`) it is worse again: 2.517 → **2.753**, most at 250–400 Hz (3.69 → 4.32) and 5–6.4 kHz
   (1.12 → 1.71) — with the foil outward the felt had been absorbing the top band. Plausible reading
   of all the felt results: 2 cm of felt on a foil sheet absorbs only where a quarter wavelength fits
   in the felt (above ~4 kHz) and is a reflector below that, foil up or down. Figure:
   `felt-foil-in-day2.pdf`. **Stripping the foil off the felt** (`felt-foil-removed`; the felt stayed on the floor)
   recovers most of what the foil cost: 2.753 (foil in) and 2.517 (foil away) → **2.159**, and the
   low end is the best since the wedges came out (250–400 Hz 3.47, 400–630 Hz 2.55). That supports
   Adam's reading: the foil sealed the Thinsulate underneath, and without it sound reaches the
   absorber. It is still behind the run with one foil-backed felt (2.107) at 1–3 kHz, but the raised
   carpet has been handled between every one of these runs, which alone moves 1–3 kHz by ~0.5 dB.
   Figure: `felt-foil-removed-day2.pdf`. **Flipping the foil-free felt** (`felt-foil-free-inverted`)
   improved every band (2.159 → **2.008**, 1–1.6 kHz 1.31 → 0.95), the best score since the wedges came
   out. But the map moved 0.85 dB — more than turning over a uniform sheet should cause — so part of
   it is the carpet being rearranged underneath; the side the foil was glued to may also differ.
   Figure: `felt-foil-free-inverted-day2.pdf`. **Removing the glue layer the foil left behind**
   (`felt-bare`) helped the upper bands (1–1.6 kHz 0.95 → 0.74, 1.6–3 kHz 0.95 → 0.84, 5–6.4 kHz
   1.17 → 1.03), cost a little at 400–630 Hz (2.40 → 2.53), and left the total where it was
   (2.008 → **1.998**) — the best since the wedges came out. Figure: `felt-bare-day2.pdf`. **Raising the
   floor layer further** (`floor-raised-3`) moved the map 0.48 dB but not the score (1.998 → 1.992;
   250–400 Hz 3.39 → 3.32). Figure: `floor-raised-3-day2.pdf`.
   **USB hub resets happened twice today** (16:08 and 18:09): the hubs reset and some capsules came
   back delivering full-scale noise. `capture_rig` now refuses to start on such a stream
   (`rig.assert_streams_ok`, a 0.5 s silence check at −40 dBFS); fix by re-enumerating the capsule.
9. **What remains:** 250–400 Hz is still the worst band, 1.74 dB with the carpet on the floor.

## Files

- `tripod-unwrapped.pdf/.png` — the headline figure (built by `build_tripod_figure.py`)
- `carpet-floor-vs-ceiling.pdf/.png` — no carpet, floor, ceiling side by side
- `felt-floor-day2.pdf/.png` — felt on the floor, day 2
- `grid-95.txt` — the exact 95 frequencies of every treatment run (pass to `--freqs`)
- `floor-carpet.pdf/.png` — the carpet step (`build_step_figure.py <ref> <run> "<what>" <name>`; its last panel colours each cell by whether it moved toward flat (blue, better) or away (orange, worse), with a per-capsule net in the margin)
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
