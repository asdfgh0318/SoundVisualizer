# Thread G — change the measurement, not the room

Reference-source corrections, two-distance methods, rotating the source, near-field and arrays.
Compiled 2026-09-08. All quotes verified against a fresh plain `pdftotext -q` dump of the PDF
actually opened (dumps in `papers/arc-validation/refetch-txt/` for held papers re-read, and
`papers/arc-validation/txt/` for newly downloaded sources). Held-paper identity was confirmed
against BIBLIOGRAPHY.md via `pdfinfo` + page 1 before quoting; see per-source notes below.

---

## 1. Payne & Simmons 1996, NPL Report CIRA(EXT) 009

- **File**: `papers/anechoic-simulation/Payne-Simmons_1996_NPL-CIRA009_environmental-correction-K2.pdf`
- **Identity confirmed**: page 1 prints "CIRA(EXT) 009 / April 1996 / R C Payne and D J Simmons / Centre for Ionising Radiation and Acoustics / National Physical Laboratory". Matches BIBLIOGRAPHY.md (title itself is OCR-garbled on the scan, authors/report number are not).
- **Evidence level**: III — report (national metrology lab), five-room controlled comparison with a calibrated RSS, outdoor cross-check.
- **What it says (Q1)**: This is the primary source for how K2 is derived by each ISO method and what residual/uncertainty results. Four methods compared in five rooms (hemi-anechoic → semi-reverberant): absolute (RSS substitution), reverberation-time, two-surface, estimated-absorption. Absolute method is the only consistently accurate one; two-surface under-predicts K2A, worst near obstacles; reverberation over-predicts, best when RT(A) > 1 s. K2 is always a **single scalar per room/configuration**, derived from the *spatially averaged* Lp over 10 (ISO 3744) or 4 (ISO 3746) key microphone positions — no per-position breakdown of K2 itself is reported anywhere in the results tables, only the source-position dependence of the single K2A value (§5.5).

**Verbatim quotes** (page = printed PDF page):

> "It is concluded that the absolute method using a reference sound source is the only method that will consistently provide an accurate assessment of K2A." (Abstract, p. i / unnumbered)

> "The environmental correction, K2, is given by: K2 = Lwr − Lw ...(2) where Lwr is the calibrated sound power level of the reference sound source. In the case of the reference sound source used in this study, Lwr was taken to be 90.9 dB re 1 pW." (§2.2, p. 3)

> "This method is only applicable to rooms whose length and width are each less than three times the ceiling height. Here the sound power level determined from measurements using a surface of area S is compared with the sound power level determined from measurements using a geometrically similar surface, symmetrical with respect to the machine under test, with a larger surface area, S2. ... the ratio S2/S should be at least 2, and preferably greater than 4." (§2.4 Two Surface Method, p. 4)

> "S/A = (1 − M.S/S2) / (4(M − 1)) ...(6) ... M = 10^(0.1(Lp1−Lp2)) ...(7) where Lp1 is the average sound pressure level on S, and Lp2 is the average sound pressure level on S2." (§2.4, p. 4)

> "It can be seen that measured sound power levels range from 90.8 dB to 98.4 dB, a potential range of K2A-factors of 7.6 dB" (§5.1, p. 15)

> "the variation of sound power level with measurement surface for room A indicates that the room cannot be regarded as hemi-anechoic at the larger measurement distances (the room only satisfies ISO 6926 up to a maximum 1.5 m radius). The measurements were repeated on a large outdoor hemi-anechoic site where the sound power level measured using surface 4 was found to be only 0.2 dB greater than that measured using surface 2." (§5.1, p. 15–16)

> Room A absolute-method K2A by surface: "a[0] / 0.6 / 1 / 1.1" dB for surfaces 1–4 (Table 10, p. 20).

> "the value of the K2A-factor has increased (cf Tables 12 and 13), consistent with reflections from the nearby walls elevating the measured sound power level... It is concluded therefore that as K2A is clearly dependent on the position of the noise source relative to the walls neither of these two methods of K2A determination should be used in the above situations." (§5.5 Effect of Source Position in Room, p. 21–22) — this is a source-*position* sensitivity study of the single scalar K2A, not a decomposition of K2 by measurement direction.

> Theoretical model: "K2 = 10.log[1 + 4(r/R)² − ((1/α) − 1)]" where r is the measurement-surface radius and R the enclosing spherical boundary radius (§3, p. 6). The text's own worked numeric example is internally inconsistent about which α pairs with which case — it first states "for a room with highly absorbent walls (α = 0.9)... small [K2 change]... For a room with reflective walls (α = 0.1) the K2-factor depends critically on the measurement distance," then immediately gives "for approximately hemi-anechoic conditions (α = 0.1) ... 0.3 dB [change]; the corresponding change for semi-reverberant conditions (α = 0.9) is approximately 5 dB" (p. 6) — the α labels are swapped between the two sentences (very likely an OCR/scan artefact in this heavily garbled 1996 document, e.g. "referencesound", "K2Aand" throughout); quoted verbatim, not corrected, and not relied on for any number in the Answers section below.

- **Per-direction correction discussed?** No. K2 (and K2A) are always the single scalar per configuration; the only "spatial" dimension examined is *source* position relative to walls (§5.5), not decomposition of the correction across microphone directions.

---

## 2. Simmons, Jobling & Payne 2004, NPL Report DQL-AC 007

- **File**: `papers/chamber-problems/Simmons-Jobling-Payne_2004_NPL-DQL-AC007_hemi-anechoic-sound-power-uncertainties.pdf`
- **Identity confirmed**: page 1 "NPL REPORT DQL-AC 007 / Acoustic parameters and uncertainties associated with determining sound power level in hemi-anechoic rooms / Dan Simmons, Barry Jobling, Richard Payne / August 2004". Matches BIBLIOGRAPHY.md.
- **Evidence level**: III — report, 11-state controlled wedge-removal experiment in an NPL hemi-anechoic chamber, RSS-based.
- **What it says (Q1)**: Gives the ISO 3744 K2 definition verbatim (identical wording to ISO 3744:2010/ISO 26101-2:2024, source #3 and #8 below — cross-confirms this definition has been stable ISO wording since at least 2004). Shows K2A rising from ~1.3 dB to 7.2 dB once about half the absorbent wedges are removed, and that correcting sound-power data with the RSS-derived K2 collapses the uncertainty caused by a degraded room by roughly an order of magnitude.

**Verbatim quotes**:

> "Environmental correction factor (K2) ... Expressed in decibels, this is a frequency dependent correction term applied to the mean (energy-average) of the time-averaged sound pressure levels at all the microphone positions on the measurement surface, to account for the influence of reflected or absorbed sound." (§2.2.2, p. 4)

> "It was observed that the change in K2 was relatively insignificant up to the point where around half of the absorbing wedges had been removed. Following this halfway stage, K2A increased from 1.3 dB to 7.2 dB." (§5, Summary & Conclusions, p. 51)

> "The values of ∆Lmax listed in Tables 12, 13 and 14 for the RSS are actually values of K2 and when used to correct the sound power levels of the drill and the box source it can be seen that the values of ∆Lmax are greatly reduced. ... for the ISO 3745:2003 procedure reducing from 6.4 dB and 7.3 dB to 0.8 dB and 0.1 dB." (§4.4.2.4, p. 49)

> "Clearly, the use of a RSS in a sound power level determination provides a much more reliable result, even when measurements are carried out in rooms that are clearly not hemi-anechoic." (§4.4.2.4, p. 49; repeated verbatim in §5 Summary & Conclusions, p. 52)

> "The possibility of defining a value of K2 that must not be exceeded in order that a room may be considered as hemi-anechoic is dependent on the level of measurement uncertainty that is acceptable for a particular application. ISO 3745 is considered to be a precision grade standard and so quotes an A-weighted reproducibility uncertainty of 0.5 dB and so the value of K2 should certainly be less than this value." (§4.4.2.4, p. 49)

- **Per-direction correction discussed?** No — the K2 definition quoted above (p. 4) is explicit that it is a mean over *all* microphone positions; the report tabulates K2/K2A per one-third-octave frequency band and per room state (Table 8), never per microphone position/direction. No two-surface-method use in this report (only the absolute/RSS method, per §2.4 "Reference Sound Source (RSS)").

---

## 3. ISO 26101-2:2024 (held, iTeh preview sample)

- **File**: `papers/reflection-localization/ISO-26101-2_2024_standard-preview_environmental-correction.pdf`
- **Identity confirmed**: "ISO 26101-2 / Acoustics — Test methods for the qualification of the acoustic environment — / First edition 2024-06 / Part 2: Determination of the environmental correction". Matches BIBLIOGRAPHY.md. Content confirmed to run only Foreword–Clause 5.1 (ends mid-page-4, "5.1 General... preferred method... ISO 3744:2024, Annex A."); Clauses 5.2 onward (including 6.3 Two-surface method, which the ToC lists) are **not** in this preview.
- **Evidence level**: VII — standard (preview sample only).
- **What it says (Q1)**: Gives the current (2024) definitive wording for K2 and confirms the two-surface method now lives in ISO 26101-2 Clause 6.3 rather than in ISO 3744 Annex A (that move happened between the 2010 and 2024 ISO 3744 editions), with Clause 5 "Absolute comparison test" pointing at "ISO 3744:2024, Annex A" for the RSS method specifically.

**Verbatim quotes**:

> "3.3 environmental correction / K2 / correction applied to the mean (energy average) sound pressure levels over all the microphone positions on the measurement surface (3.2), to account for the influence of reflected or absorbed sound ... Note 3 to entry: In general, the environmental correction depends on the area of the measurement surface and usually K2 increases with S." (§3.3, p. 2)

> "4.2 Absolute comparison test / The absolute comparison test (see Clause 5) is carried out with a reference sound source (RSS) and may be used outdoors and indoors. This is the preferred procedure for qualifying a test environment according to ISO 3744, particularly if data in frequency bands are required... This method is expected to yield the most accurate results in typical industrial environments." (§4.2, p. 3)

> "4.3 Methods based on room absorption / The methods based on room absorption (see Clause 6) require the determination of the equivalent absorption area, A, of the test room and can be less accurate than the absolute comparison test in typical industrial environments. These tests are based on the assumption that the room has approximately a cubic shape, is substantially empty, and that sound is absorbed at the room boundaries only. Three methods are specified in which A is calculated either from measurements of reverberation time (see 6.2), from measurements of sound pressure levels from the noise source under test using a secondary measurement surface (see 6.3) or from measurements on a reference sound source (see 6.4)." (§4.3, p. 3)

> "5.1 General / This method represents the preferred method to determine the environmental correction according to ISO 3744:2024, Annex A." (§5.1, p. 4)

- **Per-direction correction discussed?** No — same "mean ... over all the microphone positions" wording as sources #2 and #8. No per-direction procedure appears anywhere in the retrieved sample (Clauses 2–4, 5.1 only).

---

## 4. González & Kob 2026, DAGA Dresden

- **File**: `papers/anechoic-simulation/Gonzalez-Kob_2026_DAGA_room-acoustics-loudspeaker-directivity.pdf`
- **Identity confirmed**: "DOI: 10.71568/daga2026.688 / DAGA 2026 Dresden / Influence of room acoustics on directivity measurement of loudspeakers / Rubén González, Malte Kob". Matches BIBLIOGRAPHY.md. Whole 4-page paper read (no preview truncation).
- **Evidence level**: III — peer-reviewed conference paper, four-room comparison against an anechoic 5°-resolution reference.
- **What it says (Q3)**: Directly answers the "rotate the source instead of the microphones" question for the loudspeaker case: a Neumann KH120A on a Stage Banner 10AT turntable, following AES56-2008, in four rooms from anechoic to reverberant. AES56-2008 "does not specify the room acoustic conditions" for the same rotate-the-source procedure, so room-induced error is measured directly by comparing turntable results across rooms of known RT/volume.

**Verbatim quotes**:

> "This study evaluates the effect of the reverberant field and reflections in four different rooms on swept sine measurements for directivity acquisition of two high-end loudspeakers following the AES56-2008 procedure" (Abstract, p. 1220)

> "For loudspeaker directivity measurements using polar representations, the AES 56-2008 standard [1] defines the requirements necessary to ensure data accuracy and measurement repeatability. However, this standard does not specify the room acoustic conditions for measurements performed at typical angular resolution (5 · 5°)." (Introduction, p. 1220)

> "In the reverberant hall and laboratory at ETI, significant differences in sound pressure levels are observed, particularly for frequencies of 1 kHz and above, within the MA range from 150° to 180°." (Results and Analysis, p. 1221)

> "The most pronounced amplitude variations occur around 90 Hz, which is attributed to the alignment of the measurement axis with a node of an excited room mode." ... "At frequencies above 1 kHz some comb filtering effect appears due to the very early reflections arriving from the table and other nearby surfaces as seen in Figure 1." (p. 1221)

> "In the ETI laboratory, pressure level reductions of up to 18 dB occur at specific frequencies." (Discussion, p. 1223)

> "Several additional factors beyond critical distance influence loudspeaker directivity measurements at standard angular resolution. These include reflections from the turntable, early reflections from walls, ambient noise, and the orientation of the measurement axis relative to the room geometry." (Discussion, p. 1223)

> "Despite differences in size between the anechoic rooms at KIO and ETI, the directivity representations of the Neumann KH120A loudspeaker shown in Figure 3 are highly consistent across all frequency bands. This suggests that, for loudspeaker directivity measurements, a room treated with sound absorbing materials such as rock wool is sufficiently effective at attenuating reflections and minimizing image sources" (Discussion, p. 1223)

**Note**: rotating the source on a turntable does not by itself remove room error — the paper's whole point is that the *same* turntable procedure gives different polars in different rooms, because the turntable itself and nearby surfaces still reflect. It converts "room error smeared across a moving microphone position" into "room error fixed at whatever microphone position(s) are used," which is exactly the mechanism Q3 asks about, but with the caveat that the turntable/mount is itself a new reflector at close range.

---

## 5. ISO 5305:2024 (held, iTeh preview sample)

- **File**: `papers/anechoic-simulation/ISO-5305_2024_standard-preview_UAS-noise-measurement.pdf`
- **Identity confirmed**: "ISO 5305 / Noise measurements for UAS (unmanned aircraft systems) / First edition 2024-01". Matches BIBLIOGRAPHY.md. Content confirmed to run Foreword through §7.3.1 only (file ends mid-clause 7.3.1, page 8); **Annexes B (Numerical examination of the acoustic far-field condition) and C (Measurement of far-field condition for a UAS propeller noise) are listed in the ToC (pp. 34, 38) but their text is not in this preview** — confirms the thread brief's assumption.
- **Evidence level**: VII — standard (preview sample).
- **What it says (Q4)**: Gives the explicit far-field distance rule in UAS/vehicle diameters, and — importantly for Q1 — shows that room *qualification* (as opposed to the K2 correction itself) already requires checking the inverse-square-law deviation at **every** source position and measurement direction used, with a fixed dB tolerance per band.

**Verbatim quotes**:

> "3.17 UAS diameter / DA / unmanned aircraft system diameter / diameter of the smallest cylinder that encompasses the projection shape of the unmanned aircraft system (UAS) (3.16) on a plane" (§3.17, p. 4) — distinct from "3.19 propeller diameter / DR / diameter of each propeller employed for the multi-propeller powered unmanned aircraft system" (p. 4). **DA is the whole-vehicle diameter, not the single-propeller diameter** — relevant because SoundVisualizer's test article is a bare propeller on a stand, not a multirotor airframe, so this formula's DA does not map directly onto our DR-scale geometry.

> "For UAS noise measurements, to ensure the acoustic far-field condition, the microphone distance R shall be at least 5DA, i.e. R ≥ 5DA (1)" (§6.2, p. 5)

> "For sound at a high frequency, the significant interference pattern can affect the validity of the far-field condition proposed in Formula (1). However, the effect can be minimized when summing in a frequency band, for example, a 1/3-octave band, is performed." (§6.2, p. 5)

> "The validity of the inverse square law defined in ISO 26101-1 shall be ensured for all source positions and measurement directions specified in this document. The maximum allowed deviation from the inverse square law in any of the measured directions for any of the microphone positions shall not exceed the values given in Table 1." (§7.2.2, p. 7) — Table 1: ±1.5 dB (125–630 Hz), ±1.0 dB (800–5000 Hz), ±1.5 dB (≥6300 Hz).

- **Per-direction correction discussed (Q1 cross-reference)?** Not a per-direction *correction*, but a per-direction/per-position *qualification pass-fail test*: the same tolerance must hold "for all source positions and measurement directions" (§7.2.2), i.e. the room must be shown good enough everywhere it will be used, even though the scalar K2/K2f correction that gets applied afterwards (per ISO 3744/26101-2) remains a single spatial average.

---

## 6. Fasulo et al. 2025, Aerospace (MDPI) 12:647

- **File**: `papers/chamber-problems/Fasulo_2025_Aerospace_rotor-noise-directivity-decay.pdf`
- **Identity confirmed**: "Experimental Acoustic Investigation of Rotor Noise Directivity and Decay in Multiple Configurations / Giovanni Fasulo, Giosuè Longobardo, Fabrizio De Gregorio and Mattia Barbarino". Matches BIBLIOGRAPHY.md. Uses the same **Tyto Robotics 1585 stand** as SoundVisualizer.
- **Evidence level**: III — peer-reviewed journal, controlled distance sweep with 10 calibrated 1/2″ mics from L/D≈0.9 to 10.4.
- **What it says (Q4)**: Gives explicit near/far-field decay-rate numbers in propeller diameters D (=230 mm) for a small two-blade rotor on the same stand type SoundVisualizer uses.

**Verbatim quotes**:

> "For L < 2D, the level falls by about 17 dB per distance doubling, indicating that the field is still dominated by the reactive component. Beyond L = 3D, however, the measurements adhere closely to the far-field decay law, exhibiting a reduction on the order of 6 dB per distance doubling. Specifically, the observed mean attenuation across all tested rotational speeds is marginally less than 6 dB, consistent with the influence of ground reflections. Superimposed on this trend, pronounced oscillations appear, most evident at 7000 and 8000 rpm. These fluctuations originate from constructive and destructive interference between the direct acoustic wave and its ground-reflected counterpart, yielding frequency- and range-dependent local sound pressure minima and maxima." (p. 15)

> "In the near field (L < 2D), the decay rate is steep, approximately 17 dB per doubling of distance. Beyond roughly L = 3D, however, the decay relaxes to nearly the far-field value of 6 dB per doubling, although slightly elevated (between 6 and 8 dB)." (p. 16, BPF-1 harmonic)

> "The array radius was set to eight propeller diameters (1840 mm) from the hub or plate centre." (§2.3, p. 6) — the directivity-arc setup (setup #1) itself is run at 8D, i.e. comfortably beyond the paper's own 3D far-field threshold.

> "a near-field decay of approximately 17 dB per distance doubling that relaxed to the classical 6 dB law beyond three diameters. Reversing the sense of rotation revealed that even modest geometric asymmetries, here the support pylon, can shift directivity by up to 4 dB." (Conclusions, p. 24)

- **Bearing on Q1/error-averaging**: not a K2-style correction, but confirms that even at 8D (comfortably "far field" by this paper's own 3D threshold and by ISO 5305's 5DA-type rule), ground/support reflections still add ripples on top of the 6 dB/doubling law — i.e. going further out is necessary but not sufficient to erase reflection error.

---

## 7. Schmal, Herrin & Fernández Comesaña, "Acoustic Characterization of a Quadcopter Using a Test Stand" (held, venue/year not printed)

- **File**: `papers/anechoic-simulation/Schmal_nd_conf_acoustic-characterization-quadcopter-test-stand.pdf`
- **Identity confirmed**: page 1 "Acoustic Characterization of a Quadcopter Using a Test Stand / Session: Experimental Acoustic and Flow Measurements / Jared Schmal, University of Kentucky... D. W. Herrin... Daniel Fernández Comesaña, Microflown Technologies". Matches BIBLIOGRAPHY.md; venue/year genuinely not printed anywhere in the 13-page text (re-checked).
- **Evidence level**: VI — conference paper, single-facility characterisation (hemi-anechoic, University of Kentucky), draw-away PU-probe measurements.
- **What it says (Q4, the "kr" form)**: Gives the far-field threshold in **wavenumber × distance (kd)**, i.e. exactly the kr-style non-dimensional criterion the thread brief asks for (their "d" is measurement distance from the source, not propeller diameter — confirmed from the running text, see quote).

**Verbatim quote**:

> "Draw away measurements were used to calculate decay rates and are plotted against the wave number multiplied by the distance from the source (kd), enabling an analysis of the results in terms of acoustic wavelength. ... Velocity and pressure converge to approximately the same rate once the far-field is reached at kd equals 1.8, with the exception of an increase in sound pressure when kd equals 7.3. This increase is likely due to issues with approaching the edges of the anechoic chamber." (§4, p. 7)

---

## 8. ISO 3744:2010 [new download]

- **File**: `papers/arc-validation/ISO-3744_2010_standard-preview_two-surface-absolute-comparison.pdf`
- **Route**: `https://cdn.standards.iteh.ai/samples/52055/dc2f473b243a423683f769c42dbba984/ISO-3744-2010.pdf` (found via web search of the iTeh CDN sample host per the thread brief; `file` confirms "PDF document, version 1.4, 15 page(s)"; `pdfinfo`/page 1 confirm "ISO 3744 / Third edition / 2010-10-01").
- **Evidence level**: VII — standard (preview sample).
- **Coverage actually retrieved**: Front matter, Scope/Introduction, Clauses 1–3 (Terms and definitions) in full, and Clause 4 (Test environment) through §4.2.3 — the file **ends at page 9, mid-Clause-4**. **Annex A "Qualification procedures for the acoustic environment" (p. 32) — where the actual two-surface-method and absolute-comparison-method formulas live in the 2010 edition — is listed in the Table of Contents (line "Annex A (normative) Qualification procedures for the acoustic environment ... 32") but its text is NOT reachable in this preview; "Annex A" appears exactly once in the whole 958-line extracted dump, in the ToC.** This directly could not be improved on: it is the same preview iTeh serves; no alternate free route was found (see RETRIEVAL-G.md).
- **What it says (Q1)**: Gives the identical K2 definition found in the two NPL reports and ISO 26101-2:2024, confirming the "mean over all microphone positions" wording has been stable ISO text since at least this 2010 edition, and states the two available test environments.

**Verbatim quotes**:

> "3.17 environmental correction / K2 / correction applied to the mean (energy average) of the time-averaged sound pressure levels over all the microphone positions on the measurement surface, to account for the influence of reflected or absorbed sound ... NOTE 3 In general, the environmental correction depends on the area of the measurement surface and usually K2 increases with S." (§3.17, p. 5)

> "3.16 K1 / correction applied to the mean (energy average) of the time-averaged sound pressure levels over all the microphone positions on the measurement surface, to account for the influence of background noise" (§3.16, p. 5) — background-noise correction K1 uses the identical "mean over all positions" construction as K2.

> "The test environments that are applicable for measurements in accordance with this International Standard are: a) a laboratory room or a flat outdoor area which is adequately isolated from background noise ... and which provides an acoustic free field over a reflecting plane; b) a room or a flat outdoor area which is adequately isolated from background noise ... and in which an environmental correction can be applied to allow for a limited contribution from the reverberant field to the sound pressures on the measurement surface." (§4.1, p. 8)

- **Per-direction correction discussed?** No — same negative finding as sources #1–3, now from a third independent document (the standard itself, at an earlier edition), which is a strong triangulation: **K2 is a scalar spatial average by definition in every version of this text family we could retrieve (2010, 2004 report quoting it, 2024 revision); no per-direction/per-microphone K2 was found anywhere.**

---

## 9. ISO 6926:2016 [new download]

- **File**: `papers/arc-validation/ISO-6926_2016_standard-preview_reference-sound-sources.pdf`
- **Route**: `https://cdn.standards.iteh.ai/samples/42873/06beb558d2184d0b95cec315cc69abfc/ISO-6926-2016.pdf`. `pdfinfo`/page 1 confirm "ISO 6926 / Third edition / 2016-01-15 / Acoustics — Requirements for the performance and calibration of reference sound sources".
- **Evidence level**: VII — standard (preview sample).
- **Coverage actually retrieved**: Front matter, Scope, Terms and definitions (Clause 3) in full, Clause 4 (reference conditions) and Clause 5 through §5.4 "Spectral characteristics" — file ends at page 5, **just before §5.5 "Directivity" (ToC page 6), so the actual numeric directivity tolerance for an RSS is not in this preview** (only the definition of the directivity index it is measured against, below).
- **What it says (Q2)**: Defines exactly what standards require of a reference sound source (stability, spectral flatness, directivity), and gives a **per-direction** directivity index formula for the RSS itself — the one place across this whole thread's held+new sources where a "correction"-like quantity (DIi) is explicitly indexed by microphone direction i, rather than averaged away.

**Verbatim quotes**:

> "This International Standard specifies the acoustical performance requirements for reference sound sources: — temporal steadiness (stability) of the sound power output; — spectral characteristics; — directivity. ... The performance requirements on directivity index can only be verified in a hemi-anechoic room (see 5.5.)" (§1 Scope, p. 1)

> "3.9 directivity index / DIi / measure of the extent to which a source radiates sound in a particular direction, relative to the mean sound radiation over the measurement surface, where for fixed microphones, the direction is from the source to the position of the microphone... Note 1 to entry: The directivity index of direction, i, is calculated from measurements in a hemi-anechoic room by the following formula: DIi = Lpi − Lp where Lpi <for fixed microphones> is the sound pressure level for each one-third-octave band at the ith microphone position on the measurement surface... Lp is the surface sound pressure level averaged over the same measurement surface" (§3.9, pp. 3–4)

> "The RSS shall produce broadband steady sound over the frequency range in which it is intended for use, but at least for one-third-octave midband frequencies between 100 Hz and 10 000 Hz. Over this frequency range, all of the one-third-octave-band sound power levels... shall be within a range of 12 dB. ... the sound power level in each one-third-octave band shall not deviate by more than 3 dB from the sound power level in the adjacent higher or lower one-third-octave band" (§5.4, p. 5)

> "A reference sound source meeting the requirements of this International Standard shall include information on the range of variation of the source of electrical or mechanical power (e.g. the line voltage) within which the sound power level in any one-third-octave band within the frequency range of interest shall not vary by more than ±0,3 dB." (§5.2, p. 5)

- **Bearing on Q1's per-direction question**: DIi is a per-direction *diagnostic index for the reference source's own uniformity*, not a per-direction *environmental correction* — it exists precisely so that the RSS used in the K2 absolute method (source #1, #2, #3, #8) can be shown to be close enough to omnidirectional that using one scalar Lwr is valid. It is the standards' own acknowledgment that a real RSS is not perfectly omnidirectional, addressed by design (a good RSS) rather than by a per-direction correction.

---

## 10. ISO 3382-1:2009 [new download]

- **File**: `papers/arc-validation/ISO-3382-1_2009_standard-preview_room-acoustic-parameters.pdf`
- **Route**: `https://cdn.standards.iteh.ai/samples/40979/b0e9f87f3d9f4df6b18f767e3439bfb6/ISO-3382-1-2009.pdf`. `pdfinfo`/page 1: "ISO 3382-1 / First edition 2009-06-15 / Acoustics — Measurement of room acoustic parameters — Part 1: Performance spaces".
- **Evidence level**: VII — standard (preview sample; covers Clause 4 Equipment in full, ends part-way into Clause 4.2.2.3).
- **What it says (Q2)**: Gives the directivity-tolerance table for an omnidirectional test source used in room acoustics measurement — directly answering "omnidirectionality limits vs frequency" — and the procedure (gliding 30° arcs, or 5° steps if no turntable) and minimum source–mic distance used to establish it.

**Verbatim quotes**:

> "4.2.1 Sound source / The sound source shall be as close to omnidirectional as possible (see Table 1)." (§4.2.1, p. 3)

> "Table 1 lists the maximum acceptable deviations from omnidirectionality when averaged over "gliding" 30° arcs in a free sound field. In case a turntable cannot be used, measurements per 5° should be performed, followed by "gliding" averages, each covering six neighbouring points. The reference value shall be determined from a 360° energetic average in the measurement plane. The minimum distance between source and microphone shall be 1,5 m during these measurements." (§4.2.1, p. 3)

> "Table 1 — Maximum deviation of directivity of source in decibels for excitation with octave bands of pink noise and measured in free field / Frequency, hertz: 125 250 500 1 000 2 000 4 000 / Maximum deviation, decibels: ±1 ±1 ±1 ±3 ±5 ±6" (Table 1, p. 3)

- **Bearing on Q2**: this is the numeric answer to "what small omnidirectional sources exist and what are their limits vs frequency" from the standards side: even the standard's own *allowance* for an "as close to omnidirectional as possible" test source grows from ±1 dB at 125–500 Hz to ±6 dB at 4 kHz — i.e. no physically realizable small source (dodecahedron or closed-box driver) is treated as omnidirectional above ~1 kHz; the standard manages this by tolerance, not by claiming better sources exist. This is consistent with, and independent confirmation of, our SoundVisualizer band of interest (200 Hz–3.15 kHz per the arc-validation error map) sitting exactly in the range where a reference source's own directivity starts to matter (±3 dB tolerance already at 1 kHz).

---

## 11. IEC 60268-21:2018 [new download]

- **File**: `papers/arc-validation/IEC-60268-21_2018_standard-preview_acoustical-output-measurements.pdf`
- **Route**: `https://cdn.standards.iteh.ai/samples/22872/facd6f9ed97e40e6b0fa8cbca5ccaf97/IEC-60268-21-2018.pdf`. `pdfinfo`/page 1: "IEC 60268-21 / Edition 1.0 2018-11 / Sound system equipment – Part 21: Acoustical (output-based) measurements".
- **Evidence level**: VII — standard (preview sample; covers front matter, Scope, Normative references, and Clauses 3–5.3 — ends mid-Clause-5. **Clause 19.5 "Corrections based on a free-field reference measurement" and Clause 20.3 "Directional far field characteristics" are listed in the ToC (pp. 34, 39) but their text is not reachable in this preview** — this is the clause that looked most promising for Q2 and could not be retrieved.)
- **What it says (Q3)**: Confirms this standard's scope explicitly covers near-and-far-field directional characteristics for loudspeakers/sound systems, and that it normatively cites both the ISO 3744/3745 sound-power family and **CTA 2034-A** (the successor branding of CEA-2034, the "Spinorama" loudspeaker measurement method) side by side — i.e. the loudspeaker-measurement world and the ISO K2/sound-power world are formally cross-linked in this one document, even though we could not reach the operative directivity clauses themselves.

**Verbatim quotes**:

> "1 Scope / This part of IEC 60268 specifies an acoustical measurement method that applies to electro-acoustical transducers and passive and active sound systems, such as loudspeakers, TV-sets, multi-media devices, personal portable audio devices, automotive sound systems and professional equipment. ... This document describes only physical measurements that assess the transfer behaviour of the DUT between an arbitrary analogue or digital input signal and the acoustical output at any point in the near and far field of the system." (§1, p. 11)

> "Directional characteristics and complex near field properties / The comprehensive evaluation of professional equipment, including directional characteristics, can be realized by considering the complex near-field properties as a supplement to the existing far-field measurement techniques." (Introduction, p. 10–11)

> Normative references list (§2, pp. 11–12) includes "ISO 3744, Acoustics – Determination of sound power levels ... Engineering methods for an essentially free field over a reflecting plane"; "ISO 3745, ... Precision methods for anechoic rooms and hemi-anechoic rooms"; "CTA 2034-A, Standard Method of Measurement for In-Home Loudspeakers, Consumer Technology Association (Formerly CEA), 02/01/2015"; "CTA 2010-B, Standard Method of Measurement for Powered Subwoofers... 11/28/2014."

---

## 12. AES56-2008 (reaffirmed 2014) [new download — abstract/front-matter only]

- **File**: `papers/arc-validation/AES56_2008_standard-preview_loudspeaker-polar-radiation.pdf`
- **Route**: `https://www.elecenghub.com/Samples/AES/155789534/AES-56-2008-(R2014)-en.pdf` (AES's own e-library is a known blocker per the campaign protocol; this third-party sample mirror served a real, if very short, preview PDF — `file` confirms "PDF document, version 1.4, 3 page(s)"; `pdfinfo` Title: "AES standard on acoustics - Sound source modeling - Loudspeaker polar radiation measurements").
- **Evidence level**: VII — standard, but **only the front matter and Abstract are in this 3-page preview; every operative clause (measurement geometry, resolution, reporting format) is paywalled and not retrieved.** Every AES56 claim in this file (and relayed into the Answers section) is therefore abstract-level by the nature of what was retrievable, not by choice — flagged accordingly.
- **What it says**: The one-paragraph Abstract, verbatim, is all the technical content available:

> "This standard describes how the measurements of loudspeaker polar radiation data shall be made and documented. This acquired data is suitable for application in room acoustic, electro-acoustic, and sound system predictions, and loudspeaker data sheets." (Abstract, unnumbered page 3)

> Cover page: "This is a preview. Click here to purchase the full publication." (pp. 1, 3) — confirms no more content exists at this route.

---

## 13. Schatzman & Malpica 2019, Vertical Flight Society 75th Annual Forum (NASA NTRS 20190025111)

- **File**: `papers/arc-validation/Schatzman-Malpica_2019_VFS-Forum_tiltrotor-test-rig-shaft-angle-sweep.pdf`
- **Route**: `https://ntrs.nasa.gov/api/citations/20190025111/downloads/20190025111.pdf`. Venue/date confirmed from the NTRS citation JSON (`meetings` field): "Vertical Flight Society's Annual Forum and Technology Display", Philadelphia, PA, 13–16 May 2019 (not stated on the PDF's own page 1, which prints only title/authors/affiliation).
- **Evidence level**: V — conference abstract/short paper (NASA peer-reviewed, but explicitly labelled preliminary: "Preliminary plots show geometric angle of attack; corrected angle of attack will be provided in the final paper").
- **What it says (Q3)**: This is the closest match found to "has anyone tilted a rotor/propeller on a thrust stand to sweep elevation past fixed microphones." The Tiltrotor Test Rig (TTR) has **fixed microphones** (four, at fixed elevation/azimuth angles relative to the rotor hub) and the test explicitly **sweeps the rotor shaft tilt angle** rather than moving the microphones, specifically to map how the acoustic signature (there, blade-vortex-interaction noise) depends on the angle between the rotor plane and the fixed observers.

**Verbatim quotes**:

> "The TTR is a rig that is able to rotate on the test-section turntable and fly at various angles from airplane mode to helicopter mode, from 0- to 100-deg shaft tilt angles." (Introduction, p. 1)

> "The scope of acoustic testing includes a sweep of shaft angle (αs) at an advance ratio (µ) of 0.125 and 0.150 and a blade loading coefficient (CT/σ) of 0.075. Upon completion of this sweep, data will be analyzed in order to identify the shaft angle that yields the peak BVISPL. ... The desired shaft angles to be measured for the TTR are from -6° to +12° at 3° increments." (Test Conditions, p. 3)

> "Precision required of the shaft angle placement (implemented through the wind tunnel turntable yaw angle) during the test was governed by the sensitivity of the BVI to shaft angle. BVI sensitivity to the shaft angle is not constant, but rather a function of the specific microphone location and the shaft angle itself" (Test Conditions, p. 3)

> Table 2 gives four fixed 2018 TTR microphone elevation angles relative to the hub: −45°, −60°, −20°, −30° (at azimuths 150°/131°/150°/144°) (p. 2).

- **Caveat for our use case**: the *purpose* here is to find the peak-BVI shaft angle (a search), not to reconstruct one directivity balloon by combining several tilt angles' data the way Q3 envisions (turning a mic-fixed room error into a per-mic constant that cancels out on averaging) — but the underlying mechanical action (fixed mics, swept shaft/rotor-plane tilt angle via the mounting turntable, not the microphones) is exactly what was asked about, and the paper explicitly notes that sensitivity to shaft angle is a function of microphone location, i.e. shaft tilt and mic position are not interchangeable in general — a caution for anyone proposing to use tilt-sweeps as a stand-in for a full elevation arc.

---

## 14. Klippel AN54 — "Directivity Measurement with Turntables" [vendor]

- **File**: `docs/references/Klippel_AN54_Directivity_Turntables.pdf` (already held; re-extracted fresh to `papers/arc-validation/refetch-txt/Klippel_AN54_Directivity_Turntables.txt`).
- **Identity**: `pdfinfo` Author "Klippel GmbH"; body text "Directivity Measurement with Turntables AN54 / Application Note to the KLIPPEL ANALYZER SYSTEM (Document Revision 1.7)", "Last updated: June 18, 2021" (p. 8).
- **Evidence level**: vendor application note (tool-specific instructions), 8 pages, read in full.
- **What it says (Q3)**: The reference implementation of "rotate the source, not the mic" for loudspeakers: one turntable carries the loudspeaker for the polar (ϑ) axis, an optional second turntable for the azimuthal (ϕ) axis, and the microphone stays fixed at ϑ=0°.

**Verbatim quotes**:

> "The turntable 1 at the bottom is used as polar (ϑ-) axis. In the two dimensional setup a second turntable 2 for the circular (ϕ-) axis is arranged perpendicular to turntable 1. The microphone needs to be positioned at the polar position of ϑ =0°. The loudspeaker driver should point into this direction as well. ... Thus, rmic is defined as the distance between the microphone and this center point of turntable 1. Please make sure that the distance rmic does not change during the measurement." (§1.1, p. 2)

> "A special measurement task of the POL module is the CEA2034 measurement, which requires two POL scans." (§5, p. 8)

---

## 15. ARTA Application Note No. 6 — "Directivity Measurements" (Mateljan) [vendor]

- **File**: `docs/references/ARTA_AN6_Directivity_Measurements.pdf` (already held; re-extracted fresh to `papers/arc-validation/refetch-txt/ARTA_AN6_Directivity_Measurements.txt`).
- **Identity note**: `pdfinfo` reports Author "Mateljan" (consistent with the held ARTA AN4, same author) but the PDF's **Title metadata field reads "Near Field, Far Field and Free Field"**, which is the title of a *different* ARTA note; the document's own printed running header, repeated on every page, is unambiguously "ARTA - APPLICATION NOTE No 6: Directivity Measurements" — the content matches the filename, not the stale metadata field (most likely explained by the file having been produced from a copy of an earlier note's template). Flagged as an observation, not a substantive discrepancy — content used is from what the pages actually say.
- **Evidence level**: vendor application note, 13 pages, read in full.
- **What it says (Q3, and a related time-domain technique for Q4/Q5's spirit)**: Same turntable-rotates-the-source architecture as Klippel AN54 (source #14) for loudspeaker measurement, plus a numeric example of a **time-domain reflection-gating window** as a different way of "changing the measurement, not the room."

**Verbatim quotes**:

> "Usually the speaker is measured on a turntable with a scale to show the angle... The measurement microphone should be positioned so that it is aimed exactly at 0° with respect to the center... of the loudspeaker frame... It is important to ensure that the chosen reference point for rotation does not change." (p. 1)

> "The non-central positioning of the sound source, or rather the sound propagation point, leads to the fact that, depending on the angle of rotation, the distance will change... and thus different levels will be measured. This would have to be corrected after the measurement. In this case each individual measurement would have to be scaled to a one meter distance." (p. 1) — i.e. even in the pure rotate-the-source case, an off-axis mounting reintroduces a distance/level error that must be corrected per angle, illustrating why Q3's premise (mic-fixed error becomes a *per-mic constant*) requires the rotation axis to coincide with the acoustic centre.

> "The analysis takes into account a window using the selected starting position and length of the window. In this case it is possible to hide the region and thus have free-field conditions. ... With a normal ceiling height of 2.50 m, a measurement height one half of the room height and a measuring distance of about one meter, the window should be about 4.5 ms." (p. 3)

---

## 16. Klippel AN69 — "Far Field Measurement using Microphone Arrays" [vendor]

- **File**: `docs/references/Klippel_AN69_Far_Field_Mic_Arrays.pdf` (already held; re-extracted fresh to `papers/arc-validation/refetch-txt/Klippel_AN69_Far_Field_Mic_Arrays.txt`).
- **Identity**: `pdfinfo` Pages 11, no printed author (branding "KLIPPEL R&D System" throughout); body "Far Field Measurement using Microphone Arrays AN 69 / Application Note to the KLIPPEL R&D and QC SYSTEM (Document Revision 1.2)".
- **Evidence level**: vendor application note, read in full.
- **What it says (Q5, negatively)**: This is the vendor's own description of using a static microphone array instead of a turntable — the closest thing in the held/available corpus to "our" arc-of-fixed-mics geometry — but it explicitly still assumes an anechoic chamber; it is sold as a **data-collection speed-up over rotating the source**, not as a reflection-rejection technique, and makes no claim about suppressing room reflections.

**Verbatim quotes**:

> "As an alternative to rotating the loudspeaker, the radiation pattern can be measured using microphone arrays in combination with a multiplexer." (Description, p. 1)

> "The device under test is a transducer mounted in the floor of a half anechoic chamber." (§Introduction/Target, p. 4)

- **Bearing on Q5**: no reflection-rejection claim of any kind is made for the array; the array here is purely a substitute for a turntable, still run inside a qualified anechoic space. Supports the thread's negative finding for Q5 (below).

---

## 17. Bellmann & Klippel, "Fast Loudspeaker Measurement in Non-Anechoic Environment" [vendor technical paper]

- **File**: `papers/arc-validation/Bellmann-Klippel_nd_vendor-paper_non-anechoic-loudspeaker-measurement.pdf`; text dump `papers/arc-validation/txt/Bellmann-Klippel_nd_vendor-paper_non-anechoic-loudspeaker-measurement.txt`.
- **Route**: `https://klippel.de/fileadmin/klippel/Bilder/Know-How/Literature/Papers/Fast%20Loudspeaker%20Measurement%20in%20Non-Anechoic%20Environment.pdf`. `pdfinfo`: Author "c.bellmann@klippel.de;wklippel@klippel.de", Title "Fast Loudspeaker Measurement in Non-Anechoic Environment", 10 pages. Body: "Christian Bellmann, Wolfgang Klippel / KLIPPEL GmbH, Mendelssohnallee 30, 01309 Dresden, Germany." **No convention/venue or year is printed anywhere in the 10-page body** (checked — no "preprint", "Convention Paper" or "AES" self-reference found, only in the reference list citing *other* AES papers up to 2017); dated no more precisely than "some time at or after 2017" from its own reference list. Treated as a vendor technical paper, not a confirmed peer-reviewed proceeding.
- **Evidence level**: vendor technical paper (not confirmed peer-reviewed venue) — tagged [vendor], used only for the compensation-function concept and equations, not as an authority on chamber standards.
- **What it says (Q2)**: This is the most direct match found anywhere in this thread for "a paper that applies a per-position free-field correction derived with a reference source to a directivity measurement." It defines a compensation function computed **per test point rt** from a reference response measured once under known-good (anechoic or holographically-extrapolated) conditions, then applied to convert an in-situ (non-anechoic) measurement at that same point into a simulated free-field response.

**Verbatim quotes**:

> "The evaluation of the loudspeaker performance requires a measurement of the sound pressure output in the far field of the source under free field condition. If the available test room does not fulfil this condition, it is common practice to generate a simulated free field response by separating the direct sound from the room reflection based on windowing and holographic processing. This paper presents a new technique that performs a filtering of the measured sound pressure signal with a complex compensation function prior to other time and frequency analysis. ... Different methods are presented for the generation of the compensation function based on a reference response measured under anechoic conditions and a test response measured under in-situ conditions." (Abstract, p. 1)

> "3.1. Room and Position Compensation / A simulated free-field response Hfree(f,rr) at a defined reference point rr can be generated by multiplying the transfer response Htest(f,rt) measured at a test point rt in a non-anechoic environment (in-situ test) with a compensation function Hc(f): Hfree(f,rr) = Htest(f,rt) Hc(f) (6) ... Hc(f) = Href(f,rr) / Htest(f,rt)" [simplified single-reference-point form] "(7)" (§3.1, p. 3)

> "A much simpler method is to use a reference transfer function Href(f,rr) measured at a reference point rr under anechoic condition. If an anechoic room of sufficient size and wall treatment is available, a single measurement of the loudspeaker in this room while placing the microphone at the reference position rr is suitable for generating a valid reference function Href(f,rr)." (§3.1, p. 3)

> "The coefficients Cmn(f) of the wave expansion Eq. (4) identified with a minimum of scanning points allow the generation of the required reference curve Href(f,rt) at any test point rt determined in the final testing. Thus, the compensation function Hc(f,rt) can be automatically determined after defining the test point rt and measuring the in-situ response Htest(f,rt)." (§4/discussion, p. 8) — **Hc is explicitly indexed by test point rt**, i.e. this is the per-position correction Q2 asks about, though derived from a holographic model of the *device under test* extrapolated to each position, not from a separate physical reference sound source measured at each position in turn.

- **Caveat**: the "reference" here is the loudspeaker's own anechoic (or holographically-modelled) response, used as its own free-field standard — not a certified reference sound source of known directivity substituted at the test-object's position the way ISO 6926/26101-2's RSS methods use one. It answers the "per-position correction exists and has been published" half of Q2 but not the "using a certified reference source" half in the same paper; no single retrieved source does both at once.

---

## Answers to the thread questions

### Q1 — Two-distance / two-surface methods

**How K2 is derived**: Two independent, mutually consistent method families across every source read (NPL 1996, NPL 2004, ISO 3744:2010, ISO 26101-2:2024):
- **Absolute/substitution method**: `K2 = Lwr − Lw` (Payne & Simmons 1996, §2.2, p. 3) using a calibrated RSS (ISO 6926-compliant) placed where the test object goes.
- **Two-surface method**: only valid when room length and width are each < 3× ceiling height; compare Lp on two similar, concentric surfaces S and S2 with S2/S ≥ 2 (preferably > 4); `S/A = (1 − M·S/S2)/(4(M−1))`, `M = 10^(0.1(Lp1−Lp2))`, then `K2 = 10·log(1+4S/A)` (Payne & Simmons 1996, §2.4, p. 4).
- ISO 26101-2:2024 confirms the modern (2024) home of these methods: absolute test = Clause 5 (pointing to ISO 3744:2024 Annex A), two-surface = Clause 6.3 — **the operative formulas for the current edition were not retrievable** (preview stops at §5.1; ISO 3744:2010's own Annex A, which held the 2010-edition formulas, is also outside its preview — see source #8's note and RETRIEVAL-G.md). The NPL 1996 report's formulas (above) are the only fully-quoted two-surface derivation obtained in this thread.

**Residual/uncertainty claimed**: Payne & Simmons 1996 found the two-surface method under-predicts K2A by up to −2.2 to −4.0 dB depending on room, "particularly badly where the second surface was affected by reflections from nearby objects," while the absolute method was "the only method that will consistently provide an accurate assessment of K2A" (Abstract; §5.4, p. 22–23). Simmons, Jobling & Payne 2004 quantified how much correcting with RSS-derived K2 helps: A-weighted ΔLmax fell from 6.4/7.3 dB (uncorrected, ISO 3745:2003 rooms) to 0.8/0.1 dB after applying K2 (§4.4.2.4, p. 49).

**Per-direction correction discussed anywhere?** **No — not once, across five independent documents that define K2 (Payne-Simmons 1996; Simmons-Jobling-Payne 2004; ISO 3744:2010; ISO 26101-2:2024).** All five use verbatim-identical or near-identical language: K2 is "a correction applied to the mean (energy average) of the time-averaged sound pressure levels over all the microphone positions on the measurement surface" (ISO 3744:2010 §3.17, p. 5; ISO 26101-2:2024 §3.3, p. 2; paraphrased identically in NPL 2004 §2.2.2, p. 4). The only place any source examines a *spatial* dependency of K2 at all is Payne & Simmons 1996 §5.5 (p. 21–22), which varies *source position relative to the walls* and finds the resulting single scalar K2A changes — not a decomposition of K2 across measurement directions. Separately, ISO 5305:2024 requires the room-*qualification* deviation (not K2 itself) to be checked "for all source positions and measurement directions" against a fixed tolerance (§7.2.2, p. 7) — a per-direction pass/fail gate on the room, not a per-direction correction term.

### Q2 — Substitution/comparison with a reference source of known directivity

ISO 6926:2016 requires an RSS to meet stability (±0.3 dB across line-voltage variation, §5.2, p. 5), spectral-flatness (within 12 dB overall / 3 dB step-to-step across 100 Hz–10 kHz, §5.4, p. 5), and directivity requirements verifiable only in a hemi-anechoic room (§1, p. 1) via a **per-direction** directivity index `DIi = Lpi − Lp` (§3.9, pp. 3–4) — the RSS's own uniformity is graded direction-by-direction even though the K2 it produces (Q1) is a scalar.

Small omnidirectional sources and their frequency limits: ISO 3382-1:2009's Table 1 (p. 3) is the clearest quoted numeric answer — even a source chosen to be "as close to omnidirectional as possible" is only held to ±1 dB at 125–500 Hz, but the *tolerance itself* widens to ±3 dB at 1 kHz, ±5 dB at 2 kHz, ±6 dB at 4 kHz — i.e. no small source (dodecahedron or closed-box) is expected to stay near-omnidirectional above ~1 kHz; this is directly relevant to SoundVisualizer's 630 Hz–3.15 kHz problem bands.

A paper applying a per-position free-field correction with a reference-type measurement: Bellmann & Klippel [vendor] define `Hc(f,rt)`, a compensation function computed at each test point rt from a reference response `Href` (measured once under anechoic/holographic-reference conditions) and applied to the in-situ response to yield a simulated free-field result (§3.1, p. 3; discussion, p. 8) — this is a genuine per-position correction, but its "reference" is the device under test's own extrapolated response, not a certified reference sound source of known directivity substituted at the object's position. **No retrieved source does both — uses a certified RSS of known directivity, and derives a separate correction per microphone direction/position — in one method.**

### Q3 — Rotating the source instead of the microphones

González & Kob 2026 (DAGA) directly measured this for loudspeakers: a turntable-mounted source following AES56-2008 in four rooms shows level differences up to 18 dB at specific frequencies in non-anechoic rooms versus anechoic (Discussion, p. 1223), caused by "reflections from the turntable, early reflections from walls... and the orientation of the measurement axis relative to the room geometry" (p. 1223) — i.e. rotating the source converts distributed room error into error tied to the turntable/mount geometry, but does not eliminate it; only rooms absorptive enough (anechoic-grade) gave results "highly consistent across all frequency bands" between two differently-sized anechoic rooms (p. 1223). Klippel AN54 and ARTA AN6 [vendor] confirm this is the standard commercial architecture (one or two turntables carrying the source, fixed mic at ϑ=0°), and AES56-2008's retrievable abstract confirms it is what that standard documents ("how the measurements of loudspeaker polar radiation data shall be made," p. 3) — though its operative clauses were paywalled. IEC 60268-21:2018's scope confirms the same family of standards (referencing CTA 2034-A, §2, p. 12) covers near/far-field directional characteristics, but its own directivity clauses (19–20) were likewise outside the retrievable preview.

**Tilting a rotor/propeller shaft to sweep elevation past fixed microphones**: found. Schatzman & Malpica 2019 (NASA/VFS, Tiltrotor Test Rig) run exactly this mechanical arrangement — four **fixed** microphones at fixed elevation/azimuth angles, and a **swept rotor shaft-tilt angle** (−6° to +12° in 3° steps, "implemented through the wind tunnel turntable yaw angle," p. 3) to map blade-vortex-interaction noise versus the angle between the rotor plane and each fixed observer. The paper explicitly notes "BVI sensitivity to the shaft angle is not constant, but rather a function of the specific microphone location and the shaft angle itself" (p. 3) — a caution that shaft-tilt and microphone-elevation sweeps are not simply interchangeable, relevant to any plan to substitute one for the other on SoundVisualizer's rig.

### Q4 — Moving microphones closer versus the far-field requirement

ISO 5305:2024's retrievable clauses give `R ≥ 5DA` (§6.2, Formula 1, p. 5) where DA is the *whole-UAS* diameter (§3.17, p. 4) — not directly transferable to a bare-propeller test article, where DR (propeller diameter) is the only size scale available. Annexes B/C (numerical and measured far-field validation, listed pp. 34/38 in the ToC) are not in the retrieved preview.

Fasulo et al. 2025 (same Tyto 1585 stand as SoundVisualizer) give the clearest in-diameters numbers: reactive near field below L=2D decays ~17 dB/doubling; beyond L=3D decay relaxes to the classical ~6 dB/doubling far-field law, "although slightly elevated (between 6 and 8 dB)" with ripples from ground-reflection interference persisting even there (p. 15–16); their own directivity-arc setup runs at 8D (p. 6). Schmal et al. (held) give the equivalent non-dimensional kr-style criterion directly: far field reached "at kd equals 1.8" (their d = distance from source, not diameter), with an anomalous rise at kd = 7.3 attributed to the chamber's own edges (§4, p. 7) — a caution that going *too* far can reintroduce chamber-boundary error, not just too close.

### Q5 — Microphone arrays/beamforming to reject reflections in a small room

**No OA source quantifying this was found and verified**, despite a dedicated search (queries below). Klippel AN69 [vendor] — the one held/available source that measures directivity with a static array instead of a turntable, i.e. architecturally closest to SoundVisualizer's own arc — explicitly still assumes a "half anechoic chamber" (p. 4) and markets the array purely as a data-collection speed-up over rotating the source, making no claim about reflection rejection. General DOA/beamforming literature exists (e.g. Morgenstern & Rafaely 2024, arXiv:2401.03458, on spherical-array reflection *localisation*) but addresses a different problem (finding where reflections come from, by simulation) and does not quantify reflection-rejection performance, in dB, for a small array measuring a source's own directivity in a small non-ideal room. This question is answered in RETRIEVAL-G.md as SEARCHED AND REJECTED / NOT PURSUED rather than claimed.

---

## Comparison with earlier notes

Re-read from fresh plain `pdftotext -q` dumps in `papers/arc-validation/refetch-txt/` for every held paper used, compared against `papers/anechoic-simulation/MATRIX-3W.md`, `papers/reflection-localization/MATRIX-3W.md`, and `papers/chamber-problems/MATRIX-3W.md` / `EXTRACTS-downloaded.md` / `EXTRACTS-local.md`.

- **Payne & Simmons 1996**: Agree. All quoted numbers (K2A range 7.6 dB; room A absolute-method values 0/0.6/1.0/1.1 dB across surfaces 1–4; "the room only satisfies ISO 6926 up to a maximum 1.5 m radius"; outdoor cross-check 0.2 dB) match MATRIX-3W.md exactly, same page references. No discrepancy found. One addition beyond what MATRIX-3W.md quoted: the full two-surface-method formulas (§2.4, Eqs. 6–7) and the theoretical-model formula (§3, Eq. 8) — MATRIX-3W.md's condensed note did not carry these; also flagged (new, not in MATRIX-3W.md) the internal α=0.1/α=0.9 label inconsistency in the report's own worked numeric example on p. 6, which does not affect any number relied on here.
- **Simmons, Jobling & Payne 2004**: Agree. The "K2 ... mean (energy average) ... over all the microphone positions" definition, the "1.3 dB to 7.2 dB" K2A rise, the ΔLmax reduction (6.4/7.3 → 0.8/0.1 dB), and the "much more reliable result" quote all match EXTRACTS-downloaded.md verbatim. One page-attribution refinement, not a disagreement: EXTRACTS-downloaded.md cites the "much more reliable result" sentence at p. 52; the fresh re-read confirms this exact sentence is printed **twice** — once at the end of §4.4.2.4 (p. 49) and again verbatim in the §5 Summary & Conclusions (p. 52) — both page citations are correct for their respective occurrence.
- **ISO 26101-2:2024**: Agree. The K2 definition, the "usually K2 increases with S" note, the four-method structure (absolute/room-absorption/inverse-square/estimated), and the "In hemi-anechoic rooms, the other qualification procedures can yield unreliable results" quote all match MATRIX-3W.md (reflection-localization) exactly, same pages. No discrepancy found. Confirmed independently that the preview genuinely stops at §5.1 (p. 4) as MATRIX-3W.md's "Clauses 2–4 and 5.1 only" note states — Clause 6.3 (two-surface method) is not retrievable there either.
- **González & Kob 2026**: Agree. Every quoted sentence and page number (90 Hz room-mode note and comb-filtering note both p. 1221; "18 dB" and "highly consistent" both p. 1223) matches MATRIX-3W.md (anechoic-simulation) exactly, confirmed independently by locating the page-footer markers ("1220"/"1221"/"1222"/"1223") in the raw pdftotext line stream. No discrepancy found.
- **ISO 5305:2024**: Agree. The `R ≥ 5DA` formula, the Table 1 tolerances (±1.5/±1.0/±1.5 dB), the "aerodynamic ground effect" height rule, and the "significant interference pattern... minimized when summing in a frequency band" quote all match MATRIX-3W.md (anechoic-simulation) exactly, same pages. Confirmed independently, as MATRIX-3W.md states, that Annexes B/C are ToC-only in this preview. One addition beyond MATRIX-3W.md's note: the DA-vs-DR (whole-vehicle vs single-propeller diameter) distinction (§3.17/3.19, p. 4), which matters for applying Formula 1 to a bare-propeller test article and was not called out in the earlier note.
- **Fasulo et al. 2025**: Agree. The L<2D "~17 dB/doubling," L>3D "~6 dB/doubling... marginally less than 6 dB, consistent with... ground reflections... constructive and destructive interference" quote (p. 15) and the "Reversing the sense of rotation... up to 4 dB" conclusion (p. 24) both match EXTRACTS-local.md (chamber-problems) verbatim and on the same pages. One clarification added here (not a disagreement): the array radius for their directivity-arc setup, "eight propeller diameters (1840 mm)" (§2.3, p. 6), which situates their own directivity measurement well beyond their own 3D far-field threshold — useful context EXTRACTS-local.md's condensed note did not carry.
- **Schmal (Acoustic Characterization of a Quadcopter Using a Test Stand)**: Agree. The "kd equals 1.8... kd equals 7.3... issues with approaching the edges of the anechoic chamber" quote matches MATRIX-3W.md (anechoic-simulation) verbatim, same page (§4, p. 7). Confirmed independently that "d" in "kd" is defined in the running text as "the distance from the source," not the propeller diameter — worth flagging explicitly for this thread since Q4 asks for a kr-style (not kD-style) far-field criterion and this held paper is the one source that actually supplies it in that exact non-dimensional form.

No held paper's re-read produced a number, quote, or page reference that contradicted the earlier MATRIX/EXTRACTS notes in this thread.
