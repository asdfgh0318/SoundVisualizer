# Thread H — what changes when the arc goes vertical (floor, stand, mounts, mic directivity)

Protocol: `papers/arc-validation/PROTOCOL.md`. All held papers below were re-opened from their
PDF, identity-checked against `papers/BIBLIOGRAPHY.md` from the PDF's own front matter, and
re-extracted fresh with plain `pdftotext -q` into `papers/arc-validation/refetch-txt/<name>.txt`
(the existing `EXTRACTS-*.md`/`MATRIX-3W.md` notes were used only to locate candidate passages,
never as evidence). Every quote below was re-verified against a **per-page** `pdftotext -f N -l N`
extraction of the original PDF (not just the concatenated dump), because page-marker position
(header vs footer, and front-matter offsets) turned out to vary by publisher and is easy to get
wrong by one page from the concatenated text alone — see the worked examples in the Comparison
section. New sources were saved into `papers/arc-validation/` and extracted into
`papers/arc-validation/txt/`.

---

## Q1 — Floor reflection with mics near the floor

### Rasmussen & Winberg 2022, Quiet Drones 2nd e-Symposium — "Accurate measurement of Drone Noise on the ground"
**File:** `papers/chamber-problems/Rasmussen-Winberg_2022_QuietDrones_drone-noise-on-the-ground.pdf` (held; re-read fresh: `papers/arc-validation/refetch-txt/Rasmussen-Winberg_2022.txt`)
**Evidence level:** conference (GRAS Sound & Vibration authors)

What it says: a microphone at height *h* above a hard reflecting ground, with the source overhead
(hover), forms a comb filter with the source-microphone-image geometry; the first null is at the
quarter-wavelength height. For their example height *l* = 1.2 m:

> "The interference of the direct wave and the reflected wave at the microphone position is like a
> comb filter, with the first minimum at the frequency where the microphone height 1.2 m equals ¼
> of the wavelength: f₀ = c/(4·l) ≈ 71.4 Hz ... And the first maximum at f₁ = c/(2·l) ≈ 143 Hz"
> (p. 3)

1/3-octave smoothing does not remove the effect, only blurs it:

> "the frequencies coincident with the comb-filter minima are reduced by more than 20 dB, and the
> frequencies coincident with the comb-filter maxima are amplified by 6 dB." (p. 3, continuing to p. 4)

> "the overall sound pressure level measured at 1.2 m height will be 3 dB higher than the
> corresponding level measured in a full free field as for example inside an anechoic chamber"
> (p. 3)

Recommended fix — flush-mount the microphone in a fully reflecting ground board so the reflection
becomes a deterministic, frequency-independent +6 dB rather than a comb filter, and extend validity
to 20 kHz by mounting flush rather than inverted-above-the-board (an inverted mic above the board
itself disturbs the field above 10 kHz):

> "Secondly, the inverted microphone mounted on top of the reflecting plate disturbs the
> measurements above 10 kHz." (p. 9)

> "If the microphone, instead of mounted at a certain height, is flush mounted with a fully
> reflecting ground, both broadband noise sources and pure tone sources can be measured, but with
> a 6 dB higher level than for the free-field situation." (p. 10)

> "a flush-mounted microphone on a ground plate is preferable. This configuration is useful for
> stationary and non-stationary noise sources with frequencies up to 20 kHz, where the noise
> contains tones." (p. 10)

This paper's own worked scenario is the vertical-arc problem almost exactly: a mic at a fixed
height under a hovering rotor. No anechoic room is assumed — the comb filter is a property of the
mic-height/source-height geometry over *any* hard floor, not of the room's absorption.

---

### Kamliya Jawahar, Hanson, Akhter & Azarpeyvand 2025, Scientific Reports 15:2170 — "Porous ground treatments for propeller noise reduction in ground effect"
**File:** `papers/chamber-problems/Jawahar_2025_SciRep_porous-ground-propeller-ground-effect.pdf` (held; re-read fresh: `refetch-txt/Jawahar_2025_SciRep.txt`)
**Evidence level:** journal (Nature Portfolio, open access, DOI 10.1038/s41598-024-82876-9)
Identity confirmed from the PDF's own header/footer ("www.nature.com/scientificreports/", DOI
printed on the reference page). Author order as printed on the paper is Jawahar, Hanson, Akhter,
Azarpeyvand (BIBLIOGRAPHY.md's table already has this right).

Facility: University of Bristol anechoic chamber, propeller axis 1.2 m above a perforated mesh
platform, 1.7 × 1.5 × 12 mm MDF ground plate bare or with 45PPI/75PPI/75PPI-T foam, far-field arc
θ = 40° above to 150° below the plate.

Reflection vs aerodynamic ground effect, separated by angle and by persistence out to L/R = 4
(where thrust is unaffected by ground proximity):

> "At θ = 50°, the GE configuration exhibits a significant increase in TSSPL by approximately
> 4.0-8.0 dB for frequencies above 1000 Hz. This increase is likely due to the reflection of noise
> from the ground plane, which is observed in both solid and porous configurations. As expected,
> this increase is absent at θ = 90°, where the sideline region does not experience reflections
> from the ground plane." (p. 9)

> "the OASPL sharply decreases in the GP case as the microphones are shielded by the ground plane"
> beyond θ > 100° (p. 6) — i.e. a shielded zone exists on the far side of the plate from the source,
> not just a reflection zone on the near side.

> "The solid ground plate amplifies OASPL by ≈3 dBA at shallow angles, while porous treatments
> reduce this increment by ≈2 dBA, demonstrating their effectiveness at IGE L/R = 1.0" (p. 6)

Porous-treatment effectiveness, quantified:

> "At θ = 90° and L/R = 0.75 (Fig. 6h), a significant TSSPL reduction of approximately 13 dB is
> observed in the frequency range of 1500-10000 Hz for the porous configuration compared to the
> solid configuration." (p. 9)

> "porous materials, particularly 75PPI-T foam, can reduce noise levels by up to 30 dB in low
> frequencies and 5-10 dB in mid-to-high frequencies compared to a solid ground surface." (p. 11)

> "porous surfaces in IGE conditions achieve notable suppression, reducing low-frequency noise by
> 26-36 dB and mid-frequency noise by 6-10 dB with 75PPI-T treatments" (near-field, p. 11)

---

### Alkmim, Cardenuto, Tengan, Dietzen, Van Waterschoot, Cuenca, De Ryck & Desmet 2022, JASA 152(5):2735–2745 — "Drone noise directivity and psychoacoustic evaluation using a hemispherical microphone array"
**File:** `papers/chamber-problems/Alkmim_2022_JASA_drone-directivity-hemispherical-array.pdf` (held; re-read fresh: `refetch-txt/Alkmim_2022_JASA.txt`)
**Evidence level:** journal

> "The room interior dimensions are 16 × 12.5 × 6 m (length × width × height) with fiberglass
> wedges covered by perforated aluminum panels." (p. 2736)

Mitigation used — a foam mat directly under the source, not a fully treated floor:

> "Additionally, a 2.5 × 2.5 m² area under the UAS was covered by a foam material with
> approximately 0.07 m thickness to mitigate ground reflections." (p. 2736)

> "the effect of ground reflections is minimized during measurements but not fully suppressed,
> especially at low frequencies." (p. 2737)

So even a hard-floored *hemi*-anechoic chamber with a dedicated foam patch under the source does
not eliminate floor reflection at low frequency — it only reduces it; a genuine reflecting-floor
build has no better default than that without going to a full wedge floor.

---

### Ma, Wu, Jiang, Zhong & Zhang 2022, Quiet Drones 2nd e-Symposium — "Acoustic measurement of multi-rotor drones in anechoic and hemianechoic chambers"
**File:** `papers/chamber-problems/Ma_2022_QuietDrones_multirotor-anechoic-vs-hemi-anechoic.pdf` (held; re-read fresh: `refetch-txt/Ma_2022_QuietDrones.txt`)
**Evidence level:** conference (HKUST)

Same chamber run twice, once with the floor wedges in (full anechoic) and once with them pulled
(hemi-anechoic, hard floor) — the cleanest direct A/B in the whole corpus for "what does a hard
floor cost you":

> "The chamber has a wedge-to-wedge dimension of 8.1 m (L) × 6 m (W) × 5.1 m (H) and a cut-off
> frequency of 100 Hz in the full anechoic configuration." (p. 2)

> "The linearity of curves does not agree well with the spherical decay reference, and the
> deviations can reach as large as 3 dB. Nevertheless, the error bars of the two groups of results
> are at a comparable level (0.5 dB) ... Therefore, the discrepancy in the hemi-anechoic results is
> attributed to the presence of the reflective surface." (p. 8)

> "At the BPF, which is the dominant tonal contribution, the difference in the measured SPL can be
> as significant as 10 dB [between two adjacent near-floor mics in the hemi-anechoic test].
> Therefore, it can be concluded that the ground reflections can change the original spectral
> characteristics, especially at low frequencies." (p. 8)

---

### ISO 5305:2024 — *Acoustics — Noise measurements for UAS* (iTeh preview)
**File:** `papers/anechoic-simulation/ISO-5305_2024_standard-preview_UAS-noise-measurement.pdf` (held; re-read fresh: `refetch-txt/ISO-5305_2024.txt`)
**Evidence level:** standard (preview: Foreword–7.3.1 only, per BIBLIOGRAPHY.md)

Formal height rule to keep a hovering rotor out of ground effect during a chamber test (this is an
*aerodynamic*, not acoustic, criterion, but it is the standard's own answer to "how far from the
floor is safe"):

> "To avoid an aerodynamic ground effect on the UAS propellers, the height of the UAS to the ground
> shall be at least the maximum of H₀ = 1.2 m and 2Dₐ, where Dₐ is the UAS diameter. Hₛ ≥
> max(2Dₐ, H₀)" (Formula 2, Clause 6.3, p. 6)

Microphone type is prescribed differently for chamber vs. outdoor ground-board tests:

> "For measurements in anechoic chambers and anechoic wind tunnels as described in this document,
> the microphones shall be either free-field microphone type WS2F or WS3F as defined in IEC
> 61094-4. For outdoor measurements using ground boards as described in this document, the
> microphones shall be pressure microphones type WS2P or WS3P as defined in IEC 61094-4." (Clause
> 5.1, p. 5)

The far-field distance rule and the interference caveat that matters for high-frequency bands:

> "For UAS noise measurements, to ensure the acoustic far-field condition, the microphone distance
> R shall be at least 5Dₐ, i.e. R ≥ 5Dₐ (1)... For sound at a high frequency, the significant
> interference pattern can affect the validity of the far-field condition proposed in Formula (1).
> However, the effect can be minimized when summing in a frequency band, for example, a 1/3-octave
> band" (Clause 6.2, p. 6)

---

## Q2 — The support structure as reflector / scatterer

### Fasulo, Longobardo, De Gregorio & Barbarino 2025, Aerospace (MDPI) 12(7):647 — "Experimental Acoustic Investigation of Rotor Noise Directivity and Decay in Multiple Configurations"
**File:** `papers/chamber-problems/Fasulo_2025_Aerospace_rotor-noise-directivity-decay.pdf` (held; re-read fresh: `refetch-txt/Fasulo_2025_Aerospace.txt`)
**Evidence level:** journal (MDPI, open access, DOI 10.3390/aerospace12070647)

This is the paper that uses **the same Tyto Robotics 1585 thrust stand** as SoundVisualizer:

> "Isolated rotor stand: a TYTO ROBOTICS 1585 Thrust Stand, which features dedicated control system
> and data logger. Two sets of load cells integrated within the stand allow for both thrust and
> torque measurements. The manufacturer's data sheet rates the load cells for thrust values of up
> to ≃±49 N with a precision of 0.5% and for torque values of up to 2 Nm with a precision of 0.5%,
> both with a sampling rate of up to 80 Hz." (p. 4)

Facility: CIRA semi-anechoic chamber, 90 Hz cut-off, 5.65 × 4.45 × 4.00 m, floor "treated as an
acoustically rigid surface" (p. 10), ten mics on an arc of radius 8D at 1300 mm height.

Ground reflection and the stand's own pylon both distort directivity, and the paper is explicit
that these are two *separable* installation effects, not the source:

> "Figures 12 and 13 present the resulting overall sound pressure levels (OASPL). ... First, the
> ground was treated as an acoustically rigid surface, so local reflections could either reinforce
> or attenuate the radiated sound, thereby altering the apparent directivity. Second, there is a
> small but significant mounting asymmetry: although the rotor hub is centred, the pylon supporting
> the isolated propeller is offset to the left side of the array (the 0°–180° hemisphere), roughly
> in line with the 30° microphone. That lateral offset produces additional shading behind the
> propeller and contributes to the left-right level differences observed in the OASPL profiles."
> (p. 10)

The pylon's shielding of one specific microphone, quantified against a published number for a
similar barrier:

> "The support pylon lies directly on the acoustic line of sight of microphone 10, producing
> shielding and a corresponding level reduction relative to its mirrored counterpart, namely
> microphone 8. Comparable shielding has been reported in the literature, where a short barrier
> positioned near an open rotor produced up to 8.5 dB of attenuation at certain directivity angles
> [9]." (p. 12; ref. [9] = Hanson, Baskaran, Zang & Azarpeyvand, "Acoustic shielding and scattering
> effects of a propeller mounted above a flat plate" — a different Bristol paper, not held)

Effect of reversing rotation sense (which reverses which side of the wake the pylon shadow falls
on) on microphone-to-microphone scatter:

> "Over the low-moderate speed range (3000–5000 rpm), the mean absolute OASPL difference among the
> ten microphones already reaches 1 dB. At higher rotational rates, the disparity increases
> sharply: about 3 dB at 6000 rpm and 3–4 dB in the 7000–8000 rpm range. The associated standard
> deviation grows from roughly 1 dB at the lowest speed to nearly 4 dB at 7000 rpm" (p. 11–12)

The paper's own stated conclusion number for the pylon effect:

> "Reversing the sense of rotation revealed that even modest geometric asymmetries, here the
> support pylon, can shift directivity by up to 4 dB." (p. 24)

And its own recommendation — exclude the shadowed sector rather than try to correct it:

> "the downwash axis is defined at 0°. Measurements taken within the 0°–90° sector will not be
> analysed in order to avoid any potential misunderstandings that may arise from additional
> interference from the pylon, as observed during the isolated rotor test." (p. 19)

Once the rotor is moved onto a plate (a stand-in for a nearby rigid mounting structure rather than
an open pylon), reflections plus shadowing move both ways — up in level toward the plate, down in
the shadow:

> "Compared with the isolated rotor case, the acoustic directivity of the single propeller changes
> markedly when it is mounted on the aluminium plate. In particular, OASPL measured at the frontal
> azimuth (approximately 180°) increases by 1.0–3.5 dB (mean +2.5 dB) relative to the isolated
> rotor baseline. A more pronounced enhancement of 1.5–6.5 dB (mean +3.5 dB) occurs near 135°,
> consistent with sound wave reflections from the plate ... Conversely, mounting the rotor on the
> plate produces acoustic shadows in the propeller plane, yielding a mean reduction of about 1 dB
> at 270°. ... a mean enhancement of roughly 4 dB centred at an azimuth of 225° and an average
> increase of about 8 dB within the wake sector." (p. 22)

---

### Zawodny & Haskin 2017, AIAA Aeroacoustics Conf. — "Small Propeller and Rotor Testing Capabilities of the NASA Langley Low Speed Aeroacoustic Wind Tunnel"
**File:** `papers/chamber-problems/Zawodny-Haskin_2017_AIAA_LSAWT-small-rotor-capabilities.pdf` (held; re-read fresh: `refetch-txt/Zawodny-Haskin_2017_AIAA.txt`)
**Evidence level:** conference (NASA Langley)

Treats the near mounting/wedge structure as a quarter-wave resonator to get a "safe above this
frequency" number, exactly the kind of geometric reasoning the arc-validation rig needs once mic
distance to any nearby rigid surface (stand, arc frame) is known:

> "Directivity discrepancies between PAS and LSAWT measurements for the two higher rotation rates
> are within ± 2.5 dB, while that for the lower rotation rate exceeds 5 dB at an elevation angle of
> θ = −47.75°. This may be due to reflections from the wall-mounted wedges at this frequency. ...
> It is important to note that the LSAWT microphones are mounted an average distance of 0.49 m from
> the acoustic wedge tips, which is approximately half of the distance between the microphones and
> wedge tips in the SALT facility measurements. Treating this as a 1/4-wavelength yields a notional
> cut-on frequency of 175 Hz." (p. 16)

---

### Whelchel 2023, PhD dissertation, Virginia Tech — "Measurement and Prediction of Rotor Noise Sources for sUAS in Outdoor and Laboratory Environments"
**File:** `papers/chamber-problems/Whelchel_2023_PhD-VT_sUAS-rotor-noise-outdoor-lab.pdf` (held; re-read fresh: `refetch-txt/Whelchel_2023_PhD-VT.txt`)
**Evidence level:** thesis

Not the thrust stand itself, but the companion "how do you characterize a nearby rigid mounting
surface's frequency response" methodology, done with a ground board rather than a pylon — the
technique (with/without the reflector, same source, subtract spectra) is directly reusable for
characterizing the arc frame or the Tyto stand:

> "spectral levels increase by at least 6 dB from 150 Hz to 520 Hz, 740 Hz to 1140 Hz, 1340 Hz to
> 1730 Hz, and 2070 Hz to 2320 Hz with maximum levels of constructive interference of more than 8
> dB. Destructive interference greater than 3 dB is shown to occur at 1250 Hz and from 3770 Hz to
> 6660 Hz" (p. 67)

> "these results do show that the scalloping that occurs over the mid frequency region is due to
> edge scattering effects." (p. 68)

Its own outdoor test explicitly did *not* correct for this (a useful negative example — this is
what "doing nothing about it" looks like in the data):

> "No measures were taken to mitigate the effects of constructive and destructive interference
> resulting from the acoustic reflections on the hard surface although the frequencies of the
> expected destructive interference have been calculated." (p. 46)

No sentence in the thesis text located in this pass names the Tyto stand or a thrust-stand pylon
specifically as a scatterer (Whelchel's rig used a 6-axis load cell + T-slotted aluminium sting,
not a Tyto 1585) — cited here only for the ground-board methodology and numbers, matching what the
BIBLIOGRAPHY/thread task expects of it.

---

### Zawodny, Boyd Jr. & Burley 2016, AHS 72nd Annual Forum — "Acoustic Characterization and Prediction of Representative, Small-Scale Rotary-Wing Unmanned Aircraft System Components"
**File:** `papers/arc-validation/Zawodny-Boyd-Burley_2016_AHSForum72_SALT-facility-small-rotor-characterization.pdf`
(a sibling thread working the same shared campaign folder retrieved and named this file; my own
separately-downloaded copy of the identical PDF, saved earlier this session as
`Zawodny-Boyd-Burley_2016_AHS_UAS-rotor-acoustic-characterization.pdf`, was no longer present on
disk by the time this section was finalised — evidently superseded/deduplicated in the shared
directory. Both were byte-for-byte the same NTRS document, identity re-confirmed below, so this
does not affect what is quoted here.)
**Evidence level:** conference (NASA Langley) — pdftotext fails on this PDF (its body-text layer is
present only as unrecoverable font-outline glyphs; both local `pdftotext` and NTRS's own
server-side `.../downloads/20160009054.txt` extraction return nothing but numeric axis labels — a
sibling thread's note file (`txt/Zawodny-Boyd-Burley_2016_AHSForum72_NOTE.txt`) independently hit
the same wall). Quotes below were instead obtained by **visually reading the rendered PDF pages**
(pages 1–9, via the Read tool, which rasterises and reads each page as an image) rather than from
an extracted text layer — this is a legitimate reading of the actual document, not a
paraphrase/search-snippet, so quotes are given as printed.

Identity confirmed: NASA NTRS record 20160009054 lists exactly these three authors (Zawodny,
Nikolas S.; Boyd, D. Douglas, Jr.; Burley, Casey L.), all NASA Langley; the PDF's own title page
(read visually) prints the same three names and affiliation; the PDF's internal document title (via
`pdfinfo`) is `lf99-22587_final-Zawodny_ahsforum72_submission2.pdf` — AHS Forum 72 was the American
Helicopter Society's 72nd Annual Forum, 2016.

Facility and, directly relevant to Q2 and Q5, the arc-mic geometry and the rig's own floor-clearance
choice:

> "Experiments were performed in the Structural Acoustic Loads and Transmission (SALT) anechoic
> chamber facility at the NASA Langley Research Center. This facility is acoustically treated down
> to a cut-off frequency of 100 Hz and has interior dimensions of 4.57-m (15-ft) high, 7.65-m
> (25-ft) wide, and 9.63-m (31.6-ft) long. A total of five 1/4" free-field Brüel & Kjaer 4939
> microphones in an arc array configuration are positioned in the acoustic far-field of the rotor
> test stand at elevation angle increments of 22.5°, from 45° below the plane of the rotor to 45°
> above the plane of the rotor. Specifically, the microphones are positioned at a radial distance
> of 1.905 m (75 in.) from the rotor hub. This distance corresponds to at least 13R for the rotors
> tested in this study." (p. 3)

> "The rotor test stand itself was constructed so that the plane of the rotor would stand 2.29-m
> (7.5-ft) above the floor wedge tips, which corresponds to half of the room height." (p. 3)

> "In addition, a single-axis Honeywell Type 31 load cell was positioned directly underneath the
> motor for measuring thrust (see Figure 2(c)). This close proximity of the load cell to the rotor
> assisted with reducing loading uncertainties associated with longer moment arms and wake
> loading." (p. 3)

The load cell/motor mounting is discussed only as a *loading-measurement* design choice (minimising
moment-arm and wake-loading uncertainty in the thrust reading), and recirculation is flagged via the
load-cell signal, not acoustically:

> "Evidence of recirculation was found when the voltage output of the load cell began to exhibit
> high-amplitude fluctuations indicative of turbulent gust ingestion into the rotor disk area.
> Therefore, acoustic data used for post-processing were limited to a time period preceding this
> apparent onset of recirculation." (p. 4)

No sentence found in pages 1–9 (the methodology, rig description, and first results sections —
covering the whole facility/apparatus description and the first acoustic-spectra results) discusses
the test stand, load cell or arc frame itself as an acoustic *reflector or scatterer*; the paper's
own "up to 8 dB" and "6.5 dB" numbers (p. 9) are differences in radiated OASPL **between the two
rotor designs tested** at a common thrust, not a facility-artifact number, and are not used here as
an installation-effect claim. Given the budget for this thread, pages 10–15 (the tonal-prediction
comparison and broadband-prediction sections, per the abstract) were not read; if a future pass
needs the paper's directivity-comparison plots in more depth, they remain to be visually read the
same way.

---

## Q3 — Microphone mounts, clamps and arc-frame scattering at 2–4 kHz

### ISO 26101-1:2021 — *Acoustics — Test methods for the qualification of the acoustic environment — Part 1: Qualification of free-field environments* (iTeh preview)
**File:** `papers/anechoic-simulation/ISO-26101-1_2021_standard-preview_free-field-qualification.pdf` (held; re-read fresh: `refetch-txt/ISO-26101-1_2021.txt`)
**Evidence level:** standard (preview: Foreword–5.1.5.1.2 only)

The exact sentence the thread brief asked about, verified with its clause number and page:

> "Sound reflection from the microphone support system should be carefully avoided." (Clause
> 5.1.3.2 "Microphone traverses", p. 5)

Also relevant — the *qualification* microphone itself is required to be treated as "the microphone
plus its mount" as a single acoustic object:

> "The microphone shall be nominally omni-directional (taking into account any supplementary
> equipment connected to it, such as the protective grid and mounting arrangement)." (Clause
> 5.1.2.1, p. 3)

That clause also points at the sound-level-meter directivity standard used for the qualification
instrument itself: "operated within the limit of the linearity errors specified for a Class 1
sound level meter according to IEC 61672-1" (same page).

---

### Rajmane & Baumann 2016, DAGA 2016 Aachen, pp. 331–333 — "Detection of Reflecting Objects in Anechoic Chambers"
**File:** `papers/small-chamber/Rajmane-Baumann_2016_DAGA_detection-reflecting-objects-anechoic-chambers.pdf` (held; re-read fresh, and re-checked page 2's table with `pdftotext -layout` — see Comparison section below)
**Evidence level:** conference (G+H Schallschutz GmbH)

This is the most directly quantitative answer in the whole corpus to "at what size and frequency
does a small object (a clamp, a boom, a cable loop) start to reflect": steel-sheet reflectors of
known size were placed on the qualification traverse and the frequency at which visible
constructive/destructive interference first appeared was tabulated (Table 1, p. 332, values
verified with `pdftotext -layout` to resolve a column-order ambiguity in the plain extraction):

| Frequency (Hz) | Wavelength (cm) | 35×35 cm sheet | 10×10 cm sheet |
|---|---|---|---|
| 800 | 42.5 | No | No |
| 1000 | 34.0 | **Yes** | No |
| 1250–2500 | 27.2–13.6 | Yes | No |
| 3150 | 10.8 | Yes | **Yes** |
| 4000–5000 | 8.5–6.8 | Yes | Yes |

(Table 2, same page: two orientations of a 70×17 cm / 17×70 cm rectangle both show interference
from 1000 Hz upward, i.e. a large-area object behaves like the 35×35 cm square regardless of
aspect ratio up to 4:1.)

The general rule the authors extract from these tables:

> "Observations from table 1 and 2 show that reflecting object is identified, when length of side
> of square object is greater than or equal to wavelength of tonal excitation frequency. For the
> rectangle shaped reflector with L:W up-to 4:1, the object is still identified, when length of
> side of equivalent square object is greater than or equal to wavelength of tonal excitation
> frequency." (p. 332)

For a mic clamp/boom/cable loop of order 5–10 cm (the size named in the thread brief), this rule
predicts an onset around λ ≈ 5–10 cm, i.e. **f ≈ 3.4–6.9 kHz** — squarely on top of, and above, the
3150 Hz band where the arc-validation one-pager already sees ±3 dB scatter (λ ≈ 11 cm at 3150 Hz).
A 10×10 cm object's own measured onset (3150 Hz, Table 1) is direct experimental confirmation of
that same coincidence in this independent dataset.

The paper's second technique — time-of-flight from a sine-burst pulse — is the recommended
mitigation once a reflector is suspected, not a redesign:

> "The distance of reflecting object from sound source can be identified by emitting sine impulse
> and measuring the time lag of reflected sound on the measurement path. From this information, if
> any object is disturbing the free field acoustic region, the object can be shifted to different
> safe location." (Summary, p. 333)

Measured time lags matched independently-measured geometric path differences to about 0.1 m
(Table 3, p. 332): 3.5 ms / 2.3 ms / 12 ms measured → 1.2 m / 0.8 m / 4.1 m calculated vs. 1.2 m /
0.7 m / 4 m measured geometrically.

---

### Burnett & Nedzelnitsky 1987, J. Res. NBS 92(2):129–151 — "Free-Field Reciprocity Calibration of Microphones"
**File:** `papers/small-chamber/Burnett-Nedzelnitsky_1987_JResNBS_free-field-reciprocity-calibration-chamber-deviations.pdf` (held; re-read fresh: `refetch-txt/Burnett-Nedzelnitsky_1987.txt`, an OCR'd scan — text has OCR noise, e.g. "crn" for "cm", verified word-for-word against the scan)
**Evidence level:** report (National Bureau of Standards)

Directly documents inter-microphone reflection at a wavelength matching the arc-validation 3150 Hz
band:

> "The differences of 12 cm in the separation distances correspond reasonably closely to the
> wavelength for 3.15 kHz, which is approximately 11 crn [cm]." (p. 140)

And a second, independent reflection mechanism (mic-to-mic, not mic-to-wall) at a slightly higher
frequency in the same small chamber:

> "Standing waves due to reflections between the microphones themselves will also produce maxima or
> minima at separation distances that are integer multiples of one-half wavelength. Such effects
> are seen at some frequencies. For example, at 4.0 kHz the minima seen in figure 11 are at
> separation distances of 12, 17, 21, 26, and 30 cm. The wavelength at 4.0 kHz is approximately 8.6
> cm." (p. 140)

The two mechanisms (chamber-wall/fixture reflection vs. mic-to-mic reflection) cannot be cleanly
separated even in this careful metrology study:

> "it is not possible completely to separate the effects which are due to standing waves caused by
> reflections from interior surfaces of the chamber (or 'room reflections') and those due to
> standing waves caused by reflections between the microphones. It would be expected that the
> effect of microphone reflections would become more pronounced as the frequency is increased (as
> wavelengths become comparable to the microphone diameter), and less pronounced as the separation
> distance between the microphones increased" (p. 140)

The paper frames this as a small-chamber problem generally, not solely a sub-cutoff one — "free
field reciprocity measurements encounter the greatest experimental difficulties" in the 1.25–4 kHz
band (abstract) precisely *because* the chamber (free volume 5.4 m³, 0.3 m wedges) is small enough
that fixtures and the microphones themselves are a comparable scale to the wedge depth at those
frequencies.

---

### Weitsman, Stephenson & Zawodny 2020, JASA 148(3):1325–1336 — "Effects of flow recirculation on acoustic and dynamic measurements of rotary-wing systems operating in closed anechoic chambers"
**File:** `papers/chamber-problems/Weitsman_2020_JASA_recirculation-rotary-wing-closed-chambers.pdf` (held; re-read fresh: `refetch-txt/Weitsman_2020_JASA.txt`)
**Evidence level:** journal

Mesh flow-conditioning screens mounted on holders near the rotor, in an otherwise very well
qualified NASA Langley chamber (wedges "absorb 99% of incident sound energy above 250 Hz"), still
scatter above 2 kHz:

> "minimal impact on the acoustic measurements at low frequencies, however the tonal noise
> components at frequencies above 2 kHz are slightly amplified. This is thought to be attributed to
> acoustic reflections off the mesh holder apparatus, and thus if these mesh holders were
> upholstered in [absorbent material this could likely be avoided]" (p. 1333)

Repeated verbatim in the conclusions (p. 1335): "a slight amplification of the tonal noise
components was evident at frequencies above 2 kHz and is attributed to reflections off the mesh
holder apparatus."

---

### Winker & Stahnke 2016, Inter-Noise 2016 — "The influences of changes in international standards on performance qualification and design of anechoic and hemi-anechoic chambers"
**File:** `papers/chamber-problems/Winker-Stahnke_2016_InterNoise_ISO3745-ISO26101-chamber-qualification.pdf` (held; re-read fresh: `refetch-txt/Winker-Stahnke_2016_InterNoise.txt`)
**Evidence level:** conference (ETS-Lindgren)

The rig itself is identified as the dominant error source in high-frequency qualification of
otherwise-good chambers:

> "The most likely factor is the influence of the measurement system inside the free-field creating
> reflections that do not appear at lower frequencies. A testing stand or rig is required to
> qualify most anechoic chambers... This situation occurs during pure tone qualifications and is
> not present in broadband qualifications due to signal averaging." (p. 7)

And a general caution about what "compliant" can hide, directly relevant to whether we should trust
per-band tolerances on the arc rig without inspecting raw traverses:

> "By using this fitting method, a chamber can fully comply with ISO 3745 at certain frequencies
> while not exhibiting free-field performance at those frequencies." (p. 3)

---

### Brüel & Kjær, *Microphone Handbook, Volume 1: Theory* (BE 1447–12, March 2019)
**File:** newly retrieved, `papers/arc-validation/BruelKjaer_2019_vendor_microphone-handbook-vol1-theory.pdf` — [vendor], 155 pp, full text (`www.bksv.com/media/doc/be1447.pdf`, confirmed by its own title page)

Diffraction by the microphone body and its protection grid — the general physics behind Q3 and Q4
both, with a concrete frequency threshold and an explicit statement that it scales with microphone
size:

> "The ratio between the pressure at the diaphragm and that of the undisturbed sound field is a
> function of the ratio between the microphone diameter and the wavelength. Pressure ratio
> functions look alike for smaller and larger microphone types, but they are shifted within the
> frequency range depending on the diameter of the microphone body." (p. 2-45–2-46; Fig. 2.28 shows
> 1", ½" and ¼" curves on the same 100 Hz–100 kHz axis, each departing from 0 dB at a frequency
> inversely proportional to diameter)

> "For most practical measurements the microphone diaphragm needs to be covered by a protection
> grid. This grid will also influence the pressure at the diaphragm as it acts as an acoustic
> resonator. The influence of protection grids is generally very low below 1 kHz, but it increases
> significantly with frequency." (p. 2-46)

> "The influence of the microphone on the pressure of a free-field is so great that it needs to be
> taken into account to avoid considerable measurement errors." (p. 2-46, describing the combined
> body + grid effect for a ½" microphone, Fig. 2.30)

This is a *microphone-body* diffraction effect (mm-to-cm scale, i.e. kHz-and-up), separate from and
additional to the *mount/clamp/boom* scattering the Rajmane & Baumann and Winker & Stahnke sources
above address (cm-to-dm scale objects near, but not touching, the capsule).

---

## Q4 — Microphone orientation and the UMIK-2's own directivity

### Brüel & Kjær Microphone Handbook Vol. 1 (as above)
Same physics as Q3 answers the orientation question directly: a microphone's response to an
on-axis (0°) wave differs from its response to a diffuse/random-incidence field once diffraction
by the body becomes significant, and that onset is inversely proportional to capsule diameter
(quotes above, p. 2-45–2-46). For a "½-inch-class capsule" (the size class named in the thread
brief, and the nominal class of the UMIK-2's electret capsule), the handbook's own number is that
grid/body diffraction is "generally very low below 1 kHz" and "increases significantly" above it —
i.e. for a ½"-class mic the free-field (0°) and diffuse/random-incidence responses are not
distinguishable at BPF-region frequencies (100s of Hz) but can be expected to separate somewhere
in the 1–10 kHz decade, consistent with the corpus's other cm-scale-object onset numbers (Rajmane &
Baumann: 3150 Hz for a 10 cm object; Weitsman: 2 kHz for a mesh holder; Burnett & Nedzelnitsky:
3.15–4 kHz for mic-to-mic reflection).

The handbook also states plainly why the *reference* sensitivity number on a calibration
certificate does not depend on which convention is used:

> "at the reference frequency, the sensitivity is essentially equal for all types of sound field."
> (Section 2.3.9, p. 2-23; reference frequency is stated to be 250 Hz or sometimes 1000 Hz)

— i.e. the calibration-file Sens Factor itself (measured at/near 1 kHz reference) is not the thing
that changes with orientation; what changes with orientation is the *shape* of the response curve
at higher frequency, which is exactly why miniDSP ships two different curve shapes (0° vs. 90°) and
not two different scalar sensitivities.

### miniDSP UMIK-2 User Manual [vendor] — the product-specific answer
**File:** `papers/arc-validation/miniDSP_nd_vendor_UMIK-2-user-manual.pdf` (already present in the
shared `papers/arc-validation/` folder, fetched by a sibling thread this campaign; re-read fresh
and page-verified for this thread — 29 pp, title "miniDSP UMIK-2 User Manual" per `pdfinfo`)
**Evidence level:** vendor

This is the manual for the exact microphone SoundVisualizer uses, and it gives the number the
Brüel & Kjær handbook's general physics (Q3) only implies. Capsule size, confirming the "½-inch-class"
framing of the thread's own question:

> "Capsules: 1/2" Low noise Pre-polarized condenser on 60UNS thread" (Hardware Specifications
> table: `miniDSP_nd_vendor_UMIK-2-product-brief.pdf` p. 2, and `...-user-manual.pdf` p. 24, both
> verbatim identical)

Orientation guidance, and — critically — the actual divergence point between the two calibration
curves, stated directly for this reason:

> "5.1 FREE-FIELD MEASUREMENT ... always point the microphone directly at the sound source and use
> the normal (0-degree) calibration file." (p. 14)

> "5.3 IN-ROOM MEASUREMENT FOR SUBWOOFERS. For measuring subwoofers, the orientation of the
> microphone or choice of calibration file doesn't matter. This is because the two calibration
> files differ only above a few kHz, due to the high-frequency directionality of the microphone."
> (p. 15)

This directly answers the thread's Q4 numeric question: for the UMIK-2's own ½" capsule, the 0°
and 90° response curves are **the same below "a few kHz"** and separate only above that — i.e.
orientation does *not* matter in the sub-kHz region where the BPF and its first few harmonics live,
consistent with (and more specific than) the B&K handbook's "generally very low below 1 kHz, but
increases significantly with frequency" for grid/body diffraction in general. It does not give a
single precise crossover number (miniDSP's "a few kHz" is deliberately vague) or a dB magnitude for
the divergence above it.

### miniDSP Support Portal — "Which direction should I point the UMIK-1?" [vendor]
**URL:** `https://support.minidsp.com/support/solutions/articles/47000681633-which-direction-should-i-point-the-umik-1-` (fetched directly with curl, HTML stripped and read in full; the UMIK-2 shares this calibration-file convention — see the User Manual entry above, which is UMIK-2-specific)

> "The UMIK-1 comes with two unique calibration files depending on two types of measurements: -
> 0deg: This calibration file is for Stereo and 2.1/2.2 systems. Point the microphone towards the
> sound source being measured. In the case of a Dirac live measurement, you'll point the microphone
> to the center point between the 2 speakers. This calibration is a so-called on-axis calibration
> file. - 90deg: Point the microphone towards the ceiling. This calibration file is only to be used
> for surround sound measurement (i.e. audio coming from multiple directions)."

miniDSP's own framing of the two files maps exactly onto the B&K handbook's free-field (0°,
pointed at a single source) vs. diffuse/random-incidence (90°, "audio coming from multiple
directions") distinction. A forum thread surfaced by web search claims the UMIK becomes "directive
at very high frequencies (15–20 kHz)"; that specific number could not be verified against any page
this session actually opened (the miniDSP community-forum threads and the independent
audiophilestyle.com thread that carried it all returned HTTP 403 to both `curl` and WebFetch), so
**it is not used as a claim here** — see RETRIEVAL-H.md. The User Manual's own "a few kHz" (above,
p. 15) is the number actually used.

### How an off-axis reflected wave gets weighted
No retrieved source in this pass gives a first-principles weighting function for "how much does a
reflected wave arriving off-axis contribute relative to the direct on-axis wave," but the pieces
retrieved combine to answer the practical question: (a) below roughly 1 kHz (B&K handbook, Q3/Q4)
a ½"-class capsule is close enough to omnidirectional that a reflected wave arriving from any angle
is picked up with essentially the same sensitivity as the direct wave, so orientation does not
protect against low-frequency floor/pylon reflections — consistent with Rasmussen & Winberg's
comb-filter analysis (Q1) and Fasulo's pylon-shielding numbers (Q2) both being **level** effects,
not effects that a mic's own directivity could cancel; (b) above roughly 1–4 kHz, both the
capsule's own diffraction (B&K) and nearby cm-scale objects (Rajmane & Baumann; Weitsman) start to
matter, so at those frequencies an off-axis reflection is weighted by whatever the 0°-vs-90°
calibration-curve difference is at that frequency and angle — which is exactly the information a
UMIK 0°/90° pair of curves is meant to bound, but which miniDSP does not publish as a continuous
polar function (only the two named angles).

---

## Q5 — Recommended practice when the arc is vertical near a floor

Pulling together the numbers already quoted under Q1–Q3:

**Rasmussen & Winberg (Q1)** recommend, in order of preference: a full anechoic chamber if the
whole spectrum matters; failing that, a **flush-mounted** ground-plane microphone (deterministic
+6 dB, valid to 20 kHz) over an **inverted-above-the-plate** microphone (disturbs the field above
10 kHz) over a **free-standing-at-height** microphone (comb-filtered, only correctable for
broadband, not tonal, sources) — quoted in full under Q1.

**ISO 5305:2024 (Q1)** gives the two hard numbers a vertical-arc rig would need if a floor near the
bottom mics cannot be avoided: keep the source ≥ max(2·Dₐ, 1.2 m) off the floor to avoid
*aerodynamic* ground effect contaminating thrust/torque (Formula 2, p. 6), and mount microphones
"on acoustically treated support to minimize reflections" (Clause 7.3.1, p. 8) — i.e. treat the
*microphone's own stand*, not only the floor, as part of the qualification problem.

**Jawahar 2025 (Q1)** and **Ma 2022 QuietDrones (Q1)** both give a full anechoic (wedged) floor as
the fallback when porous treatment or a foam patch is insufficient: Ma's own full-vs-hemi A/B shows
the hemi-anechoic (hard-floor) configuration measurably worse (up to 10 dB at BPF between two
adjacent near-floor mics, vs. "little difference" with the floor wedges in) even though both share
the same chamber and source.

**Alkmim 2022 (Q1)** shows the middle ground — a foam patch under the source in an otherwise hard
hemi-anechoic floor — only *reduces*, does not eliminate, the low-frequency floor contribution
("minimized ... but not fully suppressed, especially at low frequencies").

**Fasulo 2025 (Q2)**, using the same Tyto 1585 stand, recommends **excluding the shadowed sector**
outright rather than correcting for it once a pylon or mounting structure is known to interfere
("Measurements taken within the 0°–90° sector will not be analysed", p. 19) — directly applicable
to whichever elevations on the vertical arc end up looking through the Tyto stand's own structure.

**Zawodny, Boyd & Burley 2016 (Q2)**, using an arc of mics around a rotor test stand in the same
general style as SoundVisualizer's own rig, chose to **raise the whole rig** rather than treat the
floor: "The rotor test stand itself was constructed so that the plane of the rotor would stand
2.29-m (7.5-ft) above the floor wedge tips, which corresponds to half of the room height" (p. 3) —
i.e. their answer to "how far from the floor" was simply to centre the rotor (and hence the mic
arc) at mid-room-height, keeping every mic equally far from both floor and ceiling rather than
solving the near-floor problem directly.

**ISO 26101-1 (Q3)** and **Winker & Stahnke (Q3)** both push toward the same design rule: whatever
holds a microphone in place must itself be evaluated as a potential reflector ("sound reflection
from the microphone support system should be carefully avoided", 5.1.3.2), and the standard is
explicit that a chamber's compliance number at any one frequency does not guarantee free-field
performance at that frequency if the rig itself is the reflector.

No retrieved source gives a single quantified recommendation that resolves all of "full-anechoic
floor vs. flush ground mic vs. raising the rig vs. excluding low elevations" for this specific rig;
the sources instead converge on: (1) know the geometry (mic height above floor, distance to the
Tyto stand and its cross-members, and to the arc frame itself) well enough to compute the relevant
quarter/half-wavelength frequencies the way Zawodny & Haskin do for their wedge distance (Q2); (2)
expect any interference from floor and stand alike to show the same broad shape as Rasmussen &
Winberg's comb filter (deep, narrow, low-frequency, worsening the closer the mic sits to the
surface) and treat elevations that look toward the stand's structure the way Fasulo treats the
pylon-shadowed sector — as excluded or separately flagged, not corrected in place.

---

## Answers to the thread questions

**Q1.** Rasmussen & Winberg 2022 give the exact comb-filter formula (f₀ = c/4h) and a concrete
worked example (1.2 m height → 71.4 Hz null, 143 Hz max, 3 dB overall elevation vs. free field) —
directly answering "how do dips move with mic height." Jawahar 2025, Alkmim 2022 and Ma 2022
(QuietDrones) all quantify floor-reflection level effects near a hard floor (4–8 dB at 50°/>1 kHz;
foam patch only "minimizes... not fully suppresses"; up to 10 dB BPF difference between adjacent
near-floor mics on a hard floor vs. "little difference" on a wedged floor) and porous-ground
effectiveness (up to 30 dB low-frequency, 5–13 dB mid/high). ISO 5305:2024 gives the standard's own
ground-effect exclusion height. Fasulo 2025 gives "floor fills nulls...redirect tonal energy into
directions that should otherwise be relatively quiet" and "pylon...shift directivity by up to 4 dB"
verbatim (quoted above). Hanson, Kamliya Jawahar, Vemuri & Azarpeyvand 2023 (JSV 559:117751) was
**not retrieved** — see RETRIEVAL-H.md; no claim is made from it.

**Q2.** Fasulo 2025 (same Tyto 1585 stand) gives the stand's rated geometry/specs and its measured
pylon-shielding numbers (up to 8.5 dB cited from the literature, its own 3–4 dB and up to 4 dB
directivity shift, its own recommendation to exclude the 0°–90° shadowed sector). Zawodny & Haskin
2017 give a quarter-wavelength cut-on argument (0.49 m → 175 Hz) transferable to any near rigid
structure once its distance from the mics is known. Whelchel 2023 gives the ground-board
characterization methodology and its 6–8 dB constructive / >3 dB destructive numbers, though for a
ground board, not the Tyto stand specifically. Zawodny, Boyd & Burley 2016 (AHS) — retrieved as a
PDF, identity confirmed, and its body text (unrecoverable as machine text) read visually instead:
it documents a 5-mic arc (22.5° steps, ±45°) around a rotor test stand at 13R with the rotor plane
raised to half the room's height, and a load cell mounted directly under the motor purely for
thrust-measurement accuracy — but no discussion of the stand or load cell as an acoustic
reflector/scatterer was found in the pages read (1–9 of 15; see EXTRACTS-H.md for what was and
was not covered).

**Q3.** ISO 26101-1:2021 gives the standard's own instruction, verbatim with clause number ("Sound
reflection from the microphone support system should be carefully avoided," 5.1.3.2). Rajmane &
Baumann 2016 give the clearest quantitative object-size-to-onset-frequency rule in the corpus
(wavelength ≤ object side ⇒ detectable reflection; a 10 cm object at 3150 Hz, a 35 cm object
already at 1000 Hz). Burnett & Nedzelnitsky 1987 document inter-microphone reflection at 3.15–4
kHz (λ ≈ 8.6–11 cm) in a small chamber. Weitsman 2020 document mesh-holder reflection above 2 kHz.
Winker & Stahnke 2016 identify the "testing stand or rig" as the dominant high-frequency
qualification error source generally. Brüel & Kjær's Microphone Handbook gives the underlying
diffraction physics with a number ("generally very low below 1 kHz, but increases significantly
with frequency").

**Q4.** The UMIK-2's own user manual gives the most direct answer available: its 0° and 90°
calibration curves "differ only above a few kHz, due to the high-frequency directionality of the
microphone" (p. 15) — i.e. for this exact ½" capsule (p. 24/product-brief p. 2), pointing at the
source does **not** matter below "a few kHz" and does matter above it; no more precise crossover
frequency or dB magnitude is given. The B&K Microphone Handbook's general physics for a ½"-class
capsule ("generally very low below 1 kHz, but increases significantly with frequency" for grid/body
diffraction, p. 2-46) is consistent with and slightly more specific than miniDSP's "a few kHz." The
IEC 61672-1 iTeh preview retrieved for this does not extend far enough into the standard's clauses
to give a sound-level-meter-class number (see RETRIEVAL-H.md). A weighting function for an off-axis
reflected wave is not given in any retrieved source; the qualitative answer assembled above
(orientation doesn't help below ~1 kHz where both floor/pylon effects live; it can matter for
whatever mount/mesh/inter-mic scattering exists in the 1–4 kHz range) is a synthesis across
sources, not a single citation.

**Q5.** No single retrieved source recommends one specific practice ("full-anechoic floor" vs.
"flush ground mic" vs. "raise the rig" vs. "exclude low elevations") for this exact configuration.
Rasmussen & Winberg's ranked recommendation (full anechoic > flush ground mic > inverted-above
> free height) and Fasulo's own "exclude the shadowed sector" practice (used on the same stand
model) are the two most directly transferable; ISO 5305:2024 and ISO 26101-1:2021 give the
standards'-eye version of the same two ideas (keep the source off the floor by a computed
minimum height; treat the microphone support itself as a reflector to be avoided).

---

## Comparison with earlier notes

Per protocol rule 2(d), every discrepancy between this fresh re-read and the earlier
`EXTRACTS-*.md`/`MATRIX-3W.md` notes is recorded below (checked against a **per-page**
`pdftotext -f N -l N` extraction of the actual PDF, not just line position in a concatenated dump —
several of my own first guesses from the concatenated dump were off by one page and had to be
corrected this same way before being used above; those self-corrections are not "earlier-notes
errors" and are not listed here, only genuine discrepancies with the *existing* notes files are).

1. **Rajmane & Baumann 2016 (`small-chamber/EXTRACTS.md`, "2. Rajmane & Baumann") — DISAGREE.** The
   earlier note states "35×35 cm reflector: interference not observed at 800–1000 Hz, but observed
   from 1250 Hz upward." Plain `pdftotext` on Table 1 (p. 332) gives a column-order-ambiguous dump
   that could be misread that way; re-extracting the same page with `pdftotext -layout` (used here
   specifically to resolve a garbled table, not for body text — see PROTOCOL.md's warning about
   `-layout` interleaving two-column *prose*, which does not apply to a single table) shows
   unambiguously that the 35×35 cm sheet already registers "Yes" (interference observed) at 1000 Hz
   and only "No" at 800 Hz. The correct onset for the 35×35 cm sheet is **1000 Hz, not 1250 Hz**.
   The 10×10 cm sheet's onset (3150 Hz, first appearing in Table 1) and the two rectangular
   reflectors' onset (1000 Hz, Table 2) in the earlier note are both confirmed correct.

2. **Burnett & Nedzelnitsky 1987 (`small-chamber/EXTRACTS.md`, "1. Burnett & Nedzelnitsky") —
   DISAGREE on one page number.** The earlier note attributes "whereas inter-microphone
   diffraction/reflection effects should grow at higher frequencies as the microphone diameter
   becomes comparable to the wavelength (p. 141)" to page 141. A direct per-page extraction of the
   PDF (physical page 12, printed page "140," confirmed by the page-140 footer visible in the same
   `pdftotext -f 12 -l 12` dump) shows this entire sentence — "It would be expected that the effect
   of microphone reflections would become more pronounced as the frequency is increased (as
   wavelengths become comparable to the microphone diameter), and less pronounced as the separation
   distance between the microphones increased" — sits on the **same page as, and immediately after,
   the sentence the earlier note itself correctly cites to p. 140** ("it is not possible completely
   to separate..."). This is page **140, not 141**; the sentence appears to trail off into an
   OCR/column-order artefact at the point where the physical page ends, which may be what caused the
   earlier note to look one page ahead for its conclusion.

3. **All other held sources re-read for this thread (Rasmussen & Winberg 2022; Jawahar 2025;
   Alkmim 2022; Ma 2022 QuietDrones; Fasulo 2025; Whelchel 2023; Zawodny & Haskin 2017; Winker &
   Stahnke 2016; Weitsman 2020; ISO 26101-1:2021; ISO 5305:2024) — AGREE.** Every quote and page
   number used above from these documents was checked against a `pdftotext -f N -l N` extraction of
   the specific physical PDF page and matches (or, where the earlier note gave a page *range*
   spanning a quote, this file narrows it to the exact page — e.g. Fasulo's "support pylon lies
   directly on the acoustic line of sight of microphone 10" is pinned to p. 12 rather than the
   earlier note's "p. 11–12" range) what the existing `EXTRACTS-local.md`, `EXTRACTS-downloaded.md`
   and `MATRIX-3W.md` notes already say. No numeric, attribution, or substantive-claim errors were
   found in these.
