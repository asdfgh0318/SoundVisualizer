## Thread I — how other small rotor/propeller labs qualify, correct and report a chamber that is not free-field at BPF

Compiled 2026-09-08. All quotes below were re-extracted fresh with plain `pdftotext -q` into
`papers/arc-validation/refetch-txt/` (held papers) or `papers/arc-validation/txt/` (new NTRS
papers), except the Zawodny/Boyd/Burley 2016 AHS paper, whose text layer is not extractable
(see its entry) — that one was read visually page-by-page with the Read tool. File paths below
are relative to `/home/adam/ŻYCIE/PRACA/SoundVisualizer/papers/`.

---

## A. NASA Langley facilities — SALT and SHAC (Q1)

**Identity-critical finding: the 2016 and 2017 Zawodny papers named in the thread's Q1 do NOT
describe the Small Hover Anechoic Chamber (SHAC).** They describe a different, larger NASA
Langley facility — the Structural Acoustic Loads and Transmission (SALT) chamber. SHAC's own
numbers come only from the 2019/2020 JASA papers and the two 2025/2026 NASA Technical
Memoranda retrieved for this thread. This is stated explicitly in both 2016/2017 papers by name
("SALT anechoic chamber facility") and confirmed by dimensions: SALT is 4.57 × 7.65 × 9.63 m
(100 Hz cut-off, per Rizzi 2013, held in `chamber-problems/`) while SHAC is 3.87 × 2.56 × 3.26 m
(250 Hz cut-on/cut-off) — completely different rooms.

### A1. Zawodny, Boyd & Burley 2016 — AHS 72nd Annual Forum (SALT, not SHAC)

**Citation as printed**: Zawodny, N. S., Boyd, D. D. Jr. & Burley, C. L. *Acoustic Characterization
and Prediction of Representative, Small-Scale Rotary-Wing Unmanned Aircraft System Components.*
American Helicopter Society 72nd Annual Forum, West Palm Beach, FL, 17–19 May 2016. NASA
NTRS accession 20160009054.

**File**: `arc-validation/Zawodny-Boyd-Burley_2016_AHSForum72_SALT-facility-small-rotor-characterization.pdf`
(retrieved via NTRS API, `ntrs.nasa.gov/api/citations/20160009054/downloads/20160009054.pdf`).
**Evidence level**: conference paper (peer-reviewed AHS Forum submission).

**Extraction note**: `pdftotext` on this PDF returns only isolated figure-axis numerals and
symbol-substitution artifacts (e.g. "3" for θ, "+" for φ, "7Pa" for µPa) — the body-paragraph text
has no extractable text layer (`pdffonts` shows only 3 embedded subset fonts; `pdfimages -list`
shows only small figure-crop JPEGs, not full-page scans, so this is a font/text-object encoding
quirk, not a scan). Per protocol this PDF's own front matter was confirmed by page-1 title/author
match (`Read` tool, pages 1–3, rendered visually), and the quotes below were read directly off the
rendered page images rather than from a `pdftotext` dump.

**What it says**: Compares two isolated small UAS rotors (DJI-CF, APC-SF) in hover in the SALT
facility; up to 8 dB OASPL difference between rotors at similar thrust; broadband self-noise and
motor-noise prediction (ANOPP-PAS, OVERFLOW2).

**Verbatim quotes** (page numbers are the PDF's own printed footer numbers, confirmed visually):
> "Experiments were performed in the Structural Acoustic Loads and Transmission (SALT) anechoic
> chamber facility at the NASA Langley Research Center (Ref. 10). This facility is acoustically
> treated down to a cut-off frequency of 100 Hz and has interior dimensions (wedge tip to wedge
> tip) of 4.57-m (15-ft) high, 7.65-m (25-ft) wide, and 9.63-m (31.6-ft) long. A total of five 1/4"
> free-field Brüel & Kjaer 4939 microphones in an arc array configuration are positioned in the
> acoustic far-field of the rotor test stand in elevation angle increments of 22.5°, from 45° below
> the plane of the rotor to 45° above the plane of the rotor. Specifically, the microphones are
> positioned at a radial distance of 1.905 m (75 in.) from the rotor hub. This distance corresponds
> to at least 13R for the rotors tested in this study. The rotor test stand itself was constructed
> so that the plane of the rotor would stand 2.29-m (7.5-ft) above the floor wedge tips, which
> corresponds to half of the room height." (p. 3)

No qualification method, wedge depth, or artefact discussion is given on the pages read (1–3);
the rest of the paper (not re-read in full given the extraction problem) is results/prediction, per
its abstract and section structure visible on p. 1.

### A2. Zawodny & Boyd 2017 — AHS 73rd Annual Forum (SALT, not SHAC)

**Citation as printed**: Zawodny, N. S. & Boyd, D. D. Jr. *Investigation of Rotor-Airframe
Interaction Noise Associated with Small-Scale Rotary-Wing Unmanned Aircraft Systems.* American
Helicopter Society 73rd Annual Forum, Fort Worth, TX, 9–11 May 2017. NASA NTRS accession
20180001470 (distributed 2019).

**File**: `arc-validation/Zawodny-Boyd_2017_AHSForum73_rotor-airframe-interaction-SALT.pdf`.
Fresh text: `arc-validation/txt/Zawodny-Boyd_2017_AHSForum73_rotor-airframe-interaction-SALT.txt`.
**Evidence level**: conference paper.

**What it says**: Same SALT facility, now with an airframe (carbon-fibre tube / conical section)
near the rotor to study rotor–airframe interaction tones.

**Verbatim quote** (p. 2, confirmed both in the fresh `pdftotext` dump and visually):
> "Experiments were performed in the Structural Acoustic Loads and Transmission (SALT) anechoic
> chamber facility at the NASA Langley Research Center (Refs. 4, 11). A total of five 6.35 mm Type
> 4939 free-field Brüel & Kjaer microphones in an arc array configuration are positioned in the
> acoustic far-field of the rotor test stand. The microphones are positioned at a radial distance of
> 1.905 m from the rotor hub, which corresponds to approximately 16R for the rotor tested in this
> study. ... The rotor test stand itself was constructed so that the plane of the rotor would stand
> 2.29 m above the floor wedge tips, which corresponds to half of the room height."

Table 1 (p. 2) gives the exact microphone angular grid (θ, φ) in degrees at r = 16R: M1 (0.0, 0.0),
M2 (−22.5, 0.0), M3 (−45.0, 0.0), M4 (−45.0, +45.0), M5 (−45.0, +90.0).

### A3. Zawodny, Schiller, Pettingill & Medina 2025 — NASA/TM-20250009190 (SHAC, ducted propeller)

**Citation as printed**: Zawodny, N. S., Schiller, N. H., Pettingill, N. A. & Medina, G. L.
*Aerodynamic and Acoustic Characterization of a Ducted Propeller in a Small Hover Anechoic
Chamber.* NASA/TM–20250009190, NASA Langley Research Center, September 2025.

**File**: `arc-validation/Zawodny-Schiller-Pettingill-Medina_2025_NASA-TM-20250009190_ducted-propeller-SHAC.pdf`.
Fresh text: `arc-validation/txt/Zawodny-Schiller-Pettingill-Medina_2025_NASA-TM-20250009190_ducted-propeller-SHAC.txt`.
**Evidence level**: NASA Technical Memorandum (agency report, not journal-refereed but internally
reviewed — STI type TECHNICAL_MEMORANDUM).

**What it says (the SHAC facility itself)**: dimensions, cut-on, 8-mic array, recirculation
screens, and the periodic/broadband tonal-extraction method, all confirmed visually against the
rendered PDF pages (10–11, 13–14, 33) as well as the fresh `pdftotext` dump.

**Verbatim quotes**:
> "Tests were conducted in the NASA Langley Small Hover Anechoic Chamber (SHAC) [17], formerly
> known as the Small Anechoic Jet Facility (SAJF) [18]. SHAC is an acoustically treated facility
> with a cut-on frequency of 250 Hz and measures 3.87 m × 2.56 m × 3.26 m (L × W × H) from wedge
> tip to wedge tip. It has an air inlet and outlet, through which a freestream flow of approximately
> 5 m/s is possible with the use of a downstream single speed fan. ... the flow conditioning is only
> comprised of a 6 inch (152 mm) deep honeycomb filter installed within the SHAC inlet nozzle. The
> freestream turbulence intensity at the core flow centerline was measured to be rather large at
> TI = 100 × Urms/U∞ ≈ 4.2%" (p. 10).

> "As shown in Fig. 6, the SHAC contains an eight element microphone array that encompasses a
> range of directivity angles. The sensors are 6.35 mm-diameter free-field Brüel & Kjær microphones
> with associated preamplifiers. ... This allows for a nearly flat free-field frequency response up
> to approximately 80 kHz. Their locations in terms of a radial distance and elevation angle
> relative to the propeller hub center are provided in Table 3." (p. 10)

Table 3 (p. 11): 8 mics, radial distance 1.91–2.38 m, elevation θₒ = +37.3° to −50.1° (M1 2.38 m
/37.3°, M2 2.10/25.8°, M3 1.94/5.7°, M4 1.91/−0.8°, M5 2.04/−19.2°, M6 2.30/−35.2°, M7 2.31/−43.5°,
M8 2.23/−50.1°).

Recirculation mitigation (p. 13):
> "Testing static hover conditions required the installation of two screen meshes of different
> percentage open area downstream of the rotor stand [19]. The purpose of these screens is to delay
> the onset of flow recirculation by breaking up the wake structures of highest energy shed by the
> propulsor and reducing the energy of the recirculated flow. ... Data acquisition runs were
> approximately ten seconds in duration. Static hover runs consisted of a rapid ramp-up ... The
> ramp-up period lasted approximately two seconds. The remaining eight seconds was comprised of a
> 'clean' propeller operation condition, followed by a 'dirty' operation condition characterized by
> an onset of flow recirculation in the facility." (p. 13–14)

How tonal levels are extracted (p. 14, method) and how OASPL bands are chosen relative to the
cut-on (p. 33):
> "Periodic and broadband extraction is performed in this study by discretizing the measured
> acoustic pressure time histories into data blocks corresponding to the rotor period of
> revolution, computing an average revolution acoustic time history, then repeating this averaged
> time history and subtracting it from the raw measured signal." (p. 14)

> "Therefore, the periodic OASPL contribution is computed as the sum of the acoustic energy in the
> first three BPF harmonics. Next, the residual noise OASPLs were computed starting at a cut-on
> frequency of approximately 1 kHz because this was the frequency at which propeller broadband
> noise was seen to occur above the facility background noise. ... Note that all spectra are
> plotted with a 16 Hz frequency resolution and are corrected to a common arc distance of 1.91 m
> using spherical spreading (denoted by [ ]∗)." (p. 33)

No formal ISO/ANSI qualification (traverse, inverse-square deviation table) is reported anywhere
in this TM — the "cut-on frequency of 250 Hz" is stated as a design/treatment figure, not the
result of a documented qualification traverse.

### A4. Pettingill & Zawodny 2026 — NASA/TM-20250003316 (SHAC, COTS/OPT2 rotors)

**Citation as printed**: Pettingill, N. A. & Zawodny, N. S. *Aerodynamic Performance and Acoustic
Impacts of Varying Tip Speeds and Tripping Conditions on Small Rotors in an Anechoic Hover
Chamber.* NASA/TM–20250003316, NASA Langley Research Center, March 2026 (NTRS submission id
20250003316, distributed under a 2025 accession number but the report cover itself is dated March
2026).

**File**: `arc-validation/Pettingill-Zawodny_2026_NASA-TM-20250003316_tip-speed-tripping-SHAC.pdf`.
Fresh text: `arc-validation/txt/Pettingill-Zawodny_2026_NASA-TM-20250003316_tip-speed-tripping-SHAC.txt`.
**Evidence level**: NASA Technical Memorandum.

**Verbatim quote** (p. 8, confirmed visually and in the fresh dump):
> "The rotors were tested in the NASA Langley Small Hover Anechoic Chamber (SHAC). ... The SHAC
> is acoustically treated down to 250 Hz and has working dimensions (wedge tip to wedge tip) of
> 3.87 m x 2.56 m x 3.26 m. The test setup in the SHAC was similar to that of Ref. [5]. ... Six
> B&K Type 4939 and two B&K Type 4954B free-field microphones are located in the upper corner of
> the SHAC and span a range of +44° above the plane of the rotor to −49° below the plane of the
> rotor. ... These microphones are located at a minimum of 10 rotor radii away from the rotor,
> which is in the geometric far-field."

Figure 4 (p. 8) labels the same 8-mic array with explicit radii: θₒ≈44°, r=2.38 m; θₒ=0°, r=1.90 m;
θₒ≈−49°, r=2.21 m; plus a "Coarse Mesh Screen" and "Fine Mesh Screen" drawn downstream of the
rotor stand between it and the SHAC outlet.

Known artefact / how residual tones are handled (p. 15):
> "In Fig. 8, these residual harmonics are seen at frequencies between 400 Hz and 4 kHz. These
> residual harmonics can be due to several sources, the most likely being related to turbulence
> ingestion. The three most likely sources of turbulence ingestion in a facility such as SHAC are
> incident turbulence from the inlet of the facility, perpendicular blade vortex interactions, and
> flow recirculation generated by the wake of the rotor."

### A5. Stephenson, Weitsman & Zawodny 2019 — JASA 145(3) (SHAC — held, re-read)

**Citation as printed**: Stephenson, J. H., Weitsman, D. & Zawodny, N. S. *Effects of flow
recirculation on unmanned aircraft system (UAS) acoustic measurements in closed anechoic chambers
(L).* J. Acoust. Soc. Am. 145(3), 1153–1155, 2019. doi:10.1121/1.5092213.

**File**: `chamber-problems/Stephenson_2019_JASA_recirculation-UAS-closed-anechoic-chambers.pdf`.
Fresh text: `arc-validation/refetch-txt/Stephenson_2019.txt`. **Evidence level**: journal (Letter).

**Verbatim quotes** (page numbers are the journal's own, confirmed from the inline
"1153"/"1154"/"1155" running-footer markers preserved in the `pdftotext` dump):
> "The SHAC measures 12.70 × 8.40 × 10.70 (L × W × H) from wedge-tip to wedge-tip." (p. 1153;
> units not printed in this text — the 2020 companion paper below gives the same numbers in feet)

Table I (p. 1154) gives all six microphone radii, axial offsets and elevation angles (in.,
degrees) relative to the rotor hub: M1 83.6/57.6/43.6, M2 82.8/37.0/26.6, M3 74.9/8.6/6.6, M4
74.6/0/0 (in-plane), M5 78.9/25.3/18.7, M6 89.5/51.3/34.9 (signs not preserved by extraction; text
elsewhere states M1 is above and M6 below the rotor plane).

> "This higher harmonic content is not indicative of what a rotor in hover outdoor would emit, but
> is instead an artifact of testing within the confined space of an anechoic chamber." (p. 1154)

No qualification standard, wedge depth or cut-off frequency is stated anywhere in this Letter.

### A6. Weitsman, Stephenson & Zawodny 2020 — JASA 148(3) (SHAC — held, re-read)

**Citation as printed**: Weitsman, D., Stephenson, J. H. & Zawodny, N. S. *Effects of flow
recirculation on acoustic and dynamic measurements of rotary-wing systems operating in closed
anechoic chambers.* J. Acoust. Soc. Am. 148(3), 1325–1336, 2020. doi:10.1121/10.0001901.

**File**: `chamber-problems/Weitsman_2020_JASA_recirculation-rotary-wing-closed-chambers.pdf`.
Fresh text: `arc-validation/refetch-txt/Weitsman_2020.txt`. **Evidence level**: journal.

**Verbatim quotes** (journal page numbers, confirmed via the inline "1326" marker and the
consistent extracted-page → 1323+N offset established from the article's own "Pages: 1325–1336"
banner):
> "This experiment was conducted in the Small Hover Anechoic Chamber (SHAC, formally known as the
> Small Anechoic Jet Facility) at the NASA Langley Research Center (LaRC). The test facility is
> treated with woven fiberglass acoustic wedges, which absorb 99% of incident sound energy above
> 250 Hz. The interior dimensions (wedge tip to wedge tip) of the facility measure 10.67 ft (3.25 m)
> in height, 8.38 ft (2.55 m) in width, and 12.67 ft (3.86 m) in length." (p. 1326)

> "Since the microphone closest to the rotor, M4, is located at a radial distance greater than 12
> rotor radii from the rotor hub, the microphones are considered to be located in the acoustic
> far-field of the rotor." (p. 1326)

How tonal levels are extracted:
> "The periodic noise components are extracted by calculating the RMS of the ensemble-averaged
> pressure time history over a specific number of shaft revolutions. This tonal extraction
> technique is well documented by Zawodny et al." (p. 1327)

No ISO/ANSI qualification traverse is reported; "99% absorption above 250 Hz" is a wedge
specification, not a measured free-field-deviation result.

**Cross-source consistency (A3–A6):** SHAC's dimensions (3.87 × 2.56 × 3.26 m ≈ 3.86 × 2.55 × 3.25 m)
and its 250 Hz cut-on/cut-off are stated identically across four independently published NASA
documents spanning 2019 to 2026 (Stephenson 2019 in ft only, Weitsman 2020 in ft+m, Zawodny et al.
2025 and Pettingill & Zawodny 2026 in m). None of the four states a documented ISO 3745/26101
qualification traverse for SHAC; "cut-on/cut-off = 250 Hz" is reported as a treatment/design
figure, not a measured-deviation result. The one recorded artefact type for SHAC across all four
is flow recirculation from the rotor wake re-entering the room (not a reflection/standing-wave
artefact), mitigated with downstream mesh screens.

---

## B. Other small rotor/propeller facilities (Q2)

### B1. Bristol — Jawahar, Hanson, Akhter & Azarpeyvand 2025, Scientific Reports 15:2170

**File**: `chamber-problems/Jawahar_2025_SciRep_porous-ground-propeller-ground-effect.pdf`.
Fresh text: `arc-validation/refetch-txt/Jawahar_2025.txt`. **Evidence level**: journal.

> "Experiments to investigate propellers operating in GE were conducted in the Aeroacoustic
> facility at the University of Bristol. The anechoic chamber has dimensions of 7.9 m in length,
> 5.0 m in width and 4.6 m in height, including the surrounding acoustic walls." (p. 3)

> "Far-field noise measurements were acquired using a polar array of 23 microphones distributed in
> the axial direction centred on the propeller at a distance of 1.75 m (≈ 13R). The polar array
> covers observer locations between θ = 40° above the plate and θ = 150° below the plate." (p. 3)

No cut-off frequency or ISO qualification is stated in this paper; the propeller (APC 10×5.5″,
R=127 mm, BPF≈233 Hz at 7000 RPM) is well above any plausible cut-off for this chamber, so the
paper does not need to address a sub-cut-off band — its low-frequency artefact discussion is about
ground-plane reflection (+4–8 dB above 1 kHz at θ=50°), not chamber cut-off.

### B2. Bristol — Huang (student research report, supervisor Azarpeyvand)

**File**: `anechoic-simulation/Huang_nd_Bristol-report_height-dependent-rotor-noise-thrust.pdf`.
Fresh text: `arc-validation/refetch-txt/Huang_nd.txt`. **Evidence level**: unreviewed student report.

> "Experimental investigations into the aeroacoustic characteristics of a two-bladed rotor were
> conducted at the Aeroacoustics Facility of the University of Bristol, within an anechoic chamber
> measuring 7.9 m × 5.0 m × 4.6 m (L × W × H), with a cut-off frequency of 160 Hz." (p. 3)

Same physical chamber as Jawahar 2025, with a stated cut-off (160 Hz) that Jawahar's paper does
not mention — no contradiction, just an added fact. No band-exclusion statement is made because
the BPF here (12,000 RPM two-blade propeller) is far above 160 Hz.

### B3. TU Delft — Merino-Martínez et al. 2020, Applied Acoustics 170:107504

**File**: `chamber-problems/Merino-Martinez_2020_ApplAcoust_TU-Delft-anechoic-wind-tunnel.pdf`.
Fresh text: `arc-validation/refetch-txt/MerinoMartinez_2020.txt`. **Evidence level**: journal.

> "The selected wedge geometry (with a total height of 0.49 m) should allow for free-field
> propagation of sound for frequencies above approximately 173.5 Hz." (p. 4)

> "It can be observed that all the frequency bands above 250 Hz fulfill the standards in ISO3745
> [56] for the full range of distances considered. The results for the three next one-third-octave
> bands below 250 Hz, (125 Hz, 160 Hz and 200 Hz) only show acceptable values up to r = 1.5 m. For
> aeroacoustic experiments, the distance between the microphone array and the jet axis normally
> corresponds to r ≤ 1.5 m, so acoustic measurements at these three frequency bands could be
> considered as acceptable in that distance range." (p. 12)

This is the thread's clearest example of **distance-conditioned validity rather than a hard
frequency cut**: bands down to 125 Hz are usable, but only inside a stated radius; the paper does
not claim free-field behaviour below 125 Hz at any distance.

### B4. VKI — Gallo et al. 2025, Acta Acustica 9:16

**File**: `chamber-problems/Gallo_2025_ActaAcustica_aeroacoustic-propeller-test-bench.pdf`.
Fresh text: `arc-validation/refetch-txt/Gallo_2025.txt`. **Evidence level**: journal.

> "The size of the main room is 2.5 m × 4.5 m. This room has been commissioned according to the
> ISO:3745 standard [22], demonstrating free-field behavior down to 150 Hz for both broadband and
> tonal noise sources [23]." (p. 2)

On recirculation (relevant to Q4's "measured the room and separated it from the source" theme,
though by time-domain rather than reversed-rotation means):
> "The spectrum does not reveal any rise in either tonal or broadband noise levels over time. Given
> the small size of the room, one would have expected to see a transient effect of the recirculating
> flow." (p. 7)

### B5–B7. HKUST — Ma 2022 (Quiet Drones), Ma 2024 (Acoustics Australia), Cao 2025 (Forum Acusticum)

**Files**: `chamber-problems/Ma_2022_QuietDrones_multirotor-anechoic-vs-hemi-anechoic.pdf`;
`chamber-problems/Ma_2024_AcoustAust_recirculation-free-flying-UAS-anechoic.pdf`;
`small-chamber/Cao-etal_2025_ForumAcusticum_sub-7kg-multirotor-anechoic-noise.pdf`.
Fresh text: `arc-validation/refetch-txt/Ma_2022_QD.txt`, `Ma_2024_AA.txt`, `Cao_2025.txt`.
**Evidence level**: conference (Ma 2022, Cao 2025), journal (Ma 2024).

All three describe the same HKUST Aerodynamic and Acoustic Facility chamber, with identical
dimensions and cut-off across all three independently published texts:
> "The chamber has a wedge-to-wedge dimension of 8.1 m (L) × 6 m (W) × 5.1 m (H) and a cut-off
> frequency of 100 Hz in the full anechoic configuration. With the bottom wedges removed, the
> chamber is in the hemi-anechoic configuration and the height is 5.7 m." (Ma 2022, p. 2)

> "The chamber has wedge tip-to-tip dimensions of 8.1 m (L) × 6 m (W) × 5.1 m (H) and a cut-off
> frequency of 100 Hz." (Ma 2024, p. 2)

> "The chamber, measuring 8.1 m × 6.0 m × 5.1 m, is fully wedge-lined and provides free-field
> conditions above 100 Hz. A nylon safety cage was installed to define an internal working volume
> of 6.8 m × 4.8 m × 4.0 m, ensuring a minimum 600 mm clearance from all walls." (Cao 2025, p. 3)

No ISO qualification traverse/tolerance numbers appear in any of the three; "100 Hz" is reported
as a facility specification. Ma 2022 shows that even above the stated cut-off, a reflective floor
in hemi-anechoic mode causes up to 10 dB disagreement between two adjacent near-floor mics at BPF
— i.e. a within-band artefact distinct from the cut-off question (p. 8, already fully quoted in
`chamber-problems/EXTRACTS-local.md` and re-confirmed present verbatim in the fresh dump).

### B8. CIRA — Fasulo, Longobardo, De Gregorio & Barbarino 2025, Aerospace 12(7):647 (Q2 + Q4)

**File**: `chamber-problems/Fasulo_2025_Aerospace_rotor-noise-directivity-decay.pdf`.
Fresh text: `arc-validation/refetch-txt/Fasulo_2025.txt`. **Evidence level**: journal (MDPI,
open access). Page numbers below are the article's own printed "N of 26" footer, confirmed
directly in the extracted text.

Facility (p. 3):
> "operated in the Italian Aerospace Research Centre's semi-anechoic chamber [15]. The chamber,
> with a 90 Hz cut-off frequency, measures 5.65 m × 4.45 m × 4.00 m."

Band handling / floor treatment (p. 10):
> "the ground was treated as an acoustically rigid surface, so local reflections could either
> reinforce or attenuate the radiated sound, thereby altering the apparent directivity."

**Q4 — reversed rotation used to separate an installation/room asymmetry from the source** (p. 24,
in the paper's own summary of results, confirmed verbatim in the fresh dump):
> "Reversing the sense of rotation revealed that even modest geometric asymmetries, here the
> support pylon, can shift directivity by up to 4 dB."

Earlier in the results (p. 11–12) this is elaborated: the support pylon is offset toward one mic
(mic 10), producing shielding there; running the rotor with blades in the opposite rotational
sense flips which side of the directivity pattern the wake/loading asymmetry favours while the
pylon's physical position does not move, so a rotation-sense-dependent shift in the pattern (found
to be ≈1 dB at 3000–5000 rpm, growing to 3–4 dB at 7000–8000 rpm, SD up to ≈4 dB) is attributable
to the fixed geometry (pylon) rather than to the rotor itself. This is the only source found in
this thread's corpus that explicitly uses a *reversed-rotation* test to attribute part of a
measured directivity pattern to the rig/room rather than the source. No source in this thread's
corpus (see comparison note in the "not found" line of Q4 below) subtracts a measured *room-error
spectrum* from rotor directivity data the way Q4 also asks about; the closest partial analogue is
Nardari 2019's loudspeaker-based per-microphone inverse-square check, which is used to define an
error tolerance/exclusion band rather than to correct rotor data (see B10).

### B9. FCRI Palakkad (India) — Garg et al. 2019, MAPAN 34(3):357–369 ("2 m³ box")

**File**: `chamber-problems/Garg_2019_MAPAN_microphone-free-field-calibration-uncertainty.pdf`.
Fresh text: `arc-validation/refetch-txt/Garg_2019.txt`. **Evidence level**: journal.

> "A dedicated transportable anechoic chamber (make SPEKTRA, Germany) of internal volume of 2 m³
> completely lined with wedge-shaped absorbers is utilized for free-field calibrations in the
> frequency range of 125 Hz–20 kHz using the substitution method as per the IEC 61094-8 standard."
> (p. 357, abstract; confirmed against the journal's own printed page number, which appears as a
> bare digit at the top of the following extracted page in the `pdftotext` dump)

> "The outside dimensions of the chamber are 2 m × 2 m × 2.4 m." (p. 358)

This is a microphone-calibration chamber, not a rotor-noise facility, but it is the thread's
clearest worked example of **restricting the usable region rather than the frequency band**: the
chamber's ISO 26101 tolerance (±1.5 dB ≤630 Hz, ±1.0 dB 800–5000 Hz, ±1.5 dB ≥6300 Hz) is met only
inside a specific working distance (0.79–0.89 m from the source), found empirically by scanning
distance at each low-frequency band and keeping only the interval where every band is inside
tolerance.

### B10. Amazon Prime Air — Nardari et al. 2019, AIAA 2019-2497

**File**: `chamber-problems/Nardari_2019_AIAA_flow-confinement-UAV-rotor-noise.pdf`.
Fresh text: `arc-validation/refetch-txt/Nardari_2019.txt`. **Evidence level**: conference.

> "The chamber is Lx = 8.76D long, Ly = 8.86D wide and Lz = 7.79D tall, where D is the rotor
> diameter. Its walls and ceiling are treated with anechoic foam paneling, while the floor – a
> thick concrete slab – is left untreated and reflective. Our calibration experiments indicate that
> the chamber is hemi-anechoic within ±1 dB above a blade passing frequency (BPF) harmonic of 2.2,
> but only within ±4 dB below that, primarily due to the onset of standing waves, which are a
> consequence of the nearly cuboidal shape of the chamber." (p. 2)

This paper does not state an absolute room size (D is left as a variable) or a Hz cut-off — the
qualified/unqualified boundary is expressed relative to the source's own BPF (a harmonic number,
2.2× BPF), which is unusual among the thread's sources (most others use an absolute Hz figure).
The ±4 dB below-threshold band is not excluded from the paper's later confinement-effect analysis
— it is carried with an explicit caveat instead (Q4-adjacent: the ±1 dB/±4 dB split itself comes
from a **reference loudspeaker** traverse compared against ideal inverse-square decay, i.e. exactly
the "measured the room error with a reference source" method Q4 asks about — but the measured
error is used to set a tolerance band, not subtracted from the rotor spectra).

### B11. Colombia (UTP) — Orrego González, Ealo Cuello & Pazos Ospina 2018, Scientia et Técnica

**File**: `small-chamber/Orrego-Ealo-Pazos_2018_ScientiaTechnica_low-cost-small-anechoic-chamber.pdf`.
Fresh text: `arc-validation/refetch-txt/Orrego_2018.txt`. **Evidence level**: conference/university
journal (Spanish, with English abstract/figures read).

> "La cámara posee dimensiones de trabajo de 1,94 m de largo x 1,91 m de ancho x 1,84 m de alto y
> frecuencia de corte nominal de 400 Hz." (p. 1) ["The chamber has working dimensions of 1.94 m
> long × 1.91 m wide × 1.84 m high and a nominal cut-off frequency of 400 Hz."]

> "It is appreciated that one measured point is exceeding the limits by 1.0 dB at 500 Hz." (p. 476,
> i.e. the article's own page numbering; extracted `pdftotext` page 6 + 470 offset)

Not a rotor/propeller chamber (no rotor is tested), but it is exactly the "purpose-built small
anechoic room" type the thread's Q2 asks about, and shows a mid-band (500 Hz) ISO 3745 exceedance
sitting just above its own 400 Hz design cut-off, attributed tentatively to "a small frequency
distance between adjacent [room] modes" rather than to a construction fault.

### B12. ITMO (St. Petersburg) — Bikmukhametov et al. 2026, arXiv:2603.16556

**File**: `anechoic-simulation/Bikmukhametov_2026_arXiv_ITMO-radiowave-chamber-acoustic-free-field.pdf`.
Fresh text: `arc-validation/refetch-txt/Bikmukhametov_2026.txt`. **Evidence level**: journal
preprint (submitted to Elsevier; not yet peer-reviewed).

> "Without coatings, the length of the walls is 4.46 and 6.96 m, and the height of the ceiling is
> 3.3 m." (p. 2)

> "the largest deviation reaches the value of 15.5 dB. In general, the chamber meets the
> requirements only for a limited set of frequencies and distances to the source." (p. 5)

This is a radio-wave (EM) anechoic chamber repurposed and qualified acoustically — not a rotor
facility — but it is the thread's most extreme example of a facility that is anechoic only for a
"limited set of frequencies and distances" simultaneously (free field only 50–3150 Hz at
0.5–0.8 m; one direction usable 50 Hz–10 kHz only at 0.5–0.9 m), attributed to non-uniform
absorber coverage rather than a global low-frequency cut-off.

### B13. University of Split — Russo, Kraljević, Stella & Sikora 2018, Euronoise 2018

**File**: `anechoic-simulation/Russo_2018_Euronoise_ISO3745-vs-ISO26101-Split-chamber.pdf`.
Fresh text: `arc-validation/refetch-txt/Russo_2018.txt`. **Evidence level**: peer-reviewed
conference proceedings.

> "We have recently constructed a small anechoic chamber (with internal dimensions L×W×H – 2.8 ×
> 1.7 × 2.05 m) at University of Split, Croatia." (p. 2228, i.e. Euronoise proceedings p. 2225+3)

> "the lowest one-third-octave band we could measure was 250 Hz band in order to end the traverse
> 50 cm from the tips of acoustic wedges ... However, because of the chamber dimensions, in this
> scenario, the measured range is small and not suitable for practical applications." (p. 2229)

Explicitly documents the ISO 26101:2012→2017 revision that halved the required qualification
traverse length from λ/2 to λ/4 specifically because small chambers like this one could not always
meet the λ/2 traverse requirement at low frequency (§2.3.2, p. 2227) — directly relevant to how the
qualified low-frequency limit of a *small* chamber is itself a standards-writing concern, not just
a per-facility one.

### B14. NASA Langley LSAWT — Zawodny & Haskin 2017, AIAA Aeroacoustics Conference

**File**: `chamber-problems/Zawodny-Haskin_2017_AIAA_LSAWT-small-rotor-capabilities.pdf`.
Fresh text: `arc-validation/refetch-txt/ZawodnyHaskin_2017.txt`. **Evidence level**: conference.

> "The floor, ceiling, and walls are treated with 0.61-m tall acoustic fiberglass wedges. This
> acoustic treatment ensures anechoic facility characteristics down to a cut-on frequency of
> approximately 200 Hz." (p. 2)

> "It is important to note that the LSAWT microphones are mounted an average distance of 0.49 m
> from the acoustic wedge tips, which is approximately half of the distance between the microphones
> and wedge tips in the SALT facility measurements. Treating this as a 1/4-wavelength yields a
> notional cut-on frequency of 175 Hz. ... below this cut-on frequency, caution should be used in
> quantitative comparisons at frequencies below the notional cut-on frequency of approximately
> 175 Hz." (p. 16)

This is the thread's clearest example of a lab **deriving its own practical low-frequency limit
from microphone-to-wedge-tip distance** (a λ/4 rule applied to the mic's own clearance, not the
wedge depth) rather than from a formal qualification traverse, and using it to bound which BPF
values it will quantitatively trust rather than to exclude data outright — directivity *trends*
below the notional cut-on were still judged informative (p. 16).

### B15. Palchikovskiy et al. 2016, AIP Conf. Proc. 1770:030116 (PNRPU, Perm)

**File**: `chamber-problems/Palchikovskiy_2016_AIPConfProc_anechoic-chamber-tests-aeroacoustics.pdf`.
Fresh text: `arc-validation/refetch-txt/Palchikovskiy_2016.txt`. **Evidence level**: conference
(ICMAR 2016).

> "Qualification tests have determined that in the chamber there is a free acoustic field within
> radius of 2 m for tonal noise and 3 m for broadband noise." (p. 2, abstract)

This is the thread's clearest example of a lab reporting **two different qualified radii for the
same chamber depending on signal type** (tonal vs. broadband) rather than a single frequency
cut-off — directly relevant to Q3's "how papers state the valid envelope."

### B16. Virginia Tech — Whelchel 2023, PhD dissertation

**Citation as printed**: Whelchel, J. *Measurement and prediction of rotor noise sources for sUAS
in outdoor and laboratory environments.* PhD dissertation, Virginia Tech, 2023.

**File**: `chamber-problems/Whelchel_2023_PhD-VT_sUAS-rotor-noise-outdoor-lab.pdf`. Fresh text:
`arc-validation/refetch-txt/Whelchel_2023.txt`. **Evidence level**: thesis. Page numbers below are
the thesis's own printed page numbers; the fresh `pdftotext` split runs 16 pages ahead of them
(front matter/table of contents/list of figures), confirmed at two independent anchor points by
the printed page number visible at the bottom of the same extracted-page block.

Facility (p. 41):
> "The chamber, designed by Eckel Industries, is fully anechoic, providing a low frequency cut-off
> of 100 Hz, and has inner dimensions from wedge tip to wedge tip of 4.5 (L) × 2.5 (W) × 2.5 (H) m."

Known artefact and how it is characterised rather than corrected (p. 82) — averaging-time
dependence used as the recirculation diagnostic, in place of a hard onset time:
> "The BPF and its harmonics are all shown to increase by at least 7 dB with increasing averaging
> time suggesting that the turbulent wake is being reingested. ... the noise appears to be
> converging towards a steady state after approximately 20s of run time."

The dissertation also tested a smaller anechoic open-jet test section at the same lab ("fully
anechoic down to 420 Hz", elsewhere "the anechoic limit of the facility of 400 Hz") with a rotor
whose BPF (≈90–92 Hz) sat "just below the anechoic limit of the [main] chamber, 100 Hz" — i.e. a
single research programme running one rotor deliberately close to, and one facility explicitly
below, its own chamber's qualified floor, and reporting both directivity sets side by side with
the limitation stated in the text rather than the low-BPF case being dropped.

---

## C. Reporting practice: stating the valid envelope and handling sub-cut-off bands (Q3)

### C1. Hochbaum, Herold, Kempen & Fiebig 2026, Quiet Drones (Delft) — TU Berlin

**File**: `chamber-problems/Hochbaum_2026_QuietDrones_drone-directivity-anechoic-realistic-flight.pdf`.
Fresh text: `arc-validation/refetch-txt/Hochbaum_2026.txt`. **Evidence level**: conference.

> "The measurement campaign was conducted in the fully anechoic room of the Engineering Acoustics
> Lab at TU Berlin, with dimensions of 13.5 m, 8.3 m, and 7.4 m (L × W × H) and a lower cut-off
> frequency of 63 Hz." (p. 3)

> "It should be noted that the BPF band of the UBADRON partly falls below the cut-off frequency of
> the anechoic chamber." (p. 9)

This is the thread's cleanest example of the reporting pattern the question asks about: state the
facility's cut-off as a single number, then, for the one test case whose BPF sits below it, add a
one-sentence caveat directly beside the directivity result rather than omitting the data point or
correcting it.

### C2. Merino-Martínez et al. 2020 — TU Delft (see B3 for facility numbers)

Already quoted in full above (B3): "125 Hz, 160 Hz and 200 Hz only show acceptable values up to
r = 1.5 m" is the thread's clearest example of stating the valid envelope as a joint
(frequency-band, distance) condition rather than a single Hz threshold, and of confining later
measurements to the qualified geometry ("the distance between the microphone array and the jet
axis normally corresponds to r ≤ 1.5 m") rather than excluding the bands.

### C3. Palchikovskiy et al. 2016 (see B15)

Already quoted above: separate tonal (2 m) / broadband (3 m) qualified radii is a second pattern
for stating a valid envelope precisely (by signal type, not frequency band).

### C4. ISO 5305:2024 — Noise measurements for UAS (iTeh preview)

**File**: `anechoic-simulation/ISO-5305_2024_standard-preview_UAS-noise-measurement.pdf`.
Fresh text: `arc-validation/refetch-txt/ISO5305_2024.txt`. **Evidence level**: international
standard (preview only — Foreword through the start of Clause 7.3.1, per the earlier
bibliography's characterisation, confirmed: the fresh read reaches into 7.3.1 and stops there).

Clause 7.2.2, "Anechoic chamber qualification" (p. 14 of the preview PDF; note this is an iTeh
sample extract, not the standard's own page numbers):
> "The validity of the inverse square law defined in ISO 26101-1 shall be ensured for all source
> positions and measurement directions specified in this document. The maximum allowed deviation
> from the inverse square law in any of the measured directions for any of the microphone positions
> shall not exceed the values given in Table 1." — Table 1: ±1.5 dB for one-third-octave mid-band
> frequencies 125–630 Hz, ±1.0 dB for 800–5000 Hz, ±1.5 dB for ≥6300 Hz.
> "All microphones shall be placed within the region in the anechoic chamber satisfying the
> qualification. This distance of the microphone to the walls, floor, and ceiling (or the wedge
> tips) is denoted as Hm." (p. 14)

ISO 5305 imports the ISO 26101-1 tolerance table verbatim (identical numbers to those used by
Palchikovskiy 2016 and Bikmukhametov 2026, both citing the ISO 3745/26101 lineage) and does not
itself specify what to do with a UAS whose BPF falls below 125 Hz — the standard's qualification
clause simply has no defined tolerance below the bottom of Table 1, which is consistent with every
paper in this thread treating "below the lowest qualified one-third-octave band" as a caveat/
exclusion problem for the *experimenter* to solve, not something the standard adjudicates.

---

## Answers to the thread questions

**Q1 (NASA SHAC).** The 2016 AHS-Forum paper (Zawodny, Boyd & Burley) and the 2017 AHS-Forum paper
(Zawodny & Boyd) both used a *different* NASA Langley facility, SALT, not SHAC — see the identity
note at the top of Section A. SALT: 4.57 × 7.65 × 9.63 m (H×W×L), 100 Hz cut-off, 5-mic arc at
1.905 m (13–16R), elevation 45° below to 45° above the rotor plane in 22.5° steps (A1–A2). SHAC's
own numbers, from the four sources that actually test in it (A3–A6, spanning 2019–2026): 3.87 ×
2.56 × 3.26 m (L×W×H) wedge-tip-to-tip (Stephenson 2019 gives the same figures less precisely, in
feet, as 12.70×8.40×10.70), cut-on/cut-off 250 Hz (wedges "absorb 99% of incident sound energy
above 250 Hz," Weitsman 2020, p. 1326), 6–8 free-field B&K mics (4939, later +4954B) at 1.9–2.4 m
(≥10–12R) spanning roughly +37…+44° to −49…−51° in a fixed vertical arc — no azimuthal traverse.
No source describes a documented ISO 3745/26101 qualification traverse for SHAC; "250 Hz" is
reported as a wedge/treatment specification. The only recorded artefact is flow recirculation
(BPF harmonics ≥2 amplified 15–30 dB a few seconds into a run), not reflection/standing waves;
mitigated with downstream mesh screens (A3, A4, A6). Tonal levels are extracted by ensemble-
averaging the pressure signal over an integer number of shaft revolutions and subtracting that
periodic waveform from the raw signal to isolate broadband residual (Weitsman 2020 p. 1327,
Zawodny et al. 2025 p. 14); OASPL is then summed over the first three BPF harmonics for the
"periodic" component, with the broadband residual integrated from ≈1 kHz up, and all spectra are
distance-corrected to a common 1.91 m arc via spherical spreading (Zawodny et al. 2025, p. 33).

**Q2 (other facilities).** Fourteen non-NASA-SHAC facilities were checked (Sections B1–B16,
including Virginia Tech/Whelchel 2023, B16): all state a room size and a cut-off/cut-on Hz figure
or an ISO-qualified radius; none reported here formally *corrects* sub-cut-off data — every one
either (a) excludes/omits it (HKUST, Bristol, CIRA all report only above-cut-off results in their
headline OASPL/directivity numbers), (b) restricts the *distance* rather than the frequency (TU
Delft, B3; Garg/FCRI, B9), (c) reports two qualified radii by signal type (Palchikovskiy/PNRPU,
B15), (d) derives an ad-hoc practical limit from mic-to-wedge geometry rather than a formal
traverse (Zawodny & Haskin/LSAWT, B14), (e) carries the sub-threshold band forward with an explicit
± dB caveat instead of excluding it (Nardari/Amazon, B10: ±4 dB below 2.2×BPF, "primarily due to
the onset of standing waves"), or (f) runs a rotor whose BPF sits just below the chamber's own
stated cut-off anyway and reports the result with the limitation stated in the text (Whelchel/VT,
B16: BPF≈90–92 Hz rotor against a 100 Hz chamber cut-off). Room sizes range from Orrego's
1.94×1.91×1.84 m (400 Hz cut-off) up to Hochbaum's 13.5×8.3×7.4 m (63 Hz); mic distances range from
13R (Bristol, LSAWT) to >16R (Zawodny & Boyd 2017) to a fixed 1.5–1.75 m; none of the retrieved
facilities reported a formal below-cut-off *correction* factor applied to rotor data.

**Q3 (reporting practice).** Papers state the valid envelope either as a single (frequency,
distance) pair — Merino-Martínez/TU Delft's "125, 160 and 200 Hz only show acceptable values up to
r = 1.5 m" (C2) — or as parallel radii by signal type — Palchikovskiy's "free acoustic field within
radius of 2 m for tonal noise and 3 m for broadband noise" (C3) — and then either caveat a
below-envelope result in one sentence next to the plot (Hochbaum: "the BPF band of the UBADRON
partly falls below the cut-off frequency of the anechoic chamber," C1) or simply do not test there.
ISO 5305:2024 imports ISO 26101-1's ±1.5/±1.0/±1.5 dB tolerance table (125–630 / 800–5000 / ≥6300
Hz) for anechoic-chamber qualification and states no tolerance, hence no defined valid envelope, at
all below 125 Hz (C4) — the standard leaves "what to do below the qualified band" entirely to the
individual paper's practice documented in C1–C3 and Section B.

**Q4 (reference-source subtraction / reversed rotation).** Fasulo et al. 2025 (CIRA, B8) is the
only source in this thread's corpus that runs the rotor with reversed rotation specifically to
separate a rig/room asymmetry (the support pylon) from the source, concluding "Reversing the sense
of rotation revealed that even modest geometric asymmetries, here the support pylon, can shift
directivity by up to 4 dB" (p. 24). No source in this thread's corpus subtracts a measured
room-error *spectrum* from rotor data outright; the closest analogues measure room error with a
reference loudspeaker and use it to define a tolerance/exclusion band rather than to correct rotor
spectra — Nardari 2019 (Amazon, B10, ±1 dB/±4 dB split from a loudspeaker inverse-square traverse)
and Zawodny & Haskin 2017 (LSAWT, B14, λ/4-from-wedge-tip notional cut-on). No retrieved source
answers the "subtracted a measured room error from rotor data" half of Q4 directly.

---

## Comparison with earlier notes

Every held paper re-read for this thread was checked against `chamber-problems/EXTRACTS-local.md`,
`chamber-problems/EXTRACTS-downloaded.md`, `chamber-problems/MATRIX-3W.md`,
`anechoic-simulation/MATRIX-3W.md`, and `small-chamber/EXTRACTS.md`. Result: **no wrong numbers,
wrong pages, or wrong attributions were found in any of the 20 held-paper quotes checked.** Two
minor gaps/enhancements, no corrections:

- **Stephenson 2019 / Weitsman 2020 (SHAC dimensions)**: earlier notes quote the SHAC dimensions
  sentence from Stephenson without a page number; the fresh read supplies it (p. 1153, confirmed
  via the inline running-footer page markers preserved by `pdftotext`). No numeric or attribution
  error — just an added citation precision.
- **Cao et al. 2025 (HKUST safety cage)**: `small-chamber/EXTRACTS.md` quotes the safety-cage
  working volume as "6.8 m × 4.8 m" (two dimensions only, with a bracketed editorial guess "[wedge
  tip-to-tip?]" attached to the room's own 5.1 m figure). The fresh read supplies the complete,
  unambiguous sentence: "A nylon safety cage was installed to define an internal working volume of
  6.8 m × 4.8 m × 4.0 m, ensuring a minimum 600 mm clearance from all walls" (p. 3) — three
  dimensions plus the clearance figure, resolving the earlier note's bracketed uncertainty (the
  room itself, separately, is confirmed as 8.1 × 6.0 × 5.1 m, matching the earlier note).
- All other checked quotes (Weitsman's 99%-above-250-Hz and >12R far-field statements; Nardari's
  ±1/±4 dB qualification and its page/section; Jawahar's and Huang's Bristol chamber dimensions;
  Merino-Martínez's 0.49 m wedge/173.5 Hz and 1.5 m/125–200 Hz passages and their page numbers 4
  and 12; Gallo's 2.5×4.5 m room and no-transient recirculation quote; Ma 2022/2024's identical
  8.1×6×5.1 m/100 Hz HKUST description; Fasulo's 5.65×4.45×4.00 m/90 Hz facility line and its
  reversed-rotation conclusion on p. 24; Garg's 2 m³/125 Hz–20 kHz description; Orrego's
  1.94×1.91×1.84 m/400 Hz and 500 Hz/1.0 dB exceedance; Bikmukhametov's 4.46×6.96×3.3 m and 15.5 dB
  maximum deviation; Russo's 2.8×1.7×2.05 m and the 250 Hz/50 cm traverse-limit passage;
  Palchikovskiy's 2 m/3 m qualified-radius abstract line; Whelchel's 4.5×2.5×2.5 m/100 Hz VT
  chamber and its "increase by at least 7 dB with increasing averaging time" recirculation
  passage; Zawodny & Haskin's 200 Hz wedge cut-on and 175 Hz notional-cutoff derivation) matched
  the earlier notes' wording and page citations exactly, once each paper's own front-matter/
  running-footer page numbers were reconciled against `pdftotext`'s raw page-split count (several
  of these PDFs carry an extra, unnumbered repository cover page or thesis front matter, which
  shifts the raw split index by a constant offset from the printed page number — verified
  independently for each document via its own inline page-number text rather than assumed).
- The four NASA NTRS papers used for Q1 (A1–A4) are new retrievals, not held papers, so no
  "earlier notes" comparison applies to them; their identity was instead confirmed directly from
  each PDF's own front matter (title/author page, or NTRS citation metadata cross-checked against
  the rendered page image for the one PDF — A1 — whose text layer could not be extracted).
