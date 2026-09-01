# Papers still to fetch

Adam is pulling these through a university proxy. Drop the PDFs into the directory
named in each section — any filename, they get normalised on ingest.

**When they land:** re-check every claim tagged `○` (abstract-only) in
[`docs/anechoic-simulation.html`](../docs/anechoic-simulation.html) and
[`docs/reflection-localization.html`](../docs/reflection-localization.html) against the
actual text, correct whatever the abstracts got wrong, and promote the tag to `●`.
The one-pager PDF (`docs/anechoic-simulation-onepager.pdf`) is derived from the review,
so re-render it *after* the review is corrected, never in parallel.

---

## Priority 1 — these change what the reviews say

→ `papers/anechoic-simulation/`

- [ ] **Bonfiglio, P. & Pompoli, F. (2013)** — *Numerical methodologies for optimizing and
      predicting the low frequency behavior of anechoic chambers.* JASA 134(1) 285–291.
      <https://doi.org/10.1121/1.4807820>
      **Why:** the core methodology paper. All of §01 — converting wedge impedance to a
      spherical-wave oblique-incidence reflection coefficient and predicting the interior
      field with complex image sources instead of meshing the room — is currently sourced
      from its abstract. If one paper gets fetched, this is it.

- [ ] **Cunefare, K. A. et al. (2003)** — *Anechoic chamber qualification: traverse method,
      inverse square law analysis method, and nature of test signal.* JASA 113(2) 881–892.
      <https://doi.org/10.1121/1.1527595>
      **Why:** failure mode 09 — that the choice of reference/fitting method changes the
      pass/fail verdict, "significantly" so for pure-tone qualification. Quoted from the
      abstract; the size of the effect is unknown to us.

- [ ] **Schneider, S. (2009)** — *Numerical prediction of the quality of an anechoic chamber
      in the low frequency range.* JSV 320(4–5) 990–1003.
      <https://doi.org/10.1016/j.jsv.2008.08.019>
      **Why:** the other low-frequency chamber-prediction paper. Unread entirely — cited
      only as existing.

- [ ] **Jiang, C., Zhang, S. & Huang, L. (2016)** — *On the acoustic wedge design and
      simulation of anechoic chamber.* JSV 381 139–155.
      <https://doi.org/10.1016/j.jsv.2016.06.020>
      **Why:** the UGFW (uniform-then-gradient flat-wall) alternative to wedges, which
      reportedly hits 100–250 Hz cut-offs in less total depth. Only matters if a chamber
      actually gets built, but then it matters a lot.

## Priority 2 — quoted numbers currently rest on abstracts

→ `papers/anechoic-simulation/`

- [ ] **Vorländer, M. (2013)** — *Computer simulations in room acoustics: concepts and
      uncertainties.* JASA 133(3) 1203–1213. <https://doi.org/10.1121/1.4788978>
      **Why:** §04's claim that the input-data quality needed for JND-accurate prediction
      is not obtainable from reverberation-room measurements.

- [ ] **Brinkmann, F. et al. (2019)** — *A round robin on room acoustical simulation and
      auralization.* JASA 145(4) 2746. <https://doi.org/10.1121/1.5096178>
      **Why:** the ±5 dB max-deviation figure behind failure mode 12.

- [ ] **Singh, K. S., Garg, M. & Narayanan, S. (2020)** — *Estimation of the lower cut-off
      frequency of an anechoic chamber: an empirical approach.* Int. J. Aeroacoustics.
      <https://doi.org/10.1177/1475472X20905070>
      **Why:** the ±3 % empirical cut-off formula in failure mode 01.
      **Note:** SAGE blocks the PDF but renders full text in a browser —
      <https://journals.sagepub.com/doi/10.1177/1475472X20905070> may be readable directly.

→ `papers/reflection-localization/`

- [ ] **Sun, H., Mabande, E., Kowalczyk, K. & Kellermann, W. (2012)** — *Localization of
      distinct reflections in rooms using spherical microphone array eigenbeam processing.*
      JASA 131(4) 2828. <https://doi.org/10.1121/1.3688476>
- [ ] **Mabande, E., Kowalczyk, K., Sun, H. & Kellermann, W. (2013)** — *Room geometry
      inference based on spherical microphone array eigenbeam processing.* JASA 134(4).
      <https://doi.org/10.1121/1.4820895>
      **Why (both):** the foundational spherical-array localisation work. The tier-3
      accuracy figures in the diagnostics review come from Lovedee-Turner alone; these
      would turn one data point into a range.

## Priority 3 — background, nothing hangs on them

→ `papers/anechoic-simulation/` (first four), `papers/reflection-localization/` (last)

The wedge-modelling lineage, for completeness if the chamber gets built:

- [ ] Easwaran, V. & Munjal, M. L. (1993) — FEM of wedges used in anechoic chambers. JSV
      160(2) 333–350. <https://doi.org/10.1006/jsvi.1993.1027>
- [ ] Wang, C.-N. & Tang, M.-K. (1996) — BEM evaluation of sound-absorbing wedges. EABE
      18(2) 103–110. <https://doi.org/10.1016/S0955-7997(96)00017-3>
- [ ] Kar, T. & Munjal, M. L. (2006) — Plane-wave analysis of acoustic wedges via the
      boundary-condition-transfer algorithm. Appl. Acoust. 67(9) 901–917.
      <https://doi.org/10.1016/j.apacoust.2005.11.009>
- [ ] Tavakkoli Nejad, M. E., Loghmani, A. & Ziaei-Rad, S. (2020) — Wedge geometry and
      arrangement vs absorption coefficient. Appl. Acoust. 169 107458.
      <https://doi.org/10.1016/j.apacoust.2020.107458>
- [ ] Pawlak, A. & Lee, H. (2026) — Spatial segmentation of impulse response for room
      reflection analysis. Appl. Acoust. 249 111303.
      <https://doi.org/10.1016/j.apacoust.2026.111303>
      SSRN preprint may be free: <https://doi.org/10.2139/ssrn.5708563>

## Free — no proxy needed, just a browser

- [ ] Dereverberation beamforming for noise source localization in anechoic and
      semi-reverberant environments. <https://pmc.ncbi.nlm.nih.gov/articles/PMC11987664/>
      Open access; PMC blocks automated download but a browser gets it in seconds.
      → `papers/reflection-localization/`

## Worth more than any single paper — the full ISO texts

We hold published previews only (scope, terms, tolerance tables) — they stop before the
annexes, which is where the useful part is. If FESB/PKN or the university has an ISO
subscription:

- [ ] **ISO 5305:2024** — Noise measurements for UAS. **Annex B** (numerical validation of
      the far-field condition) and **Annex C** (a measured far-field determination for a UAS
      propeller in an anechoic chamber, following ISO 26101-1). Annex C is the closest
      published thing to our exact measurement.
- [ ] **ISO 26101-1:2021** — Annex A: default traverse layouts and qualification criteria.
- [ ] **ISO 26101-2:2024** — Clauses 5–8, the four K₂ procedures in full, plus Annex A on
      the uncertainty of the environmental correction.

---

## Retrieval routes — do not re-try the dead ends

Confirmed **blocked** to automated fetching this session: AIP (`pubs.aip.org`), Elsevier
(`sciencedirect.com`), SAGE PDFs, ResearchGate, Academia.edu, `ets-lindgren.com`
(white papers moved to `/articles/`), PMC's `/pdf/` route, ANSI webstore previews.

Confirmed **working**, and worth remembering:

| Route | Pattern |
|---|---|
| White Rose (York, Leeds, Sheffield) | `eprints.whiterose.ac.uk/<id>/1/Manuscript_*.pdf` — got Lovedee-Turner |
| Aaltodoc (DSpace 7 REST) | item UUID → `/server/api/core/items/<uuid>/bundles` → `/bundles/<uuid>/bitstreams` → `_links.content.href` — got Meyer-Kahlen |
| DEGA proceedings (ICA, DAGA) | `pub.dega-akustik.de/<CONF>/data/articles/<id>.pdf` — open |
| Euronoise | `euronoise2018.eu/docs/papers/<n>_Euronoise2018.pdf` — **needs `curl -k`**, bad cert chain |
| ISO published previews | `cdn.standards.iteh.ai/samples/<id>/<hash>/<STD>.pdf` |
| MDPI | `mdpi-res.com/d_attachment/...`, never `mdpi.com` |
| Crossref for DOIs | `api.crossref.org/works?query.bibliographic=...` — fast, no rate limit |
| Semantic Scholar for OA mirrors | rate-limits hard; pace requests or it 429s the whole batch |
