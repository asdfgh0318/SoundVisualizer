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

- `*.pdf` — papers read at source (33). Names: `venueYEAR_firstauthor_topic.pdf`.
- `txt/` — `pdftotext -layout` dumps; `*.abstract.txt` = abstract-only sources; `*.NOTE.txt` = translation notes.
- `EXTRACTS-core.md` — structured notes on the five core chamber papers (read in full by Claude).
- `EXTRACTS-local.md` — notes on the 14 papers copied from elsewhere on the laptop (rotor/recirculation/ground-plane set).
- `EXTRACTS-downloaded.md` — notes on the papers fetched for this brief (qualification standards, active absorption, wind tunnels, ground treatments).
- `RETRIEVAL-A.md`, `RETRIEVAL-B.md` — what was and was not retrieved, with the URL that worked or the best URL for a manual/proxy fetch.

## Still missing (manual fetch)

Fetched by Adam 2026-09-07: Singh 2020, Garg 2019, Ma 2022, UCMAR 2019, Jenny & Anderson 2011, Palchikovskiy 2016, Belyaev 2015 (English). Remaining:

| Paper | DOI / URL |
|---|---|
| Hanson et al. 2023, *Experimental investigation of propeller noise in ground effect*, JSV 559:117751 | 10.1016/j.jsv.2023.117751 — CC-BY, one click in a browser |
| Stroud 2010, AES Convention 129 paper 8170 | https://aes.org/publications/elibrary-page/?id=15593 |
| Xiang, Wang & Chen 1990, Applied Acoustics 29 139 | 10.1016/0003-682X(90)90027-R |
| Amiet 1978, JSV 58 467 (NASA CR-3371 held as substitute) | 10.1016/0022-460X(78)90353-X |
| "Miniature anechoic chamber for medical devices" | https://www.researchgate.net/publication/293101716 |

Drop PDFs here with any name; re-run `pdftotext -layout` into `txt/` and update the extracts and the brief's ledger.
