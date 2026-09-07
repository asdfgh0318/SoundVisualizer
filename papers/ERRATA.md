# ERRATA — corrections from the 2026-09-07 claim-by-claim audit

Source: `AUDIT-1.md` … `AUDIT-5.md` (five Sonnet auditors, one per batch, each reading the paper text and checking every number, quote and page reference attached to it in the extracts, matrices and the four docs). This file lists what was **wrong** and where it was fixed. Page-number slips of ±1 page and rounding of printed values are recorded in the AUDIT files but not repeated here.

## Wrong facts (fixed in the docs)

| # | Where | Was | Now | Source of truth |
|---|---|---|---|---|
| 1 | brief §03 | "rooms that qualify under the 1977 broadband rule can carry A-weighted errors of 6.4–7.3 dB" | the free-r₀ **ISO 3745:2003** regression carries 6.4–7.3 dB; the 1977 rule 0.8–1.5 dB | Simmons, Jobling & Payne 2004, pp. 45, 51 (AUDIT-5) |
| 2 | brief §02 table | "BPF harmonics ≥ 2 jump 15–30 dB" cited to Stephenson, Weitsman, Nardari, Whelchel | 15–30 dB is Stephenson/Weitsman only; Nardari 5–10 dB for harmonics ≥ 3; Whelchel ≥ 7–8 dB | AUDIT-5 |
| 3 | brief §04d, synthesis §03 | "24 mm 75 PPI foam" | the 24 mm treatment is "75PPI-T"; "75PPI" is a different 12 mm foam; the 13 dB is within 1.5–10 kHz | Jawahar et al. 2025 (AUDIT-4) |
| 4 | brief §02 table | Kim 2022 cited for "excess below 50–100 Hz at microphones under the rotor" | Kim's microphones were above a hovering drone and read ~3 dB high in A-weighted level, no band breakdown | AUDIT-4 |
| 5 | brief, synthesis, matrix | Singh below-cut-off slope "0.1–0.3 dB per doubling at 100 Hz" | 0.01–0.30 dB (Tables 2–3) | AUDIT-4 |
| 6 | brief §01 | Haasjes quote "designed for 75 Hz" | "designed with a cut off frequency of 75 Hz" | AUDIT-4 |
| 7 | brief §02 table | Rizzi row: "keep the source as far as possible from the walls" | that sentence is Schneider's; Rizzi says keep microphones off walls below 250 Hz | AUDIT-5 |
| 8 | brief §02 table | Schlinker & Amiet row: "lose coherence … coherence-loss model or Kevlar wall" | coherence loss and Kevlar are Bahr 2020/2021; Schlinker & Amiet report tone broadening and amplitude change | AUDIT-5 |
| 9 | brief ledger, RETRIEVAL-A, filename | "Amiet 1981, NASA CR-3371" | Schlinker & Amiet, NASA CR-3371, December 1980 | title page (AUDIT-3) |
| 10 | synthesis matrix, chamber-problems matrix | Stephenson 2019 "JASA-EL" | JASA 145(3) Letter, doi:10.1121/1.5092213 | AUDIT-5 |
| 11 | synthesis §03 | SHAC "40 m³" | ≈32 m³ from the printed dimensions | AUDIT-5 |
| 12 | review card 06 | ITMO "0.5–0.9 m in every direction" | 0.5–0.8 m in every direction (0.9 m in three of four; Table 3) | AUDIT-1 |
| 13 | review card 01, brief §01 | Jiang "57 % of the centre-to-corner line" | 56.7 % of the centre-to-vertex line | AUDIT-1 |
| 14 | review §04 | "uncertainty-quantification studies … target exactly three parameters: flow resistivity, thickness, hard-surface absorption" attributed to Vorländer | not in Vorländer; replaced by Prinn §6.3.1's statement | AUDIT-2 |
| 15 | review, one-pager, bibliography | "Beranek & Sleeper 1946, JASA" | the held document is Beranek, Sleeper & Moots, OSRD Report 4190, 1945; the JASA article is not held | AUDIT-2 |
| 16 | review ledger | "NIST TN 1305 … methodological only" | National Bureau of Standards TN 1305 (1986), an empirical off-axis error study | AUDIT-1 |
| 17 | review §06 | "5.604 ms gate valid above 178 Hz" | ARTA prints 177.9 Hz (and 178.4 Hz in its arithmetic note) | AUDIT-2 |
| 18 | review figure | "leaves ±1.5 dB at 1.32 m" (Nash) | derived from Nash's fit, not printed; now labelled as derived | AUDIT-2 |
| 19 | reflection review ledger | Sun 2012 / Mabande 2013 "not retrieved" | both held and audited; ledger text replaced | AUDIT-3 |
| 20 | reflection review §01/§04 | Lovedee-Turner "11.5–18.9 cm measured", "16–25 cm once non-convex" | 11.5–18.9 cm are simulated L-room sets; the real room is 15.4 cm RMS; non-convexity as such does not degrade accuracy (L room 4.7 cm, T room 16.5 cm) | AUDIT-3 |
| 21 | EXTRACTS-core (Bonfiglio) | "agrees except within ~1 m of the source where differences are 1.5–5 dB" | no radius is attached to the near-source discrepancy; the ~1 m figure belongs to free-field persistence near the boundaries | AUDIT-1 |
| 22 | EXTRACTS-local (Stephenson) | elevation "0° to −43.6°" | +43.6° to −34.9° (pdftotext drops the signs) | AUDIT-5 |
| 23 | EXTRACTS-local (Weitsman) | meshes "36–72 % open area" | 35–72 % | AUDIT-5 |
| 24 | EXTRACTS-downloaded (Jenny & Anderson) | letter "adds" the ORM sentence | already in the thesis conclusion | AUDIT-4 |
| 25 | matrices, bibliography | Hochbaum venue "unclear" | Quiet Drones 2026, Delft (printed as an image) | AUDIT-4 |
| 26 | matrices, bibliography | Rodriguez "AMTA 2016?" | AMTA 2017, doi:10.23919/AMTAP.2017.8123694 | AUDIT-2 |
| 27 | review ledger | Prinn "Acoustics 5(2) 22"; Aussal title truncated | Acoustics 5, 367–395; "… in complex structures", pp. 6059–6066 | AUDIT-1/2 |

## Findings about the sources themselves (not our errors)
- Bikmukhametov (ITMO): prose gives 16 000 / 8 000 Hz upper limits for directions III/IV; its own Table 3 supports 10 000 / 4 000 Hz.
- Merino-Martínez 2020: designed cut-off 173.5 Hz, conclusion says 200 Hz, gap unremarked.
- Belyaev 2015: AC-11 volume 230 m³ (English) vs 210 m³ (Russian original).
- Singh 2020: Eq. 4 and Eq. 5 are algebraically identical yet Table 4 lists 320 and 312 Hz for them.
- Kanda & Wyss 1986: Table 1 prints ±1.2 dB where the prose says ±1.4 dB for the same case.
- Both Schmal papers print no venue or year; the earlier "Quiet Drones / Inter-Noise 2023" attribution was never supported and is withdrawn.

## Still unverified
- Huang (Bristol student report): the review cited "arXiv:2510.26453" for it; no arXiv identifier appears in the document. Treat as an unreviewed report.
