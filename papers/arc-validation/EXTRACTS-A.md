# Thread A — single-reflection interference: how big, and what correction is legitimate

Compiled 2026-09-08. Every held paper below was re-opened as a PDF, re-extracted fresh with
plain `pdftotext -q` into `papers/arc-validation/refetch-txt/`, and quoted from that fresh dump
(not from the earlier EXTRACTS/MATRIX notes, which were used only to find candidates and are
compared against at the end of each entry). New PDFs are saved in `papers/arc-validation/` with
text in `papers/arc-validation/txt/`. Page numbers are the **printed** page where the source has
one; where a source has no printed pagination (arXiv, some standards previews) the PDF page is
given and flagged as such.

---

## 1. Rasmussen, P. & Winberg, L. (2022) — *Accurate measurement of Drone Noise on the ground*

**File:** `papers/chamber-problems/Rasmussen-Winberg_2022_QuietDrones_drone-noise-on-the-ground.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/Rasmussen-Winberg_2022_QuietDrones.txt`)
**Venue:** Quiet Drones, 2nd International e-Symposium on UAV/UAS Noise, 27–30 June 2022.
**Evidence level:** conference paper; authors are GRAS Sound & Vibration staff (acoustic
consultant / business development), so flagged as practitioner/vendor-adjacent, but the content
is a physically modelled (COMSOL BEM) analysis, not a marketing note — treated as conference tier.
Identity confirmed from the PDF's own page 1 header/byline.

**What it says (Q1, Q3):** For a microphone at height *h* = 1.2 m directly under a hovering
source (ICAO Annex 16 pole-microphone geometry), interference between the direct and the
ground-reflected wave is "like a comb filter" with the first minimum at f₀ = c/(4·l) ≈ 71.4 Hz
and the first maximum at f₁ = c/(2·l) ≈ 143 Hz (p. 3) — **note:** the paper's own typeset
equations use the italic symbol that renders as lowercase "l", not "h", even though the same
quantity is called "microphone height h" in the body text one sentence earlier and in Figure 1's
own label ("Microphone at height h"). I opened the PDF page as an image to check this was not a
`pdftotext` artefact: **it is printed as "l" in the source PDF itself** — a minor internal
notation inconsistency in the paper, not an extraction error. In 1/3-octave-filtered data, "the
frequencies coincident with the comb-filter minima are reduced by more than 20 dB, and the
frequencies coincident with the comb-filter maxima are amplified by 6 dB" (p. 4). The resulting
overall (broadband) level is "3 dB higher than the corresponding level measured in a full free
field" for a pole microphone, and 6 dB higher (simple pressure doubling) for a microphone
flush-mounted in a fully reflecting ground board (p. 4, p. 10–11). Broadband sources can in
principle be corrected for the comb filter; **"if the source signal contains pure tone
components, it will not be possible to do this correction"** (p. 5) — some tones land on a
comb maximum ("+6dB by comb filter") and are amplified, others land on a minimum and are
"Removed by comb filter" (Fig. 6, p. 5), and neither can be recovered after the fact. Hover
(source directly overhead) is the worst geometry for interference; for a fly-by the comb pattern
shifts continuously with elevation angle (Fig. 9, p. 7). Even soft ground (flow resistivity
30 kPa·s/m²) still gives "considerable" interference at 1.2 m, and moving the microphone closer
to the ground "will further increase the influence of the ground reflection" (p. 6). A ground
board with a **flush-mounted** microphone avoids the interference entirely (simple, frequency-flat
pressure doubling, usable to 20 kHz for tonal or broadband, stationary or moving sources) but an
**inverted** microphone held a few mm above the same ground board is "very sensitive to changes in
the distance between the ground plate and the microphone diaphragm" (7 vs 4 vs 9.6 mm move the
whole high-frequency response, Fig. 13, p. 9) and itself "disturbs the measurements above 10 kHz"
(p. 9); the plate's geometric centre is "not the optimum position" compared with the ICAO-specified
off-centre point r = 0.15 m (p. 8–9).

**Verbatim quotes:**
- "This introduces interference between the direct wave and the reflected wave at the microphone
  position." (p. 3)
- "The interference of the direct wave and the reflected wave at the microphone position is like a
  comb filter, with the first minimum at the frequency where the microphone height 1.2 m equals ¼
  of the wavelength: f₀ = c/(4∗l) ≈ 71.4 Hz" ... "And the first maximum at f₁ = c/(2∗l) ≈ 143 Hz"
  (p. 3)
- "the frequencies coincident with the comb-filter minima are reduced by more than 20 dB, and the
  frequencies coincident with the comb-filter maxima are amplified by 6 dB." (p. 4)
- "the overall sound pressure level measured at 1.2 m height will be 3 dB higher than the
  corresponding level measured in a full free field as for example inside an anechoic chamber"
  (p. 4)
- "In practice it may be possible to correct the data for the comb-filtering effect as long as the
  source signal is broadband noise. However, if the source signal contains pure tone components,
  it will not be possible to do this correction." (p. 5)
- "The hover situation, with the sound source directly above the microphone position, is the worst
  as far as interference between the direct and reflected wave." (p. 6)
- "very sensitive to changes in the distance between the ground plate and the microphone
  diaphragm" (p. 9); "disturbs the measurements above 10 kHz" (p. 9)
- Conclusions: "the overall level of a broadband noise source can be obtained ... but in general the
  level obtained with this method will be 3 dB higher than the free-field condition" (pole mic);
  "if the microphone, instead of mounted at a certain height, is flush mounted with a fully
  reflecting ground, both broadband noise sources and pure tone sources can be measured, but with a
  6 dB higher level than for the free-field situation." (p. 10–11)

**Comparison with earlier notes** (`papers/chamber-problems/EXTRACTS-local.md`): agrees on every
substantive number and quote. One page-attribution correction: the earlier note cites the "hover
... is the worst" sentence as "(Fig. 9, p. 7)"; in the fresh extraction that sentence is on **p. 6**
(Figure 9 itself, the elevation-angle comb-shift plot, is on p. 7 — the earlier note conflated the
two). The earlier note already transcribed the formula variable as "l", matching the fresh dump;
what is new here is the visual confirmation that this is genuinely how the source PDF is typeset,
not an extraction artefact.

---

## 2. Friot, E. & Gintz, A. (2009) — *Estimation and global control of noise reflections*

**File:** `papers/chamber-problems/Friot-Gintz_2009_arXiv_estimation-global-control-noise-reflections.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/Friot-Gintz_2009_arXiv.txt`)
**Venue:** arXiv:0911.4639 (CNRS Laboratoire de Mécanique et d'Acoustique). No printed page
numbers in the source — PDF page given.
**Evidence level:** conference-style preprint.

**What it says (Q5):** Active-control method to estimate and cancel scattered/reflected sound in
an anechoic room, using "scattering filters" derived from a Kirchhoff/Green's-function integral
representation of scattered pressure (Eq. 1–3). For **identifying** the scattering filters (i.e.
separating the direct and reflected/scattered field to generate training data) the authors tried
**four** distinct approaches and report on each:
1. **Time windowing** — tried and abandoned: "methods involving windowing of time responses have
   failed, mainly because at low frequency echoes from a scattering body are very difficult to
   separate from actuator responses" (PDF p. 3).
2. **Physically removing the scattering body** and taking the pressure difference — works, but
   "removing the scattering body from the set of sensors and actuators is not always feasible; it
   cannot be done in the case of an anechoic room where active control is intended to compensate
   for the wall reflections" (PDF p. 3).
3. **Dipole null-plane method** — placing a dipole source so its null plane coincides with the
   error microphone isolates the scattered field directly; "the scattering filters could be well
   identified in the case of nearly rigid walls" but "the inversion process proved to be too
   ill-conditioned in the case of absorbing walls" because the null-plane pressure became too low
   (PDF p. 8).
4. **The paper's own proposed method** — invert a linear scattering-filter model from
   measurements with the primary source off and secondary (wall-mounted) sources on; "an accurate
   calibration of the detection microphones is not required" (PDF p. 9). Achieved "in average a
   10dB reduction of the scattered pressure" at 280 Hz in a 3-D experiment (PDF p. 5–6). Roughly 3
   transducers per wavelength are needed for global control, i.e. ~100 microphones and loudspeakers
   to cover 100 Hz in the LMA's 10 × 7 × 6 m anechoic room (PDF p. 6). "Usual rooms do not allow
   anechoic measurements below 50Hz" (PDF p. 6).

**Verbatim quotes:**
- "methods involving windowing of time responses have failed, mainly because at low frequency
  echoes from a scattering body are very difficult to separate from actuator responses." (PDF p. 3)
- "the inversion process proved to be to ill-conditioned in the case of absorbing walls." [sic,
  "to" for "too" in source] (PDF p. 8)
- "Indeed, usual rooms do not allow anechoic measurements below 50Hz whereas such measurements
  would be desirable for many industrial noise sources or for validation of acoustic theoretical
  models." (PDF p. 6)

**Comparison with earlier notes** (`papers/chamber-problems/EXTRACTS-downloaded.md`): agrees in
full; the earlier note cited section numbers (§2.B, §4) without page numbers, which this pass adds.
No discrepancies.

---

## 3. Cunefare, K. A. et al. (2003) — *Anechoic chamber qualification: Traverse method, inverse
square law analysis method, and nature of test signal*

**File:** `papers/anechoic-simulation/Cunefare_2003_JASA_chamber-qualification-traverse-fit-signal.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/Cunefare_2003_JASA.txt`)
**Venue:** J. Acoust. Soc. Am. 113(2), 881–892, 2003. Page numbers below are the printed JASA
pagination (881–892), confirmed by a page-footer/number map built from the extraction.
**Evidence level:** peer-reviewed journal.

**What it says (Q2, Q3, Q4):**

*Tolerance table (Q2)*, Table I, verbatim, p. 882 — "Maximum allowable difference in anechoic
rooms between measured and theoretical free-field levels per ISO 3745 and ANSI S12.35":

| One-third octave band centre frequency (Hz) | Allowable difference (dB) |
|---|---|
| < 630 | ± 1.5 |
| 800 to 5000 | ± 1.0 |
| > 6300 | ± 1.5 |

*Frequency averaging vs. tones (Q3)*: Abstract — broadband noise "is demonstrated to be a marginal
indicator of chamber performance" compared with pure tone traverses over the same span (p. 881).
On the SAME physical traverses, analysed both ways: pure-tone deviations from inverse-square law
"vary significantly" and are "due to interference between the direct and reflected components of
the wave field" (p. 889), while "the deviations observed using broadband noise are unremarkable.
These results support the conclusion that discrete samples at just about any spacing would seem to
be suitable for broadband noise qualification" (p. 890). Table IX (percentage of traverse samples
exceeding tolerance; column order for "Fixed" vs "Optimal" reference method cross-checked against
`pdftotext -layout` for this one table only, since plain-mode strips the column headers apart from
their numbers — the printed values are identical either way, only the header-to-column mapping
needed the layout pass): at 80 Hz into the lower-northeast corner, pure-tone traverses exceed
tolerance in **56 %** of sample points under the fixed-reference method vs **13 %** under the
optimal-reference method, while noise traverses at the same frequency and location are **54 %→10 %**
— broadband is somewhat better, but still far from "unremarkable"; contrast the higher frequencies,
e.g. 1000 Hz LNE, noise is 0 %→0 % while tone is 16 %→10 %.

*Spatial sampling to resolve (not average away) the interference pattern (Q4)*: "the deviation from
inverse square law performance ... exhibit[s] a variation consistent with an interference pattern"
(p. 891, §F). Estimating the average spatial separation between zero crossings of the deviation
curve (Table XI) gives, across 80 Hz–10 kHz, spacings from 29.2 % of a wavelength (1–2 kHz) to
40.8 % (80 Hz) — i.e. roughly a third of a wavelength, not a half. Applying a Nyquist argument to
that measured spatial period: "the minimum spatial sampling should be at least twice the minimum
spatial scale of interest ... this would imply a minimum spatial resolution (distance between
samples) of 15% of a wavelength at the frequency of interest" (p. 892). The cost of NOT doing this:
"for the 4-kHz traverse ..., the 1-ft [≈0.3 m] spacing discrete traverse would indicate no
performance issues with the chamber over the entire traverse, while the continuous traverse
identifies clear violations of the tolerance limits within 1.5 m of the source" (p. 889) — i.e. a
sampling interval far coarser than the interference period can hide a real, large tolerance
violation entirely, rather than averaging it into a smaller residual error.

**Verbatim quotes:**
- "The current practice of using widely space[d] discrete sampling along a traverse is shown to
  inadequately sample the complexity of the sound field extant with pure tone traverses, but is
  suitable for broadband traverses. ... the use of broadband noise as the test signal, as compared
  to pure tone traverses over the same span, is demonstrated to be a marginal indicator of chamber
  performance." (Abstract, p. 881)
- "As the deviation is due to interference between the direct and reflected components of the wave
  field, the spatial variation is expected to occur on length scales comparable to a fraction of a
  wavelength" (p. 889)
- "In contrast to the results obtained with the pure tone excitations ..., the deviations observed
  using broadband noise are unremarkable. These results support the conclusion that discrete
  samples at just about any spacing would seem to be suitable for broadband noise qualification."
  (p. 890)
- "for the 4-kHz traverse in Fig. 12, the 1-ft spacing discrete traverse would indicate no
  performance issues with the chamber over the entire traverse, while the continuous traverse
  identifies clear violations of the tolerance limits within 1.5 m of the source." (p. 889)
- "the minimum spatial resolution (distance between samples) of 15% of a wavelength at the
  frequency of interest." (p. 892)

**Comparison with earlier notes** (`papers/anechoic-simulation/VERIFICATION-2026-09-07.md`, card 2):
fully confirmed — "Table IX (p. 891): 80 Hz LNE tone 56 % → 13 % out of tolerance" and the exact
abstract wording both check out against the fresh dump and the `-layout` cross-check. No
discrepancies found.

---

## 4. Nash, A. (2019) — *Qualification of an anechoic chamber*

**File:** `papers/anechoic-simulation/Nash_2019_ICA_qualification-of-an-anechoic-chamber.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/Nash_2019_ICA.txt`)
**Venue:** Proc. 23rd ICA, Aachen, pp. 1343–1349, 2019.
**Evidence level:** peer-reviewed conference proceedings.

**What it says (Q2, Q3):** A 51 m³ IAC chamber, project-specified to ISO 3745 Annex A with a
**pure-tone-only** signal requirement ("Broadband noise, such as pink noise or white noise, is not
allowed", p. 1345). Same five traverses measured with (a) a supplemental broadband pink-noise
signal and (b) the required 12/13-tone clusters. Tolerance as paraphrased from the project spec/ISO
3745: "For frequencies between 800 and 5000 hertz, the allowable deviations are plus or minus one
decibel. Below 800 hertz and above 5000 hertz, the allowable deviations are relaxed to plus or
minus 1.5 decibels" (p. 1344) — note this simplifies away the 630/6300 Hz inner breakpoints that
Cunefare's and Winker & Stahnke's verbatim ISO 3745 tables give (both papers cite the identical
630/800–5000/6300 breakpoints; Nash's own account only distinguishes 800 Hz and 5000 Hz). On the
broadband traverse, 2 kHz gives a near-ideal fit (slope −19.8 dB/decade of distance ratio, R² = 0.9,
against the ideal −20); 4 and 6.3 kHz bands are "too shallow" (−16.2 to −18.4 dB/decade, R² = 0.8)
(p. 1347). On the exact same traverse with discrete tones instead: "Compared to bands of noise, the
use of discrete tones is more revealing of residual acoustical reflections arising from the walls,
floor, and ceiling surfaces. It is now quite obvious that the acoustical environment in the chamber
is not behaving like a free field" (p. 1348). The 2056 Hz tone gives a slope of −26.4 dB/decade
(R² = 0.3) — "a value that is physically impossible. The severe notch in the draw-away for the
2056-Hz tone suggests an acoustical cancellation occurring between the arriving wave front and a
strong reflection from a nearby surface" (p. 1348). Low-frequency tones (125, 257, 325, 824 Hz)
show high R² (0.7–1.0) that look like a good inverse-square fit, but "this appearance is deceiving
since the 25-millimeter spatial sampling interval is only a small fraction of a wavelength" (p.
1348). Verdict: "The chamber could satisfy the ISO tolerances when using random noise but failed to
qualify when using pure tones" (Abstract, p. 1343); "In short, the chamber is absorptive but not
anechoic" (p. 1349).

**Verbatim quotes:** as above; also "For an ideal anechoic chamber, the draw-away characteristic
should appear as a straight line ... y = -20x + intercept" and "For a distance ratio of 1.5, an
ideal free field should exhibit a reduction in sound pressure of precisely 3.522 decibels
(equivalent to 6.0206 decibels per doubling of distance)" (p. 1347–1348).

**Comparison with earlier notes** (`papers/anechoic-simulation/MATRIX-3W.md`, line 19):
**discrepancy found.** The earlier note attributes the "Compared to bands of noise, the use of
discrete tones is more revealing ..." quote, the "physically impossible" quote, and the "25-mm
spatial sampling interval is only a small fraction of a wavelength" quote all to **"§7, p. 1347"**.
Re-checked directly against `pdftotext -q -f 6 -l 6` (isolating exactly one PDF page) and its
footer: **all three of those sentences are on printed p. 1348**, one page later than the earlier
note says. p. 1347 contains only the pink-noise Figure 5 discussion (the 2 kHz / 4 kHz / 8 kHz
one-third-octave fits) and the definition of the ideal −20 dB/decade line; the tone-vs-noise
comparison and the 2056 Hz "physically impossible" discussion begin at the top of the next page.
This is a page-citation error in the earlier note, not a wrong quote — the quoted text itself is
verbatim-correct.

---

## 5. Winker, D. & Stahnke, B. (2016) — *The influences of changes in international standards on
performance qualification and design of anechoic and hemi-anechoic chambers*

**File:** `papers/chamber-problems/Winker-Stahnke_2016_InterNoise_ISO3745-ISO26101-chamber-qualification.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/Winker-Stahnke_2016_InterNoise.txt`)
**Venue:** Inter-Noise 2016, Hamburg. Page numbers are the paper's own self-contained pagination
(1–8, printed at the foot of each page); no separate proceedings page range is printed in the text.
**Evidence level:** peer-reviewed conference paper; authors are ETS-Lindgren (chamber manufacturer)
staff — flagged as vendor-adjacent, but content is a data-backed standards critique, not sales copy.

**What it says (Q2, Q3, Q4):**

*Tolerance table (Q2)*, their Table 1, verbatim, p. 2:

| Type of test room | 1/3-oct band (Hz) | Allowable deviation (dB) |
|---|---|---|
| Anechoic (free-field) | ≤630 | ±1.5 |
| | 800 to 5000 | ±1.0 |
| | ≥6300 | ±1.5 |
| Hemi-anechoic (hemi-free-field) | ≤630 | ±2.5 |
| | 800 to 5000 | ±2.0 |
| | ≥6300 | ±3.0 |

Identical anechoic-row values to Cunefare's Table I (2003) — the two papers, 13 years and one ISO
3745 revision apart, agree exactly.

*ISO 3745's free acoustic-centre offset can mask a real defect (Q1/Q2 context)*: "By using this
fitting method, a chamber can fully comply with ISO 3745 at certain frequencies while not
exhibiting free-field performance at those frequencies" (p. 3) — the standard only requires the
fitted offset r₀ to "should" (not "shall") sit within 200 mm of the true source, an ambiguity the
authors say can be exploited.

*Frequency averaging vs. tones (Q3)*: high-frequency (>10 kHz) traverse failures from
measurement-rig reflections are "counter-intuitive for uniform chambers"; "**This situation occurs
during pure tone qualifications and is not present in broadband qualifications due to signal
averaging** and is especially pronounced in frequencies above 10 kHz" (p. 7). "When using the ISO
26101 curve fit method, it is often impossible to fit the high frequency data" (p. 8).

*The λ/2 traverse-length rule (Q4)*: "ISO 26101 requires the traverse path distance to extend out
to one-half wavelength of the lowest frequency of interest in order to qualify the chamber" (p. 4),
a requirement the authors argue is unnecessary and drives up chamber size without improving the
qualification's power to detect a real problem. Case study, small chamber (3.35 × 3.05 × 2.74 m):
at 160 Hz the ISO 26101 curve-fit shows deviation from inverse square law "clearly seen before the
half-wavelength distance of 1.1 m" (p. 5); at 200 Hz the chamber "follows inverse square law to a
distance of 1 m as designed, but the current requirements of ISO 26101 invalidate this claim
because the required traverse distance could not be performed" — geometry, not acoustics, caps the
chamber's ISO-26101-qualified range at 214 Hz instead of the true 200 Hz (p. 5–6). General claim:
"The range under which the chamber follows inverse square law and where it begins to deviate from
inverse square law is obvious without employing either curve fit methodology. This performance is
evident well before the one-half wavelength traverse distance required by ISO 26101" (p. 5).
ISO 26101 spatial-sampling requirement: "at least one-tenth wavelength measurement spacing at
frequencies below 1 kHz and 25 mm at frequencies above 1 kHz. ISO 3745 allows measurement spacing
up to 100 mm" (p. 4).

**Comparison with earlier notes** (`papers/chamber-problems/EXTRACTS-downloaded.md`): fully
confirmed, including page numbers, for every quote checked. No discrepancies.

---

## 6. Simmons, D., Jobling, B. & Payne, R. (2004) — *Acoustic parameters and uncertainties
associated with determining sound power level in hemi-anechoic rooms*

**File:** `papers/chamber-problems/Simmons-Jobling-Payne_2004_NPL-DQL-AC007_hemi-anechoic-sound-power-uncertainties.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/Simmons-Jobling-Payne_2004_NPL-DQL-AC007.txt`)
**Venue:** NPL Report DQL-AC 007, August 2004. Printed page numbers confirmed by a footer map
(offset PDF page − 6 = printed page, verified at 20 sampled points across the 66-page PDF).
**Evidence level:** national-metrology-institute report.

**What it says (Q2, Q3, Q4):** A hemi-anechoic room was progressively degraded by removing
absorbent wedges in steps (0 to 2626 of the room's wedges), and re-tested at each step with both
pure tones (125 Hz–10 kHz) and broadband noise from a cavity point source, plus a Brüel & Kjær 4204
Reference Sound Source (RSS).

*Tolerance table (Q2)*, their Table 2, verbatim, p. 15 — "ISO 3745 inverse square test tolerance
limits" (hemi-anechoic): ≤630 Hz → 2.5 dB; 800–5000 Hz → 2.0 dB; ≥6300 Hz → 3.0 dB. Identical to
Winker & Stahnke's hemi-anechoic row.

*K2 method (Q2)*: "The difference between the sound power level determined for the RSS in-situ in
each of the degraded room states and the sound power level of the RSS determined in true
hemi-anechoic conditions provides the values of environmental correction K2. The correction ... is
given by: K2 = L*W − LWr" where LWr is the RSS's hemi-anechoic sound power and L*W its uncorrected
in-situ value over the same ISO-3744 10-microphone, 1.5 m hemispherical surface (p. 16–17).

*Tone vs. broadband (Q3), quantified*: Table 4 (broadband) shows maximum deviation from the
inverse-square best-fit line reaching **3.7 dB** (at 1008 wedges removed, 125 Hz); Table 5 (pure
tones), same rooms, reaches **14.3 dB** (at 1450 wedges removed, 4000 Hz) (p. 25). Resulting
measurement uncertainty: "an average standard uncertainty of 0.7 dB for the ISO 3745:1977
procedures but this increased to 4 dB when considering the current ISO 3745:2003 standard" for
rooms qualified with **broadband** noise, vs. "the average standard uncertainty was the same for
both standards at a much lower value of 0.02 dB" for rooms qualified with **tones** (p. 52).
Mechanism, stated explicitly: "**It was shown that broadband noise deviated less than pure tones,
which could be attributed to averaging of the interference between the limits of the frequency
band being analysed**" (p. 51). Consequently: "it is concluded that the procedure for qualifying
rooms using the broad-band noise methodology is **over-tolerant of poor acoustic room
performance**, especially that specified in ISO 3745:2003, and can lead to unacceptably high levels
of measurement uncertainty" (p. 49). K2 correction efficacy: applying the measured K2 to the drill
and box-source machines "for the ISO 3745:2003 procedure reduc[es] from 6.4 dB and 7.3 dB to 0.8 dB
and 0.1 dB" (p. 49) — i.e. the correction removes most, not all, of the room-induced error, and
does so far more effectively than simply trusting the ISO broadband pass/fail criterion. (The
report gives two slightly different tellings of the K2A-vs-wedges-removed progression: §4.2.2 says
"K2A ... increased from 0.4 dB to 7.2 dB" following "the halfway stage" of wedge removal (p. 32),
while §5's Summary says "K2A increased from 1.3 dB to 7.2 dB" for the same halfway point (p. 51) —
both are consistent with the underlying Table 8 data (p. 31: A-weighted K2 = 0.4, 1.3, 3.7, 7.2 dB
at successive later room states), they just anchor "before halfway" at different room states; not
a citation error, just an internal inconsistency in how the source narrates its own table.)

*Directivity/tonal sources not addressed for K2 itself*: nothing in this report ties K2 to source
directivity; K2 is defined and measured purely as a surface-averaged sound-power correction.

*Spatial averaging (Q4, partial)*: when setting the reference tone/noise level for the cavity
source, "the amplitude at each frequency for pure tone signals was set by measuring the signal
level in the hemi-anechoic room prior to degradation, with microphones positioned at four heights
on a hemispherical measurement surface of radius 1.5 m. The measured sound pressure levels were
averaged **in order to reduce cancellation effects from the ground plane**" (p. 8) — a real,
explicit example of deliberate multi-position spatial averaging to suppress a ground-reflection
interference pattern, though for calibrating the *source* signal rather than for measuring a
device under test, and with no stated residual-error figure for the averaging step itself.

**Verbatim quotes:** all given inline above.

**Comparison with earlier notes** (`papers/chamber-problems/MATRIX-3W.md`, line 17): fully
confirmed — "Tone deviations to 14.3 dB while broadband ≤ 3.7 dB ... K₂ correction 6.4→0.8 dB;
'over-tolerant of poor acoustic room performance'" all check out verbatim, now with exact page
numbers and the specific room-state/frequency each figure belongs to added.

---

## 7. Payne, R. C. & Simmons, D. J. (1996) — NPL Report CIRA(EXT) 009 (environmental correction K2)

**File:** `papers/anechoic-simulation/Payne-Simmons_1996_NPL-CIRA009_environmental-correction-K2.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/Payne-Simmons_1996_NPL-CIRA009.txt`)
**Venue:** NPL Report CIRA(EXT) 009, April 1996. Printed pagination confirmed (offset PDF page − 4
= printed page for pages 5 onward; pages 1–4 are unnumbered title/abstract/contents front matter).
The scanned title page is OCR-garbled (matches the bibliography's note); the body text is clean.
**Evidence level:** national-metrology-institute report.

**What it says (Q2):** Predates and is the methodological basis for the 2004 NPL report above.
Measures K2A in five real rooms (hemi-anechoic to semi-reverberant) by all four methods the ISO
3740/11200 series then permitted:
1. **Absolute comparison** (reference sound source, B&K 4204, 90.9 dB ± 0.2 dB re 1 pW): K2 = Lwr − Lw
   (Eq. 2, p. 3).
2. **Room absorption / reverberation time**: K2 = 10 log₁₀(1 + 4S/A) (Eq. 3, p. 3), A from a
   measured reverberation time (not applicable to hemi-anechoic rooms, p. 5).
3. **Two-surface method**: compare Lp on two similar, nested measurement surfaces S and S₂ with
   S₂/S "at least 2, and preferably greater than 4"; M = 10^(0.1(Lp1−Lp2)), S/A = (1−M·S/S₂)/(4(M−1))
   (Eq. 6–7, p. 5).
4. **Estimated room absorption**: A read off a qualitative table of room descriptions in the ISO
   standards.

Framing the stakes: "Taken together, these standards permit K2 to range from 0 dB to 7 dB. Since K2
is added to measured noise levels, it is clear that it must be determined accurately" (p. 1).
Conclusion (Abstract): "It is concluded that the absolute method using a reference sound source is
the only method that **will** consistently provide an accurate assessment of K2A. The method
involving measurement of reverberation time generally over-estimates K2A and will result in values
of sound power level that are too low ... The two surface method generally under-estimates K2A and
will result in values of sound power level which are too high ... The estimated room absorption
method provides only a range of possible values of K2A." Restated in §6 Conclusions with slightly
different wording (present tense, no "will"): "It is concluded that the absolute method using a
reference sound source is the only method that consistently provides an accurate assessment of
K2A" (p. 23) — **both phrasings genuinely appear in the source**, once in the Abstract and once in
the Conclusions; not a misquote in either case. Quantified errors of the other methods, two example
rooms: reverberation-time method over-predicts K2A by a mean of 0.7 dB (Room A) and 1.3 dB (Room B);
two-surface method under-predicts by a mean of roughly −0.4 dB (Room A) to −1.3/−2.2 dB (Room B,
worse "where the second surface was close to various room obstacles") (p. 17–18).

**Directivity/tonal sources**: not addressed — the whole report is A-weighted broadband
machinery-noise sound-power work; no tonal or directivity content, confirming a genuine gap in this
part of the K2 literature.

**Verbatim quotes:** as above.

**Comparison with earlier notes** (`papers/anechoic-simulation/MATRIX-3W.md`, "Payne & Simmons
1996" entry): confirmed on every number checked (Room B mean +1.3 dB reverberation over-prediction,
−2.2 dB two-surface under-prediction, the §6/p.23 "consistently provides" quote verbatim). One
addition, not a conflict: the earlier note only quotes the p. 23 (Conclusions) wording; the Abstract
states the identical conclusion with "will consistently provide" instead of "consistently
provides" — worth knowing if this sentence is ever re-quoted from a different page.

---

## 8. ISO 26101-1:2021 (iTeh standard preview) — *Qualification of free-field environments*

**File:** `papers/anechoic-simulation/ISO-26101-1_2021_standard-preview_free-field-qualification.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/ISO-26101-1_2021.txt`)
**Evidence level:** standard (preview only — Foreword through clause 5.1.5.1.2; the preview stops
mid-formula, before reaching Annex A, which is where the actual numeric tolerance table and
traverse-layout requirements live. **The tolerance table itself is therefore not verbatim in this
held preview** — see items 3, 5 and 6 above for the table as quoted, with page numbers, by three
independent papers that do reproduce it from the standard.)

**What the accessible part says (Q1, Q2, Q4):**
- "The free sound field performance is evaluated by quantifying the contributions of both the
  direct and the reflected components of acoustic energy" (§5.1.1).
- Discrete-frequency qualification signal-purity rule: "If pure tones or multiple pure tones are
  used for discrete-frequency qualification, the measured signal after any filtering shall not
  contain energy at frequencies not being characterized that are within 15 dB of the frequencies
  being characterized" (§5.1.4.2).
- Continuous-traverse method is explicitly sanctioned by the standard itself (matching what
  Cunefare's 2003 paper implemented): "Alternatively, for discrete-frequency measurements using
  pure tone signals, the microphone may be moved slowly and continuously along the traverse and the
  sound pressure levels recorded" (§5.1.4.3, preceding page).
- Care notes: "to ensure that the sound pressure levels are more than 6 dB, and preferably more
  than 15 dB, above the background noise levels" and "in positioning the monitor microphone to
  avoid acoustic interference with the traversing mechanism affecting the results" (§5.1.2.2).

**Comparison with earlier notes**: no dedicated extracts entry existed for this preview beyond the
one-line bibliography description ("Foreword–5.1.5.1.2 only"); confirmed accurate — that is indeed
exactly where the preview stops.

---

## 9. ISO 26101-2:2024 (iTeh standard preview) — *Determination of the environmental correction*

**File:** `papers/reflection-localization/ISO-26101-2_2024_standard-preview_environmental-correction.pdf`
(re-extracted: `papers/arc-validation/refetch-txt/ISO-26101-2_2024.txt`)
**Evidence level:** standard (preview only — front matter through §5.1; Annex A, which per §4.1
holds "Information on the uncertainty of the environmental correction," is not in the preview).

**What it says (Q2):** Current (2024) statement of the K2 methodology, structurally the same four
families as the 1996 NPL report, 28 years later: **(4.2) Absolute comparison test** with a
reference sound source — "the preferred procedure for qualifying a test environment according to
ISO 3744 ... This method is expected to yield the most accurate results in typical industrial
environments." **(4.3) Methods based on room absorption** (reverberation time / secondary
measurement surface [= the two-surface method] / reference sound source) — "can be less accurate
than the absolute comparison test." **(4.4) Inverse-square-law qualification of parallelepiped and
cylindrical measurement surfaces** — for hemi-anechoic rooms only, "the preferred method to qualify
a hemi-anechoic room and represents the most accurate method"; note: "In hemi-anechoic rooms, the
other qualification procedures can yield unreliable results." **(4.5) Approximate method based on
an estimation of the equivalent absorption area** — "considered to be the least accurate method."
General caveat: "In some industrial buildings, which are of low height and have reflecting
surfaces, the sound propagation can be distorted. In these conditions, the qualification procedures
according to Clause 6 and Clause 8 might not be applicable" (§4, unnumbered note).

**Directivity/tonal sources**: K2 "is a function of both the reflected sound from the test
environment and the shape and size of the measurement surface" (§1 Scope) — no mention of source
directivity or tonal vs. broadband content anywhere in the accessible clauses.

**Comparison with earlier notes** (`papers/reflection-localization/MATRIX-3W.md`, ISO 26101-2
entry): fully confirmed, verbatim, including the "most accurate method" and "the other
qualification procedures can yield unreliable results" quotes and their clause/page attributions.
No discrepancies.

---

## 10. Pao, S. P., Wenzel, A. R. & Oncley, P. B. (1978) — *Prediction of Ground Effects on Aircraft
Noise* [NEW — retrieved this session]

**File:** `papers/arc-validation/Pao-Wenzel-Oncley_1978_NASA-TP1104_ground-effects-aircraft-noise.pdf`
(text: `papers/arc-validation/txt/Pao-Wenzel-Oncley_1978_NASA-TP1104_ground-effects-aircraft-noise.txt`)
**Venue:** **NASA Technical Paper 1104** (NASA-TP-1104, report no. L-11833), 1978. **Identity
correction**: the thread brief named this "NASA RP-1004"; the document itself (confirmed from its
own title page and the NTRS citation metadata) is designated **NASA TP-1104**, not RP-1004 — same
paper (same title/authors/1978 date), the series letters and last two digits were transposed in the
brief. Retrieved via NTRS: `https://ntrs.nasa.gov/api/citations/19780009880/downloads/19780009880.pdf`.
Page numbers below are the report's own printed pagination (confirmed via footer numbers visible in
the OCR text; OCR quality is poor — character spacing is irregular throughout, e.g. "I n" for "In" —
quotes below are reproduced with spacing normalised where it does not change any word, and flagged
where a number could be misread).
**Evidence level:** NASA technical report (peer-reviewed-adjacent government report).

**What it says — this is the single most useful new source for Q1 and Q5:**

*General formula (Q1)*: the point-source-over-an-impedance-plane wave field (their Eq. 3, p. 16):

    p = -(G/r1) { e^(ikr1) + [Γ + (1−Γ)F(σ)] e^(ikr2)/r2 · r1 }   (their notation, condensed)

where Γ = (cos θ − V)/(cos θ + V) is the plane-wave reflection coefficient (their Eq. 4, p. 16), r1
and r2 are the direct- and reflected-wave path lengths, V is the (complex) ground admittance and
F(σ) is a spherical-wave correction ("ground and surface wave") factor. The first term is the
direct wave, the second the reflected wave modified by Γ and F. **This is the general form of the
"direct + reflected wave" model the thread brief asked for**; the compact scalar dB formula
(peaks/dips at integer/half-integer wavelength path differences) is not stated by the source in
that exact algebraic shorthand — it **is** the high-frequency, real/hard-surface limit of this
equation (Γ real, F → 1), which I derive here rather than quote: level relative to free field
= 20·log₁₀|1 + Γ·(r1/r2)·e^(ikΔr)|, giving a maximum of 20·log₁₀(1 + Γ·r1/r2) at path difference
Δr = nλ and a minimum of 20·log₁₀|1 − Γ·r1/r2| at Δr = (n+½)λ. That this reduction is right is
corroborated qualitatively by the source's own historical review, same page range: citing Ingard,
"the excess attenuation resulting from destructive interference between the direct and reflected
sound paths was determined mainly by the impedance of the ground surface. The phase shift of ground
reflection at near-grazing incidence can easily exceed 160° ... Maximum destructive interference can
be reached by an additional geometrical path difference of 0.05 wavelength such that the total
mismatch between the direct and the reflected sound waves is half a wavelength at the point of
measurement" (p. 5).

*Static engine/propeller test-stand correction — directly answers Q1's "any NASA TM/TP on
ground-reflection corrections for static engine/propeller tests"*: Summary states the paper's
purpose explicitly includes "correcting static test-stand data to free-field conditions" (p. 1).
Section "Standard Practice in Correcting for Ground Effects" (p. 13–15) is a direct survey of
what test facilities actually do:
- **Flush-mounted microphones**: "now being extensively used for outdoor acoustic measurements,
  especially for engine static tests." Common practice: "combine the low-frequency data from
  flush-mounted microphones with high-frequency data from the raised microphones, thereby reducing
  the flush-mounted-microphone data by **6 dB** and the raised-microphone data by about **2 dB**
  to obtain a composite free-field sound pressure level spectrum" (p. 13) — the same 6 dB
  pressure-doubling figure Rasmussen & Winberg (2022) and Lamancusa's course notes (below) give
  independently, 44 years apart.
- **Raised microphones**: push the first interference dip below the band of interest by geometry —
  worked numeric example: "a separation distance of 20 m combined with source and microphone
  heights at 6 m will bring the first interference dip in the spectrum to about 50 Hz" (p. 13).
  Flagged as "less accurate than the flush-mounted-microphone concept" and "susceptible to errors
  caused by environmental factors" (p. 13).
- **Gravel test pads**: many facilities use gravel instead of concrete; "the gravel-filled area is
  sometimes acoustically calibrated for ground effects" — a computer search locates "the frequency
  and magnitude of the first interference dip" then applies the calibrated correction to the whole
  spectrum (p. 14–15, "these methods are also found to be successful").
- **Manual/visual correction — and its explicit tone caveat (Q3)**: "Data which show prominent dips
  in lower frequency bands are frequently corrected by the trained eye and hand of the test
  engineer. This correction can be fairly successful for data obtained over hard surfaces if the
  test engineer understands the theoretical background ... **This procedure will obviously be
  incorrect in cases where a strong tone is present.** Therefore, the test engineer should also be
  familiar with the characteristics of the sound source so as to distinguish which frequency bands
  legitimately should contain interference corrections and which ones may include real tones"
  (p. 14). This is a 1978 NASA report making the identical point Rasmussen & Winberg make in 2022 and
  Simmons/Jobling/Payne make in 2004 (item 6): a ground-reflection dip can be smoothed/corrected only
  when it is known NOT to coincide with a genuine tone.
- **Analytic correction with known ground impedance**: validated against a real static jet-engine
  test — "Figure 5 shows a comparison between a one-third-octave band spectrum of a jet engine on
  static test as recorded over a gravel surface with a microphone 75 m away and as recorded from a
  balloon the same distance above the source ... Even with the rough impedance estimate, there is a
  very good agreement with the measured data" (p. 13–14, using Dickinson's impedance data for
  "broken tarmacadam").
- **Cepstral technique (Q5)**, attributed to "Miles et al. (ref. 45)": "For acoustic measurements at
  short range with the sound source and the microphone high above a hard surface, the maximums and
  minimums of the interference pattern occur at regular frequency intervals. Furthermore, the first
  interference dip often occurs at a very low frequency which lies below the range of practical
  interest so that it may be ignored. **A Fourier transformation of the logarithm of the spectrum
  results in a cepstral function in which interference maximums and minimums are represented as a
  single spike. The location of this spike is determined by the frequency span between two
  consecutive maximums or minimums. By removing this spike from the cepstral function and taking an
  inverse Fourier transformation, the result is a logarithm spectrum without ground effects.** Note
  that this technique is applicable only for acoustic measurements over a hard surface where the
  surface reflection does not introduce any significant phase shift into the acoustic signal"
  (p. 15). Reference 45, resolved from the paper's own reference list (p. 31): **Miles, Jeffrey H.;
  Stevens, Grady H.; Leininger, Gary G. "Application of Cepstral Techniques to Ground-Reflection
  Effects in Measured Acoustic Spectra." J. Acoust. Soc. America, vol. 61, no. 1, Jan. 1977,
  pp. 35–38.** This original paper is JASA/AIP — a known blocker — and was **not independently
  retrieved this session**; the description above is Pao et al.'s secondary account of it, not a
  direct quote of Miles et al. Two related Miles NASA TMs are also in the reference list and were
  not pursued this session: TM X-3179 (1975) and TM X-71696 (1975).
- **Analytic/iterative computer correction** (Miles, refs. 43–44, same author, different method):
  an iterative scheme that postulates a free-field spectrum, adds a modelled ground effect, compares
  to measured data via an error function, and adjusts; used at an asphalt-surfaced test area (20 m
  range, ~4 m source/mic height), "found to provide satisfactory results ... under such conditions"
  (multiple-source geometry) (p. 14).

**Verbatim quotes:** all given inline above, with page numbers.

**Comparison with earlier notes**: this paper was not previously held in the corpus — no
comparison applicable. First retrieval this session.

---

## 11. Lamancusa, J. S. (2009) — Penn State "Noise Control" course notes, Ch. 10 *Outdoor Sound
Propagation* [NEW — retrieved this session, as an open-access substitute for the blocked Embleton
1996 JASA tutorial]

**File:** `papers/arc-validation/Lamancusa_2009_PennState-CourseNotes_outdoor-sound-propagation.pdf`
(text: `papers/arc-validation/txt/Lamancusa_2009_PennState-CourseNotes_outdoor-sound-propagation.txt`)
**Source:** hosted openly at `angelofarina.it/Public/Acoustics-Course/Penn-State-Course/10_osp.pdf`
(Angelo Farina's course-materials mirror); confirmed from the PDF's own header ("NOISE CONTROL",
"J. S. Lamancusa, Penn State, 7/20/2009") on every page.
**Evidence level:** university teaching text, not peer-reviewed — the lowest tier used in this
extract, included only because (a) the actual Embleton (1996) JASA tutorial the thread brief named
is blocked (`pubs.aip.org`), and (b) this document's own account of the ground-reflection formula
is explicitly sourced to, and consistent with, the peer-reviewed review it cites (Piercy, Embleton
& Sutherland, 1977, JASA 61(6), 1403–1418 — itself JASA/AIP-blocked, not independently retrieved).
Page numbers below are the chapter's own printed numbering (10.1, 10.2, ...).

**What it says (Q1):** "Depending on their relative phases and amplitudes, [the direct and
reflected waves] may constructively add or destructively interfere. In the limit, for both source
and receiver near the ground and perfect reflection and no atmospheric turbulence (coherent
addition), the sound level at the receiver will be increased by 6 dB (an excess attenuation of
–6dB). Effectively, the receiver sees two sources, the actual source, and a reflected or 'image'
source and the sound pressure is doubled" (p. 10.8) — matching the +6 dB flush-mount/pressure-doubling
figure independently given by Rasmussen & Winberg (2022) and Pao, Wenzel & Oncley (1978, item 10).
General governing equation (their Eq. 13, p. 10.9, same Chien–Soroka/Thomasson theoretical lineage
as Pao et al.'s Eq. 3): p/p₀ = (1/rd)e^(ikrd) + (Rp/rr)e^(ikrr) + (1−Rp)·F/rr·e^(ikrr), "the first
term ... is the direct wave, the second term describes a reflected wave, after its amplitude and
phase have been modified by the plane wave reflection coefficient. The third term accounts for the
difference between the reflection of a plane wave, and that of the actual case of a spherical
wave ... called the ground and surface wave" (p. 10.9), with Rp = (sin θ − Z_air/Z_ground)/(sin θ +
Z_air/Z_ground) — an equivalent formulation to Pao et al.'s Γ. Notes explicitly that "coherent
addition of the direct and reflected wave is assumed" in deriving this, and that real-atmosphere
turbulence smears the interference pattern, sometimes by "10 dB or more over a period of minutes"
(p. 10.10), citing Chessel (1977) and Daigle (1979).

**Verbatim quotes:** as above.

**Comparison with earlier notes**: not previously held; first retrieval this session.

---

## 12. ISO 3745:2012 (iTeh standard preview) [NEW — retrieved this session]

**File:** `papers/arc-validation/ISO-3745_2012_standard-preview_precision-methods-anechoic-rooms.pdf`
(text: `papers/arc-validation/txt/ISO-3745_2012_standard-preview_precision-methods-anechoic-rooms.txt`)
**Route:** `https://cdn.standards.iteh.ai/samples/45362/5080c9a729fb42b08f433df7ed8129f6/ISO-3745-2012.pdf`
**Evidence level:** standard (preview only, 15 pages of an much longer document). Confirmed from
its own title page: "ISO 3745, Third edition, 2012-03-15."

**What the accessible part says (Q2)**: this is the standard that Cunefare (2003), Nash (2019),
Winker & Stahnke (2016) and Simmons/Jobling/Payne (2004) all cite for the tolerance table quoted in
items 3, 4, 5, 6 above — but **the preview itself stops at clause 5.1 ("Test rooms")**, before
reaching **Annex A** (its own table of contents, read from the preview, confirms: "Annex A
(normative) General procedures for qualification of anechoic and hemi-anechoic rooms......... 29"),
which is where the numeric tolerance table actually lives in the standard's own text. This preview
therefore corroborates the STRUCTURE (Annex A = general qualification; Annex B = qualification for
specific sound-power test rooms; Annex C = A-weighting) but not the numbers themselves — for the
numbers as quoted verbatim from the standard, see the three independent secondary sources above,
which agree with each other exactly. Useful accessible content: the formal definitions of surface
time-averaged SPL (Eq. 4), sound power level (Eq. 6) and directivity index (Eq. 9), and clause 5.1's
framing: "Anechoic or hemi-anechoic rooms that are applicable for measurements in accordance with
this International Standard either satisfy: a) Annex A over the frequency range of interest, for
use in general purpose measurements; or b) Annex B ... for determination of sound power levels of
specific noise sources."

**Comparison with earlier notes**: not previously held; first retrieval this session.

---

## 13. Randall, R. B. (2013) — *A History of Cepstrum Analysis and its Application to Mechanical
Problems* [NEW — retrieved this session, and identity-corrected]

**File:** `papers/arc-validation/Randall_2013_Surveillance7_history-of-cepstrum-analysis.pdf`
(text: `papers/arc-validation/txt/Randall_2013_Surveillance7_history-of-cepstrum-analysis.txt`)
**Venue:** Surveillance 7 international conference, Oct. 2013 (confirmed from the PDF's own
metadata: `Subject: Surveillance 7, International Conference - Full Papers`, `CreationDate: Oct
2013`, `Author: Robert B Randall`).
**Retrieval note**: the thread brief asked for "Randall's 2017 history of cepstrum on ResearchGate/
Bath repository" — this is Randall, R. B. (2017), *A history of cepstrum analysis and its
application to mechanical problems*, Mech. Syst. Signal Process. 97, 3–19,
doi:10.1016/j.ymssp.2016.12.026. **That 2017 journal paper was not retrieved** — see
`RETRIEVAL-A.md`. What was retrieved is Randall's own **earlier, same-titled 2013 conference
paper**, a different, non-identical publication (the 2017 MSSP paper is its expanded journal
version). A copy of this 2013 paper already existed in `papers/arc-validation/` from an unrelated
earlier session, mis-named as if it were the 2017 target; it has been renamed to reflect its actual
identity (confirmed from its own front matter, per protocol) and re-extracted fresh into `txt/`.
**Evidence level:** peer-reviewed conference paper (cepstrum-history survey by a leading authority
on mechanical/vibration cepstrum applications; not itself about room acoustics — see below).

**What it says (Q5, background only — confirmed it does NOT address the thread's actual question):**
A search of the fresh extraction for "room", "reverberant" and "direct sound" returns **zero
hits** — this paper's survey of cepstrum applications covers seismology, speech analysis, gear and
bearing diagnostics, diesel-engine combustion-pressure extraction, and modal analysis of mechanical
structures, but **not architectural/room-acoustics reflection separation**. It is retained here
only for two general points that bear on Q5's framing of what a cepstrum is and why it separates
echoes:
- On the original 1963 paper's purpose: "The original application was to the detection of echoes in
  seismic signals, where it was shown to be greatly superior to the autocorrelation function,
  because it was insensitive to the colour of the signal" (p. 1).
- On liftering: "the word and concept of a 'lifter' (a filter in the cepstrum) was defined in the
  original paper" (p. 1) — the terminology the thread brief's "cepstral deconvolution" question
  presupposes.
- A mechanical-diagnostics analogue of echo removal (not a room reflection, but structurally the
  same idea Pao et al. describe in item 10): "the cepstrum of a signal with an inverted echo is
  entirely negative, so that its integral over quefrency becomes markedly more negative when such
  an inverted echo is in the analysed section of time record" — used to detect (not remove) a
  spalled-gear-tooth echo via a "moving cepstrum integral" (p. 8); separately, rotor-harmonic
  contamination in a helicopter vibration signal was "largely removed ... by using a comb lifter
  adjusted to the rahmonic spacing" (p. 15) — a lifter-based removal of a *periodic* interference
  pattern in quefrency, conceptually the same operation Pao et al.'s Miles-attributed technique
  performs on a *ground-reflection* comb (item 10), just applied to a different physical source of
  periodicity.
- Full citation for Bogert, Healy & Tukey (1963), taken from this paper's own reference list and
  useable to locate/order the original: "B.P. Bogert, M.J.R. Healy, and J.W. Tukey, *The Quefrency
  Alanysis of Time series for Echoes: Cepstrum, Pseudo-Autocovariance, Cross-Cepstrum, and Saphe
  Cracking*, in Proc. of the Symp. on Time Series Analysis, ed. M. Rosenblatt, Wiley, NY, (1963),
  pp. 209–243" (References [1], p. 15).

**Comparison with earlier notes**: not previously held under its correct identity (it was
mis-filed as the 2017 paper); no prior extracts existed for it under either identity. First proper
retrieval this session.

---

## Answers to the thread questions

**Q1 — direct + one reflected wave, level error vs. amplitude ratio and path difference:**
Retrieved sources give the physics at two levels. (a) *General, rigorous form*: Pao, Wenzel & Oncley
(1978, item 10, their Eq. 3–4) and, independently, Lamancusa's course notes (2009, item 11, their
Eq. 13, same Chien–Soroka/Thomasson theoretical family) both give p(receiver) = direct term
(1/r₁)e^(ikr₁) + reflected term modified by a plane-wave reflection coefficient Γ (or Rp) and, for
a spherical rather than plane incident wave, a further correction factor F(σ) ("ground and surface
wave"). (b) *Compact scalar dB form*: no retrieved source states the "20·log₁₀(1 ± R·r_d/r_r)"
shorthand in exactly that algebra; it is the real-reflection-coefficient, F→1 limit of (a), which I
derive rather than quote (item 10). What the retrieved sources DO state, verbatim, in that limit's
own numbers: Rasmussen & Winberg (2022, item 1) work the fully-idealised Γ=1 (perfectly hard ground)
case for a 1.2 m pole microphone under a hovering source — first dip at f₀ = c/(4h) ≈ 71.4 Hz, first
peak at f₁ = c/(2h) ≈ 143 Hz, 1/3-octave dip depth ">20 dB", peak height "+6 dB", overall level +3 dB
(pole) or +6 dB (flush-mounted, simple pressure doubling); the same +6 dB pressure-doubling figure is
given independently by Pao et al. (1978, item 10, p. 13: "reducing the flush-mounted-microphone data
by 6 dB") and by Lamancusa (2009, item 11, p. 10.8: "the sound level at the receiver will be
increased by 6 dB ... the sound pressure is doubled"). Pao et al. also give the qualitative
"dip/peak at odd/even half-wavelength path-difference" rule in words, citing Ingard: maximum
destructive interference occurs when "the total mismatch between the direct and the reflected sound
waves is half a wavelength at the point of measurement" (item 10, p. 5). Nash (2019, item 4) shows
a real (non-idealised) instance: a genuine strong single reflection collapsing a chamber traverse to
a "physically impossible" −26.4 dB/decade slope at one frequency (p. 1348).

**Q2 — standards and K2:** The ISO 3745/ISO 26101 tolerance table (anechoic ±1.5/±1.0/±1.5 dB below
630/800–5000/above 6300 Hz; hemi-anechoic ±2.5/±2.0/±3.0 dB in the same bands) is confirmed verbatim
and identically across three independent, peer-reviewed-or-report sources spanning 2003–2016
(Cunefare Table I, item 3; Winker & Stahnke Table 1, item 5; Simmons/Jobling/Payne Table 2, item 6);
the held iTeh previews of ISO 3745:2012 itself and of ISO 26101-1:2021 (items 8, 12) both stop before
reaching the annex that contains this table, so the table's ultimate source (the standard's own
Annex A) was not directly read this session — flagged. K2 is determined by one of four canonical
procedures, essentially unchanged from 1996 (Payne & Simmons, item 7) to 2024 (ISO 26101-2 preview,
item 9): absolute comparison with a reference sound source (K2 = Lwr − Lw), a room-absorption family
(reverberation time / two-surface / RSS-based estimate of equivalent absorption area), and — new in
26101-2 — an inverse-square-law qualification of the hemi-anechoic measurement surface itself. Both
the 1996 report and the 2024 standard agree the **absolute/reference-source method is the most
accurate** ("the only method that will consistently provide an accurate assessment of K2A", 1996,
item 7; "expected to yield the most accurate results in typical industrial environments", 2024,
item 9); the 1996 report quantifies the alternatives' errors (reverberation-time method
over-predicts by a mean of 0.7–1.3 dB across two rooms; two-surface method under-predicts by
−1.3 to −2.2 dB) and states "these standards permit K2 to range from 0 dB to 7 dB" (item 7, p. 1).
Simmons/Jobling/Payne (2004, item 6) show the correction, once measured, collapses a 6.4–7.3 dB
uncorrected room-induced level error down to a 0.1–0.8 dB residual. **Tonal sources**: none of the
K2-specific sources (items 7, 9) treat tones separately from broadband — K2 methodology itself is
signal-agnostic — but item 6 shows the *qualification framework K2 feeds into* is far less
protective for tones (14.3 dB max tone deviation vs. 3.7 dB broadband in the same rooms) and that
rooms passing on broadband can still be "clearly ... not hemi-anechoic" by the K2 measure itself
(item 6, p. 49). **Directivity**: not addressed by any retrieved K2 source — K2 and the ISO
tolerance table both correct/bound a surface- or point-averaged *level*, not the shape of a
directivity pattern; this appears to be a genuine gap in the retrieved literature, not merely an
omission in this thread's search.

**Q3 — frequency averaging hides interference; how wide must the band be:** Four independent
sources, spanning 1978–2016, state the same mechanism and, in three cases, quantify it. Most
explicit: Simmons, Jobling & Payne (2004, item 6, p. 51): "broadband noise deviated less than pure
tones, which could be attributed to **averaging of the interference between the limits of the
frequency band being analysed**" — quantified as 3.7 dB (broadband) vs. 14.3 dB (tone) maximum
deviation, and 0.7–4 dB vs. 0.02 dB resulting sound-power uncertainty, in the same progressively
degraded rooms. Winker & Stahnke (2016, item 5, p. 7): high-frequency qualification failures occur
"during pure tone qualifications and [are] not present in broadband qualifications due to signal
averaging." Cunefare et al. (2003, item 3): on identical traverses, tone deviations exceed tolerance
in up to 56 % of sample points while broadband deviations are "unremarkable" (Table IX, p. 891).
Nash (2019, item 4): a single chamber where 1/3-octave pink noise gives a near-ideal fit while the
same traverse with tones shows a "physically impossible" notch (p. 1347–1348). Pao, Wenzel & Oncley
(1978, item 10, p. 14) independently make the practitioner-level version of the same point: manual
ground-effect smoothing "will obviously be incorrect in cases where a strong tone is present."
**No retrieved source states a quantitative bandwidth-vs-comb-spacing criterion** (e.g. band Δf
relative to comb spacing c/2Δr) for how wide a band must be before averaging reliably works — this
sub-question is unanswered by anything retrieved this session; the closest indirect evidence is that
1/3-octave or full-octave filtering was empirically sufficient at the frequencies Cunefare (2003)
tested, and that Rasmussen & Winberg's (2022, item 1) own 1/3-octave-filtered data still shows a
visibly smoothed but not eliminated comb signature (p. 4).

**Q4 — spatial averaging over ~λ/2:** The only standard-level requirement resembling "move ~λ/2"
in the retrieved set is ISO 26101's own traverse-length rule (Winker & Stahnke 2016, item 5, p. 4:
"the traverse path distance to extend out to one-half wavelength of the lowest frequency of
interest"). Winker & Stahnke quantify, with two real-chamber case studies, that this specific
distance requirement is **not needed to detect a real defect**: measured deviations from
inverse-square law are "evident well before the one-half wavelength traverse distance required by
ISO 26101" (p. 5) — i.e. the residual risk of stopping short of λ/2 appears low in their data, while
the cost (chamber size, or an artificially reduced qualified frequency range) is real and
demonstrated (p. 5–6). Cunefare et al. (2003, item 3) quantify the complementary risk — inadequate
spatial *sampling density* within that span, not total distance — deriving from the measured
interference-pattern zero-crossing spacing (29–41 % of a wavelength, not a half) a Nyquist-style
requirement of ≤15 % of a wavelength between samples, and showing a concrete case where 0.3 m
discrete sampling at 4 kHz misses a violation that continuous sampling catches within 1.5 m of the
source (p. 889-892) — the best-quantified "residual error from inadequate spatial averaging" figure
retrieved, though it concerns discrete-sample spacing rather than a deliberate λ/2 sweep-and-average
technique. Simmons, Jobling & Payne (2004, item 6, p. 8) describe one real instance of deliberate
multi-position averaging expressly to cancel a ground-plane interference pattern (four heights on a
1.5 m hemisphere, "averaged in order to reduce cancellation effects from the ground plane"), but for
calibrating a reference source, not a device under test, and with no residual-error number attached.
**No retrieved source describes moving the *source* over ~λ/2 to average an interference pattern
in a free-field context**, and no retrieved source frames the λ/2 traverse as an averaging technique
per se (all frame it as a spatial-extent requirement for detecting a deviation) — flagged as not
directly answered by anything retrieved this session.

**Q5 — separating direct from reflected field for a continuous source:**
- *Time gating*: confirmed failing at low frequency, exactly as flagged. Friot & Gintz (2009,
  item 2, PDF p. 3): "methods involving windowing of time responses have failed, mainly because at
  low frequency echoes from a scattering body are very difficult to separate from actuator
  responses," in their LMA anechoic-room active-control experiments.
- *Cepstral deconvolution*: described in detail, at second hand, by Pao, Wenzel & Oncley (1978,
  item 10, p. 15), attributing the technique to Miles, Stevens & Leininger (1977, JASA 61(1), 35–38
  — **not independently retrieved**, AIP/JASA blocked): take the log-spectrum, Fourier-transform it
  so the comb pattern collapses to a single "quefrency" spike, remove the spike, inverse-transform to
  recover a ground-effect-free spectrum — explicitly caveated as valid "only for acoustic
  measurements over a hard surface where the surface reflection does not introduce any significant
  phase shift." (Bogert, Healy & Tukey 1963, the original cepstrum paper, and Randall's 2017 MSSP
  history-of-cepstrum survey were both dispatched for retrieval and **not obtained** — see
  RETRIEVAL-A.md. Randall's own earlier 2013 conference version of the same survey **was**
  retrieved (item 13) but, checked directly, does not cover room/architectural acoustics at all —
  it confirms only the general echo-detection motivation and the "lifter" terminology, and shows a
  structurally analogous lifter-based removal of a periodic interference pattern in a mechanical
  vibration signal, p. 1 and p. 15.)
- *Alternatives to gating, all from Friot & Gintz (2009, item 2)*: physically removing the reflecting
  body and differencing (works, but "cannot be done in the case of an anechoic room where active
  control is intended to compensate for the wall reflections", PDF p. 3); placing a microphone in an
  acoustic dipole's null plane so only the reflected field is picked up (worked for rigid walls,
  "too ill-conditioned" for absorbing walls, PDF p. 8); inverting a linear scattering-filter model
  from primary-off/secondary-on measurements (the paper's own proposed method, ~10 dB reduction
  achieved, PDF p. 5–6).
- *Analytic/impedance-based correction, not gating or cepstral*: Pao, Wenzel & Oncley (1978, item 10,
  p. 13–14) describe correcting a measured spectrum by computing the ground reflection analytically
  from an independently known or estimated ground impedance, validated against a real static
  jet-engine test (75 m over gravel, matched against a balloon-suspended reference microphone at the
  same distance — "very good agreement").
- *"Two-distance" methods*: **not found described as such, by that name, in any source retrieved
  this session.** The closest structural analogue in the retrieved set is the K2 "two-surface"
  method (items 7, 9: comparing sound levels on two similar, nested measurement surfaces of
  different radius, S₂/S ≥ 2), which separates a *global* room correction, not a *single reflector's*
  direct/reflected split, from two-distance data. No claim is made that this is the same technique
  the question has in mind.
- *Coherence-based separation*: not found in any source retrieved this session — flagged as
  unanswered.

---

*Files*: this document and `RETRIEVAL-A.md` are the two required deliverables for Thread A. New PDFs
are in `papers/arc-validation/`; fresh plain-text re-extractions of every held paper used are in
`papers/arc-validation/refetch-txt/`; plain-text extractions of the four new PDFs are in
`papers/arc-validation/txt/`.
