# AUDIT-4 — bibliographic and claim audit of 11 chamber-problems papers

Scope: `papers/chamber-problems/` — Haasjes, Hochbaum, Jawahar, Jenny (BYU thesis), Jenny & Anderson (JASA-EL),
Kim, Ma 2022 (Appl. Acoust., active-control MPP), Ma 2022 (Quiet Drones), Ma 2024 (Acoust. Aust.),
Merino-Martínez, Singh. Each paper's full `txt/` extract was read at source (long documents by section/`sed`
range) and checked against every claim made about it in `EXTRACTS-local.md`, `EXTRACTS-downloaded.md`
(including its Batch C section), `MATRIX-3W.md`, `../../docs/anechoic-chamber-problems-brief.html` and
`../../docs/chamber-literature-synthesis.html`. Bibliographic details were checked against the PDF's own
title/first/last pages where the `.txt` extraction was ambiguous. This file is the audit; where it disagrees
with the four documents above, this file — because it was checked against the primary sources — governs, and
those documents should be corrected accordingly.

---

## Haasjes, R. (2025). "Towards an active acoustic anechoic chamber." PhD dissertation, University of Twente. DOI: 10.3990/1.9789036562836. — Haasjes_2025_PhD-Twente_active-acoustic-anechoic-chamber

- **Bibliographic check**: Title (printed, cover and title page): "Towards an active acoustic anechoic chamber." Author: Rick Haasjes. Type: PhD dissertation, University of Twente, publicly defended Monday 20 January 2025, 14:45. Promotor: prof. dr. ing. B. Rosić; co-promotor: dr. ir. A.P. Berkhoff. ISBN (print) 978-90-365-6282-9, ISBN (digital) 978-90-365-6283-6, DOI https://doi.org/10.3990/1.9789036562836. Copyright line reads "© 2024 Rick Haasjes" (colophon page), i.e. printed/copyrighted 2024 but defended 2025 — the year discrepancy the existing extract flagged ("year not printed in text read") is resolved: **both years appear, on different pages, for different reasons** (copyright vs. defense). Filename `Haasjes_2025_PhD-Twente` is **correct** — right author, right institution, and 2025 is the correct citation year for a doctorate (conferred at the public defense), not the copyright-page year.

- **Claim audit**:
  - "a typical acoustic anechoic chamber has a lower cut-off frequency of up to 200 Hz, meaning that free-field conditions are not guaranteed below this frequency" (Summary, p. i) — OK, verbatim.
  - "6 dB for every doubling of the distance" free-field description (§1.1, p. 1) — OK, verbatim ("the sound pressure level (SPL) decreases by 6 dB for every doubling of the distance between the source and receiver").
  - Wedge cut-off (10% pressure reflection / 99% absorption, impedance tube) "not necessarily equal to the cut off frequency of the AAC" (§1.2, p. 3) — OK, verbatim, correct page.
  - "an AAC designed with a cut off frequency of 75 Hz is studied, which showed perturbations in the 110 to 160 Hz frequency range. Therefore, the cut off frequency lies at 200 Hz rather than 75 Hz. One of the identified causes of imperfections is the doors" (§1.2, pp. 3–4) — OK, verbatim.
  - brief.html: chamber "designed for 75 Hz" (given as a direct quote) — **WRONG → not a verbatim quote**. The thesis says "designed **with a cut off frequency of** 75 Hz," not "designed for 75 Hz." The rest of the same sentence, "lies at 200 Hz rather than 75 Hz," **is** verbatim. Minor quote-fidelity slip, not a factual error.
  - Harvard AAC deviations from inverse-square law "below about 100 Hz" (§1.2, p. 4) — OK, verbatim.
  - UNAM chamber: largest deviations "below 200 Hz, and increase for decreasing frequencies" (§1.2, p. 4) — OK, verbatim.
  - Fresnel-volume argument: chamber volume smaller than Fresnel volume around direct path affects forward-scattered amplitudes (§1.2, p. 3) — OK.
  - "At this point it can be concluded that AACs suffer from low-frequency sound waves (up to about 200 Hz) reflecting off the walls, in some cases even above the cut off frequency the chamber is designed for." (§1.2, p. 4) — OK, verbatim, exact page.
  - "Existing AAC's suffer from low-frequency reflections of up to 200 Hz [18,31,32], due to limitations of the passive absorption material." (§1.6.1, p. 13) — OK, verbatim, exact page.
  - Scattering-filter identification (Friot et al. approach) by removing the diffracting object "ill-conditioned" and impossible for chamber walls (§1.4, p. 10) — OK in substance; exact wording spans pp. 10–11, a minor page-range imprecision, not an error.
  - 2-D rig: 0.92 × 0.92 m footprint, height 20 cm, "considered two-dimensional up to about 850 Hz," glass lid 1.2 cm (§6.2, pp. 95–96) — OK, all verbatim/exact.
  - 12 secondary Visaton W130X sources on the edges, 3 per side, 0.3 m spacing (§6.2, p. 96) — OK, verbatim.
  - 12 primary sources fed through 1 m tubes to the centre (§6.2, p. 96) — OK, verbatim.
  - 12 sensors on a circle, each with 3 radial microphones (§6.2, p. 101; restated Ch. 7) — OK, verbatim.
  - Numerical small-scale model: 0.84 m square room, walls Z = 10ρc, 12 channels, sensors on r = 0.24 m (§5.3, pp. 78–79) — OK, verbatim.
  - Numerical large-scale model: 5 × 5 m room, 200 channels, sensors at rs = 1.4 m (§5.4, pp. 90–91) — not directly re-verified (outside the four required-read sections), but a spot check at p. 92 (200 sources/200 reference sensors/225 performance sensors) is consistent with it, not contradictory.
  - Spatial-Nyquist spacing dmax = c/(2 fmax) = 0.286 m for 600 Hz (§5.3, p. 79; recurs in §6.2, p. 102) — OK, verbatim, confirmed in both places.
  - Small-scale numerical: 15.4 dB (with artificial delay) / 13.8 dB (delay removed) reduction (§5.3, p. 84) — OK, verbatim, exact page.
  - Large-scale numerical: 13.4 dB average reduction (§5.4, p. 92) — OK, confirmed.
  - Real-time PBC-CG: 9.6 dB average reduction up to ~600 Hz (§6.3, p. 112–113) — OK, verbatim; extract's page cite is off by one page (113), a negligible rounding, not a substantive error.
  - Real-time CC-CG: 9.4 dB average reduction (§6.4, p. 117–119) — OK, verbatim; same minor ±1-page note.
  - Active control "increases the noise floor... after the impulse response has decayed" (§6.3, p. 113) — OK, verbatim.
  - T10 reduced 0.036/0.037/0.036 s → 0.022/0.016/0.020 s (PBC-CG) — OK, exact match sensor-by-sensor.
  - T10 reduced 0.037/0.036/0.036 s → 0.026/0.017/0.023 s (CC-CG) — OK, exact match sensor-by-sensor.
  - T10 fit "avoid the influence of direct sound or strong early reflections," regression −5 to −15 dB — OK, verbatim.
  - Secondary-source spacing 0.3 m limits accurate secondary-field generation to 570 Hz rather than 600 Hz (§6.2, p. 102) — OK, verbatim, exact page.
  - Future work: 3-D real-time extension; effect of secondary sources on HF reflections unstudied; particle-velocity sensors could lower the limit further (Ch. 7, pp. 122–123) — OK, all three verbatim.
  - MATRIX-3W.md row 16 (WHY/HOW/WHAT, T2/T6/T7("doors")/T8 flags, Level III, Quality A) — OK, consistent throughout; the "T7 doors" flag correctly reflects a case Haasjes *cites*, not an original Haasjes measurement, and the matrix does not misattribute it as one.
  - synthesis.html row (line 106): "9.4–9.6 dB reduction to ~600 Hz real-time; chambers 'suffer from low-frequency sound waves (up to about 200 Hz) … even above the cut off frequency'" — OK, verbatim and numerically correct.
  - synthesis.html T2 paragraph (line 162): "Schneider and Haasjes show doors and mounting add to it" — OK in substance, though again this is Haasjes citing another study's chamber, not his own measurement.
  - synthesis.html T8 paragraph (line 170): "Active control reaches 9–15 dB in a 2-D rig and in simulation (Haasjes)" — OK, consistent with the 9.4–15.4 dB range across numerical (13.4–15.4 dB) and real-time (9.4–9.6 dB) results.
  - synthesis.html bullet (line 213): "Expect the room's real limit 20–30% above the wedge cut-off... (T2; Jiang, Schneider, Haasjes, Merino-Martínez)" — OK, consistent with the 75→200 Hz (2.67×) framing, correctly presented as a cross-source aggregate rather than a single Haasjes number.

- **Verified facts card**:
  - A typical anechoic chamber's usable low-frequency limit is well above the wedge's own absorption cut-off: "a typical acoustic anechoic chamber has a lower cut-off frequency of up to 200 Hz" (Summary, p. i).
  - A chamber's wedge-material cut-off and its real free-field cut-off are different quantities: "the cut off frequency of the absorption elements is not necessarily equal to the cut off frequency of the AAC" (§1.2, p. 3).
  - A real chamber commissioned for 75 Hz measured perturbations far above that: "showed perturbations in the 110 to 160 Hz frequency range. Therefore, the cut off frequency lies at 200 Hz rather than 75 Hz" (§1.2, pp. 3–4).
  - Chamber doors are a specifically identified reflection source even when acoustically lined: "One of the identified causes of imperfections is the doors in the AAC, even though they are fitted with acoustic lining" (§1.2, p. 4).
  - General conclusion spanning the literature reviewed: "AACs suffer from low-frequency sound waves (up to about 200 Hz) reflecting off the walls, in some cases even above the cut off frequency the chamber is designed for" (§1.2, p. 4).
  - Active noise control (KHI estimate of reflected field from a ring of pressure+velocity microphones) achieved "an average reduction of 13.4 dB" in a 200-source/200-sensor/225-performance-sensor large-scale numerical room (§5.4, p. 92).
  - In a real physical 2-D rig, active control gave "an average of 9.6 dB" reduction up to ~600 Hz (PBC-CG) and 9.4 dB (CC-CG) (§6.3, p. 113; §6.4, p. 119).
  - Control is not free of side effects: it "increases the noise floor, as can be seen when the impulse response has decayed" (§6.3, p. 113).
  - Reverberation time T10 dropped from ~36–37 ms to 16–26 ms across three verification sensors under active control (§6.3–6.4, pp. 113, 119).
  - The method's frequency ceiling is set by microphone/loudspeaker spacing via dmax = c/(2 fmax); with 0.3 m loudspeaker spacing the accurate limit is 570 Hz rather than the nominal 600 Hz (§6.2, p. 102).

- **Relevance**: Low, but real: SoundVisualizer's chamber (like every passive room Haasjes reviews) will have a real low-frequency free-field limit set by reflections, not just wedge geometry, and doors/fixtures are a named cause worth checking; the active-control method itself (ring-of-microphones KHI + FIR feedforward) is far beyond SoundVisualizer's scope and not something to implement.

---

## Hochbaum, F., Herold, G., Kempen, V.R., Fiebig, A. (2026). "Drone Directivity Measurements under Realistic Flight Conditions in an Anechoic Environment for Spectral and Psychoacoustic Characterization." Quiet Drones 2026, Delft, 29 June – 1 July 2026 (session: UAS/UAM noise modeling). — Hochbaum_2026_QuietDrones_drone-directivity-anechoic-realistic-flight

- **Bibliographic check**: Title (printed exactly): "Drone Directivity Measurements under Realistic Flight Conditions in an Anechoic Environment for Spectral and Psychoacoustic Characterization," subtitled "Session: UAS/UAM noise modeling." Authors: Felix Hochbaum (Engineering Acoustics, TU Berlin), Gert Herold (DLR, Institute of Propulsion Technology, Engine Acoustics Dept.), Vanessa R. Kempen (Chair of Flight Guidance and Air Transport, TU Berlin), André Fiebig (Engineering Acoustics, TU Berlin). **Venue correction — the existing extract's "venue unclear in text" is wrong; the venue IS printed, but only as a raster logo image on p. 1 that `pdftotext` drops entirely**: "QUIET DRONES 2026 / Delft, 29th June - 1st July 2026." This is the same Quiet Drones symposium series as `Ma_2022_QuietDrones` and `Rasmussen-Winberg_2022_QuietDrones` in this same folder, just the 2026 Delft edition. No DOI, no ISBN, no paper/session number, no volume or serial page range anywhere in the PDF (checked pp. 1 and 13 directly) — only internal pagination 1–13. PDF metadata: Producer pdfTeX-1.40.27, CreationDate 2026-06-19 (10 days before the conference), Title/Author fields blank. Filename: year "2026" is correct (confirmed via the venue graphic, not guessable from text alone); "conf" is accurate but under-specified — for consistency with sibling files it would ideally read `Hochbaum_2026_QuietDrones_...`, though this is a naming-convention suggestion, not an error.

- **Claim audit**:
  - Chamber "13.5 m, 8.3 m, and 7.4 m (L × W × H) and a lower cut-off frequency of 63 Hz": OK (p. 3, verbatim).
  - "walkable Kevlar mesh floor," "heavy-duty safety nets": OK (p. 3).
  - "usable flight volume ~10 × 6 × 3.5 m": OK, exact (p. 3).
  - Wedge depth / qualification standard "not stated": OK — neither appears anywhere in the text.
  - "64 GRAS 40PK 1/4 in. mics at 102.4 kHz": OK, exact (p. 3).
  - X500 1.96 kg, UBADRON 12 kg / 2.6 m tip-to-tip: OK, exact (pp. 2–3).
  - "blocks rejected if any FFT bin exceeded 70 dB below 100 Hz (X500) or 77 dB below 40 Hz (UBADRON)": OK, exact (pp. 5–6).
  - "For the X500 55.2% and for UBADRON 56.4% of the checked blocks were rejected" (Fig. 4, p. 6): OK.
  - "Owing to the UAV's size and the resulting rotor downwash, no valid measurements were obtained below the UAV" (p. 9): OK, exact.
  - "the BPF band of the UBADRON partly falls below the cut-off frequency of the anechoic chamber" (p. 9): OK, exact.
  - Interpretation-guidance quote on 245°–295° / ~65° uncertainty regions, "attributed to the low number of valid observations and to possible outliers or wind-induced disturbances" (p. 9): OK, exact.
  - "Recirculation: not mentioned": OK — full-text search confirms no occurrence of "recircula*" anywhere in the paper.
  - MATRIX-3W row 39, "55% of blocks rejected for wind under the drone": imprecise — 55.2% is the X500 figure only; UBADRON's is 56.4%. Not wrong, but collapses two distinct numbers into one without saying which drone.
  - synthesis.html row 108 and brief.html line 122 repeat the same "55%" simplification: same imprecision.
  - brief.html line 122's shared-row framing ("Excess below ~50–100 Hz only at microphones under the rotor... Windscreens, block rejection by LF threshold... Hochbaum 2026 ●"): OK for Hochbaum specifically — matches the paper's own rejection-by-frequency-threshold method and below-drone mic placement.

- **Verified facts card**:
  - Venue is printed only as an image, invisible to text extraction: "QUIET DRONES 2026 Delft, 29th June - 1st July 2026" (p. 1, graphic).
  - Chamber: "the fully anechoic room of the Engineering Acoustics Lab at TU Berlin, with dimensions of 13.5 m, 8.3 m, and 7.4 m (L × W × H) and a lower cut-off frequency of 63 Hz" (p. 3).
  - Usable flight volume bounded by a walkable Kevlar mesh floor and safety nets: "approximately 10 m × 6 m × 3.5 m" (p. 3).
  - Wind, not acoustics, dominates near-source low-frequency data: "microphones located directly below the UAV were frequently affected by wind-induced low-frequency noise" (p. 5), rejecting over half the blocks (55.2%/56.4%, p. 6).
  - "Owing to the UAV's size and the resulting rotor downwash, no valid measurements were obtained below the UAV" (p. 9).
  - "the BPF band of the UBADRON partly falls below the cut-off frequency of the anechoic chamber" — a large/slow rotor's fundamental tone can sit below even a purpose-built chamber's rated cutoff (p. 9).
  - Irregular, non-equiangular microphone geometry required a post-hoc angular-binning workaround rather than a true directivity sphere (pp. 5–6).
  - "A residual uncertainty in the exact temporal alignment remains" between LiDAR position and audio (p. 4).
  - Recirculation is never discussed or measured in this paper — absence, not a "ruled out" finding.

- **Relevance**: The wind-contamination protocol (FFT-bin dB threshold below a set frequency, rejecting mics directly under/near the rotor's downwash) is directly applicable to any mic on SoundVisualizer's vertical arc that sits close to the rotor's flow column; the BPF-below-chamber-cutoff caveat is a reminder to check the fundamental against the actual room cutoff, not just the wedge design value.

---

## Jawahar, H.K., Hanson, L., Akhter, M.Z., Azarpeyvand, M. (2025). "Porous ground treatments for propeller noise reduction in ground effect." Scientific Reports 15:2170. DOI: 10.1038/s41598-024-82876-9. — Jawahar_2025_SciRep_porous-ground-propeller-ground-effect

- **Bibliographic check**: Title, authors (Hasan Kamliya Jawahar, Liam Hanson, Md. Zishan Akhter, Mahdi Azarpeyvand), journal (Scientific Reports), article number (15:2170) and DOI (10.1038/s41598-024-82876-9) all print exactly as filed. Received 6 Sep 2024; Accepted 10 Dec 2024; header and footer both print "(2025) 15:2170" and the copyright line reads "© The Author(s) 2025." PDF metadata (`pdfinfo`) confirms CreationDate 11 Jan 2025. **The filename's "2025" is correct.** The DOI suffix's embedded "-024-" is Nature/Springer's DOI-minting-year convention (tied to manuscript processing), not the publication year, so EXTRACTS-downloaded.md's parenthetical "(file dated 2024; DOI …)" is misleading and should be dropped or reworded — no printed date on the article itself says 2024.

- **Claim audit**:
  - Facility "7.9 × 5.0 × 4.6 m including the acoustic walls (p. 3)" — OK.
  - "APC 10×5.5″ pusher propeller (R = 127 mm), 7000 RPM (BPF = 233.33 Hz)" — OK.
  - "axis 1.2 m above the chamber's perforated mesh platform" — OK.
  - "Ground plane: 1.7 × 1.5 m, 12 mm MDF plate at L/R = 0.75–4" — OK.
  - "bare or covered with 45PPI, 75PPI (12 mm) or 75PPI-T (24 mm) foam" — OK.
  - "23 G.R.A.S. 40PL mics at 1.75 m (≈13R), θ = 40° above to 150° below the plate" — OK.
  - "8 flush surface mics S1–S8 at 50 mm spacing" — OK.
  - "PSD with Hanning window, Δf = 2 Hz, 16 s at 2^16 Hz (pp. 3–4)" — OK.
  - "GE configuration exhibits a significant increase in TSSPL by approximately 4.0–8.0 dB for frequencies above 1000 Hz" at θ = 50°, L/R = 4, "absent at θ = 90°" (p. 9) — OK, page verified.
  - "solid ground plate amplifies OASPL by ≈3 dBA at shallow angles" at L/R = 1 (p. 6) — OK.
  - θ > 100° "sharply decreases … shielded by the ground plane" (p. 6) — OK.
  - "CT and CP rise exponentially for L/R ≤ 2; porous surfaces add up to 30%/15% over solid (p. 5)" — OK, but imprecise: the 30%/15% figure is specifically the 75PPI-vs-Solid comparison; 45PPI's own increment over the isolated baseline is only ~20%/11%, and "porous surfaces" (plural) slightly overgeneralizes.
  - "Extra mid-frequency harmonics (600–2500 Hz, m = 6–9)… broadband humps 3.8–13 kHz… peak >10 kHz is motor mechanical noise (pp. 7–8)" — OK, all three numbers verbatim and page-confirmed.
  - "Coherence between surface mics drops in IGE (chaotic flow) (p. 11)" — OK.
  - "75PPI-T reduces far-field sideline TSSPL by ~13 dB in 1.5–10 kHz at L/R = 0.75" — OK but imprecise: the text attributes the ~13 dB reduction to "the porous configuration" as a class at that test point, not exclusively 75PPI-T (75PPI-T is separately stated to give "the greatest reduction" overall).
  - "OASPL increment by ≈2 dBA at shallow angles" (reduction from porous treatments at L/R = 1.0) — OK.
  - "near-field reductions up to 26–36 dB low-frequency and 6–10 dB mid/high (pp. 9–11)" — OK; appears both in results (pp. 9–10) and restated in the Conclusion (p. 11).
  - "Propeller mounted 1.2 m above the mesh floor 'to prevent interference with the propeller's airflow' (p. 3)" — OK.
  - MATRIX-3W row 36 "Bare plate +4–8 dB above 1 kHz at 50°, absent at 90°; 75PPI-T −13 dB sideline" — OK (same minor 75PPI-T-vs-"porous configuration" imprecision noted above).
  - brief.html: "Jawahar et al. cut sideline levels ~13 dB in 1.5–10 kHz and the OASPL increment by ≈2 dBA **with 24 mm 75 PPI foam**" — **WRONG → the 24 mm foam is named "75PPI-T" in the paper, distinct from "75PPI" (which is only 12 mm thick)**; the brief conflates the two porosity labels. The ≈2 dBA OASPL figure is also stated generally for porous treatments at L/R = 1.0, not tied uniquely to the 24 mm variant in that sentence.
  - brief.html: "even at four radii clearance the bare plate adds 4–8 dB above 1 kHz at shallow angles, absent at 90°" — OK.
  - synthesis.html row 109 "Bare plate +4–8 dB above 1 kHz at 50°, absent at 90°; 75PPI-T −13 dB sideline" — OK (same nuance as matrix row).
  - synthesis.html line 188 "Jawahar's 24 mm foam removes ~13 dB only above 1.5 kHz" — **WRONG → should read "75PPI-T foam (24 mm) removes ~13 dB in the 1.5–10 kHz range"**; the naming error repeats, and "only above 1.5 kHz" drops the paper's explicit upper bound (10 kHz), implying an open-ended band the text doesn't claim.
  - synthesis.html line 214 (T4 "Strong" finding citing Jawahar among others) — OK, general non-numeric use, consistent with its findings.

- **Verified facts card**:
  - Facility: "The anechoic chamber has dimensions of 7.9 m in length, 5.0 m in width and 4.6 m in height, including the surrounding acoustic walls." (p. 3)
  - Reflection persists far from the plate: "At θ = 50°, the GE configuration exhibits a significant increase in TSSPL by approximately 4.0-8.0 dB for frequencies above 1000 Hz." (L/R = 4, p. 9)
  - Reflection is angle-gated: "this increase is absent at θ = 90°, where the sideline region does not experience reflections from the ground plane." (p. 9)
  - Shielded-zone cutoff: "beyond θ > 100°, the OASPL sharply decreases in the GP case as the microphones are shielded by the ground plane." (p. 6)
  - IGE OASPL bump: "The solid ground plate amplifies OASPL by ≈3 dBA at shallow angles, while porous treatments reduce this increment by ≈2 dBA" (p. 6)
  - Ground-induced spectral content: "additional mid-frequency harmonics (600 − 2500 Hz, m = 6 − 9), absent in the Isolated case." (p. 7)
  - Near-field low-frequency suppression: "up to 30 dB in low frequencies and 4.0-5.0 dB in high frequencies at the propeller tip region (S4)" (OGE, p. 9)
  - Coherence collapses close to the ground: "the coherence diminishes, particularly between the inner microphones (S1-S4)" entering IGE. (p. 11)
  - Aerodynamic vs acoustic separation: CT/CP "begin to increase exponentially as the propeller enters IGE (L/R ≤ 2)" (p. 5) — a thrust-scaling signature distinct from the angle-gated reflection signature above.
  - Motor floor: "A singular high-frequency peak (f > 10 kHz)… is attributed to mechanical noise originating from the motor." (p. 8)

- **Relevance**: SoundVisualizer has no ground-plane test, but this paper's diagnostic — a level rise present at shallow angles and unchanged with thrust is acoustic reflection, while a rise that scales with thrust and adds new harmonics is aerodynamic — is directly usable for spotting floor contamination in SoundVisualizer's own vertical mic arc at low elevation angles.

---

## Jenny 2011, BYU senior thesis (advisor B.E. Anderson) — Jenny_2011_BYU-thesis_ultrasonic-chamber-qualification

- **Bibliographic check**: Title (as printed, all-caps on cover/abstract): "ULTRASONIC ANECHOIC CHAMBER QUALIFICATION: ACCOUNTING FOR ATMOSPHERIC ABSORPTION AND TRANSDUCER DIRECTIVITY." Sole author Trevor Jenny; advisor Brian E. Anderson (not a co-author of the thesis). Venue: senior thesis submitted to the faculty of Brigham Young University, Dept. of Physics and Astronomy, in partial fulfillment of a Bachelor of Science, dated **April 2011**. No DOI, volume or journal pagination printed (the companion letter's Ref. 11 gives a now-informal URL, `physics.byu.edu/Thesis/view.aspx?id=263`). Filename is correct.

- **Claim audit**:
  - Chamber dims "3.57 × 2.88 × 2.59 m", wedges "Future Foam 70200YW13, 0.032 g/cm³", base "30.48 cm", alternately oriented (§II, p. 4) — OK.
  - Qualification "6.3 kHz–100 kHz," standard "stops at 20 kHz" — OK.
  - Sources "KEF Hypertweeter and Parasonics 40/58/75 kHz piezo transducers"; "G.R.A.S. 40BE ¼″ mic from 0.5 to 1.0 m in 5 cm steps along five corner traverses"; "swept sine below 50 kHz, random noise above" (Table 1, p. 7) — OK, all confirmed against Table 1.
  - "these estimates are clearly not accurate as the acoustic center cannot be located that far away from the physical surface of the transducer" (pp. 10–11) with r0 = 13.7/20.6 cm — OK, verbatim.
  - "The FRM only qualifies when absorption is accounted for." (p. 10) — OK, verbatim.
  - ka = 0.73 at 6.3 kHz, ka = 33.7 at 80 kHz; ISO deviation allowances ±1.5/2.0/2.5/5.0 dB — cited as "(§III.B, p. 12)" — **WRONG → these sentences are on p. 11**, not p. 12 (§III.B begins on p. 11; only the subsequent "22.5 dB / 10.6 dB" average-deviation sentence falls on p. 12). Minor page misattribution, numbers themselves correct.
  - "Average deviations from omnidirectionality are 22.5 dB (72.2 dB at most) without the beam blocker... 10.6 dB (38.2 dB at most)" (p. 12) — OK.
  - Bands ≥63 kHz "commonly yield levels that exceed the allowable ±1.5 dB range with the beam blocker in place" (p. 12) — OK.
  - "there appears to be evidence of interference from x = 70 cm and in the up and down swings in the data..." + 9.2 λ at 63 kHz (pp. 12–13) — OK, quote and page span both verified.
  - "measurements would need to be made every 1.03 mm for a frequency of 50 kHz" / "0.15 of a wavelength" (p. 6) — OK.
  - "The high directivity of the source likely does not illuminate the entire chamber and thereby can be considered to provide a pseudo qualification for an anechoic chamber." (§III, p. 8) — OK, verbatim, and confirmed **absent from** the JASA-EL letter (unique to the thesis).
  - Quotable: "When atmospheric absorption is not accounted for, the optimal reference method employs nonphysical estimates of the acoustic center..." (§IV, p. 15) — OK.
  - brief.html (line 131): "5 cm steps are 9.2 wavelengths apart" at 63 kHz — OK.
  - brief.html/synthesis.html (lines 110, 183): fitted r0 rounded to "14–21 cm for a tweeter" — imprecise rounding of 13.7/20.6 cm but not misleading; OK (rounded).
  - MATRIX-3W.md row 13 numbers (r0 13.7/20.6 cm, 22.5 dB, 9.2 λ) — OK (this is a merged thesis+letter row; see the JASA-EL section below for the companion-paper check).

- **Verified facts card**:
  - Standard gap: "the standard makes no attempt to address frequencies above 20 kHz" (§I, p. 1).
  - Air absorption is mandatory at ultrasonic distances: "The FRM only qualifies when absorption is accounted for." (p. 10).
  - Optimal-reference fitting can hide a real problem behind a fake source offset: "the acoustic center cannot be located that far away from the physical surface of the transducer" (pp. 10–11).
  - Highly directional sources risk under-illuminating the chamber, producing "a pseudo qualification for an anechoic chamber" (§III, p. 8).
  - A beam blocker roughly halves directivity deviation (22.5→10.6 dB average) but the chamber still fails ISO tolerance above 63 kHz with it in place (p. 12).
  - Coarse traverse spacing (7.3–9.2 λ at 50–63 kHz) can leave real interference undetected: "it is uncertain what degree of interference is present with the coarse spacing" (p. 12).
  - The standard's fixed ±1.5 dB/±5.0 dB directivity tolerances by band are quoted in full (p. 11).
  - Recommendation: prefer the fixed reference method over the optimal reference method at ultrasonic frequencies to avoid nonphysical acoustic-centre fits (§IV, p. 15).

- **Relevance**: Minimal — this is an ultrasonic (6.3–100 kHz) qualification study, far above SoundVisualizer's 20 Hz–24 kHz working band, but its core caution (a free-parameter curve fit can absorb a real reflection/interference problem into an implausible fitted offset, and coarse spatial sampling can hide interference) is a transferable methodological warning for any future free-field check of the SoundVisualizer rig.

---

## Jenny, T., Anderson, B.E. (2011). "Ultrasonic anechoic chamber qualification: Accounting for atmospheric absorption and transducer directivity." Journal of the Acoustical Society of America, Express Letters 130(2):EL69–EL75. DOI: 10.1121/1.3606461. — Jenny-Anderson_2011_JASA-EL_ultrasonic-chamber-qualification

- **Bibliographic check**: Title identical to the thesis (sentence case here): "Ultrasonic anechoic chamber qualification: Accounting for atmospheric absorption and transducer directivity." Authors: **Trevor Jenny; Brian E. Anderson** (now a co-author, unlike the thesis). Venue: Journal of the Acoustical Society of America, Express Letters, **130(2), EL69–EL75**, received 16 Apr 2011, accepted 3 Jun 2011, published online 22 Jul 2011, issue Aug 2011. DOI **10.1121/1.3606461**. Filename is correct. EXTRACTS-downloaded.md's Batch C entry and brief.html line 239 (DOI + pagination) both match this exactly — OK.
  - **Correction to the existing "Differences from the BYU thesis version" note** (end of the Batch C section): item (4) states the letter's conclusion "adds the explicit statement 'Even when absorption is accounted for, the optimal reference method yield nonphysical estimates for the acoustic center.'" — **WRONG**. That exact sentence (including the ungrammatical "method yield") is already present verbatim in the **thesis's own** Conclusion (p. 15, lines 643–646), so it is not something the letter adds; the two conclusions are essentially identical on this point. This is the most serious inaccuracy found in either paper's existing extracts.
  - Items (1)–(3) of that same "Differences" paragraph were independently re-verified and are correct: the thesis's "pseudo qualification" sentence is genuinely absent from the letter; the letter's turntable line is OCR-degraded to "2.5 rotations for 360" versus the thesis spelling out "degree" both times; the letter does replace the thesis's Table 1 with "specified in Ref. 11."

- **Claim audit**:
  - Chamber dims, wedge material/mass, "a base, that is, 30.48 cm2" (p. EL70) — OK.
  - Qualification "6.3 kHz to the 80 kHz third-octave band and up to 100 kHz" cited as "(p. EL71)" — **WRONG → this sentence is on pp. EL69–EL70** (it closes the Introduction, before the "2. Experiment setup" header); the ±1.5 dB tolerance sentence bundled with it is correctly on EL71. Minor page misattribution, not a numeric error.
  - "The FRM only qualifies when absorption is accounted for." (p. EL72) — OK.
  - r0 = 13.7 cm / 20.6 cm, "clearly not accurate as the acoustic center cannot be located that far away..." (pp. EL72–EL73) — OK, quote genuinely spans the page break around Fig. 2.
  - ka = 0.73/33.7 and the ±1.5/2.0/2.5/5.0 dB tolerance table cited as "(p. EL74)" — **WRONG → these are on p. EL73**; only the subsequent "22.5 dB (72.2 dB max) / 10.6 dB (38.2 dB max)" sentence is on EL74. Numbers themselves correct.
  - Bands ≥63 kHz exceed ±1.5 dB with the beam blocker; 50 kHz band SNR shortfall in a couple of bins (p. EL74) — OK.
  - "9.2 λ / 7.3 λ / 1.03 mm" and the "up and down swings" quote, cited "(pp. EL71, EL74)" — OK, correctly split across the two pages where each fact actually appears.
  - Broadband-averaging quote "suppresses interference, and therefore the deviation from the inverse square law" cited "(pp. EL69–EL70)" — OK, genuinely spans that page break.
  - "as long as this is understood when reporting data" (p. EL74) — OK.
  - MATRIX-3W.md row 13 (merged thesis+letter row): r0, 22.5 dB, 9.2 λ — OK for both papers.
  - brief.html line 239 (DOI, "130 EL69", bundled topic description) — OK.
  - synthesis.html line 110 (same MATRIX row rendered) — OK.

- **Verified facts card**:
  - Same chamber/wedge geometry as the thesis, confirmed independently in the letter's own text (p. EL70).
  - Standard silence above 20 kHz repeated verbatim from the thesis (p. EL69).
  - FRM is recommended as the safer method: "We propose that the fixed reference method be used for ultrasonic frequencies to avoid this issue." (Conclusions, p. EL74).
  - ORM's acoustic-centre problem persists even with absorption corrected: "Even when absorption is accounted for, the optimal reference method yield nonphysical estimates for the acoustic center." (p. EL74) — identical to the thesis, not an addition (see correction above).
  - Directivity numbers (ka 0.73→33.7; 22.5→10.6 dB average deviation with beam blocker) reproduced unchanged from the thesis (pp. EL73–EL74).
  - The letter explicitly defers experimental detail to the thesis: "The specifics of the measurements... are specified in Ref. 11." (p. EL70) — confirms it is a condensed companion publication, not an independent dataset.
  - Coarse-traverse interference caveat repeated: "it is uncertain what degree of interference is present with the coarse spacing" (p. EL74).
  - Acknowledgments confirm Los Alamos National Laboratory funding, same as the thesis (p. EL74).

- **Relevance**: Same as the thesis — negligible direct overlap with SoundVisualizer's audio-band drone measurements, but the letter reinforces (as an independently peer-reviewed, condensed version of the same result) the caution against trusting a free-parameter inverse-square fit without checking that the fitted offset is physically plausible.

---

## Kim, Y.-H., Oh, G.-I., Ku, B.-S., Lee, J.-W., Lee, S.-S., Kim, S.-H. (2022). "Noise Characteristics of Drones (UAV) According to Testing Environmental Conditions." Proc. 28th International Congress on Sound and Vibration (ICSV28), Singapore, 24–28 July 2022. — Kim_2022_ICSV28_drone-noise-vs-testing-environment

- **Bibliographic check**: Title (printed exactly, as displayed): "NOISE CHARACTERISTICS OF DRONES (UAV) ACCORDING TO TESTING ENVIRONMENTAL CONDITIONS." Authors: Yong-Hee Kim, Gyu-In Oh, Bon-Soo Ku, Jang-Won Lee (Y'sU Youngsan University); Seung-Soo Lee (Korea Conformity Laboratories); Sang-Ho Kim (Konkuk University). Venue printed on p. 1 and in the footer of every page: "The 28th International Congress on Sound and Vibration (ICSV28), 24-28 July 2022," Singapore (per the p. 1 banner graphic: "ICSV28 SINGAPORE 24–28 JULY"). No DOI, no ISBN, no volume, no serial page range — only internal pagination 1–8. Filename `Kim_2022_ICSV28_drone-noise-vs-testing-environment` is correct on every count.

- **Claim audit**:
  - "box-type semi-anechoic room... Daejeon, South Korea... 8.2 m in length, 7.0 m in width and 4 m in height from the metallic ground surfaces. Cut-off frequency of the room was 63 Hz": OK, exact (p. 2).
  - Background "< 15 dB(A)" indoor: OK (paper says "less than 15 dB(A)," p. 2).
  - Outdoor field "101 m in length and 62 m in width," background "~50 dB(A)": OK, exact (p. 2).
  - Wedge depth/qualification standard "not stated": OK.
  - EU 2019/945 (ISO 3744) → Directive 2000/14/EC six-mic layout, radius 3 m indoor / 5 m outdoor, hover 0.5 m: OK, all exact (pp. 2–3).
  - "physical interference between some unstably hovering drones and the tenth microphone": OK, exact quote and page (p. 2).
  - "M5/M6 at 2.4 m... higher sound levels by about 3 dB on average than other four microphones at 1.5 m height. This can be seen as the effect of the propeller wind acting in a downward direction": OK, exact quote and page (p. 4).
  - Four-mic 0.5 m simplified LWA "4.6 to 7.4 dB" lower than the Directive method, "the measurement height rather than... the number of measurement points": OK, exact (p. 4).
  - Octocopter ~1 dB rise and Phantom 4 Pro ~3.5 dB rise (0.5→5 m, 1.5 m mic height); quadcopter only "10 dB difference to background": OK, all exact (pp. 6–7).
  - Low-noise propeller "4.2 dB" reduction, safeguard "±0.5–2.7 dB" inconsistent effect: OK — measured values are 0.9 dB reduction, 0.5 dB amplification, and 2.7 dB amplification (Mavic Air); the extract's "0.5–2.7 dB" range correctly spans them.
  - "LWA 82.6 dB (hover 0.5 m, semi-anechoic) vs 82.5 dB (hover 1 m, outdoor)" and "it may be possible to measure drone noise as much as a laboratory even outdoors...": OK, exact (p. 7).
  - MATRIX-3W row 38 "Upper mics +3 dB from downwash; L_WA 82.6 (lab) vs 82.5 dB (outdoor)": OK.
  - **brief.html line 122 (shared symptom row with Alkmim/Hochbaum) — MISCHARACTERIZED for Kim.** The row's symptom is "Excess below ~50–100 Hz only at microphones under the rotor," cause "Flow pseudo-sound from downwash over the diaphragm... 55% of blocks rejected at TU Berlin," citing "Kim 2022 ●" alongside Alkmim/Hochbaum. Kim's paper supports neither half of this for Kim specifically: (a) Kim reports only a broadband/A-weighted sound-power gap ("~3 dB on average"), with **no frequency-band breakdown at all**, let alone one confined to 50–100 Hz; (b) Kim's M5/M6 mics are at 1.5–2.4 m height above a drone hovering at 0.5 m — i.e. **above** the rotor plane, not "under the rotor" as the row states (that phrase correctly describes Alkmim's and Hochbaum's geometries, not Kim's). The brief is compressing three papers into one symptom line and loses Kim's actual (different) finding in the process.

- **Verified facts card**:
  - Chamber: "8.2 m in length, 7.0 m in width and 4 m in height from the metallic ground surfaces," cutoff "63 Hz," reflecting (metallic) floor (p. 2).
  - Indoor/outdoor background contrast: "less than 15 dB(A)" vs "about 50 dB(A) due to nearby road traffic sources" (p. 2).
  - ISO 3744's ten-mic hemisphere was abandoned for safety: "possibilities of physical interference between some unstably hovering drones and the tenth microphone on the top of the measuring hemisphere" (p. 2).
  - Mic-height effect: "two microphones of M5 and M6 at 2.4 m height... shows higher sound levels by about 3 dB on average than other four microphones at 1.5 m height... the effect of the propeller wind acting in a downward direction" (p. 4).
  - Lower measurement height, not fewer mics, drove most of the gap to the simplified 4-point method: "This difference seems to be because of the measurement height rather than the effect of the number of measurement points" (p. 4).
  - Indoor 0.5 m and outdoor 1 m sound power for the same Phantom 4 Pro nearly matched: "82.6 dB and 82.5 dB, respectively" (p. 7).
  - Noise scaled with the log of drone weight regardless of battery presence, with two named outliers (Mavic 2 Enterprise/Pro) below trend (p. 6).
  - No mention anywhere of recirculation, standing waves, or chamber qualification/traverse data — the paper treats the room only as a fixed backdrop for a sound-power protocol.

- **Relevance**: Limited. Kim measures whole-drone sound power over a reflecting floor with a hemisphere protocol, not the directivity of a single stand-mounted rotor on a vertical arc; the one transferable point is that microphones positioned in a hovering drone's downwash column read several dB high on an overall/power basis, a caution for arc-mic placement near flow.

---

## Ma, X., Chen, K., Wang, L., Liu, Y., Ding, S. (2022). "Active control of low frequency sound absorption of large sized micro-perforated panel absorber by using point source." Applied Acoustics 185:108424. DOI: 10.1016/j.apacoust.2021.108424. — Ma_2022_ApplAcoust_active-control-large-MPP-absorber

- **Bibliographic check**: Title, all five authors + affiliations, journal, volume/article number (185, 108424) and DOI (`10.1016/j.apacoust.2021.108424`) confirmed exactly as printed on the PDF's masthead and footer of every page. This **resolves the DOI-confusion note** in EXTRACTS-downloaded.md's original abstract-only entry ("the DOI …108383 supplied earlier resolves to a different paper"): the correct DOI is unambiguously `…108424`, matching Batch C's corrected entry and the reference ledgers in both HTML docs (which already print `108424` correctly). No residual error. Filename `Ma_2022_ApplAcoust_active-control-large-MPP-absorber` is correct.

- **Claim audit**:
  - MPPA parameters: 0.4 mm holes, 0.5 mm plate, 1% porosity, 0.08 m cavity (Table 1, p. 4) — OK, verbatim.
  - Case 1 panel 0.6×0.8 m, Case 2 1.0×1.2 m (pp. 2–4) — OK, verbatim on p. 4.
  - Table 3 modal frequencies: Case 1 (0,1,0) 215, (1,0,0) 287, (1,1,0) 358, (0,2,0) 430 Hz; Case 2 143/172/224/287 Hz (p. 7) — OK, verbatim match to printed Table 3.
  - Corner source S1 cuts off at (0,1,0); mid-side S2 at (1,0,0); centre S4 at (0,2,0); "the highest cutoff frequency of the active MPPA is the resonant frequency of the (0,2,0) cavity mode" (p. 6) — OK, verbatim.
  - "the forward sound intensity will be cancelled by the negative sound intensity and the surface net sound intensity will be very small" (p. 5) — OK, verbatim.
  - "The high order cavity mode (except for (0,0,0) mode) has no contribution to sound absorption improvement due to the symmetrical property of their mode shape" (abstract, p. 1) — OK, verbatim.
  - "The larger the size of active MPPA is, the narrower the controllable frequency band is." (p. 6) — OK, verbatim.
  - Field uniformity breaks down at 400 Hz, wavelength "about 0.86 m … close to the size of the cavity" (p. 5) — OK, verbatim.
  - Duct cut-off "is only 215 Hz"; centring avoids (0,1),(1,0),(1,1) modes, extends plane-wave validity to 430 Hz (p. 10) — OK, verbatim.
  - Below 80 Hz, control loudspeaker's limited response degrades performance (p. 12) — OK, verbatim.
  - Results "a little undulant" for S1/S3, attributed to the real loudspeaker not being a true point source (p. 11) — OK, verbatim.
  - Error sensing: pressure-release / impedance-matching, IM "slightly better," sensing point away from centre, "significantly weakened when the sensing point is close to the central area" (p. 9) — OK, verbatim.
  - "there will be no control effect or even the sound absorption coefficient will be reduced" above cutoff — OK, verbatim.
  - Absorption "highly improved and nearly close to 1 in the low frequency range," upper limit "up to 400 Hz" for Case 1 (p. 4) — OK, verbatim.
  - MATRIX row 18 / synthesis.html line 113 (theme T8=S; "Absorption ≈ 1 up to ~400 Hz; limit = first excitable cavity mode") — OK, fully consistent.
  - brief.html lines 198–199 paraphrase (215–430 Hz range, "larger…narrower the controllable band," antisymmetric modes/nodal-line placement) — OK.

- **Verified facts card**:
  - This is a bounded-cavity active-absorption method paper, not a chamber-qualification study: "This paper presents a theoretical investigation on actively controlling the low frequency sound absorption of large-sized micro-perforated panel absorber (MPPA) by using point source placed in the cavity" (Abstract).
  - Absorption improvement is capped by the first cavity mode the point source can excite from its position: "there is a cutoff frequency for each location of the point source, after which the control effect hardly works" (p. 4).
  - Larger absorbers have a lower usable band: "The larger the size of active MPPA is, the narrower the controllable frequency band is." (p. 6).
  - Antisymmetric modes cancel net control authority: "the forward sound intensity will be cancelled by the negative sound intensity" (p. 5).
  - Placing the source on a mode's nodal line prevents exciting it, raising the cutoff (best case, centred source, up to the (0,2,0) mode) (pp. 4–6).
  - Field non-uniformity re-emerges once wavelength approaches cavity size (~0.86 m at 400 Hz) (p. 5).
  - Sensing-point placement matters as much as source placement: control "significantly weakened when the sensing point is close to the central area" (p. 9).
  - Experimentally, absorption "highly improved and close to 1 after control" up to the theoretical cutoff for each source position (p. 10, Conclusions).

- **Relevance**: None to SoundVisualizer directly — this is an active low-frequency absorption technique for a bounded MPP cavity/duct, not a chamber-qualification, rotor-testing, or reflection-diagnosis study; it is cited in the brief/synthesis only as one data point on how far active absorption schemes can push a low-frequency limit in principle.

---

## Ma, Z., Wu, H., Jiang, H., Zhong, S., Zhang, X. (2022). "Acoustic Measurement of Multi-Rotor Drones in Anechoic and Hemi-Anechoic Chambers." Quiet Drones — Second International e-Symposium on UAV/UAS Noise, 27–30 June 2022. — Ma_2022_QuietDrones_multirotor-anechoic-vs-hemi-anechoic

- **Bibliographic check**: Title (printed exactly): "Acoustic measurement of multi-rotor drones in anechoic and hemi-anechoic chambers." Authors: Zhida Ma, Han Wu, Hanbo Jiang, Siyang Zhong, Xin Zhang (Dept. of Mechanical and Aerospace Engineering, HKUST; Zhong also HKUST Institute for Advanced Study; Zhang also HKUST-Shenzhen Research Institute). Venue printed on p. 1: "QUIET DRONES / Second International e-Symposium on UAV/UAS Noise / 27th to 30th June 2022," co-organized by INCE Europe and CidB (Centre d'information sur le Bruit). No DOI, no ISBN, no volume — only internal "Page | N" pagination, 1–13. Filename `Ma_2022_QuietDrones_multirotor-anechoic-vs-hemi-anechoic` is correct on every count.

- **Claim audit**:
  - Chamber "8.1 m (L) × 6 m (W) × 5.1 m (H)," cutoff "100 Hz" full anechoic, hemi-anechoic height "5.7 m": OK, exact (p. 2).
  - Qualification standard "not stated": OK.
  - "15 GRAS 46BE 1/4 in. mics (9 vertical near a corner, 6 horizontal 0.12 m above bottom wedges, 0.5 m spacing), windscreens": OK, exact (p. 3).
  - "20 s at 50 kHz, Welch Δf = 5 Hz": OK, exact (p. 3).
  - "deviations can reach as large as 3 dB," "attributed to the presence of the reflective surface," ~0.5 dB repeatability: OK, exact, p. 8.
  - Mics "#9, #10," "difference in the measured SPL can be as significant as 10 dB" at BPF, "little difference" in full anechoic: OK, exact, p. 8.
  - "L = d + D," L = 0.59 m, "R ≥ 5L," decay follows 1/R over "3.4L ~ 7.4L": OK, all exact, pp. 3–4 and 8.
  - EU 2019/945 criticism, "can directly impinge the reflecting surface, resulting in an aerodynamic ground effect," no far-field requirement: OK, exact quotes; page citation "(p. 2)" is plausible but not fully verifiable (the title page carries no printed footer number), not flagged as wrong.
  - Cruise fly-over, "a prominent pressure fluctuation at low frequencies due to rotor wake": OK, exact, p. 12.
  - "The results illustrate the need to use a full anechoic facility to measure the drone noise spectra": OK, exact, p. 8.
  - Position drift "0.05 m (0.085L) horizontally and 0.026 m (0.044L) vertically": OK, exact (p. 5).
  - **Minor conflation in the existing "Solutions/mitigations" bullet**: it lists "five repeats" and, in the same breath, "rotate the drone heading in 15° steps... swap rotors diagonally between repeats" as if one scheme. These are actually two separate experiments: the hemi-vs-full-anechoic comparison used **5** repeats per hover point (p. 4), while the heading/directivity test with 15° steps and diagonal rotor-swapping used **4** repeats (p. 5) and scaled data to "3.2 m" (p. 8, §3.4). Both numbers (5 and 4) are individually correct in the source, but bundling them under one bullet risks implying the swap-rotor protocol used 5 reps rather than 4.
  - Conclusion quote "could considerably degrade the tonal noise assessment accuracy": OK, exact, p. 12.
  - MATRIX-3W row 29: all values ("10 dB," "3 dB," quote) OK as above.
  - synthesis.html line 114: OK, matches matrix row 29.
  - brief.html line 112: mostly OK, but "Two adjacent microphones **at the same distance and angle**" slightly overstates the paper's own wording — the paper says the two mics' "observer distance and equivalent angle are **close**," not identical. Minor imprecision, not a numeric error.

- **Verified facts card**:
  - Chamber: "wedge-to-wedge dimension of 8.1 m (L) × 6 m (W) × 5.1 m (H) and a cut-off frequency of 100 Hz in the full anechoic configuration. With the bottom wedges removed, the chamber is in the hemi-anechoic configuration and the height is 5.7 m" (p. 2).
  - Reflecting floor directly costs directivity accuracy: "the discrepancy in the hemi-anechoic results is attributed to the presence of the reflective surface" (p. 8).
  - Two adjacent near-floor mics at similar range/angle diverge sharply only in hemi-anechoic mode: "the difference in the measured SPL can be as significant as 10 dB" at BPF (p. 8).
  - Full-anechoic decay tracks the inverse-square law cleanly over "3.4L ~ 7.4L," where L = d + D = 0.59 m for this drone (pp. 4, 8).
  - The EU 2019/945 standard test (0.5 m hover over a reflecting plane) is criticized because the wake "can directly impinge the reflecting surface, resulting in an aerodynamic ground effect" (p. 2).
  - Repeatability was tight in both configurations (~0.5 dB) even though hemi-anechoic absolute levels departed from theory by up to 3 dB — repeatability alone does not certify a chamber (p. 8).
  - Rotor wake produces a low-frequency pressure spike at a microphone during a fly-past: "a prominent pressure fluctuation at low frequencies due to rotor wake" (p. 12).
  - Bottom line: "using a hemi-anechoic chamber could considerably degrade the tonal noise assessment accuracy" (p. 12, Conclusions).

- **Relevance**: Highly relevant — this is a controlled, same-chamber, same-rotor A/B test proving that a hard floor alone (not distance, not rotor, not repeatability) produces up to 10 dB of tonal error and 3 dB of decay-law departure versus a fully anechoic setup, a direct cautionary analog for any floor or fixture reflection near SoundVisualizer's stand-mounted rotor and vertical mic arc.

---

## Ma, Z., Zhou, P., Zhang, X., Zhong, S. (2024). "Experimental Assessment of the Flow Recirculation Effect on the Noise Measurement of a Free-Flying Multi-rotor UAS in a Closed Anechoic Chamber." Acoustics Australia 52:313–322. DOI: 10.1007/s40857-024-00327-x. — Ma_2024_AcoustAust_recirculation-free-flying-UAS-anechoic

- **Bibliographic check**: Title, all four authors, journal name, volume/page range (52:313–322) and DOI all printed exactly as above on the PDF's first page. Received 5 Feb 2024 / Accepted 20 May 2024 / Published online 12 June 2024. Filename `Ma_2024_AcoustAust_recirculation-free-flying-UAS-anechoic` is correct.

- **Claim audit**:
  - Facility "wedge tip-to-tip dimensions of 8.1 m (L) × 6 m (W) × 5.1 m (H) and a cut-off frequency of 100 Hz" (p. 314) — OK, verbatim.
  - "Qualification standard: not stated" — OK.
  - Five 1/4″ GRAS 46BE mics, vertical plane, windscreens; DJI Phantom 4 Pro, four 240 mm rotors, 1.4 kg; hover 2.2–3.2 m; 60 s @ 50 kHz — OK, all verbatim/matches Table 1 and §2.1.
  - "recirculation forms around 30 s after the UAS's take-off, manifested as prominent fluctuations in blade passage frequency and its harmonics" (abstract) — OK, verbatim.
  - "the precise determination of this transition moment is not feasible as the intensity of the tonal fluctuations increases gradually" (p. 316) — OK, verbatim.
  - Instantaneous OASPL (100–20,000 Hz) "does not show a significant deviation … but presents slight higher fluctuation values up to 2 dB" (p. 316) — OK, verbatim.
  - Post-recirculation "tonal spikes become broader, and two or more separated spikes can be present at high-order BPF harmonics" (p. 317) — OK, verbatim.
  - Table 2: tonal SPL range −0.89…+0.66 dB, broadband OASPL +1.08…+2.03 dB (largest mic #5), SE +0.068…0.083 (p. 318) — OK, all four figures verified against the printed Table 2.
  - "chamber … significantly larger, approximately 8 and 12 times the volume of the ones employed by Stephenson et al. [7] and Bu et al. [11]" (p. 317) — OK, verbatim.
  - Test protocol Steps 1–5 incl. "Wait for at least 5 min to ensure an environment with quiescent air before the next test" (pp. 314–315) — OK, verbatim.
  - SE band 100–2000 Hz "as a reference to detect the formation of the recirculation" (p. 316) — OK, verbatim.
  - Broadband via moving-median + moving-minimum + Gaussian smoothing; tonal SPL via ≥−20 dB-re-peak band integration (p. 315) — OK.
  - Four repeats, heading rotated front/left/back/right — OK (pp. 315–316).
  - "does not significantly change the total acoustic energy but increases the uncertainties in the spectral distribution" (abstract) — OK, verbatim.
  - "the instantaneous OASPL value cannot distinguish the transition into the post-recirculation flow regime" (p. 316) — OK, verbatim.
  - Summary quote "the recirculation has a negligible effect on the tonal SPLs at the first four BPF harmonics but slightly (∼2 dB) enhances the broadband OASPL out of the rotor plane" (p. 321) — OK, verbatim.
  - "a characterization of the flow recirculation effect before conducting any accurate acoustic assessments is important…" (p. 321) — OK, verbatim.
  - Cross-paper note in EXTRACTS-local.md "Free-flying multirotor in a large chamber: OASPL unchanged, tones broaden/split, broadband +1–2 dB (Ma 2024)" — OK, consistent with Table 2 range (1.08–2.03 dB).
  - MATRIX row 28 and synthesis.html lines 115/181 (onset ~30 s; OASPL unchanged; "negligible effect on tonal SPLs"; room 8–12× larger) — OK throughout, all figures and quotes verified.

- **Verified facts card**:
  - Chamber cut-off 100 Hz, wedge tip-to-tip 8.1×6×5.1 m: "cut-off frequency of 100 Hz" (§2.1, p. 314).
  - Recirculation onset for a free-flying multirotor is much later than for a stand-mounted rotor in a small chamber: "forms around 30 s after the UAS's take-off" (Abstract).
  - OASPL is not a reliable recirculation-onset indicator for a free-flying vehicle: "the instantaneous OASPL value cannot distinguish the transition into the post-recirculation flow regime" (p. 316).
  - Spectral entropy (100–2000 Hz) is proposed as the onset detector instead: SE "increases by about 0.1 (17%)" at the transition (p. 316).
  - Broadband noise rises modestly out of plane, tones do not: "negligible effect on the tonal SPLs at the first four BPF harmonics but slightly (∼2 dB) enhances the broadband OASPL out of the rotor plane" (p. 321).
  - Broadband increment grows with proximity to the ceiling: higher hover height → "recirculated flow is expected to be less uniform and non-axial to the rotors" (pp. 318–319).
  - Broadband increment shrinks with vehicle inertia: heavier gross mass "adds inertia … making it less vulnerable to the disturbances" (p. 320).
  - Quiescent-air settle time used between runs: "Wait for at least 5 min to ensure an environment with quiescent air before the next test" (p. 315).
  - Authors attribute their much smaller effect (vs. Stephenson/Weitsman/Nardari on stand-mounted rotors) partly to chamber volume: "approximately 8 and 12 times the volume of the ones employed by Stephenson et al. … and Bu et al." (p. 317).

- **Relevance**: Directly on-topic for recirculation risk during SoundVisualizer captures, but the mechanism/detector (spectral entropy, tone broadening) is calibrated for a free-flying multirotor in a chamber roughly 8–12× larger than the SHAC/Weitsman rig; for our stand-mounted single rotor the isolated-rotor literature (Stephenson/Weitsman/Nardari) is the closer analogue, and this paper mainly serves as the contrasting case explaining why free-flight and stand-mounted recirculation signatures differ.

---

## Merino-Martínez, R., Rubio Carpio, A., Lima Pereira, L.T., van Herk, S., Avallone, F., Ragni, D., Kotsonis, M. (2020). "Aeroacoustic design and characterization of the 3D-printed, open-jet, anechoic wind tunnel of Delft University of Technology." Applied Acoustics 170, Article 107504. DOI: 10.1016/j.apacoust.2020.107504. — Merino-Martinez_2020_ApplAcoust_TU-Delft-anechoic-wind-tunnel

- **Bibliographic check**: Title, all seven authors, journal, volume/article (170 (2020) 107504) and DOI print exactly as filed on the cover page, TU Delft repository page, and the article's own header/footer lines. Received 5 Feb 2020; Accepted 19 Jun 2020. PDF metadata confirms CreationDate 13 Jul 2020. **Filename is correct.**

- **Claim audit**:
  - "anechoic plenum floor ≈ 6.4 × 6.4 m, height 3.2 m (§2, p. 2)" — OK, verbatim: "The floor of the anechoic plenum is approximately a square of 6.4 m × 6.4 m and the height of the room is 3.2 m." Correctly distinguished from the separate settling-chamber room (also ≈6.4 m square but 5 m tall) — no conflation in the extract.
  - "total wedge height 0.49 m, designed on the λ/4 criterion for free-field 'above approximately 173.5 Hz' (p. 4)" — OK, verbatim match.
  - "floor foam under a 10 mm metal grid" — OK.
  - "Five interchangeable nozzles (Table 1, p. 4)" — OK, dimensions match Table 1 exactly.
  - "64-mic G.R.A.S. 40PH array on perforated steel plates (51% open area)" — OK.
  - "plate borders covered with foam" — OK.
  - "tone at 890 Hz at 10 m/s protruding ~8 dB above broadband, located… 'near the collector and the fan room'" (p. 9) — OK.
  - "smaller peak at 325 Hz at higher velocities" (p. 9) — OK.
  - "63 Hz hump probably mains hum" (p. 9) — OK, verbatim "most likely due to electric noise (also known as mains hum)."
  - "Electronic-noise spectral peaks at 150, 250,…, 4450 Hz and 16 kHz present even at 0 m/s (p. 8)" — OK; the 150–4450 Hz sentence is on p. 7 and the "16 kHz" continuation/conclusion is on p. 8, so the citation is a defensible range, not an error.
  - "A-weighting removes up to 30 dB, 'indicating the strong low-frequency noise content' (p. 10)" — OK, verbatim.
  - "Velocity exponent k = 6.2–6.9 (Table 3), below the ideal 8 (p. 10)" — OK, verbatim "values between 6.2 and 6.9"; Table 3's five values (6.89/6.23/6.28/6.57/6.39) confirm the range.
  - "Reverberation from the settling chamber through the open nozzle (T60 = 0.22 s measured with nozzle open; §5.3, p. 12)" — OK, verbatim.
  - "Array kept 1 ≤ h ≤ 1.5 m from the jet axis 'to avoid contact with the shear layer' (p. 5)" — OK, verbatim.
  - "Recommendation: cover the nozzle to minimize reverberation from the settling chamber (p. 12)" — OK, verbatim.
  - "Inverse-square test: bands ≥250 Hz meet ISO 3745…125/160/200 Hz only acceptable to r = 1.5 m (§5.2, p. 12)" — OK, verbatim.
  - "PSF check at 2 and 4 kHz…'no physical sound source is observed in the dynamic range selected (18 dB)' (p. 13)" — OK, verbatim.
  - "SNR ≥ 10 dB desired (p. 9)" — OK, verbatim.
  - "Conclusion quotes 'cutoff frequency of 200 Hz' (§6, p. 14)" — OK, verbatim. This is a genuine **internal inconsistency in the source paper itself** (design value 173.5 Hz vs. conclusion's 200 Hz), correctly flagged by the extract rather than an extract error.
  - brief.html "Standing wave of the open-jet column (TU Delft: 168.8 Hz and 125 Hz for two nozzles)" — OK, verbatim numbers.
  - brief.html "1–1.5 m off the jet axis to stay out of the shear layer" — OK.
  - MATRIX-3W row 19 / synthesis.html row 116 "125–200 Hz bands OK only to 1.5 m; jet-column standing wave 125–169 Hz independent of speed" — OK (168.8 Hz rounds sensibly to "169").
  - synthesis.html line 213 "Expect the room's real limit 20–30% above the wedge cut-off even in a well-built room… (T2; Jiang, Schneider, Haasjes, Merino-Martínez)" — **imprecise for this paper specifically**: Merino-Martínez's own design-to-observed gap is 173.5→200 Hz ≈ +15%, below the 20–30% range the sentence implies; the range is defensible only as a cross-source aggregate, not as this paper's individual number. A soft overstatement, not an outright fabrication.

- **Verified facts card**:
  - Anechoic plenum: "The floor of the anechoic plenum is approximately a square of 6.4 m × 6.4 m and the height of the room is 3.2 m." (p. 2)
  - Wedge design vs. reality gap: designed "for free-field propagation of sound for frequencies above approximately 173.5 Hz" (p. 4) but the Conclusion states "a cutoff frequency of 200 Hz" (p. 14) — an unremarked ~15% gap between design and stated operating limit.
  - Standing wave, not source, signature: "the peaks do not change in frequency with the mean flow velocity V, and only their magnitude is increased. This is attributed to the standing wave created by the jet column." (p. 8)
  - Low-band inverse-square failure: "the three next one-third-octave bands below 250 Hz (125 Hz, 160 Hz and 200 Hz) only show acceptable values up to r = 1.5 m." (p. 12)
  - Settling-chamber reverberation must be closed off for pure acoustics: "it is recommended to cover the nozzle to minimize the reverberation originating from the settling chamber" (p. 12); measured T60 = 0.22 s with nozzle open.
  - Mic placement rule against shear-layer contact: "For most experiments, 1 m ≤ h ≤ 1.5 m to avoid contact with the shear layer." (p. 5)
  - PSF confirms no chamber reflection artifact in the array's dynamic range: "no physical sound source is observed in the dynamic range selected (18 dB)" (p. 13)
  - Electronic-noise floor identifiable by its presence at zero flow: peaks "measured at 150, 250, 350, …, 4450 Hz independently of nozzle type or freestream velocity" and also "present in data measured at 0 m/s" (pp. 7–8)

- **Relevance**: This is an open-jet flow-tunnel paper (shear-layer siting, jet-column standing waves), so most of its detail doesn't transfer to SoundVisualizer's static, no-flow chamber. The one directly useful lesson is generic: the paper's own 173.5 Hz-designed/200 Hz-operating gap is a concrete illustration that a wedge-based cutoff estimate can understate a room's real low-frequency limit, reinforcing the same caution SoundVisualizer should apply to its own chamber.

---

## Singh, K.S., Garg, M., Narayanan, S. (2020). "Estimation of the lower cut-off frequency of an anechoic chamber: An empirical approach." International Journal of Aeroacoustics 19(1–2):57–72. DOI: 10.1177/1475472X20905070. — Singh_2020_IJAeroacoustics_lower-cutoff-frequency-empirical

- **Bibliographic check**: Title, authors, journal, volume/issue/pages and DOI all confirmed exactly as printed. Received 30 Oct 2019 / accepted 25 Nov 2019. Filename `Singh_2020_IJAeroacoustics_lower-cutoff-frequency-empirical` is correct.

- **Claim audit**:
  - Facility: external 2.75×2.40×2.98 m, working space 2.6×1.7×2.20 m tip-to-tip (p. 61) — OK, verbatim.
  - ~300 PU-foam wedges, 32 FR foam, 30±1 kg/m³, block 600×600×300 mm, wedge 275 mm on 25 mm base (Table 1, pp. 60–61) — OK, all values verbatim.
  - Cut-off "found to be 315 Hz within 0.5 dB" by inverse-square-law traverses per ISO 3745:2012 — OK, verbatim (abstract, pp. 58, 66).
  - GRAS 40PH ¼″ mic, 50 mV/Pa, NI cDAQ 9174 + NI 9222, 10 s @ 50 kHz, 1024-pt Hanning FFT averaged (p. 61) — OK, verbatim.
  - Source "smaller than 0.005 times the chamber size … generates unidirectional sound" (p. 62) — OK, verbatim exactly including the paper's own (likely erroneous) word "unidirectional" — correctly flagged in the extract as printed-but-odd, not silently corrected to "omnidirectional."
  - Signals: 500 Hz and 10 kHz sines + white noise, "signal-to-noise ratio – 0.05" (Tables 2–3) — OK, verbatim (odd SNR figure faithfully reproduced, not corrected).
  - Mic positions 20/40/80/160 cm along paths OA, OB — OK.
  - Empirical Eq. 2 (Blanco semi-anechoic): `a + 2a + λ/4 + lw = d`; Eq. 3 (fully anechoic): `a + 4a + λ/2 + 2lw = d` — OK, verbatim.
  - Proposed Eq. 4: `a + 2λ + λ/4 + lw = d`; Eq. 5: `f_chamber = 2.25c/(d − lw − a)`; Eq. 6 (a-neglected): `f_chamber = 2.25c/(d − lw)` — OK, verbatim, correct equation numbers.
  - Table 4: Eq. 1 → 285 Hz (10.52%); Eq. 3 → 92 Hz (242%); Eq. 4 → 320 Hz (1.60%); Eq. 5 → 312 Hz (0.95%); measured 315 Hz (p. 68) — OK, all five values verified verbatim.
  - "Eq. 4 and Eq. 5 are algebraically identical, so why they give 320 vs 312 Hz is unclear in text" — OK; confirmed the paper's Fig. 8/9 vary the source-size term `a` without stating which single value of `a` was used to generate the Table 4 row for each equation, so this is genuinely unresolved in the text, not an extract error.
  - d = 2.77 m, lw = 0.3 m per Fig. 9 caption (p. 69) — OK, verbatim.
  - **"No '±' appears in the paper; the earlier abstract-only entry's '±3%' was an editorial addition."** — OK, confirmed: abstract reads "compares well within 3%" and Conclusions read "within 3%," neither carries a "±" sign. The same superseded abstract-only entry also silently added an unstated "±" to the *0.5 dB* figure ("315 Hz within ±0.5 dB") — the paper's own wording is "within 0.5 dB," also with no "±." This second spurious "±" was not explicitly flagged by the Batch C retraction, though it is moot since Batch C's own entry (and this audit) always quotes "within 0.5 dB" correctly without "±".
  - Table 2 (500 Hz+noise) slopes: 0.29/0.12 dB at 100 Hz, 3.02/3.65 dB at 200 Hz, 5.67/6.17 dB at 315 Hz (p. 67) — OK, verbatim.
  - Table 3 (10 kHz+noise) slopes: 0.01/0.30 dB at 100 Hz, 2.98/3.63 dB at 200 Hz, 5.44/6.23 dB at 315 Hz (p. 68) — OK, verbatim.
  - "Above cut-off the slopes scatter around 6 dB: 5.23–6.35 dB at 630–1000 Hz, 6.74–6.77 dB at 5 kHz, 5.34–5.86 dB at 10 kHz, and 7.30–7.62 dB at 15 kHz (Tables 2–3)" — **WRONG → the 630–1000 Hz low end should read 5.21 dB, not 5.23 dB** (Table 3, 1000 Hz, Corner 2 = 5.21; Table 2's minimum in that range is 5.23, but the sentence purports to combine both tables). Every other bound in this sentence (6.35 high end; 6.74–6.77 at 5 kHz; 5.34–5.86 at 10 kHz; 7.30–7.62 at 15 kHz) is OK and verified against the printed tables.
  - Background-noise / air-lock quotes (pp. 60, 62) — OK, verbatim.
  - "Thus, equation (4) could be considered as the best alternate for the accurate prediction of the lower cut-off frequency of the anechoic chamber over equation (1)." (p. 70) — OK, verbatim.
  - Conclusions: "matches very well … and is within 3%" (p. 70) — OK, verbatim.
  - brief.html line 89 quoting "0.29/0.12 dB at 100 Hz and 3.02/3.65 dB at 200 Hz … against 5.67/6.17 dB at 315 Hz" — OK, exact match to Table 2.
  - brief.html line 108 / synthesis.html line 124: "slopes 0.1–0.3 dB/doubling at 100 Hz, 3.0–3.7 dB at 200 Hz" — **WRONG (imprecise) at the 100 Hz lower bound**: the actual combined Tables 2–3 minimum at 100 Hz is 0.01 dB, not 0.1 dB (a 10× understatement of how close to flat the decay is); the 200 Hz bound "3.0–3.7" is an acceptable rounding of the true 2.98–3.65 range. The same imprecise "0.1–0.3" figure is repeated in MATRIX-3W.md row 11 — same correction applies there.
  - brief.html line 152 / synthesis.html: "f = 2.25c/(d − l_w − a) … 312–320 Hz predicted against 315 Hz measured, 'within 3%' … c/(4L) under-predicted it by 10.5%" — OK, all verified (10.52% rounds to 10.5%).
  - synthesis.html line 184 (Singh↔Jiang reconciliation: "6±0.5 dB slope over four discrete distances in one 2.6×1.7×2.2 m room") — OK.
  - Reference-ledger DOI `10.1177/1475472X20905070` (brief.html line 238) — OK, matches printed DOI exactly.

- **Verified facts card**:
  - Cut-off is operationally defined by decay-slope collapse, not an absorber spec: "The lower cut-off frequency is defined as the minimum frequency from which the chamber shows its anechoic behavior" (p. 58).
  - Decay slope collapses close to flat well below the declared cut-off: 0.01–0.30 dB per doubling at 100 Hz vs 5.44–6.17 dB at 315 Hz (Tables 2–3, pp. 67–68).
  - Their own new formula, fitted on their own chamber only: `f_chamber = 2.25c/(d − lw − a)`, giving 312–320 Hz vs. 315 Hz measured, "within 3%" (Eq. 5, p. 59; Conclusions p. 70).
  - The classic λ/4 wedge-only rule under-predicts the real chamber cut-off for this room by over 10%: Eq. 1 → 285 Hz vs 315 Hz measured, 10.52% deviation (Table 4, p. 68).
  - Corners/edges not covered by full wedges still need patching to avoid reflection: "left-out edges and corners of the chamber are also properly covered with pieces of PU in order to avoid spurious reflections from the small surfaces" (p. 60).
  - Background noise must be suppressed for a valid traverse: "the presence of background noise will provide an extraneous value to the acoustic signals" (p. 62).
  - Broadband (fan) spectra inside vs. outside used only as a qualitative anechoicity check, not a quantitative cut-off determination, over "about 500 Hz to 20 kHz" (p. 70).
  - The paper's own Eq. 4/5 vs Eq. 6 discrepancy (320 vs 312 Hz) shows the source-size term `a` materially shifts the predicted cut-off, but the exact value used for the headline comparison is not stated (Table 4 vs Figs. 8–9, pp. 68–69) — a gap worth noting when applying the formula elsewhere.

- **Relevance**: Moderately relevant as a worked method example — the decay-slope-vs-log-distance verification and its collapse-below-cut-off signature (Eq. 19, Tables 2–3) is directly transferable to qualifying a small chamber like ours, but the fitted cut-off formula is validated on exactly one small room and should not be trusted as a generalizable predictor for a rotor-on-a-stand geometry.

---

## Retrieval note

All 11 papers were read at source in full (or, for the two PhD theses, in the specified required sections: Summary/Ch. 1/Ch. 6 real-time experiment/Ch. 7 for Haasjes; in full for the much shorter Jenny thesis). No paper in this batch was unobtainable; no request to Adam for a missing PDF was needed.
