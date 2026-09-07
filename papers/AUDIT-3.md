# AUDIT-3 — verification of reflection-localization/ and chamber-problems/ claims against source text

Method: every paper listed was opened in full (txt extract; PDFs for anything the extract lacked) and
checked against every existing claim about it in `reflection-localization/MATRIX-3W.md`,
`chamber-problems/MATRIX-3W.md`, `chamber-problems/EXTRACTS-local.md`, `chamber-problems/EXTRACTS-downloaded.md`,
`docs/reflection-localization.html`, and `docs/anechoic-chamber-problems-brief.html`. Where this audit and an
earlier document disagree, this audit is the one that re-read the source; the earlier document should be
corrected to match, not the reverse.

---

# Part A — reflection-localization/

## Sun 2012, J. Acoust. Soc. Am. 131(4):2828–2840 — Sun_2012_JASA_spherical-array-reflection-localization.pdf
- **Bibliographic check**: Title "Localization of distinct reflections in rooms using spherical microphone array eigenbeam processing." Authors Haohai Sun, Edwin Mabande, Konrad Kowalczyk, Walter Kellermann. *J. Acoust. Soc. Am.* 131(4), 2828–2840 (2012). DOI 10.1121/1.3688476 (received 7 Oct 2011, accepted 26 Jan 2012). All exactly as printed. Filename is correct.
- **Claim audit** (vs. reflection-localization/MATRIX-3W.md's "Sun 2012" row):
  - "Eigenmike, 32 mics on rigid sphere a = 0.042 m, order N = 4, 44.1 kHz" — OK
  - "white Gaussian noise via loudspeaker" — OK ("stationary white Gaussian noise was consistently used as a source signal")
  - "two shoebox rooms (T60 ≈ 900 ms and ≈ 400 ms, height 3.03 m)" — OK
  - "array at 1.41 m height" — OK
  - "Focusing frequency 4.5 kHz (k0a = 3.5)" — OK
  - "frequency-smoothing range 3.2–4.5 kHz (ka ∈ [2.5, 3.5])" — OK
  - "FFT 1024" — OK
  - "1° acoustic-map grid" — OK
  - "WNG constraint 0.6 dB" — OK
  - "SNRs 5 dB (room 1) and 3 / 17 dB (room 2); one parameter set for all cases" — OK
  - "Ground-truth DOAs from measured geometry fed to CATT" — OK
  - "resolves direct sound plus five first-order reflections and one second-order (walls 2+3) in room 1" — OK (Table I/V list exactly Direct, Ceiling, Floor, Wall2, Wall3, Wall4 = 5 first-order + Walls2+3 second-order)
  - Room 1 FS+WNGC deviations "direct 2.0°, ceiling 1.6°, floor 3.3°, wall 2 2.2°, wall 3 4.1°, wall 4 6.1°, walls 2+3 3.0°" — OK, matches Table V "FS and WNGC" column exactly
  - Room 2 (Table VI) "direct 2.0°, floor 1.0°, walls 3.6 / 2.2 / 3.1°; ceiling not localised at all" — OK, matches Table VI FS+WNGC column and footnote d
  - Eight loudspeaker positions (Table VII, SNR 5 dB): "three strongest reflections within 1.0–5.1°" — OK (Table VII min 1.0, max 5.1)
  - SNR sweep (Table VIII): "3 dB → 1.0/3.6/2.2/3.1°; 17 dB → 1.0/2.6/1.2/2.0°" — OK, exact match
  - "EB-ESPRIT localises only direct + one reflection (~3°)" — OK (Table IX: 4 deviations, 3.0/3.1/3.1/3.4°)
  - Quote "Up to six coherent sources, namely the direct-path sound and five first-order reflections can be well localized using the EB-MVDR with frequency smoothing and WNG control." (Sec. V, p. 2835) — OK, verbatim, correct page
  - Quote "the DOA-estimation deviation of reflected signals is larger than that of the direct sound signal, since the SNRs of reflected signals are much lower than for the direct sound, and some boundary surfaces in the rooms are not perfect reflectors." (Sec. V, p. 2837) — OK, verbatim, correct page
  - Quote (Table IV footnote d) "The ceiling in room 2 is not regular and it has several lights with quite large reflecting surfaces. Therefore, the localization results for the ceiling are all far from the ground truth values." (p. 2839) — OK, verbatim; page is correct
- **Verified facts card**:
  - EB-MVDR with frequency smoothing and a 0.6 dB white-noise-gain constraint is the most accurate and most robust of the tested methods: "the EB-MVDR has been shown to give comparable resolution and accuracy to the well-tuned EB-MUSIC, both of which significantly outperform the other investigated approaches" (Sec. VI, Conclusions, p. 2839).
  - Reflection SNR, not array error, dominates localisation error: reflected-signal DOA deviation exceeds the direct sound's "since the SNRs of reflected signals are much lower than for the direct sound" (Sec. V, p. 2837).
  - An irregular, fixture-laden ceiling defeats localisation outright: room 2's ceiling has "several lights with quite large reflecting surfaces," and its results are "all far from the ground truth values" (Table IV footnote d, p. 2839) — a concrete case of a non-planar/fixture-heavy boundary breaking a spherical-array reflection locator.
  - A single compact (32-mic, 8.4 cm-diameter) spherical array recording once can localise the direct path plus up to six early reflections (five first-order + one second-order) to 1–6° in ordinary shoebox rooms (T60 400–900 ms) at SNRs from 3–17 dB (Tables V, VI, VIII).
  - EB-ESPRIT, despite being subspace-based, "is not well suited for the localization of multiple reflections in reverberant environments" and only reliably resolves the direct path plus one reflection (Sec. V, p. 2837).
  - Frequency smoothing over a narrow band (here 3.2–4.5 kHz) is required to decorrelate the coherent direct/reflected signals before DOA estimation; narrowband beamformers "suffer from the self-cancellation of the coherent sources" (Sec. V, p. 2835).
  - Ground truth for these experiments came from CATT room-acoustics simulation software fed with manually measured geometry, not from an independent physical measurement of the reflection paths (Sec. V, p. 2833–2834).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low — the method needs a co-located 32-channel spherical array with coherent inter-channel phase, which the arc's independently-triggered UMIK-2s cannot provide; it is evidence for what a proper spherical-array tier could achieve, not a technique directly usable on this rig.

---

## Mabande 2013, J. Acoust. Soc. Am. 134(4):2773–2789 — Mabande_2013_JASA_room-geometry-inference-spherical-array.pdf
- **Bibliographic check**: Title "Room geometry inference based on spherical microphone array eigenbeam processing." Authors Edwin Mabande, Konrad Kowalczyk, Haohai Sun, Walter Kellermann. *J. Acoust. Soc. Am.* 134(4), 2773–2789 (2013). DOI 10.1121/1.4820895 (received 2 Apr 2013, accepted 26 Aug 2013). All exactly as printed. Filename is correct.
- **Claim audit** (vs. reflection-localization/MATRIX-3W.md's "Mabande 2013" row):
  - "focusing 4.5 kHz, smoothing 1.3–4.5 kHz i.e. ka ∈ [1, 3.5], WNG ζ = 1.148 = 0.6 dB, 1° grid, peaks kept only if in upper two-thirds of image power range" — OK, all verbatim/exact
  - Eigenmike 32 mics, a = 0.042 m, N = 4, 5 s signals, 44.1 kHz — OK
  - "Q = 1024 bins (~43 Hz)" — OK
  - "Simulated image-source shoebox (229.32 m³, α = 0.5–0.9, SNR 10–30 dB, open and rigid sphere, plus 240-mic a = 0.111 m array, N = 10)" — OK
  - "real lecture room T60 ≈ 900 ms, height 3.03 m, J = 4, loudspeaker 0.08 m diaphragm, 22.8 °C" — OK
  - "Real-room SNR stated as 12 dB in text and figure captions but 'SNR = 15 dB' in the Table IX header (inconsistent in text)" — OK, confirmed: text says "An SNR of 12 dB was measured" (p. 2785) and Fig. 15/16 captions say "an SNR of 12 dB," but Table IX header literally reads "SNR = 15 dB" (p. 2786) — a genuine inconsistency in the source paper itself, correctly flagged
  - "Simulation, J = 4, SNR 30 dB, α = 0.7: mean orientation deviation 1.6°, mean distance deviation 1.52 cm, relative volume error 0.35% (Table II)" — OK, exact
  - "J = 1: only 5 of 6 planes (P1 unresolvable, reflection too close in angle to direct path)" — OK
  - "SNR 10 dB: 5 of 6 planes, 6.1° / 5.11 cm; SNR 20 dB: 1.9° / 2.24 cm / 0.90% (Table III)" — OK, exact
  - "α = 0.9 (wood panelling): 5.8° / 2.14 cm, spurious higher-order planes (Table IV)" — OK, exact
  - "Large array: 0.6° / 1.38 cm (Table V)" — OK, exact
  - "Speech: 2.4° / 1.08 cm / 1.36% (Table VI)" — OK, exact
  - "Real room (Table VIII/IX): DOA deviations 1.0–5.0°" — OK
  - "TDOAs 3.6 / 3.9 / 24.4 ms matched exactly" — **WRONG → only 3.6 ms and 24.4 ms matched exactly; the 3.9 ms reflection was estimated at 3.8 ms by the RMVDR-based extraction (both noise and speech), and at 0.9 ms by EB-DAS.** Table VIII shows ground truth τ = 3.9 ms against estimates 3.8/3.8/0.9 ms — none of which is an exact match.
  - "noise 2.4° / 1.04 cm / 0.23% volume error, speech 3.2° / 1.44 cm / 0.21%" — OK, exact (Table IX)
  - "three reflections localised from one position" — OK, verbatim
  - "EB-DAS extraction gets the weakest TDOA wrong (0.9 vs 3.9 ms)" — OK
  - Quote "The positions of the walls, even in large acoustic enclosures, are estimated precisely up to a few centimeters only." — **WRONG page → p. 2786–2787 (opening of Sec. VIII Conclusions), not p. 2789** (p. 2789 is the reference list).
  - Quote "the errors in boundary plane estimation are mainly due to the errors in the DOA estimation, which substantially influence the orientation of the boundaries" (Sec. VII C 5, p. 2784) — OK, verbatim, correct page
- **Verified facts card**:
  - The method needs no measured room impulse response, only DOA/TDOA of the direct and reflected signals from uncontrolled broadband recordings via one compact spherical array: "the only a priori information required being the relative position of the sources to the array and the array geometry" (Sec. VIII, p. 2787).
  - Room-volume estimation is accurate to a few percent across all tested conditions: "the method is also directly applicable to room volume estimation, with an estimation accuracy error of 2% or less" (Sec. VIII, p. 2787).
  - The method is restricted to convex, piecewise-planar rooms: "restricted to rooms with walls that are piecewise planar and whose overall geometry is convex due to the boundary parameter estimation procedure" (Sec. VIII, p. 2787).
  - One microphone position cannot resolve every boundary: with a single source position, only 5 of 6 planes are found because "the angular distance between the reflection on the boundary and the direct path...is too small so that the spatial resolution of the beamformer does not suffice to discriminate them" (Sec. VII C 2, p. 2782–2783).
  - Highly reflective boundaries (α = 0.9, "wood paneling") degrade accuracy through spurious detections: "very high reflection coefficients result in many spurious planes resulting from higher-order reflections" (Sec. VII C 4, p. 2783).
  - The dominant error source is angular, not temporal: "the errors in boundary plane estimation are mainly due to the errors in the DOA estimation, which substantially influence the orientation of the boundaries" (Sec. VII C 5, p. 2784).
  - In the real lecture room, pillars were explicitly excluded from the ground-truth model: "its dimensions were also taken for simulations where the pillars have been neglected" (p. 2781) — a named, unmodelled fixture in the very room used to validate the method.
  - A larger array (240 mics vs 32) roughly triples DOA/orientation accuracy but does not always beat the small array on volume error, since "the larger individual errors of the boundary estimates average out" in the small-array case (Sec. VII C 5, p. 2784).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low — same as Sun 2012, this requires a single coherent spherical array rather than the arc's independent mics, though its confirmation that fixtures/pillars near a boundary go unmodelled and degrade estimates is a useful cautionary parallel for a chamber with equipment racks or a support pylon near the rotor.

### Documentation-staleness finding (Sun 2012 / Mabande 2013)
`docs/reflection-localization.html`'s evidence ledger (§07) lists Sun 2012 and Mabande 2013 under "Not retrieved — need the PDFs," stating "The first two are the foundational spherical-array localisation papers; nothing in §01 or §04 depends on them beyond what their abstracts state, but the accuracy figures quoted for tier 3 come from Lovedee-Turner alone rather than from a body of work." **This is factually wrong as of this audit.** Both papers are present as full PDFs with complete `pdftotext` extracts in `papers/reflection-localization/txt/`, and `reflection-localization/MATRIX-3W.md` itself states "Source texts: `papers/reflection-localization/txt/` (8 files, each read in full, 2026-09-07)" and carries detailed WHY/HOW/WHAT rows for both papers with page-cited quotes and tables — work that could only have been done from the full text, not an abstract. The html brief is stale relative to its own source directory. Fix: move Sun 2012 and Mabande 2013 to the "Read at source" panel, and reconsider the claim that tier-3 numbers rest on Lovedee-Turner alone, since Sun and Mabande now independently corroborate single-array reflection localisation to a few degrees / few centimetres.

---

## Lovedee-Turner &amp; Murphy 2019, J. Acoust. Soc. Am. 146(5):3339–3352 — Lovedee-Turner-Murphy_2019_JASA_3D-reflector-localisation.pdf
- **Bibliographic check**: Title "3D Reflector Localisation and Room Geometry Estimation using a Spherical Microphone Array." Authors Michael Lovedee-Turner and Damian Murphy (University of York AudioLab). Year 2019. Venue *The Journal of the Acoustical Society of America*. DOI 10.1121/1.5130569 (printed on the White Rose eprints cover page). The held file is the accepted manuscript — its own running header shows "pp. 1-15" — the citable published pagination (JASA 146(5):3339–3352) is **not printed anywhere in this text**. Filename is correct.
- **Claim audit** (vs. MATRIX-3W.md):
  - "Simulated RMS ∆Position (Table I): cuboid 4.63cm/8.59°, octagonal 2.69cm/2.01°, L 4.69cm/14.02°, T 16.45cm/8.03°" — OK.
  - Simulated-array (240-mic) / J=1/J=4 sweep, lecture-room, "SNR=15dB inconsistency" material some readers might expect here — **NOT FOUND in this text; MISATTRIBUTED — those numbers belong to Mabande et al. 2013** (audited separately above), not to this paper. (MATRIX-3W.md itself does not make this error — it correctly keeps Mabande's numbers in Mabande's own row — but this note is here because the two papers share methodology closely enough that a careless reader could conflate them.)
  - "L-room sets (Table II): 11.50±0.1cm/7.28°, 18.91±0.17cm/3.69°, per-set ranges 3.95–35.58cm" — OK (Room One's range; Room Two's is 4.22–32.81cm, not quoted by MATRIX but not contradicted).
  - "Real room (Table III): RMS 15.37cm, 1.21°, 23.02cm length; walls 4.02–25.46cm, floor 14.5cm, ceiling 10.60cm" — OK, exact match.
  - "Prior cuboid-only work: 0.063–29.38cm using 6–64 positions versus ≤3 here" — OK, verbatim.
  - Quote "The RMS boundary position errors are comparable to prior work with a maximum difference in RMS error of 16.38 cm, using at most three measurement positions, compared to 6-64 used in this prior work." (Sec. VII) — OK, exact, correct section.
  - Quote "the ceiling was covered in large metal piping connected to extractor fans and a layer of metal railing approximately 1 m from the ceiling." (Sec. IV) — OK, exact.
  - Quote "inaccuracies are likely due to either imperfect specular reflections, under or over estimation of the ToA for reflections in the measured impulse responses, or any inaccuracy in the estimated DoA" (Sec. V C) — OK, exact.
  - All HOW details (EDESAR framing, εa/εd/εes/εO thresholds, 80% overlap rule, band-pass 100Hz–5kHz, EM32 spatial Nyquist 8kHz, CATT parameters, room sizes, real-room dimensions/instrumentation) — OK, verified verbatim.
- **Claim audit** (docs/reflection-localization.html, §01 TIER 3 box and §04):
  - "RMS boundary error 2.7–4.7 cm simulated" — numerically matches Table I's cuboid/octagonal/L-shaped values (4.63/2.69/4.69cm) but silently **excludes the T-shaped room (16.45cm) with no stated rationale**, and silently **includes the L-shaped room, which the paper explicitly labels non-convex** ("a non-convex L-Shaped Room, and a non-convex T-Shaped Room," Sec. IV) — undermines the html's own convex/non-convex framing in §04.
  - "11.5–18.9 cm measured" — **WRONG**. These are Table II's *simulated* L-shaped-room-set values (Scenario Two, CATT simulation with the same parameters as Scenario One's L-room). The paper's actual measured/real-world result (Scenario Three, Table III) is a single RMS of **15.37 cm**, not an 11.5–18.9cm range. The html has mislabelled a simulated number as measured.
  - "aliasing frequency — 8 kHz for the EM32" — OK.
  - "every boundary must be at least 50 cm from both source and array" — OK, verbatim assumption.
  - "accuracy degrades sharply — 16 to 25 cm — once the room stops being convex" — **WRONG**. No such range is stated for non-convex rooms as a class. The paper's one non-convex outlier is the T-Shaped room (RMS 16.45cm, Table I), attributed explicitly to "the inferred boundaries being angled" (Sec. VI), not to non-convexity per se — and the *other* non-convex room tested, the L-Shaped room, scores 4.69cm (Table I), as good as the convex rooms, directly contradicting a "non-convex ⇒ 16–25cm" rule. The ~25cm figure appears to trace to Table III's individual boundary error (25.46cm) from the real-world measurement — which is an explicitly **cuboid (convex)** room, not a non-convex one.
- **Verified facts card**:
  - Assumptions require ≥50cm source/receiver-to-boundary clearance and parallel floor/ceiling, perpendicular walls (§I).
  - EM32's spatial Nyquist limits the reflection-detection band: "high-pass filtered at 100 Hz, reducing the impact of diffuse spectral components as a result of the spatial Nyquist frequency, 8 kHz" (p.3, §III.A).
  - Real-room measurement had non-removable confounding fixtures: "the ceiling was covered in large metal piping connected to extractor fans and a layer of metal railing approximately 1 m from the ceiling" (p.9, §IV).
  - Real cuboid-room floor and ceiling were localised to sub-15cm error: floor 14.5cm, ceiling 10.60cm (Table III, p.12).
  - Non-convex rooms are not inherently harder — only the T-shaped room was: L-Shaped RMS 4.69cm vs T-Shaped 16.45cm, both non-convex (Table I, p.10).
  - Method needs no large positional counts: real geometry recovered from at most three source/receiver measurement positions vs 6–64 in prior cuboid-only literature (p.12–13, Conclusions).
  - Errors trace mainly to ToA/DoA estimation quality, not geometry-inference math: "inaccuracies are likely due to either imperfect specular reflections, under or over estimation of the ToA…or any inaccuracy in the estimated DoA" (p.9, §V.C).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: High as a *locating* method (a spherical array could pin down which surface produces an unexplained reflectogram peak) but not directly usable with the arc's non-coherent, non-spherical mic layout; the ≥50cm-from-boundary and known-source-distance assumptions would need checking against the actual chamber before trusting cm-level output.

---

## Tervo, Pätynen, Kuusinen &amp; Lokki 2013, J. Audio Eng. Soc. 61(1/2):17–28 — Tervo_2013_JAES_spatial-decomposition-method.pdf
- **Bibliographic check**: Title "Spatial Decomposition Method for Room Impulse Responses." Authors Sakari Tervo, Jukka Pätynen, Antti Kuusinen, Tapio Lokki. *J. Audio Eng. Soc.*, Vol. 61, No. 1/2, 2013 January/February, pp. 17–28. No DOI printed anywhere in the text. Filename is correct (2013 matches the printed publication date). MATRIX-3W.md's parenthetical "(file labelled 2012)" refers to the PDF's internal document-title metadata ("JAES-1165-12_LR.dvi," a manuscript-ID artifact, confirmed via `pdfinfo`), not to anything in the rendered text, and does not contradict the 2013 publication date — worth softening in MATRIX-3W.md's own row to avoid implying a real dating dispute.
- **Claim audit** (vs. MATRIX-3W.md):
  - Method description (TDOA via generalized cross-correlation + exponential-fit interpolation, m̂=V⁺τ̂, n̂=−m̂/‖m̂‖, distance=ck∆t) — OK.
  - "Requirements: ≥4 non-coplanar mics, one omni, array ≤ head size, L∆t &gt; 2dmax/c" — OK, verbatim.
  - "Echo-density limit τ1 ≈ 0.0014·√V" — OK.
  - "7-mic open array (6 on sphere, 100mm spacing, +centre), 1.33ms Hann window, 99% overlap, 48kHz" — OK.
  - "image-source simulations of 30×20×12m (RT 2.0s) and 5×3×2.8m (RT 0.4s), reflection coeff. 0.85, 45th order" — OK.
  - "VBAP over 14 loudspeakers; 17 listeners; SDM vs SIRR (7 and 13 mics)" — OK.
  - "1ms window keeps one event per window until 119ms after direct sound in 7200m³; small room τ1=1.4ms" — OK.
  - Quote "The image-sources with the highest energy are correctly analyzed." (Fig. 3 caption) attributed to "p. 21" — **WRONG page → p. 20** (confirmed against the printed page-break markers: the "20" footer precedes this caption and the "21" footer follows it).
  - Quote "as the time progresses the number of acoustic events per time window increases... localizes the sound to the location of the reflection that is the strongest one in that time window." (Sec. 1.4) attributed to "p. 21" — **WRONG page → p. 20**.
  - "Listening-test similarity means: reference 0.98, SDML7 0.80, SIRR13 0.48, SIRRL7 0.40, anchor 0.00" — OK, exact.
  - "No localisation error in degrees or cm is reported" — OK, confirmed.
- **Claim audit** (docs/reflection-localization.html): Tervo appears only in the evidence-ledger reference list, with no attached numeric claim elsewhere in the html — citation itself OK, no DOI given, consistent with the source printing none.
- **Verified facts card**:
  - SDM needs only 4 non-coplanar mics with one omni channel and head-sized aperture: "the minimum requirement of the number of microphones is four, which are not on the same plane" (p.19, §1.2).
  - Window length is bounded below by the array's transit time: "the window size should be larger than the time that it takes for a sound wave to travel through the array, i.e., L∆t &gt; 2dmax/c" (p.19, §1.2.1).
  - Two simultaneous arrivals in one window collapse to the stronger one (p.20, §1.4).
  - Echo density gives a closed-form limit on single-event validity: τ1 ≈ 0.0014√V (Eq.7), yielding 119ms for a 7200m³ room at a 1ms window (p.19–20).
  - Perceptual validation, not geometric accuracy, is the paper's evidence: mean similarity SDML7 0.80 vs reference 0.98 vs SIRRL7 0.40 (p.24, §3).
  - Only ideal specular reflections were simulated; diffuse reflections are explicitly untested (p.25, §4.1).
  - The listening room used for validation itself deviated from ITU recommendations (NR30 vs recommended NR15; 1.2m vs &gt;2m listening distance) (p.21–22, §2.1).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Limited — SDM needs a compact, phase-coherent multichannel array (≥4 mics within head-sized spacing) to assign a direction per sample, which the arc's widely-spaced, independently-triggered UMIK-2 channels cannot provide; the echo-density/window-size reasoning is conceptually transferable to bounding when two arrivals become inseparable in time.

---

## Hadadi 2024, arXiv:2409.15484 — Hadadi_2024_arXiv_blind-localization-early-reflections.pdf
- **Bibliographic check**: Title "Blind Localization of Early Room Reflections with Arbitrary Microphone Array". Authors Yogev Hadadi, Vladimir Tourbabin, Zamir Ben-Hur, David Lou Alon, Boaz Rafaely (Ben-Gurion University of the Negev + Reality Labs Research @ Meta). Printed as arXiv:2409.15484v1 [eess.AS], 23 Sep 2024. No venue/journal, no DOI, no formal page range (informal running numbers 1–10 only) — preprint. Filename correct.
- **Claim audit**:
  - Four shoebox rooms 6×4×3 to 12×9×5 m, T60 0.62–1.22 s, 7.9–25.6 reflections in 20 ms (Table I) — OK
  - Source–array distance 0.7–1.7 m, ≥1.2 m from walls — OK
  - DRR range [−10, 10] dB — OK
  - STFT: 150 ms Hann, 75% overlap, 16 kHz — OK
  - Processing band 500–5000 Hz in 2 kHz bands — OK
  - Order N = 8; 900 Fliege–Maier DoAs; TP tolerance 0.5 ms/15° — OK
  - DBSCAN + k-means sub-clustering, threshold 0.25 — OK
  - Quote "reflections with high amplitudes, i.e. 0.4 with respect to the direct sound or higher, are easier to detect" (Sec. IV D) — OK exact
  - Quote "reflections that appear later, i.e. 10 ms with respect to the direct sound, are harder to detect" (Sec. IV D) — OK exact
  - Up to 15% of misses from clustering at 28–32 reflections — OK (Sec. IV E)
  - Azimuth-only cuts PFA for semi-circle (up/down ambiguity) — OK (Sec. IV F)
  - MUSHRA room 12×7×5 m, T60 = 0.57 s, RIR truncated at 20 ms, KU-100 HRTF, 16 listeners — OK
  - Spherical PD = 1, semi-circular PD = 0.85, both PFA = 0.4 — OK exact
  - RM-ANOVA F(3,45) = 54.04, p &lt; 0.001; spherical vs reference p = 0.057 (not significant); semi-circular significantly worse — OK exact
- **Verified facts card**:
  - FF-PHALCOR treats each reflection as an attenuated, delayed replica: "each reflection is considered as attenuated and delayed replicas of the direct sound" (Sec. II.B).
  - Detection quality falls as reflection density rises: "an increase in the number of reflections within the initial 20 ms leads to a reduction in PD" (Sec. IV.C).
  - Semi-circular array has an inherent front/back-style ambiguity: "an ambiguity in determining whether the origin of a reflection is the upper or the lower half-space" (Sec. IV.F).
  - Method works blind, with no RIR or source-signal knowledge: "Blindly estimating the direction of arrival (DoA) of early room reflections without prior knowledge of the room impulse response or source signal" (Abstract).
  - Listening test shows the spherical-array estimate is perceptually indistinguishable from the true reference: "no significant difference between the reference signal and the spherical array estimate" (Sec. V.C).
  - Reflections farther than the truncation point are excluded by design: RIR "truncated to include only the direct sound and early reflections with arrival time not longer than 20 ms" (Sec. V.B.1).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low — the method needs a coherent multi-microphone array (spherical or semi-circular) processing simultaneous channels for DoA, which the arc's single-axis, non-beamforming layout cannot provide; the delay/amplitude thresholds for detectability (≥0.4 amplitude, &lt;10 ms delay) are still useful sanity checks when predicting whether a floor bounce would even be separable.

---

## Sprunck et al. 2022, arXiv:2208.14017v2 — Sprunck_2022_arXiv_gridless-3D-recovery-image-sources.pdf
- **Bibliographic check**: Title "Gridless 3D Recovery of Image Sources from Room Impulse Responses". Authors Tom Sprunck, Antoine Deleforge (Univ. Lorraine/CNRS/Inria/LORIA), Yannick Privat (IRMA, Univ. Strasbourg/CNRS), Cédric Foy (UMRAE, Cerema/Univ. Gustave Eiffel/Ifsttar). Header prints "PREPRINT, NOVEMBER 2022"; the arXiv line reads "arXiv:2208.14017v2 [cs.SD] 7 Dec 2022" — the v2 timestamp (Dec) postdates the printed running-header date (Nov), an internal inconsistency in the PDF itself, not an extract error. No DOI, no journal (preprint). Filename correct.
- **Claim audit**:
  - 200 random shoebox rooms, L,W∈[2,10] m, H∈[2,5] m, wall absorption 0.01–0.3 — OK (Sec. V)
  - em32 geometry scaled ×2, d = 16.8 cm, fs = 16 kHz; Tmax = 50 ms, cTmax = 17.15 m — OK exact
  - Recovery tolerance 2° / 1 cm from array centre — OK exact
  - Grid-on-spheres init ~40k points, BFGS refinement, λ = 3·10⁻⁵, spikes &lt; 0.1 dropped — OK
  - Table I all four rows (recall/precision/RE/AE/EE/AmE for 0–150, 150–300, 300–500, 500–1323 sources) — OK exact match to printed table
  - "only 3 out of 1200 first-order image sources were missed... all 200 true sources were recovered" — OK exact
  - fs = 32 kHz or d = 42 cm → near-100% recall up to 500 sources — OK
  - PSNR 40 dB harmless, &lt;30 dB degrades, 30 dB recall recovers with 6° threshold — OK
  - Previous best [24] ~25 nearest image sources, 4.3° mean angular error, blind method — OK exact
  - Quote "The strength of the proposed gridless approach is revealed by the mean radial and angular errors, which are below tenths of millimeters and fractions of degrees." (Sec. V) — OK exact
  - Quote "applying the method to real data will require a number of challenging extensions. Indeed, real RIRs are impacted by the frequency and angular dependencies of source, microphone and wall responses." (Sec. VI) — OK exact
- **Verified facts card**:
  - Recovery accuracy is essentially arbitrarily fine under noiseless idealization: "mean radial and angular errors, which are below tenths of millimeters and fractions of degrees" (Sec. V).
  - Performance degrades in small/dense rooms: "the recall and precision significantly drop in smaller rooms, where the echo density is higher, making the image sources harder to separate" (Sec. V).
  - The method assumes frequency-independent wall reflection: real RIRs need "new formulations... in the Fourier and spherical-harmonic domains... frequency-dependent amplitudes" before use on real data (Sec. VI).
  - Occlusion (a reflection audible only to some microphones) is explicitly unhandled: "Generalization to non-cuboid polyhedral rooms will require robust extensions to occlusions" (Sec. VI).
  - The comparable discrete-grid approach would need "a spatial grid of at least 111 million points to achieve errors below 1° and 1 cm" (Sec. V) — four orders of magnitude larger than this method's grid.
  - Only one source/array placement is tested; extending to multiple placements is flagged as future work (Sec. VI).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low-to-none as a directly applicable method (it needs a compact spherical array and full-bandwidth RIR, not the arc's sparse single-elevation-per-mic layout), but its confirmation that frequency-independent, first-order image-source physics is the load-bearing assumption for any locator is a useful sanity check when trilaterating a floor bounce from the arc's own impulse responses.

---

## ISO 26101-2:2024 — ISO-26101-2_2024_standard-preview_environmental-correction.pdf
- **Bibliographic check**: "ISO 26101-2, Acoustics — Test methods for the qualification of the acoustic environment — Part 2: Determination of the environmental correction." First edition, 2024-06. Prepared by ISO/TC 43, Subcommittee SC 1, in collaboration with CEN/TC 211. No DOI (standards do not carry one — not printed). No author list (institutional document). Filename correct.
- **Claim audit**:
  - "ISO/TC 43/SC 1" — OK exact
  - Preview covers only front matter, Scope, Clauses 2–4 and 5.1 — OK, confirmed the extract cuts off mid-Clause 5 (§5.1 General) with nothing from §5.2 onward
  - Clause 5 (absolute comparison test) "expected to yield the most accurate results in typical industrial environments" — OK exact (4.2)
  - Clause 6 assumption "approximately a cubic shape, ... substantially empty, ... sound is absorbed at the room boundaries only", three sub-methods — OK (4.3)
  - Clause 7 "the preferred method to qualify a hemi-anechoic room and represents the most accurate method", goal K2 = 0, hemi-anechoic only — OK (4.4)
  - Clause 8 "considered to be the least accurate method" — OK exact (4.5)
  - Quote "In some industrial buildings, which are of low height and have reflecting surfaces, the sound propagation can be distorted. In these conditions, the qualification procedures according to Clause 6 and Clause 8 might not be applicable." (4.5 NOTE, p. 3) — OK exact
  - Quote "In hemi-anechoic rooms, the other qualification procedures can yield unreliable results." (4.4 NOTE, p. 3) — OK exact
  - "K2 increases with S" (3.3 Note 3, p. 2) — OK exact — "In general, the environmental correction depends on the area of the measurement surface and usually K2 increases with S."
  - Numeric criteria (7.2.2, 7.2.4, Annex A) outside the sample — OK confirmed — TOC lists them, body text is not present
  - HTML §05 table: clause-by-clause procedure/when/verdict cells — OK, all four match Clauses 4.2–4.5 verbatim content
- **Verified facts card**:
  - K2 is defined narrowly, tied to a specific measurement surface: "correction applied to the mean (energy average) sound pressure levels over all the microphone positions on the measurement surface... to account for the influence of reflected or absorbed sound" (3.3).
  - K2 is frequency-dependent, with distinct symbols for band and overall values (K2f, K2A) (3.3, Note 2).
  - Four qualification procedures exist and must be selected via Fig. 1, not applied interchangeably (4.1–4.5).
  - The inverse-square-law method (Clause 7) is restricted to hemi-anechoic rooms only: "may be used to qualify hemi-anechoic test rooms" (4.4).
  - No procedure in this document localises an individual reflection — K2 is a single scalar (or band series) correction, not a spatial diagnostic (Scope, Clause 3).
  - The absolute-comparison method (Clause 5) is usable indoors or outdoors and does not require removing the source under test in all cases (4.2, 5.2 reference).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Direct and high — Clause 5's reference-sound-source method is the standard's own recommended path for a room that cannot be made anechoic, giving a defensible, frequency-resolved K2 correction without removing the rig, exactly the situation of a rotor permanently mounted on the Tyto stand.

---

## Meyer-Kahlen, Amengual Garí &amp; Lokki 2022, ICA 2022 proceedings — Meyer-Kahlen_2022_ICA_what-SDM-can-and-cannot-do.pdf
- **Bibliographic check**: "What the spatial decomposition method can and cannot do." Nils Meyer-Kahlen, Sebastià V. Amengual Garí, Tapio Lokki. Published in ICA 2022 proceedings, Acoustical Society of Korea (ASK), paper ID ABS-0825. No DOI, no page range printed (only informal running page numbers). Affiliations: Aalto University (Espoo, Finland) and Reality Labs Research, Meta. The city "Gyeongju" is not printed anywhere in this text — correct as background but not sourced from the paper itself. Filename correct.
- **Claim audit**:
  - Fig. 2 caption "Direct sound as well as [floor] and ceiling reflection are easily visible on both plots" — OK exact (OCR drops the "fl" ligature)
  - TDoA returns direction of largest peak, PIV returns weighted mean, for overlapping events — OK (Sec. 3.3)
  - Nmin = 2·fs·dmax/c (Eq. 9); fsa = c/(2πr) — OK exact
  - Two plane waves Δt = 0.05 ms, 6 dB level difference, 0.5 ms window (Fig. 3) — OK, with the caveat that the source text prints "005 ms"/"05 ms" with dropped decimal points; 0.05/0.5 ms is the only physically sensible reading and matches the paper's own array-size arguments
  - 180 Gaussian noise sources, arrays "r = 125 cm" (Fig. 4) — confirmed unresolvable OCR ambiguity (possibly a lost decimal point), correctly flagged as "unclear in text" already
  - Quote "The estimate follows the directional distribution only to some extend." (Sec. 3.4) — OK exact, including the paper's own typo ("extend" for "extent")
  - Quote "directional analysis fails if two sound events occur simultaneously, wherein it is important to note that simultaneously does not mean that the sound events need too occur within one sampling interval, but within one analysis block." (Sec. 3.3) — OK exact, including paper's typo "need too occur"
  - Quote "the broadband analysis stage of SDM is a robust way to identify reflections in the early part of the response, but that the temporal resolution is limited by the size of the used microphone array, regardless of the estimation method." (Sec. 5) — OK exact
  - "No numeric DoA accuracy given (unclear in text)" — OK confirmed
  - HTML claim "misses two arrivals closer together than the time a wave takes to cross the array — the limit scales with array size" — OK, directly supported by Sec. 3.3 and the Sec. 5 conclusion
- **Verified facts card**:
  - SDM's whole model is one direction per time sample: "at any given sample at time t of a room impulse response, exactly one sound event occurs, originating from a direction of arrival (DoA)" (Sec. 2).
  - Raising sample rate does not fix temporal resolution: "increasing the sampling rate fs does not improve the separation of the reflections" (Sec. 3.3).
  - PIV needs first-order (B-format/Ambisonics) signals, TDoA needs ≥4 non-coplanar open omnis (Sec. 3.1).
  - SDM renderings are known to sound "rough" or "grainy" on transient content unless compensated (Sec. 4.2).
  - In direct comparison, SDM is usually distinguishable from a real reference in listening tests (Sec. 4.4).
  - Late-field (high reflection density) directional estimates remain partially informative despite violating the one-direction-per-sample model (Sec. 3.4).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low-to-moderate — the paper's core lesson (temporal separability is capped by array transit time, not sample rate) is directly transferable reasoning for judging whether any future compact array on the rig could resolve a floor bounce from the direct sound, but the arc itself has no coherent multi-channel phase relationship needed for TDoA/PIV analysis.

---

# Part B — chamber-problems/

## Alkmim et al. 2022, J. Acoust. Soc. Am. 152(5):2735–2745 — Alkmim_2022_JASA_drone-directivity-hemispherical-array.pdf
- **Bibliographic check**: Title "Drone noise directivity and psychoacoustic evaluation using a hemispherical microphone array." Authors Mansour Alkmim, João Cardenuto, Elisa Tengan, Thomas Dietzen, Toon Van Waterschoot, Jacques Cuenca, Laurent De Ryck, Wim Desmet. *J. Acoust. Soc. Am.* 152(5), pp. 2735–2745, published online 7 Nov 2022. DOI 10.1121/10.0014957. Filename is correct.
- **Claim audit**:
  - MATRIX-3W row 33 "Hemi-anechoic 16×12.5×6 m, foam under drone, SHD" — OK, text: "room interior dimensions are 16 × 12.5 × 6 m (length × width × height)" (p. 2736).
  - "Reflection 'minimized … but not fully suppressed, especially at low frequencies'" — OK, verbatim, p. 2737.
  - "aliasing above 164 Hz" — OK (text gives fmax = 163.77 Hz, p. 2739; 164 Hz is a rounding, not an error).
  - "'a 2.5 × 2.5 m² area under the UAS was covered by a foam material with approximately 0.07 m thickness to mitigate ground reflections'" — OK, verbatim, p. 2736.
  - "Polar 'null point … closer to the 90° elevation' and up to 12 dB elevation variation" — OK, verbatim, p. 2740.
  - Nulls "attributed to the symmetry of the drone" — OK, verbatim, p. 2740.
  - "OSPL of reconstructed vs target differs by 2.5 dB at 4987 rpm" — OK, text: "OSPL difference of 2.5 dB" for 4987 rpm, "no difference" at 6152 rpm, p. 2743.
  - "At low frequencies, below 50 Hz, the −70° direction has much higher levels … attributed to the downward airflow across the microphone diaphragm" — **questionable**: the extracted text reads "the 70° direction" with no minus sign (p. 2742), likely OCR-dropped (this OCR drops "±" and "×" elsewhere too); the elevation-sign convention isn't recoverable from the text layer alone — flag for a visual PDF check if the sign matters downstream.
  - Windscreen "can account for high-frequency attenuation at this position" — OK, paraphrased faithfully, p. 2742.
  - Recirculation "not mentioned" — OK, confirmed absent from the text.
  - Brief.html's "55% of blocks rejected at TU Berlin" listed alongside Alkmim — **not misattributed**: that figure belongs to Hochbaum 2026, and the row correctly groups three sources under one general symptom without asserting Alkmim reported 55%.
- **Verified facts card**:
  - Facility: "hemi-anechoic chamber with an acoustically hard ground" fitted with "fiberglass wedges covered by perforated aluminum panels," 16×12.5×6 m (p. 2736).
  - Ground-reflection mitigation: 2.5×2.5 m² foam pad, ≈0.07 m thick, under the drone (p. 2736).
  - Reflection still present: "the effect of ground reflections is minimized during measurements but not fully suppressed, especially at low frequencies" (p. 2737).
  - Signal processing already excludes flow noise: SPL computed from signals "bandpass filtered between 20 Hz and 20 kHz, in particular, to discard flow-induced low-frequency pseudo-sound" (p. 2741).
  - Spatial-aliasing limit for the 3rd-order SHD, R = 1 m: fmax = 163.77 Hz, valid "up to the first BPF tone for rotor speeds lower than 4900 rpm" (p. 2739).
  - Directivity nulls in every polar plot: "a null point can be observed closer to the 90° elevation," with elevation-to-elevation SPL variation "as much [as] 12 dB" (p. 2740), attributed to drone symmetry, not the room.
  - Mic 1 (directly under the rotors) required "a windscreen foam" because of downward propeller airflow (p. 2736).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Directly relevant — a rotor rigidly stood over a hard hemi-anechoic floor, using foam-patch mitigation and a vertical/hemispherical mic array, is architecturally the same class of measurement as the SoundVisualizer arc rig, and it explicitly documents an unsuppressed low-frequency floor-reflection residual plus a flow-noise artefact at the under-rotor microphone.

---

## Fasulo et al. 2025, Aerospace 12(7):647 — Fasulo_2025_Aerospace_rotor-noise-directivity-decay.pdf
- **Bibliographic check**: Title "Experimental Acoustic Investigation of Rotor Noise Directivity and Decay in Multiple Configurations." Authors Giovanni Fasulo, Giosuè Longobardo, Fabrizio De Gregorio, Mattia Barbarino (CIRA / Univ. Naples Federico II). *Aerospace* 2025, 12, 647. DOI 10.3390/aerospace12070647, MDPI, open access (CC BY). Filename is correct. Note: the printed "Citation:" block itself reads "Fasulo, G.; Fasulo, G.; De Gregorio, F.; Barbarino, M." — a duplication typo in the source PDF's own front matter (the byline correctly lists Longobardo as second author) — this is the journal's printing error, not a SoundVisualizer transcription error.
- **Claim audit**:
  - "CIRA semi-anechoic chamber … 90 Hz cut-off frequency, measures 5.65 m × 4.45 m × 4.00 m" — OK, verbatim, p. 3.
  - "the ground was treated as an acoustically rigid surface, so local reflections could either reinforce or attenuate the radiated sound, thereby altering the apparent directivity" — OK, verbatim, p. 10.
  - "reflections from the chamber floor redirect tonal energy into directions that should otherwise be relatively quiet, most notably at 0° and 180°" — OK, verbatim, p. 12.
  - "dips are far less pronounced than theory anticipates" — OK, verbatim, p. 12.
  - Near-field decay "~17 dB/doubling" below 2D, far-field "marginally less than 6 dB, consistent with the influence of ground reflections" beyond 3D — OK, verbatim, p. 15.
  - "pronounced oscillations … constructive and destructive interference between the direct acoustic wave and its ground-reflected counterpart" — OK, verbatim, p. 15.
  - "The quasi-constant OASPL observed at certain distances and frequencies is not yet understood" — OK, verbatim, p. 15.
  - Pylon offset "produces additional shading" and "lies directly on the acoustic line of sight of microphone 10" — OK, verbatim, but these are two separate facts on **pp. 10 and 12 respectively**, not a single "p. 11–12" as some extract bullets imply — minor page-citation imprecision, not a content error.
  - "Reversing the sense of rotation revealed that even modest geometric asymmetries, here the support pylon, can shift directivity by up to 4 dB." — OK, verbatim, p. 24 (Conclusions).
  - Rotation-sense OASPL spread: ~1 dB (3000–5000 rpm), ~3 dB (6000 rpm), 3–4 dB (7000–8000 rpm), SD growing to ~4 dB at 7000 rpm — OK, p. 12.
  - Plate installation: mean 6.5 dB left/right asymmetry at BPF‑1, ~10 dB local at BPF‑2, 1.6 dB path-length effect deemed insufficient, "near-field interactions, in which the rotor's pressure field couples with the plate edge and ground surface" — OK, all verbatim, p. 22.
  - Mic 9 in downwash: "intense, large-scale turbulent structures that amplified the low-frequency broadband noise," omitted from OASPL — OK, pp. 9–10.
  - Motor tones: fmot ≈ 133 Hz, electromagnetic tone ≈1870 Hz, sidebands at ±q·fmot, motor tone ≥20 dB below BPF raising OASPL "by no more than 0.004 dB" — OK, pp. 9–11.
  - Δf = 3 Hz chosen so multi-rotor BPF lines "coalesce into a single, unambiguous peak" — OK, p. 7.
  - Recirculation ruled out: "BPF harmonics remain sharp and strictly horizontal … no progressive rise in broadband energy," rotor plane "~6 D above the floor," nearest wall "more than 12 D downstream" — OK, p. 18.
  - Brief.html §5 "exclude the sector shadowed by the pylon" ↔ "Measurements taken within the 0°–90° sector will not be analysed … additional interference from the pylon" — OK, verbatim, p. 19.
  - Blade-set repeatability "&lt; 0.6 dB" — OK, p. 11/Conclusions.
- **Verified facts card**:
  - Rig: isolated propeller on a "TYTO ROBOTICS 1585 Thrust Stand" — the same model stand used by SoundVisualizer (p. 4).
  - Chamber: 5.65 m × 4.45 m × 4.00 m, "90 Hz cut-off frequency"; OASPL integration bounds set at 90 Hz–20 kHz "excluding room-reflected energy below 90 Hz" (p. 7).
  - Floor reflection fills in theoretical directivity nulls at 0°/180° for the isolated rotor (p. 12).
  - Far-field decay beyond 3 diameters is "marginally less than 6 dB" per doubling, with ripples from direct/ground interference (p. 15).
  - Reversing rotation sense — not changing hardware — shifted directivity "by up to 4 dB," proof the asymmetry is a fixture/room effect, not a source effect (p. 24).
  - A rigid mounting plate produced near-field coupling asymmetries up to ~10 dB locally, too large to be explained by simple blockage/path-length (only ~1.6 dB) (p. 22).
  - Recirculation was checked and excluded via 30 s spectrograms plus geometric clearance (~6 D floor, &gt;12 D wall) (p. 18).
  - The chamber's rigid floor was an accepted, explicitly stated experimental limitation, not a hidden confound (p. 10).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Maximally relevant — this is the closest analogue in the whole corpus to SoundVisualizer's own rig (same Tyto 1585 stand, small semi-anechoic room, tonal rotor noise on an elevation-varying microphone layout), and it directly demonstrates floor-filled directivity nulls, decay-law ripples from ground interference, and a multi-dB directivity shift traceable to a support-pylon/asymmetry artefact rather than the rotor.

---

## Amiet 1980/1981 — Schlinker-Amiet_1980_NASA-CR3371_refraction-scattering-shear-layer.pdf
- **Bibliographic check**: Title (title page and Report Documentation Page) "REFRACTION AND SCATTERING OF SOUND BY A SHEAR LAYER." **Authors: Robert H. Schlinker and Roy K. Amiet** — NOT solely "Amiet" as the filename and every existing citation of this report (RETRIEVAL-A.md, docs/anechoic-chamber-problems-brief.html's evidence ledger) imply. Performing organization: United Technologies Research Center, East Hartford, CT 06108, under NASA contract NAS1-15339. Report number NASA CR-3371; the Report Documentation Page's field 5 "Report Date" prints **December 1980**, and the closing line reads "NASA-Langley, 1980" — but the NTRS accession number used to retrieve it (19810008332) is a 1981 catalogue/release id, which is presumably why downstream lists call it "1981." No DOI (pre-DOI-era NASA CR; item 3 "Recipient's Catalog No." is blank). Item 21 "No. of Pages" prints **189**, not the "192 pp" figure used to describe it in RETRIEVAL-A.md/README.md (a minor discrepancy — possibly front-matter/roman-numeral pages counted differently). **Filename is misleading**: it should be `Schlinker-Amiet_1980_NASA-CR3371_...` to match both the actual authorship and the printed report date, consistent with the naming already used for the companion `Schlinker-Amiet_1978_NASA-CR145359_...` file (same two authors, same order, same UTRC facility, extending the same theory).
- **Claim audit**: No paper-specific numeric value or quotation is attributed to this report by name anywhere in `chamber-problems/MATRIX-3W.md` (which has no row for it at all), `EXTRACTS-local.md`, or `EXTRACTS-downloaded.md`. `docs/anechoic-chamber-problems-brief.html`'s evidence ledger (the row listing "Merino-Martínez et al. 2020...; Schlinker & Amiet 1978, NASA CR-145359; Amiet 1981, NASA CR-3371; Bahr et al. 2020, 2021...") cites it only as a general background reference for "open-jet tunnels, shear-layer refraction/scattering, ultrasonic qualification" — every specific number in the brief's body text near that row (M 0.2, 5 kHz, the 600 µs Tukey window, etc.) is independently attributable to Schlinker & Amiet 1978 or the Bahr papers, not to this report. So: **no existing claim to mark right or wrong**, other than the authorship point above, which is a genuine bibliographic error in how this report has been cited (`WRONG → co-authored by Schlinker and Amiet, not Amiet alone`).
- **Verified facts card** (new — first extraction of this report into the corpus):
  - Same UTRC Acoustic Research Tunnel and 0.91 m open jet as the shorter 1978 companion report, extended with an off-axis correction and a turbulence-scattering study: "Experiments were performed using a 0.91 m diameter open jet in the United Technologies Research Center (UTRC) Acoustic Research Tunnel" (Summary, p. 1).
  - Refraction is significant at any of the Mach numbers tested: "Far-field noise directivity patterns measured in open-jet acoustic test facilities are significantly altered at test Mach numbers of 0.1 and greater due to sound wave refraction by the open-jet shear layer" (Conclusions §a, p. 67).
  - Refraction/amplitude changes are independent of both shear-layer thickness and of frequency over 1–10 kHz, confirming the theory's zero-thickness assumption (Conclusions §c–d, p. 67).
  - The off-axis correction theory disagrees with experiment specifically when the source sits close to the shear layer: "For an off-axis source situated at a source-to-shear layer separation distance less than one jet radius, measurable differences between theory and experiment occurred for the refraction angle change. The disagreement, at present, is not understood" (Conclusions, p. 68).
  - Turbulence scattering (tested 5–15 kHz, M 0.1–0.3) is worse close to the jet axis and further downstream: "Scattering is stronger at angles close to the open jet axis than at 90°... Scattering becomes stronger as the acoustic source position shifts downstream" (Conclusions, p. 67).
  - Scattering becomes significant once the propagation-path-length-to-wavelength ratio approaches 10: "Scattering becomes significant as the ratio of shear layer propagation path length to acoustic wave length approaches a value of 10" (Conclusions, p. 68).
  - Tone broadening (frequency scattering) is explained mechanistically as Doppler-shifting by turbulence upstream/downstream of the ray's shear-layer crossing point, and its presence implies angular scattering also occurred (Conclusions, p. 68).
  - The report supplies an analytical method to predict the onset frequency of scattering, separate from the refraction-angle correction: "The frequency at which the onset of turbulence scattering occurs can be estimated using an analysis developed during the present study" (Conclusions, p. 68).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low/indirect — this report is entirely about free-jet (open-jet wind-tunnel) shear-layer refraction and turbulence scattering, which requires a moving air stream between source and microphones; SoundVisualizer's rotor sits in still air in a closed room, so the shear-layer correction machinery itself does not apply. The only transferable idea is the general one that a propagation medium's properties (there: a moving shear layer; here: a reflecting floor) must be corrected for before trusting far-field directivity, and downstream literature's habit of citing "the Amiet correction" traces back to the *theory* originated by Amiet, tested jointly with Schlinker in this report and its 1978 predecessor.

---

## Bahr, Hutcheson &amp; Stead 2020 (NASA/NTRS accession 20205011271) — Bahr-Hutcheson-Stead_2020_NASA-NTRS_open-jet-vs-Kevlar-propagation.pdf
- **Bibliographic check**: Title (exact): "Unsteady Propagation and Mean Corrections in Open-Jet and Kevlar Wind Tunnels." Authors (exact, full list): Christopher J. Bahr and Florence V. Hutcheson (NASA Langley Research Center), Daniel J. Stead (Science and Technology Corporation) — three authors, matching the filename's "Bahr-Hutcheson-Stead." Footnote: "Presented as Paper 2018-3118 at the 24th AIAA/CEAS Aeroacoustics Conference, Atlanta, GA, 25–29 June 2018." No journal name, volume/pages, or DOI for this document itself appears anywhere in the text. No "2020" date is printed in the body; the filename's "2020" is not attested in-text — it evidently comes from the NTRS accession number 20205011271 (catalog/release year, not a printed publication date). Filename is otherwise correct.
- **Claim audit**:
  - "600 µs 25% Tukey window ... to remove any reflected or scattered signals ... reducing analysis to a single propagation path" — OK, verbatim.
  - γ² ≈ 0.2 at 10 kHz for the −45° mic at Mach 0.17 — OK, verbatim: "as low as 𝛾² = 0.2 at 10 kHz for the −45° microphone at Mach 0.17."
  - Background noise "similar to open jet at 3 kHz, ~5 dB higher at 10 kHz, &gt;25 dB higher at 40 kHz (M 0.17)" — OK, matches almost verbatim.
  - "could completely mask a 40 kHz source that is perfectly observable otherwise" — OK, verbatim.
  - "Microphone grid cap distorts the pulse waveform significantly" — OK in substance: "The microphone grid in particular was observed to add significant distortion to the signal."
  - Open-jet CV reaching unity/≥10 at high frequency, M=0.17, at −60°/−45° — OK.
  - Kevlar ringing after the pulse + Doppler-related ripple — OK.
  - Brief.html row 121's "significant above M 0.2 and 5 kHz" framing: this specific Mach/frequency threshold is **not this paper's finding** — it is Schlinker & Amiet 1978's scattering threshold. The brief's row cites Bahr 2020/2021 in the same sentence as a general "src" tag alongside Schlinker & Amiet 1978 and Wang 2019 without itemising which number belongs to which paper. This is loosely-attributed rather than misattributed (no specific number is falsely pinned to Bahr), but the html could be clearer about which source owns which number.
- **Verified facts card**:
  - Two test-section types compared at NASA Langley Quiet Flow Facility: open-jet vs. tensioned Kevlar panel (Style 120, 34 fibres/inch) (Abstract).
  - Source is a laser-plasma pulsed point source in the flow, arc of 1/8″ mics outside the flow at −45°…−135° (§III).
  - Time-gating with a 600 µs 25% Tukey window isolates the direct path before any Fourier analysis.
  - Open-jet coherence loss is far worse than Kevlar: γ² drops to 0.2 at 10 kHz at −45°, M 0.17, vs. ~0.7 with Kevlar (§IV.C).
  - Kevlar's own background noise is its chief drawback, growing from parity at 3 kHz to +25 dB at 40 kHz (M 0.17).
  - "The background noise production of the Kevlar is sufficiently high such that it could completely mask a 40 kHz source that is perfectly observable otherwise" — the paper's central trade-off statement.
  - Kevlar shows deterministic post-pulse ringing (panel's own mechanical response), not present in the open-jet case.
  - Practical guidance: choose Kevlar for coherence-critical (array) work, open-jet for very low background-noise needs.
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low/indirect — this is an open-jet vs. Kevlar-wall wind-tunnel comparison for phased-array coherence, not a closed anechoic chamber with a static rotor rig; the only transferable idea is that time-gating (a short Tukey window around the direct arrival) isolates the direct path from reflections/scattering, the same principle SoundVisualizer would use for reflection localisation.

---

## Bahr 2021 (NASA/NTRS accession 20210015848) — Bahr_2021_NASA-NTRS_open-vs-closed-test-section-arrays.pdf
- **Bibliographic check**: Title (exact): "Toward Relating Open- and Closed-Test Section Microphone Phased Array Aeroacoustic Measurements." Author: Christopher J. Bahr (sole author), NASA Langley Research Center — the filename correctly shows only "Bahr" (single-author, unlike the 2020 paper). No journal, volume/pages, or DOI printed for this document itself. No explicit "2021" copyright date is printed, but the reference list cites its own companion work as "27th AIAA/CEAS Aeroacoustics Conference, to be published, 2–6 August 2021," and the text mentions the open-jet test occurred "in 2020/2021" — consistent with the NTRS accession 20210015848. Filename is correct.
- **Claim audit**:
  - "tunnel walls are approximately rigid in the acoustic sense, leading to significant reflections in the reverberant environment" — OK, verbatim (Introduction).
  - "severe blurring due to the decorrelation of acoustic waves passing through a turbulent free shear layer" — OK, verbatim (Abstract).
  - "at 10.6 kHz baseline DAMAS begin[s] to fall apart due to coherence loss" — OK, matches.
  - "at 30 kHz conventional beamforming 'completely fails to localize' and the open-jet DAMAS map 'is, for the most part, unusable'" — OK, both phrases verbatim.
  - "Coherence loss underestimates summed levels: correction raises wing spectra ~2 dB and slat ~5 dB at high frequency" — OK, verbatim.
  - "Corrected closed vs open-jet slat spectra still differ by up to 8 dB at 40 kHz" — OK, matches.
  - Mutual coherence function fitted with a von Kármán correlation to in-wing speaker coherence data — OK, confirmed.
  - "Relative (Mach-scaling) comparisons are insensitive to facility: ~5 dB at low frequency" — OK, matches.
- **Verified facts card**:
  - Same CRM-HL high-lift model tested at NASA Langley 14×22-Foot Subsonic Tunnel in closed-wall (2018) and open-jet (2020/2021) configurations, same Mach numbers (Abstract).
  - Closed test section: "the tunnel walls are approximately rigid in the acoustic sense, leading to significant reflections in the reverberant environment" (Introduction) — reflections/background noise dominate, not shear-layer effects.
  - Image-source Green's functions mirrored across floor/ceiling (24,030-point extended grid) were used in DAMAS to model incoherent floor/ceiling reflections in the closed section.
  - Open-jet DAMAS deconvolution degrades sharply with frequency: usable at low/mid frequency, "begin[s] to fall apart" by 10.6 kHz, and by 30 kHz is "for the most part, unusable."
  - A coherence-loss correction (von Kármán-based mutual coherence function) partially restores summed spectral levels in the open jet, but a residual gap (up to 8 dB at 40 kHz for the slat) remains between corrected closed and open-jet results.
  - "Counterintuitively, improving the physics modeling in the propagation functions is detrimental to the agreement between the two facility configurations" — the paper's stated caution about over-interpreting agreement.
  - Recommendations: always acquire empty-tunnel background data (none was taken for the closed-section 2018 test — a stated limitation), quantify instrumentation/protective covers, and build coherence-loss models from known reference sources.
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low/indirect — this concerns large wind-tunnel phased-array beamforming (DAMAS) in open-jet vs. closed test sections, not single-mic-per-elevation rotor-on-stand measurement; the only transferable concept is that closed, reflective enclosures contaminate array data with coherent image sources (floor/ceiling), qualitatively the same floor-reflection problem SoundVisualizer's arc faces, just without any array/beamforming machinery to correct for it.

---

## Belyaev, Golubev, Zverev, Makashov, Palchikovskiy, Sobolev &amp; Chernykh 2015 — Belyaev_2015_AcoustPhys_wedge-absorption-anechoic-chambers-EN.pdf + Belyaev_2015_AkustZh_wedge-absorption-anechoic-chambers-RU.pdf
- **Bibliographic check**: Title (both printings, identical in translation): "Experimental Investigation of Sound Absorption of Acoustic Wedges for Anechoic Chambers." Authors: I.V. Belyaev, A.Yu. Golubev, A.Ya. Zverev, S.Yu. Makashov, V.V. Palchikovskiy, A.F. Sobolev, V.V. Chernykh (TsAGI + Perm National Research Polytechnic University). Year 2015. English printing: *Acoustical Physics* 61(5):606–614, DOI 10.1134/S1063771015050048, © Pleiades Publishing. Russian original: *Akusticheskii Zhurnal* 61(5):636–644 (a "DOI"-shaped string in the Russian OCR text is garbled/unreadable — not a real DOI; the genuine DOI is the one printed in the English translation). Both filenames are correct. OCR finding: the Russian scan's byline appears to read a fifth author as "Нальчиковский" ("Nalchikovskiy") where the English Pleiades translation gives "Palchikovskiy" — almost certainly an OCR misread of "Пальчиковский" (Palchikovskiy is independently attested as a co-author of this same chamber programme in Palchikovskiy et al. 2016), not a genuine authorship discrepancy.
- **Claim audit**:
  - "AC-3 V = 125 m³" — OK, both languages.
  - "AC-11 volume 230 m³ (English) vs 210 m³ (Russian)" — **DISCREPANCY BETWEEN EN AND RU PRINTINGS, confirmed**: English "reverberation chamber of the AC11 acoustic bench volume V = 230 m³"; Russian "объем V = 210 м³." The Russian original is authoritative as the original-language publication (a volume figure is exactly the kind of value a translator/typesetter can transpose digits on). No other numeric discrepancy was found after comparing Tables 1–2, block surface areas, and all geometry figures between the two printings.
  - "AC-2 baseline: wire frame, caprone fibre 80–90 kg/m³, 600 mm total height, 200×200×150 mm base, blocks of 25, 100 mm from wall" — OK, both languages.
  - "αn ≥ 0.99 at f≥100 Hz except 160 Hz (αn=0.978)" — OK, both languages.
  - "AC-2 certified per ISO 3745:2003 for f &gt; 200 Hz" — OK, both languages.
  - "BSFF wedges 800×200×1000 mm, base 100mm, densities 20/30/40 kg/m³, fibre ≤1–2 µm"; "40 kg/m³ BSFF tests deemed invalid" — OK, both languages.
  - "TMF wedges 5–9 µm fibre, 30/50/70 kg/m³, plus 110 cm-tall version" — OK.
  - "Aavg (AC-3): 2.9 / 4.6 / 4.5 m²"; "Aavg (AC-11): 4.2 / 3.5 / 3.7 / 3.7 / 4.4 / 4.4 m²"; "block surface areas 7.0 / 8.9 / 12.4 m²" — OK, Tables 1–2, both languages.
  - "α &lt; 0.7 throughout; agreement between heights only above 1250 Hz" — OK, exact match both languages.
  - "α 'has physical meaning only for a flat sample ... not for a discrete absorber'" — OK, verbatim both.
  - "2 mm vs 4 mm frame rods made no appreciable difference"; "glass-cloth coating negligible effect / within accuracy limits" — OK, verbatim.
  - "final judgement by ISO 3745 1/R deviation" — OK, verbatim both: "The estimate of the results is determined by the value of the deviation from the 1/R law."
  - "BSFF wedges recommended and installed in PNRPU chamber (Fig. 11)"; "expected free field not lower than 200 Hz" — OK.
  - "PNRPU chamber dimensions 11.8 × 8.2 × 5.3 m" — OK, both languages.
- **Verified facts card**:
  - AC-2's own wedges achieve αn ≥ 0.99 above 100 Hz except at 160 Hz (0.978), yet the chamber is ISO 3745:2003-certified only for f &gt; 200 Hz: "Certification of the AC-2 AC according to ISO 3745:2003 showed that this chamber corresponds to the requirements imposed on ACs for a frequency range of f &gt; 200 Hz." (EN p.609) — a wedge nearly meeting the 0.99 criterion at a given band does not guarantee the chamber is free-field there.
  - No reliable conversion exists between normal-incidence (impedance-tube) and diffuse-field (reverberation-chamber) absorption values: "no reliable technique for converting one value into another exists" (EN p.607) (translated from Russian at source; English is the cited printing here).
  - Diffuse-field absorption results from different reverberation chambers are not directly comparable, even for the same wedge type — a reference sample had to be re-measured in both chambers to bridge them (EN p.610).
  - The flat-sample absorption coefficient α = A/S is not a valid figure of merit for a discrete (wedge) absorber: "the thus-defined sound-absorption coefficient has physical meaning only for a flat sample of a sound-absorbing material but not for a discrete absorber" (EN p.612).
  - Ultimate wedge-quality judgement is made by qualifying the finished, wedge-lined room per ISO 3745:2003 via 1/R-law deviation, not by any lab absorption metric (EN p.607).
  - Increasing wedge height increases absorption mainly by increasing surface area, not through a more favourable intrinsic mechanism (EN p.612).
  - For a flow (wind-tunnel-type) anechoic chamber, wedges must additionally survive non-stationary mechanical loading from return flows near the walls (EN p.609).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low — this is a wedge-material selection/measurement study for a large flow-through chamber under construction, not about rotor testing or reflection localisation; the one transferable point is that a chamber's advertised low-frequency limit must be verified by 1/R-law qualification of the finished room, not inferred from any single absorber-level metric.

---

## Friot &amp; Gintz 2009, arXiv:0911.4639 — Friot-Gintz_2009_arXiv_estimation-global-control-noise-reflections.pdf
- **Bibliographic check**: Title "Estimation and global control of noise reflections." Authors: Emmanuel Friot, Alexandre Gintz, CNRS, Laboratoire de Mécanique et d'Acoustique (LMA), Marseille. No year, journal/conference name, DOI, or page numbers are printed anywhere in the document body itself (only reference-list entries to *other* papers carry journal/year info) — "not printed in the text." The 2009 date and arXiv identifier 0911.4639 come from RETRIEVAL-B.md's retrieval record (the arXiv ID's YYMM prefix places the submission in November 2009), not from the document body. Filename is otherwise correct.
- **Claim audit**:
  - "usual rooms do not allow anechoic measurements below 50Hz" — OK, verbatim.
  - "time-windowing 'failed, mainly because at low frequency echoes from a scattering body are very difficult to separate from actuator responses'" — OK, verbatim (§2.B).
  - "dipole null-plane identification worked for rigid walls but the inversion process proved too ill-conditioned for absorbing walls; no filters could be identified" — OK, verbatim (including the source's own typo "proved to be to ill-conditioned").
  - "3-D experiment achieved ~10 dB average reduction of scattered pressure at 280 Hz" — OK, verbatim: "real-time control of the error signals led in average to a 10dB reduction of the scattered pressure" at the stated 280 Hz test frequency.
  - "about 3 transducers per wavelength needed → ~100 microphones and loudspeakers for 100 Hz in the 10×7×6 m room" — OK, verbatim, room stated as "10m x 7m x 6m."
  - "~1400 passive wedges in that room" — OK, verbatim.
  - "feedforward reference 'might be problematic for some primary sources such as aeroacoustic noise sources'" — OK, verbatim.
  - "duct control ineffective below 100 Hz (insufficient actuator authority) and above 750 Hz (second duct mode)" — OK, verbatim.
  - "global control fails at the resonance frequencies of the volume enclosed by the minimisation microphones" — OK, paraphrase matches source.
  - "cavity resonances have been largely reduced in the estimated direct pressure, indicating the scattered field was reasonably estimated" — OK, verbatim.
- **Verified facts card**:
  - Conventional rooms cannot support anechoic measurement below about 50 Hz, motivating active control of the residual wall reflection: "usual rooms do not allow anechoic measurements below 50Hz whereas such measurements would be desirable for many industrial noise sources or for validation of acoustic theoretical models."
  - Time-gating/windowing to separate a reflection from the direct sound specifically fails at low frequency because the actuator's own transient response overlaps the echo (§2.B).
  - A dipole source placed so its null plane sits at the sensor lets that sensor register reflected sound only, but this only works cleanly against rigid walls; absorbing walls suppress the null-plane signal too far below the noise floor (§2.B/4).
  - Real-time active cancellation of an estimated scattered field achieved about 10 dB average reduction at 280 Hz in a 3-D LMA anechoic-room experiment with 14 control channels (§3.B).
  - Scaling active wall-reflection cancellation down to 100 Hz in a 10×7×6 m room needs roughly 100 microphones and 100 loudspeakers, comparable in count to the room's ~1400 passive wedges (§4).
  - Global active control fails specifically at the resonance frequencies of the cavity volume enclosed by the ring/mesh of minimisation microphones, independent of the scattering-estimation method (§2.A).
  - A causal feedforward reference signal — required for real-time control — may not exist for some primary sources, explicitly including aeroacoustic noise; the fallback is post-hoc subtraction of the estimated scattered field rather than real-time cancellation (§5).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Low/indirect — this is an active-control method paper for cancelling wall reflections electronically, not a diagnostic for locating or interpreting a reflection with passive microphones; its one transferable point is the explicit warning that a causal feedforward reference is hard to get for an aeroacoustic (rotor) source, ruling out this class of active correction for a drone/propeller rig without a separate reference signal.

---

## Gallo, De Decker, Bresciani, Haezebrouck, Garone &amp; Schram 2025, Acta Acustica 9, article 16 — Gallo_2025_ActaAcustica_aeroacoustic-propeller-test-bench.pdf
- **Bibliographic check**: Title "Development and commissioning of an aeroacoustic test bench for the investigation of single and coaxial propeller noise." Authors: Erica Gallo, Julien De Decker, Andrea Bresciani, Pauline Haezebrouck, Emanuele Garone, Christophe Schram. *Acta Acustica* 2025, 9, 16. DOI 10.1051/aacus/2024085. Received 3 June 2024, accepted 18 November 2024. Filename is correct. MATRIX-3W.md's "Acta Acust. 9" omits the article number (16) — minor incompleteness, not an error.
- **Claim audit**:
  - "VKI 2.5×4.5 m + discharge room" — OK ("main room is 2.5 m × 4.5 m," "a discharge room, separated by a wall partition with a 1 m × 1 m opening," p.2).
  - "ISO 3745 to 150 Hz" / "commissioned according to the ISO:3745 standard [22], demonstrating free-field behavior down to 150 Hz for both broadband and tonal noise sources [23]" — OK, verbatim. Pre-existing internal inconsistency confirmed: the paper's own reference [22] is "ISO 3744" (a sound-power standard), not ISO 3745 — this is the source paper's own error, already correctly flagged in EXTRACTS-local.md, not a new finding.
  - "'the range of frequencies for which the room is practically anechoic (f &gt; 100 Hz)'" — OK, exact quote (p.6).
  - "propeller plane 1.80 m from it [wall partition]"; "auxiliary fan not run" — OK, both exact (p.2).
  - "GRAS 40PL mics"; "3-mic initial set plus a 24-mic traversing antenna (216 points)"; "30 s records at 51.2 kHz" — OK, all confirmed (24-sensor array × 9 traverse positions = 216 points; fs = 51,200 Hz).
  - "'The cooling system defines the background broadband noise for frequencies above 300 Hz. The motors add a tonal background noise'" — OK, exact quote (p.6).
  - "peaks at the 100 Hz shaft frequency 'presumably linked to slight asymmetries or misalignment'"; "Motor-to-propeller margin at 1st BPF &gt; 30 dB" — OK, both exact (p.6).
  - "spectrogram... 'does not reveal any rise in either tonal or broadband noise levels over time. Given the small size of the room, one would have expected to see a transient effect'" — OK, exact quote (p.7).
  - Attribution to wake turbulence "trapped" in the downstream room or recirculation time comparable to the 10 s RPM-stabilisation ramp — OK, both quoted elements verified (p.6–7), synthesised from two adjacent sentences rather than one continuous quote — acceptable paraphrase.
  - "Cooling air injection offsets the load cell"; "Coaxial phase not locked → repeatability checked over 10 s at one mic (Appendix B)"; "Reflections/standing waves: not discussed" — OK, all confirmed.
- **Verified facts card**:
  - Facility is two rooms (main test room + discharge room) linked by a 1×1 m wall opening, propeller wake vented into the discharge room (p.2, §2.1).
  - Room commissioned to ISO 3745 per the prose, but the paper's own reference list cites ISO 3744 for that citation — an internal inconsistency in the source itself (p.2, refs).
  - No recirculation rise seen over a 30 s acoustic run despite the room's small volume, with two candidate explanations offered: "Given the small size of the room, one would have expected to see a transient effect of the recirculating flow." (p.7, §3.2).
  - Cooling-air injection for thermal management measurably offsets the load-cell reading, requiring a calibration correction (p.3, §2.2).
  - Motor/cooling background is well separated from propeller tones: &gt;30 dB margin at the first BPF (p.6, §3.1).
  - Coaxial (contra-rotating) phase is not locked between the two rotors; the authors explicitly test for repeatability as a result (p.14, App. B).
  - Fairing decouples the load-cell reading from propeller-slipstream pressure/viscous loads on the outer wall (p.3, §2.2).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: High — this is a rotor-on-a-load-cell-stand rig in a small anechoic room (2.5×4.5 m) using a spectrogram-over-time check for recirculation, directly comparable in method and scale to SoundVisualizer's setup, though its microphones traverse a plane rather than sit on a fixed vertical arc.

---

## Garg, Surendran, Dhanya, Chandran, Asif &amp; Singh 2019, MAPAN – Journal of Metrology Society of India 34(3):357–369 — Garg_2019_MAPAN_microphone-free-field-calibration-uncertainty.pdf
- **Bibliographic check**: Title "Measurement Uncertainty in Microphone Free-Field Comparison Calibrations." Authors (exact order/initials as printed): N. Garg, P. Surendran, M. P. Dhanya, A. T. Chandran, M. Asif, M. Singh (CSIR-National Physical Laboratory, New Delhi + Fluid Control Research Institute, Palakkad). Received 2 July 2019, accepted 25 August 2019, published online 24 September 2019. DOI 10.1007/s12647-019-00343-7. Filename correct. Retrieval history: chamber-problems/README.md and RETRIEVAL-B.md record this paper as originally retrieved abstract-only, then the full PDF fetched by Adam on 2026-09-07; the txt file read here is confirmed full text (95 KB, six sections, Tables 1–6, references), not the superseded abstract file.
- **Claim audit** (none of Singh 2020's numbers were found misattributed to this paper anywhere in the brief; the "Predicting the chamber cut-off" bullet in §04a of docs/anechoic-chamber-problems-brief.html is correctly scoped to "Singh, Garg &amp; Narayanan," a different paper, and is out of scope for this entry):
  - Facility: "2 m³ transportable chamber, 0.35 m wedges" — OK (internal volume 2 m³, outer dims 2×2×2.4 m, wedges "of length 35 cm").
  - "125 Hz: +4.52 → −7.13 dB over 0.64–1.14 m" — OK, exact match to Table 2 (p.362).
  - "tolerance only 'between 79 and 89 cm'" — OK, exact quote (p.360).
  - "U = 0.36–0.52 dB" — OK, exact (abstract and p.365: "±0.36 dB to 0.52 dB").
  - 160 Hz +2.03→−2.57 dB, 250 Hz +0.97→−2.47 dB — OK, Table 2.
  - Radial 1 cm sphere at 0.84 m (max 0.5 dB at 12.5 kHz top, 0.4 dB at 125 Hz/0.83 m, ≤0.2 dB 250–8000 Hz); 1×5 cm cylinder at 86.5 cm (0.63 dB right/125 Hz, 0.58 dB centre/125 Hz, 0.30 dB at 1 kHz, &lt;0.30 dB elsewhere) — OK, exact, pp.361–362.
  - Position sensitivity 0.035/0.024/0.02 dB/mm, ±1 mm contribution 0.05/0.03/0.026 dB — OK, exact, pp.363–364.
  - Air attenuation 0.0004–0.0011 dB (Table 4); Monte Carlo 2×10⁵ trials agreeing to 0.03 dB (Table 6); validation &lt;0.16 dB (B&amp;K 4180) and &lt;0.25 dB (B&amp;K 4191) — OK, all exact.
  - "The entire 1.09 m column of Table 2 sits ~−0.8 to −1.3 dB below its neighbours... not commented on in the text" — OK as an editorial observation (pattern confirmed present, correctly labelled as unexplained by the paper itself, not a paper claim).
- **Verified facts card**:
  - Chamber's theoretical lower cut-off is 250 Hz, derived from geometry and lining, distinct from any measured value: "The lower cut-off frequency of this chamber derived in theory from its dimensions and the characteristics of the materials used for lining the chamber is 250 Hz." (p.358–359, §2.1).
  - The 125–630 Hz band deviation table shows a working space of only 10 cm (0.79–0.89 m) meeting ISO 26101 tolerance: "the axial working space between 0.79 and 0.89 m truly complies with the free-field requirements." (p.360, §3.1).
  - Below cut-off, the room "deteriorates gradually" rather than failing sharply, with reflections attributed to falling wall absorption at low frequency: "In the frequency range of 125–250 Hz, the acoustical properties of the room deteriorate gradually... some reflections from the walls may occur due to reduction in sound absorption coefficient of the wall lining at lower frequencies." (p.364, §4.1).
  - Positioning/acoustic-centre uncertainty is frequency-dependent and largest at the lowest frequency (125 Hz) (p.363–364, §4.1).
  - Radial (off-axis) sensitivity around the working point stays small (≤0.63 dB) across 125 Hz–20 kHz, supporting the chosen reference point (p.362, §3.2).
  - Two independent uncertainty-evaluation methods (GUM/LPU and Monte Carlo) agree to within 0.03 dB (p.368, §4.2; Table 6).
  - Final calibration is externally validated against a second facility's values, bounding total systematic error: "the deviation is observed to be less than 0.16 dB in the entire measurement frequency range" (B&amp;K 4180) (p.368, §5).
- **Relevance to a small chamber with a rotor on a stand and a vertical microphone arc**: Indirect but useful — this is a static microphone-calibration chamber, not a rotor rig, but its method (mapping inverse-square-law deviation versus distance and frequency to define a narrow usable working space, only 10 cm wide at 125 Hz) is a directly transferable diagnostic for finding where a small chamber's free-field envelope actually lies before trusting directivity data from it.

---

# Summary of the most serious errors found

1. **`docs/reflection-localization.html`'s evidence ledger is stale.** It lists Sun 2012 and Mabande 2013 as "Not retrieved — need the PDFs," but both were fully read on 2026-09-07 (full PDFs + `pdftotext` extracts sit in `papers/reflection-localization/`, and `MATRIX-3W.md` itself records "each read in full, 2026-09-07"). The ledger's own claim that "the accuracy figures quoted for tier 3 come from Lovedee-Turner alone rather than from a body of work" is therefore also wrong — Sun 2012 and Mabande 2013 independently corroborate single-array reflection localisation to a few degrees/centimetres.
2. **The same html's TIER-3 and §04 numbers for Lovedee-Turner-Murphy 2019 mix simulated and measured results.** "11.5–18.9 cm measured" is actually Table II's *simulated* L-shaped-room CATT data (Scenario Two); the paper's one real measured result (Table III) is a single RMS of 15.37 cm. "Accuracy degrades sharply — 16 to 25 cm — once the room stops being convex" is not supported at all: the paper's other non-convex room (L-shaped) scores 4.69 cm, as good as the convex ones, and the ~25 cm figure traces to an individual-wall error in the *convex* real room, not a non-convex one.
3. **Amiet 1981 (NASA CR-3371) is misattributed by author throughout the corpus.** Every existing citation (`RETRIEVAL-A.md`, the chamber-problems brief's evidence ledger, the filename itself) calls it "Amiet 1981," but the report's own title page and Report Documentation Page list the authors as **Robert H. Schlinker and Roy K. Amiet** — the same pair, same order, as the companion `Schlinker-Amiet_1978` report. The Report Documentation Page also prints "Report Date: December 1980" (not 1981; 1981 is the NTRS catalogue/accession year) and "No. of Pages: 189" (not the "192 pp" used to describe it elsewhere).
4. **Mabande 2013's own Table VIII/Table IX numbers don't fully support one existing summary claim.** "TDOAs 3.6/3.9/24.4 ms matched exactly" is only two-thirds right: the 3.9 ms ground-truth reflection was actually estimated at 3.8 ms (RMVDR) or 0.9 ms (EB-DAS) — none of the three estimators hit 3.9 ms exactly. A separate quote ("walls...estimated precisely up to a few centimeters") was also mis-cited to p. 2789 (the reference list) instead of its actual location, pp. 2786–2787.
5. **A genuine 230 vs 210 m³ discrepancy between the two printings of Belyaev et al. 2015 is confirmed real**, not an extraction artefact: the English (Acoustical Physics) translation prints AC-11's reverberation-chamber volume as 230 m³ where the Russian original (Akusticheskii Zhurnal) prints 210 m³. The Russian, as the original-language publication, is authoritative.

Everything else audited — Hadadi 2024, Sprunck 2022, ISO 26101-2:2024, Meyer-Kahlen 2022, Alkmim 2022, Fasulo 2025, Bahr-Hutcheson-Stead 2020, Bahr 2021, Friot & Gintz 2009, Gallo 2025, Garg 2019, Tervo 2013 (aside from two page-number slips), and Sun 2012 — checked out clean: every other numeric value, page/section reference, and verbatim quote in the existing matrices, extracts, and both HTML documents matched the source text.
