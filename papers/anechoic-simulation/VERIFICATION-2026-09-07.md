# Source Verification Report — docs/anechoic-simulation.html re-check

Mode: `deep-research` / fact-check (source_verification_agent protocol, §4 Factual Claim Verification), run by hand from `~/.claude/skills/deep-research/agents/source_verification_agent.md` on 2026-09-07. Scope: every claim in the review that was tagged ○ (abstract or secondary report) plus every untagged passage citing a paper whose full text arrived today. Source texts: `txt/` in this directory and `../chamber-problems/txt/`.

## Overall assessment

Claims reviewed: 8 · Verified as written: 3 · Verified with added precision: 4 · **Corrected: 1** · Sources still unread: 3 (cited only as existing).

## Claim matrix

| # | Claim in review (before) | Source | Full-text check | Outcome |
|---|---|---|---|---|
| 1 | Singh et al. 2020 "fit an empirical cut-off from source volume, chamber volume and wedge height to within ±3% of measurement" (card 01) | Singh, Garg & Narayanan, Int. J. Aeroacoustics 19(1–2) 57–72 — `../chamber-problems/txt/ijaeroacoustics2020_singh_*` | Formula is f = 2.25c/(d − l_w − a) (Eq. 5, p. 59); inputs are source-to-wall distance, wedge length, source size, not volumes. "within 3%" (abstract p. 57; conclusions p. 70) — no ± sign. Validated on a single chamber, the authors' own (Table 4, p. 68: 320/312 Hz vs 315 Hz). | **Rewritten** with the formula, the single-chamber caveat, and the below-cut-off slopes (Tables 2–3). Tier ○→● |
| 2 | Cunefare et al. 2003: optimal reference method "significantly improves the apparent performance of the chamber for pure tone qualifications" (card 09) | JASA 113(2) 881–892 — `txt/jasa2003_cunefare_*` | Exact abstract wording: "is shown to significantly improve the apparent performance of the chamber for pure tone qualifications" (p. 881). Table IX (p. 891): 80 Hz LNE tone 56 % → 13 % out of tolerance. Table X: two offsets > 2× source dimension coincide with worst traverses. | **Verified**; quote made exact, numbers added. ○→● |
| 3 | "Round-robin studies … up to ±5 dB maximum deviation on sound strength and >50% differences on some quantities, with errors concentrated where modal density is low" (card 12) | Brinkmann et al., JASA 145(4) 2746–2760 — `txt/jasa2019_brinkmann_*` | No "±5 dB", no "sound strength", no "modal density" statement in the paper. What it says: errors "once the assumptions of geometrical acoustics are no longer met" (abstract); RT overestimated 58 % at 125 Hz, 35 % at 250 Hz (p. 2753); spectral errors 2–2.5 dB (p. 2754); no algorithm within JND in all bands (p. 2758–59); comb-filter structure of a diffusor reflection not matched (p. 2758). | **Corrected**: figures withdrawn, replaced by Brinkmann's own; withdrawal noted in the card. ○→● |
| 4 | Vorländer 2013: input-data quality for JND-accurate RT "is simply not available from reverberation-room measurements" (§04) | JASA 133(3) 1203–1213 — `txt/jasa2013_vorlander_*` | Abstract, p. 1203: "prediction of reverberation times with accuracy better than the just noticeable difference requires input data in a quality which is not available from reverberation room measurements". Also p. ~1208: "it is not adequate to 'calibrate' a computer model by modification of input data". | **Verified**; direct quotes substituted. Untagged→● |
| 5 | Stage A methodology: Bonfiglio & Pompoli turn the impedance into a spherical-wave oblique-incidence reflection coefficient and predict the field with complex image sources (§01 method stack, §06 Stage A, one-pager) | JASA 134(1) 285–291 — `txt/jasa2013_bonfiglio_*` | §II.A–B: FEM of four wedges in a virtual impedance tube → normal-incidence impedance → R_pw(θ) → R_sw via Chien & Soroka F(p_e) → image-source sum to 20th order, convergence < 0.05 dB / 0.5°, 7th order sufficed. Caveat: they used an FEM of the wedge, not a flat-sample tube measurement, and a locally-reacting R_pw. | **Verified as written**; the review's Stage A already inserts the FEM unit-cell step and flags the locally-reacting shortcut. Added to card 01: free field "up to a distance of around 1 m from the boundaries" below cut-off (p. 291). |
| 6 | Schneider 2009 "unread entirely — cited only as existing" (ledger) | JSV 320 990–1003 — `txt/jsv2009_schneider_*` | Local admittance "failed to predict the quality of the chambers at frequencies below ~150 Hz, regardless of the admittance applied" (p. 996); α = 0.997/1.0/0.997 linings give different 1.5 dB regions (Fig. 8, p. 998); asymmetry 170–190 Hz; non-local admittance matrix recovers 110–160 Hz perturbations (p. 1001). | **Added** as ● evidence on card 03 (locally-reacting assumption). |
| 7 | Jiang et al. 2016: UGFW "reportedly hits 100–250 Hz cut-offs in less total depth" (TODO note; review cites only as existing) | JSV 381 139–155 — `txt/jsv2016_jiang_*` | Fig. 7 / §3.1: UGFW minimum depth smaller than wedge for cut-offs 100–250 Hz (p. 147–148). Stronger finding: 99 % absorption ≠ anechoic; effective cut-off 128 Hz (wedge) / 120 Hz (UGFW) vs 100 Hz design (Table 3, p. 153). | **Verified**; the 99 %→10 % pressure-reflection point and 128 Hz figure added to card 01. |
| 8 | Wang & Tang 1996 — cited only as existing | Eng. Anal. Bound. Elem. 18 103–110 — `txt/eabe1996_bem_*` | Cut-off "strongly affected by the length of the wedge and the flow resistance"; base/air-gap thickness barely move it; 10–20 cm tip cut harmless, 30 cm not (§6, p. 109). | **Verified**; moved to read-at-source list. Used in the companion brief, not in the review body. |

## Still unread (cited only as existing)

Easwaran & Munjal 1993 (10.1006/jsvi.1993.1027) · Kar & Munjal 2006 (10.1016/j.apacoust.2005.11.009) · Tavakkoli Nejad et al. 2020 (10.1016/j.apacoust.2020.107458). No claim in the review depends on them.

## Derived documents

`docs/anechoic-simulation-onepager.html/.pdf` re-rendered after the review was corrected (card 12 sentence and the "blocked" panel replaced). The review governs where the one-pager disagrees.

## Not in scope

`docs/reflection-localization.html` still carries ○ tags for Sun et al. 2012 and Mabande et al. 2013; both full texts are now in `../reflection-localization/txt/` and the same pass is owed there.
