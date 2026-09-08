# Extracts — Thread C: tone-on-the-band-edge (third-octave bands, RPM jitter, tone/broadband separation, order-domain analysis)

Compiled 2026-09-08. Every quote below was verified by this agent against a fresh `pdftotext` (or,
where noted, a page-rendered visual read or an archive.org OCR transcript) of the PDF named. Page
numbers are the **printed** page number confirmed from the page's own footer/header, not a line-count
guess — see the "how confirmed" note under each source where it matters.

---

## 1. Cunefare, Biesel, Tran, Rye, Graf, Holdhusen & Albanese (2003) — JASA 113(2), 881–892
**File:** `papers/anechoic-simulation/Cunefare_2003_JASA_chamber-qualification-traverse-fit-signal.pdf`
(held; re-extracted fresh to `papers/arc-validation/refetch-txt/Cunefare_2003_JASA_chamber-qualification-traverse-fit-signal.txt`, plain `pdftotext -q`). Identity confirmed from p.881 masthead: title, all seven author names, DOI 10.1121/1.1527595 match `papers/BIBLIOGRAPHY.md`.
**Evidence level:** I — peer-reviewed journal (JASA).
**How confirmed:** printed page numbers read from each page's own footer using `pdftotext -f N -l N`, not inferred from line position in the concatenated dump (footers for this PDF sit inline in the text stream, page 1 of the *file* is a citation cover page inserted by the host, so PDF-page-2 = printed p.881, PDF-page-3 = p.882, … PDF-page-13 = p.892).

**What it says (Q3):** This is the closest held source to Q3, but it does **not** discuss deliberate RPM
variation or "warble" tones — it discusses **pure tone vs. broadband-noise excitation** of a static
loudspeaker source, and its conclusion runs opposite to the "averaging smooths interference dips
beneficially" framing in Q3: broadband (frequency-smeared) excitation is shown to be a *worse*, more
forgiving indicator of real chamber defects than a swept/stepped pure tone, precisely because
frequency-averaging hides the same interference structure that narrow-band data reveals.

- Abstract (p. 881): *"The current practice of using widely space discrete sampling along a traverse is
  shown to inadequately sample the complexity of the sound field extant with pure tone traverses, but is
  suitable for broadband traverses. … the use of broadband noise as the test signal, as compared to pure
  tone traverses over the same span, is demonstrated to be a marginal indicator of chamber performance."*
- Conclusion (p. 892): *"In light of the marked differences between the pure tone and broad band noise
  traverses observed in our facility, it is our opinion that the use of broadband noise as the test sound
  signal is of dubious value for qualification purposes in chambers where sources with pure tone
  components are to be tested."*
- Method detail for how they excited/measured tones (p. 886): *"The time data was digitally band-pass
  filtered about the excitation frequency of interest. One-third octave and full octave filters were used
  for broadband noise excitations as appropriate to the test frequency. For pure tone excitations a narrow
  band-pass filter (bandwidth = 1/20 of the center frequency) was used to improve the signal-to-noise
  ratio."*

No mention of "warble," "modulated," "swept," or "beating" anywhere in the text (grepped the full
re-extracted dump) — the paper's test signals are strictly *stationary* pure tones or stationary broadband
noise, never a frequency-varying tone.

---

## 2. ISO 26101-1:2021 — *Acoustics — Test methods for the qualification of the acoustic environment — Part 1: Qualification of free-field environments* (iTeh preview, Foreword–5.1.5.1.2)
**File:** `papers/anechoic-simulation/ISO-26101-1_2021_standard-preview_free-field-qualification.pdf`
(held; re-extracted to `refetch-txt/ISO-26101-1_2021_standard-preview_free-field-qualification.txt`).
**Evidence level:** VII — standard (sample only; Annex A tolerances not in the preview).
**How confirmed:** page footers via `pdftotext -f 11 -l 11` → printed p. 5 for both quotes below.

**What it says (Q3):** The preview allows a **band-limited or broad-band noise** test signal as one of
four options (alongside pure tone, multiple pure tones, or a combined "mix"), and gives one operational
reason for using multiple simultaneous tones — speed, not interference-averaging:

- (5.1.4.2, p. 5): *"The test sound source described in 5.1.2.2 may be operated with a test signal of pure
  tones, multiple pure tones, band-limited or broad-band noise. If pure tones or multiple pure tones are
  used for discrete-frequency qualification, the measured signal after any filtering shall not contain
  energy at frequencies not being characterized that are within 15 dB of the frequencies being
  characterized. … NOTE Use of a mix of pure tones spaced apart by more than a one-third-octave band can
  be much more rapid than sequential traverses, each at a single pure tone. When using tonal or mixed tone
  signals, care should be taken to avoid distortion due to excessive signal levels."*

This is **not** a warble/swept tone (each component is stationary), and the standard gives no rationale
tying broadband/band-limited noise to smoothing interference nulls — that rationale (and its *rejection*
as unreliable) is what Cunefare 2003, above, actually argues. Grepped the full re-extracted dump for
"warble," "swept," "modulat," "interference," "standing wave" — only one hit, unrelated (monitor-mic
placement, p. not relevant to test-signal type).

---

## 3. ISO 5305:2024 — *Noise measurements for UAS (unmanned aircraft systems)* (iTeh preview, Foreword–7.3.1)
**File:** `papers/anechoic-simulation/ISO-5305_2024_standard-preview_UAS-noise-measurement.pdf`
(held; re-extracted to `refetch-txt/ISO-5305_2024_standard-preview_UAS-noise-measurement.txt`).
**Evidence level:** VII — standard (sample only).
**How confirmed:** `pdftotext -f N -l N`; footers read "vi" (PDF p. 6) and "6" (PDF p. 12).

**What it says (Q1/Q2):** Directly on point for Q2's "recommended practice: report tones separately" —
and it explicitly **declines** to specify how:

- Introduction (p. vi): *"This document focuses on the methods of measuring the sound pressure signals
  of the UAS under different working conditions, based on which post-processing of the recorded data can
  be conducted. For example, by computing the narrow-band noise spectra, the tonal noise components can
  be extracted. However, requirements for signal processing and evaluation of the measured data are not
  specified in this document."*
- Clause 6.2 (p. 6), on why: *"For sound at a high frequency, the significant interference pattern can
  affect the validity of the far-field condition proposed in Formula (1). However, the effect can be
  minimized when summing in a frequency band, for example, a 1/3-octave band, is performed."*
- Clause 6.1/7 (p. 5, Table 1 clause, p. 6–8): requires filters meeting **IEC 61260-1** Class 1 (*"Filters
  shall meet the requirements for a class 1 instrument according to IEC 61260-1"*), i.e. ISO 5305 itself
  hands the filter-shape question straight to IEC 61260-1 (source 8, below) rather than answering it.

So the one internationally-current UAS noise standard we hold (a) endorses narrow-band spectra as *the*
way to extract tones but sets no bin width/averaging rule, and (b) endorses summing into 1/3-octave bands
specifically to fight spatial interference, with no discussion of what that summing does to a tone that
straddles a band edge.

---

## 4. Weitsman, Stephenson & Zawodny (2020) — JASA 148(3), 1325–1336, "Effects of flow recirculation on acoustic and dynamic measurements of rotary-wing systems operating in closed anechoic chambers"
**File:** `papers/chamber-problems/Weitsman_2020_JASA_recirculation-rotary-wing-closed-chambers.pdf`
(held; re-extracted to `refetch-txt/Weitsman_2020_JASA_recirculation-rotary-wing-closed-chambers.txt`).
Identity confirmed from title page (title/authors/DOI 10.1121/10.0001901 match bibliography).
**Evidence level:** I — peer-reviewed journal.
**How confirmed:** every page number below was read directly off that page's own printed footer using
`pdftotext -f N -l N` (PDF page 2 footer = "1325", so PDF page = printed page − 1323 for this file) —
**not** inferred from where a footer-like string happens to sit in the concatenated dump, which for this
PDF is misleading (the running head/footer block for page *N* is emitted by pdftotext attached to the
*end* of page *N*'s own text, immediately followed by the *next* page's header, so a naive "nearest
footer" read of the merged file put one of the numbers below on the wrong page on a first pass; the
per-page `-f/-l` extraction is authoritative and is what is cited).

**What it says — RPM stability under ESC control (Q3):** DJI 2312A motor + off-the-shelf ESC + PWM
controller (Pololu Mini Maestro), closed-loop, no deliberate speed dither:
- p. 1327: *"In this region [the clean pre-recirculation window, 3.5–7.4 s] … the mean thrust of 0.76 lbf
  (3.38 N) and the width of the thrust envelope remain constant. There are also minimal fluctuations in
  the RPM."*
- pp. 1327–1328: *"The effects of recirculation becomes evident 7.4 s after the beginning of the trial …
  The SPL of the BPF harmonics fluctuate due to the variety of the coherent structures being ingested by
  the rotor. The mean thrust … remains constant, while the width of the thrust envelope modulates. There
  are also evident fluctuations in the RPM. These features persist throughout the remainder of the trial
  and are indicative of an increase in unsteady loading on the rotor blades."*
- p. 1333 (comparing mesh configurations): *"there are minimal fluctuations in the rotational rate"*
  (baseline, no aerodynamic disturbance).

So on this rig, a small BLDC rotor under closed-loop ESC control holds RPM essentially steady **as long as
the aerodynamic load is steady**; the RPM jitter that does appear is tied to unsteady inflow (recirculation
ingestion), not to the ESC/PWM control loop itself.

**What it says — tone extraction method (Q2):** p. 1327: *"The periodic noise components are extracted by
calculating the RMS of the ensemble-averaged pressure time history over a specific number of shaft
revolutions. This tonal extraction technique is well documented by Zawodny et al.⁵"* — reference 5 is
confirmed (p. 887 reference list) to be **Zawodny, N. S., D. D. Boyd, Jr., and C. L. Burley, "Acoustic
Characterization and Prediction of Representative, Small-Scale Rotary-Wing Unmanned Aircraft System
Components," 72nd AHS Annual Forum, 2016** — i.e. source 10 below, confirming that paper is the origin of
the ensemble-per-revolution-RMS method used across this whole family of NASA Langley small-rotor papers.

**What it says — averaging length vs. band-level uncertainty (Q4):**
- p. 1328–1329: *"The spectral average prior to the onset of recirculation was computed between 4 and 6 s
  … while the average following the onset of recirculation was computed between 9 and 11 s into the run.
  With a frequency resolution of 5 Hz, this averaging interval yields an autospectral random uncertainty
  of εr = 22.80%, which results in a random SPL uncertainty of u_r,SPL ∈ {−1.12, +0.89} dB."* (i.e. a
  **2 s** average, Hanning, 75% overlap, Δf = 5 Hz.)
- p. 1333: *"The spectral average prior to the installation of the mesh treatment was computed over the
  same two second interval as the spectra in Fig. 4, while the spectral average following the installation
  of the treatment was computed over a duration of 7 s. This extended averaging interval yields an
  autospectral random uncertainty of εr = 11.85%, which translates to a random SPL uncertainty of
  u_r,SPL ∈ {−0.55, +0.49} dB. The effect of decreasing the random SPL uncertainty is evident by the
  reduction in variance of the SPL at frequencies exceeding 1 kHz."*

So: **2 s → ±1.1 dB-ish (22.80% ε_r); 7 s → ±0.5 dB-ish (11.85% ε_r)** — the two numbers in the shared
protocol background are correct individually but belong to *different* averaging windows, not both to a
2 s spectrum (flagged in the Comparison section below and in the Q4 answer).

---

## 5. Whelchel (2023) — PhD dissertation, Virginia Tech, "Measurement and Prediction of Rotor Noise Sources for sUAS in Outdoor and Laboratory Environments"
**File:** `papers/chamber-problems/Whelchel_2023_PhD-VT_sUAS-rotor-noise-outdoor-lab.pdf`
(held; re-extracted to `refetch-txt/Whelchel_2023_PhD-VT_sUAS-rotor-noise-outdoor-lab.txt`, 6651 lines).
**Evidence level:** III — doctoral thesis.
**How confirmed:** printed page = PDF page − 16 (confirmed by reading footers on PDF pp. 96–99 → "80,
81, 82, 83" and PDF pp. 108–112 → "92, 93, 94, 95"). All page numbers below are the **printed** thesis
page.

**What it says — averaging time vs. uncertainty for a tonal-plus-broadband rotor spectrum (Q4),** §5.1.2
(9450S rotor, BPF ≈ 175 Hz, no screens, sampled at 65 536 Hz, 16 384-sample records):
- p. 81: *"the spectral levels at the BPF and its harmonics were observed independently with varying
  averaging time. … These integrated spectral quantities were calculated over a 28 Hz band centered on the
  BPF and its corresponding harmonics. … the spectral uncertainty for the ith FFT averaging time was
  computed as εᵢ = 2σ/√Nᵢ, where Nᵢ is the number of records for the 2, 4, 6, 8, 10, 12, 16, 20, and 28
  second averaging times. Given that these data were sampled at 65536 Hz and processed with a record
  length of 16384, the number of records from the shortest to longest averaging times were 15, 31, 47, 63,
  79, 95, 127, 159, 223."*
- pp. 81–82: *"Error bars have been plotted on the curve of the tone at the BPF and are initially under
  2 dB and decrease in width with increasing spectral averaging times."*
- p. 82: *"Even at the lowest FFT averaging window of 2 seconds with 15 records the uncertainty is under
  1 dB."* — and again on p. 83 for a different screen configuration: *"Uncertainties at the BPF are also
  under 1 dB for all time windows."*
- p. 82 (a **confound** to flag, not a pure statistics effect): *"The BPF increases by nearly 3 dB between
  the 2 s and 4 s sample window. … The BPF and its harmonics are all shown to increase by at least 7 dB
  with increasing averaging time suggesting that the turbulent wake is being reingested."* — i.e. part of
  the level's dependence on averaging time in this dataset is real recirculation contamination growing
  with run time, not sampling variance; Whelchel's own uncertainty numbers above are computed net of this
  from repeat-record statistics, but a reader must not treat "level changes with averaging time" as proof
  of a variance effect alone.

**What it says — tone/broadband decomposition method (Q2),** §5.1.3 "Separation of Tonal and Broadband
Components," p. 94:
- *"The periodic and random noise components are separated in the time domain using a phase average
  interpolation technique like that of Zawodny and Boyd [6]. … First the rotor position is tracked in time
  using the measured pulse from the RPM signal acquired with the laser diode. … Tᵣₑᵥ is not constant as
  the RPM varies throughout the measurement which requires the measured acoustic pressure time history to
  be interpolated onto an evenly spaced grid of nᵢₙₜ points [per Nᵣₑᵥ interpolation region] … An average of
  these is then computed which yields the phase averaged acoustic pressure … This resultant phase averaged
  acoustic pressure is then replicated Nᵣₑᵥ times yielding the mean acoustic pressure rotor revolution time
  history. … The mean acoustic pressure rotor revolution time history is then subtracted from that of the
  total acoustic pressure time history yielding the broadband component."*
- p. 96: *"Narrowband spectra of the total, tonal, and broadband can then be computed using a Hanning
  window of 50% overlap and a frequency resolution of 4 Hz. … High frequency oscillations associated with
  the electric motor were included during the initial calculations of the phase-averaged acoustic pressure
  and were removed by applying a low pass filter to the mean rotor revolution time series data in the form
  of a moving average. The moving average window was designed to remove these high frequency tones which
  corresponds to a window size of approximately 4.2° of rotation or approximately 7144 Hz at 5715 RPM."*

Note the citation: **"Zawodny and Boyd [6]"** — two authors, confirmed in the reference list (p. — full
citation: *"Zawodny, N. S., and Boyd, D. D. 'Investigation of Rotor–Airframe Interaction Noise Associated
with Small-Scale Rotary-Wing Unmanned Aircraft Systems.' Journal of the American Helicopter Society"*) —
this is a **different**, two-author Zawodny/Boyd paper (JAHS), not the three-author Zawodny/Boyd/Burley
2016 AHS Forum paper that Weitsman (source 4) cites for the RMS-per-revolution method. Both papers are
from the same NASA Langley small-rotor-acoustics programme and describe closely related, but not
identical, per-revolution decomposition techniques; this thread retrieved the three-author 2016 paper
(source 10) but not the two-author JAHS one.

This method requires a **shaft/optical tachometer signal**, which our rig does not have — directly
relevant to why "BPF must be read from the audio" (protocol background) is the harder, RPM-blind version
of the same problem these theses solve with an RPM channel.

---

## 6. Zawodny & Haskin (2017) — AIAA Aeroacoustics Conference, "Small Propeller and Rotor Testing Capabilities of the NASA Langley Low Speed Aeroacoustic Wind Tunnel"
**File:** `papers/chamber-problems/Zawodny-Haskin_2017_AIAA_LSAWT-small-rotor-capabilities.pdf`
(held; re-extracted to `refetch-txt/Zawodny-Haskin_2017_AIAA_LSAWT-small-rotor-capabilities.pdf.txt`,
plain `pdftotext -q`, LaTeX/pdfTeX source — clean text extraction).
**Evidence level:** VI — conference paper.

**What it says — plotting the harmonic level, not the band level, in a directivity/polar plot (Q5):**
- *"Finally, BPF directivity comparisons are made between PAS predictions and LSAWT measurements for
  several different rotor rotation rates in Fig. 18. These rotation rates were selected for comparison
  since they correspond to BPFs that are near the anechoic cut-on frequency of LSAWT of approximately
  200 Hz."* Figure 18's x-axis is printed as **"BPF SPL (dB re. 20 μPa)"** against elevation angle θ (−60°
  to 15°), for Ω = 4800/5400/6000 RPM → BPF = 160/180/200 Hz.
- Uncertainty of the underlying narrowband processing (same family of methods as sources 4/5/10): *"a
  total of twenty seconds of data were acquired at a sampling rate of 80 kHz, the first five seconds of
  which were FFT block-averaged using a Hanning window with 75% overlap. The resulting acoustic spectra
  have an autospectral random uncertainty of u_rSPL = ±0.6 dB."*
- On why this particular facility can even resolve BPF directivity near its own cut-on: *"the LSAWT
  microphones are mounted an average distance of 0.49 m from the acoustic wedge tips … Treating this as a
  1/4-wavelength yields a notional cut-on frequency of 175 Hz. This appears to be a reasonable
  approximation of the low-frequency capability of LSAWT based on the BPF directivity results of Fig. 18."*

---

## 7. Alkmim, Cardenuto, Tengan, Dietzen, Van Waterschoot, Cuenca, De Ryck & Desmet (2022) — JASA 152(5), 2735–2745, "Drone noise directivity and psychoacoustic evaluation using a hemispherical microphone array"
**File:** `papers/chamber-problems/Alkmim_2022_JASA_drone-directivity-hemispherical-array.pdf`
(held; re-extracted to `refetch-txt/Alkmim_2022_JASA_drone-directivity-hemispherical-array.txt`).
**Evidence level:** I — peer-reviewed journal.

**What it says — polar/directivity plots at the harmonic frequency, not the band (Q5):**
- p. 2740: *"Figure 6 shows the magnitude of the estimated directivity pattern for the real component of
  the sound pressure field considering a third-order spherical harmonics basis. The directivity is shown
  for the 4732, 4987, and 6152 rpm rotor speeds at their respective BPFs (158, 166, and 205 Hz,
  respectively)."*
- p. 2740–2741: *"Figure 7 shows the spectral SPL in polar coordinates with respect to elevation for three
  rotor speeds at their respective BPFs. The directivity pattern is derived from the third-order spherical
  harmonic decomposition."*
- On why BPF specifically, not a band: the array's spatial-aliasing ceiling is BPF-limited — *"Spatial
  aliasing above fmax = 163.77 Hz for 3rd-order SHD (R = 1 m) … valid only up to 1st BPF below 4900 rpm"*
  (p. 2739) — so the directivity reconstruction is only trustworthy exactly at the BPF tone in the first
  place, reinforcing why these groups plot the tone level rather than a band that would include
  higher-order (aliased) content.

---

## 8. IEC 61260-1:2014 — *Electroacoustics — Octave-band and fractional-octave-band filters — Part 1: Specifications* (iTeh preview, 15 of 37 pp.)
**File:** `papers/arc-validation/IEC-61260-1_2014_standard-preview_octave-fractional-octave-band-filters.pdf`
(NEW; `pdftotext -q` → `papers/arc-validation/txt/…txt`). Identity confirmed on p. 1: "IEC 61260-1,
Edition 1.0 2014-02 … Electroacoustics – Octave-band and fractional-octave-band filters – Part 1:
Specifications."
**Route:** iTeh sample, `https://cdn.standards.iteh.ai/samples/13383/3c4ae3e762b540cc8111744cb8f0ae8e/IEC-61260-1-2014.pdf`.
**Evidence level:** VII — standard (sample only; the numeric acceptance-limit Table 1, referenced in the
preview's own table of contents at p. 15, is **not** included in the 15-page free sample — the sample
stops mid-clause 5.5, one clause short of it. This is an honest gap: **IEC 61260-1's own numeric
band-edge attenuation table could not be retrieved**; source 9 (ANSI S1.11-2004, a technically-aligned
counterpart standard, full text) supplies the missing numbers instead — see below).
**How confirmed:** printed pages read via the "– N –" footer pattern (`pdftotext -f N -l N`); e.g. PDF
page 11 → printed p. 9, PDF page 15 → printed p. 13.

**What it says (Q1) — the official definitions that frame the problem:**
- Definitions, p. 9: *"3.8 band-edge frequencies: frequencies at the lower and upper edges of the
  pass-band of a band-pass filter such that the exact mid-band frequency is the geometric mean of the
  lower and upper band-edge frequencies."* (Consistent with our own bands: √(224 × 282) ≈ 251 Hz ≈ the
  250 Hz nominal centre.)
- p. 9 also defines *"3.7 normalized frequency: for a band-pass filter, ratio of a frequency to the
  corresponding exact mid-band frequency"* and *"3.9 normalized bandwidth of a filter: … the ratio of the
  upper band-edge frequency minus the corresponding lower band-edge frequency to the exact mid-band
  frequency."*
- p. 13, NOTE 1 under Clause 5.4.2 (mid-band frequency formulae): *"The outputs of narrow-bandwidth
  fractional-octave-band filters that have exact mid-band frequencies determined from Formula (2) or
  Formula (3) can be combined to approximate the band level indicated by a filter of wider bandwidth with
  a corresponding exact mid-band frequency and corresponding band-edge frequencies."* — i.e. IEC's own text
  endorses building a wide band's level from many narrow (fine-FFT-bin) sub-band levels rather than a
  single physical filter, which is exactly the route to avoiding the discrete two-band all-or-nothing
  assignment our own third-octave analysis currently makes.

---

## 9. ANSI S1.11-2004 — *American National Standard Specification for Octave-Band and Fractional-Octave-Band Analog and Digital Filters*
**File:** `papers/arc-validation/ANSI-S1.11_2004_standard_octave-fractional-octave-filters.pdf` (the
official law.resource.org PDF scan of the CFR-incorporated-by-reference copy, 31 pp., largely
image-only) **plus** `papers/arc-validation/txt/ANSI-S1.11_2004_standard_octave-fractional-octave-filters.txt`
(the archive.org OCR full-text transcription of the same document, used for all quotes below because the
scanned PDF itself has no usable text layer beyond its cover page).
**Route:** PDF — `https://law.resource.org/pub/us/cfr/ibr/002/ansi.s1.11.2004.pdf` (this ANSI/ASA standard
is one of the relatively rare ones with a legitimate, complete, freely-hosted copy, because 49 CFR 227
incorporates it by reference and `law.resource.org` publishes IBR standards for that reason — confirmed
by the PDF's own cover sheet: *"By the Authority Vested … the attached document has been duly
INCORPORATED BY REFERENCE … Document Name: ANSI S1.11 … CFR Section(s): 49 CFR 227."*); OCR text —
`https://archive.org/download/gov.law.ansi.s1.11.2004/ansi.s1.11.2004_djvu.txt`.
**Evidence level:** VII — national standard, full text (via OCR transcription — flagged, same tier as the
already-held Beranek 1945 OSRD "GPO OCR transcription" per `papers/BIBLIOGRAPHY.md`). This is the
technically-aligned US counterpart to IEC 61260 (ANSI/ASA S1.11-2014/Part 1 is the current edition
literally co-badged with IEC 61260-1:2014); the 2004 edition predates the IEC/ANSI merger but uses the
same class 0/1/2, same normalized-frequency-ratio Ω = f/fₘ formalism, and (by the numbers below) is
consistent with what IEC 61260-1's un-retrievable Table 1 is known (from its own preview's cross
references) to contain the same kind of tolerance mask for.
**How confirmed:** identity from the OCR'd cover/title page (*"ANSI S1.11-2004 … AMERICAN NATIONAL
STANDARD SPECIFICATION FOR OCTAVE-BAND AND FRACTIONAL-OCTAVE-BAND … FILTERS"*) and from the table of
contents giving Table 1 → p. 8, Annex B/Table B.1 → pp. 14–15, which is the pagination cited below. This
is an **OCR transcription of a scanned document**, so the table's row *labels* (the Ω = G^x column) are
partly garbled by the OCR (superscripts and Greek-letter symbols do not survive scanning); the *numeric*
values are legible and, for Table B.1, independently self-checking (see below).

**What it says (Q1) — this is the actual numeric answer the "−3 dB at the edge" folk‑statement is
usually a loose paraphrase of, and the real numbers are not −3 dB:**

Clause 4.4.4, p. 8: *"Figure 1 illustrates the limits on minimum and maximum relative attenuation for an
octave-band filter. The figure also shows the discontinuous changes in minimum and maximum relative
attenuation at the bandedge frequencies and the linear variation of relative attenuation limits between
the breakpoint normalized frequencies of table 1."*

**Table 1** (octave-band filters), p. 8 — at the octave band edge (Ω = G^½, the geometric-mean point
between adjacent 1/1-octave centres):

> minimum; maximum attenuation limits, in decibels — class 0 / class 1 / class 2:
> **+2.3; +4.5 / +2.0; +5.0 / +1.6; +5.5** dB

(immediately followed, one octave further out at Ω = G¹, by +18.0/+17.5/+16.5 dB minimum, ∞ maximum — the
"discontinuous change" the clause text refers to is the *minimum* bound jumping from a small negative
number just inside the passband to +2.0…+2.3 dB right at the edge.)

**Table B.1** (one-third-octave-band filters, Annex B, pp. 14–15) — at the 1/3-octave band edge, printed
as normalized frequency *f/fₘ* = **1.122,02 (base-ten) / 1.122,46 (base-two)**:

> minimum; maximum attenuation limits, dB — class 0 / class 1 / class 2:
> **+2.3; +4.5 / +2.0; +5.0 / +1.6; +5.5** dB (footnoted "a" — coincident with the bandedge, cf. the
> discontinuity rule above)

This agent independently verified the breakpoint frequency itself rather than trusting the OCR row label:
2^(1/6) = 1.122462…, which matches the printed "base-two" value 1.122,46 to 5 significant figures — i.e.
the row is unambiguously the 1/3-octave band-edge row (224/1.1225 ≈ 200 Hz-side edge; 282×1.1225⁻¹ ≈
251 Hz-side edge — consistent with our own arc-validation band edges of 224 Hz/282 Hz around a 250 Hz
centre, and by symmetry ≈179/1.1225 ≈ 200 Hz-side for the 200 Hz-band's own upper edge).

**So:** a Class-1 real (non-ideal) 1/3-octave filter is required to sit somewhere **between 2.0 dB and
5.0 dB down** exactly at its nominal edge — not a single fixed "−3 dB / half-power" point. The −3.01 dB
half-power figure sometimes quoted for "the" band edge is a property of a specific idealized (e.g.
2-pole Butterworth) design, not a number this standard mandates; the standard instead defines the edge
purely geometrically (source 8, §3.8) and brackets its attenuation with a tolerance *envelope*, which
happens to straddle −3 dB but is not centred on it (2.0–5.0 dB, class 1). A tone sitting exactly at a
band edge is, by construction, only partially rejected by both of its neighbouring filters at once (each
one down by roughly 2–5 dB, not fully in or fully out) — which is the standards-grounded version of "a
tone at the edge contributes to both bands," and explains why a small BPF shift across the true 224 Hz
edge does not move all the energy cleanly from one third-octave bin to the other: real filters (and our
own FFT-then-band-sum, which behaves like an even sharper/more discontinuous version of the same idea)
both leave a transition region where the energy split is graded, not binary — but a graded split over
only a few dB of overlap is still enough, combined with the FFT-bin/PWM-linked BPF drift documented in
the Q3/Q4 sources above, to produce the ±11 dB single-cell swings we observe when *most* of a tone's
energy tips from one side of the (comparatively sharp, effectively brick-wall for an FFT-then-sum
implementation) edge to the other from run to run.

---

## 10. Zawodny, Boyd Jr. & Burley (2016) — 72nd AHS Annual Forum Proceedings, "Acoustic Characterization and Prediction of Representative, Small-Scale Rotary-Wing Unmanned Aircraft System Components"
**File:** `papers/arc-validation/Zawodny-Boyd-Burley_2016_AHSForum_UAS-rotor-acoustic-characterization.pdf`
(NEW). **Route:** NASA NTRS citation 20160009054 →
`https://ntrs.nasa.gov/api/citations/20160009054/downloads/20160009054.pdf` (Report No. NF1676L-22587).
**Evidence level:** VI — peer-reviewed-conference (AHS Forum proceedings), NASA Langley.

**Retrieval caveat — read carefully:** this PDF's body-text fonts (embedded CID TrueType,
Identity-H-encoded) do **not** extract to real Unicode text with either `pdftotext` or PyMuPDF
(`fitz`) — both return almost nothing (`pdftotext`: 787 words total from a 15-page paper; `fitz`: empty
string on body pages) even though the file is a completely genuine, correctly-named PDF from the
official NASA API (7.5 MB, confirmed valid PDF, `pdffonts` shows the fonts are embedded and flagged
"has Unicode map" but the map evidently does not resolve correctly for this file). **All quotes below
were obtained by rendering the affected pages to PNG at 150 dpi (`pdftoppm`) and reading them visually**
(agent's own eyes, not OCR software) — every page number cited was read directly off that page's own
visible printed footer digit in the rendered image, so the page attribution is as solid as for a
text-extracted PDF even though the transcription itself is manual. Axis labels and a handful of isolated
words in figures *did* extract normally (they use a different, correctly-mapped font), which is how the
existence of "BPF SPL (dB re. 20 μPa)" polar plots (Figs. 15–16) was first located before being confirmed
visually.

**What it says — RPM stability of small BLDC rotors under ESC control (Q3), p. 8:**
*"The DJI-CF results, however, show much cleaner broadband spectra with much less retained mid- and
high-frequency tonal content. This is because the DJI-CF rotor was observed to exhibit rotation rate
fluctuations on the order of ±3 RPM for the case shown. The APC-SF rotor, on the other hand, was observed
to exhibit rotation rate fluctuations on the order of ±20 RPM for the case shown. This is also believed
to be the cause for the lower broadband-extracted levels relative to the floor of the raw spectra over a
frequency range of 5-12 kHz in Figure 10. These results demonstrate the challenges associated with
extracting the broadband levels for the case of a rotor-motor configuration exhibiting considerable RPM
variations."*

Two different small brushless rotor-motor-ESC combinations, same measurement rig, same day: one holds
RPM to **±3 RPM**, the other to **±20 RPM** — nearly an order of magnitude apart — and the paper
explicitly attributes the *worse* rotor's degraded tone/broadband separation quality directly to this RPM
spread. (Both are still far tighter, in absolute RPM terms, than the ~90–290 Hz-wide BPF range our own
five-PWM-step protocol sweeps deliberately — this is jitter *within* one nominally fixed PWM/RPM setpoint.)

**What it says — tone/broadband decomposition method and its explicit RPM-drift failure mode (Q2 and Q3
together), p. 7, "Acoustic Measurement Post-Processing":**
*"The acquired acoustic data are processed three ways. The first and simplest method is to simply treat
the acquired time data as a random data set. Acoustic narrowband spectra were computed using the fast
Fourier Transform (FFT) with a Hanning window of 75% overlap and a frequency resolution of 5 Hz. As
stated previously, only five seconds of acquired acoustic data were utilized for post-processing for a
given RPM condition. This was both because of the onset of recirculation as well as RPM drift for longer
motor run times. As a result of this, the autospectral random uncertainty was fairly large at εr =
14.14% (Ref. 20). This translates to a random SPL uncertainty of u_r,SPL ∈ {−0.66, +0.57} dB."*
[Q4-relevant: 5 s window → ±0.6 dB-ish.]

*"The second post-processing technique … emulates a deterministic analysis. … a 3rd-order Butterworth
narrow bandpass filter was applied to the time series data, with a ± 40 Hz frequency band centered around
the frequency of interest. The TTL pulse signal from the tachometer was used to parse the time series data
into blocks corresponding to individual revolutions of the rotor. Acoustic amplitudes of each frequency of
interest were computed by calculating the RMS of the ensemble-averaged pressure time history across all
revolutions: SPL_{n×BPF} = 20 log₁₀(p̄_rms/p_ref). … the uncertainties of these tonal amplitudes were
approximated by the 95% confidence intervals of the RMS pressure values: u_{SPL_{n×BPF}} = 20
log₁₀[(p̄_rms ± 1.96 σ_{p_rms}/√N_revs)/p_ref]."*

*"The third post-processing technique … extracting the non-periodic, or broadband noise … parsing the
time series data into blocks of rotor revolutions, then computing a mean rotor revolution time history.
This mean revolution time history was then subtracted from the individual time blocks, which are then
FFT-processed as a random time series."*

*"The primary drawback of these latter two techniques is that they do not account for fluctuations in the
rotor rotation rate. In other words, all time blocks were defined to be the same length, which enforces a
condition of constant RPM. As a result of this, these techniques would yield higher uncertainties in the
ensemble-averaged pressure values at higher frequencies due to phase drift and retain higher frequency
tonal content in the broadband-extracted spectrum for a run condition in which the RPM was seen to vary
by a considerable amount."*

This is the single most direct statement retrieved on the mechanism behind Q3/Q4: **any per-revolution
ensemble/phase-average technique silently assumes constant RPM within its analysis window; when RPM
drifts, the assumption breaks and both the extracted tone (phase-smeared) and the extracted "broadband"
residual (still carrying unremoved tonal energy) degrade.** This is functionally the same failure mode as
our own fixed-length-FFT third-octave banding: a BPF drifting inside a 2 s capture window (or across
5-step-PWM runs) does not sit still long enough for either a per-revolution or a fixed-bandwidth analysis
to cleanly separate it from its neighbours.

**What it says — plotting the harmonic level in a directivity/polar plot (Q5), p. 12:**
*"Finally, BPF directivity comparisons are made between PAS predictions and LSAWT measurements for
several different rotor rotation rates in Fig. 18"* [sic — this sentence recurs near-verbatim in source 6,
the 2017 follow-on paper by the same lead author, confirming a house convention]. In this 2016 paper the
equivalent figures are captioned **"Fig. 15. Total noise directivity predictions of 2×BPF harmonic …"**
and **"Fig. 16. Total noise predictions at BPF using PAS for the two rotors"**, both plotted as SPL at the
harmonic (x-axis **"BPF SPL (dB re. 20 μPa)"** / **"2×BPF SPL (dB re. 20 μPa)"**) against elevation angle
θ (y-axis, −90°…+90°) — not a band level. Numeric example from the same page: *"the reduction in BPF
between these two conditions (120 Hz versus 200 Hz) offers a potential human perception benefit … the
APC-SF rotor offers a noise benefit increasing from 3.6 dB at θ = +45° to 8.9 dB at θ = −45°."*

**What it says — 1/3-octave banding visibly obscures the same BPF/harmonic structure it is meant to
summarize (supporting context for the whole thread, p. 9, Figs. 8–9):** the paper's own 1/3-octave-band
summary panels ("1/3-Octave Spectra," SPL₁/₃ vs. frequency, for both the APC-SF and DJI-CF rotors) show a
sharp single-band spike at the low-frequency end (BPF-containing bin) immediately followed by a deep dip
in the next band, at every rotation rate plotted — the narrowband panels immediately above each 1/3-octave
panel confirm this is exactly the sharp BPF tone (100–200 Hz range) landing predominantly in one
third-octave bin rather than being smoothly spread; the text does not comment on this explicitly (no
sentence names "band edge"), so this is this agent's own reading of Figs. 8–9, offered as a visual
corroboration of the thread's core phenomenon in a fully independent dataset, not a textual claim from the
paper.

---

## 11. Heutschi, Ott, Nussbaumer & Wellig (2020) — Acta Acustica 4, 24, "Synthesis of real world drone signals based on lab recordings"
**File:** `papers/arc-validation/Heutschi-Ott-Nussbaumer-Wellig_2020_ActaAcustica_synthesis-drone-signals.pdf`
(NEW; open access, CC-BY). **Route:** the publisher PDF
(`acta-acustica.edpsciences.org/articles/aacus/pdf/2020/06/aacus200056.pdf`) is behind a DataDome
bot-challenge that blocks both `curl` and `WebFetch` (returns a captcha-delivery HTML stub, not the PDF,
under a plain UA or a Scholar referer); retrieved instead from the **Empa institutional repository DORA**
mirror surfaced by Unpaywall's `oa_locations` list: `https://www.dora.lib4ri.ch/empa/dload/empa:23650/PDF/view`.
Identity confirmed on p. 1 (title, all four author names and affiliations — Empa/armasuisse/RUAG — DOI
10.1051/aacus/2020023, all match).
**Evidence level:** I — peer-reviewed journal, open access.

**What it says — real-world RPM jitter under normal flight/ESC control, quantified against wind (Q3):**
Abstract: *"a random pitch shift variation to account for turbulence induced rotational speed variations
in the field"* is one of the required ingredients to make a synthesized drone signal sound real — i.e.
constant-RPM synthesis is empirically distinguishable from a real recording specifically because real
rotors under ESC control are *not* constant-RPM in flight.

§3.2.4–3.2.5, p. 6 (DJI Mavic 2 Pro, on-board recorder + rotational-speed sensor, 18 flights): *"The
variation of the rotational speed during one manoeuvre and flight was evaluated as normalised standard
deviation of the rotational speed: σₙ = σ(R[n])/R_average. In combination with the average wind speed …
a data pair was obtained to finally derive a linear relation between σₙ and v … The comparison of the
different hover manoeuvres shows an increase of the rotational speed variation with height which is in
line with the expected increase of wind speed with height. The manoeuvre sink exhibits very large rpm
variations, almost independent of the wind speed. … In forward flight, the rpm variation is substantially
larger in upwind conditions compared to downwind."* Flights covered *"average wind speed at 2.5 m …
between 0.3 and 5.3 m/s."*

**Table 5** (p. 7) gives the fitted model σₙ = a + b·v_wind,2.5m per manoeuvre:

| manoeuvre | a | b [s/m] |
|---|---|---|
| Hover 10 m | 0.005 | 0.0052 |
| Hover 20 m | 0.005 | 0.0079 |
| Hover 50 m | 0.006 | 0.0109 |
| Climb 20–50 m | 0.001 | 0.0084 |
| Sink 50–10 m | 0.063 | 0.0017 |
| Forward, downwind | 0.012 | 0.0033 |
| Forward, upwind | 0.005 | 0.0130 |

i.e. even in still air a hovering consumer quadrotor's RPM standard deviation is ≈0.5–0.6% of its mean
(rising to several % with wind or in a turbulent self-wake descent) — a real, ESC-controlled,
closed-loop-governed rotor's RPM is **not** a delta function even absent any deliberate dithering; §4
of the same paper (not reproduced here — outside this thread's page budget) goes on to model this
measured σₙ as a "random pitch shift" applied on synthesis specifically to reproduce the tonal
smearing/broadening a real recording shows and a purely tonal synthetic signal does not.

No mention of "warble tone" as a deliberately-injected *test* signal for the purpose of averaging out
room interference (Q3's other half) — this paper's random-speed variation is a *field-realism*
consideration for synthesis, not a chamber-qualification technique.

---

## 12. Antoni (2009) — Mechanical Systems and Signal Processing 23, 987–1036, "Cyclostationarity by examples" (Invited Review)
**File:** `papers/arc-validation/Antoni_2009_MSSP_cyclostationarity-by-examples.pdf` (NEW; author
preprint/manuscript version, same DOI 10.1016/j.ymssp.2008.10.010 as the journal-of-record article, hosted
as course material). **Route:** `https://docente.unife.it/docenti/dleglc/a-a-2010-2011-dmsm/ciclostazionarieta.pdf`
(University of Ferrara course page — an institutional-repository-class mirror per protocol rule 4; the
publisher's own ScienceDirect copy is a listed blocker, per protocol rule 5). Identity confirmed on p. 1:
title, sole author, affiliation (UMR CNRS 6253, Compiègne), journal name/volume/page range, and DOI in
the PDF's own `pdfinfo` Title field all match.
**Evidence level:** I — peer-reviewed journal, invited tutorial review (~1500+ citations; the standard
reference for this technique).

**What it says (Q2) — the case for treating rotating-machine tones as cyclostationary rather than strictly
periodic, printed p. 990 (embedded page-number artifact retained from the original journal proof,
confirmed present in the extracted text):**
*"A great tribute is due to William A. Gardner who first established many of the theoretical foundations,
laid down the currently used terminology, and also foresaw many applications. As a matter of fact, W. A.
Gardner was probably the first to recognise that the cyclostationary framework is appropriate for any
physical phenomenon that gives rise to data with periodic statistical characteristics: 'in
mechanical-vibration monitoring and diagnosis for machinery, periodicity arises from rotation, revolution,
and reciprocating of gears, belts, chains, shafts, propellers, bearings, pistons, and so on' [10]."*

From the abstract (unpaginated, first page): *"This paper is a tutorial on cyclostationarity oriented
towards mechanical applications. The approach is voluntarily intuitive and accessible to neophytes. It
thrives on 20 examples devoted to illustrating key concepts on actual mechanical signals and demonstrating
how cyclostationarity can be taken advantage of in machine diagnostics, identification of mechanical
systems and separation of mechanical sources."*

**Note on what could not be extracted:** the paper's table of contents (in the retrieved dump) lists a
dedicated practical subsection *"Angular (re)sampling … [p.] 1019"* — exactly the tacho-driven
constant-angle resampling step that underlies the phase-averaging methods in sources 5 and 10 above, and
the natural bridge from "cyclostationary theory" to "how Whelchel/Zawodny's per-revolution technique is
really a hand-built, non-Kalman order-tracking filter" — but this agent could not locate that
subsection's body text in the extracted dump (it is a ~50-journal-page review condensed into a 19-page
preprint layout, and a plain-text search for "resampl"/"angular"/"tachomet" near the expected location
returned nothing, possibly due to a hyphenation or font artifact at exactly that heading). **No quote is
taken from that subsection** — only the general framing quote above, which was independently located and
confirmed.

---

## 13. ISO 1996-2:2017 — *Acoustics — Description, measurement and assessment of environmental noise — Part 2: Determination of sound pressure levels* (iTeh preview, 15 pp. of a ~65-page standard)
**File:** `papers/arc-validation/ISO-1996-2_2017_standard-preview_environmental-noise-measurement.pdf`
(NEW; partial). **Route:** `https://cdn.standards.iteh.ai/samples/59766/dbeb6253754b42f193ff53bd64e835b1/ISO-1996-2-2017.pdf`.
Identity confirmed on p. 1: "ISO 1996-2, Third edition, 2017-07."
**Evidence level:** VII — standard (sample only — and for this thread's purpose, an unhelpful sample).

**What could be retrieved (Q2, weak):** the table of contents confirms *"Annex J (informative) Objective
method for assessing the audibility of tones in noise — Engineering method … [p.] 54"* and *"Annex K
(informative) Objective method for assessing the audibility of tones in noise — Survey method … [p.] 56"*
exist in the standard, but **the 15-page free preview stops well before either annex** (it covers only
the front matter and the early normative clauses through the measurement-uncertainty discussion, ending
around clause 8–9). The only in-sample sentence that touches tonality at all: *"The numbers given in
Table 1 refer to A-weighted equivalent-continuous sound pressure levels only. Higher uncertainties are to
be expected on maximum levels, frequency band levels and levels of tonal components in noise."*
(page marked "20" in-sample, i.e. an early clause on measurement uncertainty — not Annex F, which the same
sentence points to for the actual uncertainty calculation).

**Bottom line: Annex C's site-selection guidance and Annexes J/K's actual tonality-audibility algorithm
(the "ISO 1996-2 Annex C/J objective tonality method" Q2 asked for) are NOT retrieved** — only their
existence and titles are confirmed. Listed under NOT RETRIEVED in `RETRIEVAL-C.md` for the substantive
content; Adam's university proxy is the route to the full text if this method is wanted in detail.

---

## Answers to the thread questions

**Q1 — standard statement of tone-at-band-edge splitting, with numbers.**
IEC 61260-1:2014 (source 8) supplies the *definition* — a band edge is, by construction, the geometric
mean of the two adjacent nominal centres (§3.8, p. 9) — but its own numeric tolerance table was not in the
retrievable preview. **ANSI S1.11-2004 (source 9), the technically-aligned US counterpart standard,
supplies the actual numbers** from its own Table 1 (octave) and Table B.1 (1/3-octave, p. 15): at the
nominal 1/3-octave band edge (f/fₘ = 2^(1/6) ≈ 1.1225, independently verified arithmetically), a
Class-1 filter's relative attenuation must sit between **+2.0 dB and +5.0 dB** (Class 0: 2.3–4.5 dB;
Class 2: 1.6–5.5 dB) — **not** a single fixed "−3 dB / half-power" point as the folk version of the claim
states. No retrieved source states the −3 dB figure explicitly as a standards requirement; it appears to
be a loose paraphrase of an idealized filter's crossover, not what either IEC 61260-1 or ANSI S1.11
actually mandates. ISO 5305:2024 (source 3) separately hands this filter-shape question straight to IEC
61260-1 Class 1 without adding anything of its own.

**Q2 — recommended practice: report tones separately; extraction/decomposition methods, with numbers.**
ISO 5305:2024 (source 3) explicitly endorses narrow-band-spectrum tonal extraction but sets no bin-width
or averaging rule ("requirements for signal processing … are not specified in this document," p. vi). The
concrete, numbers-backed methods actually come from the NASA Langley small-rotor group: **per-revolution
ensemble-average RMS of the tone** (Zawodny-Boyd-Burley 2016, source 10, p. 7, Eq. 3–4: 3rd-order
Butterworth ±40 Hz pre-filter, TTL tachometer-gated blocks, 95%-CI uncertainty) and the companion
**phase-average-and-subtract broadband residual** (same paper, p. 7; elaborated in full step-by-step
detail with an explicit interpolation grid in Whelchel 2023, source 5, p. 94–96: Hanning, 50% overlap,
4 Hz resolution, both requiring a shaft tachometer signal our rig lacks). Antoni 2009 (source 12) gives
the theoretical umbrella these are all special cases of — cyclostationary/order-domain analysis, with
Gardner's own list of periodicity sources explicitly naming "propellers" (p. 990) — but this thread could
not retrieve a dedicated Vold–Kalman-filter tutorial as open access (see RETRIEVAL-C.md), and could not
locate Antoni's own "Angular (re)sampling" practical subsection in the extracted text. Heutschi et al.
2020 (source 11) is the drone-specific decomposition example requested, but its emphasis is
signal-*synthesis* (splitting a recorded tonal+broadband drone signal to re-synthesize it with a modified
pitch/Doppler/propagation), not measurement analysis — the tonal/broadband split itself is inherited from
the same rotating-machinery literature. ISO 1996-2 Annex C/J (source 13) — NOT retrieved beyond its title.

**Q3 — RPM stability of small BLDC rotors under ESC control; warble tones as deliberate interference
averaging.** On RPM stability: three independent measured datasets agree that a small BLDC rotor under
closed-loop ESC/PWM control holds RPM tight (**±3 RPM** for one rotor-motor pair, Zawodny-Boyd-Burley
2016, source 10, p. 8) to very tight (**"minimal fluctuations"**, unquantified, Weitsman 2020, source 4,
p. 1327) *as long as the aerodynamic load is steady* — but a **different** rotor-motor pair on the same
rig, same day, showed **±20 RPM** (source 10, p. 8), and RPM visibly destabilizes once inflow becomes
unsteady (recirculation onset, source 4, pp. 1327–1328; turbulent self-wake descent or wind gusts in free
flight, Heutschi et al. 2020, source 11, p. 6, Table 5: σₙ from ≈0.5% in calm hover up to 6%+ in a
turbulent descent). **No retrieved source discusses a deliberately-introduced "warble" tone or narrow-band
noise as a way to average out spatial interference dips** — grepped Cunefare 2003 (source 1) and ISO
26101-1:2021 (source 2) explicitly for "warble," "swept," "modulat," "beating," with zero hits. If
anything, Cunefare 2003 argues the *opposite* framing for its own (frequency-, not RPM-, averaged)
broadband test signal: frequency-smoothing a tonal source's spatial pattern makes chamber qualification
"of dubious value" (p. 892) because it hides the same interference structure a narrow-band tone reveals —
a caution that likely also applies to letting BPF/RPM jitter blur our own third-octave cells rather than
fixing it.

**Q4 — recording length/averaging needed for a stable tonal-plus-broadband band level.** Three
consistent, numbers-backed data points, all from the same NASA-Langley small-rotor measurement lineage:
Weitsman 2020 (source 4) — **2 s → ε_r 22.80% → u_r,SPL ∈ {−1.12, +0.89} dB** (p. 1328–1329); **7 s →
ε_r 11.85% → u_r,SPL ∈ {−0.55, +0.49} dB** (p. 1333) [note: these are two *different* averaging windows,
not both a property of a 2 s spectrum — see the Comparison section for how the shared protocol background
slightly conflates them]. Zawodny-Boyd-Burley 2016 (source 10, p. 7) — **5 s → ε_r 14.14% → u_r,SPL ∈
{−0.66, +0.57} dB**. Whelchel 2023 (source 5, pp. 81–82) — explicit uncertainty-vs-averaging-time curve
from 2 s to 28 s, with the BPF tone specifically **under 1 dB uncertainty even at the shortest (2 s, 15
records) window**, though a genuine (non-statistical) recirculation-driven level rise of "at least 7 dB"
with increasing averaging time is layered on top in that dataset and must not be mistaken for sampling
variance. ISO 1996-2:2017 (source 13) confirms only in general terms that "higher uncertainties are to be
expected on … frequency band levels and levels of tonal components" than on broadband Leq, with the actual
calculation deferred to its (unretrieved) Annex F. ISO 5305:2024 (source 3) states no averaging-duration
requirement at all in the retrieved preview.

**Q5 — plotting the harmonic level, not the band level, in polar/directivity plots.** Confirmed as
standard practice across three independent sources, all with concrete numbers: Zawodny & Haskin 2017
(source 6, Fig. 18) plots "**BPF SPL (dB re. 20 μPa)**" directly against elevation angle for three rotor
speeds; Zawodny-Boyd-Burley 2016 (source 10, Figs. 15–16) plots both "BPF SPL" and "2×BPF SPL" against
elevation, with a worked example (a 3.6–8.9 dB directional noise-reduction claim, p. 12, that depends on
comparing the *tone* level, not a band, between two different-BPF rotors); Alkmim et al. 2022 (source 7,
Figs. 6–7) plots "spectral SPL in polar coordinates with respect to elevation… at their respective BPFs"
from a spherical-harmonic reconstruction whose own validity ceiling is set by the BPF (spatial aliasing
above ~164 Hz forces the analysis to stop at the first BPF tone, p. 2739 — i.e. the harmonic-level choice
here is not just convention but a hard constraint of the array processing). **No retrieved source
describes a proportional-bandwidth-centred-on-the-harmonic convention (e.g. an explicit "BPF ± 10%")** —
all three use a genuinely single-frequency (narrowband-extracted or ensemble-RMS) tone level, not a
proportional band around it.

---

## Comparison with earlier notes

Held papers re-read for this thread and cross-checked against the pre-existing notes:

- **Cunefare 2003** — `papers/chamber-problems/EXTRACTS-core.md` (row 1) and `MATRIX-3W.md` (row 1)
  quote the same "narrow band-pass (1/20 of centre frequency) on tones" method detail this thread
  independently re-extracted (confirmed on p. 886, matching). No discrepancy. This thread adds the p. 881
  abstract and p. 892 conclusion quotes verbatim (the earlier note paraphrases the same conclusion without
  a verbatim quote) and confirms, by direct grep of the fresh text dump, that "warble" is entirely absent
  from the paper — new information, not previously checked by anyone against this specific question.

- **ISO 26101-1:2021 / ISO 5305:2024** — `papers/anechoic-simulation/MATRIX-3W.md` (rows for both
  standards) quote the same core passages this thread re-confirms (ISO 5305 §6.2 "minimized when summing
  in a frequency band," p. 6; ISO 26101-1 §5.1.4.1 bandwidth-matching-device-spectrum, p. 5). No
  discrepancy in the passages both notes share. This thread adds, from the *same* preview PDFs, several
  passages the earlier MATRIX note did not quote: ISO 5305's Introduction sentence on narrow-band tonal
  extraction (p. vi) and its explicit IEC 61260-1 Class-1 filter requirement (p. 5); ISO 26101-1's full
  §5.1.4.2 test-signal-options clause including the "band-limited … noise" and "mix of pure tones … more
  than a one-third-octave band" text (p. 5). No conflicts — pure addition.

- **Weitsman 2020** — `papers/chamber-problems/EXTRACTS-local.md` (Weitsman entry) already quotes both
  uncertainty figures this thread relies on, **and attributes them to the same pages this thread
  independently confirmed**: "2 s average gives … εr = 22.80% … ur,SPL ∈ {−1.12, +0.89} dB (p. 1328)" and
  "uncertainty falls to εr = 11.85%, ur,SPL ∈ {−0.55, +0.49} dB (p. 1333)". **Full agreement**, including
  on the page numbers — a useful independent cross-check, since this agent initially mis-attributed the
  first figure to p. 1329 from a naive read of the concatenated multi-page dump before re-verifying with
  page-isolated extraction (`pdftotext -f N -l N`) and landing on the same p. 1328 the earlier note already
  had. `MATRIX-3W.md` row 25 additionally paraphrases "thrust envelope modulates and RPM fluctuates" without
  a verbatim quote or page — this thread supplies that as a direct quote (pp. 1327–1328) and additionally
  found the "well documented by Zawodny et al.⁵" attribution (p. 1327) that neither earlier note mentions,
  which is what led this thread to the Zawodny-Boyd-Burley 2016 paper.
  **One clarification, not a discrepancy with a citable file but worth flagging**: the shared
  `PROTOCOL.md` background line "Weitsman 2020 ±1.1 → ±0.5 dB random uncertainty for a 2 s spectrum"
  slightly conflates two different averaging windows — the ±1.1 dB-ish figure is the **2 s** case, but the
  ±0.5 dB-ish figure is the **7 s** case (after mesh treatment extended the clean window), not a second
  number from the same 2 s spectrum. See the Q4 answer above for the disambiguated numbers.

- **Whelchel 2023** — `papers/chamber-problems/MATRIX-3W.md` row 27 summarizes "Harmonics ≥ 7-8 dB with
  averaging time; screens 'no beneficial effect'". This thread's own reading (pp. 81–83) is consistent on
  the harmonics-rise-with-averaging-time number ("at least 7 dB," matching "≥7-8 dB") but did not
  independently re-verify the broader "screens have no beneficial effect" conclusion — the pages read for
  this thread (screen spacing 4 and 7 rotor radii, p. 82–83) show screens *did* keep the BPF level flat for
  longer (6–8 s vs. immediate rise without screens) even though the upper harmonics still grew regardless
  of screens, which is compatible with, not contradictory to, a "screens don't meaningfully help overall"
  verdict stated elsewhere in the (much longer) thesis that this thread did not re-read in full. No
  conflict identified, but this thread's coverage of Whelchel is narrower (§5.1.2–5.1.3 only) than the
  earlier note's, which appears to draw on more of the thesis.

- **Zawodny & Haskin 2017** — `papers/chamber-problems/MATRIX-3W.md` row 31 covers the reflections/cut-on
  frequency findings from a different part of the same paper; this thread's BPF-directivity-plot finding
  (Fig. 18) is a different section of the same document and does not overlap or conflict.

- **Alkmim et al. 2022** — `papers/chamber-problems/EXTRACTS-local.md` and `MATRIX-3W.md` row 33 cover
  ground-reflection and spatial-aliasing findings; this thread's Figs. 6–7 BPF-polar-plot finding is
  additional and does not conflict (the aliasing-ceiling number, p. 2739, is shared between both threads'
  readings and matches exactly: "above fmax = 163.77 Hz").

No held source's claim used by this thread was found to conflict with the earlier notes; all
discrepancies found were either (a) missing verbatim quotes/pages in the earlier notes that this thread
supplies, or (b) the one page-attribution near-miss in this agent's own first pass (self-corrected, see
Weitsman above, and resolved to agree with the pre-existing note).
