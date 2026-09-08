# EXTRACTS — Thread F: can a small foam-lined room be fixed at 200–250 Hz?

Compiled 2026-09-08. Working directory `/home/adam/ŻYCIE/PRACA/SoundVisualizer`. All held PDFs were
re-opened, identity-checked against their own front matter, and re-extracted fresh with plain
`pdftotext -q` into `papers/arc-validation/refetch-txt/` (page numbers below were then re-derived
per-page with `pdftotext -f N -l N`, not guessed from the concatenated dump — every page cited was
independently confirmed against an explicit page-number stamp printed on that same PDF page, except
where noted). New PDFs are saved into `papers/arc-validation/` and dumped into
`papers/arc-validation/txt/`. One PDF (Zawodny/Boyd/Burley 2016) has a non-extracting body-text layer
(pdftotext returns only chart/axis labels for it — confirmed with `pdffonts`); its quotes below were
read directly off the rendered page image (via the PDF-page-image viewer), which is still "the PDF
actually opened and read," and are cited by the page number printed on the page itself.

---

## 1. Beranek, Sleeper & Moots — *The Design and Construction of Anechoic Sound Chambers*, OSRD Report No. 4190, Harvard Electro-Acoustic Laboratory, 15 Oct 1945

File: `papers/anechoic-simulation/beranek_sleeper_1946_anechoic_chambers.html` (GPO OCR transcription,
no PDF/page numbers — a 1945 typewritten report scanned and OCR'd by the U.S. Government Publishing
Office; cited by section heading below since no pagination survives in the transcription). Evidence
level: **report** (primary historical source; the foundational wedge-design dataset the entire field
still cites).

Fresh dump: `papers/arc-validation/refetch-txt/beranek_sleeper_moots_1945_OSRD.txt` (via `w3m -dump`,
since this source is HTML, not a PDF — no `pdftotext -layout` risk applies here). Front matter
confirmed: "OFFICE OF SCIENTIFIC RESEARCH AND DEVELOPMENT ... Report of October 15, 1945 ... O.S.R.D.
NO. 4190 ... ELECTRO-ACOUSTIC LABORATORY CRUFT BUILDING-HARVARD UNIVERSITY" — matches
`BIBLIOGRAPHY.md`'s identification exactly (the 1945 OSRD report, not the 1946 JASA paper).

**What it says bearing on Q1** — this is the original source of the quarter-wavelength rule and of the
10%-pressure/99%-energy cutoff definition that every later paper (Bonfiglio-Pompoli, Jiang, Wang-Tang,
and the vendor explainer already in `EXTRACTS-downloaded.md`) restates. It also gives real measured
wedge depths for three different cutoff frequencies from Harvard's own 500+ tested structures — the
closest thing in the corpus to a direct "depth needed for a given cutoff" table:

- 150 cps cutoff → 25 in (63.5 cm) total depth (21 in wedge + base/air-space) for the second Harvard chamber.
- 250 cps cutoff → 15 in (38 cm) total depth for the short, high-density wedge used in the third chamber.
- 40 cps (extrapolated) → 94 in (2.4 m) total length would be needed, with optimum flow resistance 4.8 acoustic ohm/in — "very low density... frail... difficult to manufacture."

**Verbatim quotes** (section headings used in place of page numbers; OCR errors preserved with `[sic]`):

> "In fact, the lowest frequency at which good absorp[t]ion is obtained, is that for which the length
> of the wedge equals approximately one-fourth of a wave length." — §III.D.5 "Wedge-shaped Structures"

> "The dimensional design specifications for the P.F. Fiberglas wedge structures are summarized as a
> function of desired cutoff frequency in Fig. 3. The cutoff frequency is defined as that frequency at
> which the pressure reflection rises to 10^ [sic, "10%"] of the pressure in a normally incident sound
> wave. This corresponds to the frequency at which the absorption [of] sound energy drops to 99^ [sic,
> "99%"] or at which there is a sound reduction of -SD-'db [sic — OCR-garbled; almost certainly "20 db":
> a 10% pressure-reflection coefficient means 1% power reflection, and 10·log₁₀(1/0.01) = 20 dB exactly,
> so the garbled figure is mathematically consistent with "20 db" and with no other round number] a
> single reflection." — §III.C "Generalized Wedge Specifications"

> "A linear wedge of 21 inches length was developed for use as a lining of medium depth for our second
> anechoic chamber (11 x 15 x 10 feet). A cutoff frequency of 150 cps, i.e., the frequency at which R
> reaches 10^, was obtained for a total depth of 25 inches." — Summary §6 "Medium Length Linear Wedge Structure"

> "A third chamber (12 x 20 x 12 feet) was lined with short wedges... This high density structure has a
> cutoff frequency of about 250 cps for a depth of 15 inches." — Summary §7 "Short Linear Wedge Structure"

> "Investigation of the graphs shown in Fig. 5 of the summary shows that for absorptions down as low as
> 40 cps, a wedge structure would need to have a total length of 94 Inches measured from its tip to the
> rigid backing wall... the optimum flow resistance R of the material would need to be 4.8 acoustic ohm
> per inch... This is a very low density and results in wedges which are frail, and hence, might be
> difficult to manufacture and install." — §III.D.5

---

## 2. Bonfiglio, P. & Pompoli, F. — *Numerical methodologies for optimizing and predicting the low frequency behavior of anechoic chambers*, J. Acoust. Soc. Am. 134(1), 285–291, 2013

File: `papers/anechoic-simulation/Bonfiglio-Pompoli_2013_JASA_numerical-low-frequency-anechoic-chambers.pdf`.
Evidence level: **journal**. Identity confirmed on PDF p.2 (printed p.285): title/authors/DOI match.
Fresh dump: `papers/arc-validation/refetch-txt/Bonfiglio-Pompoli_2013_JASA_numerical-low-frequency-anechoic-chambers.txt`.
Page numbers below are printed-page numbers, individually confirmed via `pdftotext -f N -l N` against
the explicit page-number stamp on that PDF page (PDF p.2=printed 285 … PDF p.8=printed 291, one-to-one
after the 1-page Scitation cover sheet).

**What it says bearing on Q1** — states the λ/4 rule and the 99% criterion as the field's standard, then
shows with FEM optimisation + Delany–Bazley that the rule is only a rough guide: a 100 Hz cutoff needs
a wedge length of order 85–90 cm, and for highly resistive material the actual optimum is *longer* than
λ/4, i.e. the rule under-predicts depth in that regime.

**Verbatim quotes:**

> "As a function of the minimum working frequency of the chamber (cut-off frequency), the wedge length
> is indicated as being equal to a quarter of the wavelength (k/4 rule hereafter) [k here renders λ] and
> the absorption coefficient at normal incidence is higher than 0.99 for all frequencies above the
> cut-off limit." — p. 285

> "...the wedges for a cut-off frequency of 100 Hz and a maximum length of the wedge of 90 cm." — p. 288

> "Fig. 5 shows that the k/4 rule is not always respected; in fact for airflow resistivity higher than
> 10 kPa·s/m², a wedge length greater than 85 cm is required (which corresponds to a quarter of the
> wavelength for a cut-off frequency of 100 Hz)." — p. 288 [check: λ/4 at 100 Hz = 343/(4·100) = 0.857 m ≈ 85 cm — matches exactly]

> "...the complete procedure is applied to design the chamber with a cut-off frequency of 100 Hz. The
> only constraint was the width of the base of the wedges fixed at 0.4 m... The best solutions satisfying
> αn > 0.99 for all frequencies between 20 Hz and 250 Hz are lw = 0.56 m and h = 0.3 m." — p. 290 (a
> 650 m³ chamber design; total wedge length ≈ 0.56 m plus 0.3 m base ≈ 0.86 m, again ≈ λ/4 at 100 Hz)

> "...it has been found that for wedges made of highly resistance porous materials the rule of choosing
> a length of the wedge equal to a quarter of the wavelength corresponding to the cut-off frequency
> could not be respected." — p. 291

---

## 3. Jiang, C., Zhang, S. & Huang, L. — *On the acoustic wedge design and simulation of anechoic chamber*, J. Sound Vib. 381, 139–155, 2016

File: `papers/anechoic-simulation/Jiang_2016_JSV_wedge-design-and-chamber-simulation.pdf`. Evidence
level: **journal**. Identity confirmed (title/authors/DOI on p.1=printed 139). Fresh dump:
`papers/arc-validation/refetch-txt/Jiang_2016_JSV_wedge-design-and-chamber-simulation.txt`. Printed
page = PDF page + 138 throughout (confirmed against the paper's own header "139–155" and per-page
stamps).

**What it says bearing on Q1** — this is the most directly quantitative source in the corpus for "depth
needed at a given cutoff, 100–250 Hz": an FEM optimisation under the constraint "99% absorption for
minimum depth" gives a depth-vs-cutoff curve read directly off Fig. 7 (viewed as a rendered page image,
PDF p.10 = printed p.148):

| Cut-off (Hz) | Classic wedge min. depth | UGFW (flat-wall alternative) min. depth |
|---|---|---|
| 100 | **0.800 m** (Table 2/3, printed p.146 & p.153) | 0.762 m |
| ~150 | ≈0.55–0.60 m (read off Fig. 7) | ≈0.50 m |
| ~200 | ≈0.38–0.40 m (read off Fig. 7) | ≈0.35 m |
| **250** | **≈0.31–0.32 m** (read off Fig. 7) | ≈0.30 m |

(The 100 Hz row is an exact table value; the 150/200/250 Hz rows are my own reading of the plotted
curve in Fig. 7, since the paper does not tabulate those three cutoffs numerically — flagged as
graph-read, not table-quoted, but the curve shape is smooth and monotonic so the reading is not
ambiguous to within ~1–2 cm.)

**Verbatim quotes:**

> "The parameters of both structures are optimized for achieving minimum absorber depth, under the
> condition of absorbing 99% of normal incident sound energy. It is found that the UGFW structure
> achieves a smaller total depth for the cut-off frequencies ranging from 100 Hz to 250 Hz." — Abstract, p. 139

> "Table 3. Summary of the performance of the two structures in anechoic chambers. Total depth [m] /
> Design cut-off frequency [Hz]: Wedge 0.800 / 100; UGFW 0.762 / 100." — p. 153

> "It is because the 99% energy absorption means 10% pressure reflection, which is still very large. In
> some area inside the anechoic chamber, the multi-reflected sound accumulates and violates the 1.5 dB
> deviation easily." — p. 154 (this is the field's own restatement of the Beranek/Wang-Tang 10%↔99%
> equivalence, and the reason a "qualified" 99%-absorbing lining still is not a free field everywhere)

---

## 4. Wang, C.-N. & Tang, M.-K. — *Boundary element evaluation on the performance of sound absorbing wedges for anechoic chambers*, Eng. Anal. Bound. Elem. 18, 103–110, 1996

File: `papers/anechoic-simulation/Wang-Tang_1996_EABE_BEM-sound-absorbing-wedges.pdf`. Evidence level:
**journal**. Identity confirmed (PDF p.1=printed 103 … PDF p.8=printed 110, 1:1 mapping, each page's
own printed-number stamp checked). Fresh dump:
`papers/arc-validation/refetch-txt/Wang-Tang_1996_EABE_BEM-sound-absorbing-wedges.txt`.

**What it says bearing on Q1** — independently corroborates the 10% definition and, importantly, shows
that depth is not the only lever: for a *flat-backed* wedge, increasing base/air-gap thickness barely
moves the cutoff, and the wrong flow resistance can leave a deeper wedge no better than a shallower
one — matching what my own Delany–Bazley re-calculation below finds for a flat slab (§ "Illustrative
calculation" under Q1 answers).

**Verbatim quotes:**

> "The cut-off frequency (i.e. the frequency at which the pressure reflection coefficient is 0.1)..." — p. 107

> "The figure shows that as the length of the wedge increases, the cut-off frequency is obviously
> reduced." — p. 107 (wedge-length effect, base/air-gap held fixed at 20 cm/10 cm)

> "The influence of increasing base and air layer thickness on cut-off frequency is not obvious." — from
> the concatenated re-read (§5.3.1, printed p.108 by page-count; not independently page-stamp-verified,
> flagged as lower-confidence page attribution — content itself is directly quoted from the fresh dump)

> "The cut-off frequency is strongly affected by the length of the wedge and the flow resistance of the
> porous material. If a further reduction in cut-off frequency is required without changing the space of
> an anechoic chamber, the hybrid wedge is a good choice." — p. 109 (Conclusion)

---

## 5. Alba, J., del Rey, R. & Rodríguez, J. C. — *Fitting Methods for Empirical Models of Open-Pore Foams*, Acoustics 7(4), 62, 2025 — **[NEW]**

File: `papers/arc-validation/Alba-delRey-Rodriguez_2025_MDPIAcoustics_fitting-methods-open-pore-foams.pdf`.
DOI: 10.3390/acoustics7040062. Evidence level: **journal** (MDPI *Acoustics*, open access). Retrieved
via `mdpi-res.com` (protocol route). Identity confirmed on PDF p.1 (title/authors match). Fresh dump:
`papers/arc-validation/txt/Alba-delRey-Rodriguez_2025_MDPIAcoustics_fitting-methods-open-pore-foams.txt`.
1:1 PDF-page = printed-page mapping confirmed via the paper's own "N of 16" footer.

**What it says bearing on Q1** — this paper does not tabulate α(250 Hz) directly, but it gives real,
measured flow resistivities for actual melamine and polyurethane foam samples (two-microphone
impedance-tube method, ISO/two-thickness method), which is the missing input for a Delany–Bazley
prediction at other thicknesses (used below).

**Verbatim quote (Table 1, p. 4):**

> "Table 1. Materials analysed. Material / Density (kg/m³) / Thickness (mm) / Airflow Resistivity
> (kNs/m⁴): M1: Melamine foam 4 cm / 9.4 / 39.1 / 18.4. M2: Polyurethane foam 2.5 cm / 26.4 / 25.0 / 3.8.
> M3: Polyurethane foam 4 cm / 21.7 / 40.5 / 3.9." — p. 4

---

## 6. Bikmukhametov, F. et al. — *Applicability of radiowave anechoic chambers for acoustic free-field measurements... ITMO University*, arXiv:2603.16556v1 (submitted to Elsevier), 2026

File: `papers/anechoic-simulation/Bikmukhametov_2026_arXiv_ITMO-radiowave-chamber-acoustic-free-field.pdf`.
Evidence level: **preprint**. Re-identity-checked (title/authors on PDF p.1). Fresh dump:
`papers/arc-validation/refetch-txt/Bikmukhametov_2026_arXiv_ITMO-radiowave-chamber-acoustic-free-field.txt`.
PDF page = printed page 1:1 (confirmed via the paper's own "Page N of 9" footer).

**What it says bearing on Q1** — an unusually clean, apples-to-apples measured comparison of a
*flat disk* sample of foam-rubber (25 mm thick) against the *same material shaped into a full pyramid
wedge* (425 mm pyramid + 35 mm base = 460 mm total depth), both fit to the Delany–Bazley model. It is
strong direct evidence that shape (graded taper), not just raw material thickness, is what makes a
wedge work — the flat 25 mm sample never exceeds α≈0.5 anywhere in 290–1800 Hz, while the 460 mm
pyramid of the *same* material reaches α≈0.815 at 290 Hz and only clears 0.9 above 410 Hz. Even a wedge
nearly half a metre deep therefore falls short of ISO's 0.99 at 290 Hz.

**Verbatim quotes:**

> "The height of each pyramid is 425 mm, while the thickness of the base is 35 mm, and the width of the
> base is 150 mm." — p. 2 ("Description of the chamber")

> "The porous material is described with the Delany-Basley [sic, Delany–Bazley] model with flow
> resistivity 3437 Pa·s/m² defined in the fitting step... The absorption coefficient [for the flat disk]
> is below 0.5 for the whole considered spectral range. The situation changes drastically for the
> pyramid element, such that at 290 Hz the absorption coefficient is about 0.815 and then increases to
> 0.996 with increasing frequency." — p. 3

> "...the absorption coefficient starts to overcome the value of 0.9 at frequencies above 410 Hz." — p. 4

> "(a) Measured absorption coefficient of the coating material and its approximation via Delany-Bazley
> model. The sample represents a disk with the radius 55 mm and the thickness 25 mm." — Fig. 2 caption, p. 3

---

## 7. Ma, X., Chen, K., Wang, L., Liu, Y. & Ding, S. — *Active control of low frequency sound absorption of large sized micro-perforated panel absorber by using point source*, Appl. Acoust. 185, 108424, 2022

File: `papers/chamber-problems/Ma_2022_ApplAcoust_active-control-large-MPP-absorber.pdf`. Evidence
level: **journal**. Identity re-confirmed (title/authors, p.1). Fresh dump:
`papers/arc-validation/refetch-txt/Ma_2022_ApplAcoust_active-control-large-MPP-absorber.txt`. Page
numbers below are the article's own internal 1–13 pagination (1:1 with PDF pages, confirmed).

**What it says bearing on Q2** — a micro-perforated-panel (MPP) absorber only 8 cm deep. *Passive* (no
control), its own theoretical/Maa's-theory curve (Fig. 2, viewed directly as a page image on p.4) shows
α ≈ 0.15–0.2 at 250 Hz, rising to a single resonance peak of ≈0.9 around 500–600 Hz, then falling again
— i.e. at our target band an 8 cm MPP alone is barely better than bare foam. Adding one loudspeaker as
an active point source inside the same 8 cm cavity drives the absorption "nearly close to 1" up to a
location-dependent cutoff, reaching 400 Hz for the smaller (0.6 × 0.8 m) panel.

**Verbatim quotes:**

> "Table 1. The geometric parameters of the model... Cavity depth of the MPPA [=] 0.08 m." — p. 4

> "For validating the theoretical model, the sound absorption coefficient of the large sized active MPPA
> is calculated before control for the dimension being 0.6 m × 0.8 m (length × width), as shown in
> Fig. 2. It is also calculated by using Maa's theory. General good agreement is found between these two
> results." — p. 4 (Fig. 2's plotted curve: α rises from ~0 at low frequency to a peak of ≈0.9 near
> 500–600 Hz, reading α≈0.15–0.2 at 250 Hz and ≈0.25–0.3 at 300 Hz — read directly off the page image, not text)

> "The sound absorption coefficient of the active large sized MPPA is highly improved and nearly close
> to 1 in the low frequency range after control... there is a cutoff frequency for each location of the
> point source, after which the control effect hardly works... the controllable bandwidth is much longer
> for the small sized active MPPA (Case 1), in which case the upper limit controllable frequency can
> reach up to 400 Hz and be close to the resonance frequency of the MPPA." — p. 4

> "The larger the size of active MPPA is, the narrower the controllable frequency band is." — p. 6

> Cavity-mode cutoffs (Table 3): for the 0.6×0.8 m panel (Case 1), depending on where the point source
> sits, the controllable band is capped at the (0,1,0) mode 215 Hz, the (1,0,0) mode 287 Hz, or (best
> case, source at the wall centre) the (0,2,0) mode — matching the ≈400 Hz figure above; for the larger
> 1.0×1.2 m panel (Case 2) the same modes sit at 143/172/224/287 Hz, i.e. a bigger panel gets *less*
> controllable bandwidth for the same 8 cm depth.

---

## 8. Haasjes, R. — *Towards an active acoustic anechoic chamber*, PhD dissertation, University of Twente, 2025

File: `papers/chamber-problems/Haasjes_2025_PhD-Twente_active-acoustic-anechoic-chamber.pdf`. Evidence
level: **thesis**. Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Haasjes_2025_PhD-Twente_active-acoustic-anechoic-chamber.txt`
(10,622 lines). Printed page = PDF page − 13 throughout (front matter is 13 unnumbered/roman pages;
confirmed against 5 independent page-stamp checks: PDF 25→12, 38→25, 95→82, 112→99, 115→102, 130→117 —
all satisfy the same offset).

**What it says bearing on Q2** — the fullest active-control dataset in the corpus, with real hardware
counts, achieved reductions, and bandwidths, at three scales:

| Scale | Hardware | Result | Band |
|---|---|---|---|
| Small numerical (2-D) | 12 secondary + 12 primary + 12 reference sources | 12.8 dB average reduction (FD-RMFE algorithm) | results shown at 56.2, 161.7, 396.1 Hz |
| Large numerical (2-D, 5×5 m room) | 200 secondary + 200 primary + 200 reference + 200 error + 225 performance sensors | 13.4 dB average reduction | broadband (impulse) |
| **Real hardware** (0.92×0.92 m 2-D box) | 12 secondary + 12 primary + 12 reference + 12 error = 48 transducers | **9.4 dB average reduction** | logarithmic sweeps 60–600 Hz per primary source |

**Verbatim quotes:**

> "...found in literature, typical AAC's have a cut off frequency at about 200 Hz [18,31,32]." — p. 25

> "The room is of dimensions 5-by-5 m², with the walls having an impedance of Z = 10ρc... Secondary
> sources: 200, Primary sources: 200, Reference sensors: 200, Error sensors: 200[,] Performance sensors: 225." — p. 92

> "The control coefficients W(z) are used to simulate the performance of the system... showing an
> average reduction of 13.4 dB." — p. 92

> "The FD-RMFE algorithm converged to a reduction of 12.8 dB, averaged over all performance sensors...
> Using the same settings, the normalized FeLMS algorithm converged to 3.3 dB averaged over all
> sensors." — p. 82

> "...the maximum frequency for accurate secondary sound field generation lies at 570 Hz, rather than
> 600 Hz [owing to 0.3 m loudspeaker spacing against the spatial-Nyquist limit]." — p. 102

> "During real-time control, each primary source generates an independent logarithmic sweep from 60 to
> 600 Hz... The spectral densities of the first four performance signals are shown in Fig. 6.31, which
> shows an average reduction of 9.4 dB." — p. 117

> (Describing a *different*, prior published method, not Haasjes' own): "An experiment with a
> one-dimensional tube is shown, in which a reduction of 95% of the reflected energy in a frequency
> range from 0.6−5.6 kHz is achieved." — p. 12 (this is a 1-D-tube result at a much higher band than our
> 200–250 Hz target and is *not* Haasjes' own chamber-scale demonstration — flagged so it is not
> mis-cited as a room-scale 200 Hz-band result)

---

## 9. Friot, E. & Gintz, A. — *Estimation and global control of noise reflections*, CNRS-LMA, arXiv:0911.4639, 2009

File: `papers/chamber-problems/Friot-Gintz_2009_arXiv_estimation-global-control-noise-reflections.pdf`.
Evidence level: **conference/preprint** (matches a published Acoustics'08/Proceedings-style paper from
LMA Marseille). Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Friot-Gintz_2009_arXiv_estimation-global-control-noise-reflections.txt`.
This arXiv PDF carries no printed page stamps; page numbers below are the PDF's own page count (10 pages total).

**What it says bearing on Q2** — real hardware, a real anechoic room, and the clearest statement in the
corpus of *how many* transducers active wall control needs to scale to a whole room, expressed as a
density rule (transducers per wavelength) rather than a fixed count — which is what lets the number be
rescaled to our much smaller room.

**Verbatim quotes:**

> "Figure 2 shows the scattered pressure with or without control when 0–100Hz white noise is monitoring
> the primary loudspeaker. Below 100Hz, control is not efficient because the control authority of the
> secondary loudspeaker is too low. Above 750Hz control is not efficient because a second acoustic mode
> is propagating in the duct." — PDF p. 4

> "Since 'only' 14 control channels and loudspeakers were available, global control of the scattered
> radiation could not be implemented. Instead numerical simulations... suggested the arrangement...for
> control of the scattered radiation at 280Hz in a restricted angular sector." — PDF p. 4

> "Figure 4b shows that real-time control of the error signals led in average to a 10dB reduction of the
> scattered pressure." — PDF p. 5 (LMA's own 3-D anechoic-room experiment, at 280 Hz, with only 14 channels)

> "...the required number of sensors and actuators (about 3 per wavelength all around the body) makes it
> unrealistic to contemplate control for a real submarine with today's technology. A more sensible
> application of active scattering control is the reduction of the low-frequency reflections on the
> walls of anechoic rooms. Indeed, usual rooms do not allow anechoic measurements below 50Hz..." — PDF p. 6

> "In a 10m x 7m x 6m anechoic room such as shown in figure 3, the 3 transducers per wavelength rule
> suggests that about 100 microphones and loudspeakers would allow estimation and control of the wall
> scattered radiation up to 100Hz. Although 200 transducers may seem high a number, it complies with
> today's controller technology and it has to be compared with the number of the room[']s 1400 passive
> wedges." — PDF p. 6

---

## 10. Long, H., Liu, C., Shao, C., Cheng, Y., Chen, K., Qiu, X. & Liu, X. — *Subwavelength broadband sound absorber based on a composite metasurface*, Sci. Rep. 10, 13823, 2020 — **[NEW]**

File: `papers/arc-validation/Long-etal_2020_SciRep_subwavelength-composite-metasurface-absorber.pdf`.
DOI: 10.1038/s41598-020-70714-7. Evidence level: **journal** (Nature *Scientific Reports*, open
access). Identity confirmed (title/authors, p.1). Fresh dump:
`papers/arc-validation/txt/Long-etal_2020_SciRep_subwavelength-composite-metasurface-absorber.txt`.
1:1 PDF-page = printed page.

**What it says bearing on Q2** — the single most on-target Q2 result in the whole search: a
coiled-space (Helmholtz-type) metasurface backing an *ultrathin sponge* gets >80% absorption over
185–385 Hz — a band that straddles the 200–250 Hz blade-passage band almost exactly — at a total device
thickness of only ~100 mm (calculated from their own stated λ/thickness ratio, and matching the 100 mm
value in their own parameter table). That is roughly a third of the ≈310–320 mm a plain graded foam
wedge needs for the same cutoff per Jiang 2016 (§3 above), at the cost of being a narrowband,
individually-tuned resonant structure rather than a broadband absorber.

**Verbatim quotes:**

> "By coupling an ultrathin sponge coating with the designed metasurface, a deep-subwavelength broadband
> absorber with high absorptivity (>80%) exceeding one octave from 185 Hz to 385 Hz (with wavelength λ
> from 17.7 to 8.5 times of thickness of the absorber) has been demonstrated." — p. 1, Abstract [Arithmetic
> check, mine: λ(185 Hz)=343/185=1.854 m ÷17.7 = 0.105 m; λ(385 Hz)=343/385=0.891 m ÷8.5 = 0.105 m — both
> give ≈105 mm, consistent with the "L=100 mm" case reported later in the same paper.]

> "(d) Absorptance of specific cases with sponge thickness at lp = 0.05 m[,] a wavelength λ being from
> 12.6 to 9.0 times of the thickness at absorptance > 95%) has been devised [citing a prior design].
> However, the bandwidth of absorption is still limited, i.e., less than one octave." — p. 1 [that prior,
> thinner (5 cm) design's band: λ=12.6×0.05=0.63 m→f=343/0.63≈544 Hz; λ=9.0×0.05=0.45 m→f≈762 Hz — a
> higher band than our 200–250 Hz target, i.e. even the earlier "thin" design does not reach down to 250 Hz.]

> "The total thickness L in these cases are at [71.8, 81.2, 90.6, 100, 109.6, 119, 128.5, 138] mm
> corresponding to w1 ranging from 7 to 14 mm." — p. 4 (their parameter sweep over device thickness)

---

## 11. Jiménez, N., Cox, T. J., Romero-García, V. & Groby, J.-P. — *Metadiffusers: Deep-subwavelength sound diffusers*, Sci. Rep. 7, 5389, 2017 — **[NEW]**

File: `papers/arc-validation/Jimenez-etal_2017_SciRep_metadiffusers-deep-subwavelength.pdf`. DOI:
10.1038/s41598-017-05710-5. Evidence level: **journal** (Nature *Scientific Reports*, open access).
Identity confirmed. Fresh dump:
`papers/arc-validation/txt/Jimenez-etal_2017_SciRep_metadiffusers-deep-subwavelength.txt`. 1:1
PDF-page = printed page (confirmed via the "Scientific Reports | 7: 5389" footer + explicit page numeral).

**What it says bearing on Q3** — this is the direct, quotable source for "diffusers are ineffective (or
impractically deep) below their design frequency," with the same quarter-wave law as the wedge
literature, applied to a *diffuser well* instead of an absorbing wedge:

**Verbatim quotes:**

> "...each well acts as a quarter wavelength resonator... the phase shift introduced by each well occurs
> at its quarter wavelength resonance, i.e., L = c₀/4f where f is the frequency, L is the depth of the
> well and c₀ is the speed of sound in air. Therefore, a limitation of Schroeder diffusers is that the
> depth becomes large for low design frequencies. This results in thick and heavy panels, limiting the
> use of phase grating diffusers for low-frequencies where the wavelength of sound in air is of the order
> of several meters." — p. 2 [Arithmetic check, mine: at 250 Hz, L=343/(4×250)=0.343 m — i.e. a
> conventional Schroeder diffuser well needs ≈34 cm depth at 250 Hz, essentially the same order as the
> foam-wedge depth found above from Jiang/Beranek — diffusers and absorbers hit the same physical wall
> at low frequency for the same reason.]

> "Using well-folding the total thickness of a diffuser can only be reduced to about half the depth of a
> standard Schroeder diffuser." — p. 2

> "...a broadband metadiffuser panel of 3 cm thick was designed using optimization methods for
> frequencies ranging from 250 Hz to 2 kHz." — p. 1, Abstract (their own deep-subwavelength engineered
> exception — achieved only via internal Helmholtz-resonator loading of each slit, not a plain wedge or
> a plain diffuser well)

> "...primitive root and ternary sequence diffusers are mimicked by metadiffusers whose thickness are
> 1/46 to 1/20 times the design wavelength, i.e., between about a twentieth and a tenth of the thickness
> of traditional designs." — p. 1

---

## 12. Rasmussen, P. & Winberg, L. — *Accurate measurement of Drone Noise on the ground*, Quiet Drones 2nd e-Symposium, 27–30 June 2022

File: `papers/chamber-problems/Rasmussen-Winberg_2022_QuietDrones_drone-noise-on-the-ground.pdf`.
Evidence level: **conference** (authors are GRAS Sound & Vibration staff — tag [vendor-adjacent] for
the ground-board-product angle, but the physics/formula content is standard acoustics, not a vendor
claim). Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Rasmussen-Winberg_2022_QuietDrones_drone-noise-on-the-ground.txt`.
This document carries its own explicit "Page | N" footers throughout, used directly below (no
re-derivation needed).

**What it says bearing on Q3** — gives the exact closed-form formula for how the ground/wall-reflection
comb-filter interference pattern's frequencies scale with reflector distance, plus measured dB
magnitudes for the resulting error:

**Verbatim quotes:**

> "The interference of the direct wave and the reflected wave at the microphone position is like a comb
> filter, with the first minimum at the frequency where the microphone height 1.2 m equals ¼ of the
> wavelength: f₀ = c/(4·l) ≈ 71.4 Hz[.] And the first maximum at f₁ = c/(2·l) ≈ 143 Hz." — p. 3 (l = the
> reflector distance — here mic-to-ground height; the formula shows the interference pattern scales as
> 1/l: halve the distance to the reflecting surface and every notch/peak frequency doubles)

> "...the frequencies coincident with the comb-filter minima are reduced by more than 20 dB, and the
> frequencies coincident with the comb-filter maxima are amplified by 6 dB... the overall sound pressure
> level measured at 1.2 m height will be 3 dB higher than the corresponding level measured in a full free
> field." — p. 4

> "...even very soft ground surfaces will not prevent the interference." — p. 6

> "As the angle varies, the distance travelled by the direct and the reflected wave will change, and this
> will change the comb-filter effect..." — p. 7 (elevation-angle-dependence of the same formula — this is
> geometrically exactly our arc-error situation: a fixed off-centre reflector, mics at varying angle/path
> length to it)

> "By placing the measurement microphone on a fully reflecting ground board, the influence of the
> reflection becomes well defined and will result in a simple pressure doubling." — p. 1, Summary (the
> geometric-mitigation trick: put the mic *on* the reflecting surface so the path-length difference is
> exactly zero at every frequency, converting an uncontrolled frequency-dependent comb filter into a flat,
> correctable +6 dB)

---

## 13. Fasulo, G., Longobardo, G., De Gregorio, F. & Barbarino, M. — *Experimental acoustic investigation of rotor noise directivity and decay in multiple configurations*, Aerospace 12(7), 647, 2025

File: `papers/chamber-problems/Fasulo_2025_Aerospace_rotor-noise-directivity-decay.pdf`. Evidence
level: **journal**. Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Fasulo_2025_Aerospace_rotor-noise-directivity-decay.txt`. 1:1
PDF-page = printed page (MDPI "N of 26" footer confirmed on every page cited).

**What it says bearing on Q3 (distance decay/interference) and Q4 (facility)** —

**Verbatim quotes:**

> "...operated in the Italian Aerospace Research Centre's semi-anechoic chamber. The chamber, with a
> 90 Hz cut-off frequency, measures 5.65 m × 4.45 m × 4.00 m." — p. 7

> "f1 and f2 are chosen as 90 Hz (cut-off frequency of the chamber) and 20 kHz, respectively, thus
> confining the analysis to the audible range and excluding room-reflected energy below 90 Hz." — p. 7
> [an explicit **exclusion** of the sub-cutoff band from every OASPL integration in the paper]

> "For L < 2D, the level falls by about 17 dB per distance doubling, indicating that the field is still
> dominated by the reactive component. Beyond L = 3D, however, the measurements adhere closely to the
> far-field decay law, exhibiting a reduction on the order of 6 dB per distance doubling... Superimposed
> on this trend, pronounced oscillations appear... These fluctuations originate from constructive and
> destructive interference between the direct acoustic wave and its ground-reflected counterpart,
> yielding frequency- and range-dependent local sound pressure minima and maxima." — p. 15

> "Because microphone 9 lies within the propeller wake, it registers substantial low-frequency energy...
> making its OASPL highly sensitive to the lower integration bound. Its data were therefore omitted from
> the OASPL plots." — p. 10 [a second, independent **exclusion** example — a low-frequency-contaminated
> channel dropped rather than corrected]

> "The first harmonic of the BPF contour displays the strongest anisotropy, with a mean level difference
> of roughly 6.5 dB between mirrored left- and right-side microphones... the 266.7 Hz tone observed at
> 8000 rpm corresponds to an acoustic wavelength of roughly 1.3 m, over three times the 0.36 m plate
> span, rendering classical blockage effects insufficient... Likewise, under a far-field decay
> assumption, the minor path length difference would contribute only about 1.6 dB. Instead, the
> pronounced asymmetry may arise from near-field interactions, in which the rotor's pressure field
> couples with the plate edge and ground surface, producing direction-dependent interference among
> direct, reflected, and scattered acoustic components." — p. 22 [directly on Q3's "how the interference
> error scales with path-length ratio": a simple geometric path-length-difference argument predicts only
> ≈1.6 dB of asymmetry from the off-centre mounting, but the *measured* anisotropy is 6.5 dB — near-field
> multi-path interference, not the simple 1/r distance argument, dominates the error]

---

## 14. Jawahar, H. K., Hanson, L., Akhter, M. Z. & Azarpeyvand, M. — *Porous ground treatments for propeller noise reduction in ground effect*, Sci. Rep. 15, 2170, 2025

File: `papers/chamber-problems/Jawahar_2025_SciRep_porous-ground-propeller-ground-effect.pdf`.
Evidence level: **journal**. Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Jawahar_2025_SciRep_porous-ground-propeller-ground-effect.txt`.
Page numbers below independently confirmed against the paper's own "Scientific Reports | (2025) 15:2170
| ... | N | www.nature.com" footer on every page cited.

**What it says bearing on Q3 (distance decay of ground/reflector effect) and Q4 (Bristol facility)** —

**Verbatim quotes:**

> "Experiments to investigate propellers operating in GE were conducted in the Aeroacoustic facility at
> the University of Bristol. The anechoic chamber has dimensions of 7.9 m in length, 5.0 m in width and
> 4.6 m in height, including the surrounding acoustic walls... a rigid flat plate acting as the ground
> plane (GP) was placed at 8 different positions (L) away from the propeller... to induce varying
> degrees of GE corresponding to L/R = 0.75, 1, 1.5, 2, 2.5, 3, 3.5, and 4... Far-field noise
> measurements were acquired using a polar array of 23 microphones distributed in the axial direction
> centred on the propeller at a distance of 1.75 m (≈13R)." — p. 3 [note: **no cut-off frequency is
> stated anywhere in this paper** — the "160 Hz cut-off" figure for this same physical chamber comes from
> a *different* paper on the same Bristol facility, Huang (nd) below, not from Jawahar 2025 — see
> Comparison-with-earlier-notes]

> "The directivity plots in Fig. 4(a) for OGE condition at L/R = 4.0 shows minimal ground effect... As
> ground proximity decreases to L/R = 2.0..., OASPL begins to increase at shallower angles (θ<90°) due to
> ground reflection effects... At closer distances corresponding to IGE conditions (L/R ≤ 1.0), the
> ground effect becomes more pronounced. The solid ground plate amplifies OASPL by ≈3 dBA at shallow
> angles, while porous treatments reduce this increment by ≈2 dBA... The ground effect is strongest at
> L/R = 0.75 in extreme IGE conditions." — p. 6 [a measured decay curve of reflector-induced level error
> with distance: negligible by L/R=4, detectable at L/R=2, ≈3 dBA at L/R=1, strongest at L/R=0.75 — for
> R=127 mm (10-inch APC prop) these correspond to absolute plate distances of 508/254/127/95 mm]

---

## 15. Huang, Q. (supervisor M. Azarpeyvand) — *Height-dependent rotor noise and thrust in urban air mobility: an experimental study*, University of Bristol student research report, n.d.

File: `papers/anechoic-simulation/Huang_nd_Bristol-report_height-dependent-rotor-noise-thrust.pdf`.
Evidence level: **report** (student research report, not peer-reviewed — flagged accordingly).
Re-identity-checked (title page, p.1: "Height-Dependent Rotor Noise and Thrust in Urban Air Mobility...
Qiyu Huang, Supervisor: Professor Mahdi Azarpeyvand"). Fresh dump:
`papers/arc-validation/refetch-txt/Huang_nd_Bristol-report_height-dependent-rotor-noise-thrust.txt`.

**What it says bearing on Q4** — this is the actual source of the Bristol chamber's 160 Hz cut-off
figure (same physical chamber Jawahar 2025 uses, but Jawahar's own paper never states a cutoff):

**Verbatim quote:**

> "...conducted at the Aeroacoustics Facility of the University of Bristol, within an anechoic chamber
> measuring 7.9 m × 5.0 m × 4.6 m (L × W × H), with a cut-off frequency of 160 Hz." — p. 3

---

## 16. Merino-Martínez, R. et al. — *Aeroacoustic design and characterization of the 3D-printed, open-jet, anechoic wind tunnel of Delft University of Technology*, Appl. Acoust. 170, 107504, 2020

File: `papers/chamber-problems/Merino-Martinez_2020_ApplAcoust_TU-Delft-anechoic-wind-tunnel.pdf`.
Evidence level: **journal**. Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Merino-Martinez_2020_ApplAcoust_TU-Delft-anechoic-wind-tunnel.txt`.
Printed page = PDF page − 1 (confirmed against explicit page stamps on printed pp. 4, 12, 14).

**What it says bearing on Q4** — the A-tunnel's wedge geometry was explicitly *designed* around the
quarter-wave criterion for a 173.5 Hz target and *validated* by measurement at that same figure at
r ≤ 1.5 m, while the paper's own headline conclusion rounds the practical result to 200 Hz — both
numbers are genuinely in the text, at different points for different purposes (design target vs. stated
overall capability), not a contradiction:

**Verbatim quotes:**

> "...the total height of the wedge should be larger [than the quarter-wavelength criterion demands, for
> practical margin]... design frequency cutoff... 173.5 Hz." — p. 4

> "...the distance between the microphone array and the jet axis normally corresponds to r ≤ 1.5 m, so
> acoustic measurements at these three frequency bands could be considered as acceptable in that distance
> range. These results are consistent with the expected cutoff frequency of 173.5 Hz mentioned in
> Section 2." — p. 12

> "6. Conclusion[.] This paper explains the design and performance of the recently-refurbished
> aeroacoustic wind tunnel of Delft University of Technology (A-tunnel). This facility is a vertical wind
> tunnel with an anechoic plenum around the test section (with a cutoff frequency of 200 Hz)..." — p. 14

---

## 17. Gallo, E. et al. — *Development and commissioning of an aeroacoustic test bench for the investigation of single and coaxial propeller noise*, Acta Acustica 9, 16, 2025

File: `papers/chamber-problems/Gallo_2025_ActaAcustica_aeroacoustic-propeller-test-bench.pdf`.
Evidence level: **journal**. Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Gallo_2025_ActaAcustica_aeroacoustic-propeller-test-bench.txt`.

**What it says bearing on Q4** — the smallest qualified acoustic test room in the whole thread-F
corpus, and closest in floor-plan scale to our own room:

**Verbatim quote:**

> "The test mockup is located in the ALCOVES anechoic laboratory... The facility consists of two rooms, a
> main test room, and a discharge room, separated by a wall partition... The size of the main room is
> 2.5 m × 4.5 m. This room has been commissioned according to the ISO:3745 standard, demonstrating
> free-field behavior down to 150 Hz for both broadband and tonal noise sources." — p. 2

---

## 18. Ma, Z., Wu, H., Jiang, H., Zhong, S. & Zhang, X. — *Acoustic measurement of multi-rotor drones in anechoic and hemianechoic chambers*, Quiet Drones 2nd e-Symposium, 2022

File: `papers/chamber-problems/Ma_2022_QuietDrones_multirotor-anechoic-vs-hemi-anechoic.pdf`. Evidence
level: **conference**. Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Ma_2022_QuietDrones_multirotor-anechoic-vs-hemi-anechoic.txt`.

**Verbatim quote (p. 314):**

> "The experiments were conducted in the anechoic chamber of the Aerodynamic and Acoustic Facility at
> the Hong Kong University of Science and Technology. The chamber has a wedge-to-wedge dimension of
> 8.1 m (L) × 6 m (W) × 5.1 m (H) and a cut-off frequency of 100 Hz in the full anechoic configuration."
> — no caveat about sub-cutoff bands is needed here: the paper separately states (p. 315 of the fresh
> dump) the measured "blade passage frequency (BPF) is at around 182 Hz," safely above the 100 Hz cutoff.

---

## 19. Ma, Z., Zhou, P., Zhang, X. & Zhong, S. — *Experimental assessment of the flow recirculation effect on the noise measurement of a free-flying multi-rotor UAS in a closed anechoic chamber*, Acoustics Australia 52, 313–322, 2024

File: `papers/chamber-problems/Ma_2024_AcoustAust_recirculation-free-flying-UAS-anechoic.pdf`. Evidence
level: **journal**. Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Ma_2024_AcoustAust_recirculation-free-flying-UAS-anechoic.txt`. Page
numbers confirmed against the paper's own header/footer ("Acoustics Australia (2024) 52:313–322" +
page numeral — note a separate standalone "123" appearing on several pages is a Springer imprint code,
**not** a page number, and was excluded from page attribution).

**Verbatim quote (p. 314):**

> "...has wedge tip-to-tip dimensions of 8.1 m (L) × 6 m (W) × 5.1 m (H) and a cut-off frequency of
> 100 Hz." (same HKUST chamber as source 18; mic setup dimensioned around a "3.2 m UAS hover," p. 315)

---

## 20. Orrego-Ealo, J. & Pazos — *[low-cost small anechoic chamber]*, Scientia Técnica, 2018

File: `papers/small-chamber/Orrego-Ealo-Pazos_2018_ScientiaTechnica_low-cost-small-anechoic-chamber.pdf`.
Evidence level: **journal**. Re-identity-checked. Fresh dump:
`papers/arc-validation/refetch-txt/Orrego-Ealo-Pazos_2018_ScientiaTechnica_low-cost-small-anechoic-chamber.txt`.
Page numbers directly confirmed (PDF p.1→printed 471, PDF p.6→printed 476; the earlier
`small-chamber/EXTRACTS.md`'s "p.471" citation for this material is independently reconfirmed).

**What it says bearing on Q4** — the smallest chamber in the corpus, closest in *scale* (not
performance) to a "few cm of foam" room:

**Verbatim quote (p. 471):**

> "The working dimensions of the chamber are 1.94 m long x 1.91 m wide x 1.84 m high. The nominal cutoff
> frequency [is] 400 Hz." — built from polyurethane foam, steel tube frame, fiberglass, fibercement and
> particle-board panels; i.e. a room *smaller* than our 3×3×2.5 m target still needed a 400 Hz cutoff design
> (worse, not better, than 250 Hz) with real acoustic wedges — not a few centimetres of flat foam.

---

## 21. Zawodny, N. S., Boyd, D. D. Jr. & Burley, C. L. — *Acoustic Characterization and Prediction of Representative, Small-Scale Rotary-Wing Unmanned Aircraft System Components*, AHS 72nd Annual Forum, Paper 72-2016-044, West Palm Beach, FL, 2016 — **[NEW]**

File: `papers/arc-validation/Zawodny-Boyd-Burley_2016_AHSForum72_SALT-facility-small-rotor-characterization.pdf`
(a copy already existed under this name from a different thread working the same shared protocol —
confirmed byte-identical via `md5sum` to my independently-fetched copy, which was deleted to avoid a
duplicate in the shared corpus). NASA NTRS ID 20160009054, downloaded via
`https://ntrs.nasa.gov/api/citations/20160009054/downloads/20160009054.pdf` (protocol NTRS route).
Evidence level: **conference / NASA** (AHS Forum paper, hosted on NTRS). **Note on extraction method:**
`pdftotext` returns only chart axis-labels for this file (confirmed with `pdffonts`: the body-text glyphs
do not extract, even though real, non-scanned CID TrueType fonts are embedded) — the quotes below were
read directly from the rendered page images (title/authors/abstract confirmed on the rendered p.1; the
facility description on the rendered p.3), which is still "the PDF actually opened and read," just via
the page-image viewer instead of `pdftotext`.

**What it says bearing on Q4** —

**Verbatim quote (rendered p. 3, "Experimental Setup"):**

> "Experiments were performed in the Structural Acoustic Loads and Transmission (SALT) anechoic chamber
> facility at the NASA Langley Research Center... This facility is acoustically treated down to a
> cut-off frequency of 100 Hz and has interior dimensions (wedge tip to wedge tip) of 4.57-m (15-ft)
> high, 7.65-m (25-ft) wide, and 9.63-m (31.6-ft) long. A total of five 1/4" Brüel & Kjaer 4939
> free-field microphones in an arc array configuration are positioned in the acoustic far-field of the
> rotor test stand in elevation angle increments of 22.5°... Specifically, the microphones are positioned
> at a radial distance of 1.905 m (75 in.) from the rotor hub. This distance corresponds to at least 13R
> for the rotors tested in this study. The rotor test stand itself was constructed so that the plane of
> the rotor would stand 2.29-m (7.5-ft) above the floor wedge tips, which corresponds to half of the room
> height."

> (rendered p. 4): "...operation of the rotors for a long time results in recirculation build-up, which
> can compromise the desired static condition. Evidence of recirculation was found when the voltage
> output of the load cell began to exhibit high-amplitude fluctuations... Therefore, acoustic data used
> for post-processing were limited to a time period preceding this apparent onset of recirculation... a
> time period of five seconds was established."

---

## 22. Liu, R., Zhang, Z. & Zheng, X. — *The Modern Numerical and Experimental Methods for the Sound Absorbing Characteristics of Dissipative Sound Absorbing Materials: A Review*, Materials 18(23), 5353, 2025 — **[NEW, weak/supporting only]**

File: `papers/arc-validation/Liu-Zhang-Zheng_2025_MDPIMaterials_review-sound-absorbing-methods.pdf`. DOI:
10.3390/ma18235353. Evidence level: **journal (review)**. Identity confirmed. Fresh dump:
`papers/arc-validation/txt/Liu-Zhang-Zheng_2025_MDPIMaterials_review-sound-absorbing-methods.txt`.

**What it says bearing on Q1** — surveyed for a tabulated α(f)-by-thickness dataset; it does not
contain one. It only reports in-situ-method *validation ranges* against melamine/PU samples (not a
frequency-response table), so it is **not used as a numeric source** for Q1's 50/100/200 mm request —
listed here only because it was opened and read, and to record why it was set aside (see "Comparison
with earlier notes" — n/a, first read — and RETRIEVAL-F.md, SEARCHED AND REJECTED). One incidental
verbatim data point kept for completeness:

> "Using melamine foam (50 mm thick) as the sample, experiments showed that when the constraint value
> was 22 dB, the measurement results in the 160–1600 Hz frequency band were highly consistent with those
> of the impedance tube method." — p. 6 of the fresh dump (a method-validation statement, not an
> absorption-coefficient value)

---

## Illustrative calculation for Q1 (mine — not a claim from any source)

No open-access source in the 60–90-minute search window tabulates measured or Delany–Bazley-predicted
α(250 Hz) for plain 50/100/200 mm polyurethane/melamine slabs (see RETRIEVAL-F.md). To give the thread
a number, I computed normal-incidence absorption for a **flat, rigid-backed** slab using the standard
Delany–Bazley empirical model (the same model Bonfiglio-Pompoli 2013 p.288 and Wang-Tang 1996 p.109
both invoke for wedge design), fed with the *real, measured* flow resistivities Alba et al. 2025
reported for actual PU and melamine foam samples (source 5 above, Table 1, p. 4): σ≈3850 Pa·s/m² for
polyurethane, σ≈18,400 Pa·s/m² for melamine. Formulas used: Zc, kc from Delany–Bazley (1970); surface
impedance of a rigid-backed slab Zs = −j·Zc·cot(kc·L); α = 1 − |((Zs−Z0)/(Zs+Z0))|². This is **a
calculation, not a measurement or a quote** — flagged accordingly, and its validity is itself limited
(Delany–Bazley is only considered reliable for the dimensionless parameter X=ρ₀f/σ roughly in
0.01–1.0; at 250 Hz, X=0.079 for the PU value and X=0.0165 for the melamine value — the melamine case
sits right at the edge of the model's normal validity range, so treat that row as more approximate):

| Material (σ from Alba 2025) | 50 mm | 100 mm | 200 mm |
|---|---|---|---|
| Polyurethane, σ=3850 Pa·s/m² | α=0.16 | α=0.45 | α=0.94 |
| Melamine, σ=18,400 Pa·s/m² | α=0.21 | α=0.66 | α=0.67 |

A second calculation, scanning slab thickness continuously at 250 Hz, shows the flat-slab response is
**not monotonic** in thickness (unlike a graded wedge): the PU slab's α peaks at ≈0.98 near 250 mm, then
*falls* to a plateau of ≈0.92 for anything thicker; the melamine slab (higher flow resistivity) peaks at
only ≈0.71 near 150 mm and plateaus at ≈0.66 — never reaching 0.9, let alone 0.99, at any thickness,
because its resistivity is too high to be a good normal-incidence match to air at 250 Hz. This is the
quantitative version of what Wang-Tang 1996 (p.107–108) and Bonfiglio-Pompoli 2013 (p.291) both say in
words: past some flow resistivity, more flat material does not buy you the cutoff you want — you need
the *taper* (Beranek/Bonfiglio/Jiang, §§1–3 above), or an engineered resonant structure (Ma 2022 /
Long 2020, §§7,10 above), not just more flat thickness.

---

## Answers to the thread questions

**Q1 — Porous-absorber physics: absorption vs. thickness and wavelength; the quarter-wave rule; 10%
pressure-reflection = 99% absorption; measured/predicted α at 250 Hz for 50/100/200 mm.**

Answered in full by sources 1–6 plus the illustrative calculation. The quarter-wave rule (`L≈λ/4`) is
stated identically by Beranek 1945 ("§III.D.5"), Bonfiglio-Pompoli 2013 (p.285), and — for a diffuser
well rather than an absorbing wedge — Jiménez et al. 2017 (p.2), and its numeric consequence at 250 Hz
(λ/4 ≈ 34 cm) is directly corroborated by real wedge-depth data: Beranek's own tested short wedge needed
15 in (38 cm) for a 250 cps cutoff; Jiang 2016's FEM optimum for 250 Hz reads ≈31–32 cm off Fig. 7;
Bonfiglio-Pompoli's 100 Hz optimum (85–90 cm) matches λ/4=85.7 cm almost exactly. The 10%-pressure/
99%-energy equivalence is stated by Beranek 1945 (§III.C, with a garbled but arithmetically-consistent
"-20 db" figure), by Wang-Tang 1996 (p.107, "pressure reflection coefficient is 0.1"), and explicitly
spelled out by Jiang 2016 (p.154: "99% energy absorption means 10% pressure reflection"). No single
open-access source tabulates measured/D-B-predicted α(250 Hz) for 50/100/200 mm PU/melamine directly;
Alba et al. 2025 (p.4) supplied real measured flow resistivities for both materials, which I fed
through the standard D-B model myself (table above) — giving α≈0.16/0.45/0.94 (PU) and
α≈0.21/0.66/0.67 (melamine, non-monotonic) at 50/100/200 mm. Bikmukhametov et al. 2026 (p.3) supplies
an independent, real measured/D-B-fit data point at a nearby frequency and much greater depth: a 460 mm
foam-rubber pyramid reaches only α≈0.815 at 290 Hz (>0.9 only above 410 Hz), while a flat 25 mm sample
of the *same material* never exceeds α≈0.5 anywhere in 290–1800 Hz — directly demonstrating that a
"few cm of foam" is nowhere near either the depth or (without a taper) the geometry needed at 250 Hz.

**Q2 — Alternatives that absorb low frequencies in little depth: membrane/panel, Helmholtz/MPP,
metamaterial/coiled-space, active absorption — achievable absorption, depth, area, bandwidth.**

Micro-perforated panel (MPP): Ma et al. 2022 (p.4) — 8 cm cavity, passive α≈0.15–0.2 at 250 Hz (single
resonance peaked near 500–600 Hz); adding one active point source in the same 8 cm cavity drives α
"nearly close to 1" up to a location-dependent cutoff reaching 400 Hz for a 0.6×0.8 m panel (p.4), but
"the larger the size... the narrower the controllable frequency band" (p.6) — a bigger panel (1.0×1.2 m)
only reaches 143–287 Hz depending on source placement (Table 3). Coiled-space/Helmholtz metasurface:
Long et al. 2020 (p.1) — ~100 mm total thickness, >80% absorption across 185–385 Hz (straddling our
200–250 Hz target), roughly a third of the ≈310–320 mm a plain graded wedge needs for the same cutoff.
Active wall-reflection control: Haasjes 2025 (pp.82,92,102,117) — real hardware (48 transducers on a
0.92 m box) gives 9.4 dB average reduction over 60–600 Hz; scaled numerically to a 5×5 m room with 200
transducers per channel type (1000 total), 13.4 dB. Friot & Gintz 2009 (PDF pp.4–6) — real 3-D
anechoic-room hardware (14 channels) gives 10 dB reduction at 280 Hz; scaling their stated "3
transducers per wavelength" rule to a 10×7×6 m room needs ~100–200 loudspeakers+microphones for control
up to 100 Hz, "compared with the room's 1400 passive wedges" — i.e. active control trades wedge depth
for a comparably large (though differently-shaped) hardware count, not a free lunch.

**Q3 — Geometric mitigation: how interference error scales with reflected/direct path length and
reflector distance; angling; diffuser low-frequency ineffectiveness.**

Rasmussen & Winberg 2022 (p.3) give the closed-form scaling directly: comb-filter minima/maxima sit at
f₀=c/(4l), f₁=c/(2l) where l is the reflector distance, so the error pattern's frequency scales as 1/l
— halve the distance to the reflector and every notch/peak frequency doubles; magnitude is up to −20 dB
at minima, +6 dB at maxima, +3 dB overall (p.4), and does not disappear even for soft surfaces (p.6) or
off-normal angles (p.7, only the *pattern* shifts with elevation angle). Fasulo et al. 2025 (p.15) give
a measured example of the same physics in free flight: level decays 17 dB/doubling in the near field
(L<2D), relaxes to the classic 6 dB/doubling beyond L=3D, with ground-reflection interference
superimposed as "pronounced oscillations" on top of the decay law. Jawahar et al. 2025 (p.6) give a
measured decay of ground-plate-induced level error with L/R: negligible by L/R=4, detectable at L/R=2,
≈3 dBA at L/R=1, strongest at L/R=0.75. Fasulo et al. 2025 (p.22) also show that a *simple* path-length
argument under-predicts the real error: an off-centre-mount asymmetry that a naïve 1/r calculation
would put at ≈1.6 dB was actually measured at 6.5 dB, because near-field multi-path interference (not
distance alone) dominates — a caution against using distance-only formulas to predict arc errors at
close range. On diffusers: Jiménez et al. 2017 (p.2) state the low-frequency limit explicitly — a
standard Schroeder diffuser well is a quarter-wave resonator (L=c₀/4f), so "the depth becomes large for
low design frequencies... limiting the use of phase grating diffusers for low frequencies," with
well-folding buying at most a factor of ~2 in depth (p.2); only an engineered deep-subwavelength
metadiffuser (their own 3 cm/250 Hz–2 kHz design, p.1) breaks this, at the cost of narrow-band tuning
via internal Helmholtz resonators.

**Q4 — What small propeller/drone labs actually did about low bands.**

| Facility | Room size | Cut-off | Mic distance | Low-band handling |
|---|---|---|---|---|
| Bristol (Jawahar 2025 + Huang nd) | 7.9×5.0×4.6 m | 160 Hz (Huang p.3; **not stated** in Jawahar's own paper) | 1.75 m ≈13R (Jawahar p.3) | no explicit caveat found in Jawahar's text |
| CIRA (Fasulo 2025) | 5.65×4.45×4.00 m | 90 Hz | not a single fixed distance — polar+radial arrays | **excludes** sub-90 Hz explicitly (p.7); **drops** a low-frequency-contaminated mic entirely (p.10) |
| TU Delft A-tunnel (Merino-Martínez 2020) | plenum ≈6.4×6.4×3.2 m (per held EXTRACTS; not re-quoted here) | design target 173.5 Hz (p.4), validated at r≤1.5 m (p.12); conclusion states 200 Hz (p.14) | r≤1.5 m | states both a design figure and a rounder practical figure; no explicit exclusion found |
| VKI ALCOVES (Gallo 2025) | 2.5×4.5 m (smallest room in this thread) | qualified free-field to 150 Hz | not a single stated far-field distance found | no explicit low-band caveat found |
| HKUST (Ma 2022/2024) | 8.1×6×5.1 m | 100 Hz | mics 0.5 m apart in an arc | none needed — BPF≈182 Hz safely above cutoff |
| ITMO (Bikmukhametov 2026) | 4.46×6.96×3.3 m (RF chamber re-purposed) | "anechoic" only for source distance 0.5–0.8 m and 50–3150 Hz (p.5); worst-case deviation 15.5 dB elsewhere | 0.5–0.9 m tested | qualifies performance as direction- and distance-dependent, not a blanket cutoff (p.5) |
| Orrego small chamber (2018) | 1.94×1.91×1.84 m (smallest *chamber*, built-for-purpose) | 400 Hz | not applicable (traverse method) | worse cutoff than our 250 Hz target despite deliberate small-chamber engineering |
| NASA SALT (Zawodny/Boyd/Burley 2016) | 4.57×7.65×9.63 m | 100 Hz | 1.905 m ≈13R | recirculation, not cutoff, is the caveat: data window capped at 5 s |
| Mississippi State (Vesa 2020) | — | — | — | **NOT RETRIEVED** — see RETRIEVAL-F.md |

No facility in this table gets anywhere close to a "few cm of foam, 200–250 Hz" combination; the
smallest *purpose-built* chamber (Orrego, 1.94 m box) still needed a 400 Hz cutoff, and the smallest
*qualified* room (Gallo/VKI, 2.5×4.5 m) only reaches 150 Hz — both consistent with, not contradicting,
the one-pager's claim that distance (not foam alone) is the practical fix at 250 Hz in a small room.

---

## Comparison with earlier notes

- **Beranek 1945**: no prior EXTRACTS/MATRIX entry specific to wedge-depth-vs-cutoff numbers existed to
  compare against (the earlier `anechoic-simulation/MATRIX-3W.md` cites Beranek mainly for the
  1945-vs-1946 identity point, already correctly recorded in `BIBLIOGRAPHY.md`) — no discrepancy to
  report; this thread adds new depth-vs-cutoff figures (150/250/40 cps → 25/15/94 in) not previously
  extracted anywhere in the corpus.
- **Bonfiglio-Pompoli 2013**: no earlier extracts file quoted the specific 85–90 cm/100 Hz or λ/4-fails
  passages — new to this thread, no discrepancy.
- **Jiang 2016**: `anechoic-simulation/MATRIX-3W.md` does not carry Jiang's Table 2/3 numbers or Fig. 7
  — new extraction; no discrepancy with prior notes (there were none on this specific point).
- **Wang-Tang 1996**: same — no prior specific extraction to compare; no discrepancy.
- **Ma 2022 Appl. Acoust. (MPP)**: `chamber-problems/MATRIX-3W.md` row 18 already states "Absorption ≈ 1
  up to ~400 Hz; limit = first excitable cavity mode; 'larger…narrower the controllable band'" — this
  **agrees exactly** with my fresh re-read (p.4, p.6). `chamber-problems/EXTRACTS-downloaded.md`'s entry
  for this paper (crediting "Applied Acoustics 186:108424" and flagging "note: the DOI ...108383 supplied
  earlier resolves to a different paper") is a **minor volume-number discrepancy worth flagging**: the
  paper's own header reads "Applied Acoustics 185 (2022) 108424" (confirmed on PDF p.4/p.6 of my fresh
  re-read) — volume **185**, not 186; `BIBLIOGRAPHY.md`'s entry correctly says 185. The earlier
  `EXTRACTS-downloaded.md` mis-typed the volume as 186 even while correctly giving the article number
  108424 — a small transcription slip, not a wrong-paper identification.
- **Haasjes 2025**: no prior extracts file in the corpus quoted this thesis's specific dB-reduction
  numbers — new extraction; no discrepancy.
- **Friot-Gintz 2009**: same — new extraction (this arXiv paper had not previously been mined for its
  "3 transducers per wavelength" / "1400 wedges" comparison); no discrepancy.
- **Rasmussen-Winberg 2022**: no prior extracts file quoted the f₀/f₁ comb-filter formula explicitly —
  new extraction; no discrepancy.
- **Jawahar 2025**: `chamber-problems/MATRIX-3W.md` row 36 states "Bristol chamber, plate at 0.75–4 R,
  23-mic arc; Bare plate +4–8 dB above 1 kHz at 50°, absent at 90°; 75PPI-T −13 dB sideline" — this is
  about the >1 kHz band and is **consistent with, and complementary to** (not contradicting) my
  fresh-read numbers for the OASPL-vs-L/R trend at all-frequency scale (p.6: ≈3 dBA at L/R=1). No
  discrepancy, different frequency slice of the same dataset. One correction to flag: the **160 Hz
  Bristol cutoff figure that `anechoic-simulation/MATRIX-3W.md` row (HOW column) attributes to "Bristol
  aeroacoustic facility"** is, on this fresh re-read, **not present anywhere in Jawahar 2025's own text**
  (I searched exhaustively for "cut-off"/"cutoff" in the fresh dump — zero hits). It is a real quote, but
  belongs to Huang (nd), a *different* paper about the *same physical chamber* — worth being precise
  about which paper is the source when the two are cited together, since Jawahar 2025 is the
  peer-reviewed Sci Rep paper and Huang is an unreviewed student report.
- **Merino-Martínez 2020**: `chamber-problems/EXTRACTS-downloaded.md` credits this paper with "designed
  on the λ/4 criterion for free-field 'above approximately 173.5 Hz' (p. 4)" and "Conclusion quotes
  'cutoff frequency of 200 Hz' (§6, p. 14)" — **both independently reconfirmed** on this fresh re-read,
  at the same pages (p.4 and p.14 respectively); no discrepancy. I additionally located the connecting
  passage on p.12 (not previously extracted) showing the 173.5 Hz figure was also experimentally
  validated at r≤1.5 m, which explains why the paper is comfortable stating both numbers.
- **Gallo 2025**: no prior extracts file quoted the 2.5×4.5 m / 150 Hz figures specifically — new
  extraction; no discrepancy.
- **Ma 2022/2024 (HKUST)**: `chamber-problems/EXTRACTS-local.md` already states "wedge-to-wedge dimension
  of 8.1 m (L) × 6 m (W) × 5.1 m (H) and a cut-off frequency of 100 Hz" for both papers — **confirmed
  exactly**, same page numbers (314/315 for 2022; matching text for 2024). No discrepancy.
- **Orrego 2018**: `small-chamber/EXTRACTS.md` states "≈6.8 m³... Nominal cutoff frequency 400 Hz" at
  "p. 471" — **confirmed exactly** via independent per-page stamp check on this fresh re-read (PDF p.1 =
  printed 471). No discrepancy.
- **Bikmukhametov 2026**: no prior extracts file in the corpus quoted the pyramid-vs-disk absorption
  numbers or the 0.5–0.8 m/50–3150 Hz qualified range — new extraction; no discrepancy with the identity
  information already in `BIBLIOGRAPHY.md`.
- **Fasulo 2025**: no prior extracts file quoted the near-/far-field decay-law numbers, the mic-9
  exclusion, or the 1.6 dB-vs-6.5 dB path-length comparison — new extraction; no discrepancy with
  `chamber-problems/MATRIX-3W.md`'s existing (different-topic) row for this paper.
