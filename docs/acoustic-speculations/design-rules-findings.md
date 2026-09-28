# Quiet multicopter design rules — findings and their papers

Key findings from `quiet-multicopter-design-rules.pdf` (2026-09-28), each with its source.
Evidence tags: **E** experiment · **S** simulation/model · **R** reported second-hand (the paper cites someone else) · **T** our own reviews.
The verbatim quote and page behind each line are in `papers/SoundVisualizer/design-rules/EXTRACTS-*.md`
(private papers repo), which govern where this list and they disagree. Full list of all 101 sources: the PDF appendix.

**Read the numbers as single-study results.** Most rows are one rig, one propeller size, one observer set. dB figures use different metrics (tonal vs overall, dB vs dBA, one microphone vs sound power, relative to different baselines), so do not compare rows with each other. This list was audited on 2026-09-28; the corrections are listed at the end.

## Vehicle layout — arms, spacing, rotor count

| Finding | Paper |
|---|---|
| Arm below the rotor, about one blade chord wide: moving it 0.1→0.2 R below the tip gave the largest drop (up to ~8 dB unweighted, ~10 dBA tonal at the lowest microphone). At 0.4 R the unweighted tonal levels matched an isolated rotor; at 0.5 R both weightings did. Single 9.4-in rotor, hover [E] | Zawodny & Boyd 2017, AHS Forum (NASA) |
| A conical arm was typically louder than a round rod for observers below the rotor; the one number given (~6 dB, A-weighted, one mic) is at 0.5 R, where the unweighted levels were nearly identical [E] | Zawodny & Boyd 2017 |
| Rotors under the arms 8.1 dB louder than above (tonal OASPL over the first 10 BPF harmonics, one Phantom-like geometry) [S] | Zawodny, Christian & Cabell, NASA sUAS summary |
| Aft rotors raised 64 mm (0.33 R) above the airframe: −4 to −8 dBA in forward flight at −10° pitch, −3.5 to −5 dBA at −4°. Authors attribute it to the front-rotor wake energised over the airframe. Hover: one rotor −1 to −4 dB, full vehicle inconclusive [E] | Zawodny, Pettingill & Thurman 2022, Inter-Noise |
| Side-by-side rotors: thrust −7.9 % at 0.2 D tip gap, force oscillations mostly gone by 0.75–1.0 D, louder at 0.2 D than 1.0 D. Four isolated rotors, **no arms or body** [S] | Lee & Lee 2020, Phys. Fluids |
| 2→4 rotors added 6–8 dB broadband vs 3 dB for 1→2 (DJI Phantom II, static, chamber; authors note possible recirculation) [E] | Intaratep et al. 2016, AIAA |
| Two vehicles checked: Phantom 2 ≈ 0.46 D and NASA SUI Endurance ≈ 0.34 D tip gap (our arithmetic). Two examples, not a survey | Lee & Lee 2020; Pettingill et al. 2022 AIAA |
| Coaxial axial gap 0.2–0.4 D quietest at 8 N; below 0.2 D more blades = more tonal noise. Supporting optima cited in the paper include the same group's earlier work, so the agreement is less independent than it looks [E] | Hirono, Robertson & Torija 2024, JSV |
| 15-in contra-rotating pair: 17 mm spacing significantly louder than 48 mm; OASPL fell with spacing up to 70 mm [E] | McKay et al. 2021, Appl. Acoust. |
| Coaxial octocopter layout had the highest peak SPL of the three layouts simulated (+5 dB vs single-plane) [S] | Aziz & Shi 2024, Aerospace |
| Two 9-in props in 9 m/s inflow at 5000 rpm: 90° phase offset gave −19 dB at the first BPF **relative to in-phase (the worst case)**. The same group's earlier static test gave only −8 dB at BPF and −2 dB OASPL. "Spacing hardly matters" was tested only between s/D 1.01 and 1.05 [E] | Turhan et al. 2025, Drones |
| Inflow speed does not move the phase that gives the minimum [E] | Del Duchetto et al. 2025, Aerospace |
| With a ground plane present (both in and out of ground effect), OASPL rose ~6 dB in the reflection zone and fell in the shielded zone; within 1 D of the ground (L/R ≤ 2) typically another 1–2 dB. Single 10-in propeller [E] | Hanson et al. 2023, JSV |
| Solid ground +3 dBA at shallow angles at L/R = 1; porous ground removed ~2 dBA of it [E] | Jawahar et al. 2025, Sci. Rep. |
| Strut installation + forward flight radiate more than the steady blade loading (analytical model, generic strut) [S] | Roger & Moreau 2020, Acoustics |
| Rotor behind a body of revolution shows humps at BPF multiples (LES, 5-blade rotor, Re ≈ 1.9×10⁶ — far above drone scale) [S] | Zhou et al. 2024, JFM |

## Propellers and blades

| Finding | Paper |
|---|---|
| Twisted **and re-cambered** blade (twist and aerofoil changed together): +9.3 % figure of merit, up to −4.3 dB (−2.2 dB average) at the same thrust; 200 mm, hover [E+S] | Sun et al. 2023, Drones |
| Optimised MAV rotor vs a NACA0012 constant-chord baseline, 2 N: measured sound power −8.8 dB(A) and shaft power −3.9 W (Table 2; the figure caption says 10 dB(A)). Model over-predicted the tonal gain [E+S] | Serré et al. 2019, IJMAV |
| More blades quieter at constant thrust; louder broadband at constant tip speed. Chord and pitch fixed, so solidity rose with blade count [E] | Baskaran et al. 2024, JSV |
| Iso-thrust 2→5 blades: −10 dB in the rotor plane, no change at ±60° [E] | Gojon et al. 2021, JASA |
| Higher-solidity prop quieter at equal thrust only because it spins slower [E] | Jordan et al. 2020, AIAA |
| Boundary-layer trip: −3 to −11 % thrust; broadband −3.9 dB (commercial rotor) to −8.9 dB (optimised rotor) out of plane, up to −21 dB at 6.1 kHz at low tip speed; for one rotor type, tripping the outer 50 % of span was enough. R = 190.5 mm [E] | Pettingill & Zawodny 2026, NASA TM |
| LE trip: −5 dBA isolated, only −1.5 dBA on the full hovering drone [E] | Zhao et al. 2023, J. Phys. Conf. Ser. |
| TE serration design limits (h* > 0.25, angle < 45°, St > 1) are taken from earlier literature; in this paper's 23 serrated props tooth count seemed not to matter (possibly because some teeth stall) [R/E] | Candeloro et al. 2020, J. Phys. Conf. Ser. |
| CNC-machined serrations: −7.5 dB in hover, −12 dB in forward flight at their peak Strouhal number; ~5 % lift loss forward [E] | Li et al. 2018, Acoustics 2018 |
| 3D-printed cut-in serrations with a blunt root made broadband louder; add-on serrations reduced it. One 25 cm SLA rotor [E] | Santamaria et al. 2026, JSV |
| Plain TE plate >3 dB louder; serrated Gurney flap (3 mm, 1 mm gap, 3–6 cm from the tip) best of those tested within a 10 % efficiency budget [E+S] | Noda et al. 2022, Front. Aerosp. Eng. |
| Uneven blade spacing: −5 dB A-weighted tonal near the rotor plane, +4 dB below 50°; −8.5 % thrust with paired blades. **4-in propeller at tip Mach ~0.6 and ~37 000 rpm — not the multicopter regime** [E] | Kim 2016, UC Irvine thesis |
| Blade sweep more robust than uneven spacing (optimisation on in-plane SPL) [S] | Fruncillo et al. 2025, Forum Acusticum |
| Commercial 5-in toroidal: no noise or efficiency advantage; up to 10 dB louder than a high-pitch prop that was itself the least efficient [E] | Meister et al. 2026, Acta Acustica |
| Another toroidal study reports −5.2 / −19.6 dB(A) (radial/axial) at equal thrust — in conflict with the above [E+S] | Wei et al. 2024, Drones |
| Loop-tip blade: −4.7 dB isolated, −3.5 dB installed; lower modelled loudness and tonality, higher sharpness, slightly lower FM [E] | Sun et al. 2023, IJERPH |
| Winglets + serrations: +9.7 % thrust, −2.7 dB low-frequency broadband, up to −9.1 dB on certain BPF tones [E] | Khalaf & Kennedy 2025, Drones |
| Owl serration + cicada geometry: −5.5 dB vs one industry benchmark blade [E+S] | Wei et al. 2024, Nat. Commun. |
| Resin-printed 254 mm prop was the quietest of three copies (resin, wood, aluminium) [E] | Chen et al. 2025, Aerospace |
| Optimised prop: plain level change <1.8 dB but **computed** psychoacoustic-annoyance metric −20 % (no listening test). Its half-BPF shaft tone was higher [E] | Merino-Martínez et al. 2024, ICSV30 |

## Ducts and shrouds

| Finding | Paper |
|---|---|
| 5-in shrouded prop, CFD at three gaps only: 0.6 % and 1.1 % of R similar, sudden drop at 3.6 %. Where between 1.1 and 3.6 % the drop starts is not known [S] | Chew, Gan & Hesse 2021, AIAA |
| Tip gap 3.04→1.71 % R +17.85 % efficiency; 5.17 % below an open rotor — **cited from earlier work, not this paper's own result** [R] | Dayhoum et al. 2025, Appl. Sci. |
| Own experiment (16 cm rotor, 17 shrouds): up to +94 % thrust or −62 % power; 10° / 50 % diffuser optimum [E]. Struts moved 5.5 % Dt away → −10 dB is from fenestron tail-rotor tests quoted in the thesis [R] | Pereira 2008, PhD thesis |
| Diffuser length showed no correlation with thrust (CFD, authors say more data needed) [S] | Ma'arof et al. 2023 |
| Inlet-lip separation raised broadband and tip clearance was acoustically insignificant — **one 10-in fan study (Martin & Boxwell) quoted in a review** [R] | Zhang & Barakos 2020, Aeronaut. J. |
| 30 cm duct, 2 mm gap, no inflow: no region quieter, up to +12 dB at the top and bottom of the array; with 10 m/s inflow quieter at every mic [E] | Malgoezar et al. 2019, IJA |
| For their propeller and duct, tone attenuation was best with the propeller centred axially [E] | Simon et al. 2022, Inter-Noise |
| NASA 10-in duct: 1.27 mm tip gap, +4.6 % rpm needed to match thrust [E]; duct thickness at the prop plane ≥10 % D is Black & Wainauski's rule, quoted [R] | Zawodny et al. 2025, NASA TM |
| Per-prop shrouds +24 % FM vs whole-frame duct +9.7 % (CFD, aero only) [S] | Li, Yonezawa & Liu 2021, Drones |

## Linings and materials

| Finding | Paper |
|---|---|
| No 10–30 mm absorber can be flat-broadband from ~400 Hz; thin liners must be tuned resonators (our review of Yang et al. 2017) [T] | Koszałka, materials review |
| 23 mm Helmholtz liner (four units, one per duct wall) cut four tones of a 120 mm fan by 4.5–10.8 dB(A); mass flow −2.6 % [E] | Wu et al. 2025, Appl. Acoust. |
| 15 mm liner in a server fan under real flow: −3 dBA at the 620 Hz blade tone [E] | Killeen et al. 2023, Appl. Acoust. |
| Over-tip liner, 16-in prop: on-axis far field −6 dB at BPF but +9 dB at 2×BPF [E] | Pallejà-Cabré et al. 2025, Forum Acusticum |
| Tip liner 5 dB vs 3 dB for an inlet liner; tighter gap helped. **48-in low-speed fan** [E] | Sutliff & Jones 2009, J. Aircraft |
| Deliberately scratched sealing tape cut the transmission-loss peak of a printed liner sample by 10 dB [E] | Jamois et al. 2025, Acta Acustica |
| 9-resonator panel: near-perfect absorption 300–1000 Hz, but 11 cm deep (impedance tube) [E] | Jiménez et al. 2017, Sci. Rep. |
| Cork and rubber composites help mainly above ~1 kHz (second-hand values in our review). **We found** no acoustic data for EPP, XPS, cardboard or felt [T] | Koszałka, materials review |

## Beyond the propeller

| Finding | Paper |
|---|---|
| On one coaxial rig, the motor dominated below ~1500 rpm and the propeller above ~1860 rpm (the crossover is rig-specific) [E] | Russo et al. 2023, Aerospace |
| Periodic errors add tones; random errors add broadband (model) [S] | Zhong et al. 2023, JFM |
| Drones more annoying than road or aircraft noise at the same level [R] | Schäffer et al. 2021, IJERPH |
| For the sounds tested, annoyance tracked perceived noise level and sharpness [E] | Torija & Nicholls 2022, IJERPH |
| Synthetic helicopter-like bursts: 1 ms bursts annoy as much as 20 ms ones at 6–8 dB less [E] | Schlittenlacher & Wales 2023, Noise-Con |
| "Medical delivery" framing lowered annoyance (online listening test, eVTOL drone) [E] | Woodcock et al. 2025, Front. Acoust. |

## Audit, 2026-09-28 — what changed and why

Checked against the source texts, not the earlier summaries. Passages behind each correction were added to the EXTRACTS files ("Audit addenda").

**Wrong or misleading numbers**
- Hanson: "within 1 D of ground: +6 dB" was wrong. The ~6 dB appears in the reflection zone with the ground plane at any tested height (in and out of ground effect); levels fall in the shielded zone.
- Zawodny & Boyd: "conical arm ~6 dB louder" came from the one exception case (0.5 R, A-weighted, one mic, unweighted levels nearly identical).
- Serré: "10 dB(A), 4 W" is the figure caption; the measured table gives −8.8 dB(A) and −3.9 W, against a weak NACA0012 baseline.
- Turhan: −19 dB is relative to in-phase (worst) operation and in 9 m/s inflow. The same group measured only −8 dB at BPF (−2 dB OASPL) static. "Spacing hardly matters" covered s/D 1.01–1.05 only.

**Generalisations beyond the evidence**
- "Real quads run 0.34–0.46 D" came from two vehicles.
- "Sounds like an isolated rotor" became tonal levels at the measured mics.
- "Must centre the propeller" became "for their geometry".
- "Outer 50 % span is enough" applies to one rotor type only.
- "Leaky seams cost 10 dB" became deliberately scratched tape on one sample.
- "No data exist for EPP/XPS/cardboard/felt" became "we found none".
- "Annoyance −20 %" is a computed metric, not listeners.
- "Inlet separation drives duct broadband" rests on one 10-in study quoted in a review.

**Evidence tags corrected**
- Dayhoum tip-gap numbers: S → R (cited from earlier work).
- Candeloro serration limits: taken from earlier literature (R).
- NASA duct ≥10 % D thickness: R (Black & Wainauski).
- Pereira strut −10 dB: R (fenestron).
- Twist result: twist and camber changed together.

**Scale mismatches now flagged**
- Kim uneven spacing: 4-in, tip Mach 0.6.
- Sutliff: 48-in fan.
- Zhou: Re ≈ 1.9×10⁶.
- Schlittenlacher: synthetic helicopter-like sounds.
- Russo: rig-specific crossover.

**Independence**
- Hirono's supporting optima include the same group's work (Torija is a co-author), so the z/D 0.2–0.4 agreement is not fully independent. McKay adds an independent group for the "closer is louder" part only.
