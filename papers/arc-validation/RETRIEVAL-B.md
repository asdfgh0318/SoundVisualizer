# Retrieval log — Thread B (reflection vs. rotor/inflow asymmetry, ±36° BPF-band pattern)

Session 2026-09-08. All PDFs verified with `file <pdf>` (real "PDF document") and `pdfinfo`
before use; new PDFs also had page 1 read to confirm title/authors/report number against the
citation metadata before trusting them.

## RETRIEVED

### New sources (NASA NTRS)

| Citation | Report # / DOI | Route | File |
|---|---|---|---|
| Hanson, D. B. (1977). *Study of Noise and Inflow Distortion Sources in the NASA QF-1B Fan Using Measured Blade and Vane Pressures.* Hamilton Standard, for NASA Lewis Research Center. | NASA CR-2899 | `ntrs.nasa.gov/api/citations/search?q=Hanson%20spectrum%20rotor%20noise%20atmospheric%20turbulence` → id 19770026169 → `ntrs.nasa.gov/api/citations/19770026169/downloads/19770026169.pdf` | `Hanson_1977_NASA-CR-2899_QF-1B-inflow-distortion-rig-interference.pdf` |
| Hodder, B. K. (1977). *Further Studies of Static to Flight Effects on Fan Tone Noise Using Inlet Distortion Control for Source Identification.* Ames Research Center / U.S. Army AMRDL. | NASA TM X-73183 | `ntrs.nasa.gov/api/citations/search?q=turbulence%20control%20structure%20fan%20noise` → id 19770007084 → `.../downloads/19770007084.pdf` | `Hodder_1977_NASA-TMX-73183_static-to-flight-fan-tone-noise.pdf` |
| Woodward, R. P.; Wazyniak, J. A.; Shaw, L. M.; MacKinnon, M. J. (1977/78). *Effectiveness of an Inlet Flow Turbulence Control Device to Simulate Flight Fan Noise in an Anechoic Chamber.* NASA Lewis. Presented at the 94th ASA Meeting, Miami, Dec 1977. | NASA TM-73855 | `ntrs.nasa.gov/api/citations/search?q=Woodward%20inflow%20control%20device%20fan%20noise` → id 19780005913 → `.../downloads/19780005913.pdf` | `Woodward-etal_1978_NASA-TM-73855_inlet-turbulence-control-device-anechoic-chamber.pdf` |
| Woodward, R. P.; Glaser, F. W. (1980). *Effect of Inflow Control on Inlet Noise of a Cut-on Fan.* NASA Lewis. | NASA TM-81487 | same search → id 19800014609 → `.../downloads/19800014609.pdf` | `Woodward-Glaser_1980_NASA-TM-81487_inflow-control-cuton-fan.pdf` |
| Homyak, L.; McArdle, J. G.; Heidelberg, L. J. (1983). *A Compact Inflow Control Device for Simulating Flight Fan Noise.* NASA Lewis. AIAA-83-0680, 8th AIAA Aeroacoustics Conf. | NASA TM-83349 | `ntrs.nasa.gov/api/citations/search?q=inflow%20control%20device%20fan%20noise` → id 19830018372 → `.../downloads/19830018372.pdf` | `Homyak-etal_1983_NASA-TM-83349_compact-inflow-control-device.pdf` |

### Additional source found already retrieved in the shared pool

| Citation | Route | File |
|---|---|---|
| Zawodny, N. S.; Boyd, D. D. Jr. (2017). *Investigation of Rotor-Airframe Interaction Noise Associated with Small-Scale Rotary-Wing Unmanned Aircraft Systems.* 73rd Annual Forum of the American Helicopter Society (Vertical Flight Society). | Already present in `papers/arc-validation/` when this thread began working — evidently fetched by a concurrent thread on the same campaign, not by this thread. Read fresh this session (`pdftotext -q` → `txt/Zawodny-Boyd_2017_AHSForum73_rotor-airframe-interaction-SALT.txt`), identity-confirmed from its own front matter, every quoted passage re-verified against the source PDF with `pdftotext -f N -l N`. | `Zawodny-Boyd_2017_AHSForum73_rotor-airframe-interaction-SALT.pdf` |

It is the strongest single source found for Q2 (a rotor test with a genuine elevation-*and*-
azimuth microphone sub-array, purpose-built to test rotor–nearby-structure interaction) — see
EXTRACTS-B.md. It is not previously extracted as its own paper anywhere in `papers/*/EXTRACTS*.md`
or `MATRIX-3W.md` (Whelchel 2023's held extract in `EXTRACTS-local.md` cites "Zawodny & Boyd"
only in passing, as the source of a phase-averaging *method* Whelchel reused — not an extraction
of this paper's own findings), so there is nothing to reconcile it against.

While reading this file, a handful of other PDFs were also found already sitting in the shared
`papers/arc-validation/` pool (evidently other threads' retrievals) with titles that looked
adjacent to Q1/Q2 — `Zawodny-Boyd-Burley_2016_AHSForum72_SALT-facility-small-rotor-characterization.pdf`,
`Pettingill-Zawodny_2026_NASA-TM-20250003316_tip-speed-tripping-SHAC.pdf`,
`Schatzman-Malpica_2019_VFS-Forum_tiltrotor-test-rig-shaft-angle-sweep.pdf`. Title/abstract
pages were skimmed (facility-capability, tripping/boundary-layer, and large-scale tiltrotor BVI
validation, respectively — none obviously about azimuthal directivity or reflection-vs-source
discrimination) but they were not read in full or quoted, both because they read as less central
to this thread's specific questions than what is already retrieved, and to respect that they are
very likely already in use by whichever sibling thread fetched them. **Not claimed as read; not
quoted; flagged here only so Adam/another thread knows they exist in the shared pool.**

All five NASA reports were fetched with
`curl -sL -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36" -o <file> https://ntrs.nasa.gov/api/citations/<id>/downloads/<id>.pdf`
per PROTOCOL.md route 4; all confirmed "PDF document" by `file`, page counts sane by `pdfinfo`,
and identity confirmed by reading page 1 (title/authors/report number visible despite OCR noise
on the 1977–1980 microfiche scans). Two report numbers initially guessed from the search-result
title were corrected against the citation JSON's `otherReportNumbers` field before final
filenames were fixed: Woodward et al. is **TM-73855** (not TM-73586 as first guessed from a
stale note), Woodward & Glaser is **TM-81487** (not TM-81507).

### Held papers, re-read fresh (all already in `papers/chamber-problems/`)

| Citation | DOI | Fresh dump |
|---|---|---|
| Stephenson, Weitsman & Zawodny (2019). JASA 145(3), 1153–1155. | 10.1121/1.5092213 | `refetch-txt/Stephenson_2019.txt` |
| Weitsman, Stephenson & Zawodny (2020). JASA 148(3), 1325–1336. | 10.1121/10.0001901 | `refetch-txt/Weitsman_2020.txt` |
| Nardari, Casalino, Polidoro, Coralic, Brodie & Lew (2019). AIAA 2019-2497. | 10.2514/6.2019-2497 | `refetch-txt/Nardari_2019.txt` |
| Ma, Zhou, Zhang & Zhong (2024). Acoustics Australia 52, 313–322. | 10.1007/s40857-024-00327-x | `refetch-txt/Ma_2024.txt` |
| Fasulo, Longobardo, De Gregorio & Barbarino (2025). Aerospace 12, 647. | 10.3390/aerospace12070647 (confirmed against this session's own fresh dump, line 74: "https://doi.org/10.3390/aerospace12070647") | `refetch-txt/Fasulo_2025.txt` |
| Jawahar, Hanson, Akhter & Azarpeyvand (2025). Sci. Rep. 15, 2170. | 10.1038/s41598-024-82876-9 | `refetch-txt/Jawahar_2025.txt` |
| Zawodny & Haskin (2017). AIAA (NASA Langley LSAWT capability paper). | — (AIAA conference paper, no DOI captured) | `refetch-txt/Zawodny-Haskin_2017.txt` |
| Gallo, De Decker, Bresciani, Haezebrouck, Garone & Schram (2025). Acta Acustica 9, 16. | 10.1051/aacus/2024085 | `refetch-txt/Gallo_2025.txt` |
| Whelchel (2023). PhD thesis, Virginia Tech. | — | `refetch-txt/Whelchel_2023.txt` |
| Alkmim, Cardenuto, Tengan, Dietzen, Van Waterschoot, Cuenca, De Ryck & Desmet (2022). JASA 152, 2735–2745. | 10.1121/10.0014957 | `refetch-txt/Alkmim_2022.txt` |
| Hochbaum et al. (2026). Quiet Drones (Delft) conference paper. | — | `refetch-txt/Hochbaum_2026.txt` |
| Kim, Oh, Ku, Lee, Lee & Kim (2022). ICSV28. | — | `refetch-txt/Kim_2022.txt` |

All twelve extracted with `pdftotext -q <pdf> refetch-txt/<name>.txt` (plain, not `-layout`),
identity-checked against each PDF's own front matter (title/author/DOI visible in the first ~30
lines of the dump), and independently compared against `papers/chamber-problems/EXTRACTS-local.md`
/ `EXTRACTS-downloaded.md` — see "Comparison with earlier notes" in `EXTRACTS-B.md`. Every
specific page number used in `EXTRACTS-B.md` for a standalone conference/report/thesis document
(Nardari, Zawodny-Haskin, Gallo, Homyak, Hodder, Hanson 1977, Hochbaum) was additionally
cross-checked against the source PDF with `pdftotext -f N -l N <pdf> - | grep -F "<quote
fragment>"` (a binary search over pages), because a first-pass line-marker heuristic (treating
any bare digit on its own line as a page footer) was caught making ±1-page errors on both
Jawahar (guessed p.8, confirmed p.9 — matches the earlier note) and Hochbaum (guessed pp.2/4/8,
confirmed pp.3/5/9 — no earlier note to check against for that document). Journal articles with
their own continuous printed pagination (Stephenson, Weitsman, Ma, Fasulo's "N of 26" footers,
Alkmim) were page-mapped from the literal page-number strings visible in the running
header/footer of the pdftotext dump, cross-checked at 3+ points per document.

## NOT RETRIEVED

| Citation | DOI / best URL | Reason |
|---|---|---|
| Hanson, D. B. (1974). "Spectrum of rotor noise caused by atmospheric turbulence." *J. Acoust. Soc. Am.* 55(4), 762–767. | 10.1121/1.1919518 | JASA/AIP — known blocker (PROTOCOL.md rule 5). Semantic Scholar's `openAccessPdf` resolves to `asa.scitation.org/doi/pdf/10.1121/1.1919518` (AIP's own platform, status "BRONZE" i.e. free-to-view-not-open-license, not a real mirror) — same publisher family as the blocked `pubs.aip.org`, not attempted. NTRS search for this exact paper returned nothing beyond Hanson's 1977 CR-2899 (retrieved and used as the best available Hanson primary source instead — see EXTRACTS-B.md). **Adam: fetchable via your Politechnika Warszawska library proxy at the DOI above, or via ASA/AIP if your institution subscribes.** |
| Hanson, D. B. (1975). "Measurements of Static Inlet Turbulence." AIAA Paper 75-467. | no DOI found; cited only as a reference inside Woodward et al. 1978 (NASA TM-73855) | AIAA conference paper, not separately searched on NTRS this session (time budget); Woodward et al. 1978 paraphrases its finding (see EXTRACTS-B.md) and that paraphrase, not a first-hand reading, is what is quoted. |
| Hanson, D. B. (1975). "A Study of Subsonic Fan Noise Sources." AIAA Paper 75-468. | no DOI found; same citation context as above | Same reason as 75-467. |
| Kantola, R. A.; Warren, R. E. (1979). "Reduction of Rotor-Turbulence Interaction Noise in Static Fan Noise Testing." AIAA Paper 79-0656. | NTRS id 19790042912 | Found on NTRS (abstract only: describes a flared reverse-cone inlet, boundary-layer suction and a turbulence-control-structure honeycomb+screen); NTRS lists `downloadsAvailable: []` — AIAA holds copyright on this one and NTRS has metadata only, no PDF. **Adam: fetchable via AIAA ARC (`arc.aiaa.org`) through your library proxy, or Ingenta.** |
| Hanson, Jawahar, Vemuri & Azarpeyvand (2023). "Experimental investigation of propeller noise in ground effect." *J. Sound Vib.* 559, 117751. | 10.1016/j.jsv.2023.117751 | ScienceDirect/Elsevier — known blocker (PROTOCOL.md rule 5); confirmed HYBRID/CC-BY open access via Semantic Scholar (`isOpenAccess: true`) but its `openAccessPdf.url` just resolves back to the ScienceDirect DOI page. Tried the ScienceDirect `pdfft?isDTMRedir=true&download=true` route directly (returns an HTML challenge page, not a PDF); tried Europe PMC (`0` hits — not a biomedical-indexed journal); tried CORE.ac.uk API (redirect loop requiring an API key not held here); did not find a Bristol Pure repository deposit for this specific record. **Adam: the DOI above should render in a browser given the CC-BY hybrid status — try `sciencedirect.com/science/article/pii/S0022460X23002006` directly in a logged-in/proxied browser, or your PW library proxy.** (This exact gap was already logged once before, 2026-09-07, in `papers/chamber-problems/RETRIEVAL-B.md` #5 — still open.) |
| Sevik, M. (1971). Turbulence-ingestion noise paper (exact venue/title not confirmed — likely a Fan Noise Symposium or ASME paper from that era; no clean bibliographic record found). | none found | Crossref bibliographic search for "Sevik 1971 propeller noise turbulence ingestion" returned only later, unrelated papers (Sevik is not a listed author on any of them); NTRS search for "Sevik turbulence ingestion propeller" returned zero results. Could not identify a citable record to even mark as "found but blocked." **Adam: if you have a specific title/venue for this from the original literature-search prompt, send it and it can be searched again.** |

## SEARCHED AND FOUND BUT NOT PURSUED (time budget — already well covered by retrieved sources)

These NTRS records surfaced on the same searches as the five NASA reports above, are
substantively on-topic for Q1, and have PDFs available (`downloadsAvailable: true`), but were
not downloaded/read this session because the retrieved set already answers Q1 with numbers from
multiple independent sources and the protocol's budget guidance (6–12 sources, ~60–90 min) was
already exceeded by the time they surfaced:
- Paterson, R. W.; Amiet, R. K. (1980). "Noise of a model helicopter rotor due to ingestion of
  turbulence." NASA CR (NTRS id 19800002821).
- Hagen, M. J.; Yamauchi, G. K.; Signor, D. B.; Mosher, M. (1995). "Measurements of atmospheric
  turbulence effects on tail rotor acoustics." NTRS id 19950005947.
- Simonich, J. C. (1989). "Noise produced by turbulent flow into a rotor" theory/user manuals.
  NTRS ids 19890018095, 19890019783.

## SEARCH QUERIES USED

- NTRS: `inflow control device fan noise`; `turbulence control structure fan noise`; `Woodward
  inflow control device fan noise`; `Ginder Balombin fan noise` (0 results); `Hanson spectrum
  rotor noise atmospheric turbulence`; `Hanson 1974 spectrum rotor noise atmospheric turbulence`;
  `Sevik turbulence ingestion propeller` (0 results); `Sevik noise propellers turbulence` (0
  results); `rotor noise atmospheric turbulence ingestion`.
- Crossref: `query.bibliographic=Sevik+1971+propeller+noise+turbulence+ingestion`;
  `query.bibliographic=Hanson+1974+spectrum+rotor+noise+atmospheric+turbulence`.
- Semantic Scholar (rate-limited, ≤1 request/10 s, per protocol): `DOI:10.1016/j.jsv.2023.117751`
  (Hanson et al. 2023 JSV — confirmed CC-BY hybrid, no usable mirror); `DOI:10.1121/1.1919518`
  (Hanson 1974 JASA — resolves to AIP's own bronze-access page, not attempted per blocker rule).
- Direct URL attempts: Europe PMC REST search for the JSV DOI (0 hits); `research-information.
  bris.ac.uk` search page for the Hanson/Jawahar/Vemuri/Azarpeyvand JSV paper (returned nothing
  usable); ScienceDirect `pdfft?isDTMRedir=true&download=true` for the same DOI (returned an
  HTML page, confirmed by `file` as "HTML document" not PDF); CORE.ac.uk `/v3/search/works`
  (redirect requiring an API key).
- Held-corpus search (no network): `grep -rl` across `papers/*/*.md` for author-name matches to
  find every earlier note touching a paper this thread reuses, before re-reading each one fresh.
