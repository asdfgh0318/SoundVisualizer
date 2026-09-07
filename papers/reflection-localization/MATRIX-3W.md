# Reflection-localization literature matrix (three-way scan: WHY / HOW / WHAT)

Source texts: `papers/reflection-localization/txt/` (8 files, each read in full, 2026-09-07).
Themes scored S (supports) / C (contradicts) / P (peripheral) / — (not addressed):

- **T4** Ground/floor reflection distorts tonal levels and directivity
- **T6** Locally-reacting admittance or α alone is insufficient at low frequency; phase-preserving models needed
- **T7** Discontinuities and fixtures are the dominant practical reflectors
- **T10** A single strong reflection can be localised from array data with practical accuracy once a chamber fails qualification

Evidence level: III = controlled measurement with ground truth; VI = simulation-only or single case; VII = standard/expert.
Quality: A peer-reviewed full method + numbers; B conference/report with numbers; C preview/sample; D insufficient.

---

### Sun 2012, J. Acoust. Soc. Am. 131(4):2828–2840 — jasa2012_sun_spherical_array_reflection_localization.txt
- Type: journal
- WHY: Localise an unknown broadband source and its dominant early reflections from a single recording with a compact off-the-shelf spherical array (no RIR, no source reference), and decide which eigenbeam (EB) method — EB-DAS, PWD, EB-MVDR, EB-MUSIC, EB-ESPRIT — is robust enough for practice.
- HOW: Eigenmike, 32 mics on rigid sphere a = 0.042 m, order N = 4, 44.1 kHz, white Gaussian noise via loudspeaker; two shoebox rooms (T60 ≈ 900 ms and ≈ 400 ms, height 3.03 m), array at 1.41 m height. Focusing frequency 4.5 kHz (k0a = 3.5), frequency-smoothing range 3.2–4.5 kHz (ka ∈ [2.5, 3.5]), FFT 1024, 1° acoustic-map grid, WNG constraint 0.6 dB. SNRs 5 dB (room 1) and 3 / 17 dB (room 2); one parameter set for all cases. Ground-truth DOAs from measured geometry fed to CATT.
- WHAT: EB-MVDR with frequency smoothing + WNG control resolves direct sound plus five first-order reflections and one second-order (walls 2+3) in room 1. Angular deviations (Table V, room 1, FS+WNGC): direct 2.0°, ceiling 1.6°, floor 3.3°, wall 2 2.2°, wall 3 4.1°, wall 4 6.1°, walls 2+3 3.0°. Room 2 (Table VI): direct 2.0°, floor 1.0°, walls 3.6 / 2.2 / 3.1°; ceiling not localised at all. Eight loudspeaker positions (Table VII, SNR 5 dB): three strongest reflections within 1.0–5.1°. SNR sweep (Table VIII): 3 dB → 1.0 / 3.6 / 2.2 / 3.1°; 17 dB → 1.0 / 2.6 / 1.2 / 2.0°. EB-ESPRIT localises only direct + one reflection (~3°). Verbatim: "Up to six coherent sources, namely the direct-path sound and five first-order reflections can be well localized using the EB-MVDR with frequency smoothing and WNG control." (Sec. V, p. 2835). Also: "the DOA-estimation deviation of reflected signals is larger than that of the direct sound signal, since the SNRs of reflected signals are much lower than for the direct sound, and some boundary surfaces in the rooms are not perfect reflectors." (Sec. V, p. 2837). Ceiling failure: "The ceiling in room 2 is not regular and it has several lights with quite large reflecting surfaces. Therefore, the localization results for the ceiling are all far from the ground truth values." (Table IV footnote d, p. 2839).
- Themes:
  - T4: P — floor reflection localised (1.0–3.3°) but its effect on levels/directivity not analysed.
  - T6: — — DOA only in a 3.2–4.5 kHz band; no boundary-impedance or phase modelling.
  - T7: P — ceiling lights with large reflecting surfaces destroyed ceiling localisation (footnote d); fixtures as confounder, not shown dominant.
  - T10: S — one compact array, one recording, reflections to 1–6° at 3–17 dB SNR in T60 0.4–0.9 s shoebox rooms; ground truth is CATT prediction from measured geometry.
- Evidence level: III
- Quality: A

---

### Mabande 2013, J. Acoust. Soc. Am. 134(4):2773–2789 — jasa2013_mabande_room_geometry_inference.txt
- Type: journal
- WHY: Infer full 3D room geometry (positions and orientations of boundary planes) from uncontrolled broadband signals (noise or speech) captured by one compact spherical array, without measuring RIRs; the challenge is low reflected-signal SINR and strong coherence between direct sound and reflections.
- HOW: Two-stage: (1) DOAs from steered EB-RMVDR acoustic image (focusing 4.5 kHz, smoothing 1.3–4.5 kHz i.e. ka ∈ [1, 3.5], WNG ζ = 1.148 = 0.6 dB, 1° grid, peaks kept only if in upper two-thirds of image power range); TDOAs by cross-correlating frequency-dependent EB-RMVDR-extracted direct and reflected signals with an adaptive zero-lag exclusion b. (2) Image-source geometry from known source distance/DOA, plane categorisation across J source positions (dot-product masking), least-squares plane fit, post-processing for highly reflective walls. Eigenmike 32 mics, a = 0.042 m, N = 4, 5 s signals, 44.1 kHz, Q = 1024 bins (~43 Hz). Simulated image-source shoebox (229.32 m³, α = 0.5–0.9, SNR 10–30 dB, open and rigid sphere, plus 240-mic a = 0.111 m array, N = 10) and a real lecture room T60 ≈ 900 ms, height 3.03 m, J = 4, loudspeaker 0.08 m diaphragm, 22.8 °C. Real-room SNR stated as 12 dB in text and figure captions but "SNR = 15 dB" in the Table IX header (inconsistent in text).
- WHAT: Simulation, J = 4, SNR 30 dB, α = 0.7: mean orientation deviation 1.6°, mean distance deviation 1.52 cm, relative volume error 0.35% (Table II). J = 1: only 5 of 6 planes (P1 unresolvable, reflection too close in angle to direct path). SNR 10 dB: 5 of 6 planes, 6.1° / 5.11 cm; SNR 20 dB: 1.9° / 2.24 cm / 0.90% (Table III). α = 0.9 (wood panelling): 5.8° / 2.14 cm, spurious higher-order planes (Table IV). Large array: 0.6° / 1.38 cm (Table V). Speech: 2.4° / 1.08 cm / 1.36% (Table VI). Real room (Table VIII/IX): DOA deviations 1.0–5.0°, TDOAs 3.6 / 3.9 / 24.4 ms matched exactly; noise 2.4° / 1.04 cm / 0.23% volume error, speech 3.2° / 1.44 cm / 0.21%; three reflections localised from one position. EB-DAS extraction gets the weakest TDOA wrong (0.9 vs 3.9 ms). Verbatim: "The positions of the walls, even in large acoustic enclosures, are estimated precisely up to a few centimeters only." (Sec. VIII, p. 2789). "the errors in boundary plane estimation are mainly due to the errors in the DOA estimation, which substantially influence the orientation of the boundaries" (Sec. VII C 5, p. 2784).
- Themes:
  - T4: P — floor/ceiling planes P5/P6 located (0.2° / 0.16 cm sim; 1.3° / 0.28 cm real) but no level-distortion discussion.
  - T6: — — specular, frequency-independent reflection assumed; only scalar α varied.
  - T7: — — pillars of the real room neglected; piecewise-planar convex rooms only.
  - T10: S — one compact array; real room at 12 dB SNR, T60 0.9 s gives reflectors to 1–5° DOA and ~1–2 cm plane distance; needs known source distance and DOA, several source positions for all walls.
- Evidence level: III
- Quality: A

---

### Tervo 2013, J. Audio Eng. Soc. 61(1/2):17–28 (Jan/Feb 2013; file labelled 2012) — tervo2012_spatial_decomposition_method.txt
- Type: journal
- WHY: Encode a spatial room impulse response as a set of image-sources (pressure sample + 3D location per sample) using any compact array with few microphones, so that room-acoustic analysis and multichannel convolution reverb are not tied to a specific array or reproduction technique.
- HOW: Spatial Decomposition Method (SDM): per discrete time step, TDOAs from generalized cross-correlation with exponential-fit interpolation, least-squares slowness vector m̂ = V⁺τ̂ under a plane-wave model, direction n̂ = −m̂/‖m̂‖, distance c·k·Δt; pressure from the centre omni mic. Requirements: ≥4 non-coplanar mics, one omni, array not larger than a head, window L·Δt > 2·dmax/c. Echo-density limit τ1 ≈ 0.0014·√V for one reflection per window. Evaluation: 7-mic open array (6 on a sphere, spacing 100 mm, plus centre), 1.33 ms Hann window, 99% overlap, 48 kHz; image-source simulations of a 30×20×12 m room (RT 2.0 s) and a 5×3×2.8 m room (RT 0.4 s), reflection coefficient 0.85, 45th order; VBAP over 14 loudspeakers; 17 listeners compared SDM to SIRR (7 and 13 mics).
- WHAT: No localisation error in degrees or cm is reported. Fig. 3 (simulated 20×30×12 m room): "The image-sources with the highest energy are correctly analyzed." (Fig. 3 caption, p. 21). 1 ms window keeps one event per window until 119 ms after the direct sound in 7200 m³; in the small room τ1 = 1.4 ms, so the 1.33 ms window is already marginal. Listening-test similarity means: reference 0.98, SDML7 0.80, SIRR13 0.48, SIRRL7 0.40, anchor 0.00; SDM not significantly different from the reference for speech and trombone in the large room. Verbatim on limits: "as the time progresses the number of acoustic events per time window increases, and eventually more than one reflection arrives during the time window. In this case, a cross-correlation-based localization algorithm localizes the sound to the location of the reflection that is the strongest one in that time window." (Sec. 1.4, p. 21). "The accurate localization of first acoustic events with respect to time in the impulse responses, i.e., the direct sound and the first reflections, is possible as shown in [24] and [18], respectively." (Sec. 1.4, p. 21).
- Themes:
  - T4: — — no floor-specific analysis.
  - T6: P — notes reflections are time-spread with a boundary-absorption frequency response; band-wise analysis left as future work.
  - T7: P — edge diffraction admitted as modellable by weighted image-sources; no claim about dominance of fixtures.
  - T10: S (qualitative) — the strongest reflection in each window is what SDM localises with a 4–7 mic compact array; accuracy in degrees (unclear in text); simulation only.
- Evidence level: VI
- Quality: B — peer-reviewed, but reflection-localisation accuracy is not quantified; numbers are perceptual similarity and echo-density bounds.

---

### Meyer-Kahlen 2022, ICA 2022 Proceedings (Gyeongju; Acoustical Society of Korea) — sdm_can_and_cannot_do.txt
- Type: conference
- WHY: Reconcile divergent reports on SDM ("graininess", poor results in some comparisons) by stating explicitly what the analysis and rendering stages can and cannot do, and give practical guidance.
- HOW: Position paper with illustrative simulations. Analysis: TDoA (open array ≥4 omnis, interpolated cross-correlation, Nmin = 2·fs·dmax/c) versus pseudo-intensity vector PIV (FOA/tetrahedral, band-limited below spatial-aliasing frequency fsa = c/(2πr)). Tests: two plane waves Δt = 0.05 ms, 6 dB level difference, 0.5 ms window (Fig. 3); anisotropic diffuse field of 180 Gaussian noise sources (Fig. 4; arrays printed as "r = 125 cm", likely a typographic loss of the decimal point — unclear in text). Rendering: nearest-loudspeaker synthesis, Ambisonics encoding, binaural; roughness compensation with Schroeder allpass cascade M = 37, 113, 215; block-wise equalisation against whitening.
- WHAT: Direct sound and floor/ceiling reflections are "easily visible" in SDM energy plots (Fig. 2 caption). Two events inside one analysis block cannot be separated: TDoA returns the direction of the largest peak, PIV a weighted mean; temporal resolution is set by array size, and raising the sampling rate does not help. Late-field directional distribution is followed "only to some extend". No numeric DoA accuracy given (unclear in text). Verbatim: "directional analysis fails if two sound events occur simultaneously, wherein it is important to note that simultaneously does not mean that the sound events need too occur within one sampling interval, but within one analysis block." (Sec. 3.3). "the broadband analysis stage of SDM is a robust way to identify reflections in the early part of the response, but that the temporal resolution is limited by the size of the used microphone array, regardless of the estimation method." (Sec. 5).
- Themes:
  - T4: P — floor and ceiling reflections shown as clearly identifiable; no level/directivity distortion analysis.
  - T6: — — no boundary-impedance content.
  - T7: — — not addressed.
  - T10: S (qualitative) — a single dominant early reflection is exactly the case SDM resolves; fails when two arrive within 2·dmax/c; accuracy in degrees (unclear in text).
- Evidence level: VI
- Quality: B

---

### Lovedee-Turner 2019, J. Acoust. Soc. Am. 146(5):3339–3352 (accepted manuscript, White Rose eprint) — lovedee_turner_murphy_3d_reflector_localisation.txt
- Type: journal
- WHY: Localise reflective boundaries and infer geometry for convex and non-convex rooms from few spherical-array SRIRs, with explicit error management for false and higher-order detections, which prior methods lacked.
- HOW: EDESAR detection: third-order SH SRIR, 0.45 ms frames with 50% overlap, Hann window, band-pass 100 Hz–5 kHz (Eigenmike spatial Nyquist 8 kHz), frames discarded if peak < εa = 0.01 or COMEDIE diffuseness > εd = 30%; MVDR (measured) or PWD (simulated) directional spectrum on a 1° grid; watershed image segmentation to split overlapping regions; DoA from summed spectrum, ToA from beam steered to DoA; 80% region-overlap rule across frames. E-ARC inference: image-source reversion with previous-source search (εes = 30 cm, εO = 15 cm), then reflection-path, line-of-sight and closed-geometry validation. Assumptions: known source distance and temperature, ≥50 cm from boundaries, parallel floor/ceiling, walls perpendicular. Scenarios: CATT simulations (10⁷ rays, WOOD30, diffuse off) of cuboid, octagonal, L and T rooms with 2–3 positions; two L-rooms (320, 360 m³) with 33 source combinations each; real cuboid 10.35 × 13.29 × 4.19 m with Eigenmike EM32 and Genelec 8030, 20 s sweep 100 Hz–20 kHz averaged over four speaker orientations, noise floor 60.2 dBA, 24.4 °C (c = 346.97 m/s), fixed curtains and ceiling piping/railing present.
- WHAT: Simulated RMS boundary position / dihedral angle (Table I): cuboid 4.63 cm / 8.59°, octagonal 2.69 cm / 2.01°, L 4.69 cm / 14.02°, T 16.45 cm / 8.03°. L-room sets (Table II): 11.50 ± 0.1 cm / 7.28°, 18.91 ± 0.17 cm / 3.69°, per-set ranges 3.95–35.58 cm. Real room (Table III): RMS 15.37 cm, 1.21°, 23.02 cm length; walls 4.02–25.46 cm, floor 14.5 cm, ceiling 10.60 cm. Prior cuboid-only work: 0.063–29.38 cm using 6–64 positions versus ≤3 here. Verbatim: "The RMS boundary position errors are comparable to prior work with a maximum difference in RMS error of 16.38 cm, using at most three measurement positions, compared to 6-64 used in this prior work." (Sec. VII). Real-room caveat: "the ceiling was covered in large metal piping connected to extractor fans and a layer of metal railing approximately 1 m from the ceiling." (Sec. IV). Error attribution: "inaccuracies are likely due to either imperfect specular reflections, under or over estimation of the ToA for reflections in the measured impulse responses, or any inaccuracy in the estimated DoA" (Sec. V C).
- Themes:
  - T4: P — floor and ceiling localised (14.5 / 10.6 cm real) but no analysis of level distortion.
  - T6: — — frequency-independent reflection assumed in the SRIR model (Eq. 1).
  - T7: P — curtains, ceiling piping and railing named as confounders in the real measurement; not shown to dominate.
  - T10: S — one spherical array, ≤3 positions: real cuboid boundaries to 4–25 cm (RMS 15 cm) and 1.2° dihedral; simulated 2.7–16 cm; requires known source distance, ≥50 cm clearance, specular boundaries.
- Evidence level: III
- Quality: A

---

### Hadadi 2024, arXiv:2409.15484 (preprint, BGU / Meta Reality Labs) — blind_localization_early_reflections_arbitrary_array.txt
- Type: report (preprint)
- WHY: Blindly estimate DoA and delay of early reflections with no RIR or source knowledge, for arbitrary arrays including wearables; characterise FF-PHALCOR's misses and false alarms versus reflection delay, amplitude and density, and test the perceptual value of the estimates.
- HOW: FF-PHALCOR: frequency focusing T(f, f0) from pseudo-inverse of steering matrices (900 Fliege-Maier DoAs), phase-aligned spatial correlation, rank-1 SVD per delay, OMP for reflection DoAs, DBSCAN clustering plus proposed k-means sub-clustering (threshold 0.25). Monte Carlo: 300 scenes in four shoebox rooms (6×4×3 to 12×9×5 m, T60 0.62–1.22 s, 7.9–25.6 reflections in first 20 ms), source–array 0.7–1.7 m, DRR −10…10 dB, speech at 16 kHz, STFT 150 ms Hann 75% overlap, 500–5000 Hz in 2 kHz bands, order N = 8; arrays: em32-like 32-mic sphere and 6-mic semi-circular open array. True positive if within 0.5 ms and 15°. MUSHRA with 16 listeners in a 12×7×5 m, T60 = 0.57 s room, RIR truncated at 20 ms, KU-100 HRTF.
- WHAT: PD falls as the number of reflections within 20 ms rises; semi-circular PD significantly below and PFA above em32 (values only in Fig. 2; unclear in text). Reflections with amplitude ≥ 0.4 of the direct sound are easier to detect; those later than ~10 ms are harder and generate more false alarms; up to 15% of misses due to multi-reflection clustering at 28–32 reflections; sub-clustering raises PD without raising PM; azimuth-only estimation cuts PFA for the semi-circle (up/down ambiguity). Listening-test scene: spherical PD = 1, semi-circular PD = 0.85, both PFA = 0.4; RM-ANOVA F(3,45) = 54.04, p < 0.001; spherical estimate not significantly different from reference (p = 0.057), semi-circular significantly worse. Verbatim: "reflections with high amplitudes, i.e. 0.4 with respect to the direct sound or higher, are easier to detect." (Sec. IV D). "reflections that appear later, i.e. 10 ms with respect to the direct sound, are harder to detect." (Sec. IV D).
- Themes:
  - T4: — — floor not singled out.
  - T6: — — reflections modelled as attenuated, delayed replicas; no impedance content.
  - T7: — — shoebox simulations only.
  - T10: S (blind, simulation) — strong (≥0.4 amplitude), early (<10 ms) reflections detected within 15° / 0.5 ms tolerance by a 32-mic sphere; 6-mic semi-circle suffers up/down ambiguity; numeric PD only in figures.
- Evidence level: VI
- Quality: B

---

### Sprunck 2022, arXiv:2208.14017v2 (preprint, Inria / Strasbourg / Cerema) — gridless_3d_recovery_image_sources.txt
- Type: report (preprint)
- WHY: Recover continuous 3D positions and amplitudes of image sources from a discrete, band-limited multichannel RIR without a spatial grid, avoiding the cubic grid growth, peak-overlap and basis-mismatch limits of existing methods.
- HOW: Convex relaxation (BLASSO) over Radon measures with a new linear operator from the wave-equation Green's function convolved with the microphone response; adapted Sliding Frank-Wolfe with grid-on-spheres initialisation (~40k points), BFGS refinement, λ = 3·10⁻⁵, spikes < 0.1 dropped. 200 random shoebox rooms (L, W ∈ [2, 10] m, H ∈ [2, 5] m, wall absorption 0.01–0.3), one omni source and one 32-mic open sphere in em32 geometry scaled ×2 (d = 16.8 cm), fs = 16 kHz, Tmax = 50 ms (all image sources within 17.15 m), sinc microphone filter, pyroomacoustics ground truth, c = 343 m/s. Recovered if within 2° and 1 cm of the array centre.
- WHAT: Table I (noiseless): 0–150 image sources recall 94.3%, precision 81.8%, radial error 0.069 mm, angular 0.38°, Euclidean 94 mm, amplitude 0.042; 150–300: 92.1% / 83.1% / 0.099 mm / 0.36°; 300–500: 86.1% / 78.1% / 0.151 mm / 0.38°; 500–1323: 57.3% / 51.6% / 0.300 mm / 0.46°. Only 3 of 1200 first-order image sources missed; all 200 true sources found. fs = 32 kHz or d = 42 cm gives near-100% recall up to 500 sources; PSNR 40 dB harmless, < 30 dB degrades, at 30 dB recall recovers with a 6° threshold. Previous best (blind, [24]): ~25 nearest image sources at 4.3° mean angular error. Verbatim: "The strength of the proposed gridless approach is revealed by the mean radial and angular errors, which are below tenths of millimeters and fractions of degrees." (Sec. V). Caveat: "applying the method to real data will require a number of challenging extensions. Indeed, real RIRs are impacted by the frequency and angular dependencies of source, microphone and wall responses." (Sec. VI).
- Themes:
  - T4: — — floor not distinguished from other walls.
  - T6: P — authors state frequency-dependent wall responses are missing and require a Fourier/SH-domain reformulation with frequency-dependent amplitudes.
  - T7: — — cuboid rooms only; occlusions deferred.
  - T10: S (idealised simulation) — first-order image sources from one compact array to < 1 mm radial and < 0.5° angular; requires PSNR ≥ 30 dB, frequency-independent walls, no real-data validation.
- Evidence level: VI
- Quality: B

---

### ISO 26101-2:2024 (ISO/TC 43/SC 1; iTeh preview sample) — iso26101-2-2024_environmental_correction_sample.txt
- Type: standard (preview sample: front matter, Scope, Clauses 2–4 and 5.1 only)
- WHY: Qualify a test environment that approximates a free field near one or more reflecting planes by determining the environmental correction K2, needed for sound-power (ISO 3744/3746) and emission-sound-pressure (ISO 11201/11202/11204) determinations.
- HOW: Four procedures: absolute comparison test with a reference sound source (Clause 5, preferred, indoors or outdoors, "expected to yield the most accurate results in typical industrial environments"); room-absorption methods (Clause 6: reverberation time, two-surface, RSS direct), assuming an approximately cubic, substantially empty room absorbing only at boundaries; inverse-square-law qualification of parallelepiped/cylindrical measurement surfaces in hemi-anechoic rooms with goal K2 = 0 (Clause 7, "the most accurate method"); approximate estimate of equivalent absorption area A (Clause 8, least accurate). Flowchart Figure 1. Numeric criteria (7.2.2 maximum deviations, 7.2.4 volume, Annex A uncertainty) are outside the sample (unclear in text).
- WHAT: K2 corrects energy-averaged surface levels for reflected or absorbed sound, is frequency dependent (K2f per band, K2A overall) and "usually K2 increases with S" (3.3 Note 3, p. 2). Verbatim: "In some industrial buildings, which are of low height and have reflecting surfaces, the sound propagation can be distorted. In these conditions, the qualification procedures according to Clause 6 and Clause 8 might not be applicable." (4.5 NOTE, p. 3). "In hemi-anechoic rooms, the other qualification procedures can yield unreliable results." (4.4 NOTE, p. 3). No localisation of individual reflections is defined; K2 is a global correction.
- Themes:
  - T4: P — entire scope is correcting for reflecting planes, but the sample gives no tonal or directivity numbers.
  - T6: — — no boundary-impedance content in the sample.
  - T7: P — low-height buildings with reflecting surfaces flagged as distorting propagation; fixtures not named.
  - T10: — — defines qualification and a scalar correction, no reflection-localisation procedure.
- Evidence level: VII
- Quality: C
