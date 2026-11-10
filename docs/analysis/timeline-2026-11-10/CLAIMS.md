# Claims ledger

Adam's account of the work from 2 October 2026 on, each statement checked against the recordings.
Numbers come from `levels.csv` (built by `story_levels.py`), which governs where this file and it disagree.
All values are at 2000 µs. Level = total 500 Hz–20 kHz, mean over the microphones from −54° to +90°,
mean of the run's repeats. Thrust is shown as a magnitude. Stage 6 is at 1900 µs, from `levels-1900.csv`.

Verdicts: **supported**, **partly** (true in a narrower form, stated), **not checkable** (needs something the recordings do not hold).

## Verdicts at a glance

| Stage | Dates | Statement | Verdict | Evidence |
|---|---|---|---|---|
| 1 | 2, 7 Oct | First rounds of materials around the 5 in propeller | Supported | Every material louder than the bare propeller (72–73 dB against 76.5–79.7 dB) and lower in thrust (3.6 N against 2.9–3.5 N) |
| 2 | 8–9 Oct | Small duct with a membrane wall, no aerodynamic treatment | Supported | Thrust 3.76 N bare, 0.37–1.20 N ducted; duct 8.5–15.7 dB louder than the bare propeller |
| 2 | 8–9 Oct | The membrane lets sound reach the material | Not checkable | No run of the same duct with a solid wall |
| 3 | 27 Oct–2 Nov | Before the inlet, noise was heavily influenced by aerodynamic performance | Partly | More thrust went with less noise on 2 Nov (r = −0.98) and 29 Oct (r = −0.96), not on 28 Oct; the level moved about 1 dB for 1.3 N |
| 3 | 27 Oct–2 Nov | Thinsulate 4 was quiet and the most efficient | Supported for 2 Nov only | 2 Nov: +1.26 N, +13 % N/W, −0.95 dB against the unlined duct; near the bottom on thrust on 28 Oct |
| 3 | 27 Oct–2 Nov | The Thinsulate 4 gain is not a win: it came from shaping the airflow, not from the material | Supported for thrust, mostly for noise | A plain inlet gave +2.1 N against +1.26 N for the lining; with the inlet the lining adds no thrust and takes off 0.31 dB, not 0.95 dB |
| 3 | 27 Oct–2 Nov | Thinsulate 4 was the closest to the inlet diameter | Not checkable | No geometry in the recordings |
| 4 | 3–6 Nov | The inlet settled thrust around 10 N for all materials | Supported | Ten runs: 10.03–10.27 N; unlined duct 8.0 N without the inlet, 10.1 N with it |
| 5 | 2, 3 Nov | The inlet reduced the influence of the materials | Supported | Thinsulate 2 / 4: thrust gain +0.80 / +1.26 N became −0.05 / −0.06 N; level −0.60 / −0.95 dB became −0.22 / −0.31 dB |
| 5 | 2, 3 Nov | Aerodynamics matters most | Supported for thrust, not for noise | Inlet: +2.1 N at an unchanged level; the duct stays 13.1 dB louder than the bare propeller |
| 6 | 9 Nov | The linings do more with the small propeller | Supported | 1900 µs: −0.72 / −0.90 dB with the 5 in propeller, +0.04 / −0.25 dB with the 8 in |
| 6 | 9 Nov | Because the duct's aerodynamic influence is minimised there | Not checkable yet | No bare 5 in propeller on this motor; the lining costs the same 0.06–0.08 N with both propellers |

## Stage 1 — materials around the 5 in propeller (2 and 7 Oct, `v1-`)

Stated: first rounds of materials around the 5 in propeller, from 2 October.

- Dates **supported**: 2 Oct 18:13–19:15 (bare, cage, cork, rubber, felt + rubber, felt) and 7 Oct 13:47–14:59
  (PU foam, PU foam double, Thinsulate 4, Thinsulate 8, two combinations). One repeat each.
- Every material was louder than the bare propeller of 2 Oct (72.0–72.9 dB): 77.7–79.7 dB on 2 Oct,
  76.5–78.7 dB on 7 Oct (the 7 Oct set has no bare run of its own day).
- Thrust fell with every material: 3.62–3.65 N bare, 3.23–3.49 N on 2 Oct, 2.88–3.33 N on 7 Oct.
- 7 Oct 16:56–18:39: the same idea with the 8x4.5 propeller, three repeats. Bare in the cage 7.05 N / 75.6 dB;
  with materials 5.69–6.58 N / 82.0–86.9 dB.

## Stage 2 — small duct with a membrane wall (8–9 Oct, `v1-membrane-`)

Stated: a small duct with an Oracover membrane wall, so sound reaches the material with little attenuation;
no aerodynamic treatment.

- Dates **supported**: 8 Oct 16:46–16:52, 9 Oct 15:12–18:10, three repeats each.
- The duct cost most of the thrust: bare propeller 3.76 N (9 Oct 18:10), ducted 0.37–1.20 N at similar power (127–135 W against 140 W).
- The duct was 8.5–15.7 dB louder than the bare propeller (73.9 dB bare; 82.3–89.5 dB ducted).
- Lowest level: Thinsulate 4 (82.3 dB) and Thinsulate 2 (83.7 dB), but these two also had the lowest thrust
  (0.39 and 0.37 N against 0.88–1.20 N for the rest), so level and loading changed together.
- "Membrane lets sound through to the material" is **not checkable** from these runs: there is no same-duct run with a solid wall.

## Stage 3 — the 8 in duct without an inlet (27 Oct–2 Nov, `r27-`)

Stated: before the inlet, the noise level was heavily influenced by aerodynamic performance, seen as thrust going up or down.

- **Partly.** Thrust did vary a lot between set-ups: 5.67–9.23 N over the no-inlet ducted runs, 7.93–9.23 N on 2 Nov alone.
- On 2 Nov (five set-ups, eight runs) more thrust went with a lower level: r = −0.98, −0.77 dB per N.
  On 29 Oct (four runs) the same: r = −0.96.
- On 28 Oct the sign is the other way (r = +0.59, eight runs, including the Thinsulate 2 run whose mount was suspect),
  and on 30 Oct thrust barely varied (8.51–8.74 N).
- The level range is small: 90.7–91.7 dB on 2 Nov, about 1 dB for 1.3 N of thrust. "Heavily" does not describe the total level.
- The lining changes thrust and absorption at once, so these runs cannot say which one moved the level.

Stated: Thinsulate 4 had great acoustic performance while being the most efficient.

- **Supported for 2 Nov, not for the earlier days.** 2 Nov, two runs: 9.23 N, 0.0392 N/W, 90.7–90.8 dB —
  the highest thrust, highest N/W and lowest level of that day's ducted set-ups (unlined: 7.93–8.01 N, 0.0346–0.0347 N/W, 91.7 dB).
  That is +1.2 N, +13 % N/W and −0.95 dB against the unlined duct.
- 27 Oct: Thinsulate 4 was the quietest lined run (89.2 dB) but had low thrust (7.52 N).
- 28 Oct: Thinsulate 4 gave 7.34 N and 0.0322 N/W, near the bottom; felt was highest (8.91 N, 0.0381 N/W).
- All Thinsulate thrusts rose by about 1 N between 28 Oct and 30 Oct (the linings were remounted), so the mount matters as much as the layer count.

Stated (10 Nov): this step is not a win, because the gain cannot be attributed to the material; it came from how the
lining shaped the airflow, since a plain, non-acoustic inlet worked better.

- **Supported for thrust, mostly for noise.** The plain inlet gave the unlined duct +2.1 N (7.97 → 10.11 N); Thinsulate 4 without
  the inlet gave +1.26 N. Once the inlet had fixed the thrust, the same lining added nothing (−0.06 N).
- Noise: Thinsulate 4 took off 0.95 dB without the inlet and 0.31 dB with it (each against the unlined duct of its own day).
  So about a third of the reduction stays when the flow is fixed, and about two thirds went with the thrust.
  The two figures are from different days.
- The inlet "worked better" on thrust only. It did not lower the level: the unlined duct with the inlet reads 91.36 dB,
  Thinsulate 4 without the inlet 90.75 dB (different days).

Stated: Thinsulate 4 was the closest to the inlet diameter for this duct.

- **Not checkable** from the recordings. Needs: duct inner diameter, thickness of one Thinsulate layer as fitted, inlet throat diameter.

## Stage 4 — the inlet (3–6 Nov, `r27-inlet-`)

Stated: aerodynamic treatment turned out to be crucial; with the inlet, thrust settled around 10 N for all materials.

- **Supported.** Ten runs with the inlet over 3, 4 and 6 Nov: 10.03–10.27 N (standard deviation 0.09 N), 0.0422–0.0432 N/W.
  Unlined duct: 7.93–8.01 N without the inlet (2 Nov), 10.08–10.13 N with it (3 Nov). Bare propeller: 10.57 N (2 Nov).
- With the inlet the level spread across set-ups is 90.9–91.4 dB, and the unlined duct is at the same level as without it (91.4 against 91.7 dB, different days).

## Stage 5 — what the inlet did to the materials (2 Nov against 3 Nov)

Stated: the inlet's aerodynamic gain reduced the influence of the materials; aerodynamics matters most, and
materials should be tried inside a structure that is already aerodynamically sound.

Each difference is lining minus the unlined duct of the same day; the two columns are different days.

| Lining | Thrust, no inlet (2 Nov) | Thrust, inlet (3 Nov) | Level, no inlet (2 Nov) | Level, inlet (3 Nov) |
|---|---|---|---|---|
| Thinsulate 2 | +0.80 N | −0.05 N | −0.60 dB | −0.22 dB |
| Thinsulate 4 | +1.26 N | −0.06 N | −0.95 dB | −0.31 dB |
| Thinsulate 8 | +0.85 N | not run | −0.54 dB | not run |
| Thinsulate 10 | +0.91 N | not run | −0.80 dB | not run |
| Thinsulate 4 + rubber | not run | +0.01 N | not run | +0.03 dB |
| Felt | not run | −0.07 N | not run | −0.35 dB |

Unlined reference: 7.97 N / 91.70 dB on 2 Nov (two runs), 10.11 N / 91.36 dB on 3 Nov (two runs).
Two runs of the same set-up on the same day differ by 0.01–0.05 dB and 0.05–0.08 N.

- "The inlet reduced the influence of the materials": **supported** for Thinsulate 2 and 4, the only linings run both ways.
  Their thrust gain went from +0.8 / +1.3 N to nothing, and their level reduction to about a third.
- "Aerodynamics matters most": **supported for thrust, not for noise.** The inlet gave +2.1 N to the unlined duct and
  left its level where it was (91.70 → 91.36 dB, different days). The duct with the inlet is still 13.1 dB louder
  than the bare propeller (78.2 dB at 10.57 N, 2 Nov) at 0.5 N less thrust. Neither the inlet nor any lining has touched that.
- The 5 in propeller result of 9 Nov looked like a counter-example; Adam's explanation of it is Stage 6.

## Stage 6 — 5 in propeller in the 8 in duct, inlet on (9 Nov, `g5-`)

Stated: with the small propeller far from the wall, the duct's aerodynamic influence is minimised, so it acts
more like a cover holding the material; the duct matters less aerodynamically than when the propeller was big
and close to it. That is why the linings do more here.

Compared at 1900 µs (most 2000 µs steps of 9 Nov have a fault). Numbers from `levels-1900.csv`.
Each difference is lining minus the unlined duct of the same day.

| Lining | Thrust, 8 in prop (3 Nov) | Thrust, 5 in prop (9 Nov) | Level, 8 in prop (3 Nov) | Level, 5 in prop (9 Nov) |
|---|---|---|---|---|
| Thinsulate 2 | −0.06 N (−0.7 %) | −0.06 N (−2.0 %) | +0.04 dB | −0.72 dB |
| Thinsulate 4 | −0.06 N (−0.7 %) | −0.08 N (−2.8 %) | −0.25 dB | −0.90 dB |

Unlined reference: 8.87 N / 89.64 dB with the 8 in propeller (two runs), 2.83 N / 78.08 dB with the 5 in (one full run;
the stopped run gives 2.79 N / 78.11 dB from a single repeat). Thinsulate 2 is the mean of three runs, Thinsulate 4 of two.
Runs of the same set-up differ by up to 0.14 dB and 0.01 N.

- "The linings do more with the small propeller": **supported.** −0.7 and −0.9 dB against +0.0 and −0.25 dB.
- "Because the duct's aerodynamic influence is minimised": **not checkable yet.** The recordings hold no bare 5 in
  propeller on this motor, so what the duct does to this propeller's thrust and noise is unknown.
  What is recorded does not show a smaller aerodynamic effect of the lining: it costs the same 0.06–0.08 N with both
  propellers, which is a larger share of the small propeller's thrust.
- The run that would settle it: the bare 5 in propeller on the AXI 2217, same day as the unlined duct with the inlet.
  If the explanation is right, thrust and N/W should be close to the ducted values and the duct should add far less
  than the 13 dB it adds to the 8 in propeller.

## Open points

- 27 Oct 17:24 `r27-petg-0-8mm` (motor typed `axi2212`) reads 74.8 dB where the other ducted runs read 89–91 dB, at ordinary thrust (7.70 N). Unexplained; left out of the numbers above.
- 23 Oct `m8-baseline`: thrust varied 7.29–9.03 N across its repeats.
- Days are not mixed in any difference above unless marked.
