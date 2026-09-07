# papers/chamber-problems

Source set for [`docs/anechoic-chamber-problems-brief.pdf`](../../docs/anechoic-chamber-problems-brief.pdf)
(HTML source: `docs/anechoic-chamber-problems-brief.html`) — how anechoic-chamber problems
(standing waves, direct/reflected interference, ground reflection, recirculation, shear layers)
show up in data, how the literature reads them, and what is done about them.

Assembled 2026-09-07. Complements `papers/anechoic-simulation/` (chamber design/qualification/
simulation set behind `docs/anechoic-simulation.html`), which holds the core papers this set
extends (Cunefare 2003, Bonfiglio & Pompoli 2013, Schneider 2009, Jiang 2016, Wang & Tang 1996,
Vorländer 2013, Brinkmann 2019 — all now full text).

## Layout

- `*.pdf` — papers read at source (26). Names: `venueYEAR_firstauthor_topic.pdf`.
- `txt/` — `pdftotext -layout` dumps; `*.abstract.txt` = abstract-only sources; `*.NOTE.txt` = translation notes.
- `EXTRACTS-core.md` — structured notes on the five core chamber papers (read in full by Claude).
- `EXTRACTS-local.md` — notes on the 14 papers copied from elsewhere on the laptop (rotor/recirculation/ground-plane set).
- `EXTRACTS-downloaded.md` — notes on the papers fetched for this brief (qualification standards, active absorption, wind tunnels, ground treatments).
- `RETRIEVAL-A.md`, `RETRIEVAL-B.md` — what was and was not retrieved, with the URL that worked or the best URL for a manual/proxy fetch.

## Still missing (manual fetch)

| Paper | DOI / URL |
|---|---|
| Singh, Garg & Narayanan 2020, *Estimation of the lower cut-off frequency of an anechoic chamber*, Int. J. Aeroacoustics | 10.1177/1475472X20905070 (SAGE, proxy) |
| Hanson et al. 2023, *Experimental investigation of propeller noise in ground effect*, JSV 559:117751 | 10.1016/j.jsv.2023.117751 — CC-BY, one click in a browser |
| Garg et al. 2019, MAPAN 34(3) | 10.1007/s12647-019-00343-7 |
| Ma et al. 2022, Applied Acoustics 186:108424 (active MPP absorber) | 10.1016/j.apacoust.2021.108424 |
| Wang et al. 2019, UCMAR, Acta Acustica united with Acustica 105 | 10.3813/AAA.919353 |
| Stroud 2010, AES Convention 129 paper 8170 | https://aes.org/publications/elibrary-page/?id=15593 |
| Jenny & Anderson 2011, JASA-EL 130 EL69 (thesis version held) | 10.1121/1.3606461 |
| Palchikovskiy et al. 2016, AIP Conf. Proc. 1770 030116 | 10.1063/1.4964058 |
| Xiang, Wang & Chen 1990, Applied Acoustics 29 139 | 10.1016/0003-682X(90)90027-R |
| Amiet 1978, JSV 58 467 (NASA CR-3371 held as substitute) | 10.1016/0022-460X(78)90353-X |

Drop PDFs here with any name; re-run `pdftotext -layout` into `txt/` and update the extracts and the brief's ledger.
