# Thread A retrieval log — single-reflection interference

## RETRIEVED

Held papers re-read fresh this session (all identity-confirmed from their own front matter; all
re-extracted with plain `pdftotext -q` into `papers/arc-validation/refetch-txt/`):

| # | Citation | File |
|---|---|---|
| 1 | Rasmussen, P. & Winberg, L. (2022). *Accurate measurement of Drone Noise on the ground.* Quiet Drones 2nd e-Symposium. | `papers/chamber-problems/Rasmussen-Winberg_2022_QuietDrones_drone-noise-on-the-ground.pdf` |
| 2 | Friot, E. & Gintz, A. (2009). *Estimation and global control of noise reflections.* arXiv:0911.4639. | `papers/chamber-problems/Friot-Gintz_2009_arXiv_estimation-global-control-noise-reflections.pdf` |
| 3 | Cunefare, K. A. et al. (2003). *Anechoic chamber qualification: Traverse method, inverse square law analysis method, and nature of test signal.* JASA 113(2), 881–892. doi:10.1121/1.1527595 | `papers/anechoic-simulation/Cunefare_2003_JASA_chamber-qualification-traverse-fit-signal.pdf` |
| 4 | Nash, A. (2019). *Qualification of an anechoic chamber.* Proc. 23rd ICA, Aachen, pp. 1343–1349. | `papers/anechoic-simulation/Nash_2019_ICA_qualification-of-an-anechoic-chamber.pdf` |
| 5 | Winker, D. & Stahnke, B. (2016). *The influences of changes in international standards on performance qualification and design of anechoic and hemi-anechoic chambers.* Inter-Noise 2016. | `papers/chamber-problems/Winker-Stahnke_2016_InterNoise_ISO3745-ISO26101-chamber-qualification.pdf` |
| 6 | Simmons, D., Jobling, B. & Payne, R. (2004). *Acoustic parameters and uncertainties associated with determining sound power level in hemi-anechoic rooms.* NPL Report DQL-AC 007. | `papers/chamber-problems/Simmons-Jobling-Payne_2004_NPL-DQL-AC007_hemi-anechoic-sound-power-uncertainties.pdf` |
| 7 | Payne, R. C. & Simmons, D. J. (1996). NPL Report CIRA(EXT) 009, environmental correction K2. | `papers/anechoic-simulation/Payne-Simmons_1996_NPL-CIRA009_environmental-correction-K2.pdf` |
| 8 | ISO 26101-1:2021, *Qualification of free-field environments* (iTeh preview). | `papers/anechoic-simulation/ISO-26101-1_2021_standard-preview_free-field-qualification.pdf` |
| 9 | ISO 26101-2:2024, *Determination of the environmental correction* (iTeh preview). | `papers/reflection-localization/ISO-26101-2_2024_standard-preview_environmental-correction.pdf` |

New PDFs retrieved and saved this session, into `papers/arc-validation/`:

| # | Citation | DOI / route that worked | File |
|---|---|---|---|
| 10 | Pao, S. P., Wenzel, A. R. & Oncley, P. B. (1978). *Prediction of Ground Effects on Aircraft Noise.* **NASA Technical Paper 1104** (report no. L-11833). | NTRS citation `19780009880`; PDF at `https://ntrs.nasa.gov/api/citations/19780009880/downloads/19780009880.pdf` | `Pao-Wenzel-Oncley_1978_NASA-TP1104_ground-effects-aircraft-noise.pdf` |
| 11 | Lamancusa, J. S. (2009). "Outdoor Sound Propagation," Ch. 10 of Penn State "Noise Control" course notes. | Hosted openly at `https://www.angelofarina.it/Public/Acoustics-Course/Penn-State-Course/10_osp.pdf` | `Lamancusa_2009_PennState-CourseNotes_outdoor-sound-propagation.pdf` |
| 12 | ISO 3745:2012, *Acoustics — Determination of sound power levels ... — Precision methods for anechoic rooms and hemi-anechoic rooms* (iTeh preview, 15 pp. of the full standard). | `https://cdn.standards.iteh.ai/samples/45362/5080c9a729fb42b08f433df7ed8129f6/ISO-3745-2012.pdf` | `ISO-3745_2012_standard-preview_precision-methods-anechoic-rooms.pdf` |
| 13 | Randall, R. B. (2013). *A History of Cepstrum Analysis and its Application to Mechanical Problems.* Surveillance 7 conference. | Pre-existing file in `papers/arc-validation/` from an unrelated earlier session, **mis-named** as if it were Randall's 2017 MSSP paper; identity re-confirmed from its own PDF metadata this session and the file renamed accordingly. Originally hosted at `surveillance7.sciencesconf.org/.../01_a_history_of_cepstrum_analysis....pdf` (per its earlier retrieval, not re-fetched). | `Randall_2013_Surveillance7_history-of-cepstrum-analysis.pdf` |

**Identity correction on retrieval**: the thread brief named the ground-effects source as "NASA
RP-1004"; the document itself, confirmed from its own title page and NASA NTRS's own citation
metadata, is **NASA Technical Paper 1104 (NASA-TP-1104)** — same paper (Pao, Wenzel & Oncley,
1978, "Prediction of Ground Effects on Aircraft Noise"), the report-series letters and the last
two digits of the number were transposed in the brief.

## NOT RETRIEVED

| Citation | DOI | Best URL for a proxy | Reason not retrieved |
|---|---|---|---|
| Embleton, T. F. W. (1996). *Tutorial on sound propagation outdoors.* J. Acoust. Soc. Am. 100(1), 31–48. | 10.1121/1.415879 | `https://pubs.aip.org/asa/jasa/article-pdf/100/1/31/11401662/31_1_online.pdf` | AIP/JASA — known blocker, not attempted. Substituted with an open course-note (item 11) that derives the same ground-effect formula family and cites this paper. |
| Piercy, J. E.; Embleton, T. F. W.; Sutherland, L. C. (1977). *Review of noise propagation in the atmosphere.* J. Acoust. Soc. Am. 61(6), 1403–1418. | — | `pubs.aip.org` (JASA) | AIP/JASA — known blocker. Found as the primary reference (ref. 3) behind both Lamancusa's (2009) course notes and Pao, Wenzel & Oncley's (1978) ground-effect equation; not independently pursued. |
| Miles, J. H.; Stevens, G. H.; Leininger, G. G. (1977). *Application of Cepstral Techniques to Ground-Reflection Effects in Measured Acoustic Spectra.* J. Acoust. Soc. Am. 61(1), 35–38. | — | `pubs.aip.org` (JASA) | AIP/JASA — known blocker. This is the original paper behind the cepstral-technique description quoted (secondhand) from Pao, Wenzel & Oncley (1978, item 10, p. 15); its citation was recovered from that source's own reference list. |
| Miles, J. H. (1975). *Method of Representation of Acoustic Spectra and Reflection Corrections Applied to Externally Blown Flap Noise.* NASA TM X-3179. | — | NTRS (not searched this session) | Not pursued — found only as a reference inside Pao et al. (1978); flagged for a future pass if the iterative-correction method needs primary-source detail. |
| Miles, J. H. (1975). *Analysis of Ground Reflection of Jet Noise Obtained With Various Microphone Arrays Over an Asphalt Surface.* NASA TM X-71696. | — | NTRS (not searched this session) | Same as above. |
| Thomas, P. (1972). *Acoustic Interference by Reflection Application to the Sound Pressure Spectrum of Jets.* NASA TT F-14,185. | — | NTRS (not searched this session) | Found only as a reference inside Pao et al. (1978); not pursued. |
| Stroud, R. (2010). *Quasi-Anechoic Loudspeaker Measurement Using Notch Equalization for Impulse Shortening.* AES Convention 129, Paper 8170. | — | `https://aes.org/publications/elibrary-page/?id=15593` | AES e-library — known blocker. Already flagged abstract-only in the held corpus (`chamber-problems/EXTRACTS-downloaded.md`); no new attempt made this session per the "known blockers, don't waste time" rule. No claim is made from it in EXTRACTS-A.md. |
| Bogert, B. P., Healy, M. J. R. & Tukey, J. W. (1963). *The Quefrency Alanysis of Time Series for Echoes: Cepstrum, Pseudo-Autocovariance, Cross-Cepstrum, and Saphe Cracking.* In M. Rosenblatt (ed.), Proc. Symp. on Time Series Analysis, pp. 209–243, Wiley, New York. | none (pre-DOI book chapter) | see below | Dispatched to a subagent; not retrieved. Routes tried and failed: (1) general web search — every hit is a citation to the paper, never a hosted copy; (2) `archive.org/advancedsearch.php` for the Rosenblatt 1963 Wiley symposium volume — 0 results, not digitized; (3) the paper is reprinted in *The Collected Works of John W. Tukey, Vol. I: Time Series 1949–1964* (Brillinger & Wadsworth, eds., 1984), pp. 455–493, which **is** on archive.org (`archive.org/details/collectedworksof0001tuke`) but is `access-restricted-item: true` — a direct download attempt returned **HTTP 401**; Internet Archive's controlled-digital-lending reader does not yield an exportable PDF even with a loan; (4) HathiTrust catalog search — **HTTP 403** (bot-blocked); (5) Internet Archive Scholar (`scholar.archive.org`) — empty JS shell via curl, no result; (6) a Bell Telephone System technical-monograph reprint was checked on archive.org — only 1920s-era monographs are digitized there, nothing from 1963. **Not attempted** (per this session's instruction to avoid the site): a ResearchGate attachment URL surfaced repeatedly in search results under a "does anyone have this paper" request thread — the single most promising concrete lead, left for Adam or a library proxy. A **full, precise citation** (confirmed independently from Randall 2013's own reference list, item 13) is given above for whoever pursues this. |
| Randall, R. B. (2017). *A history of cepstrum analysis and its application to mechanical problems.* Mech. Syst. Signal Process. 97, 3–19. | 10.1016/j.ymssp.2016.12.026 | `https://www.sciencedirect.com/science/article/abs/pii/S0888327016305556` | ScienceDirect/Elsevier — known blocker; confirmed as the sole primary host via Crossref. Also checked and failed: UNSW institutional-repository pages for Randall (this title did not appear on the pages fetched); UNSWorks DSpace REST API and sitemap — **HTTP 403** (WAF-blocked); a UNSWorks DOI that surfaced in search turned out, on inspection of its own landing-page title, to be a **different** Randall paper ("Cepstral removal of resonance effects to improve the use of traditional gear diagnostic indicators at different speeds") and was correctly discarded rather than mis-cited; Semantic Scholar API — `openAccessPdf` present but empty with `status: CLOSED`; OpenAlex — `oa_status: closed`, `best_oa_location: null` (this also rules out Unpaywall, which OpenAlex indexes); CORE.ac.uk — **HTTP 403**. **Not attempted**: a ResearchGate "Request PDF" page for the same title. Randall's own earlier, differently-published 2013 conference version of this same survey **was** retrieved instead (item 13 above) but does not cover the room-acoustics question this thread needs — see EXTRACTS-A.md, item 13, for exactly what it does and does not say. |
| ISO 3745:2012, Annex A (the tolerance table itself) and Annex B (K2/two-surface qualification procedures for specific sound-power test rooms). | — | `https://www.iso.org/standard/45362.html` (full purchase) | Only the free iTeh preview (15 pp.) was retrieved (item 12); it stops at clause 5.1, before Annex A, which its own table of contents confirms starts at the standard's internal page 29. The tolerance table itself was instead confirmed **verbatim, and identically, from three independent papers that quote it directly from the standard** — see EXTRACTS-A.md items 3, 5, 6. |
| ISO 26101-1:2021, Annex A (default traverse layouts, the actual qualification-criteria table). | — | iTeh full purchase | Same situation as above — the held preview (item 8) stops at clause 5.1.5.1.2, before Annex A. |
| ISO 26101-2:2024, Annex A (stated uncertainty of the environmental correction, referenced by its own §4.1: "Information on the uncertainty of the environmental correction can be found in Annex A"). | — | iTeh full purchase | Same situation — the held preview (item 9) stops at §5.1, before Annex A. |

## SEARCHED AND REJECTED

No candidate source was rejected outright this session as off-topic once located — every search
either produced a usable retrieval or terminated at a known-blocked host (logged above under NOT
RETRIEVED). Two negative results are worth recording so a future thread does not repeat the search:
- A UNSWorks DOI record surfacing under "Randall cepstrum" searches (`10.26190/unsworks/26605`) is
  **not** the 2017 MSSP history paper — its own landing page title is "Cepstral removal of
  resonance effects to improve the use of traditional gear diagnostic indicators at different
  speeds." Confirmed and discarded, not used anywhere in EXTRACTS-A.md.
- No source retrieved or searched this session uses the term "two-distance method" for direct/
  reflected field separation (Q5's last sub-question) — this is not a rejection of a specific paper,
  just a note that the search did not surface one under that name.

## Search queries used

- WebSearch: `NASA RP-1004 Pao Wenzel Oncley "Prediction of ground effects on aircraft noise"`
- WebSearch: `Embleton 1996 "Tutorial on sound propagation outdoors" JASA pdf`
- WebSearch: `iso 3745:2012 standards.iteh.ai preview pdf acoustics anechoic hemi-anechoic`
- NTRS: `https://ntrs.nasa.gov/api/citations/19780009880` (citation JSON, confirmed report number
  NASA-TP-1104 and the downloads list) then
  `https://ntrs.nasa.gov/api/citations/19780009880/downloads/19780009880.pdf`
- Direct `curl` fetch of the iTeh sample URL for ISO 3745:2012 surfaced directly in the WebSearch
  result list (`cdn.standards.iteh.ai/samples/45362/...`), no separate search needed.
- Subagent (cepstrum-history retrieval) queries, per its own report: general web search variants of
  "quefrency alanysis of time series for echoes pdf", "Bogert Healy Tukey 1963 cepstrum pdf",
  "saphe cracking filetype:pdf"; `archive.org/advancedsearch.php` for the Rosenblatt 1963 symposium
  volume; UNSW `research.unsw.edu.au` and `unsworks.unsw.edu.au` browsing/API calls; Semantic
  Scholar, Crossref, OpenAlex and CORE.ac.uk API lookups for the Randall 2017 DOI
  (10.1016/j.ymssp.2016.12.026).
