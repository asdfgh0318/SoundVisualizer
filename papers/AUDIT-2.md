# AUDIT-2 — claim-by-claim verification, `papers/anechoic-simulation/`

Method: each paper's full `.txt` extract (pdftotext output; the Beranek & Sleeper file via `w3m -dump` of the GPO OCR HTML) was read start to finish and checked against every number, quote and page reference currently asserted about it in `papers/anechoic-simulation/MATRIX-3W.md`, `papers/chamber-problems/EXTRACTS-core.md` (for Schneider, Wang & Tang, Vorländer), and — for the eight papers the review names (Nash, Russo, Schneider, Vorländer, Beranek, Prinn, Payne & Simmons, Schmal) — `docs/anechoic-simulation.html`. Work was split across seven parallel read-only sub-agents (one paper each for the larger/singleton papers, small groups for the rest) plus direct work by the compiling agent on the Beranek & Sleeper file; each sub-agent read its assigned `.txt` file(s) in full before scoring any claim. Quotes are verbatim as printed, OCR ligature/scan artifacts included; page/section references are the numbers printed in the source itself (running headers/footers) wherever the extraction preserved them.

Where a sub-agent additionally checked something outside local files (e.g. a Crossref/DOI lookup for an undated conference paper), that is flagged explicitly as external, not text-verified — the source `.txt`/PDF remains the authority for everything else.

---

## Mateljan, I., "ARTA — Application Note No. 4: Loudspeaker Free-Field-Response" (n.d.) — Mateljan_nd_ARTA-AN4_loudspeaker-free-field-response.txt

- **Bibliographic check**: Title exactly as printed: "ARTA - APPLICATION NOTE / No 4: Loudspeaker Free-Field-Response" (running header on every page, and cover). **No author byline is printed anywhere in the document.** Authorship as "Mateljan" is an inference (ARTA's developer; corroborated only indirectly by the document's own self-citation in §7 Literature: "Mateljan I., Models for the Estimation of the Loudspeaker In-Room Response, Int. Journal for Engineering Modeling, vol. 6., No.1-4, 1993, ISSN 1330-1365"). No publication year, volume, page range (beyond internal pp. 1–12), or DOI is printed — it is a vendor application note, not a journal article; "nd" in the filename is correct. Second reference: "Kinsler, Frey, Coppens, Sanders: Fundamental of Acoustics, J. Wiley, New York, 2000." Filename is correct: matches title, topic, and the absence of a date.

- **Claim audit** (against MATRIX-3W.md and docs/anechoic-simulation.html §05):
  - "Loudspeaker free-field response is wanted from measurements made in ordinary reverberant rooms" (WHY paraphrase) — OK (p.1 abstract: "estimation of the loudspeaker free field response from a set of measurements made in normal reverberant rooms").
  - Near-field response scaled by a/2r, valid ka≪1, "very small error … below 200Hz" — OK, exact (p.4).
  - Baffle-step diffraction model (1+jf/f0)/(2+jf/f0), f0 = 42.70/d sphere, f0 = 34.16/d square baffle — OK, exact (p.5).
  - "gating the far-field IR before the first reflection (5.6 ms gate → valid above 178 Hz)" — **WRONG → imprecise**. The paper prints two different figures at two precision levels: (a) p.8 §5: "we remove the first reflection that is **5.6ms** apart from the start of the impulse response" (no Hz given there); (b) p.9 §5: "the time-bandwidth requirement is satisfied on frequencies **above 177.9Hz**. (Note: 1/gate = 1000/**5.604** = **178.4**)." The precise gate is 5.604 ms; the paper's own stated threshold is 177.9 Hz; its own printed check value is 178.4 Hz. "178 Hz" is a rounding that appears verbatim nowhere.
  - Merge at 235 Hz — OK, exact (p.10).
  - Image-method h → 1.08 m for a 5 ms gate at d = 48 cm — OK, exact (p.11–12: "for the delay of 5ms and d=48cm we get h=1.08m").
  - Quote "It is absolutely normal that ripples in a reverberant field are larger than 5dB." (§1, p. 3) — OK, verbatim, page/section exact.
  - Quote "It is recommended that the gate length should be 5ms or more (dictated with a time-bandwidth requirement for correct frequency response estimation on frequencies above 200Hz)." (§6, p. 11) — OK, verbatim, page/section exact.
  - Quote "Usually both curves do not match ideally, and additional scaling of 1-2 dB may be necessary in practice." (§5, p. 11) — OK, verbatim; correctly cited to §5 even though it prints on p.11 just before the §6 heading.
  - docs/anechoic-simulation.html: "a 5.604 ms gate is valid above 178 Hz" — **PARTIALLY WRONG**. "5.604 ms" is quoted verbatim (from the p.9 parenthetical), but the paper never itself pairs that figure with "178 Hz" — its headline claim is "valid above 177.9Hz," and its own arithmetic note gives 178.4 Hz. "178 Hz" is a plausible rounding of either number but is not printed.
  - 1.08 m and 48 cm/0.48 m — OK, both confirmed exact, printed together (p.11–12).

- **Verified facts card**:
  - Far-field criterion: independent of source geometry only beyond 6× the source radius. "For distance r > 6a the sound pressure is independent of the directional factor..." (§2, p.3)
  - Companion near-field measurement criterion: source distance under a/20. "near-field-response measured at a distance from the center of the membrane less than d < a/20" (§6, p.11)
  - Minimum recommended gate for valid estimation above 200 Hz is 5 ms. "the gate length should be 5ms or more" (§6, p.11)
  - Image-source geometry converts a target reflection delay + source–mic spacing directly into a required mount height (1.08 m for 5 ms at 0.48 m). (§6, p.11–12)
  - Reverberant-room ripple >5 dB is normal, not a fault sign. "It is absolutely normal that ripples in a reverberant field are larger than 5dB." (§1, p.3)
  - The baffle-diffraction correction is validated only over a narrow size ratio: source occupying 1/40 to 1/10 of the baffle sphere (θ0 = 5°–20°). (§3, p.5)
  - Purely geometric/high-frequency diffraction models can be *less* accurate at low frequency than this simple empirical model. "Such models can give larger errors on low frequencies than the simple model presented here." (§3, p.6)
  - Even the merged measurement-derived curve rarely matches ideally and needs an empirical 1–2 dB trim. (§5, p.11)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Directly transferable as methodology (not as a rotor study): the gating + image-source geometry for converting a target reflection delay and source–mic spacing into a required mount height is exactly the calculation needed to decide how high the rotor stand and vertical mic arc must sit above the nearest reflecting surface, or to time-gate a residual reflection out of a capture.

---

## Nash, A., "Qualification of an anechoic chamber." Proc. 23rd International Congress on Acoustics (ICA), Aachen, Germany, 9–13 Sept. 2019, pp. 1343–1349 — Nash_2019_ICA_qualification-of-an-anechoic-chamber.txt

- **Bibliographic check**: Title as printed: "Qualification of an anechoic chamber." Author: "Anthony NASH¹" (¹Charles M. Salter Associates, USA; email anthony.nash@cmsalter.com). Venue header: "PROCEEDINGS of the 23rd International Congress on Acoustics, 9 to 13 September 2019 in Aachen, Germany." Pages confirmed by printed page-footer numerals 1343–1349 (7 pages, matching 7 form-feed breaks in the extract). No DOI is printed anywhere. Filename is correct: year, venue, and title slug all match.

- **Claim audit** (MATRIX-3W.md and docs/anechoic-simulation.html):
  - "51 m³ IAC fully-anechoic chamber with exposed foam wedges and a partly-open expanded-metal floor grate" — OK. "51 m³" is in the Abstract; "IAC"-branded and "exposed foam wedges on all six surfaces" are in §1 Introduction — both on the same printed page (1343).
  - "qualified post-construction to ISO 3745 Annex A / ISO 26101"; "project specification required pure-tone (not broadband) test signals" — OK, verbatim spec confirmed p.1345.
  - Draw-away geometry, B&K 4295 OmniSource 100–1250 Hz, custom 1.5 m pipe + JBL 2426J for 800–12 500 Hz, tone clusters, GRAS 40AE mics, flattop FFT, pink-noise repeat (36 measurements incl. 14 duplicates), floor grate covered with 50 mm glass-fibre panels — all OK, matching the Method section verbatim/numerically.
  - Pink-noise fits "near-ideal at 2 kHz (slope −19.8, R² 0.9)" and "too shallow at 4–8 kHz (−16.2…−18.4)" — OK; note the source's *own* figure caption for the same chart instead names "4 kHz and 6.3 kHz" as the shallow bands, a minor internal inconsistency in Nash's own paper, not an error in the summary.
  - 2056 Hz slope −26.4 (R² 0.3), 1600 Hz −10.0, 3880 Hz −10.7, 125 Hz −7.6 (R² 1.0), 824 Hz −28.7 (R² 1.0) — all OK, exact.
  - Quote "Compared to bands of noise, the use of discrete tones is more revealing of residual acoustical reflections arising from the walls, floor, and ceiling surfaces. It is now quite obvious that the acoustical environment in the chamber is not behaving like a free field." (§7, p. 1347) — OK, verbatim and page correct.
  - Quote "The squared correlation coefficients appear to be acceptable; however, this appearance is deceiving since the 25-millimeter spatial sampling interval is only a small fraction of a wavelength." (§7, p. 1347) — OK, verbatim and page correct.
  - Verdict quotes ("could satisfy the ISO tolerances when using random noise but failed to qualify when using pure tones," Abstract p.1343; "In short, the chamber is absorptive but not anechoic," §8 p.1349) — both OK, verbatim, pages correct.
  - "no evidence that the wedges were ever qualified by testing them in an impedance tube" — OK, verbatim, p.1349.
  - Card 05 "2056 Hz fitted −26.4 dB/decade (R²=0.3), 1600 Hz fitted −10.0 (R²=0.5)" — OK; **the R²=0.5 is correctly attached to 1600 Hz** in the source (Fig. 6), not misattributed.
  - Card 07 "expanded-metal walking grate, reflective at high frequency" — OK.
  - Figure/legend combining "125 Hz — slope −7.6", "824 Hz — slope −28.7" and the 2056 Hz series into one chart: individual numbers OK, but **flag**: these three tones actually come from two *different* traverses/sources (125 Hz and 824 Hz from the low-frequency-source traverse, Fig. 7; 2056 Hz from the high-frequency-source traverse, Fig. 6) — the figure blends them without saying so. Also 824 Hz has two different printed slopes for the two sources (−28.7 R²1.0 low-source vs. −15.7 R²0.7 high-source); the figure correctly uses the low-source value.
  - "leaves ±1.5 dB at 1.32 m" — **NOT FOUND in text verbatim**; it is a derived value. Back-calculation from Nash's own 125 Hz fit is arithmetically consistent with a ±1.5 dB crossing near 1.32 m, but Nash never prints this number himself; the 824 Hz and 2056 Hz traces do not reach ±1.5 dB within the plotted 1.0–1.5 m range at all, so the annotation is specific to the 125 Hz series only and should say so.
  - Bibliography line — OK, matches exactly.

- **Verified facts card**:
  - ISO 3745 Annex A tolerance as applied here: "±1 decibel" for 800–5000 Hz, "±1.5 decibels" outside that (§1, p.1344).
  - Ideal free-field reference point: "a reduction in sound pressure of precisely 3.522 decibels (equivalent to 6.0206 decibels per doubling of distance)" at a 1.5 distance ratio (§7, p.1347).
  - Fine spatial sampling can be deceptive: "this appearance is deceiving since the 25-millimeter spatial sampling interval is only a small fraction of a wavelength." (§7, p.1347)
  - Perforated floor grate still reflects at high frequency: "Even though the floor grating has many perforations, it is still capable of reflecting high-frequency sound." (§1, p.1343)
  - Custom HF source directivity spec: "satisfied the ISO 3745 directivity requirements up to 90 degrees off axis." (§4, p.1345)
  - Passing broadband ≠ anechoic: "The chamber could satisfy the ISO tolerances when using random noise but failed to qualify when using pure tones." (Abstract, p.1343)
  - Root cause left unverified: "There was no evidence that the wedges were ever qualified by testing them in an impedance tube." (§8, p.1349)
  - Verdict: "In short, the chamber is absorptive but not anechoic." (§8, p.1349)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: High — drone rotor noise is strongly tonal (BPF + harmonics), and Nash's central finding is exactly the risk this rig faces: pure-tone testing exposes narrow-band reflection cancellations that broadband/pink-noise testing conceals, and floor-grate/fixture reflectivity plus unverified wedge absorption are both directly transferable hazards.

---

## Okuzono, T. (2024), "Computational Accuracy and Efficiency of Room Acoustics Simulation Using a Frequency Domain FEM with Air Absorption: 2D Study," Applied Sciences 14(1), 194. https://doi.org/10.3390/app14010194 — Okuzono_2024_ApplSci_room-FEM-air-absorption-2D.txt

- **Bibliographic check**: Title exactly as printed (p.1). Sole author: Takeshi Okuzono, Environmental Acoustics Laboratory, Kobe University. "Appl. Sci. 2024, 14, 194," DOI as above (printed in the header citation block and p.1 footer). Received 16 Nov 2023, Revised/Accepted 22 Dec 2023, Published 25 Dec 2023. Open access, CC BY, MDPI. Filename correct (author/year/journal/topic all match).

- **Claim audit**:
  - WHY paraphrase (lossless-FEM norm; lossy/complex-k accuracy-efficiency undocumented) — OK, matches Introduction verbatim in substance.
  - 2D 1 km duct, 1 Hz–20 kHz, 2.5 mm dispersion-reduced Q4 elements, 800 002 DOF, 6.8 elements/λ at 20 kHz — all OK, exact.
  - α from ISO 9613-1 Annex A, three atmospheres — OK.
  - "2D office (≈10.6 × 3.8 m)" — **NOT FOUND as a stated prose dimension.** No sentence in the running text gives the office's overall size; 10.6/3.8 appear only as axis labels in Fig. 6, whose OCR is garbled (interleaved with 8.2, 7.4 and grid coordinates) — plausible but not textually confirmable at the prose level.
  - "to 6 kHz," glass-wool Miki-model impedance (σ 6900–55 000 Pa·s/m²), CSQMOR solver, 24 threads — all OK, exact.
  - Attenuation error ≤0.84% at 20 kHz (0.05% at doubled resolution) — OK, exact.
  - D < 0.5 dB to 5 kHz for two atmospheres, ≈1.0 dB at 4–5 kHz for the third — OK, exact.
  - "iteration count falls up to ≈60%, CPU time −27.5…−39.2% (Table 1)" — **OK with a citation nuance**: the −27.5…−39.2% CPU range is exactly Table 1's Rcpu range, but the "≈60%" iteration-reduction figure is **not from Table 1** — it comes from the Fig. 9/10 discussion (baseline mesh, condition (a)); Table 1 itself (higher-resolution mesh, 3–6 kHz only) shows Riter of 27.7–38.8%. If "(Table 1)" was meant to source both numbers, that attribution is wrong for the 60% figure.
  - Abstract quote, Fig. 6 caption quote, extended-reaction acknowledgment — all OK, verbatim.

- **Verified facts card**:
  - Lossy-Helmholtz FEM reproduces ISO 9613-1 attenuation to <1% error to 20 kHz at ~7 elements/λ. (§3.2, p.6)
  - Halving mesh resolution pushes error past 2% above ~12 kHz — a direct simulation-validity ceiling. (§3.2, p.7)
  - Doubling resolution cuts the 20 kHz error to 0.05%. (§3.2, p.7)
  - Air absorption is negligible for room SPL prediction below ~2 kHz. (§4.2, p.9)
  - Including air absorption costs nothing extra in memory/DOF over the lossless approach. (§4.2, p.13)
  - Standard room-acoustics FEM by convention omits air absorption entirely. (Intro, p.2)
  - ISO 9613-1 Annex A's α combines four mechanisms and depends on frequency, temperature, humidity, pressure. (§2.2, p.4)
  - Study is explicitly 2D-only; author flags 3D validation as future work. (§5, p.14)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low/marginal — a generic 2D ordinary-room FEM accuracy study with no chamber qualification, reflection, fixture, or rotor content; only transferable point is that air-absorption/dispersion error only bites above ~2 kHz / near 20 kHz, relevant solely if a full-wave FEM of the chamber were ever built.

---

## Payne, R. C. & Simmons, D. J. (1996), NPL Report CIRA(EXT) 009 — Payne-Simmons_1996_NPL-CIRA009_environmental-correction-K2.txt

- **Bibliographic check**: **No title is printed anywhere in the extracted text** — the document goes directly from the report-number/date header ("ClRA(EXT) 009" / "April 1996") to the author block to "ABSTRACT." The phrase "Environmental correction factor K2" used in citations is a descriptive slug, not a verbatim printed title (their own ref. [9], a companion report by the same authors, *does* carry a full descriptive title in the reference list, which makes it plausible 009 also had one on an uncaptured cover element — but nothing in this text confirms it). Report number "ClRA(EXT) 009" (OCR "Cl" for "CIRA") unambiguously = CIRA(EXT) 009, matching the filename. Year: "April 1996" (p.1); "©Crown Copyright 1996," ISSN 1361-4053 (p.2) — matches. Authors: "R C Payne and D J Simmons," Centre for Ionising Radiation and Acoustics, NPL, Teddington — matches, order and names correct. Venue: NPL internal report, not a journal (no DOI; ISSN given instead). **Filename verdict**: correct on every verifiable element; the descriptive slug is not a verbatim title (none exists in the text) but accurately describes the content. **Caveat found while reading**: the report is internally inconsistent on Room E's area (Table 6 gives 258 m², Table 9 gives 358 m² for the same room; volume 274 m³ agrees in both) — doesn't affect any audited claim, which only cites the 274 m³ volume, but worth knowing if Room E's area is ever quoted from this source.

- **Claim audit**: every MATRIX-3W figure checked line by line — all **OK**, including: K2 range 0–7 dB across ISO 3744/3746/11200/11201/11202/11204 (synthesized across those standards, p.1); B&K 4204 source 90.9 dB ± 0.2 re 1 pW (p.3); room A hemi-anechoic to r = 1.5 m, 91.5 m³ (Table 9); room E 274 m³ (Tables 6 &amp; 9); 1.5 m hemisphere + parallelepipeds at 0.85/1.3/1.8 m (Table 7, p.12); B&K 2144 analyser, 15 s averages, repeatability <0.2 dB (p.14–15); measured Lw range 90.8–98.4 dB (p.15); "a potential range of K2A-factors of 7.6 dB" (§5.1, p.15); the room-A hemi-anechoic-only-to-1.5 m quote plus the outdoor 0.2 dB cross-check (§5.1, p.16); Room A absolute K2A 0/0.6/1.0/1.1 dB for surfaces 1–4 and A-weighted reverberation 2.5–5.7 dB (Table 10, p.18) — note the OCR renders the "0" for surface 1 as the letter "a," a scan artifact, not a real value; reverberation over-predicts +1.3 dB mean in room B, two-surface under-predicts −2.2 dB there (p.18); estimated-α table −2.8 dB mean room C (p.19); "particularly badly where the second surface was close to room obstacles" (§5.4, p.21 — this general-summary sentence is correctly combined with the room-B-specific −2.2 dB figure from elsewhere in the same paper, not a misattribution); source-near-wall raising K2A in rooms C/D (§5.5); final quote "the absolute method using a reference sound source is the only method that consistently provides an accurate assessment of K2A" (§6, p.23) — OK, verbatim. The single docs/anechoic-simulation.html bibliography line is confirmed as the **only** mention of Payne/Simmons/CIRA anywhere in that HTML file.

- **Verified facts card**:
  - ISO 3744 requires K2 < 2 dB (else disregarded); ISO 3746 permits larger K2. (§1, p.1)
  - Room A "only satisfies ISO 6926 up to a maximum 1.5 m radius" — a real hemi-anechoic room fails qualification beyond that specific working radius even though it nominally reads as "hemi-anechoic." (§5.1, p.16)
  - An outdoor hemi-anechoic reference confirmed true free-field behaviour independently: surface-4 vs surface-2 differed by only 0.2 dB outdoors. (§5.1, p.16)
  - Reverberation-time methods are invalid near-anechoic: "Room A presents hemi-anechoic conditions and so reverberation measurements are not strictly valid." (§5.2, p.17)
  - Theoretical model K2 = 10·log[1+4(r/R)²((1/α)−1)] shows K2's sensitivity to measurement radius grows sharply as the boundary becomes more reflective. (§3, p.6)
  - Two-surface method "should not be used where the larger enveloping surface is affected by reflections from nearby objects." (§6, p.23)
  - Source proximity to a wall measurably raises K2A, confirmed in two separate rooms. (§5.5, pp.21–22)
  - The absolute/substitution method with a calibrated reference source is "the only method that consistently provides an accurate assessment of K2A." (§6, p.23)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Relevant as chamber-qualification methodology (a nominally hemi-anechoic room stays hemi-anechoic only out to a specific radius; reverberation-time checks are invalid near-anechoic; source-to-wall/obstacle proximity measurably degrades results) — not rotor/aeroacoustics-specific.

---

## Prinn, A.G., "A Review of Finite Element Methods for Room Acoustics." Acoustics 2023, 5, 367–395. https://doi.org/10.3390/acoustics5020022 — Prinn_2023_Acoustics_review-FEM-room-acoustics.txt

- **Bibliographic check**: Title "A Review of Finite Element Methods for Room Acoustics" (article type: "Review"). Sole author Albert G. Prinn, Fraunhofer Institute for Integrated Circuits IIS, Erlangen, Germany. Printed citation (masthead, verbatim): "Prinn, A.G. A Review of Finite Element Methods for Room Acoustics. Acoustics 2023, 5, 367–395. https://doi.org/10.3390/acoustics5020022." Received 7 Feb 2023, Accepted 31 Mar 2023, Published 4 Apr 2023. Volume/pages 5, 367–395 (29 pages) match the DOI-derived article number (vol. 5, issue 02, article 022) — no contradiction. Filename correct.

- **Claim audit**:
  - "Prinn 2023, Acoustics (MDPI) 5:367–395" — OK, exact match.
  - "Type: journal (narrative review)" — OK, explicitly labeled "Review."
  - WHY paraphrase — OK, matches Abstract/Introduction.
  - HOW/§6 domain-decomposition example (2271 m³ auditorium, ~150M DOF, 3 s IR to 3 kHz, 512 cores, ~2.5 h) — OK, every number verified verbatim at §6.1.2 p.383 (and restated §7 p.388).
  - Locally-reacting/extended-reaction quote (§6.3.3, p.387) — OK, verbatim.
  - Pind et al. quote (p.387) — OK, verbatim.
  - Thydal et al. quote (§6.3.1, p.386) — OK, verbatim (a line-break in the OCR splits "not accurate" / "enough," which is why a naive single-line search can miss it, but the sentence is present and correctly attributed).
  - Conclusion paraphrase (§7, p.388) — OK, matches the four-bullet list verbatim.
  - docs/anechoic-simulation.html card 03 quote — OK.
  - docs/anechoic-simulation.html §02 domain-decomposition sentence (2271 m³, ~150M DOF, 3 kHz, 512 cores, ~2.5 h, 3-second IR) — OK, every number verified (source is Yoshida et al. [93], cited by Prinn).
  - docs/anechoic-simulation.html bibliography "Prinn, A. G. ... Acoustics 5(2) 22, 2023" vs MATRIX-3W's "5:367–395" — **WRONG (format) → the paper's own printed citation reads "Acoustics 2023, 5, 367–395"** (repeated twice in the PDF); the "5(2), 22" form does not appear anywhere in the source text. Not fabricated (the DOI suffix does decode to vol. 5/issue 02/article 022, a valid alternate MDPI style) but not what is printed — the html bibliography line should be replaced with the printed page-range form.

- **Verified facts card**:
  - Rule of thumb: 6–10 DOF per wavelength, "less valid as the frequency of interest is increased." (§2.4, p.371)
  - Dispersion/pollution-effect error bound given as an explicit two-term formula (Eq. 15). (§3.1, p.372)
  - Linear elements converge like 1/N². (§3.1, p.372)
  - FEM is "good for low-frequency analyses, for which geometrical acoustic models fail to capture the relevant physics." (§3.3, p.375)
  - Hybrid FEM-below/geometrical-above-Schroeder approach, with simulation results "highly dependent on the input parameters." (§4.1, p.378)
  - Large-model cost examples: 12,000 m³ room to 1 kHz needs >29M DOF; a 13,000 m³ room used 12M DOF on 256 CPUs with a slowdown above 128 processes attributed to communication cost. (§5.1, pp.380–381)
  - Reverberation-chamber-measured absorption coefficients are "not accurate enough," pushing sim-vs-measurement gaps "beyond just noticeable differences." (§6.3.1, pp.385–386)
  - Extended-reaction vs locally-reacting: LR "is not valid for many of the materials that are typically used to absorb sound, for example, porous absorbers." (§6.3.3, p.387)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low — a general large-room/auditorium FEM review with no rotor, fixture-scattering, or anechoic-qualification content; its transferable points are generic (FEM cost scaling, dispersion/pollution error, and the LR-vs-ER boundary caveat, relevant only if the wedge lining itself were ever simulated).

---

## Prislan, R. & Svenšek, D., "Ray-tracing semiclassical low frequency acoustic modeling with local and extended reaction boundaries," arXiv:1705.03825v1 [physics.comp-ph], 10 May 2017 — Prislan-Svensek_2017_arXiv_ray-tracing-semiclassical-low-frequency.txt

- **Bibliographic check**: Title as printed (running title: "Ray-tracing semiclassical acoustic modeling"). Authors: Rok Prislan and Daniel Svenšek, Dept. of Physics, University of Ljubljana. Surname spelling confirmed as **Svenšek** (caron over the second "s"), matching MATRIX-3W; the filename's ASCII "Svensek" is a simplification, not a misreading. arXiv identifier confirmed in the PDF sidebar: "arXiv:1705.03825v1 [physics.comp-ph] 10 May 2017" — exact match. No venue is printed anywhere (bare preprint; no DOI, no volume/pages); MATRIX-3W's "journal preprint (arXiv; JASA-style)" is only half right — the layout is a generic two-column physics/acoustics template with nothing asserting JASA. **External check (not from the file itself)**: this manuscript was eventually published, under a *slightly different title*, as Prislan & Svenšek, "Ray-tracing semiclassical (RTS) low frequency acoustic modeling validated for local and extended reaction boundaries," Journal of Sound and Vibration 437 (2018) 1–15, doi:10.1016/j.jsv.2018.08.041 — **JSV, not JASA**. (The authors' earlier companion paper, their own ref. [20], *was* in JASA — likely the source of the "JASA-style" guess.) Filename is accurate for what the file actually contains (the 2017 arXiv preprint, distinct in title from the 2018 JSV version).

- **Claim audit**: every MATRIX-3W figure verified — all **OK**, including: room dims 4.215×3.647×3 m; all four boundary conditions and their parameters (real z=60z0; membrane fm=50.6 Hz; 5 cm porous layer σ=500 Ns/m⁴, angle-dependent; mixed); RTS run size (6,758,400 rays, |B|<10⁻⁶, R=0.2 m, 0.05 Hz steps to 300 Hz, 4-day cluster run); COMSOL FEM reference (≥5 points/λ to 200 Hz); T20-vs-Sabine methodology; the §V quote on peak/deep correspondence; "<70 Hz systematically slightly underestimated"; ER-boundary room-size/sound-speed shifts (~3% larger, 1–8% lower); T20 discrepancies (15% avg/31% max excluding pure ER; 3%/5% for real impedance at 125 Hz; 17–227% for pure ER); both §I quotes on local-reaction inaccuracy and phase information. "Type: journal preprint (arXiv; JASA-style)" — **partially WRONG**: preprint is correct, "JASA-style" is unsupported by the text and contradicted by the eventual JSV publication (see bibliographic check). "Due to numerical noise" (MATRIX-3W paraphrase of the 17–227% ER discrepancy) is a fair gloss of the source's own explanation (finite floating-point accuracy suspected), not a literal quote.

- **Verified facts card**:
  - Geometrical/ray methods are limited to large rooms/high frequencies "where the sound field is not significantly shaped by individual room modes." (§I, p.1)
  - The method deliberately excludes diffuse/stochastic reflections, "known to be significant in geometrical modeling techniques." (§II.A, p.2)
  - Even the FEM "ground truth" is frequency-capped by compute cost — hence the 300 Hz ceiling. (§I, p.2)
  - Without parallelization the validation run "would be running for ~a month on a single core." (§III.B, p.5)
  - "Practically valuable results are obtained already with drastically less rays and reflections." (§III.B, p.5)
  - Best T20 agreement (3–5%) occurs where absorption is highest (125 Hz, real-impedance BC); low-absorption bands/boundaries are where RTS-vs-FEM disagreement blows up (up to 227%). (§V, p.9)
  - Extended-reaction boundaries are physically more accurate than locally-reacting but numerically the hardest case for a ray method. (§I, p.2)
  - Experiments on material samples "showed that the assumption of local reaction is not accurate for a layer of porous material covering a rigid base." (§I, p.2)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Directly on-topic methodologically (a purely acoustic, low-frequency, boundary-impedance-aware geometrical method), but it studies a furnished mid-size room, not an anechoic/free-field chamber, and never treats a directional source on a stand or a measurement arc; its main transferable lesson is that ray-based predictions of chamber behaviour are least trustworthy exactly where absorption is weak — i.e. at the chamber's own low-frequency limit.

---

## Ressl, M. S. & Wundes, P. E., "Design of an Acoustic Anechoic Chamber for Application in Hearing Aid Research" (WSEAS "Recent Advances in Acoustics & Music," ISSN 1790-5095, ISBN 978-960-474-192-2; year not printed) — Ressl-Wundes_nd_WSEAS_hearing-aid-anechoic-chamber-design.txt

- **Bibliographic check**: Title exactly as printed. Authors: Marc S. Ressl and Pablo E. Wundes, GEDA (Grupo de Electrónica Digital Aplicada), Buenos Aires Institute of Technology (ITBA), Argentina. Running header every page: "RECENT ADVANCES in ACOUSTICS & MUSIC"; footer every page: "ISSN: 1790-5095 … ISBN: 978-960-474-192-2." Printed page range **18–23** (six pages) — these are the actual printed page numbers, and MATRIX-3W's p.20/21/22 citations already correctly use this numbering. **Year: not printed anywhere in the document.** Exhaustive search (years, "WSEAS," conference name, session, dates, "as of") found nothing except reference-list publication years for *cited* works (Blanco/Herráez 1993; Blackstock 2000; Beranek/Sleeper 1946; Puep Ortega/Romá Romero 2003; Farina 2000), none of which date this paper. **The word "WSEAS" itself never appears verbatim in the text** — only the venue title and ISBN/ISSN are printed; "WSEAS" is an external identification of the publisher/series, plausible but not sourced from the document itself. No conference location, dates, or session number are printed anywhere. Filename verdict: correct — "nd" (no date) is accurate, and the topic slug matches precisely.

- **Claim audit**: every MATRIX-3W figure verified — all **OK**, including: 1.103 m³ volume; 250–4000 Hz target range; dimensioning by a common scale × three small primes; geometric cutoff equation (1) → 211.7 Hz; wedge cutoff fc=c/4h, h≥0.34 m required, built at 0.15 m → 571.6 Hz; double 30 mm MDF walls + 50 mm glass-wool gap, NC-10 target, 60 dB(A) max; 450 hot-wire-cut 25 kg/m³ PU wedges on Velcro modules; MATLAB image-source model with six first-order phantom sources; rigid-vs-lined-vs-inverse-square comparison; both §2.4 and §3 quotes (571.6 Hz caveat; best-measurement-location-near-the-opposite-corner) verbatim and correctly paged; T60 < 50 ms; the §5 "flat within 3 dB" quote verbatim; wedge absorption stated as not yet measured. One item is **WRONG (attribution)**: "insulation above 6 kHz below expectation (outer box unsealed)" — the text (§5, p.22) explicitly attributes the >6 kHz shortfall to "an improper seal of the **inner** box," not the outer box; "outer box not sealed" is a real, separate caveat mentioned elsewhere (§5 general disclaimer; Fig. 6 caption) but is not what the paper cites as the cause of the >6 kHz discrepancy.

- **Verified facts card**:
  - Small chambers can partially satisfy the governing qualification standard: "possible to comply with parts of ISO 3745." (§1, p.18)
  - ISO 3745's chamber-to-source volume rule (≥200×) directly bounds what a given small chamber can validly test: "devices of up to 5515 cm³ can be measured." (§2.2, p.18)
  - A rectangular cuboid is acoustically the worse choice for a small chamber (more standing-wave risk) but was picked anyway for simplicity. (§2.1, p.18)
  - Proportioning room dimensions from a scale × distinct small primes spreads out standing-wave modes. (§2.2, p.18)
  - Optimal measurement position was found empirically, near a corner, not assumed at room centre. (§3, p.21)
  - Purpose-built DUT fixtures ("small wooden stands") were designed rather than improvised. (§4.4, p.21)
  - Isolation mounts were sized to the actual inner-box weight (220 kg, 136–272 kg rated mounts). (§4.1, p.20–21)
  - The reflection model deliberately includes only first-order reflections (six image sources) — an explicit simplification. (§3, p.20)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: High — the closest analogue in the set to this project's own problem: a small (1.1 m³), low-cost, application-specific chamber built around a directional source on a fixed axis, with explicit geometric/wedge low-frequency cutoff trade-offs, purpose-built DUT stands, and a first-order image-source reflection model — though the source (a sub-4 kHz hearing-aid mic) is far smaller/lower-frequency than a drone rotor.

---

## Rodriguez, V. (NSI-MI Technologies), "Comparing Predicted Performance of Anechoic Chambers to Free Space VSWR Measurements," AMTA 2017 (39th Annual AMTA Symposium, Atlanta, GA, Oct. 2017), IEEE Xplore 8123694, doi:10.23919/AMTAP.2017.8123694 — Rodriguez_nd_NSI-MI_EM-predicted-vs-measured-chamber-performance.txt

- **Bibliographic check**: Title as printed (p.137/1): "Comparing Predicted Performance of Anechoic Chambers to Free Space VSWR Measurements." Single author: Vince Rodriguez, NSI-MI Technologies, Suwanee, GA. **Year/venue are not stated anywhere in the running text of the paper itself** — a full search for date/session/copyright lines found none; the only in-text year clues are citation years for *other* papers (up to AMTA 2016), which only establish this paper postdates October 2016. Printed proceedings pages 137–142, but no proceedings title/year printed on any page. **External verification** (not from the text — PDF metadata + Crossref, flagged as such): PDF CreationDate 21 Sep 2017; Crossref record gives DOI 10.23919/AMTAP.2017.8123694, container "2017 Antenna Measurement Techniques Association Symposium (AMTA)," IEEE Xplore doc 8123694 — i.e. **AMTA 2017**, not "AMTA 2016" as MATRIX-3W's parenthetical guess suggested (that guess was a correct in-text-only inference about the *citations*, not the paper's own venue). Filename's "nd" (no date) is no longer strictly accurate given this external evidence, though nothing in the PDF body itself supplies the date — the rest of the filename (author, "NSI-MI," topic) is accurate.

- **Claim audit**: every MATRIX-3W figure verified — nearly all **OK**: first-order ray model with 7th-order polynomial reflectivity fit; CST full-wave check (12×22×12 m, 700 MHz); three chambers' geometries and frequency ranges (18×11.5×11.5 m, 100 MHz–12 GHz; 13.41×6.1×6.1 m, 0.8–6 GHz; 12×4.12×4.27 m, X-band) — note the source's own **Abstract** actually gives the third chamber as "14 m long by 4.12 m by 4.27 m" while the **body** (§IV.C) gives "12 m long (40 ft) by 4.12 m (13.5 ft) by 4.27 m (14 ft)" — an inconsistency in the paper itself; the claim's "12×4.12×4.27 m" matches the (correct) body text, not the abstract's typo; 700 MHz predicted −34.21 dB vs CST −36.4 dB; large-chamber measured/predicted quartet at 100 MHz/400 MHz/4 GHz/12 GHz; small-chamber 800 MHz measured −32.21 vs predicted −25 dB — all OK, exact. Two items need correction: the quote "the measured reflectivity may be **overestimated**" is **WRONG → the paper prints "overstimated,"** a typo in the original source (verified against the PDF directly) — the claim silently "corrected" a verbatim quote, which fails strict quoting; and the citation "(§IV.B, p. 142)" for the ray-tracing-asymptotic-approach quote is **WRONG → it actually follows §IV.C** (the X-band/narrow-chamber subsection), not §IV.B (the 800 MHz small-chamber subsection) — the quoted text itself is verbatim correct.

- **Verified facts card**:
  - Model deliberately uses only first-order reflections: "A simple model... in which only the 1st order reflections are considered." (§II, p.138)
  - Assumes the source antenna's front-to-back ratio suppresses the end-wall-behind-source reflection. (§II, p.138)
  - Off-axis pattern roll-off reduces energy reaching specular points ~5 dB below the direct-path level. (§II/Fig.3, p.138)
  - Reflectivity-from-scan method: fit a 2nd-order polynomial per axis and treat the residual ripple as the reflection signature. (§III.A, p.140)
  - Scan-extent-vs-wavelength caveat: "at 100 MHz the QZ is 1/3 λ. This seems to be too small to be able to catch any ripple due to reflected energy." (§IV.A, p.141)
  - The ray-tracing/asymptotic approach explicitly degrades for small rooms: "results seem to be extremely conservative when compared to the measured results." (§V, p.142)
  - Explicit statement of the model's validity regime: "intended to be used when the dimensions of the structure are much larger that the wavelength." (end of §IV, p.142)
  - No uncertainty budget existed for the reference measurements used to validate the model: "no uncertainty analysis was provided with the test reports." (end of §IV, p.142)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: EM-domain analogue only — no direct acoustic applicability, but the transferable methodology is (a) simple first-order reflection/ray models are trustworthy only when the chamber is electrically large relative to wavelength, a caution directly relevant to a small chamber at the low end of a drone's 100 Hz–20 kHz band, and (b) a scan region must span several wavelengths to catch standing-wave ripple, which maps onto sizing a vertical mic arc against the longest wavelengths of interest.

---

## Russo, M., Kraljević, L., Stella, M., Sikora, M., "Acoustic performance analysis of anechoic chambers based on ISO 3745 and ISO 26101: standards comparison and performance analysis of the anechoic chamber at the University of Split." Euronoise 2018 Conference Proceedings, pp. 2225–2230 — Russo_2018_Euronoise_ISO3745-vs-ISO26101-Split-chamber.txt

- **Bibliographic check**: Full title as printed (wrapped across 4 lines) exactly as above. Authors in printed order: Mladen Russo, Luka Kraljević, Maja Stella, Marjan Sikora — "University of Split, FESB – Laboratory for Smart Environment Technologies... Split, Croatia." Copyright line: "Copyright © 2018 | EAA – HELINA | ISSN: 2226-5147" (year 2018, ISSN as given; organized under EAA/HELINA — consistent with a Greek/Hellenic-society-run event, though the word "Crete" itself is **not printed anywhere in the paper's text**, so the venue city is external knowledge, not text-verifiable). Running header: "Euronoise 2018 - Conference Proceedings." Pages confirmed via printed footers 2225–2230. No DOI printed. Filename correct.

- **Claim audit**: every MATRIX-3W figure verified, almost all **OK**: ISO 3745's 1977 lineage, ISO 26101's 2012/2017 editions, 2.8×1.7×2.05 m Split chamber, source-stability tolerances (±0.5/±0.2 dB), background criteria (≥10/≥6 dB), spacing rules, two-parameter vs single-parameter fit, λ/2→λ/4 traverse relaxation, the 100 Hz–10 kHz-for-full-conformity vs any-contiguous-range distinction, ARTA measurement setup, RT60-from-RT30 method — all confirmed. One page citation is **WRONG**: the quote "the lowest one-third-octave band we could measure was 250 Hz band in order to end the traverse 50 cm from the tips of acoustic wedges," cited as "(§3, p. 2229)," is actually on **p. 2228** — §3 begins on p.2228 and this sentence falls there; the *following* sentence about the measured range being "small and not suitable for practical applications" is the one that is actually on p.2229. All Table I tolerance values (±1.5/±1.0/±1.5 dB) — OK, exact. The 200 Hz/16 kHz boundary-test claim, the λ/2→λ/4 quote (§2.3.2, p.2227), and the RT60 "very low, values only in figure" claim — all OK, verbatim/confirmed. docs/anechoic-simulation.html's card 09, card 10, and the λ/2→λ/4 section text — all OK as paraphrases (card 10's "moving the source to one wall" is a fair paraphrase of the paper's own "sound source at one side"; the section text's "impossible to qualify low" is a mild amplification of the paper's softer "ability... was compromised," but the practical thrust is faithfully captured).

- **Verified facts card**:
  - ISO 3745 Annex A tolerance table: ≤630 Hz ±1.5, 800–5000 Hz ±1.0, ≥6300 Hz ±1.5 dB. (Table I, §2.3.4, p.2227)
  - Full-conformity range requirement differs sharply: ISO 3745 needs 100 Hz–10 kHz; "ISO 26101 does not specify any required frequency range." (§2.3.4, p.2227)
  - ISO 26101 spacing rule: ≤λ/10 below 1 kHz, 25 mm above. (§2.3.2, p.2226–2227)
  - Traverse-length relaxation λ/2→λ/4 between the 2012 and 2017 editions. (§2.3.2, p.2227)
  - Small-chamber low-frequency ceiling is set by wedge-tip clearance, not electronics: "in order to end the traverse 50 cm from the tips of acoustic wedges." (§3, p.2228)
  - Passing tolerance ≠ practically useful measurement volume: "the measured range is small and not suitable for practical applications." (§3, p.2229)
  - Off-centre source placement is the fix for range, not a standards choice: "sound source at one side... in order to have larger measurement range." (§3, p.2229)
  - Achieved performance: "our chamber achieves very low reverberation times." (§3/Conclusion, p.2230)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: High — a worked case study of a similarly small chamber (2.8×1.7×2.05 m) whose lowest qualifiable frequency is capped by wedge-tip clearance with a centred source, recovering usable range only via off-centre placement; the same geometric trade-off (mic-arc/rotor clearance from wedge tips vs. lowest trustworthy frequency, and the λ/4-vs-λ/2 traverse rule) governs this rig.

---

## Schmal, J., Herrin, D. W. & Fernández Comesaña, D., "Acoustic Characterization of a Quadcopter Using a Test Stand" (year/venue not printed in text; conference paper, cites Dec-2023-dated sources) — Schmal_nd_conf_acoustic-characterization-quadcopter-test-stand.txt

- **Bibliographic check**: Title printed exactly as above (p.1); matches filename slug. Authors: Jared Schmal and D. W. Herrin (University of Kentucky, USA), Daniel Fernández Comesaña (Microflown Technologies, The Netherlands) — matches. **Year/venue — searched hard; here is exactly what is and is not printed**: a subtitle "Session: Experimental Acoustic and Flow Measurements" (p.1) proves this is a session-organized multi-track proceeding, but the conference's *name* is never printed. No year, ISBN, DOI, or copyright line anywhere; "Quiet Drones" does **not** appear anywhere in the text (checked exhaustively) — the filename's implicit "Quiet Drones" attribution is **not confirmed by the text**. The clearest internal dating clue: reference [3] cites a Wall Street Journal article dated "Dec. 19, 2023" and [4] a Lancet Digital Health piece "Dec. 2023," both used as live Introduction citations — so the paper was written/finalized no earlier than very late 2023 (most likely 2024). Reference [12] cites the authors' own earlier paper, "Development of a UAV Test Stand," 52nd Inter-Noise, Japan, 2023 — the *only* place "Inter-Noise"/2023 appears, and it names a **different, earlier** paper, not this one's own venue. **Conclusion: year/venue cannot be confirmed from the text**; only a "written after Dec 2023" lower bound and a citation to a separate Inter-Noise-2023 paper by the same authors are available. Filename verdict: title correct; year/venue honestly left unstated ("nd"), matching what the text does and doesn't say.

- **Claim audit**: MATRIX-3W's "Session: Experimental Acoustic and Flow Measurements" quote, the "Quiet Drones... unclear in text" note, the 61 cm wheelbase, XRotor 40A ESCs/T-Motor MN3508/38.1 cm props/~3500 RPM/22.2 V, the University of Kentucky 6.1×6.1×3.0 m hemi-anechoic chamber and its "meets the ISO requirements... at 150 Hz and above" quote, the Microflown PU-probe draw-away geometry, and the Scan&Paint 3D scan parameters — all **OK**, exact. The flow-noise quote (§4, p.6) — OK, exact wording and page, with a minor nuance: "becomes negligible at approximately 450 Hz" in the source applies to *both* sound pressure and particle velocity, not to particle velocity alone as the parenthetical implies; only "masking tonal components below 300 Hz, including the BPF" is particle-velocity-specific. BPF-as-dipole — OK. "2nd harmonic as a monopole" is correct in content but is actually on **p. 8**, not p. 7 as the compound citation implies. Far-field kd≈1.8, the kd=7.3 chamber-edge quote, and the 0.8 m/1.6 m BPF-symmetry quote — all OK, exact. "Bottom-plane intensity is 'fragmented'" — **WRONG as a verbatim quote**: the source uses the noun "fragmentation" ("Significant fragmentation can be visualized on the bottom plane due to turbulence flow and frame interactions," §4, p.9; "caused fragmentation on the bottom side," Conclusion p.12), never the adjective "fragmented" — the underlying fact is correct, only the quoted word form is off.

- **Verified facts card**:
  - Chamber's own stated ISO floor: "meets the ISO requirements for acoustic testing at 150 Hz and above." (§3, p.4)
  - "The maximum distance that could be measured was limited by the dimensions of the anechoic chamber." (§3.1, p.4)
  - Approaching the chamber boundary contaminates results even inside a qualified room: the kd=7.3 pressure increase "is likely due to issues with approaching the edges of the anechoic chamber." (§4, p.7)
  - Explicit fixture mitigation: the stand arm was rotated and the motor mount placed at the arm's end "to minimize interaction with the test stand frame." (§4, p.6)
  - Flow self-noise masks the tonal content that matters most, "masking tonal components below 300 Hz, including the BPF." (§4, p.6)
  - Empirical far-field criterion: velocity and pressure converge "once the far-field is reached at kd equals 1.8." (§4, pp.7,10)
  - The rotor's underside/flow side is measurement-hostile: turbulence/arm interactions "disrupt the typical dipole pattern." (§4, p.6)
  - Harmonic-dependent source classification: BPF ~ dipole/loading noise, 2nd harmonic ~ monopole/thickness noise, via decay-rate fitting. (§4, pp.7–8)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: High — an empirical study of exactly this scenario (rotor emulated on a fixed stand in a small qualified hemi-anechoic chamber), documenting concretely where measurements go wrong (near the chamber boundary, and on the flow/underside plane of the rotor).

---

## Schmal, J., Herrin, D. W. & Fernández Comesaña, D., "Quadcopter Sound Characterization using a UAV Test Stand" (year/venue not printed in text; conference paper) — Schmal_nd_conf_quadcopter-sound-characterization-uav-test-stand.txt

- **Bibliographic check**: Title printed exactly as above (p.1); matches filename slug. Authors as in the sibling paper, but with full postal addresses given here (a more elaborate author block). **Year/venue — searched hard; here is exactly what is and is not printed**: no "Session:" line, no conference name, no year, ISBN, DOI, or copyright notice anywhere; "Quiet Drones" does **not** appear anywhere (checked exhaustively). No internally-dated news citations exist in this reference list (unlike the sibling paper) — the newest reference is [6], the same "Development of a UAV Test Stand" paper cited as Inter-Noise 2023, plus a 2021 JSV article. This gives only a "written at or after 2023" lower bound, with no independent narrowing clue. As with the sibling paper, the Inter-Noise-2023 mention refers to a *different, earlier* paper by the same three authors, not this paper's own venue. The elaborate author-postal-address format matches the format used for the cited Inter-Noise 2023 paper, which is suggestive but **not confirmation** of shared venue. **Conclusion: year/venue cannot be confirmed from the text.** Filename verdict: title correct; year/venue honestly left unstated. **docs/anechoic-simulation.html cross-check**: the bibliography line "Schmal et al. — quadcopter characterisation on a UAV test stand, Quiet Drones and Inter-Noise 2023 (hemi-anechoic, 6.1 × 6.1 × 3.0 m)" is **not confirmed by either Schmal paper's own text** — neither states it was presented at Quiet Drones or Inter-Noise 2023; both only cite a third, earlier paper as the actual Inter-Noise 2023 item. This html line appears to conflate the research programme (which does have a genuine Inter-Noise 2023 paper) with these two undated papers' own venues — an assumption, not a textually verified fact.

- **Claim audit**: the Inter-Noise-2023-as-ref.[6] note, the shared 6.1×6.1×3.0 m chamber and its ISO-≥150-Hz quote, the Scan&Paint plane geometry, the PU-probe draw-away parameters (two planes × seven doubling distances, 30 s averages), the 1–4 propeller range, the 120 Hz BPF dipole toroid, the 2484/3328 Hz monopole-like peaks — all **OK**, exact. The "turbulence... likely causing interference on the bottom plane" quote — OK content/wording/section, but **page number "p. 4" is not independently verifiable**: this file's text extraction contains no page-footer markers anywhere (unlike the sibling paper), so no page citation for this file can be confirmed or refuted from the .txt alone. The 1–4 propeller sound-power superposition (≈100–106 dB, Fig. 9) — OK qualitatively (text confirms "the sources are indeed uncorrelated"; the exact per-count dB values are only in the chart image, not extractable as discrete text numbers, so "≈100–106 dB" is a reasonable visual estimate, not textually verifiable to the decibel). The 125 Hz draw-away decay-rate numbers (10 dB/doubling from kd 0.23, 22 dB from 0.47, 7 dB from 1.86) — OK, exact. The bottom/flow-side decay-rate quote and the "maximum distance... limited by the dimensions of the anechoic chamber" quote — OK content/wording, page not independently verifiable for the same reason as above (this exact chamber-size sentence is genuine shared text also appearing verbatim in the sibling paper — not a misattribution).

- **Verified facts card**:
  - Same chamber ISO floor repeated: "meets the ISO requirements for acoustic testing at 150 Hz and above." (§3)
  - "The maximum distance that could be measured was limited by the dimensions of the anechoic chamber." (§3.2)
  - Explicit fixture-avoidance note: measurement height was chosen "to avoid obstructions on the bottom side of the test stand for the 5 and 10 cm positions." (§3.2)
  - Flow/turbulence breaks the near-field decay model specifically on the downwash side: "the decay rate is reduced and particle velocity does not converge with sound pressure." (§4)
  - Same fragmentation phenomenon as the sibling paper, on the bottom plane. (§4)
  - Multi-rotor sound power validated as uncorrelated superposition of single-rotor measurements for 1–4 propellers. (§4, Fig. 9)
  - Near-field scan benchmark: Scan&Paint probe roved ~5 cm from the propeller surface at 1 cm cell resolution. (§3.1)
  - Capture duration benchmark for a stationary ~3500 RPM hover: 30 s per point. (§3.2)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: High — same stand/chamber class as the sibling paper, adding a validated single-to-multi-rotor superposition result and further confirmation that the rotor's flow/underside plane is where near-field decay and directivity measurements break down.

---

## Schneider, S., "Numerical prediction of the quality of an anechoic chamber in the low frequency range," Journal of Sound and Vibration 320 (2009) 990–1003, doi:10.1016/j.jsv.2008.08.019 — Schneider_2009_JSV_numerical-prediction-anechoic-chamber-quality.txt

- **Bibliographic check**: Title exactly as printed (p.990). Author: S. Schneider, CNRS/LMA, Marseille. Venue exactly as printed: "Journal of Sound and Vibration 320 (2009) 990–1003," DOI as above. Received 12 June 2007, Accepted 18 Aug 2008, online 23 Oct 2008. **Filename correct.**

- **Claim audit** (against EXTRACTS-core.md and docs/anechoic-simulation.html card 03): every figure verified **OK**, exact: LMA Marseille facility, 5.4×6.3×11.4 m tip-to-tip, 3720 melamine wedges (0.3×0.3×0.4 m base + 0.7 m taper) in an iron-wire frame with 0.25 m air gap; 20–200 Hz pure-tone measurement with a bass-reflex box 1.6 m above floor tips, 0.2 m traverse step, reference mic 0.25 m from the driver; the deviation definition Lp = 20log|pexp/pinc| against a numerical free-field model of the actual source (not a fitted 1/r); the "100–160 Hz" and "170–190 Hz asymmetric" quotes (pp.993–994); "cannot be reproduced by any uniform-admittance model" (paraphrase of p.994); the "failed to predict... below ~150 Hz, regardless of the admittance applied" quote (p.996); the melamine-frame-mobility explanation (p.996); the three-lining α=0.997/1.0/0.997 comparison and "significant differences in the size of the 1.5 dB region" quote (p.997); the non-local admittance-matrix fix, nT=3, 138,280-unknown BEM solve, <1.5 h/frequency (pp.998–1001); the >80%-correct/~10%-false-positive result (p.1002); and the source-placement quote "the source should be placed as far as possible from the walls" (p.997). One nuance flagged: docs/anechoic-simulation.html's "(5.4 × 6.3 × 11.4 m, 0.7 m melamine wedges)" is **simplified, not wrong** — 0.7 m is only the tapering-section length; the full wedge is 0.4 m base + 0.7 m taper = 1.1 m, which could mislead a reader into thinking the whole wedge is 0.7 m. One bibliography item is **WRONG (incomplete)**: docs/anechoic-simulation.html's "Schneider 2009, JSV 320 990" (vol+first page only) should read **"990–1003"** — the printed page range is unambiguous (running header, every page).

- **Verified facts card**:
  - ISO 3745/ANSI S12.35 threshold as applied here: "maximum difference allowed... is 1.5 dB at frequencies below 630 Hz." (p.992)
  - Chamber asymmetry (170–190 Hz) is fundamentally unmodelable by any uniform-admittance approach, "as the surface admittance is always assumed to be uniform." (p.994)
  - Absorption-coefficient index is trustworthy only in a narrow regime: "Only when Re(Ỹ)<1 and Im(Ỹ)≈0... can the corresponding absorption coefficient be used to judge the quality of an acoustic lining." (p.997–998)
  - Truncation quality is material-dependent: melamine's elastic, moving frame requires including the adjacent wedge layer (nT=3) above ~100 Hz. (p.1000)
  - Full-chamber BEM solve: 138,280 unknowns, GMRes, 80–120 iterations/frequency. (p.1001)
  - The method is explicitly pitched as a parametric design tool, not just a post-hoc diagnostic. (p.1002)
  - Melamine's Biot mechanical parameters are given explicitly (E=0.16×10⁶ N/m², ν=0.44, ρ_frame=8.35 kg/m³, flow resistivity 1.2×10⁴ Ns/m⁴, porosity 0.99). (Table 1, p.999)
  - Even the best (localized-admittance) model retains ~10% false positives concentrated at 160–180 Hz, again attributed to the chamber's own asymmetry. (p.1002)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Directly relevant — the strongest evidence that a flat-wall/local-admittance model (what any small-chamber qualification would default to) systematically fails below ~150 Hz regardless of the admittance value fed in, that mounting-frame dynamics (not just the wedge material) drive that failure, and that "keep the source as far as possible from the walls" is direct, actionable guidance for siting the rotor stand and mic arc.

---

## Vorländer, M., "Computer simulations in room acoustics: Concepts and uncertainties." Journal of the Acoustical Society of America 133(3), 1203–1213 (2013), doi:10.1121/1.4788978 — Vorlander_2013_JASA_room-simulation-concepts-uncertainties.txt

- **Bibliographic check**: Title as printed: "Computer simulations in room acoustics: Concepts and uncertainties." Sole author Michael Vorländer, Institute of Technical Acoustics, RWTH Aachen. Received 10 May 2012, published online 6 Mar 2013. Venue exactly as printed: J. Acoust. Soc. Am. 133(3), March 2013, pp. 1203–1213 (masthead: "133(3)/1203/11" — 11 pages, 1203 through 1213 inclusive). DOI as above. Matches EXTRACTS-core.md's "133(3) 1203–1213" exactly. **Filename correct** — author, year, venue abbreviation and topic slug all match.

- **Claim audit**:
  - "Vorländer 2013, JASA 133(3) 1203–1213" — OK, exact match to the masthead.
  - Abstract quote ("prediction of reverberation times with accuracy better than the just noticeable difference requires input data...") — OK, verbatim, Abstract p.1203.
  - "it is not adequate to calibrate a computer model by modification of input data" — OK verbatim, but EXTRACTS-core.md's page flag "p. ~1208" is **WRONG → the correct page is p. 1206**, the opening paragraph of Sec. V (confirmed via page-footer cross-check).
  - docs/anechoic-simulation.html bibliography "Vorländer 2013, JASA 133(3) 1203" (no end page) — **incomplete, not wrong** → should read "1203–1213" to match the masthead fully.
  - Characterization "error-propagation analysis" as the paper's own method — OK; the paper itself uses this exact vocabulary repeatedly ("the statistical method of error propagation," Intro; "the theory of error propagation of uncertainties," Abstract; "Concepts of error propagation," §V.C.1 heading). Minor nuance: the "not adequate to calibrate" line is introduced as "the author is of the opinion" — a stated normative position — before the quantitative error-propagation math of §V.C, not literally a numeric output *of* that calculation; the html's phrasing blends a stated opinion with a derived quantitative result, both genuinely the author's but reached differently.
  - "Formal uncertainty-quantification studies in wave-based room acoustics target exactly three parameters: the flow resistivity of the porous absorber, its thickness, and the absorption of the remaining hard surfaces" — **NOT FOUND in text — not attributable to Vorländer 2013.** Full-text search for "flow resistiv," "porous," "thickness" returns zero hits for the first two and none for the third in this sense; Vorländer 2013 frames uncertainty only around the random-incidence absorption coefficient α (ISO 354) and the scattering coefficient s (ISO 17497-1), plus geometric level-of-detail and ray count. This sentence in docs/anechoic-simulation.html is **misattributed to Vorländer 2013** and should either cite its actual source or drop the Vorländer attribution for this clause.

- **Verified facts card**:
  - Wave models can now clear the Schroeder frequency by a wide margin in real time: "simulate a volume of approximately 15,000 m³ in real time up to a frequency of 180 Hz, which is far above the Schroeder frequency of 20 Hz." (§III.B, p.1204–1205)
  - A 1993–94 Braunschweig round robin (17 simulation participants, 7 measurement participants) showed "a surprisingly large scatter with a strong tendency to underestimate the absorption coefficients and thus to overestimate the reverberation time." (§IV, p.1206)
  - Purely specular (non-scattering) models systematically overestimate reverberation time; "after reflection order three or four, the main energy propagation goes through diffuse (scattered) sound." (§IV, p.1206)
  - Fine geometric detail is fundamentally incompatible with broadband modelling: surface elements "must be large compared with wavelengths in three decades... This is practically impossible." (§V.A.1, p.1206)
  - Curved-surface focusing is severe and not fixable by absorber/diffuser treatment on the curved boundary. (§V.A.2, p.1207)
  - Diffraction "is not accounted for by the basic simulation algorithms" of geometrical acoustics. (§V.A.3, p.1207)
  - ISO-354-derived absorption-coefficient uncertainty grows with α: ~0.1 at α=0.1/0.4, ~0.2 at α=0.9. (Table I, p.1211)
  - Central conclusion: "input data of absorption coefficients are not accurate enough to obtain simulation results with an uncertainty below the JND of reverberation time. The parameters clarity and strength are more robust." (§VI, p.1212)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low direct relevance — this is a large-room/concert-hall simulation-uncertainty paper with no anechoic-chamber, free-field, or rotor content; its only transferable lesson is the general methodological caution against tuning a model's inputs to match measured results, and against trusting simulation accuracy finer than the input data's own measurement uncertainty.

---

## Wang, C.-N. & Tang, M.-K., "Boundary element evaluation on the performance of sound absorbing wedges for anechoic chambers," Engineering Analysis with Boundary Elements 18 (1996) 103–110, PII S0955-7997(96)00017-3 — Wang-Tang_1996_EABE_BEM-sound-absorbing-wedges.txt

- **Bibliographic check**: Title exactly as printed (p.103). Authors: Chao-Nan Wang and Ming-Kun Tang, Dept. of Naval Architecture and Ocean Engineering, National Taiwan University. Venue exactly as printed: "Engineering Analysis with Boundary Elements 18 (1996) 103-110." No DOI is printed (predates routine DOI assignment); only the PII (S0955-7997(96)00017-3) is given — the Elsevier PII→DOI convention would map this to 10.1016/0955-7997(96)00017-3, but that string is not itself printed, so it is noted as inferred, not printed. Received 25 Sep 1995, Accepted 29 Apr 1996; copyright line reads "© 1997," a printing/copyright-date quirk against the "18 (1996)" cover date, not a citation error. **Filename correct.**

- **Claim audit**: BEM-of-a-single-wedge-with-Delany–Bazley method, validation against Koidan et al. and AMSJ data, cutoff defined as |R|=0.1, the "strongly affected by the length of the wedge and the flow resistance" quote (Conclusion, p.109), hybrid-wedge cutoff reduction, "10–20 cm off the tip changes little," "30 cm... wedge is not suitable" quote — all **OK**, exact/verbatim. One item is **WRONG (partial)**: "base thickness and air-gap thickness (0–20 cm) have little effect on cut-off" — the 0–20 cm range is correct only for **air-gap** thickness (Figs 7, 10: 0/10/20 cm); the **base-thickness** studies (Figs 6, 9, confirmed against the source PDF page images since the OCR was ambiguous) actually use **10/20/30 cm**, not 0–20 cm. The qualitative finding itself ("little effect on cut-off, raises absorption") is correctly quoted from the Conclusion. The bibliography line "Wang & Tang 1996, Eng. Anal. Bound. Elem. 18 103" (vol+first page only) vs EXTRACTS-core.md's "18 103–110" — **incomplete → should read 103–110**, the printed range on every running header; also note the article itself never uses the abbreviated journal form "Eng. Anal. Bound. Elem." anywhere — that is a standard indexing abbreviation, not something printed in the source.

- **Verified facts card**:
  - Analysis is explicitly 2-D only, a real limitation for extrapolating to a 3-D chamber corner/room. (§1, p.104)
  - Study is capped at 500 Hz, well above Schneider's problematic <150–200 Hz band. (§5.1, p.107)
  - Delany–Bazley was originally fibrous-only; open-cell foam required separate empirical extensions (Cummings; Astley & Cummings). (§1, p.103–104)
  - Mesh-convergence rule: "at least six constant elements are required for a wave length at the corresponding frequency." (§5.1, p.107)
  - Hybrid-wedge orientation matters directionally: larger flow-resistance material must go at the tip (pyramid), not the base, or performance is degraded. (§5.4, p.109)
  - Wedge length is the single strongest lever on cutoff: "as the length of the wedge increases, the cut-off frequency is obviously reduced." (§5.2.1, p.107)
  - Foam (D12) and fibrous wedges trend similarly but use separate empirical material constants (Table 1). (§5.3.2, p.109)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Moderately relevant as a wedge-sizing/design reference (length dominates cutoff; base/air-gap thickness trades absorption for depth; hybrid wedges and tip-cutting are viable space-saving options), but it is a single-wedge, 2-D, ≤500 Hz impedance-tube model with no room-scale reflection or rotor-noise treatment, so it cannot diagnose an already-built small chamber's measured deviations the way Schneider (2009) can.

---

## Beranek, L. L., Sleeper, H. P. & Moots, E. E. — "The Design and Construction of Anechoic Sound Chambers" (OSRD Report No. 4190, 1945) — beranek_sleeper_1946_anechoic_chambers.html

- **Bibliographic check**: The HTML file is a GPO OCR transcription of **OSRD Report No. 4190**, titled exactly "THE DESIGN AND CONSTRUCTION OF ANECHOIC SOUND CHAMBERS (Relevant to Service Control Nos. NA-108 and AC-9)," submitted by **L. L. Beranek, H. P. Sleeper, Jr., and E. E. Moots** — three authors, not two — from the Electro-Acoustic Laboratory, Cruft Building, Harvard University, under NDRC Division 17, Section 5, Contract OEMsr-658. It is dated **"Report of October 15, 1945"** ("October 15, 19^5"/"I9U5" in the OCR). There is no page count, volume, issue, or DOI printed anywhere, and the string "1946" does not appear anywhere in the full text (checked by exhaustive grep) — nor does "JASA," "Journal of the Acoustical Society," or any journal citation. The commonly cited companion publication, Beranek & Sleeper, J. Acoust. Soc. Am. 18(1) 140 (1946), doi:10.1121/1.1916351, **cannot be verified from this document** — the file on disk is the 1945 OSRD report, not the 1946 journal article, and the third author (Moots) present here is not carried into the two-author JASA citation (whether that reflects a real authorship change or an omission cannot be determined from this file alone). **Filename verdict**: `beranek_sleeper_1946_anechoic_chambers.html` names only two of the three submitting authors and a year (1946) not evidenced anywhere in the file's own content (dated 1945); the topical part of the name is accurate. Treat the bibliographic year/venue/DOI used elsewhere as citing a *related but different, unretrieved* document (the JASA article), not this OSRD report.

- **Claim audit** (against docs/anechoic-simulation.html):
  - Table row "Quarter-wavelength rule / Beranek & Sleeper 1946 / First-cut absorber depth for a target cut-off / Normal incidence, plane wave, fibrous wedge" — **OK** — the report states "the lowest frequency at which good absorption is obtained, is that for which the length of the wedge equals approximately one-fourth of a wave length" (Section III.C.5, p. 28), exactly the rule attributed. ("Gives depth, not chamber performance" is a fair summary of this specific method; note the report separately also contains real chamber-level qualification data, Section IV — the table's characterization applies to the wedge-design formula, not to the whole report.)
  - Card "01 — cut-off": "Beranek & Sleeper 1946: 40 Hz needs 94 in from tip to backing wall." — **OK** — verbatim: "for absorptions down as low as 40 cps, a wedge structure would need to have a total length of 94 Inches measured from its tip to the rigid backing wall" (Section III.C.5, p. 29).

- **Verified facts card**:
  - Cutoff frequency is explicitly defined as where the pressure reflection coefficient reaches 10%: "A cutoff frequency of 150 cps, i.e., the frequency at which R reaches 10%, was obtained for a total depth of 25 inches." (Section II.B.6, p.12/8, "Medium Length Linear Wedge Structure, No. 59")
  - Quarter-wavelength design rule, in the authors' own words: "the lowest frequency at which good absorption is obtained is that for which the length of the wedge equals approximately one-fourth of a wave length." (Section III.C.5, p.28)
  - A longer wedge for a lower cutoff has a real material cost: a 94-inch wedge for 40 Hz needs flow resistance "4.8 acoustic ohm per inch," a "very low density" material that "results in wedges which are frail." (Section III.C.5, p.29)
  - Untreated floor structure degrades high-frequency performance in a small chamber: "the greater deviations at the higher frequencies are caused by the presence of the iron grills and the supporting steel structure which cover about one half the total area of the floor." (Section IV.E, p.~59–60)
  - Equipment inside the chamber measurably worsens free-field deviation: carts "in" vs "out" show deviations up to +3.0 dB vs +1.0 dB at 1000 cps, 20–30 ft (Table III, Section IV.C–D, p.52–55).
  - Only one of three possible qualification methods was actually used, for lack of time: "at least three methods might be used... Because of the lack of time, the first and most simple of these tests [inverse-square-law draw-away] was all that was performed." (Section IV.A, p.52)
  - Achieved tolerance in the large Harvard chamber (70–10,000 cps): "±0.3 db... 4 to 10 feet; ±0.5 db... 10 to 20 feet; ±1.0 db... 20 to 30 feet; ±1.5 db... 30 to 40 feet." (Section IV.D, p.55)
  - A small chamber is explicitly reported as cramped once lined: "11 x 15 x 10 feet" before treatment left "a working space of about 7 x 11 x 6 feet" after a 25-inch wedge structure, "somewhat crowded for any other than small apparatus measurements." (Section IV.E, p.59)

- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Directly relevant as the origin of the quarter-wavelength wedge-depth rule this project's own review cites, and its own qualification data illustrate two hazards this rig shares — an open/grated floor degrading high-frequency performance, and in-chamber fixtures (their "carts," analogous to a stand/mount arm) measurably worsening the free-field deviation.

---

## Cross-cutting notes for the maintainer

- **Every paper in scope was retrieved and read in full** (txt for the 14 PDFs, `w3m -dump` of the OCR HTML for Beranek & Sleeper) — nothing here rests on an abstract.
- **Two undated conference papers now have externally-verifiable venues/years that the text itself does not print**: Rodriguez (NSI-MI) is AMTA 2017 (Crossref DOI 10.23919/AMTAP.2017.8123694, IEEE Xplore 8123694 — from PDF metadata + Crossref, not the paper's own text), and Prislan & Svenšek's 2017 arXiv preprint was eventually published as a *retitled* JSV 2018 paper (doi:10.1016/j.jsv.2018.08.041), not in JASA as MATRIX-3W had guessed.
- **The two Schmal papers' "Quiet Drones and Inter-Noise 2023" venue claim in docs/anechoic-simulation.html is not supported by either paper's own text** — both papers only cite a separate, earlier Inter-Noise 2023 paper by the same authors ("Development of a UAV Test Stand"), not their own venue. This should be corrected or hedged in the review.
- **Beranek & Sleeper**: the file actually on disk is the 1945 OSRD report (three authors: Beranek, Sleeper, Moots), not the 1946 JASA article commonly cited (two authors) — the bibliographic entry in docs/anechoic-simulation.html cites a document this project has not actually retrieved.
