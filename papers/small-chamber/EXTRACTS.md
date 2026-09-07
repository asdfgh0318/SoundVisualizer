# Small-chamber / near-wall acoustic-problem literature — extracts

Scope: acoustic problems specific to SMALL anechoic/hemi-anechoic chambers and
near-wall measurement — wedge-tip/wall reflections at short range, direct–reflected
comb filtering, minimum mic/source-to-wall distance, qualification of small chambers,
mini "anechoic box" designs, image-source analysis, and whether reflections are
low-frequency-only or also mid/high-frequency.

Every entry below was read at source (PDF downloaded, `pdftotext -q` extracted to
`txt/`, quotes verified against that extraction). Two entries (Rusz 2015, Cao et al.
2025) are flagged as **tangential** — retrieved and read, but their chamber is not
small by the task's <~60 m³ criterion, or the paper is not about chamber acoustic
problems; they are kept only for background wedge-theory / context and should not be
cited as "small-chamber reflection" evidence without that caveat.

---

## 1. Burnett & Nedzelnitsky (1987) — *Free-Field Reciprocity Calibration of Microphones*

**Citation as printed:** E. D. Burnett and V. Nedzelnitsky, "Free-Field Reciprocity
Calibration of Microphones," *Journal of Research of the National Bureau of
Standards*, Vol. 92, No. 2, pp. 129–151, March–April 1987.

**File:** `Burnett-Nedzelnitsky_1987_JResNBS_free-field-reciprocity-calibration-chamber-deviations.pdf`

**Facility:** Single-walled anechoic chamber at NBS (Gaithersburg, MD), used for the
1/2-inch microphone free-field reciprocity calibration service (2.5 kHz–20 kHz
nominal service range, but chamber characterization data shown from well below that).
Chamber width 2.1 m, height 1.6 m, depth 1.6 m between wedge tips — **free volume 5.4
m³** — with **0.3 m deep fiberglass wedges** (p. 136). Located in a quiet windowless
control room isolated by ~0.3 m reinforced concrete walls; chamber rests on
elastomeric blocks.

**What was observed:** Two source (transmitting) and receiving microphones were
traversed apart on an axial slide from 1 cm to 31 cm and the measured level compared
to an inverse-distance (near-field-corrected) prediction. Deviations from that
relationship were mapped as a function of separation and frequency (Figs. 4, 5–18,
19). The authors attribute the deviations to three candidate mechanisms and argue
through which dominates:
- **Factor 1 — chamber-wall ("room") reflections**, producing axial-mode-like maxima/minima at
  separations that are integer multiples of a half-wavelength (p. 140): a maximum near
  15 cm and 27 cm separation at 3.15 kHz corresponds "reasonably closely" to the
  wavelength (~11 cm) at that frequency, though the pattern also shows non-axial-mode
  structure.
- **Factor 2 — reflections between the two microphones themselves**, producing minima
  at integer half-wavelength separations, e.g. at 4.0 kHz minima at 12, 17, 21, 26 and
  30 cm vs. a wavelength of ~8.6 cm (p. 140).
- The paper states it "is not possible completely to separate" the two reflection
  mechanisms (p. 140), but argues Factor 1 dominates because deviations grow at
  **lower** frequencies where the absorbing wedges are electrically/acoustically
  smaller relative to wavelength, whereas inter-microphone diffraction/reflection
  effects should grow at **higher** frequencies as the microphone diameter becomes
  comparable to the wavelength (p. 141) — and the observed trend is the opposite,
  i.e. worse at low frequency.

**Frequency range affected:** The chamber's own working range for this service is
2.5 kHz–20 kHz, but the qualification/deviation data discussed span roughly 1.25 kHz
upward; "free-field reciprocity measurements encounter the greatest experimental
difficulties" in the 1.25–4 kHz band, per the abstract. The paper explicitly frames
wall-reflection-driven deviation as a low-to-**mid**-frequency problem (worse as
frequency drops, in a chamber whose absolute floor is several kHz because of its
small size), not as a purely sub-100-Hz cutoff issue — i.e. in a small (5.4 m³)
chamber, "low frequency" for reflection purposes is already in the low-kHz range.
Final combined uncertainty from all effects: 0.16 dB or better at 1.25–5 kHz, 0.07 dB
or better at 5–20 kHz (abstract).

**What (if anything) "fixed" it:** Not a design fix — the paper's response is
metrological: renormalizing/correcting the data against a reference position and
bounding the residual as measurement uncertainty (Table/Fig. 19), rather than
eliminating the reflections physically.

**Verbatim quotes:**
- "Many of the reflections within the anechoic chamber will produce deviations from
  the inverse distance relationship which appear somewhat random." (p. 140)
- "It is also expected that the effect of room reflections would be more pronounced
  at the lower frequencies of measurement, at which the dimensions of the
  sound-absorbing wedges on the walls are smaller compared [to wavelength]." (p. 141)
- "It would be expected that the effect of microphone reflections would become more
  pronounced as the frequency is increased ... and less pronounced as the separation
  distance between the microphones increased." (p. 140)

---

## 2. Rajmane & Baumann (2016) — *Detection of Reflecting Objects in Anechoic Chambers*

**Citation as printed:** Abhay Rajmane and Walter Baumann (G+H Schallschutz GmbH),
"Detection of Reflecting Objects in Anechoic Chambers," *DAGA 2016 Aachen*, pp.
331–333.

**File:** `Rajmane-Baumann_2016_DAGA_detection-reflecting-objects-anechoic-chambers.pdf`

**Facility:** Not dimensioned in the paper (no chamber volume/wedge-depth figures
given); it is described only as a qualified anechoic chamber tested per DIN EN ISO
3745 Annex A / ISO 26101, with measurement path and reflector centreline at 1.5 m
above the walking net.

**What was observed:** Deliberately introduced flat steel-sheet reflectors (1.5 mm
steel, square 35×35 cm and 10×10 cm, and rectangular 70×17 cm / 17×70 cm) were placed
at a known location while a microphone was swept along the qualification traverse
under tonal (1/3-octave) excitation. The presence/absence of visible interference
(constructive/destructive ripple on the inverse-square-law trace) was tabulated
against excitation frequency (p. 332, Tables 1–2):
- 35×35 cm reflector: interference **not** observed at 800–1000 Hz, but observed
  from **1250 Hz upward** (through 5000 Hz, the top frequency tested).
- 10×10 cm reflector: interference observed only at 3150–5000 Hz (needs much shorter
  wavelength, i.e. higher frequency, than the larger sheet).
- Both 70×17 cm/17×70 cm rectangular reflectors: interference from **1000 Hz
  upward**.
- Rule extracted (p. 333): a reflecting object is detected once the wavelength of the
  tonal excitation is ≤ the object's characteristic (equivalent-square) side length —
  for rectangles up to 4:1 aspect ratio the same rule holds using the equivalent
  square side.
- In a second experiment, a sine-burst excitation and 60 µs time-domain sampling was
  used to time-tag the direct vs. reflected arrival at the microphone; measured time
  lags of 3.5 ms, 2.3 ms and 12 ms converted (via speed of sound) to path-length
  differences of 1.2 m, 0.8 m and 4.1 m, matching independently measured geometric
  path differences of 1.2 m, 0.7 m and 4 m (p. 332, Table 3).

**Frequency range affected — explicitly BOTH low and high, size-dependent:** This
paper is the clearest evidence in the set that wall/object reflections in an anechoic
chamber are **not confined to low frequency** — a small object reflects only at
correspondingly **high** frequency (short wavelength ≤ object size), while a large
object (comparable to typical chamber-wall fixtures) reflects starting in the
mid-frequency range (~1–1.25 kHz here) and continues to be visible at every higher
frequency tested up to 5 kHz.

**What fixed it:** Not a chamber redesign — a diagnostic/mitigation procedure:
locate the reflecting object (size from the onset frequency, position from the
time-of-flight lag) and physically relocate/reorient it so it no longer intrudes on
the qualified free-field region (p. 333, Summary).

**Verbatim quotes:**
- "The zone of these interferences cannot be qualified as free-field region for given
  source location and given (reflecting) objects inside anechoic chamber." (p. 331)
- "The reflecting object is identified, when length of side of square object is
  greater than or equal to wavelength of tonal excitation frequency." (p. 332)
- "If deviations from inverse square law are observed during anechoic chamber
  qualification measurement according to ISO 26101, the information about reflecting
  object can be judged." (p. 333)

---

## 3. Orrego González, Ealo Cuello & Pazos Ospina (2018) — *Low-cost and easily implemented anechoic acoustic chambers*

**Citation as printed:** Alejandro Orrego González, Joao Luis Ealo Cuello, Jhon
Fernando Pazos Ospina, "Low-cost and easily implemented anechoic acoustic chambers" /
"Cámaras anecoicas acústicas de bajo costo y fácil implementación," *Scientia et
Technica*, Año XXIII, Vol. 23, No. 04, pp. 471–478, diciembre de 2018. Universidad
Tecnológica de Pereira. ISSN 0122-1701.

**File:** `Orrego-Ealo-Pazos_2018_ScientiaTechnica_low-cost-small-anechoic-chamber.pdf`

**Facility:** A genuinely small, home/low-cost-built anechoic chamber: **working
dimensions 1.94 m × 1.91 m × 1.84 m** (long × wide × high) — internal working volume
≈ 6.8 m³ — built from polyurethane foam, steel tube frame, fiberglass, fibercement
and particle-board panels (p. 471). **Nominal cutoff frequency 400 Hz.** Measured
reverberation time inside the chamber ≈ 30 ms (p. 472). Cost quoted at $200 USD per
square metre of effective finished volume.

**What was observed:** SPL deviations from the inverse-square law were measured
along a diagonal traverse per the qualification method of Gómez et al., compared
against the ISO 3745 permissible-deviation table (their Table 1) by 1/3-octave band.
Results (p. 476, Fig. 10 and surrounding text):
- One measured point **exceeded the ISO 3745 limit by 1.0 dB at 500 Hz** — attributed
  possibly to experimental-setup imperfection and to a small frequency spacing
  between adjacent room eigenmodes near the (single, elongated) 400 Hz cutoff
  wedge/mode-density design.
- Below the nominal cutoff frequency (400 Hz), deviations **exceed** the ISO 3745
  limit, as expected.
- The chamber **meets** the ISO 3745 deviation limit for **frequencies above 500 Hz**
  and best performance is reported **between 500 Hz and 4 kHz** for all measured
  points (p. 476–477) — the upper end of the tested/verified range is bounded by the
  1/3-octave bands used in the reported evaluation, not by a stated re-emergence of
  reflection at high frequency.
- FEM simulation of the wedge itself (impedance-tube style model) predicted about
  **47 dB** attenuation relative to the incident plane wave, valid up to 4 kHz (p.
  475).
- Background noise was ≥ 10 dB below the measured pink-noise signal in all tested
  bands (p. 476).

**Frequency range affected:** Explicitly **low-frequency-dominated** in this
particular small chamber — deviations are worst below/near the 400 Hz cutoff and at
one isolated mid-band point (500 Hz); no high-frequency (multi-kHz) breakdown is
reported, though the authors note the qualification traverse itself was only
evaluated up to 4 kHz and a single diagonal path, so high-frequency wedge-tip/edge
effects were not separately investigated.

**What fixed/mitigated it:** Chamber geometry and wedge design were driven by the
"desired cutoff frequency" target (400 Hz) via wedge depth; the authors note explicit
lower cost/performance trade-off — a lower target cutoff (e.g. 100 Hz) would need
deeper wedges and a larger, more expensive chamber (p. 477–478, Conclusions).

**Verbatim quotes:**
- "The working dimensions of the chamber are 1.94 m long x 1.91 m wide x 1.84 m high.
  The nominal cutoff frequency is 400 Hz." (p. 471)
- "It is appreciated that one measured point is exceeding the limits by 1.0 dB at 500
  Hz." (p. 476)
- "Results showed that the anechoic chamber presented the best performance for
  frequencies between 500 Hz and 4 kHz for all points measured." (p. 477)

---

## 4. Biesel & Cunefare (2003) — *A Test System for Free-Field Qualification of Anechoic Chambers*

**Citation as printed:** Van B. Biesel and Kenneth A. Cunefare (Georgia Institute of
Technology), "A Test System for Free-Field Qualification of Anechoic Chambers,"
*Sound and Vibration*, May 2003, pp. 22–26.

**File:** `Biesel-Cunefare_2003_SoundVibration_test-system-freefield-qualification.pdf`

**Note on redundancy:** this is a trade-magazine companion piece by the same lead
author/group as the already-held peer-reviewed Cunefare (2003) *JASA* qualification
paper, describing the same Georgia Tech chamber and continuous-traverse measurement
system; it is kept here as a separate, distinctly-worded source because it makes the
mid/high-frequency point unusually explicitly and includes different figures, but its
core claims should be read as corroborating, not independent of, the already-held
JASA paper.

**Facility:** Georgia Institute of Technology anechoic chamber (no volume/wedge-depth
figures stated in this article); measurements taken toward a room corner opposite the
chamber door, at distances of roughly 3–10 ft from the source, up to 10 kHz.

**What was observed:** Comparing standard discrete-point traverses (1 ft spacing, the
"common practice") against a new continuous, motorized traverse system, the authors
show (Fig. 6, p. 25) that discrete sampling **misses spatial structure in the
inverse-square-law deviation** that the continuous trace reveals, and that this
under-sampling problem gets worse, not better, as frequency rises.

**Frequency range affected — explicitly mid/high, not just low:**
- "the common practice of measuring widely spaced points along a traverse line is an
  inadequate measure of inverse square law performance, **particularly for
  frequencies at and above 1000 Hz**" (p. 22, abstract).
- "This example shows how the discrete spacing fails to capture the complexity of the
  free-field deviation over the traverse span at frequencies as low as 500 Hz, **and
  especially at frequencies above 1 kHz**." (p. 25)
This directly supports the idea that comb-filter-like spatial ripple from
wall/near-field reflections is present (and under-resolved by coarse sampling) well
above the classic "low-frequency cutoff" band, up into the kHz region tested (data
shown to 10 kHz on the frequency axis of Fig. 6).

**What fixed it:** Not a chamber redesign but a measurement-method fix: an automated,
repeatable **continuous** microphone traverse (LabVIEW motion control + MATLAB
processing) replacing manual discrete-point measurement, giving real-time
pass/fail feedback against the ISO 3745 / ANSI S12.35 tolerance band.

**Verbatim quotes:**
- "the common practice of measuring widely spaced points along a traverse line is an
  inadequate measure of inverse square law performance, particularly for frequencies
  at and above 1000 Hz." (p. 22)
- "the discrete spacing fails to capture the complexity of the free-field deviation
  over the traverse span at frequencies as low as 500 Hz, and especially at
  frequencies above 1 kHz." (p. 25)
- "The cause of the inconsistencies was found to be the inability to produce
  repeatable microphone and source positions." (p. 22)

---

## 5. [TANGENTIAL — large chamber] Rusz (2015) — *Design of a Fully Anechoic Chamber*

**Citation as printed:** Roman Rusz, "Design of a Fully Anechoic Chamber," Master's
Degree Project, TRITA-AVE 2015:36, KTH Royal Institute of Technology / Honeywell /
Technical University of Ostrava, 2015.

**File:** `Rusz_2015_KTH-thesis_design-of-fully-anechoic-chamber.pdf`

**Caveat:** the chamber this thesis actually designs is **367.5 m³** (7 m × 7 m ×
7.5 m inner net volume, p. 57) — well above the task's <~60 m³ "small chamber"
threshold. It is retained here only for its general wedge/cutoff-frequency theory
(reflection-coefficient vs. wedge-length curves, room-mode calculation method),
which is background applicable to chambers of any size, not as small-chamber
reflection *evidence*. Much of its theoretical content (cutoff-frequency vs.
wedge-depth curves, pressure-reflection-factor formalism) overlaps material already
covered by the held Jiang (2016, JSV), Bonfiglio & Pompoli (2013, JASA) and Schneider
(2009, JSV) papers.

**What it covers:** ISO 3745's rule that the test-object volume must be ≤ 5% of
chamber net volume (p. 9); room-mode (axial/tangential/oblique) theory and a
worked eigenfrequency table for the 7×7×7.5 m design, showing the first ten modes
between 22.9 Hz and 73.5 Hz (p. 57–58); wedge cutoff frequency is defined as "that
frequency at which the pressure reflection rises to 10 percent of the pressure in a
normally reflected wave" (paraphrase of source, cited to Ver & Beranek); cutoff
frequency vs. wedge length curves from FEM (Ch. 3).

**Frequency range affected:** Purely a low-frequency (room-mode / cutoff) design
problem in this source — no discussion of mid/high-frequency wedge-tip specular
return or edge diffraction.

**Verbatim quotes:**
- "Inner net volume of the chamber: 367.5 m3" (p. 57)
- "the lowest third octave band for which the anechoic chamber should be validated is
  the third octave band with central frequency 100 Hz... the strongest, therefore,
  most important room modes are below this frequency." (p. 57)
- "Only requirement is determined by ISO 3745 standard which prescribes the maximum
  volume of the object that can be measured in the chamber, which is 5% of the inside
  net volume of the chamber." (p. 9)

---

## 6. [TANGENTIAL — not chamber-problem-focused] Cao et al. (2025) — *Anechoic Noise Characterization of Sub-7kg Multi-Rotor Drones*

**Citation as printed:** Runzhen Cao, Zhicheng Zhang, Zhenjun Peng, Zhida Ma, Wangqiao
Chen, Peng Zhou, Xin Zhang, "Anechoic Noise Characterization of Sub-7kg Multi-Rotor
Drones: Configuration Effects and SPL Scaling Models," *11th Convention of the
European Acoustics Association (Forum Acusticum 2025)*, Málaga, Spain, pp. 1697ff.
DOI: 10.61782/fa.2025.0137.

**File:** `Cao-etal_2025_ForumAcusticum_sub-7kg-multirotor-anechoic-noise.pdf`

**Caveat:** included in the retrieval batch because it is a drone/anechoic-chamber
paper, but it is **not** about chamber acoustic problems — it is a drone-noise
scaling-law study. The chamber it uses (Hong Kong UST Aerodynamics and Acoustics
Facility) is medium-sized, not small: "5.1 m [wedge tip-to-tip?], is fully
wedge-lined and provides free-field conditions above 100 Hz," with an internal
working volume of "6.8 m × 4.8 m" defined by a safety cage (p. 3 of PDF). No
reflection/deviation measurements, wedge-tip data, or near-wall distance analysis
appear in the text. **Not used for any claim in `docs/` beyond this note.**

**Verbatim quote:**
- "is fully wedge-lined and provides free-field conditions above 100 Hz. A nylon
  safety cage was installed to define an internal working volume of 6.8 m × 4.8 m..."
  (PDF p. 3)

---

## Summary across the retrieved set

The two sources that most directly answer the task's "low-frequency only, or also
mid/high-frequency?" question **converge on: also mid/high-frequency, and the
threshold scales with the reflecting surface/object size, not with a single fixed
cutoff.** Rajmane & Baumann (2016) show a 10×10 cm object only reflects above ~3 kHz
while a 35×35 cm or 70×17 cm object already reflects from ~1–1.25 kHz; Biesel &
Cunefare (2003) show spatial free-field-deviation structure that discrete
qualification traverses miss "especially at frequencies above 1 kHz," in a chamber
whose nominal cutoff is presumably far below that. Burnett & Nedzelnitsky's small
(5.4 m³) NBS chamber shows measurable reflection-driven deviation as high as 3–5 kHz
between closely-spaced microphones, worse (not better) at the lower end of the
1.25–20 kHz band they studied, consistent with wedge absorption degrading as
wavelength grows relative to wedge depth — but the absolute frequencies involved are
still in the kHz range because the chamber is small. Only Orrego González et al.'s
6.8 m³ chamber shows a more classical picture (deviation concentrated at/below its
400 Hz cutoff, one isolated mid-band exceedance at 500 Hz, clean 500 Hz–4 kHz
otherwise) — but note their traverse was not extended past 4 kHz, so it cannot rule
out a high-frequency wedge-tip effect the other papers found only because they
looked above that.
