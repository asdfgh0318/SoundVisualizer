## Thread I — retrieval log

## RETRIEVED

### New (this thread)

| Citation | DOI/ID | Route | File |
|---|---|---|---|
| Zawodny, N. S., Boyd, D. D. Jr. & Burley, C. L. *Acoustic Characterization and Prediction of Representative, Small-Scale Rotary-Wing Unmanned Aircraft System Components.* AHS 72nd Annual Forum, West Palm Beach, FL, 2016. | NASA NTRS 20160009054 | NTRS API: `ntrs.nasa.gov/api/citations/search` (POST JSON `{"q": "..."}`) → id → `ntrs.nasa.gov/api/citations/20160009054/downloads/20160009054.pdf` via `curl -sL -A "Mozilla/5.0 ..."` | `arc-validation/Zawodny-Boyd-Burley_2016_AHSForum72_SALT-facility-small-rotor-characterization.pdf` |
| Zawodny, N. S. & Boyd, D. D. Jr. *Investigation of Rotor-Airframe Interaction Noise Associated with Small-Scale Rotary-Wing Unmanned Aircraft Systems.* AHS 73rd Annual Forum, Fort Worth, TX, 2017 (distributed via NTRS 2019). | NASA NTRS 20180001470 | Same NTRS API route, GET form (`curl -G --data-urlencode "q=..."`) | `arc-validation/Zawodny-Boyd_2017_AHSForum73_rotor-airframe-interaction-SALT.pdf` |
| Zawodny, N. S., Schiller, N. H., Pettingill, N. A. & Medina, G. L. *Aerodynamic and Acoustic Characterization of a Ducted Propeller in a Small Hover Anechoic Chamber.* NASA/TM–20250009190, Sept. 2025. | NASA NTRS 20250009190 | Same NTRS API route | `arc-validation/Zawodny-Schiller-Pettingill-Medina_2025_NASA-TM-20250009190_ducted-propeller-SHAC.pdf` |
| Pettingill, N. A. & Zawodny, N. S. *Aerodynamic Performance and Acoustic Impacts of Varying Tip Speeds and Tripping Conditions on Small Rotors in an Anechoic Hover Chamber.* NASA/TM–20250003316, cover dated March 2026. | NASA NTRS 20250003316 | Same NTRS API route | `arc-validation/Pettingill-Zawodny_2026_NASA-TM-20250003316_tip-speed-tripping-SHAC.pdf` |

All four confirmed genuine PDFs (`file` reports "PDF document"), identity confirmed from each
PDF's own front matter: filename metadata + visual page-1 read for the 2016 AHS paper (its
`pdftotext` output has no usable body-text layer — see EXTRACTS-I.md note); title/author page-1
text match via `pdftotext` for the other three. All four `pdftotext -q` dumps saved to
`arc-validation/txt/` (the 2016 one only as a `_NOTE.txt` explaining the extraction failure, since
there was no usable text to save).

### Held papers re-read fresh for this thread (all previously retrieved by earlier sessions;
identity confirmed by grepping each fresh `pdftotext -q` dump for the paper's own title/author
string; full quotes in EXTRACTS-I.md)

| Citation | File | Fresh dump |
|---|---|---|
| Stephenson, Weitsman & Zawodny 2019, JASA 145(3):1153–1155 | `chamber-problems/Stephenson_2019_JASA_recirculation-UAS-closed-anechoic-chambers.pdf` | `arc-validation/refetch-txt/Stephenson_2019.txt` |
| Weitsman, Stephenson & Zawodny 2020, JASA 148(3):1325–1336 | `chamber-problems/Weitsman_2020_JASA_recirculation-rotary-wing-closed-chambers.pdf` | `arc-validation/refetch-txt/Weitsman_2020.txt` |
| Jawahar, Hanson, Akhter & Azarpeyvand 2025, Sci. Rep. 15:2170 | `chamber-problems/Jawahar_2025_SciRep_porous-ground-propeller-ground-effect.pdf` | `arc-validation/refetch-txt/Jawahar_2025.txt` |
| Huang (Bristol student report, n.d.) | `anechoic-simulation/Huang_nd_Bristol-report_height-dependent-rotor-noise-thrust.pdf` | `arc-validation/refetch-txt/Huang_nd.txt` |
| Merino-Martínez et al. 2020, Appl. Acoust. 170:107504 | `chamber-problems/Merino-Martinez_2020_ApplAcoust_TU-Delft-anechoic-wind-tunnel.pdf` | `arc-validation/refetch-txt/MerinoMartinez_2020.txt` |
| Gallo et al. 2025, Acta Acustica 9:16 | `chamber-problems/Gallo_2025_ActaAcustica_aeroacoustic-propeller-test-bench.pdf` | `arc-validation/refetch-txt/Gallo_2025.txt` |
| Ma et al. 2022, Quiet Drones (HKUST) | `chamber-problems/Ma_2022_QuietDrones_multirotor-anechoic-vs-hemi-anechoic.pdf` | `arc-validation/refetch-txt/Ma_2022_QD.txt` |
| Ma, Zhou, Zhang & Zhong 2024, Acoustics Australia 52:313–322 | `chamber-problems/Ma_2024_AcoustAust_recirculation-free-flying-UAS-anechoic.pdf` | `arc-validation/refetch-txt/Ma_2024_AA.txt` |
| Cao et al. 2025, Forum Acusticum 2025 | `small-chamber/Cao-etal_2025_ForumAcusticum_sub-7kg-multirotor-anechoic-noise.pdf` | `arc-validation/refetch-txt/Cao_2025.txt` |
| Fasulo, Longobardo, De Gregorio & Barbarino 2025, Aerospace 12(7):647 | `chamber-problems/Fasulo_2025_Aerospace_rotor-noise-directivity-decay.pdf` | `arc-validation/refetch-txt/Fasulo_2025.txt` |
| Garg et al. 2019, MAPAN 34(3):357–369 | `chamber-problems/Garg_2019_MAPAN_microphone-free-field-calibration-uncertainty.pdf` | `arc-validation/refetch-txt/Garg_2019.txt` |
| Orrego González, Ealo Cuello & Pazos Ospina 2018, Scientia et Técnica 23(4):471–478 | `small-chamber/Orrego-Ealo-Pazos_2018_ScientiaTechnica_low-cost-small-anechoic-chamber.pdf` | `arc-validation/refetch-txt/Orrego_2018.txt` |
| Bikmukhametov et al. 2026, arXiv:2603.16556v1 | `anechoic-simulation/Bikmukhametov_2026_arXiv_ITMO-radiowave-chamber-acoustic-free-field.pdf` | `arc-validation/refetch-txt/Bikmukhametov_2026.txt` |
| Russo, Kraljević, Stella & Sikora 2018, Euronoise 2018:2225–2230 | `anechoic-simulation/Russo_2018_Euronoise_ISO3745-vs-ISO26101-Split-chamber.pdf` | `arc-validation/refetch-txt/Russo_2018.txt` |
| Nardari et al. 2019, AIAA 2019-2497 | `chamber-problems/Nardari_2019_AIAA_flow-confinement-UAV-rotor-noise.pdf` | `arc-validation/refetch-txt/Nardari_2019.txt` |
| Whelchel 2023, PhD thesis, Virginia Tech | `chamber-problems/Whelchel_2023_PhD-VT_sUAS-rotor-noise-outdoor-lab.pdf` | `arc-validation/refetch-txt/Whelchel_2023.txt` |
| Hochbaum, Herold, Kempen & Fiebig 2026, Quiet Drones (Delft) | `chamber-problems/Hochbaum_2026_QuietDrones_drone-directivity-anechoic-realistic-flight.pdf` | `arc-validation/refetch-txt/Hochbaum_2026.txt` |
| Palchikovskiy et al. 2016, AIP Conf. Proc. 1770:030116 | `chamber-problems/Palchikovskiy_2016_AIPConfProc_anechoic-chamber-tests-aeroacoustics.pdf` | `arc-validation/refetch-txt/Palchikovskiy_2016.txt` |
| ISO 5305:2024 (iTeh preview) | `anechoic-simulation/ISO-5305_2024_standard-preview_UAS-noise-measurement.pdf` | `arc-validation/refetch-txt/ISO5305_2024.txt` |
| Zawodny & Haskin 2017, AIAA (LSAWT) | `chamber-problems/Zawodny-Haskin_2017_AIAA_LSAWT-small-rotor-capabilities.pdf` | `arc-validation/refetch-txt/ZawodnyHaskin_2017.txt` |

24 substantive sources total (4 new + 20 held), covering NASA SHAC/SALT plus 14 other facilities
across Q2, plus the Q3/Q4 reporting-practice material — within the protocol's 6–12-per-thread
guidance is exceeded here deliberately because the thread's own question list names an unusually
large number of specific facilities and papers to check.

## NOT RETRIEVED

| Citation | DOI/URL | Reason |
|---|---|---|
| Vesa, J. H. *Design of an Anechoic Chamber for Aeroacoustic Testing and Analysis of Large UAS Propellers.* MS thesis, Mississippi State University, 2020. | `https://scholarsjunction.msstate.edu/td/1307/` (PDF at `https://scholarsjunction.msstate.edu/cgi/viewcontent.cgi?article=2306&context=td`) | bepress/Digital Commons `viewcontent.cgi` returns HTTP 403 ("403 Error" page) both with a plain browser User-Agent and with an added `Referer` header pointing at the article page — this is the protocol's documented bepress blocker. Landing page itself (`/td/1307/`) is reachable and gives the title/author/abstract. **Adam: please fetch the PDF from `https://scholarsjunction.msstate.edu/cgi/viewcontent.cgi?article=2306&context=td` through your institutional proxy and drop it in `papers/arc-validation/` as `Vesa_2020_MSState-thesis_[slug].pdf`** — this thesis is the only Mississippi-State source named in the thread's question list and no claim from it appears in EXTRACTS-I.md. |

## SEARCHED AND REJECTED

| Citation | Why rejected |
|---|---|
| Whelchel, J., Alexander, W. N. & Intaratep, N. *Propeller Noise in Confined Anechoic and Open Environments.* AIAA SciTech 2020 Forum, AIAA 2020-1252. doi:10.2514/6.2020-1252. | Found via web search while looking for the Vesa thesis (same MSU-adjacent search); turned out to be a Virginia Tech (not MSU) conference paper by the same first author as the already-held Whelchel 2023 PhD thesis. Confirmed closed access: Crossref gives the DOI and authors but Unpaywall reports `"is_oa": false, "oa_locations": []`; Semantic Scholar's `openAccessPdf.url` is empty. Not chased further because the held Whelchel 2023 PhD thesis (`chamber-problems/Whelchel_2023_PhD-VT_sUAS-rotor-noise-outdoor-lab.pdf`, already re-read for this thread, Section B of EXTRACTS-I.md does not currently cite it but the earlier chamber-problems extracts do) is the fuller, later publication by the same author covering the same VT anechoic-chamber-vs-outdoor comparison — chasing the earlier, shorter, paywalled conference version was judged not worth Adam's proxy time. If Adam wants it anyway: `https://doi.org/10.2514/6.2020-1252` (AIAA ARC, a known blocker). |
| Whelchel/VTechWorks item, handle `10919/142419`, *Methods for Improving Comparability of Propeller Acoustic Experiments Conducted at Different Facilities and Scales* | Surfaced in a VTechWorks search for the AIAA 2020-1252 paper (similar abstract: ground-board behaviour in an anechoic chamber + propeller noise outdoors). Different title from anything in the thread's question list; not pursued given time budget and the overlap with the held Whelchel 2023 thesis. Left for Adam to check if wanted: `https://vtechworks.lib.vt.edu/server/api/core/items/22eba163-dcf8-4390-88ef-0b8aa26b3bb7`. |
| Elsevier, *A small-scale active anechoic chamber*, Appl. Acoust. 2024, doi:10.1016/j.apacoust.2024.110130 | Semantic Scholar flags it CC-BY/hybrid OA, but hosted only at ScienceDirect (a documented blocker) and, on inspection of its title/scope, it is a general small-scale *active* (ANC-driven) anechoic-chamber paper, not specifically a UAV-propeller test facility — not central enough to this thread's Q2 to justify fighting the Elsevier host. Not fetched, not cited. |

## SEARCH QUERIES USED

- NTRS citations API (`https://ntrs.nasa.gov/api/citations/search`, both POST-JSON and GET
  `--data-urlencode` forms): `"acoustic characterization and prediction of representative
  small-scale rotary-wing unmanned aircraft system components"`; `"Zawodny Boyd Burley acoustic
  characterization rotary-wing unmanned aircraft"`; `"Zawodny Boyd rotor airframe interaction
  noise small unmanned aircraft"`; `"Pettingill Zawodny acoustic"`.
- NTRS citation-detail API (`https://ntrs.nasa.gov/api/citations/<id>`) for each hit, to read
  `downloads[].links` and `meetings[]` (venue/date) metadata.
- Crossref (`api.crossref.org/works?query.bibliographic=...`): `"Vesa anechoic chamber drone
  propeller Mississippi State"`; `"small anechoic chamber design UAV propeller noise testing"`.
- Crossref DOI lookup (`api.crossref.org/works/10.2514/6.2020-1252`).
- Semantic Scholar Graph API
  (`api.semanticscholar.org/graph/v1/paper/DOI:<doi>?fields=title,openAccessPdf,externalIds,abstract`)
  for `10.2514/6.2020-1252` and `10.1016/j.apacoust.2024.110130`.
- Unpaywall (`api.unpaywall.org/v2/<doi>?email=...`) for `10.2514/6.2020-1252`.
- VTechWorks discovery API (`vtechworks.lib.vt.edu/server/api/discover/search/objects?query=...`)
  for `"Propeller Noise in Confined Anechoic and Open Environments"`.
- Web search (WebSearch tool): `"Vesa 2020 Mississippi State thesis propeller noise anechoic
  chamber"` — resolved the ScholarsJunction handle (`td/1307`) and article id (2306) used for the
  bepress download attempt.
- Direct `curl` attempts on `scholarsjunction.msstate.edu/cgi/viewcontent.cgi?article=2306&context=td`
  with two different browser User-Agent strings (Linux Chrome, Windows Chrome) and with/without a
  `Referer` header — both returned HTTP 403.
