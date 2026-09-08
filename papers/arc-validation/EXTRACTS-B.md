# Thread B — reflection vs. rotor/inflow asymmetry in the ±36° blade-passage-band pattern

Scope: is the ±36° pattern in the 200–250 Hz (BPF) band a room reflection, or a signature of a
rotor whose inflow is not axisymmetric (recirculation, or a nearby stand/support breaking
circumferential symmetry)? All held papers below were re-extracted fresh with plain
`pdftotext -q` into `papers/arc-validation/refetch-txt/<name>.txt` and quoted from that dump,
not from the earlier `EXTRACTS-local.md` / `EXTRACTS-downloaded.md` / `MATRIX-3W.md` notes in
`papers/chamber-problems/`. New PDFs are in `papers/arc-validation/` with text in
`papers/arc-validation/txt/`. Page numbers for journal articles with their own continuous
pagination (JASA, Acoustics Australia) are the **printed journal page**, read directly off the
running header/footer in the text dump. Page numbers for standalone conference papers, theses
and NASA reports are the **document's own page**, verified against the source PDF with
`pdftotext -f N -l N <pdf> -` (binary search for the quoted string) — this caught several ±1
errors from a first-pass heuristic (noted where relevant), so every page number below has been
confirmed this way, not just read off a running head that might be a figure/reference number.

---

## NEW SOURCES — NASA static-fan-test inflow-distortion/ICD literature (Q1, Q2)

### Hanson 1977, NASA CR-2899 — `Hanson_1977_NASA-CR-2899_QF-1B-inflow-distortion-rig-interference.pdf`
Donald B. Hanson (Hamilton Standard, for NASA Lewis Research Center), *Study of Noise and
Inflow Distortion Sources in the NASA QF-1B Fan Using Measured Blade and Vane Pressures*, NASA
Contractor Report CR-2899. Evidence level: **report** (NASA CR, contractor study with
blade-mounted pressure transducers + far-field microphones). Retrieved from NASA NTRS
(`ntrs.nasa.gov/api/citations/19770026169`), confirmed by front matter ("N A S A CONTRACTOR
REPORT / STUDY OF NOISE AND INFLOW DISTORTION SOURCES IN THE NASA QF-1B FAN ... Donald B.
Hanson ... Hamilton Standard ... for Lewis Research Center").

This is the single most directly relevant source found for Q1+Q2: it is a controlled study of
exactly the mechanism the one-pager needs ruled in or out — a **fixed, localized support
structure near a rotor inlet producing a circumferentially (azimuthally) non-uniform,
BPF-harmonic-generating inflow distortion**, with a deliberate blockage-plate experiment
isolating the effect from atmospheric turbulence.

- p.1 (SUMMARY): "In this report the inflow distortion is analyzed in terms of the unsteady
  rotor blade pressures caused by atmospheric turbulence and rig interference. **Atmospheric
  turbulence effects are considered to act more or less uniformly around the circumference
  whereas rig interference, which is roughly an equal contributor to the distortion, acts
  mainly at the bottom of the inlet. The source of rig interference appears to be the support
  structure which is located behind the inlet lip underneath the fan.**"
- p.1: "A noise spectrum peak occurs at approximately 2.2 times blade passing frequency at all
  RPMs tested... At 60, 70, and 80% of design RPM, the spectrum peaks at 1, 2, and 3 times
  blade passing frequency are caused by inlet distortion/rotor [interaction]."
- p.12 (Circumferential Distribution of Inlet Distortion): "Frequently, several distinct
  disturbances can be found at once. This is particularly obvious in figure 12 which suggests
  4 or 5 vortices streaming from the fan support structure." And: "Disturbances which enter the
  rotor at the side or top tend to migrate toward the bottom by the shortest route before
  losing their identity. A similar effect was noted in the Q-Fan tests but the migration was
  always in the direction of rotor rotation." [the migration-direction detail is from a
  companion Q-Fan study, cited by Hanson for comparison, not a re-measurement in this report]
- p.12: "The most important implication of this figure is that **the unsteady distortion σpn is
  far larger than the steady distortion, particularly near the bottom of the inlet**. Secondly,
  the steady part of the flow p̄n is distorted about equally around the circumference whereas
  **the unsteady distortion is concentrated near the bottom**."
- p.13: "...it appears that **the fan support structure is roughly as important as atmospheric
  turbulence in generating random inflow**. Therefore, to make a significant improvement in
  rotor noise, both sources would have to be reduced." And, on the deliberate obstruction
  experiment: "figure 18 shows the effect of the blockage plate. **The mean pressure is
  increased substantially to the point that it is larger than the standard deviation and is
  localized to the vicinity of the plate location.**"
- p.21 (System Calibration): "The reason for this failure probably is related to the asymmetry
  (in a statistical sense) of the inlet flow. **The localized blockage causes a noise
  directivity pattern which is not symmetric with respect to the fan axis of rotation.** The
  theory correctly handles this condition for sound power calculations but not for sound
  pressure... **since the plate blockage and the natural blockage from the support structure
  occurred at different azimuths in the inlet, sound pressures from the two configurations
  could not be related.**" (Quantified failure of the theory when azimuth isn't matched: "the
  blade passing frequency spectrum peak, which must be caused by inlet distortion at low RPM
  because of duct cutoff, was underpredicted by 10 to 15 db.")
- p.24 (CONCLUSIONS §3): "**The RMS distortion was 2 to 3 times stronger at the bottom than at
  the top. This is different from the Q-Fan whose distortion was more nearly uniform around the
  circumference.** By tracing streamlines upstream from the blade transducer locations, it was
  concluded that this additional distortion was caused by the fan support structure which was
  under the fan behind the inlet lip."
- p.25 (CONCLUSIONS, Dominant Noise Sources §1–2): "At 60, 70, and 80% of design RPM, the
  spectrum peak at blade passing frequency was caused by interaction of the rotor with inlet
  turbulence and distortion... The spectrum peaks at 2 and 3 times blade passing frequency were
  caused by interaction of the rotor with inlet turbulence and distortion at all RPM's."
- p.28 (Appendix B, Tyler–Sofrin spinning-mode theory): "the condition for mode propagation at
  blade passing frequency is [equation with] m = circumferential mode order... **The index m
  counts the number of lobes in the circumferential direction.**" This is the acoustic-theory
  basis for why a fixed asymmetric structure near a rotor produces a specific number of
  azimuthal lobes rather than a uniform ring.

### Hodder 1977, NASA TM X-73183 — `Hodder_1977_NASA-TMX-73183_static-to-flight-fan-tone-noise.pdf`
Brent K. Hodder (Ames Research Center / U.S. Army Air Mobility R&D Laboratory), *Further
Studies of Static to Flight Effects on Fan Tone Noise Using Inlet Distortion Control for Source
Identification*, NASA TM X-73183. Evidence level: **report**. Retrieved from NASA NTRS
(`ntrs.nasa.gov/api/citations/19770007084`), confirmed by front matter. This is a follow-up to
Hodder's own AIAA 76-585 (1976), "An Investigation of Possible Causes for the Reduction of Fan
Noise in Flight" (= "reference 1" in the quotes below; **not separately retrieved** — see
RETRIEVAL-B.md), which this report re-states and extends.

- p.1 (SUMMARY): "An experimental investigation reported in reference 1 linked **inflow
  distortion phenomena such as ground vortex, atmospheric turbulence, and teststand structure
  interference to the generation of fan tone noise at the blade passing frequency.**" And:
  "Atmospheric turbulence effects were reexamined with the modified engine and the distortion
  control inlet used in reference 1. Results showed a large reduction in both the level and
  variability of noise radiated at the blade passing frequency. **Reductions in far-field,
  sound-pressure levels of 7 dB were measured from an on-axis location up to 60° off-axis.**"
- p.1 (INTRODUCTION): "Engine inflow distortions investigated in reference 1, like the ground
  vortex, atmospheric turbulence, and test-stand structure interference, **were shown to
  substantially increase the sound pressure levels and variability of noise at the blade
  passing frequency.**"
- p.3 (TEST APPARATUS): "The engine was top-mounted to a pylon attached to a 3.048-m span wing.
  **The engine centerline was 7.7 fan diameters above the ground, and the bellmouth inlet was
  cantilevered 5.1 fan diameters forward of the test-stand-support struts** (fig. 2)." — a
  concrete precedent for how far test engineers keep a support structure from the rotor to
  avoid contaminating the measured directivity.
- p.7 (rotor-core-stator + T1-probe results): "As shown in figure 19(a), **removal of the core
  stators reduced the strong on-axis radiation by 13 dB**." And, on a physical obstruction (an
  inlet temperature probe) deliberately left in vs. removed from the flow: "with the production
  T1 probe installed, the measured far-field data (fig. 20(a)) showed an **increase of at least
  6 dB in f1 SPL on the axis as well as 7 dB at 30°. Beyond 60° the difference ... decreased
  rapidly. At θ = 90° and 120°, little significant difference in f1 SPL is shown.**" — i.e. a
  single localized physical obstruction near the rotor inlet raises the BPF tone strongly near
  its own side/axis and fades to nothing by 90–120° away from it, a clean angular signature of
  a structural (not atmospheric) asymmetry.
- p.9 (concluding remarks): "It seems reasonable to conclude that the results of this
  investigation have **reinforced the arguments in reference 1 for the control of inflow
  distortions common to conventional static testing**."

### Woodward, Wazyniak, Shaw & MacKinnon 1978, NASA TM-73855 — `Woodward-etal_1978_NASA-TM-73855_inlet-turbulence-control-device-anechoic-chamber.pdf`
R. P. Woodward, J. A. Wazyniak, L. M. Shaw, M. J. MacKinnon (NASA Lewis Research Center),
*Effectiveness of an Inlet Flow Turbulence Control Device to Simulate Flight Fan Noise in an
Anechoic Chamber*, technical paper for the 94th Meeting of the Acoustical Society of America
(Miami, Dec 1977), NASA TM-73855. Evidence level: **report/conference**. Retrieved from NASA
NTRS (`ntrs.nasa.gov/api/citations/19780005913`).

- p.2 (Abstract): "**A hemispherical inlet flow control device was tested on a 50.8 cm
  (20-inch) diameter fan stage in the NASA-Lewis Anechoic Chamber**... Far field acoustic power
  level results showed **about a 5 dB reduction in blade passing tone and about 10 dB reduction
  in multiple pure tone sound power** at 90% design fan speed with the inlet device in place."
- p.2 (Introduction): "Turbofan engine noise investigations have shown considerable difference
  in fan noise levels between static and flight operation... the blade passing tone level is
  often much higher under static testing conditions. A plausible explanation of this phenomenon
  is offered by Hanson (refs. 2 and 3) in which atmospheric turbulence eddies are envisioned as
  being elongated as they are drawn into the statically-operating fan, thereby generating a
  tone at blade passing frequency as several blades pass through this disturbance. No
  significant tone noise generation from this source would be expected during flight since
  these eddies would enter the fan inlet with little distortion (i.e., elongation)." [refs.
  2–3 = D. B. Hanson, "Measurements of Static Inlet Turbulence," AIAA 75-467, and "A Study of
  Subsonic Fan Noise Sources," AIAA 75-468, both March 1975 — **not separately retrieved**, see
  RETRIEVAL-B.md; this is Woodward et al.'s own paraphrase of Hanson's mechanism, not a
  first-hand quote of Hanson]
- p.12 (Significant results): "1. **The presence of the inlet flow control device reduced the
  level of the blade passing tone by about 10 dB at some angular locations, giving about a 5 dB
  reduction in the sound power level** at the fundamental tone frequency. However, the tone was
  not reduced to near broadband levels as had been observed in some flight measurements... 3.
  **Rotor-inflow disturbance interaction was more important than rotor-stator interaction** in
  the generation of inlet fundamental blade passing tone noise. However, the inlet first
  overtone (2×BPF) levels are controlled by rotor-stator interaction at close spacing..."
  (directivity measured on a polar arc at fixed azimuth — see "what none of these test the"
  note below).

### Woodward & Glaser 1980, NASA TM-81487 — `Woodward-Glaser_1980_NASA-TM-81487_inflow-control-cuton-fan.pdf`
R. P. Woodward and F. W. Glaser (NASA Lewis), *Effect of Inflow Control on Inlet Noise of a
Cut-on Fan*, NASA TM-81487. Evidence level: **report**. Retrieved from NASA NTRS
(`ntrs.nasa.gov/api/citations/19800014609`). Poor-quality 1980 microfiche scan (OCR frequently
garbled, e.g. "Rasultsof" for "Results of"); page below is the **PDF's own page ordinal**
(verified with `pdftotext -f 5 -l 5`), not a confirmed printed-page number, because the
disclaimer/title front matter length couldn't be pinned down from the OCR.

- PDF p.5: "The baseline results show a directivity pattern that is typical for rotor-inflow
  interaction **in which the energies of many acoustic radiation modes are combined with no
  particular modal pattern dominating the directivity**... **A lobed pattern begins to appear
  in the directivity with this level of inflow control, suggesting that a limited number of
  driving modes now control the directivity.**" And, at higher inflow-control levels: "**The
  remaining lobed structure in the directivity with maximum inflow control suggests a tone
  contribution from rotor-stator interaction modes.**" — i.e. broadband atmospheric turbulence
  can mask an underlying discrete-lobe (structural-asymmetry) directivity pattern; removing the
  turbulence does not remove the lobe, it reveals it.

### Homyak, McArdle & Heidelberg 1983, NASA TM-83349 — `Homyak-etal_1983_NASA-TM-83349_compact-inflow-control-device.pdf`
L. Homyak, J. G. McArdle, L. J. Heidelberg (NASA Lewis), *A Compact Inflow Control Device for
Simulating Flight Fan Noise*, AIAA-83-0680 / NASA TM-83349, 8th AIAA Aeroacoustics Conference
(Atlanta, April 1983). Evidence level: **report/conference**. Retrieved from NASA NTRS
(`ntrs.nasa.gov/api/citations/19830018372`). Page numbers below are the PDF's own page (verified
with `pdftotext -f N -l N`, and this is a clean-scan standalone paper so PDF-ordinal = the
paper's own page 1…18).

- p.5 (Introduction): "During ground static testing of jet engines, **atmospheric turbulence
  which undergoes vortex stretching and other inflow disturbances not present in flight can
  cause strong tone noise by interaction with the fan rotor.**" And, on facility geometry: "The
  support arm faired smoothly into the engine cowling and **positioned the engine inlet greater
  than 3.4 diameters from any facility or ground structure.**"
- p.6 (Directivity Patterns): "The fan blade passing frequency (BPF) modes which are most
  likely to affect the directivity patterns are: **M = 22, from interaction between 28 fan
  blades and 6 engine structural struts**; M = 19, from interaction between 28 fan blades and 9
  ICD ribs and sections; and M = −13, from interaction between 28 fan blades and 41 inlet rod
  wakes present in acoustic transmission tests." And: "At this speed the M = 19 mode is just
  cut-on, and **there appears to be a weak lobe peaking at about 60°**. This tone (considered
  insignificant) originates from rotor/rib wake interaction. At 10 800 rpm ... **the M = 22
  mode is just cut-on, and also causes a lobe near the 60° angle. This lobe has been observed in
  many previous tests with this engine.**" [i.e. a fixed, repeatable, azimuthally-lobed tone
  tied to the count of a stationary structure (6 struts) interacting with the rotating blades —
  reproduced across "many previous tests"] Also: "The q = 1 spike is observed in all tests at
  this facility, and may be caused by the ground plane (although the engine centerline is
  5-1/2 engine fan diameters from the ground)." — even ~5.5 diameters of clearance did not
  rule out a possible surface-proximity contribution to a low-order (asymmetric) spinning mode.
- p.6, on what an inlet-turbulence screen does and does not fix: "At each speed the ICD reduced
  the tone levels associated with rotor-inflow distortion interaction, but **the principal lobe
  from the M = −13 mode produced by the rod wake mechanism is essentially the same with and
  without the ICD installed.**" — a turbulence-control screen upstream of the rotor removes an
  atmospheric-turbulence-type tone but does **not** remove a tone generated by the rotor's own
  wake striking a fixed structure downstream of the screen (i.e. between the screen and the
  rotor, or the support itself) — waiting/settling or upstream screening would not help with
  that kind of source.
- p.7 (Test for rib thickness effect): "At 9700 rpm, the M = 19 mode due to nine rib-rotor
  interaction is just cut-on, so **a large lobe was expected near 60° in the directivity
  pattern**." (Confirms the same M=19/60° lobe as p.6, from an independent test varying rib
  thickness.)
- p.6 (Directivity measurement geometry): "Acoustic measurements were made from 10° to 90°
  about the engine inlet by ... far-field ground microphones on a 24.4 m (80-ft) radius circle"
  — i.e. **a single polar arc at one azimuth**, like nearly every other source in this thread;
  it does not itself sweep azimuth, but the M=22/six-strut finding is inferred from the
  Tyler–Sofrin mode count, not from a swept azimuthal mic array.

---

## ADDITIONAL SOURCE — found already in the shared `papers/arc-validation/` pool (Q1, Q2, Q5)

### Zawodny & Boyd 2017, AHS (VFS) Forum 73 — `Zawodny-Boyd_2017_AHSForum73_rotor-airframe-interaction-SALT.pdf`
Nikolas S. Zawodny, D. Douglas Boyd Jr. (NASA Langley Aeroacoustics Branch), *Investigation of
Rotor-Airframe Interaction Noise Associated with Small-Scale Rotary-Wing Unmanned Aircraft
Systems*, 73rd Annual Forum of the American Helicopter Society (Vertical Flight Society), 2017.
Evidence level: **conference**. This PDF was not fetched by this thread — it was already present
in the shared `papers/arc-validation/` pool, evidently retrieved by a concurrent thread on the
same campaign — but it was read fresh from a `pdftotext -q` dump made this session
(`txt/Zawodny-Boyd_2017_AHSForum73_rotor-airframe-interaction-SALT.txt`), identity-confirmed
from its own front matter (title/authors/NASA Langley affiliation), and every quote below
page-verified against the source PDF with `pdftotext -f N -l N`. It is the single most direct
piece of evidence found for Q2: a purpose-built experiment, in the **same SALT facility** used
by Zawodny & Haskin 2017 above, with a microphone array explicitly split into elevation *and*
azimuthal sub-arrays, testing exactly "does a fixed structural element near a hovering rotor
make the tonal directivity azimuthally non-uniform."

- p.2 (Experimental Setup): "A total of five ... free-field Brüel & Kjaer microphones in an arc
  array configuration are positioned in the acoustic far-field of the rotor test stand. The
  microphones are positioned at a radial distance of 1.905 m from the rotor hub, **which
  corresponds to approximately 16R** for the rotor tested in this study. **The microphone array
  is divided into elevation and azimuthal sub-arrays**" — Table 1 gives (θ,φ) = M1 (0°,0°), M2
  (−22.5°,0°), M3 (−45°,0°), M4 (−45°,+45°), M5 (−45°,+90°), all at r = 16R. A simple carbon-fibre
  tube ("generic airframe," representing a multicopter arm) or a conical section was cantilevered
  near the rotor tip at varying vertical clearance Δ/R.
- p.6: at the closest tested spacing (Δ/R = −0.1, i.e. 0.1 rotor radii below the tip): "M5 ... [a]
  harmonic-rich spectrum with the **second through seventh BPF harmonics having an acoustic
  amplitude greater than or equal to the BPF acoustic amplitude itself**. Microphone M3 shows a
  similar behavior, but with harmonic amplitudes all being **at least 5 dB below the BPF
  amplitude**." And, on why: "It is interesting to note how the tonal amplitudes are larger for
  M5 than for M3, and **how M5 is oriented normal to the centerplane of the rod while M3 is
  coplanar with the rod. This is an indication that the rod may be a prominent, directive noise
  contributor** for this case." [i.e. the induced tone radiates like a dipole broadside to the
  obstruction's own axis, not simply "loudest on the side nearest the obstruction" — a sharper
  mechanistic detail than the "acts mainly at the bottom" framing in Hanson 1977, complementary
  to it]
- p.6 (clearance sensitivity — a concrete distance-in-radii number): "Increasing the distance
  between the airframe and rotor tip from 0.1 to 0.2 tip radii below the rotor tip has the most
  drastic effect, with a **maximum reduction of approximately 8 dB in unweighted OASPL and
  nearly 10 dB in A-weighted OASPL at M5**. Increasing this distance to 0.4 tip radii yields
  unweighted levels for all microphones that are **nearly identical to those for the case of an
  isolated rotor**."
- p.16 (Conclusions): "Experimental measurements revealed prominent tonal noise associated with
  airframes within close proximity of the rotor plane, which was observed to decay fairly
  rapidly with increasing rotor-airframe spacings. **Cases of prominent rotor-airframe
  interaction noise were found to be highly directive as a function of observer azimuth, the
  highest amplitudes of which were exhibited by observers located out of the centerplane of the
  airframe.** Generic airframes of constant cross-section were found to have little or no effect
  on noise radiated in the plane of the rotor [i.e. at φ = 0°, coplanar with the rod] ... the
  broadband noise content was observed to be nearly identical for all tested rotor-airframe
  configurations, providing evidence that this noise is due to rotor-generated turbulence
  because the airframes tested occupy a very small azimuthal portion of the rotor disk area."

---

## HELD PAPERS — re-read fresh from `papers/arc-validation/refetch-txt/`

### Stephenson, Weitsman & Zawodny 2019, J. Acoust. Soc. Am. 145(3), 1153–1155 (Letter)
`papers/chamber-problems/Stephenson_2019_JASA_recirculation-UAS-closed-anechoic-chambers.pdf`.
Evidence level: **journal** (JASA Letter). Identity confirmed from front matter (title, authors,
DOI 10.1121/1.5092213 match `BIBLIOGRAPHY.md`).

- p.1153 (Abstract): "flow recirculation results in a significant increase in higher harmonic
  noise, **with an increase of more than 15 dB in some harmonics.**"
- p.1153 (Experimental setup): "**An azimuthal array was not employed as the acoustic emissions
  of an isolated rotor in hover should be symmetric.**" — this is the exact assumption the
  one-pager's claim rests on; Stephenson et al. state it as a premise, not a measured result.
- p.1154 (Results): spectrogram of mic M1 (above the rotor plane): the first BPF harmonic
  "appears around 3.5 s at a level of approximately 45 dB. Higher harmonics of the BPF are not
  visible between 3.5 and approximately 7.5 s. At approximately 7.5 s into the run, flow
  recirculation in the room has established and the higher harmonics of the BPF are now
  observable. **The amplitudes of the higher harmonic content have increased in excess of 15 dB
  for many of the harmonics.**"
- p.1154: "**Unsteady loading noise of a rotor is known to emit predominantly above and below
  the rotor plane, while thickness noise is predominantly emitted in the plane of the rotor.**"
  Comparing mics above (M1), in-plane (M4) and below (M6) the rotor: "**the first harmonic of
  the blade passage frequency is relatively unaffected** by the flow recirculation within the
  room. However, **the second harmonic for the out of plane microphones has increased by
  approximately 30 dB. The third blade passage harmonic has increased by more than 15 dB**...
  The relative steadiness in levels for pre- and post-recirculation for the **in-plane
  microphone** is of particular note."
- p.1155 (Conclusions): "For the current test campaign, **the onset of flow recirculation
  occurred within 5 s of reaching steady state RPM. However, this recirculation time is heavily
  dependent on the size of the facility, size of the rotor, and the thrust the rotor is
  exerting on the flow.**"

### Weitsman, Stephenson & Zawodny 2020, J. Acoust. Soc. Am. 148(3), 1325–1336
`papers/chamber-problems/Weitsman_2020_JASA_recirculation-rotary-wing-closed-chambers.pdf`.
Evidence level: **journal**. Identity confirmed (DOI 10.1121/10.0001901).

- p.1326: "**An azimuthal array was not employed as the acoustic emissions of an isolated rotor
  in hover should be symmetric.**" Facility: SHAC, "10.67 ft (3.25 m) in height, 8.38 ft (2.55
  m) in width, and 12.67 ft (3.86 m) in length" — comparable order of magnitude to the "room of
  order 3×3×2.5 m" assumed for our own rig in PROTOCOL.md.
- p.1327: "the ramp up region, which is shown to occur 3.5 s after the start of the trial ...
  the ramp up region is followed by the clean region, which is **sustained from 3.5 to 7.4 s**.
  ... In this region, the sound pressure level (SPL) of the BPF remains steady at approximately
  42 dB." And: "The effects of recirculation becomes evident 7.4 s after the beginning of the
  trial ... **The BPF harmonics are significantly amplified ... with the first three harmonics
  exhibiting an amplification of nearly 20 dB.**"
- p.1329: "As shown in figure 3, prior to the onset of recirculation, the SPL of the BPF
  surpasses that of the upper order harmonics at all three measurement locations. **The SPL of
  the BPF is also greater in the rotor plane, whereas the broadband noise levels are greater
  outside of the rotor plane. These directivity trends in the acoustic emissions are expected
  for a lightly loaded rotor.**" And, after recirculation develops: "**The greatest tonal
  amplification is evident outside of the rotor plane, where the first three BPF harmonics are
  amplified by nearly 20 dB.**"
- p.1335 (Conclusions): "Prior to the installation of the treatment, **the observed duration to
  acquire uncorrupted measurements was 3.9 s**... This duration is **highly dependent upon the
  room geometry, operational thrust condition, and size of the rotor.**" "Two meshes positioned
  parallel to, and aft of the rotor plane, yielded the best results, **extending the duration
  prior to the onset of recirculation to approximately 10 s.**"

### Nardari, Casalino, Polidoro, Coralic, Brodie & Lew 2019, AIAA 2019-2497 (25th AIAA/CEAS Aeroacoustics Conference)
`papers/chamber-problems/Nardari_2019_AIAA_flow-confinement-UAV-rotor-noise.pdf`. Evidence
level: **conference**. Identity confirmed (DOI 10.2514/6.2019-2497). Standalone paper,
pages 1–17 of its own numbering, verified against the source PDF page-by-page.

- p.1 (Abstract): "Comparison between simulations reveals a significant increase in rotor noise
  due to confinement, **up to 5 dBA in overall sound pressure level** depending on microphone
  location, with negligible impact on aerodynamic performance... **Leading-edge interactions
  between the vortical structures convected by the recirculating flow and the rotor's blades
  are demonstrated to be directly responsible for the generation of unsteady loads that lead to
  significantly higher blade passing frequency harmonic peaks.**"
- p.6: "the effect of the flow confinement results in **an almost constant offset of about 5
  dBA, with the largest differences occurring at microphones close to the rotor axis.**"
- p.9 (Analysis Process): source power level is computed from "four signals at the same angular
  position with respect to the rotor axis and different azimuthal positions... **assuming an
  axisymmetric acoustic field**." — the method *imposes* azimuthal symmetry rather than testing
  it; the paper never reports an azimuthal directivity result, only elevation/meridian angle.
- p.11: "**The first two BPF tones are almost unaffected, whereas, starting from the third BPF
  harmonic, the tones for the confined results are about 5 to 10 dB higher** than for the
  unconfined case. Such a different spectral behavior translates into about a 2 dB variation of
  OASPL at the maximum radiation angle of about 120 deg (ground side)... **Along the rotor
  axis, where the rotor-locked noise contribution tends to vanish, the confined case is up to 9
  dB louder than the unconfined case, both towards the sky (0 deg) and the ground (180 deg).**"
- p.16 (Conclusion): "**It was found that flow recirculation leads to a nearly 5 dBA increase in
  OASPL across most microphone locations, but has negligible impact on the thrust and torque of
  the rotor.**"

### Ma, Zhou, Zhang & Zhong 2024, Acoustics Australia 52, 313–322
`papers/chamber-problems/Ma_2024_AcoustAust_recirculation-free-flying-UAS-anechoic.pdf`.
Evidence level: **journal**. Identity confirmed (DOI 10.1007/s40857-024-00327-x).

- p.313 (Abstract): "The measured acoustic spectrogram reveals that **the recirculation forms
  around 30 s after the UAS's take-off**, manifested as prominent fluctuations in blade passage
  frequency and its harmonics. However, the instantaneous overall sound pressure level shows no
  obvious increase... The quantitative analysis of different noise components shows that **the
  recirculation has a minimal effect on the tonal noise levels but slightly increases the
  broadband noise level out of the rotors' plane.**"
- p.314 (Ma's own literature summary of Stephenson 2019 — a paraphrase, not a Stephenson
  quotation): "Stephenson et al. [7] tested the noise of a small-scale propeller ... The results
  suggest that recirculation can increase the measured noise by over 15 dB at the blade passage
  frequency (BPF) harmonics. They attributed this phenomenon to the unsteady loading caused by
  the recirculation, as the increase occurs predominantly out of the rotor plane. With the rotor
  producing a 0.75 lb (3.34 N) thrust, **the formation time of the recirculation is around 4
  s.**" [Ma's rounding of Stephenson's own "~5 s after steady RPM" / "~7.5 s into the run"
  figures — a paraphrase, cited here as Ma's own text, not as a re-quotation of Stephenson.]
- p.317: microphones "were in a vertical plane that passes the horizontal center of the
  chamber" (an elevation array at one fixed azimuth, like all the isolated-rotor studies above).
  "**the tonal noise levels remain largely unaffected by the presence of flow recirculation.
  Meanwhile, a slight increase in the extracted broadband noise level is observed particularly
  out of the UAS's rotor plane** ... the directivity trend is consistent with the
  characteristics of loading noise... **The SE [spectral entropy] increases by 0.07~0.08
  (12%~13%) at tested microphone locations, no prominent directivity was found for the SE
  increments.**"
- p.317 (Ma's explanation for the discrepancy with Stephenson/Weitsman): "the chamber used in
  our work is significantly larger, approximately 8 and 12 times the volume of the ones
  employed by Stephenson et al. [7] and Bu et al. [11] ... This disparity results in lower
  turbulence intensity within the recirculation zone and a longer onset time." — i.e. Ma's
  30-s/weak-tonal-effect result is for a much larger free-flying-UAS chamber and does not
  contradict Stephenson/Weitsman's fast (~4–8 s), strong-tonal-effect result for a small,
  statically-mounted rotor in a small room — the configuration closer to ours.

### Fasulo, Longobardo, De Gregorio & Barbarino 2025, Aerospace (MDPI) 12, 647
`papers/chamber-problems/Fasulo_2025_Aerospace_rotor-noise-directivity-decay.pdf`. Evidence
level: **journal** (MDPI, open access). Identity confirmed from front matter and running "of
26" footers (independently cross-checked against direct `pdftotext -f N -l N` page extraction —
all three spot-checked quotes matched their footer-implied page exactly, so the "N of 26" pages
below are reliable). **Note of direct relevance: this rig's isolated-rotor configuration uses a
Tyto Robotics 1585 Thrust Stand — the same model as SoundVisualizer's — so its pylon-asymmetry
finding is not just analogous, it is evidence about the same class of hardware.**

- p.4 (Rotor Rigs): "**Isolated rotor stand: a TYTO ROBOTICS 1585 Thrust Stand**, which features
  dedicated control system and data logger. Two sets of load cells integrated within the stand
  allow for both thrust and torque measurements."
- p.10: "there is a **small but significant mounting asymmetry: although the rotor hub is
  centred, the pylon supporting the isolated propeller is offset to the left side of the array**
  (the 0°–180° hemisphere), roughly in line with the 30° microphone. That lateral offset
  **produces additional shading behind the propeller and contributes to the left-right level
  differences observed in the OASPL profiles.**"
- p.11: "Further experiments performed with opposite senses of rotation (CW versus CCW) reveal
  **far larger azimuthal variations than those observed when only the blade was changed**. Over
  the low-moderate speed range (3000–5000 rpm), the mean absolute OASPL difference among the ten
  microphones already reaches 1 dB. At higher rotational rates, the disparity increases sharply:
  **about 3 dB at 6000 rpm and 3–4 dB in the 7000–8000 rpm range**. The associated standard
  deviation grows from roughly 1 dB at the lowest speed to nearly 4 dB at 7000 rpm, highlighting
  the substantial microphone-to-microphone scatter induced by the change in rotation sense."
- p.11–12: "**The support pylon lies directly on the acoustic line of sight of microphone 10,
  producing shielding** and a corresponding level reduction relative to its mirrored
  counterpart, namely microphone 8... this effect is most pronounced for clockwise rotation,
  whereas, when the rotor spins counter-clockwise, the attenuation at the same azimuth is
  markedly smaller, presumably because the ground reflection path is altered differently for
  the two senses of rotation. Overall, these findings demonstrate that **rotation sense can
  dominate the apparent non-uniformity of the acoustic field whenever structural or
  environmental asymmetries are present.** The observed deviations, which reach up to 4 dB,
  exceed the experimental uncertainty by a wide margin, confirming that the effect is physical
  rather than a measurement artefact."
- p.18 (recirculation explicitly checked and ruled out for this rig): "In both cases, the BPF
  harmonics remain sharp and strictly horizontal for the entire 30 s record, and no progressive
  rise in broadband energy is detected. **These observations rule out significant wake
  recirculation**, a conclusion that is consistent with the test setup. **The rotor plane is
  situated approximately 6 D above the floor and directs its flow parallel to it, while the
  nearest wall along the wake axis lies more than 12 D downstream.** Under such clearances, the
  wake cannot close a recirculation loop before dispersing."
- p.21 (plate-mounted configuration): "reveals a **pronounced left (0°–180°) versus right
  (180°–360°) asymmetry** in both the OASPL and the first two BPF harmonics, with the effect
  most marked at the fundamental tone... **The first harmonic of the BPF contour displays the
  strongest anisotropy, with a mean level difference of roughly 6.5 dB between mirrored left-
  and right-side microphones.**" Ruling out simple geometry: "the 266.7 Hz tone observed at
  8000 rpm corresponds to an acoustic wavelength of roughly 1.3 m, over three times the 0.36 m
  plate span, rendering classical blockage effects insufficient to account for the measured
  anisotropy... under a far-field decay assumption, the minor path length difference would
  contribute only about 1.6 dB. Instead, **the pronounced asymmetry may arise from near-field
  interactions, in which the rotor's pressure field couples with the plate edge and ground
  surface**, producing direction-dependent interference among direct, reflected, and scattered
  acoustic components."
- p.24 (Conclusions): "**The isolated rotor tests established a repeatable baseline: changes in
  blade manufacturing tolerance altered azimuthal OASPL by less than 0.6 dB across 3000–8000
  rpm**, confirming the internal consistency of the setup... **Reversing the sense of rotation
  revealed that even modest geometric asymmetries, here the support pylon, can shift directivity
  by up to 4 dB.**"

### Jawahar, Hanson, Akhter & Azarpeyvand 2025, Scientific Reports 15, 2170
`papers/chamber-problems/Jawahar_2025_SciRep_porous-ground-propeller-ground-effect.pdf`.
Evidence level: **journal**. Identity confirmed (7.9 × 5.0 × 4.6 m Bristol chamber, DOI
10.1038/s41598-024-82876-9).

- p.7: "the proximity to the GP [ground plane] leads to turbulent ingestion as the propeller's
  wake is reflected and recirculated by the GP, **which can generate higher-order harmonics
  such as blade-vortex interaction (BVI)**."
- p.9: "At θ = 50°, the GE [ground effect] configuration exhibits a **significant increase in
  TSSPL by approximately 4.0–8.0 dB for frequencies above 1000 Hz**. This increase is likely due
  to the reflection of noise from the ground plane, which is observed in both solid and porous
  configurations. **As expected, this increase is absent at θ = 90°, where the sideline region
  does not experience reflections from the ground plane.**"
  Caveat for this thread: Jawahar's ground plane is a single plate centred on and perpendicular
  to the propeller axis, so its θ is a *polar* angle from that axis, not an azimuthal angle
  around it — the plate itself is axisymmetric about the rotor axis. It is direct evidence that
  proximity to any rigid surface raises higher-order harmonics via wake reflection/recirculation
  (relevant to Q1/Q3), but — like Nardari's and the NASA ICD literature's ground/floor
  arcs — it is not a test of azimuthal (circumferential) asymmetry, because the obstruction here
  has none.

### Zawodny & Haskin 2017, AIAA paper (NASA Langley LSAWT capability paper)
`papers/chamber-problems/Zawodny-Haskin_2017_AIAA_LSAWT-small-rotor-capabilities.pdf`. Evidence
level: **conference**. Identity confirmed ("Small Propeller and Rotor Testing Capabilities of
the NASA Langley Low Speed Aeroacoustic Wind Tunnel," Zawodny & Haskin). Standalone paper,
17 pages of its own numbering, page below verified with `pdftotext -f 13 -l 13`.

- p.13: comparing the same isolated UAS rotor tested in the open-jet LSAWT vs. the SALT
  anechoic chamber: "The rotor was mounted in a propeller orientation within the LSAWT test
  section, which allowed for the wake to develop and convect downstream into the diffuser of
  the tunnel. **This configuration reduced the possibility of measurement contamination due to
  wake flow recirculation within the test cell.**" And, on the SALT chamber array: "**Five
  microphones were utilized in the SALT facility experiments (labeled M1–M5 in Fig. 15), that
  spanned a range of elevation (θ) and azimuthal (φ) angles** at a common radial distance of
  10R" — one of the few arrays in this set that names both angles, though the reported
  comparison (below) is only at two elevation angles, not swept azimuth.
- p.13–14: "Acoustic spectra are compared between LSAWT and SALT facility data sets for observer
  elevation angles of θ = 0° (in the plane of the rotor) and θ = −45° (below/behind the rotor
  plane)... The spectral attributes of greatest importance at this observer location are the
  tonal levels at the rotor BPF and the first several associated harmonics, **which are seen to
  agree very well between the data sets**. Focusing attention on the spectra measured at an
  observer angle of θ = −45° reveals an expected increase in mid- to high-frequency broadband
  noise, the trends of which are in excellent agreement between the two facility data sets. In
  addition, **the tonal harmonic content agrees well between the facilities; however, there are
  overall higher levels observed for the LSAWT data set.**" — a useful **null-ish result**: at
  this rotor/thrust condition, the enclosed SALT chamber's tones were not measurably worse than
  the open, wake-vented wind tunnel — consistent with Weitsman's point that recirculation onset
  is thrust- and facility-dependent, not automatic.

### Gallo, De Decker, Bresciani, Haezebrouck, Garone & Schram 2025, Acta Acustica 9, 16
`papers/chamber-problems/Gallo_2025_ActaAcustica_aeroacoustic-propeller-test-bench.pdf`.
Evidence level: **journal**. Identity confirmed (DOI 10.1051/aacus/2024085, VKI ALCOVES
facility).

- p.6: "The room includes an air inlet ... and an air outlet from the discharge room, leading to
  an auxiliary fan that can be used to drive the flow through the facility... **The propeller
  axis is aligned with the opening in the wall partition, to direct the propeller wake towards
  the discharge room.**" And: "At the first BPF, **the difference between the front and rear
  propellers is 1 dB**" [two nominally similar propellers in the same rig/session].
- p.7 (recirculation check in a small, ~11 m³ main room — comparable order of magnitude to our
  own "order 3×3×2.5 m" assumption): "The spectrum **does not reveal any rise in either tonal or
  broadband noise levels over time. Given the small size of the room, one would have expected to
  see a transient effect of the recirculating flow. The spectrograms seem to indicate
  otherwise.** This may be either attributed to the fact that the propeller wake turbulence gets
  somehow 'trapped' in the downstream room, or **that the time needed to establish the
  recirculation is comparable to the time it takes for the RPM to stabilize, in which case
  discriminating both transient effects becomes difficult.**" — direct evidence that a small
  room does **not automatically** show a recirculation transient: whether it does depends on
  whether the wake has somewhere to vent (their room has a ducted outlet to a second room; ours,
  per PROTOCOL.md, is not documented either way).

### Whelchel 2023, PhD thesis, Virginia Tech
`papers/chamber-problems/Whelchel_2023_PhD-VT_sUAS-rotor-noise-outdoor-lab.pdf`. Evidence
level: **thesis**. Identity confirmed (VT Eckel anechoic chamber, DJI rotors, ground-board
study).

- p.65–66 (Sec. 4.1.2, ground-board reflection study — a **known-source substitution**
  diagnostic, used to separate a fixture's acoustic signature from the rotor's own noise):
  "**White noise was radiated by a Bruel and Kjaer omnidirectional source (OmniPower Sound
  Source Type 4292-L) from 50–5000 Hz and recorded by a single microphone with and without the
  ground board** at the two positions... Comparison of spectra for measurements with and without
  the ground board directly beneath shows constructive interference from 140 Hz to 580 Hz...
  Performing these measurements allows one to determine the frequency response of the
  experimental arrangement when the microphone is placed at the center of a hard ground plane.
  **The frequency response is determined by subtracting spectra with the ground board installed
  from that with the Mic only.**" — Whelchel substitutes a calibrated, known, omnidirectional
  loudspeaker source for the drone rotor specifically so that the resulting frequency-response
  correction (fixture/room artefact) is measured independent of anything the rotor itself might
  be doing — a working example of the Q4 "loudspeaker substitution" diagnostic, applied to
  isolate a ground-board reflection rather than an azimuthal asymmetry, but the same logic
  (replace an aerodynamic source with a non-aerodynamic, known one; whatever pattern remains is
  the facility, not the rotor) would apply to separating our reflection from the propeller.

### Alkmim, Cardenuto, Tengan, Dietzen, Van Waterschoot, Cuenca, De Ryck & Desmet 2022, J. Acoust. Soc. Am. 152, 2735–2745
`papers/chamber-problems/Alkmim_2022_JASA_drone-directivity-hemispherical-array.pdf`. Evidence
level: **journal**. Identity confirmed (DOI 10.1121/10.0014957, "Drone noise directivity and
psychoacoustic evaluation using a hemispherical microphone array").

- p.2736: "**Microphone 1 was covered with a windscreen foam as it lies directly underneath the
  propellers.**" (18-mic hemispherical array, average radius 0.98 m, around a rigidly clamped
  quadcopter, mic radius ≈ 0.98/0.137 ≈ 7 rotor radii from the nearest rotor.)
- p.2742: "At low frequencies, below 50 Hz, the −70° direction has much higher levels compared
  to the other directions, **which can be attributed to the downward airflow across the
  microphone diaphragm.**" — this is a mic sitting in the **downwash/wake** (axial, below the
  drone), not the in-plane inflow region the thread asks about; see the caveat in the Q5 answer
  below.

### Hochbaum et al. 2026, Quiet Drones (Delft) conference paper
`papers/chamber-problems/Hochbaum_2026_QuietDrones_drone-directivity-anechoic-realistic-flight.pdf`.
Evidence level: **conference**. Identity confirmed (TU Berlin 13.5×8.3×7.4 m anechoic room, 64
GRAS mics, X500/UBADRON free-flying UAVs). All three pages below re-verified with
`pdftotext -f N -l N` after a first-pass line-marker heuristic was found to be off by one page
(caught by direct verification — the original guesses of pages 2/4/8 were each one page early;
the confirmed pages are 3/5/9).

- p.3: "microphones were equipped with custom-built windscreens **to reduce wind-induced noise
  bursts**."
- p.5: "**Despite the use of custom-built windscreens, microphones located directly below the
  UAV were frequently affected by wind-induced low-frequency noise**, so that many blocks could
  not be considered valid acoustic measurements. To exclude these corrupted blocks, a simple
  empirical rejection criterion was defined... blocks were rejected if any FFT bin magnitude
  level exceeded 70 dB below 100 Hz [X500] ... 77 dB [UBADRON] and the frequency range lowered
  to below 40 Hz."
- p.9: "Owing to the UAV's size and the resulting rotor downwash, **no valid measurements were
  obtained below the UAV.**" — again, this is the axial downwash/wake region directly beneath
  the rotor, not the in-plane (radial, 90°-elevation) region our mics occupy; see caveat below.

### Kim, Oh, Ku, Lee, Lee & Kim 2022, ICSV28 (minor use)
`papers/chamber-problems/Kim_2022_ICSV28_drone-noise-vs-testing-environment.pdf`. Evidence
level: **conference**. Identity confirmed. Used only as light corroboration, not as a primary
source for this thread (it compares chamber vs. outdoor sound-power measurement, not
azimuthal/reflection discrimination):
- (own numbering) "two microphones of M5 and M6 at 2.4 m height among the six microphones shows
  higher sound levels by about 3 dB on average than other four microphones at 1.5 m height.
  **This can be seen as the effect of the propeller wind acting in a downward direction.**" —
  another instance of mic position relative to the rotor's flow field (here, height above the
  hovering drone) producing a several-dB, flow-driven (not acoustic) offset.

---

## Answers to the thread questions

**Q1 — does non-uniform/turbulent inflow raise the BPF tone and harmonics and change their
directivity?** Yes, repeatedly and with numbers, across two independent literatures that never
cite each other: the UAS-recirculation literature (Stephenson 2019 p.1153–1155; Weitsman 2020
p.1327–1329,1335; Nardari 2019 p.1,6,11,16; Ma 2024 p.313–314,317) and the much older static
duct-fan "inflow control device" literature (Hanson 1977 p.1,12–13,24–25; Hodder 1977
p.1,3,7,9; Woodward et al. 1978 p.2,12; Woodward & Glaser 1980 PDF p.5; Homyak et al. 1983
p.5–7). The consistent pattern: **the fundamental BPF tone itself changes little or not at all**
(Stephenson p.1154: "the first harmonic ... is relatively unaffected"; Nardari p.11: "the first
two BPF tones are almost unaffected"; Ma p.317: "tonal noise levels remain largely unaffected");
**the second and higher harmonics rise sharply** (Stephenson p.1154: 2nd harmonic +~30 dB, 3rd
+>15 dB; Weitsman p.1327/1329: first three harmonics +~20 dB; Nardari p.11: 3rd+ harmonics +5–10
dB, up to +9 dB on-axis; Woodward et al. 1978 p.12: BPF −10 dB at some angles with an ICD
in place). Direction: every isolated-rotor recirculation study that reports a direction finds
the effect **larger out of the rotor plane than in it** (Stephenson p.1154, Weitsman p.1329,
Ma p.317) — the opposite of where our arc-validation mics sit (in the rotor plane), which is a
reason the effect might be *weaker*, not absent, in our data. **Important limitation for this
thread specifically: none of these sources sweep azimuth.** Every recirculation paper's array
is an elevation line at one fixed azimuth (explicitly justified by an assumed symmetry —
Stephenson/Weitsman p.1153/1326: "An azimuthal array was not employed as the acoustic emissions
of an isolated rotor in hover should be symmetric"; Nardari p.9 bakes the same assumption into
its analysis method: "assuming an axisymmetric acoustic field"; Ma p.317's array is "in a
vertical plane"). So this body of evidence establishes the *mechanism* (turbulent/non-uniform
inflow → higher BPF harmonics, out-of-plane-biased) beyond doubt, but it does not itself contain
a positive or negative test of *azimuthal* non-uniformity — for that, see Q2. One source that
*does* sweep azimuth, Zawodny & Boyd 2017 (p.6), agrees on the harmonic-order signature from the
opposite direction: at the closest rotor-to-obstruction spacing tested, BPF harmonics 2–7 reached
or exceeded the fundamental's own amplitude at the worst-placed microphone, while the fundamental
tone itself was comparatively unremarkable — the same "harmonics move, fundamental doesn't move
much" pattern as the recirculation literature, but here driven by a fixed structure, not
turbulence.

**Q1a — a diameters-of-clearance summary, since several sources give one.** For a support/duct
structure near a rotor/fan to stop mattering, the numbers found here span a fairly narrow range
once "diameters" and "radii" are put on the same footing: Zawodny & Boyd 2017 (p.6) found level
differences of ~8–10 dB at 0.1–0.2 rotor **radii** of tip clearance, falling to "nearly identical
to ... an isolated rotor" by 0.4 R; Fasulo 2025 (p.18) ruled recirculation out (not the same
question, but the same spirit of "far enough to not matter") at 6 D (=12 R) floor clearance and
>12 D (=24 R) wall clearance; Homyak et al. 1983 (p.5) kept a whole engine installation 3.4
fan-diameters (6.8 R) from any structure and still saw a possible residual ground-plane
contribution (p.6: "may be caused by the ground plane (although the engine centerline is 5-1/2
engine fan diameters [11 R] from the ground)"); Hodder 1977 (p.3) used 5.1 diameters (10.2 R)
forward of the test-stand struts. **None of these numbers were derived for a 6-inch, two-blade
propeller on a benchtop thrust stand at arc-radius order 1 m** (≈13 R for a 0.152 m-diameter
prop), so they should be read as order-of-magnitude precedent, not a validated threshold for our
rig — but they do establish that clearances well under ~10 R are where these effects are
reported, and our own rig geometry (arc radius, stand-to-prop distance) is, per PROTOCOL.md,
"not recorded anywhere," which is itself the first thing to fix before this question can be
answered quantitatively for our setup.

**Q2 — does an asymmetric obstacle/support near a hovering rotor make the tonal directivity
azimuthally asymmetric?** Yes, and this is answered directly, not just by analogy. Hanson 1977
is a controlled experiment built for exactly this question: a fixed support structure behind a
static fan's inlet produced inflow distortion "**roughly an equal contributor**" to atmospheric
turbulence, concentrated at one circumferential location ("**acts mainly at the bottom of the
inlet**", p.1) with the unsteady part **"2 to 3 times stronger at the bottom than at the top"**
(p.24) — and a deliberate blockage-plate control experiment showed the resulting far-field tone
directivity is "**not symmetric with respect to the fan axis of rotation**", localized to the
obstruction's own azimuth, to the point that measurements taken with the plate at one azimuth
and the natural support at another "**could not be related**" (p.21). Homyak et al. 1983 (p.6)
give the acoustic-theory reason: a stationary structure of N elements (6 struts, in their case)
interacting with B rotor blades locks a specific Tyler–Sofrin spinning-mode order that shows up
as a fixed, repeatable "**lobe**" at a specific angle ("this lobe has been observed in many
previous tests with this engine"), and Woodward & Glaser 1980 show that suppressing broadband
turbulence *reveals* rather than removes such a lobe. Fasulo 2025 — using the **same Tyto
Robotics 1585 stand as our own rig** — measured this directly on a small drone propeller: its
support pylon, offset to one side of an otherwise symmetric mic array, produced a "**small but
significant mounting asymmetry**" (p.10) and, when isolated by reversing rotation sense, "**can
shift directivity by up to 4 dB**" (p.24), rising to azimuthal scatter of "**about 3 dB at 6000
rpm and 3–4 dB in the 7000–8000 rpm range**" between mirrored mics (p.11) — the same order of
magnitude as several of the ±36°/±54° discrepancies in our own data. Zawodny & Boyd 2017
(p.2,6,16), with a microphone array purpose-built with real elevation *and* azimuthal sub-arrays
(not just an elevation arc, unlike almost everything else in this set), measured the same effect
directly on a simple carbon-fibre tube standing in for a multicopter arm near a small rotor:
"cases of prominent rotor-airframe interaction noise were found to be **highly directive as a
function of observer azimuth**" (p.16), with harmonics 2–7 reaching or exceeding the fundamental
at the worst azimuth (p.6) and the effect vanishing by ~0.4 rotor radii of clearance — and,
usefully, it locates the loudest azimuth **broadside to the obstruction, not toward it** ("M5 is
oriented normal to the centerplane of the rod" was louder than "M3 ... coplanar with the rod",
p.6), i.e. the induced tone behaves like a small dipole antenna hung off the obstruction rather
than a simple "shadow on the near side" — a detail worth having in hand before assuming *which*
azimuth an off-centre stand element should light up if it is the cause of our own pattern.
Jawahar 2025 (p.7,9) shows
the same recirculation-from-a-nearby-surface mechanism for a ground plane, but that geometry is
axisymmetric about the rotor axis, so it corroborates the mechanism (surface proximity → higher
harmonics) without itself producing azimuthal asymmetry.

**Q3 — time scales.** Quoted exactly: Stephenson 2019 (p.1153–1155): ramp to steady RPM at
2–4 s; BPF appears ~3.5 s; **"the onset of flow recirculation occurred within 5 s of reaching
steady state RPM"** (≈7.5 s total), "heavily dependent on the size of the facility, size of the
rotor, and the thrust." Weitsman 2020 (p.1327,1335): clean window **3.5–7.4 s (3.9 s duration)**
at baseline, extended to **"approximately 10 s"** with two downstream meshes; "this duration is
highly dependent upon the room geometry, operational thrust condition, and size of the rotor."
Ma 2024 (p.313,317): a much larger chamber (~8–12× the SHAC's volume) and a free-flying
multirotor instead: recirculation "**forms around 30 s**" and even then only weakly perturbs
tonal levels — explicitly attributed to the bigger room, not a contradiction of the small-room
result. Gallo 2025 (p.7), in a small (~11 m³) but **vented** room, saw **no** recirculation rise
in a 30 s record at all, and could not rule out that "the time needed to establish the
recirculation is comparable to the time it takes for the RPM to stabilize." **Implication for
our captures (2.0 s per PWM step, five steps back-to-back):** a single isolated 2.0 s capture
starting from a cold, settled room would very likely fall *inside* Stephenson/Weitsman's
"clean" 3.5–7.4 s window and therefore show little recirculation contamination — **but our five
PWM steps run back-to-back on the same spin-up**, not from a fresh air-settled start each time,
so by steps 3–5 (which is where 1900/2000 PWM — closest to the BPF≈240 Hz band being examined —
sit) more than 5–7 s have elapsed since the motor first started turning at step 1. None of the
sources give a model for whether recirculation "restarts" or accumulates across a changing
thrust ramp rather than a single constant-RPM run, and this is explicitly flagged as an open
question by Weitsman (p.1335: "a generalized method for predicting the duration prior to the
onset of recirculation for arbitrary experimental setups" is future work) — so recirculation as
the *sole* explanation cannot be ruled in or out from timing alone without knowing our own
room's venting (Gallo's vented small room saw none; Stephenson/Weitsman's sealed small room saw
it fast).

**Q4 — diagnostics that discriminate a reflection from a source asymmetry.** Four distinct,
source-quoted methods: (1) **Reversed rotation sense** (Fasulo 2025, p.11–12,24): if a
directivity asymmetry is caused by a fixed structure, reversing which way the blades sweep past
it changes the asymmetry (here, up to 4 dB, rising to 3–4 dB at high rpm) because the
shielding/interaction geometry relative to blade phase changes; a pure room reflection would not
care which way the rotor turns. (2) **Elevation/in-plane vs out-of-plane comparison plus a
time-domain check** (Stephenson 2019 p.1154, Weitsman 2020 p.1329): recirculation is a dipole
loading-noise effect, strongest out of the rotor plane and weak in it; a spectrogram that stays
flat over the whole run (no time-dependent rise) rules recirculation out regardless of position
(Fasulo 2025 p.18: "BPF harmonics remain sharp and strictly horizontal ... no progressive rise
... rule out significant wake recirculation"; Gallo 2025 p.7 used the identical test). (3)
**Known-source substitution** (Whelchel 2023 p.65–66): replace the rotor with a calibrated
omnidirectional loudspeaker and measure the fixture/room response with and without the
suspected reflector present; whatever pattern the loudspeaker also shows is the room, not the
rotor. Nardari 2019 (p.3 of the earlier chamber-problems notes, not independently re-verified in
this thread's dump) used a related loudspeaker check but for microphone-position error
calibration, not for separating room from source. (4) **Harmonic-order signature**: nearly
every source agrees the fundamental BPF tone is comparatively insensitive while 2nd/3rd+
harmonics rise sharply under inflow disturbance (Stephenson, Weitsman, Nardari, Woodward et al.
— see Q1); a discrepancy concentrated in the fundamental alone, with harmonics flat, would argue
against an inflow-distortion mechanism and toward a room resonance/interference explanation
instead (this is exactly the diagnostic direction the arc-validation one-pager already uses at
3150 Hz vs 200–250 Hz, though from the room side, not the rotor side).

**Q5 — pseudo-noise / bias for microphones near a static rotor, and minimum distance.** Direct
evidence exists only for microphones in the **downwash/wake** (axially below or behind the
rotor), not for microphones **in the rotor's disk plane** (radially, 90° from the axis) where
our arc mics sit: Alkmim 2022 (p.2736,2742) needed a windscreen on the one mic directly beneath
the propellers and still found "the −70° direction has much higher levels ... attributed to the
downward airflow across the microphone diaphragm" at an array radius of ≈7 rotor radii; Hochbaum
2026 (p.3,5,9) found that even with custom windscreens, mics below free-flying drones were
"frequently affected by wind-induced low-frequency noise" badly enough that "no valid
measurements were obtained below the UAV" at all, at a usable-flight-volume scale several metres
across; Kim 2022 found a smaller, few-dB downward-flow bias at mics 2.4 m above a hovering drone.
**No retrieved source gives a quantitative minimum-distance-in-rotor-radii recommendation for
in-plane (radial) microphones specifically** — Alkmim's ≈7R array radius and Weitsman/Zawodny's
"far-field" threshold of >12R (Weitsman 2020, Methods, not independently re-quoted above but
consistent with the earlier chamber-problems note) are the closest analogues, and both are
axial/elevation-array radii, not validated for a rotor-plane azimuthal arc. This is a genuine
gap: it means we cannot rule out, from the literature alone, some level of flow-induced
pseudo-noise on the in-plane mics closest to the propeller tip, but we also have no source
saying it should look like the ±36°/±54° pattern (asymmetric, opposite-signed on the two arc
halves) rather than a symmetric wind hiss.

---

## Comparison with earlier notes

Every held paper above was compared against `papers/chamber-problems/EXTRACTS-local.md` (and,
for Jawahar, `EXTRACTS-downloaded.md`) after being re-extracted and re-read independently. There
is **no numerical or attribution error** found in the earlier notes for any of the quotes this
thread relies on — every dB figure, second-count and page number this thread double-checked
(Stephenson's 15/30 dB and 3.5/7.5 s; Weitsman's 3.9/10 s and ~20 dB; Nardari's 5 dBA/9 dB and
"axisymmetric acoustic field"; Ma's 30 s and "no prominent directivity"; Fasulo's Tyto-1585
identification, pylon offset, 4 dB rotation-reversal shift, 6.5 dB plate asymmetry, 12D/6D
recirculation ruling-out; Zawodny & Haskin's LSAWT-vs-SALT agreement; Gallo's "no rise... small
size of the room"; Alkmim's windscreen and −70° note; Hochbaum's rejected-block criterion)
agrees with the earlier note. Two minor, non-substantive discrepancies surfaced only in **page
numbers**, both resolved in favour of the earlier note after direct `pdftotext -f N -l N`
verification against the source PDF:
- Jawahar's "TSSPL by approximately 4.0–8.0 dB" quote: this thread's first-pass line-count
  heuristic suggested p.8; direct page-by-page extraction confirms **p.9**, matching
  `EXTRACTS-downloaded.md`.
- No other page mismatches were found; Hochbaum's page numbers in this file were themselves
  corrected mid-research (see note under that entry) using the same direct-verification method,
  independently of the earlier notes (which do not cite Hochbaum's specific pages for the same
  passages).

What this thread adds beyond the earlier notes (new content, not corrections, since the earlier
notes were written for different threads with different questions in mind): Fasulo's exact
CW/CCW magnitude progression (1 dB at 3000–5000 rpm → 3 dB at 6000 → 3–4 dB at 7000–8000) and
its <0.6 dB blade-to-blade repeatability baseline; Nardari's explicit "assuming an axisymmetric
acoustic field" methodological admission; and the entire new-source set (Hanson 1977, Hodder
1977, Woodward et al. 1978, Woodward & Glaser 1980, Homyak et al. 1983), none of which appear in
any existing `papers/*/EXTRACTS*.md` or `MATRIX-3W.md` file in this repository.
