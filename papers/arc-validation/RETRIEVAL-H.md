# Thread H — retrieval record

## RETRIEVED

### Held papers re-read fresh (identity re-confirmed from each PDF's own front matter; fresh `pdftotext -q` dumps in `papers/arc-validation/refetch-txt/`)

| Citation | DOI / ref | File |
|---|---|---|
| Rasmussen, P. & Winberg, L. 2022. "Accurate measurement of Drone Noise on the ground." Quiet Drones 2nd e-Symposium | — | `papers/chamber-problems/Rasmussen-Winberg_2022_QuietDrones_drone-noise-on-the-ground.pdf` |
| Jawahar, H. K., Hanson, L., Akhter, M. Z. & Azarpeyvand, M. 2025. "Porous ground treatments for propeller noise reduction in ground effect." Sci. Rep. 15, 2170 | 10.1038/s41598-024-82876-9 | `papers/chamber-problems/Jawahar_2025_SciRep_porous-ground-propeller-ground-effect.pdf` |
| Alkmim, M. et al. 2022. "Drone noise directivity and psychoacoustic evaluation using a hemispherical microphone array." J. Acoust. Soc. Am. 152(5), 2735–2745 | 10.1121/10.0014957 | `papers/chamber-problems/Alkmim_2022_JASA_drone-directivity-hemispherical-array.pdf` |
| Ma, Z., Wu, H., Jiang, H., Zhong, S. & Zhang, X. 2022. "Acoustic measurement of multi-rotor drones in anechoic and hemianechoic chambers." Quiet Drones 2nd e-Symposium | — | `papers/chamber-problems/Ma_2022_QuietDrones_multirotor-anechoic-vs-hemi-anechoic.pdf` |
| Fasulo, G., Longobardo, G., De Gregorio, F. & Barbarino, M. 2025. "Experimental Acoustic Investigation of Rotor Noise Directivity and Decay in Multiple Configurations." Aerospace 12(7), 647 | 10.3390/aerospace12070647 | `papers/chamber-problems/Fasulo_2025_Aerospace_rotor-noise-directivity-decay.pdf` |
| Whelchel, J. 2023. "Measurement and Prediction of Rotor Noise Sources for sUAS in Outdoor and Laboratory Environments." PhD dissertation, Virginia Tech | — | `papers/chamber-problems/Whelchel_2023_PhD-VT_sUAS-rotor-noise-outdoor-lab.pdf` |
| Zawodny, N. S. & Haskin, H. H. 2017. "Small Propeller and Rotor Testing Capabilities of the NASA Langley Low Speed Aeroacoustic Wind Tunnel." AIAA Aeroacoustics Conf. | — | `papers/chamber-problems/Zawodny-Haskin_2017_AIAA_LSAWT-small-rotor-capabilities.pdf` |
| Winker, D. & Stahnke, B. 2016. "The influences of changes in international standards on performance qualification and design of anechoic and hemi-anechoic chambers." Inter-Noise 2016 | — | `papers/chamber-problems/Winker-Stahnke_2016_InterNoise_ISO3745-ISO26101-chamber-qualification.pdf` |
| Weitsman, D., Stephenson, J. H. & Zawodny, N. S. 2020. "Effects of flow recirculation on acoustic and dynamic measurements of rotary-wing systems operating in closed anechoic chambers." J. Acoust. Soc. Am. 148(3), 1325–1336 | — | `papers/chamber-problems/Weitsman_2020_JASA_recirculation-rotary-wing-closed-chambers.pdf` |
| Burnett, E. D. & Nedzelnitsky, V. 1987. "Free-Field Reciprocity Calibration of Microphones." J. Res. Natl. Bur. Stand. 92(2), 129–151 | — | `papers/small-chamber/Burnett-Nedzelnitsky_1987_JResNBS_free-field-reciprocity-calibration-chamber-deviations.pdf` |
| Rajmane, A. & Baumann, W. 2016. "Detection of Reflecting Objects in Anechoic Chambers." DAGA 2016 Aachen, pp. 331–333 | — | `papers/small-chamber/Rajmane-Baumann_2016_DAGA_detection-reflecting-objects-anechoic-chambers.pdf` |
| ISO 26101-1:2021. *Acoustics — Test methods for the qualification of the acoustic environment — Part 1* (iTeh preview, Foreword–5.1.5.1.2) | — | `papers/anechoic-simulation/ISO-26101-1_2021_standard-preview_free-field-qualification.pdf` |
| ISO 5305:2024. *Acoustics — Noise measurements for UAS* (iTeh preview, Foreword–7.3.1) | — | `papers/anechoic-simulation/ISO-5305_2024_standard-preview_UAS-noise-measurement.pdf` |

### New sources retrieved this session (saved into `papers/arc-validation/`)

| Citation | DOI / ref | Route that worked | File |
|---|---|---|---|
| Zawodny, N. S., Boyd, D. D., Jr. & Burley, C. L. 2016. "Acoustic Characterization and Prediction of Representative, Small-Scale Rotary-Wing Unmanned Aircraft System Components." AHS 72nd Annual Forum (2016) | NASA NTRS 20160009054 | `curl -sL -A "Mozilla/5.0..." https://ntrs.nasa.gov/api/citations/20160009054/downloads/20160009054.pdf` (found via `https://ntrs.nasa.gov/api/citations/search?q=Zawodny%20Boyd%20Burley%20rotor%20noise`) | `papers/arc-validation/Zawodny-Boyd-Burley_2016_AHSForum72_SALT-facility-small-rotor-characterization.pdf` — PDF downloaded and identity-confirmed (this session independently fetched a byte-identical copy of the same NTRS document, saved under a different filename, `Zawodny-Boyd-Burley_2016_AHS_UAS-rotor-acoustic-characterization.pdf`; that copy is no longer on disk — apparently superseded in the shared `papers/arc-validation/` folder by a sibling thread's identically-sourced copy under the name above, confirmed by `pdfinfo` reporting the same internal document title `lf99-22587_final-Zawodny_ahsforum72_submission2.pdf` on the surviving file). **`pdftotext` fails on this PDF** (body text is present only as unrecoverable font-outline glyphs — verified independently by this thread and by a sibling thread's own note file, `txt/Zawodny-Boyd-Burley_2016_AHSForum72_NOTE.txt`, which hit the same wall and recorded the same workaround). Quotes used in EXTRACTS-H.md were obtained instead by **visually reading the rendered pages** (Read tool, pages 1–9 of 15) — a legitimate direct reading of the document, not a workaround that lowers its evidence tier. |
| Brüel & Kjær. *Microphone Handbook, Volume 1: Theory.* BE 1447–12, March 2019 | — [vendor] | `curl -sL -A "Mozilla/5.0..." https://www.bksv.com/media/doc/be1447.pdf` (URL found via WebSearch) | `papers/arc-validation/BruelKjaer_2019_vendor_microphone-handbook-vol1-theory.pdf` (155 pp, full text; `txt/BruelKjaer_2019_vendor_microphone-handbook-vol1-theory.txt`) |
| IEC 61672-1:2013. *Electroacoustics — Sound level meters — Part 1: Specifications* (iTeh sample preview) | — | `curl -sL https://cdn.standards.iteh.ai/samples/17900/df52d949fc904f329404e965b6268258/IEC-61672-1-2013.pdf` (direct iTeh sample-CDN URL found via WebSearch) | saved to `/tmp/iec61672-1.pdf` (not copied into `papers/arc-validation/` — see note below) |
| miniDSP Support Portal. "Which direction should I point the UMIK-1?" [vendor] | — | `curl -sL -A "Mozilla/5.0..." https://support.minidsp.com/support/solutions/articles/47000681633-...` | fetched and read directly (HTML stripped to text with a short Python snippet); not a PDF, no local copy saved per protocol's PDF-only save instruction — page content quoted in EXTRACTS-H.md is the full verbatim text of the relevant paragraph |
| miniDSP. *UMIK-2 User Manual.* [vendor] | — | already present in the shared `papers/arc-validation/` folder (fetched by a sibling thread this campaign); re-read fresh and page-verified for this thread with `pdftotext -f N -l N` | `papers/arc-validation/miniDSP_nd_vendor_UMIK-2-user-manual.pdf` (29 pp) — this is the source of Q4's best answer (0°/90° curves "differ only above a few kHz," p. 15) |
| miniDSP. *UMIK-2 Product Brief.* [vendor] | — | already present in the shared folder (sibling thread) | `papers/arc-validation/miniDSP_nd_vendor_UMIK-2-product-brief.pdf` (2 pp) — capsule spec cross-check only |

**Note on the IEC 61672-1 preview**: this is only a 15-page iTeh *sample* (front matter, scope,
normative references, and clause 3 "Terms and definitions" — confirmed by reading every page). It
does **not** reach the standard's actual electroacoustic performance-requirement clauses/annexes
(where frontal-free-field vs. random-incidence tolerance tables would live), so it cannot answer
"the frequency where free-field and diffuse-field responses diverge" for a Class 1 sound level
meter. It is cited in EXTRACTS-H.md only for confirming that the standard formally distinguishes
free-field from diffuse-field/random-incidence response and delegates the diffuse-field calibration
method to a sister standard ("IEC 61183, Electroacoustics – Random-incidence and diffuse-field
calibration of sound level meters") and free-field corrections to another ("IEC 62585, ... Methods
to determine corrections to obtain the free-field response of a sound level meter") — both normative
references listed on the preview's own page 2 (of the numbered clauses). Because it does not answer
the thread's actual numeric question, it was not copied into `papers/arc-validation/` under a
permanent filename; the fetched copy remains at `/tmp/iec61672-1.pdf` for this session only. **The
full standard (with the performance-requirement clauses) would need to come from Adam's
institutional proxy — see NOT RETRIEVED below.**

---

## NOT RETRIEVED

| Citation | DOI | Best URL for proxy | Reason |
|---|---|---|---|
| Hanson, L., Kamliya Jawahar, H., Vemuri, S. H. S. & Azarpeyvand, M. 2023. "Experimental investigation of propeller noise in ground effect." J. Sound Vib. 559, 117751. **(Note: the thread brief's author list "Hanson, Jawahar, Akhter & Azarpeyvand" is not correct for this paper — Crossref confirms the fourth author is Vemuri, not Akhter; Akhter is a co-author on the *different*, already-held Jawahar 2025 Sci. Rep. paper.)** | 10.1016/j.jsv.2023.117751 | `https://doi.org/10.1016/j.jsv.2023.117751` (hybrid OA, CC-BY licence — confirmed via Semantic Scholar's `openAccessPdf` field, but the licence does not help against the bot-block) | ScienceDirect returns HTTP 403 to a direct fetch (`curl` with a full browser User-Agent) — a known blocker per PROTOCOL.md. Three alternative routes named in the thread brief were all tried and exhausted: (1) University of Bristol repository (`research-information.bris.ac.uk`) — the Pure record page loads (`.../en/publications/experimental-investigation-of-propeller-noise-in-ground-effect/`, found via the CORE API's `sourceFulltextUrls`) but its own "Access to Document" section lists only the same ScienceDirect DOI link, licensed CC BY — **no independently hosted PDF file**; (2) Europe PMC — `DOI:10.1016/j.jsv.2023.117751` search returns `hitCount: 0`; (3) CORE (`api.core.ac.uk`) — indexes the metadata/abstract (via Crossref + "Explore Bristol Research") but lists no `downloadUrl` or `fullTextIdentifier` for any of its three duplicate output records. No claim is made from this paper anywhere in EXTRACTS-H.md; the abstract seen via CORE's metadata was read but is **not quoted or used as evidence** for the thread's answers, per protocol rule 1. |
| IEC 61672-1:2013 (full standard, beyond the 15-page iTeh sample) | — | `https://webstore.iec.ch/en/publication/5708` or the ANSI mirror `https://webstore.ansi.org/standards/iec/iec61672ed2002` (2002 first edition) | ANSI/IEC webstores are a known blocker (paywalled, no preview beyond what iTeh already exposed). Needed only for the specific frontal-free-field-vs-random-incidence tolerance table/annex, which the retrieved 15-page preview does not reach. |

---

## SEARCHED AND REJECTED

- Zawodny, N.S.; Boyd, D.D. "Investigation of rotor–airframe interaction noise associated with
  small-scale rotary-wing unmanned aircraft systems." J. Am. Helicopter Soc. 2020, 65, 1–17. Found
  while checking Fasulo 2025's own reference list (ref. list entry, p. 26 of the PDF) while looking
  for "Zawodny, Boyd & Burley 2016" — this is a **different**, two-author, 2020 JAHS paper by an
  overlapping pair of authors, not the three-author 2016 AHS Forum paper the thread brief names.
  Not pursued further once the correct 2016 NTRS record (20160009054) was found directly.
- Hanson, Baskaran, Zang & Azarpeyvand — "Acoustic shielding and scattering effects of a propeller
  mounted above a flat plate" (Fasulo 2025's ref. [9], the actual source of the "8.5 dB shielding"
  number Fasulo cites) — not independently retrieved this pass; only seen as a reference-list
  citation inside Fasulo 2025, not as its own PDF. Left for a future pass if the 8.5 dB figure needs
  to be traced past Fasulo's citation of it.
- Singh, Garg & Narayanan 2020 and Garg et al. 2019 (both already flagged "abstract only" in
  `chamber-problems/EXTRACTS-downloaded.md`) — checked, neither addresses microphone
  mount/clamp/support scattering specifically (they address chamber cut-off frequency and
  free-field calibration uncertainty respectively); not used for this thread.
- A dedicated OA paper "quantifying scattering from a microphone stand/clamp of ~5–10 cm at 2–4
  kHz" (asked for explicitly in Q3) was searched for but not found as a standalone paper; the
  thread's answer to that specific ask is instead assembled from Rajmane & Baumann 2016's
  general object-size-vs-frequency rule (which covers the 5–10 cm / 2–4 kHz range as a special
  case: predicted onset 3.4–6.9 kHz for a 5–10 cm square) plus Weitsman 2020's and Winker &
  Stahnke 2016's specific >2 kHz / >10 kHz mount-reflection observations — see EXTRACTS-H.md Q3.

---

## Search queries used

- NASA NTRS: `https://ntrs.nasa.gov/api/citations/search?q=Zawodny%20Boyd%20Burley%20rotor%20noise&page.size=10`
- `https://ntrs.nasa.gov/api/citations/20160009054` (citation JSON, incl. `downloads` list)
- Crossref: `https://api.crossref.org/works?query.bibliographic=propeller+noise+ground+effect+Hanson+Jawahar+Journal+of+Sound+and+Vibration+2023&rows=5`
- Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.jsv.2023.117751?fields=title,openAccessPdf,externalIds,year`
- Europe PMC: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1016/j.jsv.2023.117751&format=json`
- CORE: `https://api.core.ac.uk/v3/search/works/?q=title:%22Experimental%20investigation%20of%20propeller%20noise%20in%20ground%20effect%22` then `https://api.core.ac.uk/v3/outputs/<id>` for each of the 3 output records
- Direct: `https://doi.org/10.1016/j.jsv.2023.117751` → resolves to `sciencedirect.com/science/article/pii/S0022460X23002006` (403)
- Direct: `https://research-information.bris.ac.uk/...` search endpoint (403) vs. the item page via
  the CORE-supplied handle URL `https://hdl.handle.net/1983/b13fee5d-4b41-4ea8-8292-bb85981c2c6d`
  (200 — metadata only)
- WebSearch: `Brüel Kjær "Microphone Handbook" volume 1 theory pdf bksv.com filetype:pdf`
- WebSearch: `miniDSP UMIK-2 0 degree 90 degree calibration file difference on-axis`
- WebSearch: `IEC 61672-1 preview iteh standards free-field diffuse-field response sound level meter`
- WebFetch / curl on the miniDSP community-forum threads and audiophilestyle.com thread the last
  search surfaced — all returned HTTP 403 to both tools; not used as sources.
