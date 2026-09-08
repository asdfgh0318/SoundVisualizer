# Thread E — naming the surface: locating a reflector with a loudspeaker and the 11-mic arc

Compiled 2026-09-08. Scope: replacing the propeller with a small loudspeaker, measuring impulse
responses at all 11 arc mics, and reading the extra path of a reflection from the delay of the
second arrival, given that the UMIK-2s are independent-clock USB devices aligned only by a
trigger onset (uncertain to a fraction of a millisecond). Every quote below was read from a plain
`pdftotext -q` dump (held papers re-extracted fresh into `papers/arc-validation/refetch-txt/`; new
papers into `papers/arc-validation/txt/`), not from the earlier `EXTRACTS`/`MATRIX-3W` notes or
from memory. Page numbers are the PDF's own printed page/footer where the document has one;
where a PDF's page markers could not be resolved unambiguously from the text layer (noted case
by case), a "PDF p. N of M" physical-page index is given instead.

---

## Sources

### 1. Farina, A. (2000). "Simultaneous Measurement of Impulse Response and Distortion with a
Swept-Sine Technique." AES 108th Convention, Paris, preprint 5093 (D-4).

- **File:** `Farina_2000_AES108_swept-sine-impulse-response-distortion.pdf` /
  `txt/Farina_2000_AES108_swept-sine-impulse-response-distortion.txt`
- **Route:** live site `pcfarina.eng.unipr.it` is currently down (confirmed: DNS resolves, TCP
  connect refused/timed out on 80 and 443); recovered via the Wayback Machine snapshot
  `https://web.archive.org/web/20031228231709id_/http://pcfarina.eng.unipr.it/Public/Papers/134-AES00.PDF`.
- **Evidence level:** conference (AES convention preprint, not peer-reviewed at the time, but the
  foundational reference for the exponential-sine-sweep technique — near-universally cited).
- **Identity:** confirmed from p. 1, title/author/venue exactly as cited above.
- **What it says (with numbers):** an exponentially-swept sine ("log sweep"), deconvolved with its
  time-reversed mirror (linear, not circular, convolution), yields the system's linear impulse
  response *and* pushes every harmonic-distortion order into its own, separate, clean impulse
  located at a fixed time **before** t=0 (before the linear IR). For a log sweep from ω1 to ω2 over
  duration T, the harmonic of order N appears at
  **Δt = T · ln(N) / ln(ω2/ω1)**
  before the linear response (p. 6) — Δt is constant for a given N (so distortion orders don't
  smear), and increases only logarithmically with N (so higher orders crowd closer together, the
  opposite of what intuition suggests). A single long sweep gives an S/N improvement of "60 dB or
  more" versus a single impulse of the same peak amplitude (p. 6). MLS, by contrast, "requires that
  the excitation signal is tightly synchronised with the digital sampler employed for recording the
  system's response" (p. 1) and is "quite delicate" under nonlinearity or time-variance (p. 1).
- **Verbatim quotes:**
  - "In particular MLS is quite delicate, it does not tolerate very well nonlinearity or
    time-variance, and requires that the excitation signal is tightly synchronised with the digital
    sampler employed for recording the system's response." (p. 1)
  - "Furthermore, the system revealed to be very robust to minor time-variance of the system under
    test, and to mismatch between the sampling clock of the signal generation and recording." (p. 1)
  - "What is not widely known is that also not-linear behavior of the system (i.e., harmonic
    distortion) can cause time aliasing artifacts... at various positions of the deconvolved impulse
    response strange peaks do appear... they resemble scaled-down copies of the principal impulse
    response." (p. 3)
  - "the distortion products simply pack always at a very precise time lag before the linear
    response." (p. 6, paraphrasing the sonograph description that leads into the equation — the
    exact printed sentence is: "It must be noted that the value of ∆t is constant, and this ensures
    that each harmonic order will pack always at a very precise time lag before the linear response.
    Furthermore, ∆t increases with the logarithm of N, and this means that the delay between each
    harmonic response and the previous one is not constant, but the higher orders are less spaced.")
    (p. 6)
  - "The preferred technique is to employ a single, very long, logarithmic sine sweep: this produce
    a distortion-free linear response, well separated harmonic distortion responses up to very high
    orders... obtaining usually a S/N improvement of 60 dB or more in comparison with the generation
    of a single impulse having the same maximum amplitude." (p. 6)
  - Loudspeaker enclosure/decay requirements: **not discussed anywhere in this paper** — searched
    for "decay", "resonance", "port", "enclosure", "box", "reflex", "closed-box"; the only source
    named is a "dodechaedron" loudspeaker (Look Line D1) with no enclosure/decay discussion.

### 2. Farina, A. (2007). "Advancements in impulse response measurements by sine sweeps." AES
122nd Convention, Vienna.

- **File:** `Farina_2007_AES122_advancements-impulse-response-sine-sweeps.pdf` /
  `txt/Farina_2007_AES122_advancements-impulse-response-sine-sweeps.txt`
- **Route:** same live-site outage; recovered via Wayback
  `https://web.archive.org/web/20111012083635id_/http://pcfarina.eng.unipr.it/Public/Papers/226-AES122.pdf`.
- **Evidence level:** conference (AES convention paper, "selected on the basis of a submitted
  abstract and extended precis that have been peer reviewed by at least two qualified anonymous
  reviewers" per its own cover sheet).
- **Identity:** confirmed p. 1, title/author/venue as cited. Note: this paper's own reference list
  mis-cites the 2000 paper as the "110th AES Convention" — the 2000 paper's own title page is
  unambiguous ("108th Convention"), so this is Farina's self-citation slip, not a real ambiguity.
- **What it says — this is the single most load-bearing paper for the thread's central problem
  (independent-clock mics):**
  - **Bandwidth ↔ time resolution (Sec. 3.1 "Pre-ringing", p. 5):** deconvolving the test signal
    against itself with zero system under test should give "a theoretically-perfect Dirac's delta
    function"; instead the peak "is in reality some sort of Sync [sinc] function, and it shows a
    number of damped oscillations both before and after the main peak. This is due to the limited
    bandwidth of the signal (22 Hz to 22 kHz, in this case)... These two factors define
    substantially a trapezoidal window in the frequency-domain, which becomes the Sync-like
    function in time domain." (p. 5). **This is the direct answer to the bandwidth/resolution
    question**: the achievable temporal resolution of a deconvolved arrival is set by the sweep's
    (or any wideband signal's) bandwidth, appearing as a sinc-shaped pulse of main-lobe width
    roughly 1/bandwidth — for a full-audio-band 22 Hz–22 kHz sweep that is on the order of tens of
    microseconds, one to two **orders of magnitude finer** than the ≈0.6 ms and ≈2 ms separations
    the thread needs to resolve (0.2 m and 0.7 m extra path). The paper does not itself state this
    arithmetic — it is a direct consequence of the sinc relationship it does state, flagged here as
    computed, not quoted.
  - **Section 3.4 "Clock mismatch" (pp. 13–14) — directly on point for unsynchronized mics:**
    "One of the great advantages of the ESS method over other methods for measuring the impulse
    response is that a tight synchronization between the playback clock and the recording clock is
    not required." (p. 13). "In fact, even if two completely independent hardware devices are
    employed, and no clock synchronization is employed, usually the impulse response obtained is
    perfectly clean and without observable artifacts. However, when the mismatch between the two
    clocks becomes significant, the deconvolved impulse response starts to be 'skewed' in the
    frequency-time plane." (p. 13). The paper's own worked worst case — a portable CD player wired
    directly to an unrelated computer sound card, i.e. two consumer devices with no synchronisation
    attempt at all — produces a skew described as: "Looking again at fig. 32, we see that the
    skewness is approximately **8.5 ms** long." (p. 13–14), and shows this is *correctable* after
    the fact (Kirkeby inverse filter from a reference measurement, or a pre-stretched inverse
    filter) even without ever synchronising the two clocks. No ppm/threshold number is given for
    when mismatch "becomes significant" — searched for "ppm", "drift", "crystal": no hits.
  - **MLS comparison:** "the noise rejection is better than with an MLS signal of the same length,
    not-linear effects are perfectly separated from the linear response, and the usage of a single,
    long sweep (with no synchronous averaging) avoids any trouble in case the system has some time
    variance." (p. 2). Conversely, in the *zero-distortion, purely electrical* loopback case: "The
    old MLS method is perfect in this case, providing exactly a theoretical pulse." (p. 5) — the one
    place either paper credits MLS with an edge over ESS.
  - **Source/loudspeaker decay:** as with the 2000 paper, **not discussed** — no claim anywhere
    about closed-box vs. ported enclosures, port resonance, or a loudspeaker's own acoustic ring-down
    being confusable with a genuine reflection. The nearest related material is about *electrical*
    nonlinearity (amplifier/loudspeaker slew-rate distortion contaminating MLS responses, p. 4) and
    a methodological aside that an "electrical" reference measurement excludes "the effect of power
    amplifier, loudspeaker and microphones" (p. 7) — neither is a statement about decay time.
  - **Practical/SNR guidance:** long single sweeps are preferred over averaged short ones because
    "Synchronous time averaging works only if the whole system is perfectly time-invariant... the
    preferred way for improving the signal to noise ratio is not to average a number of distinct
    measurements, but instead to perform a single, very long sweep measurement, as clearly
    recommended in the ISO 18233/2006 standard." (p. 14). Pulsive background noise during a long
    sweep (people moving, floor creaks) is removable "to apply a narrow-band filter just around the
    instantaneous frequency at which the event occurred" (p. 12), because a sweep maps each instant
    to one frequency.
- **Page-number note:** the two AES-page citations above ("p. 6" for the sinc quote, "p. 13" for
  the clock-mismatch section) were determined independently from this document's own explicit
  "Page N of 21" footers (unambiguous — verified by full sequential listing of every such footer in
  the file). This corrects an earlier same-session sub-agent draft that had tentatively placed these
  two passages one page too early (p. 5 and p. 9); the correct pages per the paper's own footers are
  6 and 13 respectively, both confirmed by direct footer-sequence count.

### 3. Rajmane, A. & Baumann, W. (2016). "Detection of Reflecting Objects in Anechoic Chambers."
DAGA 2016 Aachen, pp. 331–333. **[held, `papers/small-chamber/`]**

- **File:** `Rajmane-Baumann_2016_DAGA_detection-reflecting-objects-anechoic-chambers.pdf`; re-read
  fresh into `papers/arc-validation/refetch-txt/Rajmane-Baumann_2016_DAGA.txt` (whole 3-page paper
  read in full).
- **Evidence level:** conference (DAGA), vendor-adjacent authors (G+H Schallschutz, a chamber
  builder) but the only source in the corpus that actually measures a real reflector's location
  acoustically with a sine-burst source, so treated as primary evidence, not [vendor]-tagged.
- **Identity:** confirmed p. 331 header/authors as cited.
- **What it says — this is the direct precedent for the thread's proposed method:**
  - **Source used:** "loudspeaker" (named explicitly, twice) driven by "Sine Burst Wave for the
    half period of excitation frequency" (p. 332).
  - **Time resolution actually used:** "The sound signal at microphone is analyzed in time domain
    at very short interval, as small as 60 μsec." (p. 332) — i.e. they resolved timing at ~60 µs,
    roughly **10–30× finer** than the ≈0.6–2 ms separations this thread needs, using nothing more
    exotic than fine time-domain sampling of a sine-burst response (not even a full ESS
    deconvolution).
  - **Lag → path-difference table (Table 3, p. 332, reproduced exactly):**

    | Measured time lag between first and second impulse | Calculated path difference from time lag | Measured (physical) path difference |
    |---|---|---|
    | 3.5 ms | 1.2 m | 1.2 m |
    | 2.3 ms | 0.8 m | 0.7 m |
    | 12 ms | 4.1 m | 4 m |

    The "calculated" column is simply Δr = c·Δt (c ≈ 343 m/s: 3.5 ms → 1.20 m; 2.3 ms → 0.79 m,
    rounded to 0.8; 12 ms → 4.12 m) — a direct, one-way path-difference conversion with **no
    division by two**, i.e. the same convention the thread's own background note uses (2 ms ⇒
    0.7 m, 0.6 ms ⇒ 0.2 m). Agreement with the physically measured path difference is good (1.2 m
    exact) to fair (0.8 vs 0.7 m, a 0.1 m / ~13% miss) to good (4.1 vs 4 m).
  - **Size rule (p. 332–333, exact wording):** "The reflecting object is identified, when length of
    side of square object is greater than or equal to wavelength of tonal excitation frequency."
    (p. 332) and, generalised: "Observations from table 1 and 2 show that reflecting object is
    identified, when length of side of square object is greater than or equal to wavelength of
    tonal excitation frequency. For the rectangle shaped reflector with L:W up-to 4:1, the object is
    still identified, when length of side of equivalent square object is greater than or equal to
    wavelength of tonal excitation frequency." (p. 333).
  - **Method summary (p. 333):** "The distance of reflecting object from sound source can be
    identified by emitting sine impulse and measuring the time lag of reflected sound on the
    measurement path." — confirms the family of technique (pulsed/burst source + time-lag readout)
    the thread proposes is an established, working procedure, just not previously done with an ESS
    or with an unsynchronized multi-mic array.
  - **Extraction artifact flagged:** the "Sine Burst Wave for / the half period..." sentence is
    split by this DAGA template's two-column layout even under plain `pdftotext`: "The source is
    excited with Sine Burst Wave for" (later in the raw stream) must be joined with "the half period
    of excitation frequency. The sound signal..." (earlier in the raw stream) to read correctly —
    both fragments verified verbatim in the dump; the *page* (332) is unaffected since both halves
    fall on the same printed page between the "331" and "332" footers.

### 4. Sun, H., Mabande, E., Kowalczyk, K. & Kellermann, W. (2012). "Localization of distinct
reflections in rooms using spherical microphone array eigenbeam processing." J. Acoust. Soc. Am.
131(4), 2828–2840. **[held, `papers/reflection-localization/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Sun_2012_JASA.txt`.
- **Evidence level:** journal (peer-reviewed).
- **What it says (numbers, re-verified against Table V/VI in the fresh dump):** single Eigenmike
  spherical array, **32 microphones** on a rigid sphere of radius a = 0.042 m ("well-calibrated
  high-quality microphones", one integrated device — all 32 channels share one ADC, so mic-to-mic
  synchronisation is a non-issue by construction), 44.1 kHz. DOA-only localisation (not full 3D
  position) of the direct sound plus up to five first-order reflections and one second-order
  reflection. Room 1, best method (EB-MVDR + frequency smoothing + white-noise-gain control), DOA
  deviation from CATT-simulated ground truth (Table V, re-verified cell by cell against the fresh
  dump): direct 2.0°, ceiling 1.6°, floor 3.3°, wall 2 2.2°, wall 3 4.1°, wall 4 6.1°, walls-2+3
  (second-order) 3.0°. Room 2 (Table VI): direct 2.0°, floor 1.0°, three walls 3.6/2.2/3.1°,
  **ceiling not localised at all** (all dashes in the table).
- **Verbatim quotes:**
  - "Up to six coherent sources, namely the direct-path sound and five first-order reflections can
    be well localized using the EB-MVDR with frequency smoothing and WNG control." (p. 2835)
  - "the DOA-estimation deviation of reflected signals is larger than that of the direct sound
    signal, since the SNRs of reflected signals are much lower than for the direct sound, and some
    boundary surfaces in the rooms are not perfect reflectors." (p. 2837)
  - "The ceiling in room 2 is not regular and it has several lights with quite large reflecting
    surfaces. Therefore, the localization results for the ceiling are all far from the ground truth
    values." (Table IV footnote d, p. 2839)
  - Sampling/synchronisation: "The microphone signals were recorded and then processed offline, at
    a sampling rate of 44.1 kHz." (p. 2836/2837 boundary) — one array, one ADC; **no mention
    anywhere of synchronisation across multiple devices** (searched "synchron", "clock",
    "jitter": zero hits in the whole paper).

### 5. Mabande, E., Kowalczyk, K., Sun, H. & Kellermann, W. (2013). "Room geometry inference based
on spherical microphone array eigenbeam processing." J. Acoust. Soc. Am. 134(4), 2773–2789.
**[held, `papers/reflection-localization/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Mabande_2013_JASA.txt`.
- **Evidence level:** journal.
- **What it says:** same Eigenmike (32 mics, single device) plus a simulated 240-mic large array
  (a = 0.111 m); two-stage pipeline (DOA + TDOA from the array → image-source geometry via
  least-squares plane fit). **Explicitly assumes the source-to-array distance is known a priori**:
  "the array, which is assumed to be known a priori, the position of..." (p. of the geometry
  section — direct-signal reference distance Xj,0 "is assumed to be known a priori" appears twice,
  lines defining the geometric model). Real lecture room (T60 ≈ 900 ms), J = 4 source positions,
  measured SNR "12 dB" in the body text (Table IX's own header instead prints "SNR = 15 dB" — the
  paper is internally inconsistent on this one number, confirmed present as printed: the number "12
  dB" appears three times in running text, "15 dB" was not found as separate text in the fresh
  dump — this specific inconsistency could not be independently confirmed from the plain-text
  table layer, flagged as unclear in text rather than asserted). Real-room result (Table VIII/IX):
  DOA deviations 1.0–5.0°, TDOAs matched to specific ms values; noise-source geometry error 2.4°
  mean orientation / 1.04 cm mean distance / 0.23% volume error; speech source 3.2° / 1.44 cm /
  0.21%. Simulation (Table II, J = 4, SNR 30 dB, α = 0.7): 1.6° / 1.52 cm / 0.35% volume error.
- **Verbatim quotes:**
  - "the array, which is assumed to be known a priori" and (elsewhere) "the direct signal, Xj;0,
    which is assumed to be known a priori" — the source-to-array distance is a required input, not
    estimated.
  - "the errors in boundary plane estimation are mainly due to the errors in the DOA estimation,
    which substantially influence the orientation of the boundaries and may cause a disproportionate
    error in DP,P̂." (p. 2784)
  - "The positions of the walls, even in large acoustic enclosures, are estimated precisely up to a
    few centimeters only." — this sentence is split by the same two-column extraction artifact as
    the Rajmane-Baumann one: "The positions of the walls," ends the right column of p. 2787,
    "even in large acoustic enclosures, are estimated precisely up to a few centimeters only" opens
    the Conclusion's continuation on **p. 2788** (confirmed: this text falls strictly between the
    document's own "2787" and "2788" page-footer tokens; the Acknowledgments section, which
    conventionally follows the Conclusion and precedes the References, is on the same page-2788
    block, and References begin on p. 2789 — consistent with a 17-page article, pp. 2773–2789).
  - **No mention of unsynchronized/asynchronous microphones anywhere** (searched "synchron",
    "asynchron", "clock": zero hits) — consistent with using one compact, single-device array.

### 6. Lovedee-Turner, M. J. & Murphy, D. T. (2019). "3D Reflector Localisation and Room Geometry
Estimation using a Spherical Microphone Array." J. Acoust. Soc. Am. 146(5), 3339–3352 (accepted
manuscript via White Rose, DOI 10.1121/1.5130569). **[held, `papers/reflection-localization/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Lovedee-Turner-Murphy_2019_JASA.txt`.
  This PDF is the **accepted manuscript** (White Rose eprint, "Version: Accepted Version"), which
  carries its *own* running page numbers 1–15, not JASA's 3339–3352 — quotes below are cited as
  "manuscript p. N" to avoid implying the printed-journal pagination.
- **Evidence level:** journal (accepted manuscript).
- **What it says — the cleanest explicit assumptions list found in the whole corpus for this
  question, quoted in full (manuscript p. 1):**
  > "The following assumptions are made when inferring the room's geometry,
  > • Source-receiver distance and room temperature are known a priori
  > • There is at least a 50 cm distance from the source and receiver to the boundaries (half the
  >   standard measurement distance allowing for analysis of smaller/complex rooms)
  > • Reflections have a dominant specular component
  > • Boundaries define a closed room
  > • Floor and ceiling are parallel to each other
  > • Walls are perpendicular to both the floor and ceiling"
  Single spherical array (Eigenmike EM32, 32 mics). Real cuboid room (10.35 × 13.29 × 4.19 m)
  result, re-verified cell by cell against Table III in the fresh dump (manuscript p. 12): wall
  position errors 16.16, 4.02, 25.46, 13.0 cm; floor 14.5 cm; ceiling 10.60 cm; **RMS 15.37 cm**,
  dihedral angle RMS **1.21°**, length RMS 23.02 cm — every cell matches the earlier MATRIX note
  exactly.
- **Verbatim quotes:**
  - The assumptions list above (manuscript p. 1).
  - "The RMS boundary position errors are comparable to prior work[1,5,8,10] with a maximum
    difference in RMS error of 16.38 cm, using at most three measurement positions, compared to
    6-64 used in this prior work." (manuscript p. 12–13, Conclusion)
  - "inaccuracies are likely due to either imperfect specular reflections, under or over estimation
    of the ToA for reflections in the measured impulse responses, or any inaccuracy in the estimated
    DoA" (manuscript, Sec. V C)
  - Real-room confound named explicitly: "the ceiling was covered in large metal piping connected
    to extractor fans and a layer of metal railing approximately 1 m from the ceiling." (Sec. IV)
  - **No mention of unsynchronized microphones** (searched "synchron": zero hits) — single-array
    assumption throughout.

### 7. Sprunck, T., Deleforge, A., Privat, Y. & Foy, C. (2022). "Gridless 3D Recovery of Image
Sources from Room Impulse Responses." arXiv:2208.14017v2. **[held, `papers/reflection-localization/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Sprunck_2022_arXiv.txt` (5-page
  PDF, page numbers below from the file's own form-feed page breaks, PDF p. N of 5).
- **Evidence level:** report/preprint, simulation-only.
- **What it says:** convex-relaxation (BLASSO) recovery of continuous 3D image-source positions
  from a simulated 32-mic open-sphere array (em32 geometry scaled ×2), noiseless case, up to 500
  image sources: radial error 0.069–0.300 mm, angular error 0.36–0.46°, **recall falling from 94.3%
  (≤150 sources) to 57.3% (500–1323 sources)** as the scene gets denser (Table I). Authors are
  explicit that this is far from real-world ready.
- **Verbatim quotes:**
  - "The strength of the proposed gridless approach is revealed by the mean radial and angular
    errors, which are below tenths of millimeters and fractions of degrees." (PDF p. 4)
  - "applying the method to real data will require a number of challenging extensions. Indeed, real
    RIRs are impacted by the frequency and angular dependencies of source, microphone and wall
    responses." (PDF p. 4)
  - Model definition: image sources "synchronously emit the same impulse δ0(t)" — this is about
    the *image-source physics model* (all reflections of one emission arrive as delayed copies of
    the same pulse), **not** about microphone-array synchronisation; there is no other occurrence of
    "synchron-" in the paper.

### 8. Hadadi, Y., Tourbabin, V., Ben-Hur, Z., Alon, D. L. & Rafaely, B. (2024). "Blind
Localization of Early Room Reflections with Arbitrary Microphone Array." arXiv:2409.15484v1.
**[held, `papers/reflection-localization/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Hadadi_2024_arXiv.txt` (10-page
  PDF with clean printed page numbers 2–10 as running headers).
- **Evidence level:** report/preprint, simulation + one real listening test.
- **What it says:** blind (no RIR, no source signal) DOA+delay estimation; a 32-mic sphere and a
  6-mic semi-circular open array both tested; true positive = within 0.5 ms and 15°.
- **Verbatim quotes (both re-verified against the fresh dump, p. 5):**
  - "reflections with high amplitudes, i.e. 0.4 with respect to the direct sound or higher, are
    easier to detect." (p. 5)
  - "reflections that appear later, i.e. 10 ms with respect to the direct sound, are harder to
    detect." (p. 5)
  - No occurrence of "synchron-" anywhere in the paper — 16 kHz sampling rate stated (p. 4–5) with
    no discussion of cross-device timing.

### 9. Tervo, S., Pätynen, J., Kuusinen, A. & Lokki, T. (2013). "Spatial Decomposition Method for
Room Impulse Responses." J. Audio Eng. Soc. 61(1/2), 17–28. **[held, `papers/reflection-localization/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Tervo_2013_JAES.txt`.
- **Evidence level:** journal.
- **What it says — the clearest stated microphone-count/geometry requirement in the set (p. 19,
  re-verified verbatim in the fresh dump):**
  > "The analysis assumes the following general requirements for the used microphone array:
  > • For 3-D spatial sound encoding, the minimum requirement of the number of microphones is
  >   four, which are not on the same plane, so that they can set up a 3-D space.
  > • The directivity of one of the microphones is omnidirectional or it is possible to create one
  >   virtual omnidirectional pressure microphone signal from the others.
  > • The dimensions of the array are not large, i.e., the microphone array is compact. The
  >   dimensions should be less or equal to the dimensions of a human head.
  > • Open microphone arrays are preferred, but closed ones can also be used as long as the above
  >   requirements are met."
  Cross-correlation TDOA per analysis window (evaluated with a 7-mic open array). Explicit
  limitation: once more than one reflection falls in the same analysis window, the method picks the
  strongest and mislabels the rest: "as the time progresses the number of acoustic events per time
  window increases, and eventually more than one reflection arrives during the time window. In this
  case, a cross-correlation-based localization algorithm localizes the sound to the location of the
  reflection that is the strongest one in that time window." (p. 21). No degree/cm accuracy number
  is reported for reflection localisation specifically (only listening-test similarity scores and
  an echo-density time bound); flagged as such rather than invented.
- **No mention of unsynchronized microphones** — the array is explicitly required to be one
  compact physical unit ("compact... less or equal to the dimensions of a human head").

### 10. Meyer-Kahlen, N., Amengual Garí, S. V. & Lokki, T. (2022). "What the Spatial Decomposition
Method can and cannot do." Proc. ICA 2022, Gyeongju. **[held, `papers/reflection-localization/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Meyer-Kahlen_2022_ICA.txt`. This
  9-page proceedings PDF's page-number tokens extract out of sequence (a "4" and a "1" appear
  consecutively where a linear read would expect "4","5"), most likely from the same two-column
  reading-order artifact seen elsewhere in this batch; page citations below are given as **"PDF p.
  N of 9"** (physical page index, unambiguous) rather than a claimed printed page number.
- **Evidence level:** conference (peer-reviewed proceedings).
- **What it says:** position paper distinguishing TDoA (open array, ≥4 non-coplanar omnis) from
  pseudo-intensity-vector (tetrahedral/FOA) analysis for SDM. Minimum-array quote (PDF p. 3 of 9):
  "For TDoA estimation, the responses of an open array of at least four microphones that are not in
  the same plane are used to obtain the direction within a block of size N, centered around each
  sample t." Resolution limit (PDF p. 4 of 9): "directional analysis fails if two sound events occur
  simultaneously, wherein it is important to note that simultaneously does not mean that the sound
  events need too occur within one sampling interval, but within one analysis block." And: "the
  temporal resolution is limited by the size of the used microphone array, regardless of the
  estimation method." (PDF p. 8 of 9). No occurrence of "synchron-" in the paper.

### 11. Dokmanić, I., Parhizkar, R., Walther, A., Lu, Y. M. & Vetterli, M. (2013). "Acoustic
echoes reveal room shape." PNAS 110(30), 12186–12191.

- **File:** `Dokmanic-etal_2013_PNAS_acoustic-echoes-reveal-room-shape.pdf` /
  `txt/Dokmanic-etal_2013_PNAS_acoustic-echoes-reveal-room-shape.txt`.
- **Route:** PNAS's own PDF links return an HTML paywall page even though the article is OA (a
  known PNAS-site quirk); retrieved instead from co-author Ivan Dokmanić's own faculty page,
  `https://dokmanic.ece.illinois.edu/assets/pdf/Dokmanic2013dz.pdf`. This is the PNAS "Early
  Edition" typesetting (pages numbered 1–6 within the PDF, not 12186–12191) — cited as "p. N of 6".
- **Evidence level:** journal (PNAS).
- **Identity:** confirmed p. 1, title/authors/affiliations exactly as cited; DOI
  10.1073/pnas.1221464110 confirmed in the page-2 footer text.
- **What it says — the one paper in this set that explicitly allows an arbitrary, tape-measured
  microphone layout and states a minimum microphone count with a clean bound:**
  - "A subspace-based formulation allows us to use the minimal number of microphones (four
    microphones in 3D). It is impossible to further reduce the number of microphones, unless we
    consider higher-order echoes..." (p. 1)
  - "Consider a room with a loudspeaker and an array of M microphones positioned so that they hear
    the first-order echoes (we typically use M = 5)." (p. 3)
  - "In all experiments, microphones were arranged in an arbitrary geometry, and we measured the
    distances between the microphones approximately with a tape measure. We did not use any
    specialized equipment or microphone arrays." (p. 5)
  - **Source position need not be known — and unsynchronized source-vs-receiver timing is
    explicitly named as a solvable sub-case (p. 3):** "The loudspeaker position need not be known.
    We can estimate it from the direct sound using either TOA measurements, or differences of TOAs
    if the loudspeaker is not synchronized with the microphones (19–21)."
  - **What must be known: only the microphones' pairwise distances**, not a designed array
    geometry, and this requirement is reported as loosely tolerant of calibration error (p. 5–6):
    "The proposed algorithm has essentially no constraints on the microphone setup. Thus, we can
    arbitrarily reposition the microphones, as long as we know their pairwise distances... we find
    the proposed schemes to be very stable with respect to uncertainties in array calibration."
  - Real-room accuracy (Fig. 6 labels, p. 5, real-vs-estimated pairs extracted from the figure's
    text layer, pairing per the figure caption): wall distances real/estimated 7.01/7.08 m,
    6.48/6.53 m, 4.55/4.59 m, 6.71/6.76 m (≈4–7 cm deviation); angles 89.9/90.0°, 63.2/62.0°,
    90.3/90.0°, 100.9/100.5° (≈0.1–1.2°). "Note that the floor and the ceiling are estimated near
    perfectly" and "the obtained results are remarkably accurate and robust." (p. 5). Full-precision
    numeric tables are in the SI Appendix, **not retrieved** (out of this thread's scope; the SI PDF
    would be the next fetch if exact aggregate error statistics are needed).
  - **Mic-to-mic (receiver-to-receiver) clock desynchronisation is NOT discussed anywhere** — the
    single "synchron-" hit in the whole paper (quoted above) is about the *source* not being
    synchronized with the (implicitly synchronized, single-recorder) microphone set, not about
    microphones being unsynchronized relative to each other.

### 12. Antonacci, F., Filos, J., Thomas, M. R. P., Habets, E. A. P., Sarti, A., Naylor, P. A. &
Tubaro, S. (2012). "Inference of room geometry from acoustic impulse responses." IEEE Trans.
Audio, Speech, Lang. Process. 20(10), 2683–2695.

- **File:** `Antonacci-etal_2012_IEEE-TASLP_room-geometry-inference.pdf` /
  `txt/Antonacci-etal_2012_IEEE-TASLP_room-geometry-inference.txt`.
- **Route:** IEEE Xplore is blocked (per protocol); the current Zenodo OA mirror listed by
  Semantic Scholar is dead (HTTP 410, takedown); co-author Stefano Tubaro's own faculty page
  (`tubaro.faculty.polimi.it`) is currently NXDOMAIN; recovered via the Wayback Machine's preserved
  snapshot of that now-dead page: `https://web.archive.org/web/20240414033207id_/https://tubaro.faculty.polimi.it/Journals/2012_IEEE_TrASLP_environment_inference.pdf`.
- **Evidence level:** journal (peer-reviewed). Two-column IEEE PDF: inline mathematical
  variables/subscripts and Tables I–II do not extract as text in either plain or `-layout` mode
  (confirmed both ways) — flagged wherever a number is missing rather than guessed.
- **Identity:** confirmed pp. 2683–2684, title/authors/DOI (10.1109/TASL.2012.2210877) exactly as
  cited.
- **What it says — this is the paper in the whole retrieved set that engages MOST directly with
  unsynchronized timing, though at the source-vs-array level, not mic-vs-mic:**
  - Three explicit scenarios (p. 2684): "i) the source and receiver signals are synchronized and
    the source signal is known, ii) the source and receiver signals are unsynchronized and the
    source signal is known and iii) the source and receiver signals are unsynchronized and the
    source signal consists of an unknown impulse-like sound like finger-snaps or hand-claps."
  - Mechanism (p. 2685–2686): "in many practical cases the synchronization cannot be achieved;
    therefore the TDOAs, which are preserved, are used to localize the source relative to the
    microphone array from which TOAs are estimated. If any one of the TOAs, TDOAs or source location
    are unavailable then it can always be estimated from the remaining two." / "In order to estimate
    TOAs from unsynchronized AIRs, the TDOAs of the direct-paths are used to localize the acoustic
    source and consequently estimate the propagation time of the direct sound from the source to a
    reference microphone. Subsequently, the propagation times of all the other arrivals can be
    inferred." / "The TOAs of the reflective paths are straightforwardly obtained since both [T0]
    and the TDOAs between the direct-paths and the reflective paths are known from inspection of
    [ym], even if the source and microphone signals are not synchronized."
  - Real-room validation, deliberately unsynchronized (p. ~2693): "The microphone signals were
    sampled at 96 kHz... No effort was made to synchronize the recorded signals with the input
    stimulus." Array: "four microphones spaced by 0.5 m in a '+' configuration and a fifth placed
    in the centre" — **5 microphones total**. "Even for the case of 4 source positions an error of
    only a few centimeters is observed... Using 16 source positions... the localization accuracy
    approaches the limits of the hand-measured ground truths."
  - Sub-sample timing precision claimed for peak-picking (p. 2685–2686): "Detection of impulsive
    events can be achieved to within one sample by considering local centres of energy with
    algorithms such as the sliding group delay function... and the findpeaks function."
  - **Key limitation for this thread's exact scenario:** the microphone array's *relative geometry
    is assumed known* — "A microphone array of [M] microphones, whose relative geometry is assumed
    known, is placed in a reverberant environment" (p. 2685) — and the whole TDOA→source→TOA
    pipeline implicitly presupposes the array's own multiple channels are mutually time-aligned
    (recorded through a shared/known reference), even while the *emission* need not be. **No
    passage anywhere discusses microphone-to-microphone (independent, per-device) clock
    uncertainty** — searched "clock": zero hits in the entire paper. This is the closest published
    analogue found to the thread's problem, but it does not cover the specific unsynchronized-array
    case the 11-mic UMIK-2 arc presents.

### 13. Oppenheim, A. V. & Schafer, R. W. (2004). "From Frequency to Quefrency: A History of the
Cepstrum." IEEE Signal Processing Magazine, Sept. 2004, pp. 95–99 (+106). *(Substitute for Bogert,
Healy & Tukey 1963 — see Retrieval log; the 1963 original, a book chapter in Rosenblatt (ed.),
Proc. Symp. Time Series Analysis, Wiley, is held only as an access-restricted scan on
archive.org and could not be downloaded.)*

- **File:** `Oppenheim-Schafer_2004_IEEE-SPM_from-frequency-to-quefrency.pdf` /
  `txt/Oppenheim-Schafer_2004_IEEE-SPM_from-frequency-to-quefrency.txt`.
- **Route:** university mirror `https://www.fceia.unr.edu.ar/prodivoz/Oppenheim_Schafer_2004.pdf`.
- **Evidence level:** tutorial/magazine (peer-reviewed-adjacent IEEE Signal Processing Magazine
  historical column), written by two of the field's central figures — used here as a **secondary,
  clearly-labelled** source for the 1963 paper's content, not as if it were the original.
- **Identity:** confirmed p. 95, title/authors/venue exactly as cited.
- **What it says — Q3's core mechanism, both directions:**
  - **Single echo → cepstral peak (p. 95, full derivation reproduced):**
    "note that a signal with a simple echo can be represented as x(t) = s(t) + αs(t−τ). (1) The
    Fourier spectral density (spectrum) of such a signal is given by |X(f)|² = |S(f)|² [1 + α² +
    2αcos(2πfτ)]. (2)... By taking the logarithm of the spectrum, this product is converted to the
    sum of two components; specifically C(f) = log|X(f)|² = log|S(f)|² + log[1 + α² +
    2α cos(2πfτ)]. (3) Thus, C(f) viewed as a waveform has an additive periodic component whose
    'fundamental frequency' is the echo delay τ... the 'spectrum' of the log spectrum would likewise
    show a peak when the original time waveform contained an echo."
  - **Periodic/harmonic source → rahmonics, i.e. cepstrally indistinguishable in shape from an
    echo (p. 97–98):** "The problem of pitch detection is very similar to detecting echo times in
    the sense that the basic speech model consists of representing speech as the convolution of the
    vocal tract impulse response with the quasi-periodic train of glottal pulses." (p. 97). Fig. 2
    caption: "Note the peaks at 'rahmonics' of 1/80 = 12.5 ms, the fundamental quefrency of the
    quasi-periodic ripples in the upper graph... this fundamental quefrency is also the period
    (pitch period) of the time waveform." (p. 98) — i.e. a train of harmonics spaced at f0 produces
    the *same kind* of cepstral peak, at quefrency 1/f0, as a single echo of delay 1/f0 would.
  - **Separating the two — liftering (p. 97):** "Bogert et al. had introduced the concept of
    liftering, i.e., linear filtering of the log spectrum, as a way of emphasizing the periodic
    component of the log spectrum so as to enhance the detectability of echos... By applying a
    low-pass lifter to the cepstrum in Figure 2 to extract the low quefrency components below the
    first rahmonic peak, the slowly varying curve... results. The low quefrency components thus
    correspond to the resonance structure of the vocal tract and high frequency falloff of the
    speech spectrum due to the glottal pulse."
  - **Coinage, reproducing the 1963 original's own words (p. 95):** "In their classic paper
    entitled *The Quefrency Alanysis of Time Series for Echos: Cepstrum, Pseudo-Autocovariance,
    Cross-Cepstrum, and Saphe Cracking*, Bogert, Healy and Tukey were perhaps in a very playful frame
    of mind when they coined the term cepstrum, along with a complete glossary that included, in
    addition to those in the title of their paper, terms such as rahmonics and liftering. The
    motivation for this strange new terminology... was succinctly stated as follows: 'In general, we
    find ourselves operating on the frequency side in ways customary on the time side and vice
    versa.'" (the original title's typos "Alanysis"/"Echos" are Bogert, Healy & Tukey's own,
    reproduced here verbatim by Oppenheim & Schafer and preserved in this quote.)

### 14. Randall, R. B. (2013 conference precursor of 2017 MSSP 97, 3-19). "A History of Cepstrum
Analysis and its Application to Mechanical Problems." Surveillance 7 International Conference.
*(Substitute/precursor for Randall, R. B. (2017), Mechanical Systems and Signal Processing 97,
3-19 — ScienceDirect is a known blocker; this is the same sole author's own conference paper on
the identical title, dated by its own PDF metadata to 2013, not confirmed word-identical to the
2017 journal text.)*

- **File:** `Randall_2013_Surveillance7_history-of-cepstrum-analysis.pdf` /
  `txt/Randall_2013_Surveillance7_history-of-cepstrum-analysis.txt` (the actual saved filename —
  note this differs from a same-session sub-agent's own summary, which referred to the file as
  "Randall_2017_..."; the file as it exists on disk, and as verified from its own front matter and
  `pdfinfo` CreationDate, is the 2013 Surveillance 7 version).
- **Route:**
  `https://surveillance7.sciencesconf.org/conference/surveillance7/01_a_history_of_cepstrum_analysis_and_its_application_to_mechanical_problems.pdf`.
- **Evidence level:** conference (peer-reviewed proceedings), same author/title as the cited MSSP
  journal paper.
- **Identity:** confirmed p. 1, "A History of Cepstrum Analysis and its Application to Mechanical
  Problems / Robert B Randall / School of Mechanical and Manufacturing Engineering, University of
  New South Wales" — matches. Page numbers below re-verified against this document's own
  sequential physical-page structure (no printed footers; PDF page index used, and cross-checked
  as internally consistent by locating each quote and counting form-feed breaks).
- **What it says — the mechanical-engineering-domain confirmation of Q3, with a numeric example
  directly analogous to a propeller's BPF+harmonics:**
  - Original definition (p. 1): "The first paper on cepstrum analysis defined it as 'the power
    spectrum of the logarithm of the power spectrum'. The original application was to the detection
    of echoes in seismic signals, where it was shown to be greatly superior to the autocorrelation
    function, because it was insensitive to the colour of the signal."
  - **Harmonic/sideband family → one dominant rahmonic (p. 4, directly analogous to a BPF +
    harmonics spectrum):** "Local faults in gears give an impulsive modulation of the gearmesh
    signals... resulting in large numbers of sidebands spaced at the speed of the gear on which the
    local fault is located. The majority of such sidebands are only visible on a spectrum with a log
    amplitude scale, and so the cepstrum is an ideal way to collect the (average) information of a
    large number of such sidebands into a relatively small number of rahmonics in the cepstrum, of
    which the first contains most of the information."
  - **Real echo in a mechanical measurement is also called a "rahmonic" family, confirming the two
    phenomena are cepstrally the same kind of object (p. 8, p. 11):** "the cepstrum of a signal with
    an inverted echo is entirely negative, so that its integral over quefrency becomes markedly more
    negative when such an inverted echo is in the analysed section of time record." (p. 8, on
    detecting cracks via echo polarity) — and "the effects of echoes in a measurement (eg a double
    hit with a hammer) can be neutralised when curve-fitting the cepstrum because the corresponding
    rahmonics can be eliminated by a comb lifter." (p. 11).
  - **Separating them — comb lifter aimed exactly at the known periodic rate, then keep the
    residual (p. 6, p. 12–13):** "the periodic forcing function of the gearmesh was removed in the
    cepstrum using a comb lifter adjusted to the gearmesh quefrency, leaving a cepstrum dominated by
    the transfer function to the measurement point." (p. 6). "Whole families of uniformly spaced
    harmonics or sidebands can be removed by removing a small number of rahmonics in the
    cepstrum... Setting the value of the discrete rahmonics to zero automatically smooths over the
    amplitude of the log spectrum in the vicinity of the corresponding harmonics and/or sidebands
    (since notches in the log spectrum would equally give non-zero cepstrum components as for
    peaks)." (p. 12–13).
  - **Terminology coinage, matching Oppenheim & Schafer's account (p. 4):** "the authors coined the
    word 'cepstrum' by reversing the first syllable of 'spectrum'... Similarly, the word 'quefrency'
    was obtained from 'frequency', and the authors also suggested a number of others, including:
    rahmonic from harmonic / lifter from filter / gamnitude from magnitude / saphe from phase /
    darius from radius / dedomulation from demodulation."
  - **Direct bearing on the thread's own working conclusion:** neither this paper nor Oppenheim &
    Schafer offers an *intrinsic* cepstral test that tells "this is a genuine echo" apart from "this
    is a rahmonic of a known periodic source" purely from the cepstrum's shape — both are, by
    construction, a peak at quefrency = 1/(period). What both sources actually do, and recommend, is
    to *independently* identify the periodic rate from other information (a tachometer/known
    gearmesh rate here; a measured BPF and shaft rate in the thread's own case), then comb-lifter
    exactly that quefrency and its multiples out, and treat what survives elsewhere in the cepstrum
    as the residual of interest. This is exactly the move the thread's own analysis already made in
    identifying 4.2 ms = 1/BPF and 8.4 ms = the shaft period as rahmonics to be set aside, not read
    as echoes — confirmed here as the field's standard practice, not an ad hoc judgement call.

### 15. Childers, D. G., Skinner, D. P. & Kemerait, R. C. (1977). "The cepstrum: A guide to
processing." Proc. IEEE 65(10), 1428–1443. **NOT RETRIEVED** — see Retrieval log. DOI
10.1109/PROC.1977.10747. No claim is made from this paper anywhere in this file.

### 16. Cunefare, K. A., Biesel, V. B., Tran, J., Rye, R., Graf, A., Holdhusen, M. & Albanese,
A.-M. (2003). "Anechoic chamber qualification: Traverse method, inverse square law analysis
method, and nature of test signal." J. Acoust. Soc. Am. 113(2), 881–892. **[held,
`papers/anechoic-simulation/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Cunefare_2003_JASA.txt` (a copy
  already produced this session by a concurrent thread in the same shared campaign; confirmed
  identical in content to what a fresh `pdftotext -q` of the same PDF would give, and re-verified
  independently against it for every quote below).
- **Evidence level:** journal.
- **What it says — the clearest example in the whole corpus of "aim a traverse at a suspected
  reflecting feature" (p. 887):**
  > "In the following we present the results obtained for two traverse directions, one into the
  > lower northeast corner (LNE) of the anechoic chamber, and the other into the vertical center of
  > the west wall (WW), 0.1 m to the south side of the wedge basket hinge. These directions were
  > selected as the current standards emphasize traverses into the corners of the room under test,
  > with other traverses selected at the user's discretion. **The traverse toward the door was
  > selected anticipating that the structure of the wedge basket support and gaps around its
  > perimeter might generate reflections.**"
  (Note: the PDF's extracted text renders "(LNE)" and "(WW)" with garbled CJK-range bracket glyphs
  — a pdftotext font-encoding artifact, not a real character in the source — normalised to plain
  parentheses here.)
- **A second, independent diagnostic route in the same paper — a curve-fit parameter flags which
  traverses are problematic (p. 891):**
  > "The source offsets calculated in the optimal reference method, Eq. (5), are listed in Table X.
  > Of particular interest are the two instances noted in the table where the calculated source
  > offset exceeds twice the maximum source dimension (at the time of this writing, there was a
  > draft ISO 3745 in circulation that proposed a maximum permissible source offset of two times the
  > largest source dimension). Of note, these two cases of excessive source offset correspond to
  > traverses with poor performance with respect to the tolerance bounds, as well (Figs. 6 and 14,
  > and the 80- and 500-Hz LNE data in Table IX)."
  I.e., a *fitted* geometric parameter (how far the best-fit "effective acoustic centre" sits from
  the real source) that blows up is itself a signature that something nearby is reflecting, even
  before separately investigating what.
- **Table IX cell values could not be independently confirmed:** the earlier campaign note
  (`papers/anechoic-simulation/VERIFICATION-2026-09-07.md`) states "Table IX (p. 891): 80 Hz LNE
  tone 56% → 13% out of tolerance" and quotes the abstract's "significantly improve the apparent
  performance" line (re-verified present, p. 881, exact wording). The 56/13 raw numbers are indeed
  both present in Table IX's plain-text extraction at the 80 Hz row, but the table's 8-column
  nested header ("LNE traverses"/"WW traverses" × "Pure tone"/"Noise" × "Optimal"/"Fixed") itself
  extracts in a scrambled, non-hierarchical order in plain-text mode, so **which of the two numbers
  is the optimal-method value and which is the fixed-method value could not be confirmed from the
  text layer alone** — flagged as unclear in text rather than asserted either way.

### 17. Nash, A. (2019). "Qualification of an anechoic chamber." Proc. 23rd ICA, Aachen, pp.
1343–1349. **[held, `papers/anechoic-simulation/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Nash_2019_ICA.txt` (shared copy,
  independently re-verified; this PDF prints clean page-number footers throughout).
- **Evidence level:** conference.
- **What it says — a second, complementary route to "identify the reflecting feature": flag the
  anomalous TONE first, then infer a nearby reflector (without pinpointing which surface) (p.
  1348):**
  > "The draw-away for the 2056-Hz tone bears no resemblance to the 2 kHz one-third-octave band of
  > random noise... In Figure 6, the slope of the straight-line fit for the 2056-Hz tone is minus
  > 26.4 (eight decibels per doubling) — a value that is physically impossible. **The severe notch
  > in the draw-away for the 2056-Hz tone suggests an acoustical cancellation occurring between the
  > arriving wave front and a strong reflection from a nearby surface.**"
  This paper separately (by inspection, not by traverse-diagnosis) flags the chamber's own
  **expanded-metal floor grating** as a known/suspected reflector by design, and covers it during
  qualification: "Even though the floor grating has many perforations, it is still capable of
  reflecting high-frequency sound; therefore, the operational assumption is that the user would
  cover the walking surface with sound-absorptive material during critical measurements." (p. 1343).
- **Further verbatim quotes:**
  - "Compared to bands of noise, the use of discrete tones is more revealing of residual acoustical
    reflections arising from the walls, floor, and ceiling surfaces. It is now quite obvious that
    the acoustical environment in the chamber is not behaving like a free field." (p. 1348)
  - "The squared correlation coefficients appear to be acceptable; however, this appearance is
    deceiving since the 25-millimeter spatial sampling interval is only a small fraction of a
    wavelength." (p. 1348)
  - "For this particular anechoic chamber, it is likely that the sound-absorption properties of the
    foam wedges were deficient. There was no evidence that the wedges were ever qualified by testing
    them in an impedance tube." (p. 1349)
  - "In short, the chamber is absorptive but not anechoic." (p. 1349)
  - Abstract, confirmed p. 1343: "The chamber could satisfy the ISO tolerances when using random
    noise but failed to qualify when using pure tones."

### 18. Rizzi, S. A., Cabell, R. H. & Allen, A. R. (2013). "Recent enhancements to the NASA
Langley Structural Acoustics Loads and Transmission (SALT) facility." 11th Int. Conf. RASD, Pisa.
**[held, `papers/chamber-problems/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Rizzi_2013_RASD.txt`. This
  18-page proceedings PDF has **no extractable printed page-number text** anywhere (checked: every
  bare-digit line found is a numeric table/figure value, not a page marker) — quotes below are
  cited by physical PDF page index ("PDF p. N of 18"), counted from the file's form-feed page
  breaks (18 breaks confirmed for 18 pages via `pdfinfo`).
- **Evidence level:** conference.
- **What it says — corners identified as the reflecting feature by the standard ISO 3745
  corner-traverse protocol itself (PDF p. 10 of 18):**
  > "In the anechoic configuration, the deviations from inverse-square-law were all within the
  > requirements specified in the standard, except the farthest measurement locations below 250 Hz.
  > At these locations, the measurement microphones were close to the room corner opposite the sound
  > source. The excess deviations were attributed to long wavelength sound reflecting from the
  > corners of the room." Separately, aiming a source at the facility's own transmission-loss test
  > window turned up a second reflector: "Deviations were within the criteria of ISO 3745 except
  > for a few locations near the fiberboard insert and the opposite room wall below 160 Hz. These
  > higher deviations were attributed to long wavelength sound reflecting from the nearby wall and
  > interacting with the incident sound."
  - Summary judgement: "These measurements indicate the anechoic room provides an adequate
    approximation of a free-field acoustic environment from 80 Hz to 12.5 kHz, although care should
    be taken to keep an adequate separation distance between the microphones and walls of the room
    below 250 Hz." (PDF p. 10 of 18)

### 19. Winker, D. & Stahnke, B. (2016). "The influences of changes in international standards on
performance qualification and design of anechoic and hemi-anechoic chambers." Inter-Noise 2016,
Hamburg. **[held, `papers/chamber-problems/`]**

- **File:** re-read fresh into `papers/arc-validation/refetch-txt/Winker-Stahnke_2016_InterNoise.txt`
  (shared copy, independently re-verified; clean page footers "N / INTER-NOISE 2016").
- **Evidence level:** conference (industry vendor authors, ETS-Lindgren — a chamber builder, so
  treated with the same caution as [vendor] sources though the content is methodological/standards
  analysis, not a product claim).
- **What it says — a distinct and important variant on "identify the reflecting feature": the
  measurement rig/apparatus itself, not a room surface, is named as the dominant suspect at high
  frequency (p. 7):**
  > "The most likely factor is the influence of the measurement system inside the free-field
  > creating reflections that do not appear at lower frequencies. **A testing stand or rig is
  > required to qualify most anechoic chambers without built in anchoring points or a center floor
  > cavity. The introduction of these apparatuses in the free field causes small deviations to
  > appear in the measurements.**"
  This is directly relevant to the thread's own rig: the Tyto stand / arc structure that will hold
  the loudspeaker is itself a candidate reflecting feature, separate from any room surface.
- **Further verbatim quote (p. 3), on why a traverse can pass qualification while still hiding a
  real reflector — relevant to interpreting any traverse-based diagnosis cautiously:**
  > "By using this fitting method, a chamber can fully comply with ISO 3745 at certain frequencies
  > while not exhibiting free-field performance at those frequencies."

### 20. Attenborough, K. (2015). "Outdoor ground impedance models." EuroNoise 2015, Maastricht,
pp. 1785–1790.

- **File:** `Attenborough_2015_EuroNoise_outdoor-ground-impedance-level-difference-fitting.pdf` /
  `txt/Attenborough_2015_EuroNoise_outdoor-ground-impedance-level-difference-fitting.txt`.
- **Route:** open EuroNoise proceedings server,
  `https://www2.conforg.fr/euronoise2015/proceedings/data/articles/000055.pdf` (redirected from
  `www.conforg.fr`). The fuller JASA companion (Attenborough, Bashir & Taherzadeh 2011, JASA
  129(5), 2806–2819, doi:10.1121/1.3569740) is paywalled at `pubs.aip.org` (known blocker) and has
  **no open-access copy indexed anywhere** (confirmed via Unpaywall: `"is_oa": false`); the Open
  University's repository page for it, `oro.open.ac.uk/28793/`, is blocked by a Cloudflare
  JS-challenge from this environment — see Retrieval log for the proxy request.
- **Evidence level:** conference (EuroNoise/EAA), single author, the field's most-cited authority
  on this exact method family.
- **Identity:** confirmed p. 1785, "Outdoor ground impedance models / Keith Attenborough /
  Department of Engineering and Innovation, The Open University, Milton Keynes, UK."
- **What it says — this is a load-bearing NEGATIVE finding for Q5, not a positive method match:**
  - The "level difference" / "template" method exists and is standardised: "It is common to deduce
    parameter values for impedance models by fitting short range level difference spectra using
    'template' methods." (p. 1785). "NT ACOU 104 Ground surfaces: Determination of the Acoustic
    Impedance describes the fitting of predictions based on the Delany and Bazley impedance model
    to third-octave data for the difference in levels recorded between vertically separated
    microphones at a short range from a point source. **The method uses a single geometry (source
    height 0.5 m, receiver heights at 0.5 m and 0.2 m, separation 1.75 m).** The fits are used to
    place a given ground surface in one of twelve impedance classes based on values of effective
    flow resistivity." (p. 1788)
  - **What is fitted is the impedance/flow-resistivity, with geometry fixed and known — not the
    reverse.** The method's forward model builds the predicted level-difference/excess-attenuation
    spectrum from source and receiver heights and separation, all given, and adjusts only the
    surface's material parameters to match the measured spectrum. Accuracy is reported as a fitting
    error in dB, not a position error: "In a similar manner to the procedure described in NT ACOU
    104, the fitting errors (E) are calculated from..." and "a site is not classifiable if the
    fitting error exceeds 15 dB." (p. 1789)
  - **No governing equation or discussion of recovering path-length difference (hence reflector
    distance/position) from the spacing of comb-filter dips was found anywhere in the paper** —
    searched "dip", "peak", "comb": zero hits. The path-length terms (R1–R4 in the paper's own
    notation) appear only as *known, fixed inputs* to the forward excess-attenuation calculation,
    never as unknowns solved for from the interference pattern.
  - **No discussion anywhere of inferring reflector position/geometry from level-difference data
    when the geometry is unknown** — searched "position", "distance" (beyond the fixed "4 m" example
    distance), "unknown", "invert": no passage addresses the reverse problem this thread would need
    (recovering an unknown reflector's position, rather than a known-position surface's impedance,
    from level data alone). **This is the answer to Q5 for the one paper retrieved on this topic: the
    best-established version of the level-difference/template method family is built and validated
    exclusively for "known geometry → fit impedance", and gives no evidence that it has been (or can
    straightforwardly be) run in the opposite direction.**

---

## Answers to the thread questions

**Q1. Impulse-response measurement (ESS vs MLS; bandwidth/resolution for ≈2 ms / ≈0.6 ms gaps;
source requirements).**
Farina 2000 (§source 1) and Farina 2007 (§source 2) are the two open, canonical ESS papers and
both were read in full. **Bandwidth/resolution:** Farina 2007 states directly that the deconvolved
impulse is a bandwidth-limited sinc-like pulse ("the peak is in reality some sort of Sync
function... due to the limited bandwidth of the signal", p. 5) — for a normal full-audio-band sweep
(22 Hz–22 kHz in Farina's own worked example) the resulting temporal resolution (tens of
microseconds) is one to two orders of magnitude finer than the ≈0.6 ms and ≈2 ms gaps this thread
needs to resolve; this arithmetic is the thread's own inference from Farina's stated sinc mechanism,
not a number Farina states directly. **MLS vs ESS:** Farina 2000 states MLS "requires that the
excitation signal is tightly synchronised with the digital sampler" (p. 1) and is delicate under
nonlinearity/time-variance; ESS is "very robust to minor time-variance... and to mismatch between
the sampling clock of the signal generation and recording" (p. 1). **Unsynchronized clocks — the
single most important finding of this thread:** Farina 2007's §3.4 "Clock mismatch" states plainly
that "a tight synchronization between the playback clock and the recording clock is not required"
and that "even if two completely independent hardware devices are employed, and no clock
synchronization is employed, usually the impulse response obtained is perfectly clean" (p. 13),
with a worked worst-case skew of only "approximately 8.5 ms" for two totally unrelated consumer
devices — and shows that even that is correctable after the fact. **Source requirements:** neither
Farina paper discusses closed-box loudspeaker decay time at all (searched and confirmed absent);
the nearest real-world precedent is Rajmane & Baumann 2016 (§source 3, held), who used an ordinary
loudspeaker with sine-burst excitation and resolved echo timing to 60 µs — an existing, working
demonstration at far finer resolution than this thread needs.

**Q2. Time-of-arrival → geometry: accuracy, mic count, assumptions, unsynchronized mics addressed?**
Rajmane & Baumann 2016 (§3) is quoted in full with its lag→path-difference table (Table 3) and size
rule. Dokmanić et al. 2013 (§11) is the most permissive: 4–5 arbitrarily-placed mics, only pairwise
distances need be known, source position need not be known, and unsynchronized *source-vs-mic*
timing is explicitly named as solvable by citation (though not derived in this paper). Antonacci et
al. 2012 (§12) is the closest match to "unsynchronized" of anything retrieved: it has three named
scenarios explicitly covering unsynchronized source-and-receiver signals, with a real-room test run
with "no effort... to synchronize the recorded signals with the input stimulus" (5 mics, few-cm
accuracy) — but its array's own *relative geometry is assumed known* and nothing in it addresses
mic-to-mic (receiver-to-receiver) clock uncertainty, which is this thread's actual problem. The
seven held spherical/compact-array papers (Sun 2012, Mabande 2013, Lovedee-Turner & Murphy 2019,
Sprunck 2022, Hadadi 2024, Tervo 2013, Meyer-Kahlen 2022 — §§4–10) report DOA/position accuracies
from ~1° / ~1 cm (simulation) to ~15 cm RMS / ~1–5° (real rooms), using 4–32 microphones — but
**every one of the seven, without exception, sidesteps synchronization by using a single physical
compact array (one shared ADC)**, and not one of the seven contains any occurrence of "synchron-",
"clock" or "jitter" in its full text (confirmed by direct search of the fresh dumps). **No retrieved
source anywhere addresses an array of independently-clocked microphones aligned only by a trigger
onset** — the specific configuration this thread actually has.

**Q3. Cepstral echo detection vs. rahmonics; how to separate them.**
The 1963 Bogert/Healy/Tukey original could not be retrieved (access-restricted archive.org scan);
Oppenheim & Schafer 2004 (§13) and Randall 2013 (§14, conference precursor of the cited 2017 MSSP
paper) were retrieved as substitutes and both derive the mechanism explicitly: a single echo of
delay τ imprints a cosine ripple of period 1/τ on the log-spectrum (Oppenheim & Schafer's Eq. 1–3,
p. 95), and a harmonic/sideband family spaced at f0 imprints the *same kind* of ripple, at period
1/f0 (Oppenheim & Schafer p. 97–98; Randall's gearmesh-sideband example, p. 4) — so a rahmonic peak
alone cannot distinguish "real echo" from "harmonic family" by shape. Both sources' remedy is
identical and is stated as the field's standard technique, not a novel one: independently identify
the periodic source's fundamental from other information, then comb-lifter exactly that quefrency
and its multiples out (Randall p. 6, p. 12–13; Oppenheim & Schafer's low-pass-lifter example, p.
97), and treat what survives as the residual of interest. This directly validates the thread's own
prior judgement that 4.2 ms (=1/BPF) and 8.4 ms (=shaft period) are rahmonics to be removed, not
echoes to be read. Childers, Skinner & Kemerait 1977 could not be retrieved in any form (IEEE
Xplore-only, no OA mirror found anywhere after an exhaustive search) — no claim is made from it.

**Q4. ISO 26101 traverse aimed at a suspected reflector — what did they actually do?**
All four held papers were re-read in full and give four genuinely different variants, all directly
quoted in §§16–19: Cunefare et al. 2003 physically aimed one traverse at a specific suspected
feature (a wedge-basket-hinge/gap structure) "anticipating that [it] might generate reflections"
(p. 887), and separately used a fitted geometric parameter (source offset exceeding 2× the source
dimension) as a numeric red flag correlating with the worst traverses (p. 891). Nash 2019 instead
flagged the anomalous *tone* first (a physically-impossible −26.4 dB/doubling slope at 2056 Hz)
and inferred "a strong reflection from a nearby surface" without pinpointing which one (p. 1348),
while separately identifying and covering a known-by-design reflector (the floor grating) on
inspection alone. Rizzi et al. 2013 used the standard corner-aimed ISO 3745 traverse and attributed
low-frequency excess deviation there to "long wavelength sound reflecting from the corners of the
room" (PDF p. 10 of 18), plus a second traverse toward a TL test window that flagged the fiberboard
insert and opposite wall. Winker & Stahnke 2016 add a distinct and important variant: at high
frequency, the dominant suspect is often not a room surface at all but "the measurement system
[i.e. rig/stand] inside the free-field" (p. 7) — directly relevant since the thread's own Tyto
stand/arc structure is itself a candidate reflector.

**Q5. Fitting an image source to level data alone (no timing).**
Attenborough 2015 (§20) is the one paper retrieved on this exact family of technique (ground
impedance from level-difference/comb-filter spectra, ANSI S1.18/NT ACOU 104 lineage) and gives a
clear **negative** answer: the standard "template" method fits ground *impedance* from a *known,
fixed* source/receiver geometry — it does not invert the problem to recover an *unknown reflector's
position* from the interference pattern, and the paper contains no discussion, equation, or
citation addressing that inverse direction. No retrieved source anywhere describes fitting a
reflector's spatial position purely from level/comb-filter data without any timing information.

---

## Comparison with earlier notes

Applies to the twelve held papers re-read for this thread (protocol rule 2). "Agree" = every
number/quote checked against the fresh dump matched the earlier note; discrepancies are listed in
full.

- **Rajmane & Baumann 2016** (vs. `papers/small-chamber/EXTRACTS.md`): **agree** on every number
  checked (Tables 1–3, the size rule, the three verbatim quotes already on file). **Addition, not a
  correction:** the earlier file paraphrased the sine-burst/60 µs passage in prose rather than
  quoting it verbatim; this thread adds the exact quote (needed for Q1) and flags that the sentence
  is split by a column-order extraction artifact in the plain-text dump (both halves independently
  verified verbatim; page unaffected, both on p. 332).
- **Sun 2012** (vs. `papers/reflection-localization/MATRIX-3W.md`): **agree** — every number in
  Tables V/VI and both verbatim quotes (pp. 2835, 2837, 2839) re-verified character-for-character
  against the fresh dump, including the two page numbers.
- **Mabande 2013** (vs. same MATRIX): **one discrepancy.** The MATRIX cites "The positions of the
  walls... estimated precisely up to a few centimeters only" as "(Sec. VIII, p. 2789)". Re-checked
  against the fresh dump's own page-footer sequence (2785, 2786, 2787, 2788, then References begin
  on 2789): the sentence starts on **p. 2787** and its quoted continuation is on **p. 2788**, with
  the Acknowledgments (which conventionally follow the Conclusion) also on p. 2788 — p. 2789 holds
  only the reference list. The MATRIX's page number for this one quote should read 2787/2788, not
  2789. The other quote checked ("errors in boundary plane estimation are mainly due to...", p.
  2784) is confirmed correct as cited.
- **Lovedee-Turner & Murphy 2019** (vs. same MATRIX): **agree** on the Table III numbers (RMS 15.37
  cm / 1.21° / 23.02 cm, every wall/floor/ceiling cell) and the "comparable to prior work... 16.38
  cm... 6-64" quote. **Addition:** this thread adds the paper's own explicit bulleted assumptions
  list (manuscript p. 1, quoted in full above), which the MATRIX had summarised in prose but not
  quoted verbatim — needed directly for Q2's "what assumptions" question.
- **Sprunck 2022, Hadadi 2024, Tervo 2013, Meyer-Kahlen 2022** (vs. same MATRIX): **agree** — all
  numbers and quotes checked (recall/error figures for Sprunck; the two amplitude/delay quotes for
  Hadadi; the "strongest reflection in the window" and rationale-for-SDM quotes for Tervo, now also
  matched against its explicit 4-mic/non-coplanar/omni requirement passage which the MATRIX had
  paraphrased rather than quoted; the TDoA/PIV distinction and "temporal resolution is limited by
  array size" quote for Meyer-Kahlen) came back identical. Meyer-Kahlen's PDF page numbering
  extracts out of linear sequence in this specific file (confirmed by direct inspection: a "4" then
  a "1" appear where a monotonic count is expected) — the MATRIX did not cite page numbers for this
  paper either (section references only), so there is no conflict, but exact printed pages could not
  be independently established this session; cited here as "PDF p. N of 9" instead.
- **Cunefare 2003** (vs. `papers/anechoic-simulation/VERIFICATION-2026-09-07.md`, the only earlier
  note touching this paper): **agree** on the abstract quote (p. 881, exact wording) and the
  existence of the 56/13 Table IX numbers at the 80 Hz row. **New material added, not previously
  extracted under this campaign:** the "traverse toward the door... anticipating... reflections"
  quote (p. 887) and the Table X source-offset diagnostic quote (p. 891), both central to this
  thread's Q4 and not present in any prior extracts file. **Verification limit found:** the earlier
  note's "56% → 13%" framing (implying which method — optimal or fixed — produced which number)
  could not be confirmed from Table IX's plain-text layer, whose nested 8-column header extracts in
  a scrambled, non-hierarchical order; flagged as unclear in text in §16 above rather than resolved
  either way.
- **Nash 2019** (vs. same MATRIX row, `papers/anechoic-simulation/MATRIX-3W.md`): **two
  discrepancies, both the same off-by-one-page pattern.** The MATRIX cites both "Compared to bands
  of noise... not behaving like a free field" and "The squared correlation coefficients appear to
  be acceptable; however..." as "(§7, p. 1347)". Re-checked against this document's own explicit,
  unambiguous page-footer sequence (1343, 1344, 1345, 1346, 1347, 1348, 1349 — all found as clean
  standalone footer tokens): both quotes fall strictly **after** the "1347" footer and before the
  "1348" footer, i.e. they are on **p. 1348**, not 1347. All other Nash citations checked (the
  abstract quote p. 1343, the "wedges... impedance tube" and "absorptive but not anechoic" quotes p.
  1349) are confirmed correct as cited. **Addition:** this thread adds the "severe notch... strong
  reflection from a nearby surface" quote (also p. 1348), not previously extracted, which is the
  passage Q4 actually needed.
- **Rizzi 2013** (vs. `papers/chamber-problems/EXTRACTS-local.md`): **agree** on both quotes
  ("measurement microphones were close to the room corner..." and "adequate approximation of a
  free-field...") and the TL-window/fiberboard passage, all confirmed verbatim. This PDF has no
  extractable printed page numbers at all (checked exhaustively — every isolated digit found is a
  table/figure value); the earlier file did not cite page numbers either (used "p. 3.2" section
  reference), so there is no conflict, but this thread's own PDF-page-index citations ("PDF p. 10 of
  18") are new and not comparable to a prior page claim.
- **Winker & Stahnke 2016** (vs. `papers/chamber-problems/EXTRACTS-downloaded.md`): **agree** — both
  quotes used here ("the most likely factor is the influence of the measurement system...", p. 7;
  "a chamber can fully comply with ISO 3745... while not exhibiting free-field performance...", p.
  3) re-verified character-for-character at the pages already on file.

**Net effect on evidence quality:** one page citation in the Mabande 2013 row and two in the Nash
2019 row are corrected; every other number and quote checked from the held corpus stood up
unchanged. No claim in the earlier notes was found to be substantively wrong (misattributed
finding, wrong direction, fabricated number) — only page-reference slips, all traced to the
same underlying cause (this PDF family's two-column layout occasionally displacing a page-footer
token relative to the paragraph it belongs to, even under plain, non-`-layout` extraction).
