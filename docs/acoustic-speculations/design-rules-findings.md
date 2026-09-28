# Quiet multicopter design rules — findings and their papers

Key findings from `quiet-multicopter-design-rules.pdf` (2026-09-28), each with its source.
Evidence tags: **E** experiment · **S** simulation/model · **R** reported second-hand · **T** our own reviews.
The verbatim quote and page behind each line are in `papers/SoundVisualizer/design-rules/EXTRACTS-*.md`
(private papers repo), which govern where this list and they disagree. Full list of all 101 sources: the PDF appendix.

## Vehicle layout — arms, spacing, rotor count

| Finding | Paper |
|---|---|
| Arm 0.1→0.2 R below the rotor tip gives the biggest drop (~8 dB, ~10 dBA tonal); by 0.4–0.5 R it sounds like an isolated rotor [E] | Zawodny & Boyd 2017, AHS Forum (NASA) |
| Conical arm ~6 dB louder than a round rod at same clearance [E] | Zawodny & Boyd 2017 |
| Rotors mounted under the arms 8.1 dB louder than above [S] | Zawodny, Christian & Cabell, NASA sUAS summary |
| Raising rotors 0.33 R above the airframe: −4 to −8 dBA in forward flight; noise came from front-rotor wakes shed over struts [E] | Zawodny, Pettingill & Thurman 2022, Inter-Noise |
| Side-by-side rotor interaction fades by 0.75–1.0 D tip gap; at 0.2 D −8 % thrust and louder [S] | Lee & Lee 2020, Phys. Fluids |
| 2→4 rotors adds 6–8 dB broadband vs 3 dB for 1→2 [E] | Intaratep et al. 2016, AIAA |
| Real quads run ~0.34–0.46 D tip gaps | Pettingill et al. 2022 AIAA; Lee & Lee 2020 |
| Coaxial axial gap 0.2–0.4 D quietest; below 0.2 D more blades = louder [E] | Hirono, Robertson & Torija 2024, JSV |
| 17 mm coaxial gap much louder than 48 mm (15-in props) [E] | McKay et al. 2021, Appl. Acoust. |
| Coaxial is the loudest octocopter layout (+5 dB) [S] | Aziz & Shi 2024, Aerospace |
| Rotor phase sync at 90°: −19 dB at first BPF; spacing then hardly matters [E] | Turhan et al. 2025, Drones |
| Inflow doesn't move the optimal phase [E] | Del Duchetto et al. 2025, Aerospace |
| Within 1 D of ground: ~+6 dB [E] | Hanson et al. 2023, JSV |
| Porous ground removes ~2 of the 3 dBA ground penalty [E] | Jawahar et al. 2025, Sci. Rep. |
| Struts/installation + forward flight outweigh steady blade loading [S] | Roger & Moreau 2020, Acoustics |
| Body ahead of rotor adds humps at BPF multiples [S] | Zhou et al. 2024, JFM |

## Propellers and blades

| Finding | Paper |
|---|---|
| Twisted blade: +9.3 % figure of merit and up to −4.3 dB at same thrust [E+S] | Sun et al. 2023, Drones |
| Optimised MAV rotor 10 dB(A) quieter and 4 W less power [E+S] | Serré et al. 2019, IJMAV |
| More blades quieter at constant thrust; louder broadband at constant tip speed [E] | Baskaran et al. 2024, JSV |
| 2→5 blades: −10 dB in rotor plane, no change at ±60° [E] | Gojon et al. 2021, JASA |
| Higher solidity is quieter only because it spins slower [E] | Jordan et al. 2020, AIAA |
| Boundary-layer trip: −3 to −11 % thrust, broadband −4 to −9 dB (up to −21 dB HF); outer 50 % span is enough [E] | Pettingill & Zawodny 2026, NASA TM |
| LE trip: −5 dBA isolated, only −1.5 dBA on full drone [E] | Zhao et al. 2023, J. Phys. Conf. Ser. |
| TE serrations need h* > 0.25, angle < 45°, St > 1; tooth count irrelevant [E] | Candeloro et al. 2020, J. Phys. Conf. Ser. |
| Machined serrations −7.5 dB hover, −12 dB forward, ~5 % lift loss [E] | Li et al. 2018, Acoustics 2018 |
| 3D-printed cut-in serrations (blunt root) make it louder; add-on ones quieter [E] | Santamaria et al. 2026, JSV |
| Plain TE plate >3 dB louder; serrated Gurney flap (3 mm, 3–6 cm from tip) best [E+S] | Noda et al. 2022, Front. Aerosp. Eng. |
| Uneven blade spacing: −5 dB A-weighted in plane, +4 dB below; −8.5 % thrust if paired [E] | Kim 2016, UC Irvine thesis |
| Blade sweep beats uneven spacing [S] | Fruncillo et al. 2025, Forum Acusticum |
| Commercial toroidal prop: not quieter, up to 10 dB louder [E] | Meister et al. 2026, Acta Acustica |
| …but another toroidal reports −5 to −20 dB(A) (conflict) [E+S] | Wei et al. 2024, Drones |
| Loop-tip blade −4.7 dB, lower loudness/tonality [E] | Sun et al. 2023, IJERPH |
| Winglets + serrations: +9.7 % thrust, up to −9 dB on tones [E] | Khalaf & Kennedy 2025, Drones |
| Owl serration + cicada geometry −5.5 dB [E+S] | Wei et al. 2024, Nat. Commun. |
| Resin-printed prop quieter than wood/aluminium copies [E] | Chen et al. 2025, Aerospace |
| Redesign with <1.8 dB level change can cut annoyance 20 % [E] | Merino-Martínez et al. 2024, ICSV30 |

## Ducts and shrouds

| Finding | Paper |
|---|---|
| Tip gap 0.6 % and 1.1 % R similar; sudden drop at 3.6 % [S] | Chew, Gan & Hesse 2021, AIAA |
| Tip gap 3.04→1.71 % R +17.85 % efficiency; 5.17 % worse than open rotor [S] | Dayhoum et al. 2025, Appl. Sci. |
| Shroud up to +94 % thrust / −62 % power; 10° / 50 % diffuser; struts moved 5.5 % Dt away −10 dB [E/R] | Pereira 2008, PhD thesis |
| Diffuser length no clear effect; tip gap dominates [S] | Ma'arof et al. 2023 |
| Inlet-lip separation, not tip gap, drives duct broadband noise [R] | Zhang & Barakos 2020, Aeronaut. J. |
| Static duct louder everywhere (up to +12 dB); with 10 m/s inflow quieter [E] | Malgoezar et al. 2019, IJA |
| Propeller must be centred axially for best tone reduction [E] | Simon et al. 2022, Inter-Noise |
| NASA duct: 1.27 mm gap, wall ≥10 % D; +4.6 % rpm to match thrust [E] | Zawodny et al. 2025, NASA TM |
| Per-prop shrouds +24 % FM vs whole-frame duct +9.7 % (aero only) [S] | Li, Yonezawa & Liu 2021, Drones |

## Linings and materials

| Finding | Paper |
|---|---|
| No 10–30 mm absorber can be flat from ~400 Hz; thin liners must be tuned resonators [T] | Koszałka, materials review |
| 23 mm Helmholtz liner cut four fan tones 4.5–10.8 dB(A), 2.6 % flow cost [E] | Wu et al. 2025, Appl. Acoust. |
| 15 mm liner under real flow: −3 dBA at a 620 Hz blade tone [E] | Killeen et al. 2023, Appl. Acoust. |
| Over-tip liner: −6 dB at BPF but +9 dB at 2×BPF [E] | Pallejà-Cabré et al. 2025, Forum Acusticum |
| Tip liner 5 dB vs 3 dB in inlet; tighter gap helps [E] | Sutliff & Jones 2009, J. Aircraft |
| Leaky seams in printed liners cost 10 dB [E] | Jamois et al. 2025, Acta Acustica |
| 9-resonator panel: near-perfect 300–1000 Hz, but 11 cm deep [E] | Jiménez et al. 2017, Sci. Rep. |
| Cork, rubber only help >1 kHz; no data exist for EPP, XPS, cardboard, felt [T] | Koszałka, materials review |

## Beyond the propeller

| Finding | Paper |
|---|---|
| Motor dominates below ~1500 rpm, propeller above ~1860 rpm [E] | Russo et al. 2023, Aerospace |
| Periodic errors add tones; random errors add hiss [S] | Zhong et al. 2023, JFM |
| Drones more annoying than road/aircraft at same level [R] | Schäffer et al. 2021, IJERPH |
| Annoyance driven by perceived noise level and sharpness [E] | Torija & Nicholls 2022, IJERPH |
| 1 ms bursts annoy as much as 20 ms ones at 6–8 dB less [E] | Schlittenlacher & Wales 2023, Noise-Con |
| "Medical delivery" framing lowered annoyance [E] | Woodcock et al. 2025, Front. Acoust. |
