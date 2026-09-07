# Small-chamber literature — retrieval log

Search scope: acoustic problems specific to SMALL anechoic/hemi-anechoic chambers and
near-wall measurement (wedge-tip/wall reflections at short range, direct–reflected
comb filtering, minimum mic/source-to-wall distance, small-chamber qualification,
mini "anechoic box" designs, image-source analysis, low- vs. mid/high-frequency
reflection). Searched via WebSearch (10 queries) and attempted Semantic Scholar
(`api.semanticscholar.org`, persistently returned HTTP 429 across ~6 retries with
5–25 s backoff throughout the session — treat S2 as unavailable for this run, not as
"no results"); DOI/author confirmation for paywalled items used the Crossref API
(`api.crossref.org`, unthrottled, worked throughout).

Already-held papers turned up repeatedly by the searches and **not re-fetched** (per
task instructions), confirmed by filename match against `papers/anechoic-simulation/`
and `papers/chamber-problems/`: Cunefare 2003 JASA, Nash 2019 ICA, Jiang 2016 JSV,
Schneider 2009 JSV, Bonfiglio 2013 JASA, Bikmukhametov 2026 arXiv (ITMO), Singh 2020
IJA, Ressl & Wundes (WSEAS), Friot 2009, Fasulo 2025, Ma 2022/2024 (all three
recirculation papers: Stephenson 2019 JASA, Weitsman 2020 JASA, Ma 2024 Acoustics
Australia), Gonzalez & Kob 2026, Rasmussen 2022, Jawahar 2025, Haasjes 2025, Alkmim
2022, Merino-Martinez 2020, Rizzi 2013, Zawodny & Haskin 2017, NPL DQL-AC 007, Garg
2019 MAPAN.

## Retrieved — PDF read at source (see `EXTRACTS.md`)

| # | Citation | DOI | Status | File |
|---|----------|-----|--------|------|
| 1 | Burnett & Nedzelnitsky (1987), *J. Res. NBS* 92(2), pp.129–151 | 10.6028/jres.092.013 | **PDF read at source** | `Burnett-Nedzelnitsky_1987_JResNBS_free-field-reciprocity-calibration-chamber-deviations.pdf` |
| 2 | Rajmane & Baumann (2016), DAGA Aachen, pp.331–333 | none (conference proceedings) | **PDF read at source** | `Rajmane-Baumann_2016_DAGA_detection-reflecting-objects-anechoic-chambers.pdf` |
| 3 | Orrego González, Ealo Cuello & Pazos Ospina (2018), *Scientia et Technica* 23(4), pp.471–478 | none found (institutional journal; ISSN 0122-1701) | **PDF read at source** | `Orrego-Ealo-Pazos_2018_ScientiaTechnica_low-cost-small-anechoic-chamber.pdf` |
| 4 | Biesel & Cunefare (2003), *Sound and Vibration*, May 2003, pp.22–26 | none (trade magazine) | **PDF read at source** — companion of already-held Cunefare 2003 JASA; corroborating, not independent | `Biesel-Cunefare_2003_SoundVibration_test-system-freefield-qualification.pdf` |
| 5 | Rusz (2015), KTH Master's thesis, TRITA-AVE 2015:36 | none (thesis) | **PDF read at source — TANGENTIAL** (designs a 367.5 m³ chamber, not small; wedge-theory background only) | `Rusz_2015_KTH-thesis_design-of-fully-anechoic-chamber.pdf` |
| 6 | Cao et al. (2025), Forum Acusticum 2025 (11th EAA Convention), Málaga | 10.61782/fa.2025.0137 | **PDF read at source — TANGENTIAL** (drone SPL-scaling study, not about chamber reflections; chamber not small) | `Cao-etal_2025_ForumAcusticum_sub-7kg-multirotor-anechoic-noise.pdf` |

## Not retrieved

| # | Citation | DOI | Best URL for manual fetch | Why not retrieved |
|---|----------|-----|---------------------------|--------------------|
| 7 | Yürek & Lokki (2026), "Experimental investigation of grazing-incidence sound propagation over free-standing absorbers," *Acta Acustica* 10 | 10.1051/aacus/2026022 | https://acta-acustica.edpsciences.org/articles/aacus/full_html/2026/01/aacus250223/aacus250223.html (PDF: `.../pdf/2026/01/aacus250223.pdf`) | Cloudflare JS challenge on both the HTML page (WebFetch → 403) and the direct PDF URL (curl → JS-challenge HTML, not a PDF); no arXiv/Aaltodoc mirror found in 4 attempts. **Highly relevant to this task's grazing-incidence question — recommend Adam fetch manually and drop it in `papers/small-chamber/`.** |
| 8 | Vesa (2020), "Design of an anechoic chamber for aeroacoustic testing and analysis of large UAS propellers," Master's thesis, Mississippi State University | none (thesis) | https://scholarsjunction.msstate.edu/td/1307/ (PDF behind `viewcontent.cgi?article=2306&context=td`) | bepress/Digital Commons returned HTTP 403 to curl with two different User-Agent/Referer combinations; the abstract confirms topical relevance (UAS-propeller-specific chamber design) but full text unconfirmed for reflection/qualification numbers. |
| 9 | Lokki, Pulkki & Calamia (2008), "Measurement and modeling of diffraction from an edge of a thin panel," *Applied Acoustics* 69(9) | 10.1016/j.apacoust.2007.05.005 | https://www.sciencedirect.com/science/article/abs/pii/S0003682X07000953 | ScienceDirect — known blocker, abstract only. Directly relevant to "edge diffraction" in the search brief (measures diffraction from a thin panel edge mounted in an anechoic room with wedges on 2 of 3 edges). |
| 10 | Tavakkoli Nejad, Loghmani & Ziaei-Rad (2020), "The effects of wedge geometrical parameters and arrangement on the sound absorption coefficient," *Applied Acoustics* 169, 107458 | 10.1016/j.apacoust.2020.107458 | https://www.sciencedirect.com/science/article/abs/pii/S0003682X20305624 | ScienceDirect — known blocker, abstract only. |
| 11 | Zhou, Jiang & Huang (2022), "Quad-copter noise measurements under realistic flight conditions," *Aerospace Science and Technology* 124, 107542 | 10.1016/j.ast.2022.107542 | https://www.sciencedirect.com/science/article/abs/pii/S1270963822002164 | ScienceDirect — known blocker, abstract only. Abstract/snippet mentions chamber-floor reflections redirecting tonal energy into directions classical theory predicts should be blocked — could be directly relevant, but chamber described (ground array 5.6 m × 6.4 m) is not small, and text unconfirmed since only abstract was seen. |
| 12 | Moreland (1989), "Performance of Hemi-Anechoic Rooms for Industrial Applications," *Noise Control Engineering Journal* 32(1) | 10.3397/1.2827723 | https://ince.publisher.ingentaconnect.com/content/ince/ncej/1989/00000032/00000001/art00001 | Ingenta Connect — paywalled, abstract only (carousel-method comparison of wedge-lined vs. resonator-block hemi-anechoic rooms). |
| 13 | Eckel & Ver (2000), "Anechoic wedge design and development/anechoic chamber qualification testing," *J. Acoust. Soc. Am.* 108(5) meeting abstract | 10.1121/1.4743113 | https://pubs.aip.org/asa/jasa/article-abstract/108/5/2477/561142 (approx.) | AIP/JASA — known blocker, abstract only. |
| 14 | [Authors unconfirmed] (c.2013), "Design and qualification testing of a miniature anechoic chamber for the calibration of small medical devices" | no DOI found | https://www.researchgate.net/publication/293101716 | ResearchGate — known blocker; no independent journal/DOI record found via Crossref. Topically strong match (small ~128 Hz-cutoff chamber, ISO 3745 qualification, built for hearing-aid-scale devices) but only search-snippet-level content seen — **no verbatim quote used anywhere; abstract-level only, flagged as such.** |

## Notes on search process

- Semantic Scholar's REST API rate-limited (`429 Too Many Requests`) on every one of
  ~6 attempts spread across the session with increasing backoff (5 s, 15 s, 20 s,
  25 s) — this looks like a standing block on the environment's egress IP rather than
  a per-request throttle. All openAccessPdf lookups that would normally go through S2
  were done instead via targeted WebSearch + Crossref bibliographic search (Crossref
  was not rate-limited and supplied correct DOIs/authors for items 9–14 above).
- Additional papers surfaced by search that turned out to be near-duplicates of
  already-held items (confirmed and excluded, not listed as separate candidates
  above): "On the acoustic wedge design and simulation of anechoic chamber" (JSV
  2016) = held `Jiang_2016_JSV`; "Numerical prediction of the quality of an anechoic
  chamber in the low frequency range" = held `Schneider_2009_JSV`; "NUMERICAL
  METHODOLOGY FOR DETERMINING THE CUT-OFF FREQUENCY OF THE ANECHOIC CHAMBER OF THE
  UNIVERSITY OF FERRARA" and "Numerical methodologies for optimizing/predicting the
  low-frequency behavior of anechoic chambers" (JASA 2013) = held
  `Bonfiglio-Pompoli_2013_JASA`; "Design of an Acoustic Anechoic Chamber for
  Application in Hearing Aid Research" = held `Ressl-Wundes_nd_WSEAS`; "Estimation
  and global control of noise reflections" (arXiv 0911.4639) = held
  `Friot-Gintz_2009_arXiv`; three flow-recirculation UAS papers (Stephenson 2019 JASA,
  Weitsman 2020 JASA, "Experimental Assessment of the Flow Recirculation Effect..."
  Acoustics Australia 2024) = held `Stephenson_2019_JASA`, `Weitsman_2020_JASA`,
  `Ma_2024_AcoustAust`; "Experimental Acoustic Investigation of Rotor Noise
  Directivity and Decay..." (Aerospace 2025, DOI 10.3390/aerospace12070647) = held
  `Fasulo_2025_Aerospace`.
