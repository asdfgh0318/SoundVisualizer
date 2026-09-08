# EXTRACTS-D.md — Thread D: microphone calibration accuracy, drift, and fault-diagnosis

Scope: how to know a UMIK-style calibration file is wrong, and how accurate USB/low-cost
measurement microphones are, for the mic 811-1892 anomaly (reads 2–6 dB low, 125 Hz–2.5 kHz,
after calibration; raw ~1 dB low; its Sens Factor −10.63 dB is the least negative of the set).
Every source below was opened as a PDF (or, for the two HELD papers, re-extracted fresh with
plain `pdftotext -q` into `papers/arc-validation/refetch-txt/`) and quotes were verified against
that extraction. Page numbers are PDF page numbers unless noted as "printed p." (journal folio).

---

## 1. Garg, Surendran, Dhanya, Chandran, Asif & Singh (2019) — MAPAN 34(3):357–369 [HELD, re-read]

**Citation as printed:** N. Garg, P. Surendran, M. P. Dhanya, A. T. Chandran, M. Asif & M. Singh,
"Measurement Uncertainty in Microphone Free-Field Comparison Calibrations," *MAPAN — Journal of
Metrology Society of India* 34(3), 357–369, September 2019. doi:10.1007/s12647-019-00343-7.

**File:** `papers/chamber-problems/Garg_2019_MAPAN_microphone-free-field-calibration-uncertainty.pdf`
(re-extracted fresh to `papers/arc-validation/refetch-txt/Garg_2019_MAPAN_microphone-free-field-calibration-uncertainty.txt`,
identity confirmed from the PDF's own first page: title, authors, MAPAN 34(3):357–369, DOI).

**Evidence level:** journal (peer-reviewed), primary metrology-lab data.

**What it says, with numbers:** This is the comparison/substitution calibration method
(IEC 61094-8) worked in full, including a formal uncertainty budget — exactly the method a UMIK
factory calibration is a commercial instance of. A DUC and a reference microphone are exposed to
the same free-field sound pressure sequentially in a small (2 m³) anechoic chamber; the DUC's
free-field sensitivity level is `L_DUC = L_REF + ΔM`, `ΔM = 20·log10(|U_DUC|/|U_REF|)` (p. 358).
The chamber's own deviation from the inverse-square law was mapped 125 Hz–20 kHz and compared to
ISO 26101:2012's allowable deviations (≤630 Hz: ±1.5 dB; 800 Hz–5 kHz: ±1.0 dB; ≥6300 Hz: ±1.5 dB;
Table 1, p. 360) to find a usable working volume. The full uncertainty budget (Table 4, p. 366,
re-parsed with `pdftotext -layout` to recover row/column alignment, then cross-checked cell-by-cell
against the plain-text dump — every number below was seen intact in both) breaks the expanded
uncertainty (k=2) into **0.45 dB at 125–200 Hz, 0.30 dB at 250 Hz–1 kHz, 0.36 dB at 1.25–2.5 kHz,
0.36 dB at 3.15–5 kHz, 0.42 dB at 6.3–8 kHz, 0.48 dB at 10 kHz, 0.52 dB at 12.5–20 kHz**. The two
largest single contributors in most bands are the **reference microphone itself** (stated
uncertainty 0.25–0.40 dB k=2, i.e. 0.125–0.20 dB standard uncertainty per band) and **departure
from free-field characteristics** (0.10–0.20 dB, contributing up to 0.115 dB in most bands, worst
at low frequency). "Repeatability" — a Type A component derived from three years of repeated
sensitivity measurements on the reference PCB 377B02 microphone (Table 3, p. 365) — contributes
0.04 dB (125–200 Hz) rising to **0.07 dB at 12.5–20 kHz**, matching the text's own statement (p. 364)
that "the maximum random uncertainty is observed to be 0.07 dB at 16 kHz." Table 3's raw numbers
(eight measurements, 30 June 2015 to 12 July 2018) show real spread beyond that 0.07 dB Type-A
figure: at 16 kHz the sensitivity read −24.95 dB (2015) to −25.50 dB (2018), a **0.55 dB spread**;
at 12.5 kHz, −26.07 dB to −26.46 dB, a **0.39 dB spread**; at 250 Hz–1 kHz the spread across all
eight readings is only 0.10–0.20 dB. (That 0.07 dB the paper quotes is the *standard error of the
mean* of those eight readings at the worst frequency, not the raw range — the two numbers answer
different questions and neither one is "drift" as ordinarily meant; see Q3 below.) The method was
validated by a bilateral comparison against SPEKTRA's own values for two B&K reference microphones:
"the deviation is observed to be less than 0.16 dB in the entire measurement frequency range" for
a B&K 4180, and "less than 0.25 dB" for a B&K 4191 (p. 368) — this is what agreement between two
independent labs, both using laboratory-grade reference microphones, looks like in dB.

**Verbatim quotes:**
- "A dedicated transportable anechoic chamber (make SPEKTRA, Germany) of internal volume of 2 m3
  … is utilized for free-field calibrations … using the substitution method as per the IEC
  61094-8 standard. … The measurement uncertainty of ± 0.36–0.52 dB (k = 2, 95% confidence level)
  is evaluated in the frequency range of 125 Hz–20 kHz and is validated in a bilateral comparison."
  (Abstract, p. 357 — note this abstract range does not actually bound the paper's own Table 4,
  whose lowest band is 0.45 dB and whose 250 Hz–1 kHz band is 0.30 dB; see §"Comparison with
  earlier notes" below.)
- "Substitution calibration describes the process where reference microphone is first used to
  determine the sound pressure at specific point inside a free field and is then replaced by
  microphone under calibration. The acoustic centres of the two microphones can be located at the
  same point in the sound field." (p. 358)
- "Table 3 shows the sensitivity (in dB ref 1 V/Pa) for PCB microphone Model 377B02 … observed in
  the past three years. The maximum random uncertainty is observed to be 0.07 dB at 16 kHz." (p. 364)
- Table 4 row "Reference microphone," uncertainty value "0.25–0.40" dB, distribution "(Normal, 2)",
  per-band standard-uncertainty contribution "0.15 / 0.125 / 0.125 / 0.125 / 0.125 / 0.175 / 0.20"
  dB across the seven bands 125–200 Hz … 12.5–20 kHz; row "Expanded uncertainty (k = 2) in dB":
  "0.45 / 0.30 / 0.36 / 0.36 / 0.42 / 0.48 / 0.52". (p. 366, re-extracted with `-layout`)
- "For B&K 4180 microphone, the deviation is observed to be less than 0.16 dB in the entire
  measurement frequency range, while for the B&K 4191 microphone, the deviation is observed to be
  less than 0.25 dB in the entire measurement frequency range, which validates the measurement
  uncertainty evaluated in the entire measurement frequency range." (p. 368)

---

## 2. Burnett & Nedzelnitsky (1987) — J. Res. NBS 92(2), 129–151 [HELD, re-read]

**Citation as printed:** Edwin D. Burnett & Victor Nedzelnitsky, "Free-Field Reciprocity
Calibration of Microphones," *Journal of Research of the National Bureau of Standards* 92(2),
129–151, March–April 1987.

**File:** `papers/small-chamber/Burnett-Nedzelnitsky_1987_JResNBS_free-field-reciprocity-calibration-chamber-deviations.pdf`
(re-extracted fresh to `papers/arc-validation/refetch-txt/`; identity confirmed from the PDF's own
first page — title, authors, "Volume 92 / Number 2," March–April 1987).

**Evidence level:** report/journal (National Bureau of Standards primary metrology service).

**What it says, with numbers:** This is the **primary reciprocity method** (the one comparison
calibrations like Garg's are ultimately traceable to), used here for NBS's own 1/2-inch microphone
free-field calibration service, 2.5–20 kHz. It is the historical benchmark for "how good can the
top of the traceability chain actually do": **"0.16 dB or better (s=0.06 dB, 2σ=0.10 dB) at
frequencies 1.25 kHz ≤ f ≤ 5 kHz, and 0.07 dB or better (s=0.02 dB, 2σ=0.05 dB) for 5 kHz ≤ f ≤
20 kHz"** (abstract, p. 129) — coincidentally the same two numbers (0.16, 0.07 dB) that reappear
in Garg's bilateral-comparison and repeatability figures above, though they measure different
things in a different chamber three decades apart. Used here only as Q2 context/baseline for what
"class-1 reference" accuracy means in practice, not as evidence about UMIKs.

**Verbatim quotes:**
- "The overall uncertainty estimate for free-field calibration, expressed as the sum of the
  magnitude of credible bounds on the systematic component (s) and the random component (2σ, where
  σ is the standard deviation) is 0.16 dB or better (s=0.06 dB, 2σ=0.10 dB) at frequencies
  1.25 kHz ≤ f ≤ 5 kHz, and 0.07 dB or better (s=0.02 dB, 2σ=0.05 dB) for 5 kHz ≤ f ≤ 20 kHz."
  (Abstract, p. 129)

---

## 3. Wagner & Guthrie (2015) — J. Res. NIST 120, 164–172

**Citation as printed:** Randall P. Wagner & William F. Guthrie, "Long-Term Stability of One-Inch
Condenser Microphones Calibrated at the National Institute of Standards and Technology," *Journal
of Research of the National Institute of Standards and Technology* 120, 164–172, 2015.
doi:10.6028/jres.120.012.

**File:** `papers/arc-validation/Wagner_2015_NIST-JRes_condenser-mic-long-term-stability.pdf`
(9 pp.). Route: direct PDF from `nvlpubs.nist.gov/nistpubs/jres/120/jres.120.012.pdf`. Identity
confirmed: title/authors/DOI on p. 1 (printed folio 164).

**Evidence level:** report/journal (NIST primary calibration-service data), directly answers Q3.

**What it says, with numbers:** NIST's own multi-decade calibration records for the three
one-inch condenser microphone types most frequently sent to it (1963–2012): **32 Type LS1Pn
(Brüel & Kjær 4160), 20 Type LS1Po (Western Electric 640AA), and 24 Type WS1P (Brüel & Kjær
4144)**, selected as the **484 data sets from 76 microphones** each spanning more than 5 years
(p. 167). Average drift rates per type, with 95% confidence intervals: **LS1Pn −0.004 to
0.003 dB/year; LS1Po −0.016 to 0.008 dB/year; WS1P −0.004 to 0.018 dB/year** — none
significantly different from zero (p. 164). This is the standard for what a well-designed,
laboratory-grade condenser capsule's ageing actually looks like: essentially flat over years, with
the *between-microphone* spread of individual drift rates (not quoted as a single number, but
shown via a normal-probability plot of the 32 LS1Pn units, p. 168) dwarfing the mean.

**Verbatim quotes:**
- "The devices calibrated most frequently by the acoustical measurement services at the National
  Institute of Standards and Technology (NIST) over the 50-year period from 1963 to 2012 … were
  one-inch condenser microphones of three specific standard types: LS1Pn, LS1Po, and WS1P." (p. 164)
- "The average drift rate for Type LS1Pn microphones was -0.004 dB/year to 0.003 dB/year. The
  average drift rate for Type LS1Po microphones was -0.016 dB/year to 0.008 dB/year. The average
  drift rate for Type WS1P microphones was -0.004 dB/year to 0.018 dB/year. For each of these
  microphone types, the average drift rate is not significantly different from zero." (p. 164)
- "These selection criteria are met by 484 data sets for 76 microphones. Of these microphones, 32
  were Bruel and Kjaer Model 4160 … Type LS1Pn microphones, 20 were Western Electric Model 640AA
  Type LS1Po microphones, and 24 were Bruel and Kjaer Model 4144 Type WS1P microphones." … "For
  each microphone, the time spanned by the available data sets exceeded 5 years." (p. 167)

---

## 4. Risojević, Rozman, Pilipović, Češnovar & Bulić (2018) — Sensors 18(7), 2351

**Citation as printed:** Vladimir Risojević, Robert Rozman, Ratko Pilipović, Rok Češnovar &
Patricio Bulić, "Accurate Indoor Sound Level Measurement on a Low-Power and Low-Cost Wireless
Sensor Node," *Sensors* 18(7), 2351, 2018. doi:10.3390/s18072351.

**File:** `papers/arc-validation/Risojevic_2018_Sensors_low-cost-wireless-node-sound-level.pdf`
(22 pp.). Route: `mdpi-res.com/d_attachment/sensors/sensors-18-02351/article_deploy/sensors-18-02351.pdf`.
Identity confirmed from p. 1 header/authors.

**Evidence level:** journal (MDPI, peer-reviewed).

**What it says, with numbers:** A **MEMS** microphone node (Knowles/SiSonic SPM0408LE5H-TB,
"typical sensitivity at 1 kHz is −18 dBV/Pa," p. 8) calibrated against a Class-1 reference
(MI 6201 Multinorm, "Class 1 (Pro Set) sound level meter … compliant with IEC 61672 standard,"
p. 16) achieves **"mean difference of less than 2 dB compared to Class 1 sound level meter"**
(abstract, p. 1), and in a real 12-minute indoor recording, a Pearson correlation of R=0.88 with
**"mean difference between two devices … of 1.6 dB"** (p. 16). Getting there required more than a
flat offset: raw (non-calibrated) readings were low relative to the Class-1 reference with **"a
slight nonlinearity due to poor quality of the used microphone,"** corrected with a **3-piece
piecewise-linear fit** (different slope/intercept for SPL<60 dB, 60–70 dB, and ≥70 dB) rather than
one constant gain (p. 15) — a genuine example of a calibration curve that is not a simple offset
(a level-dependent nonlinearity, distinct from the frequency-dependent "shape" error asked about
in Q4, but the same general point: don't assume one number fixes a mic). The paper also relays two
other studies' numbers for context: **"an effective range from 55 to 100 dB at 3 dB accuracy when
compared to a Class 1 sound level meter"** (Mydlarz et al. 2017, cited as [24]) and **"good
agreement (within 3 dB) … in the range 55–100 dB"** (Blythe et al./Bell & Galatioto, cited as
[25],[26]) — both attributed to those other papers, not independently verified here (see
RETRIEVAL-D.md).

**Verbatim quotes:**
- "the proposed sound level meter can accurately measure the noise levels of up to 100 dB, with the
  mean difference of less than 2 dB compared to Class 1 sound level meter." (Abstract, p. 1)
- "The sensor node uses the SiSonic SPM0408LE5H-TB [32] low-power MEMS microphone to measure the
  sound level. … According to [32], the typical sensitivity at 1 kHz is −18 dBV/Pa." (p. 8)
- "Also, the sensitivity of MEMS microphones varies very little over temperature, a fraction of a
  decibel at most [32]." (p. 9 — [32] is the Knowles datasheet, not independently verified here.)
- "The results show that the sound pressure levels were lower than sound pressure levels obtained
  with the MI 6201 MULTINORM sound meter. We can also observe a slight nonlinearity due to poor
  quality of the used microphone and overall acoustic transfer function of the sensor node and its
  housing." … calibration fit: `SPL = 2.65·SPL_NC − 83.52` for 50≤SPL_NC<60 dB, `1.30·SPL_NC −
  10.42` for 60≤SPL_NC<70 dB, `1.01·SPL_NC + 7.49` for SPL_NC≥70 dB. (p. 15)
- "The mean difference between two devices for the both 12-min measurements is 1.6 dB." (p. 16)
- (relaying Mydlarz et al. 2017) "hardware with an effective range from 55 to 100 dB at 3 dB
  accuracy when compared to a Class 1 sound level meter." (p. 4)
- (relaying Blythe et al./Bell & Galatioto) "the authors reported that good agreement (within 3 dB)
  was verified in the range 55–100 dB." (p. 5)

---

## 5. Picaut, Can, Fortin, Ardouin & Lagrange (2020) — Sensors 20(8), 2256 (review)

**Citation as printed:** Judicaël Picaut, Arnaud Can, Nicolas Fortin, Jeremy Ardouin & Mathieu
Lagrange, "Low-Cost Sensors for Urban Noise Monitoring Networks—A Literature Review," *Sensors*
20(8), 2256, 2020. doi:10.3390/s20082256.

**File:** `papers/arc-validation/Picaut_2020_Sensors_low-cost-noise-sensors-review.pdf` (31 pp.).
Route: `mdpi-res.com/d_attachment/sensors/sensors-20-02256/article_deploy/sensors-20-02256.pdf`.
Identity confirmed from p. 1 header/authors/abstract.

**Evidence level:** journal (MDPI, peer-reviewed review). Every specific claim below is this
review's own summary of a separately-cited primary study ([citation numbers] as printed); I read
Picaut et al. directly and quote what it says about those studies, not the primary studies
themselves (see RETRIEVAL-D.md for which of those I could/couldn't independently retrieve).

**What it says, with numbers (Q1 — accuracy vs. Class-1):**
- "the network presented in [38] [= Risojević et al. 2018, above] … Indoor test measurements were
  compared with a Class-1 sound level meter showing a very good correlation on the measured sound
  levels, with a mean difference of 1.6 dB over a 12 mn testing time-period." (p. 7)
- "Peckens et al. [63] … Comparisons with sound level measurements using a Class-1 reference
  device, show a good agreement, with deviations around ±1.5 dB." (p. 7)
- MONZA project sensors "seem to provide consistent data in comparison with reference sound level
  meters, with however a systematic offset around 3 dB." (p. 7)
- "it is not necessary to seek a measurement accuracy of less than 1 dBA" for strategic noise-map
  use [22] (p. 16) — i.e. the review's own view of what accuracy is *needed*, not what a UMIK
  achieves.

**What it says, with numbers (Q3 — drift/ageing, §2.3.9/3.3):**
- "Renterghem et al. [73] have studied the effect of temperature, humidity and wind, on the sound
  levels measured by electret and MEMS microphones. … by comparison with a reference microphone,
  such temperature correction (acting as a gain on the signal) applied on an ECM was able to reduce
  the deviation of the global error from 1.6 dBA to 0.8 dBA, over the full period of observation
  (several months). … The authors have also noted inconsistent behaviour of the MEMS microphone at
  temperatures below 20°C, high relative humidity and high wind speed, but no explanation has been
  given." (p. 14–15)
- "The effect of ambient temperature on the sensitivity of a MEMS sensor was also investigated by
  Barham and Goldsmith [45]. From their results, it seems that the variation in sensitivity would
  increase with frequency and temperature (tested between −5°C–40°C), in the order of ±1 dB over
  the frequency range between 100 Hz and 8 kHz. Conversely, [67] have not seen significant variation
  of MEMS microphone sensibility with temperature." (p. 15)
- "Bartalucci et al. [80] report that they observed a reduction of acoustic sensitivity of MEMS
  microphones during the initial running-in phase, on the order of 1–2 dB on a time period of
  4 months." (p. 15)
- "Li et al. [81] have studied the reliability of MEMS microphones … Considering the corrosion
  test, wire bond corrosion and membrane embrittlement were observed after 90 days in the test
  chamber, but with a very slight impact on the frequency response of the microphone." (p. 15)
- "Knowing that the lifetime of a Class-1 sound level meter can extend to more than 10 years under
  normal conditions of use [90] …" (p. 20) — reference [90] is itself a Brüel & Kjær marketing blog
  post ("Guide: Lifetime cost of ownership for class 1 sound level meters"), not an independent
  study; flagged as weak sourcing for that one figure.

**What it says (Q4 — offset vs. shape, §2.3.7 Calibration):**
- "In the simplest case, the same correction is applied to the entire temporal signal, without
  distinction of frequency or amplitude. In a more advanced way, this correction can also correct
  linearity defects in level and frequency [38] and temperature [73]." (p. 14) — this is the
  clearest single statement found in this thread's sources that a "flat" (single-number) correction
  and a frequency/level-resolved correction are recognised in the literature as two different
  things, the latter strictly more capable than the former.

---

## 6. Mydlarz, Salamon & Bello (2016, arXiv preprint of Appl. Acoust. 117 (2017) 207–218)

**Citation as printed:** Charlie Mydlarz, Justin Salamon & Juan Pablo Bello, "The Implementation of
Low-cost Urban Acoustic Monitoring Devices," arXiv:1605.08450v1 [cs.SD], 26 May 2016. Published
version: *Applied Acoustics* 117, 207–218, 2017 (Applied Acoustics is a known-blocked publisher —
see PROTOCOL.md — so the arXiv preprint was read instead; content may differ in minor respects
from the final peer-reviewed text).

**File:** `papers/arc-validation/Mydlarz-Salamon-Bello_2016_arXiv_low-cost-urban-acoustic-monitoring.pdf`
(26 pp.). Route: `curl -sL -A <browser UA> https://arxiv.org/pdf/1605.08450`. Identity confirmed
from p. 1: title, authors, "arXiv:1605.08450v1 [cs.SD] 26 May 2016."

**Evidence level:** conference/preprint (arXiv) of a peer-reviewed journal article; the most
directly quantitative Q1/Q4 source in this set because it publishes a full per-frequency
before/after-calibration comparison table against a Type-1 reference.

**What it says, with numbers (Q1):** A custom node built around a Knowles SPU0410LR5H-QB analog
MEMS microphone was benchmarked against a Larson Davis 831 (a Type 1 SLM, itself calibrated with a
Type 1 Larson Davis CAL200) following a subset of the IEC 61672-3 periodic-test procedures, with
the paper explicitly correcting for the fact that the Type-1 reference has its own error budget
("if the type 2 tolerance bounds … are ±2.0 dB with the corresponding type 1 bounds at ±1.0 dB, the
adjusted acceptable bounds for the type 2 class in this instance are ±1.0 dB," p. 17). Table 3
(p. 18, verified with `pdftotext -layout`) is the frequency-weighting test result:

| Freq. (Hz) | DUT (dBA) | Ref. (dBA) | Δ (dB) | Adj. tolerance |
|---|---|---|---|---|
| 31.5 | 44.8 | 45.2 | 0.4 | ±1.5 |
| 63 | 63.6 | 63.7 | 0.1 | ±1.0 |
| 125 | 76.6 | 76.2 | 0.4 | ±0.5 |
| 250 | 85.3 | 84.9 | 0.4 | ±0.5 |
| 500 | 90.2 | 89.9 | 0.3 | ±0.5 |
| 1 k | 93.9 | 94.0 | 0.1 | ±0.3 |
| 2 k | 93.6 | 94.2 | 0.6 | ±1.0 |
| 4 k | 94.1 | 93.3 | 0.8 | ±2.0 |
| 8 k | 93.2 | 90.6 | 2.6 | ±3.0 |

— i.e. **the residual after a single-point (94 dB@1 kHz) offset calibration is not flat: it grows
from 0.1–0.4 dB at low/mid frequencies to 2.6 dB at 8 kHz**, though every band still meets its
(reference-tolerance-adjusted) IEC 61672-1 limit. In a 30-minute constant-level stability test the
device held within 0.07 dBA (type-2 tolerance ±0.2 dBA, p. 18); over a real 15-minute urban-audio
replay, R²=0.9723 and a mean difference of 0.4 dB (std 0.1 dBA, range 0.1–1.8 dBA) against the
Type-1 SLM (p. 20). Elsewhere it relays a *different, unrelated* project's number for context:
**"an effective range from 55-100dBA at ≈3dBA accuracy when compared to a type 1 sound level
meter"** (the Newcastle MESSAGE project, cited as [24], p. 5 — not independently verified here).

**What it says (Q3 — temperature):** citing Scheeper et al. (2003, J. Microelectromech. Syst.
12(6):880–891, cited as [32], not independently retrieved — see RETRIEVAL-D.md): **"A study
characterizing a custom MEMS microphone solution for acoustic measurement purposes [32] exhibited
a very low temperature coefficient for sensitivity of <0.017dB/°C. A large variation in humidity
was also shown to have a minimal impact on the MEMS microphones sensitivity, with decreases of
<0.1dB between relative humidity (%RH) conditions of 40% and 90%."** (p. 8–9) Cross-check:
0.017 dB/°C integrated over the −5…40°C range Barham & Goldsmith tested (Picaut §5 above) is
≈0.77 dB — consistent in order of magnitude with their reported "±1 dB over 100 Hz–8 kHz," despite
being two independent secondary reports of two different primary studies on two different MEMS
capsules.

**What it says (Q4 — offset vs. shape, mechanism):** Figure 10's calibration signal chain is:
**"input audio samples → inverse frequency response filter → frequency weighting filter → time
weighting filter → SPL calculation → output SPL values,"** with the text specifying separately that
**"the output sound pressure level … is calculated from the A weighting filtered sample values,
which represent the AC voltage produced when presented with the calibration signal of a 1kHz sine
wave at 94dBA. An offset adjustment is then applied in order to match the 94dBA SPL input level."**
(p. 16) — i.e. the device's own calibration pipeline treats "correct the frequency-response shape"
(an FIR "inverse frequency response filter," designed earlier in the paper from a swept measurement
against the reference mic, p. 12–13) and "set the absolute level" (a single-point offset at 1 kHz,
94 dB) as two distinct, separately-implemented stages — and Table 3 above is the empirical
demonstration that doing only the second (or doing the first imperfectly) leaves a
frequency-dependent residual.

**Verbatim quotes:**
- "an effective range from 55-100dBA at ≈3dBA accuracy when compared to a type 1 sound level
  meter." (p. 5, describing the Newcastle MESSAGE project, not this paper's own device)
- "A study characterizing a custom MEMS microphone solution for acoustic measurement purposes [32]
  exhibited a very low temperature coefficient for sensitivity of <0.017dB/°C. A large variation in
  humidity was also shown to have a minimal impact on the MEMS microphones sensitivity, with
  decreases of <0.1dB between relative humidity (%RH) conditions of 40% and 90%." (p. 8–9)
- "if the type 2 tolerance bounds for a particular measurement response are ±2.0dB with the
  corresponding type 1 bounds at ±1.0dB, the adjusted acceptable bounds for the type 2 class in
  this instance are ±1.0dB (type 2 tolerance range of 4dB minus the type 1 range of 2dB) when using
  the SLM as the reference device." (p. 17)
- Table 3 (p. 18): frequency-by-frequency DUT/Ref./Δ/adjusted-tolerance, reproduced above.
- "In order to test the long term stability of the DUT, it was subjected to a 30min 1kHz sine wave
  at 94dBA. … The DUT met this criteria, with an observed difference of 0.07dBA." (p. 18 — a
  30-minute constant-level test; not evidence about ageing over months/years, despite the section
  heading "Long-term stability.")
- "The total R2 value for this 15min urban signal was 0.9723 (p ≤ 0.0001). The mean difference
  between the SLM and DUT time history values was 0.4dB, with a standard deviation of 0.1dBA,
  minimum vales of 0.1dBA and maximum values of 1.8dBA." (p. 20)
- Figure 10 caption/block list: "input audio samples / inverse frequency response filter /
  frequency weighting filter / time weighting filter / SPL calculation / output SPL values." (p. 16)
- "An offset adjustment is then applied in order to match the 94dBA SPL input level." (p. 16)

---

## 7. IEC 61094-8:2012 (iTeh preview)

**Citation as printed:** IEC 61094-8:2012, *Measurement microphones – Part 8: Methods for
determining the free-field sensitivity of working standard microphones by comparison*, Edition 1.0,
2012-09.

**File:** `papers/arc-validation/IEC-61094-8_2012_standard_freefield-comparison-calibration-preview.pdf`
(15 pp., iTeh preview — Foreword/front matter + Scope + Normative references + start of
Definitions only; the numbered technical clauses with the actual procedure are not in the preview).
Route: `cdn.standards.iteh.ai/samples/18912/d6cabc2801a74056a9d31369715e9684/IEC-61094-8-2012.pdf`.

**Evidence level:** standard (preview only).

**What it says:** This is the standard Garg's method above implements, and directly names what a
UMIK factory calibration is doing metrologically — determining the free-field sensitivity of a
*working standard* microphone by comparison against a reference.

**Verbatim quotes:**
- "This part of the IEC 61094 series is applicable to working standard microphones meeting the
  requirements of IEC 61094-4 [and] describes methods of determining the free-field sensitivity by
  comparison with a laboratory standard microphone or working standard microphone (where
  applicable) that has been calibrated according to either: IEC 61094-3, IEC 61094-2 or IEC 61094-5
  (with factors from IEC/TS 61094-7), IEC 61094-6, or this part of IEC 61094." (Scope, cl. 1)
- "Methods performed in an acoustical environment that is a good approximation to an ideal
  free-field (such as a high quality free-field chamber), and methods that use post processing of
  results to minimise the effect of imperfections in the acoustical environment, to simulate
  free-field conditions, are both covered by this part of IEC 61094. Comparison methods based on
  the principles described in IEC 61094-3 are also possible but beyond the scope of this part of
  IEC 61094." (Scope, cl. 1)

---

## 8. IEC 61094-6:2004 (iTeh preview)

**Citation as printed:** IEC 61094-6:2004, *Measurement microphones – Part 6: Electrostatic
actuators for determination of frequency response*, First edition, 2004-11.

**File:** `papers/arc-validation/IEC-61094-6_2004_standard_electrostatic-actuator-grids-preview.pdf`
(15 pp., iTeh preview — Foreword + Scope + start of Normative references). Route:
`cdn.standards.iteh.ai/samples/12181/3055cee4dce64668ac18d5a74af692a8/IEC-61094-6-2004.pdf`.

**Evidence level:** standard (preview only). Directly answers the "electrostatic actuator" part of
Q2, and is relevant to Q4 because it is, by construction, a *relative*-response method.

**Verbatim quotes:**
- "This part of IEC 61094 – gives guidelines for the design of actuators for microphones equipped
  with electrically conductive diaphragms; – gives methods for the validation of electrostatic
  actuators; – gives a method for determining the electrostatic actuator response of a microphone."
  (Scope, cl. 1)
- "The applications of electrostatic actuators are not fully described within this standard but may
  include – a technique for detecting changes in the frequency response of a microphone, – a
  technique for determining the environmental influence on the response of a microphone, – a
  technique for determining the free-field or pressure response of a microphone without specific
  acoustical test facilities, by the application of predetermined correction values specific to the
  microphone model and actuator used, – a technique applicable at high frequencies not typically
  covered by calibration methods using sound excitation." (Scope, cl. 1)

---

## 9. IEC 60942:2017 (iTeh preview)

**Citation as printed:** IEC 60942:2017, *Electroacoustics – Sound calibrators*, Edition 4.0,
2017-11.

**File:** `papers/arc-validation/IEC-60942_2017_standard_sound-calibrators-preview.pdf` (15 pp.,
iTeh preview — Foreword + Scope + Definitions + start of clause 5). Route:
`cdn.standards.iteh.ai/samples/22818/021e399832234de8aee28f5e994f162c/IEC-60942-2017.pdf`. The
preview does **not** reach the numbered clauses with the actual acceptance-limit tables (dB/%
tolerances per class), only the scope/class structure and definitions.

**Evidence level:** standard (preview only). Directly answers the "sound calibrator/pistonphone
(IEC 60942)" part of Q2.

**Verbatim quotes:**
- "This document specifies the performance requirements for three classes of sound calibrator:
  class LS (Laboratory Standard), class 1 and class 2. Acceptance limits are smallest for class LS
  and greatest for class 2 instruments. Class LS sound calibrators are normally used only in the
  laboratory; class 1 and class 2 are considered as sound calibrators for field use. A class 1
  sound calibrator is primarily intended for use with a class 1 sound level meter and a class 2
  sound calibrator primarily with a class 2 sound level meter, as specified in IEC 61672-1." (Scope, cl. 1)
- "pistonphone: sound calibrator in which the sound pressure is generated in a fixed air volume by
  the motion of one or more pistons, creating a well-defined volume velocity" (def. 3.2)
- "Class LS and class 1 pistonphones that require corrections for the influence of static pressure
  to conform to the specifications for the appropriate class shall have the letter "M" added to
  their class designation. … For class LS/M and class 1/M sound calibrators, the corrections for
  static pressure … shall be stated in the instruction manual, together with the uncertainties of
  measurement corresponding to a coverage probability of 95 %." (cl. 5.1.5)

---

## 10. Cameron, Croarkin & Raybold (1977) — NBS Technical Note 952

**Citation as printed:** J. M. Cameron, M. C. Croarkin & R. C. Raybold, "Designs for the
Calibration of Standards of Mass," National Bureau of Standards Technical Note 952, Office of
Measurement Services, Institute for Basic Standards, issued June 1977. doi:10.6028/NBS.TN.952.

**File:** `papers/arc-validation/Cameron_1977_NBS-TN952_mass-calibration-designs.pdf` (74 pp.,
scanned + OCR'd — text quality is imperfect in equation-heavy passages; the prose sections quoted
below OCR cleanly and were cross-checked by eye against the surrounding text). Route: DOI resolved
to `nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote952.pdf`. Identity confirmed: title,
authors, "NBS Technical Note 952 … Issued June 1977" on the report's own title page. Page
references below are **PDF page numbers** (the scan's own printed folios are not reliably OCR'd).

**Evidence level:** report (NBS/NIST). This is **not an acoustics source** — it is the classical
metrology reference for *designed intercomparisons of physical standards* (mass, in this case),
offered here as the "any metrology source on such round-robin or Latin-square comparison designs"
requested by Q2, since no acoustics-specific source on rotating microphones through positions was
retrieved (see RETRIEVAL-D.md). The mathematics is the direct analogue of what
`scripts/arc_error_map.py` already does for the mic arc: multiple objects (weights / mics) measured
in multiple combinations (weighing series / arc runs), solved by least squares to separate an
individual object's value (weight value / mic offset) from a nuisance parameter (drift / position
error) that a single measurement can't disentangle on its own.

**What it says, with numbers:** The report is a catalogue of specific weighing-design matrices
(schedules of which weight combinations to intercompare), each built so that a least-squares
solution recovers every unknown weight's value *and* a "check standard" that monitors the
measurement process, using one or more known values as a "restraint" to make the system solvable.

**Verbatim quotes:**
- "This report presents a collection of designs for the intercomparison of sets of weights for use
  in precision calibration of standards of mass. These include a number of previously unpublished
  designs which have an additional weight in each set to serve as the check standard for monitoring
  the performance of the weighing process." (Abstract, PDF p. 11)
- "In a calibration laboratory, it is necessary to have checks on the measurement process to
  provide assurance that the process measures what it was intended to measure and that it does so
  with a nearly constant precision. A direct check on the limiting mean of the measurement process
  is provided if a known weight is calibrated regularly as if it were an unknown test weight. If
  the value obtained for the weight differs from its accepted value by an amount larger than can be
  accounted for by the imprecision of measurement, then the process would be regarded as being out
  of control." (PDF p. 12)
- "In summary then, the schedule of measurements for calibration should include provision for a
  check standard and also for within-run redundancy. The decision as to which one of a number of
  possible schedules or designs to use for intercomparison of a set of weights depends on items
  such as the variance associated with individual weights or combinations thereof. The least
  squares analysis from which the values for the weights and their variances are calculated is
  presented in the next section." (PDF p. 14)
- "In mass calibration, one has one or more standards whose value can be taken as known and these
  provide the restraint on the system needed to give a unique set of answers." (PDF p. 8, equation
  section — quoted for the "restraint" concept, i.e. our own fixed-position 0° mic)

---

## 11–13. miniDSP vendor documentation [vendor]

**11. Citation:** miniDSP Ltd, "UMIK-2" product brief (undated). File:
`papers/arc-validation/miniDSP_nd_vendor_UMIK-2-product-brief.pdf` (2 pp.). Route: direct curl of
`minidsp.com/images/documents/Product Brief - UMIK-2.pdf`.

**12. Citation:** miniDSP Ltd, "UMIK-2 User Manual" (undated). File:
`papers/arc-validation/miniDSP_nd_vendor_UMIK-2-user-manual.pdf` (29 pp.). Route: direct curl of
`minidsp.com/images/documents/miniDSP UMIK-2-User Manual.pdf`.

**13. Citation:** miniDSP Ltd, "UMIK-1" product brief (undated). File:
`papers/arc-validation/miniDSP_nd_vendor_UMIK-1-product-brief.pdf` (2 pp.). Route: direct curl of
`minidsp.com/images/documents/Product Brief - Umik.pdf`.

**Evidence level:** vendor — used only for the tool-specific facts requested (capsule identity,
what the calibration file/Sens Factor represent, and at what stated accuracy).

**What they say, with numbers:**
- **UMIK-2 capsule** (both docs, identical text): "1/2" Low noise Pre-polarized condenser on 60UNS
  thread. Sensitivity: -31.9 dB FS (94 dB SPL. 1 kHz). Noise level: -105.3dBfs (A) @ 0 dB gain. MAX
  SPL(0dBfs): 125dB SPL. Equivalent Input Noise (EIN): 20dB SPL @ 0dB gain." — i.e. a
  **pre-polarized condenser** capsule (not electret, not MEMS — the same broad technology as the
  reference-grade B&K/PCB microphones in Garg's and Wagner & Guthrie's papers, at consumer cost and
  presumably consumer manufacturing tolerance).
- **UMIK-1 capsule** (brief, p. 1): "Capsule Type & Polar pattern: 6mm electret, Omni-Directional."
  — i.e. the first-generation UMIK used a smaller **electret** capsule, distinct from the UMIK-2's
  "pre-polarized condenser" wording (electret and pre-polarized condenser are close cousins
  technologically; miniDSP's own marketing copy nonetheless describes them with different terms and
  a different diameter, 6 mm vs. 1/2 inch ≈ 12.7 mm).
- **Stated accuracy — found only for UMIK-1, not UMIK-2:** UMIK-1 brief, p. 1: "Frequency response:
  20 Hz - 20kHz +/-1dB with calibration loaded." No equivalent flatness/accuracy figure, and no
  numeric tolerance on the Sens Factor or calibration curve itself, was found anywhere in the
  UMIK-2 brief or the 29-page UMIK-2 User Manual (searched for "accuracy," "tolerance," "±," "Sens
  Factor," "sensitivity," "specification" throughout) — this is a genuine negative finding: **miniDSP
  does not publish a numeric accuracy/uncertainty figure for what the UMIK-2 calibration file or its
  Sens Factor is good to.**
- **What the calibration file contains:** UMIK-2 User Manual, §1 Product Overview: "Each UMIK-2 has
  a unique calibration file for measurement accuracy. A generated 90-degree calibration file is
  also provided for multichannel/surround-sound applications," and §4: "The calibration files are
  used to correct the raw microphone response for measurement accuracy. Two calibration files are
  provided: an on-axis calibration file measured from the actual microphone, and a 90-degree
  calibration file that is calculated from the on-axis response" (i.e. **not measured** — the
  90° file is a derived/computed curve, not an independent measurement, for every UMIK-2 unit).
  UMIK-1 brief, p. 1: "Unique microphone calibration .txt file referenced to the Serial Number.
  Includes on axis & 90deg - Frequency / Amplitude / Sensitivity drift" (quoted exactly as printed;
  the brief does not explain what "Sensitivity drift" refers to within the calibration file, and no
  other miniDSP document read for this thread uses that phrase again).
- Neither document uses the term "Sens Factor" at all (that term appears to be REW's own label for
  the field in the calibration file it reads, not miniDSP's own vocabulary — consistent with
  CLAUDE.md's existing note that the REW *format* documentation, not miniDSP, is the source for the
  sign convention already adopted in this project).

**Verbatim quotes:**
- "Capsules: 1/2" Low noise Pre-polarized condenser on 60UNS thread. Sensitivity: -31.9 dBfs (94 dB
  SPL. 1 kHz). Noise level: -105.3dBfs (A) @ 0 dB gain. MAX SPL(0dBfs): 125dB SPL." (UMIK-2 brief, p. 2)
- "Capsule Type & Polar pattern: 6mm electret, Omni-Directional" … "Frequency response: 20 Hz -
  20kHz +/-1dB with calibration loaded" … "Calibration file: Unique microphone calibration .txt
  file referenced to the Serial Number. Includes on axis & 90deg - Frequency / Amplitude /
  Sensitivity drift" (UMIK-1 brief, p. 1)
- "Each UMIK-2 has a unique calibration file for measurement accuracy." (UMIK-2 manual, §1)
- "Two calibration files are provided: an on-axis calibration file measured from the actual
  microphone, and a 90-degree calibration file that is calculated from the on-axis response." (UMIK-2
  manual, §4)

---

## Answers to the thread questions

**Q1 — Published evaluations of UMIK-1/UMIK-2 (or comparable low-cost mics) vs. class-1
references; unit-to-unit spread; low-frequency response; drift; capsule; vendor accuracy claims.**

No published evaluation of the UMIK-1 or UMIK-2 *specifically* against a class-1 reference was
found (searched arXiv, MDPI Sensors/Applied Sciences, DAGA/Inter-Noise/Euronoise/ICSV/Forum
Acusticum proceedings, and general web search — see RETRIEVAL-D.md for the queries used; only
non-peer-reviewed forum/blog material turned up and was excluded as evidence). What is retrieved is
the closely comparable case of **other USB/low-cost measurement microphones benchmarked against
Class-1 (IEC 61672) references**, which bounds what to expect: Risojević et al. (2018) report
"mean difference of less than 2 dB" (§4 above, p. 1) and, in real use, 1.6 dB (p. 16); Picaut et
al.'s review (2020) relays ±1.5 dB (Peckens et al. 2018) and a "systematic offset around 3 dB"
(MONZA project) for other MEMS/electret nodes (§5, p. 7); Mydlarz et al. (2016) publish a full
per-frequency table (§6, Table 3, p. 18) showing the residual after a single-point offset
calibration growing from 0.1–0.4 dB at low/mid frequencies to **2.6 dB at 8 kHz** against a Type-1
reference — i.e. even a careful, published low-cost-mic calibration leaves multi-dB, frequency-
dependent residuals that only partly resemble a flat gain error. On capsule and vendor claims: the
UMIK-2 uses a "1/2" Low noise Pre-polarized condenser" capsule and the UMIK-1 a "6mm electret"
(§11–13, both from miniDSP's own documentation); miniDSP states a **±1 dB, 20 Hz–20 kHz** flatness
figure for the UMIK-1 "with calibration loaded" but **no equivalent numeric accuracy or tolerance
figure for the UMIK-2, nor for the Sens Factor itself, was found in either UMIK-2 document read**
— a documented gap, not an oversight in this search. No source gives a UMIK-specific
unit-to-unit spread number; the only concrete quantitative unit-to-unit information for a
comparable device is the 76-microphone NIST drift-rate study (Q3, not Q1) and Garg's own
bilateral-comparison figures (<0.16 / <0.25 dB, §1) for full laboratory-grade reference
microphones, which is a different (better) population than consumer USB mics.

**Q2 — Standard methods for checking a mic's sensitivity/response in situ.** Answered in depth:
comparison/substitution calibration under IEC 61094-8, worked fully in Garg (2019, §1) with a
complete uncertainty budget (0.30–0.52 dB, k=2, across 125 Hz–20 kHz — narrower in the abstract's
own rounding, 0.36–0.52 dB, than the full Table 4; see "Comparison with earlier notes" below) and
the historical reciprocity benchmark in Burnett & Nedzelnitsky (1987, §2: 0.16/0.07 dB). The
electrostatic-actuator method is IEC 61094-6 (§8), explicitly scoped to *frequency-response
changes* rather than absolute sensitivity — usable in situ without an acoustic facility. The sound
calibrator/pistonphone route is IEC 60942 (§9): class LS/1/2, with class 1/M and LS/M pistonphone
variants requiring stated static-pressure corrections. On rotation/round-robin/Latin-square
designs specifically for microphones, **no acoustics-specific source was retrieved** (the one
promising lead, an IEEE paper on rotating microphones through positions for array gain
calibration, is paywalled — see RETRIEVAL-D.md); the generic metrology principle it would
implement is answered instead from mass metrology, Cameron, Croarkin & Raybold (1977, §10):
designed intercomparisons with a restraint and a check standard, solved by least squares to
separate individual-standard values from a common nuisance effect — mathematically the same
operation `scripts/arc_error_map.py` performs to separate mic offset from position error.

**Q3 — Sensitivity drift/ageing of electret/MEMS capsules, magnitude over time and temperature.**
Best-characterized baseline (laboratory condenser mics, not electret/MEMS, but the gold standard
for comparison): Wagner & Guthrie (2015, §3) find **average drift not significantly different from
zero**, bounded to a few thousandths to ~0.02 dB/year, from 484 calibrations of 76 microphones over
up to 50 years. For MEMS specifically: temperature coefficients of **<0.017 dB/°C** (Mydlarz et
al. 2016 citing Scheeper et al. 2003, §6) and **"in the order of ±1 dB over 100 Hz–8 kHz" for
−5…40°C** (Picaut et al. 2020 citing Barham & Goldsmith 2008, §5) — consistent with each other in
order of magnitude (0.017 dB/°C × 45°C ≈ 0.77 dB). Ageing/running-in: **"1–2 dB … over a time
period of 4 months"** during the initial running-in phase of MEMS mics in the MONZA project
(Picaut et al. 2020 citing Bartalucci et al. 2018, §5), and corrosion-stress testing showing
"wire bond corrosion and membrane embrittlement … after 90 days" with only slight frequency-
response impact (Picaut et al. 2020 citing Li et al. 2014, §5). Garg's own reference PCB 377B02
condenser microphone (not MEMS) shows a real multi-year spread of up to 0.55 dB at 16 kHz and
0.39 dB at 12.5 kHz across 2015–2018 (§1, Table 3), though the paper's own Type-A "repeatability"
statistic for that same data (0.07 dB) is the standard error of the mean, not the raw spread — the
two are easily conflated and answer different questions.

**Q4 — Distinguishing a flat sensitivity (offset) error from a frequency-response shape error.**
No source gives a named textbook definition of this distinction, but three independent pieces of
quoted evidence bear on it directly: (a) Picaut et al. (2020, §5, p. 14) explicitly contrast "the
same correction … applied to the entire temporal signal, without distinction of frequency or
amplitude" (a flat correction) against a "more advanced way [that] can also correct linearity
defects in level and frequency" (a shape-resolved correction); (b) Mydlarz et al. (2016, §6, p. 16)
implement exactly that distinction as two separate pipeline stages — an "inverse frequency response
filter" (shape) and a single-point "offset adjustment … to match the 94dBA SPL input level" (flat
level) — and their own Table 3 (p. 18) is the empirical demonstration that doing the offset
correction alone (or the shape correction imperfectly) leaves a residual that *grows with
frequency* (0.1 dB at 63 Hz to 2.6 dB at 8 kHz), which is how a shape error is distinguished from
an offset error in practice: an offset error is constant across frequency, a shape error is not;
(c) IEC 61094-6 (§8) institutionalises the same split at the standards level — the electrostatic
actuator method is explicitly for "detecting changes in the frequency response," a different
standard and a different measurement from the pressure/free-field reciprocity methods (IEC
61094-2/3) that give the single-number absolute sensitivity. None of this is UMIK-specific, but
applied to 811-1892: its symptom (2–6 dB low, calibrated, but only ~1 dB low raw, over a bounded
125 Hz–2.5 kHz band, with an outlier Sens Factor) is a *shape*-plus-*offset*-interaction signature
— consistent with a Sens Factor that doesn't match the unit paired with a calibration curve that
otherwise looks normal, which is exactly the kind of fault Q4 anticipated but which none of the
retrieved sources diagnose in those specific terms.

---

## Comparison with earlier notes

**Garg et al. 2019 (papers/chamber-problems/MATRIX-3W.md, row 12).** The matrix row reads: "Garg
et al. 2019, MAPAN 34 | journal | Free-field microphone calibration in a 2 m³ box | ISO 26101
traverse 125 Hz–20 kHz, uncertainty budget | 125 Hz: +4.52 → −7.13 dB over 0.64–1.14 m; tolerance
only 'between 79 and 89 cm'; U = 0.36–0.52 dB." The chamber/traverse numbers (125 Hz deviation
range, 79–89 cm usable working space) were **not independently re-verified in this pass** (this
thread only re-read the calibration-uncertainty content, not the free-field-traverse figures in
Figs. 4–5, which are a different question). The uncertainty figure the row states, **"U =
0.36–0.52 dB,"** matches the paper's own abstract exactly — but re-reading Table 4 in full (this
thread, §1 above) shows that number is the abstract's own rounding/simplification, not the full
range in the paper's own table: Table 4's seven per-band expanded-uncertainty values are 0.45,
0.30, 0.36, 0.36, 0.42, 0.48, 0.52 dB, i.e. the true min/max is **0.30–0.52 dB**, and the
lowest-frequency band (125–200 Hz) is actually the *worst*, at 0.45 dB, not the best — neither of
which is visible from the abstract's "0.36–0.52 dB" or from the matrix row that reproduces it. This
is not a transcription error by the earlier note (it accurately quotes the abstract) but it is an
internal inconsistency in the source paper itself between what its abstract/conclusion claims and
what its own Table 4 shows, worth flagging since a reader relying on the abstract alone would
underestimate the uncertainty at the lowest frequency band by 0.15 dB and overestimate it in the
250 Hz–1 kHz band by 0.06 dB.

**Burnett & Nedzelnitsky 1987 (papers/small-chamber/EXTRACTS.md, entry 1).** Re-read fresh and
compared quote-by-quote against the existing entry: chamber dimensions ("free volume of 5.4 m³,"
"fiberglass wedges are 0.3 m deep," printed p. 136), all three verbatim quotes about the two
reflection mechanisms (printed pp. 140–141), and the headline uncertainty figures ("0.16 dB or
better … 0.07 dB or better," abstract, printed p. 129) **all matched exactly**, including the
specific page numbers already recorded. **No discrepancies found.** This thread used the paper only
for its abstract's reciprocity-method uncertainty figure as Q2 context; the earlier note's chamber-
reflection content (its main subject) was not re-used here and is outside this thread's scope.
