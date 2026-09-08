# RETRIEVAL-D.md — Thread D: microphone calibration accuracy, drift, and fault-diagnosis

## RETRIEVED

| # | Citation | DOI | Route that worked | File |
|---|---|---|---|---|
| 1 | Garg, Surendran, Dhanya, Chandran, Asif & Singh (2019), MAPAN 34(3):357–369 [HELD] | 10.1007/s12647-019-00343-7 | already held in `papers/chamber-problems/`; re-extracted fresh with plain `pdftotext -q` for this thread | `papers/chamber-problems/Garg_2019_MAPAN_microphone-free-field-calibration-uncertainty.pdf`; refetch dump `papers/arc-validation/refetch-txt/Garg_2019_MAPAN_microphone-free-field-calibration-uncertainty.txt` |
| 2 | Burnett & Nedzelnitsky (1987), J. Res. NBS 92(2):129–151 [HELD] | none printed (pre-DOI; DOI 10.6028/jres.092.013 assigned retroactively) | already held in `papers/small-chamber/`; re-extracted fresh | `papers/small-chamber/Burnett-Nedzelnitsky_1987_JResNBS_free-field-reciprocity-calibration-chamber-deviations.pdf`; refetch dump `papers/arc-validation/refetch-txt/Burnett-Nedzelnitsky_1987_JResNBS_free-field-reciprocity-calibration-chamber-deviations.txt` |
| 3 | Wagner & Guthrie (2015), J. Res. NIST 120:164–172 | 10.6028/jres.120.012 | direct PDF: `curl -sL -A <browser UA> https://nvlpubs.nist.gov/nistpubs/jres/120/jres.120.012.pdf` | `papers/arc-validation/Wagner_2015_NIST-JRes_condenser-mic-long-term-stability.pdf` |
| 4 | Risojević, Rozman, Pilipović, Češnovar & Bulić (2018), Sensors 18(7):2351 | 10.3390/s18072351 | `curl -sL -A <UA> https://mdpi-res.com/d_attachment/sensors/sensors-18-02351/article_deploy/sensors-18-02351.pdf` (plain URL worked, no `-v2` needed) | `papers/arc-validation/Risojevic_2018_Sensors_low-cost-wireless-node-sound-level.pdf` |
| 5 | Picaut, Can, Fortin, Ardouin & Lagrange (2020), Sensors 20(8):2256 | 10.3390/s20082256 | `curl -sL -A <UA> https://mdpi-res.com/d_attachment/sensors/sensors-20-02256/article_deploy/sensors-20-02256.pdf` | `papers/arc-validation/Picaut_2020_Sensors_low-cost-noise-sensors-review.pdf` |
| 6 | Mydlarz, Salamon & Bello (2016), arXiv:1605.08450v1 [cs.SD] (preprint of Appl. Acoust. 117:207–218, 2017) | none (arXiv) / published version 10.1016/j.apacoust.2016.10.024 (not fetched — Elsevier) | `curl -sL -A <browser UA> https://arxiv.org/pdf/1605.08450` | `papers/arc-validation/Mydlarz-Salamon-Bello_2016_arXiv_low-cost-urban-acoustic-monitoring.pdf` |
| 7 | IEC 61094-8:2012 (preview) | none (standard) | `curl -sL https://cdn.standards.iteh.ai/samples/18912/d6cabc2801a74056a9d31369715e9684/IEC-61094-8-2012.pdf` | `papers/arc-validation/IEC-61094-8_2012_standard_freefield-comparison-calibration-preview.pdf` |
| 8 | IEC 61094-6:2004 (preview) | none (standard) | `curl -sL https://cdn.standards.iteh.ai/samples/12181/3055cee4dce64668ac18d5a74af692a8/IEC-61094-6-2004.pdf` | `papers/arc-validation/IEC-61094-6_2004_standard_electrostatic-actuator-grids-preview.pdf` |
| 9 | IEC 60942:2017 (preview) | none (standard) | `curl -sL https://cdn.standards.iteh.ai/samples/22818/021e399832234de8aee28f5e994f162c/IEC-60942-2017.pdf` | `papers/arc-validation/IEC-60942_2017_standard_sound-calibrators-preview.pdf` |
| 10 | Cameron, Croarkin & Raybold (1977), NBS Technical Note 952 | 10.6028/NBS.TN.952 | DOI resolved (`curl -sIL https://doi.org/10.6028/NBS.TN.952`) → `curl -sL -A <UA> https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote952.pdf` | `papers/arc-validation/Cameron_1977_NBS-TN952_mass-calibration-designs.pdf` |
| 11 | miniDSP Ltd, "UMIK-2" product brief [vendor] | n/a | direct curl: `minidsp.com/images/documents/Product Brief - UMIK-2.pdf` (also independently saved via a WebFetch attempt that reported "corrupted binary" but wrote a valid PDF to the session tool-results directory — copied out and cross-checked, identical content) | `papers/arc-validation/miniDSP_nd_vendor_UMIK-2-product-brief.pdf` |
| 12 | miniDSP Ltd, "UMIK-2 User Manual" [vendor] | n/a | direct curl: `minidsp.com/images/documents/miniDSP UMIK-2-User Manual.pdf` | `papers/arc-validation/miniDSP_nd_vendor_UMIK-2-user-manual.pdf` |
| 13 | miniDSP Ltd, "UMIK-1" product brief [vendor] | n/a | direct curl: `minidsp.com/images/documents/Product Brief - Umik.pdf` | `papers/arc-validation/miniDSP_nd_vendor_UMIK-1-product-brief.pdf` |

## NOT RETRIEVED

Primary sources cited *inside* a source I did read (Picaut et al. 2020, Risojević et al. 2018, or
Mydlarz et al. 2016) that I did not independently fetch/verify — claims from these in EXTRACTS-D.md
are explicitly attributed to the reporting paper, not asserted as independently checked:

| Citation | DOI / ID | Best URL for the proxy | Reason not retrieved |
|---|---|---|---|
| Renterghem, T.V., Thomas, P., Dominguez, F., Dauwe, S., Touhafi, A., Dhoedt, B., Botteldooren, D. (2011). "On the ability of consumer electronics microphones for environmental noise monitoring." *J. Environ. Monit.* 13, 544–552. | 10.1039/c0em00532k | `pubs.rsc.org/en/content/articlelanding/2011/em/c0em00532k` | RSC (Royal Society of Chemistry) — `articlepdf` route returned an HTML paywall page, not a PDF. Not in PROTOCOL.md's known-blocker list; newly encountered here. |
| Barham, R. & Goldsmith, M. (2008). "Performance of a new MEMS measurement microphone and its potential application." *Proc. Institute of Acoustics, Spring Conference*, Reading, UK, 10–11 April 2008, pp. 370–377. | none found | none found | UK Institute of Acoustics conference proceedings; no open repository located in the time budget. |
| Bartalucci, C., Borchi, F., Carfagni, M., Furferi, R., Governi, L., Lapini, A., Bellomini, R., Luzzi, S., Nencini, L. (2018). "The smart noise monitoring system implemented in the frame of the Life MONZA project." *11th European Congress and Exposition on Noise Control Engineering* (Euronoise 2018), Heraklion, Crete, 27–31 May 2018, pp. 27–31. | none found | possibly `euronoise2018.eaa-fenestra.org` proceedings archive (not checked — out of time budget for this thread) | Not attempted; conference proceedings, low priority relative to budget since the claim (1–2 dB running-in drift) was already available second-hand via Picaut et al. |
| Li, J., Broas, M., Raami, J., Mattila, T.T., Paulasto-Kröckel, M. (2014). "Reliability assessment of a MEMS microphone under mixed flowing gas environment and shock impact loading." *Microelectron. Reliab.* 54, 1228–1234. | 10.1016/j.microrel.2014.02.020 (Crossref-style DOI pattern; not independently confirmed) | `sciencedirect.com/science/article/pii/S0026271414000862` (URL guessed from DOI pattern, not confirmed by fetch) | Elsevier/ScienceDirect — known blocker (PROTOCOL.md). Not attempted. |
| Scheeper, P., Nordstrand, B., Gullv, J., Liu, B., Clausen, T., Midjord, L., et al. (2003). "A new measurement microphone based on MEMS technology." *J. Microelectromech. Syst.* 12(6), 880–891. | 10.1109/JMEMS.2003.820286 (from IEEE numbering convention; not independently confirmed) | `ieeexplore.ieee.org` (exact document ID not looked up) | IEEE Xplore — known blocker (PROTOCOL.md). Not attempted. |
| [Authors unknown from search snippets]. "Microphone Channel Frequency Response Calibration Using Circular Shifting and Spatio-Temporal Prediction." *IEEE Trans. Instrum. Meas.* | 10.1109/TIM.2023.3318705 | `ieeexplore.ieee.org/document/10262008/` | IEEE Xplore — known blocker. This was the single most promising lead for Q2's "rotating microphones through positions" ask (per its abstract, microphones are deployed in a rotating symmetric arrangement with circular shifting so each channel sees every position) but could not be fetched. |
| [Authors unknown from search snippets]. "In-situ microphone channel frequency response calibration using eigenvalue decomposition." *Applied Acoustics*. | 10.1016/j.apacoust.2024.110475 | `sciencedirect.com` | Elsevier — known blocker. Related follow-up to the IEEE paper above; not attempted. |
| Xiao, H., Shao, H.-Z., Peng, Q.-C. (2007). "A New Calibration Method for Microphone Array with Gain, Phase, and Position Errors." *J. Electron. Sci. Technol.* 5(3), 248–251. | none found | `journal.uestc.edu.cn/en/article/id/1956` | Both WebFetch and the page itself returned HTTP 403 Forbidden. |
| [Authors/year unknown from search snippet]. "Laser-based comparison calibration of laboratory standard microphones." *JASA Express Letters* 1(8), 082803. | not looked up | `pubs.aip.org/asa/jel/article/1/8/082803/220362/` | AIP Publishing — known blocker (PROTOCOL.md); not attempted, listed only because it surfaced in search and is on-topic for Q2 (a *modern* comparison-calibration uncertainty budget, which would update/extend Garg 2019 and Burnett & Nedzelnitsky 1987). Worth Adam fetching via the university proxy if a more current comparison-calibration uncertainty figure is wanted. |

## SEARCHED AND REJECTED

Found and screened but not used as evidence — either not peer-reviewed/standards-grade, or
substantively off-topic, or superseded by a better source already retrieved:

- ASR (audiosciencereview.com) forum thread, "miniDSP Umik-1 USB measurement microphone real world
  performance review" — anonymous forum test, no stated methodology or traceable reference;
  excluded per the evidence-tier rule (journal/standard/report/thesis/conference/vendor only).
- diyAudio.com, equivalent UMIK-1 review thread — same reason.
- AVS Forum, "Cross-Spectrum calibrated UMIK-1 accuracy after 4 years of normal usage" — directly
  on-topic for Q3 (a single user's UMIK-1 drift anecdote) but a single anonymous unit with no
  independent verification; excluded.
- AVS Forum, "MiniDSP's New UMIK-2 and UMIK-X Measurement Microphones" — product-announcement
  thread, no accuracy data.
- audioXpress, "Measurement Microphones: The Good, Bad, and Ugly" — trade magazine, not
  peer-reviewed; no specific number from it was used.
- Archimago's Musings (blog), UMIK-2 posts — personal blog, not evidence-grade.
- `minidsp.com/applications/acoustic-measurements/umik-1-setup-with-rew` — fetched successfully via
  curl (WebFetch was blocked with HTTP 403) but contains only a setup walkthrough; no "Sens Factor"
  definition or accuracy statement found in the page text.
- NISTIR 5672 (Fraley, K.L. & Harris, G.L., 2014, "Advanced Mass Calibration and Measurement
  Assurance Program for State Calibration Laboratories") — downloaded incidentally while trying to
  resolve a guessed NIST `pub_id` for Technical Note 952 (wrong guess); briefly reviewed and confirms
  the same "weighing design" concept as Cameron et al. 1977 (mass-standard intercomparison designs,
  restraints, drift-balancing), but Cameron et al. 1977 is the original/classic source it itself
  builds on and was obtained directly, so NISTIR 5672 was not used as a citation.

## Search queries used

WebSearch: `UMIK-1 accuracy evaluation measurement microphone class 1 comparison`; `miniDSP UMIK-2
datasheet capsule Sens Factor calibration file accuracy`; `low-cost measurement microphone
calibration comparison MDPI Sensors class 1`; `MEMS microphone sensitivity drift aging long-term
stability`; `microphone array rotation round-robin calibration separate gain position response`;
`IEC 61094-8 comparison method microphones free-field calibration scope`; `distinguish sensitivity
offset error frequency response shape error microphone calibration`; `"Long-Term Stability"
"Condenser Microphones" NIST calibration Journal of Research`; `"Free-Field Reciprocity Calibration
Of Microphones" PMC NIST Journal Research`; `Segura-Garcia low-cost acoustic sensor MEMS microphone
calibration class 1 sound level meter MDPI`; `IEC 60942 sound calibrators pistonphone class 1 scope
iTeh`; `"A New Calibration Method for Microphone Array with Gain, Phase, and Position Errors"
uestc`; `UMIK-2 review measurement accuracy anechoic frequency response comparison test`; `low cost
MEMS microphone array calibration acoustic camera drone noise directivity accuracy`; `"UMIK"
microphone DAGA OR "Inter-Noise" OR "Forum Acusticum" OR ICSV calibration accuracy`; `"UMIK-1" OR
"UMIK-2" arxiv.org measurement microphone`; `evaluation consumer measurement microphone frequency
response repeatability reference microphone journal acoustics`; `"circular shifting" microphone
channel frequency response calibration DOI publisher`; `Latin square design comparison calibration
reference standards metrology round robin`; `NIST calibration designs mass standards ABBA sequence
Latin square metrology handbook`; `IEC 61094-8 iteh standards preview sample pdf
cdn.standards.iteh.ai`.

Crossref API (`api.crossref.org/works?query.bibliographic=...`): bibliographic search for the
"circular shifting" paper (returned DOI 10.1109/tim.2023.3318705 plus two related IEEE/Elsevier
follow-ups); bibliographic search for Renterghem et al.'s title (returned DOI 10.1039/c0em00532k);
bibliographic search for Mydlarz/Salamon/Bello's title (used to confirm the arXiv preprint
corresponds to Appl. Acoust. 117:207–218).

WebFetch attempts that failed or were unnecessary: `minidsp.com/products/acoustic-measurement/umik-2`
(HTTP 403); `minidsp.com/applications/acoustic-measurements/umik-1-setup-with-rew` (HTTP 403,
retried successfully with plain `curl`); `journal.uestc.edu.cn/en/article/id/1956` (HTTP 403);
`pmc.ncbi.nlm.nih.gov/articles/PMC4730669/` (succeeded — used to identify Wagner & Guthrie 2015
before fetching the primary PDF directly from NIST).
