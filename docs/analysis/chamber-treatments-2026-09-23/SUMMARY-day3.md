# Chamber findings, day 3 — top 5 setups

Coefficient = room error below 3 kHz (rms dB across the arc vs arc mean; lower = flatter). Repeat 0.01 dB, handling ~0.04 dB. Rerun of the last config on 2026-09-30: 1.399.

| # | setup | run | room error | vs best | tilt removed | 250–400 | 400–630 | 630–1000 | 1000–1600 | 1600–3000 | qualified from | bands failed /11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | last config | `2026-09-25/carpet-reordered` | **1.387** | +0.086 | 1.165 | 1.99 | 1.52 | 1.47 | 0.85 | 0.96 | 2000 Hz | 4 |
| 2 | cleanup-1 | `2026-09-25/cleanup-1` | **1.301** | — | 1.157 | 1.56 | 1.62 | 1.43 | 0.81 | 1.03 | 1000 Hz* | 3 |
| 3 | backed-5cm | `2026-09-25/backed-5cm` | **1.303** | +0.002 | 1.157 | 1.57 | 1.61 | 1.44 | 0.81 | 1.03 | 1000 Hz* | 3 |
| 4 | closer | `2026-09-25/closer-a` | **1.311** | +0.011 | 1.183 | 1.99 | 1.28 | 1.29 | 0.86 | 0.97 | 315 Hz* | 1 |
| 5 | cleanup-2 | `2026-09-25/cleanup-2` | **1.314** | +0.014 | 1.162 | 1.61 | 1.72 | 1.40 | 0.79 | 0.98 | 500 Hz | 2 |

- **last config** — ACCEPTED (Adam, 2026-09-30) and the last configuration of day 3 (19:20): the full carpet on standoffs, layer order changed (bottom layer moved to the top).
- **cleanup-1** — BEST by score. The backed-5cm state with the loose felt sheets removed.
- **backed-5cm** — Accepted on 2026-09-25, superseded by the last config: speaker backed off 5 cm from the ring plane, raised thick carpet.
- **closer** — Speaker moved ~20 cm closer to the ring, still on the axis; morning floor stack of day 3 (after the blue absorbing carpet was added). Repeat `closer-b` agrees to 0.006 dB.
- **cleanup-2** — The accepted state after more junk was removed (what, not stated).

`*` = the cut-off band is marginal (within the day-to-day scatter of the limit).

**The last config's deficit is the source, not the carpet:** with each map's top-to-bottom tilt fitted out it scores 1.165 vs 1.157 for cleanup-1. The source moved at cleanup-3 (level +0.63 dB, 16:20) and at carpet-removed (tilt +0.49 → -0.31, 17:23); it was not put back.

The accepted state is setup 1. Alone, it is clearly over the limit at 250, 500, 800, 1600 Hz and marginal at 630, 1250 Hz; band level qualified from 2000 Hz.

Top four are tied (span 0.014 dB). Setup 1 is the last config of the day; the waterfall page for each is in `SUMMARY-day3.pdf` (A4), drawn against cleanup-1.

## Bands (ISO 3745 analogue: ±1.5 dB to 630 Hz, ±1.0 dB from 800 Hz; reference = arc mean)

| band | limit | tones | setups over the limit, of 5 | pure tones in limit, median | verdict |
|---|---|---|---|---|---|
| 250 Hz | ±1.5 | 3 | 2 clear + 1 marginal | 88 % | setup-dependent |
| 315 Hz | ±1.5 | 8 | 3 clear + 1 marginal | 61 % | avoid |
| 400 Hz | ±1.5 | 8 | 3 clear + 1 marginal | 61 % | avoid |
| 500 Hz | ±1.5 | 8 | 1 clear + 0 marginal | 66 % | setup-dependent |
| 630 Hz | ±1.5 | 8 | 0 clear + 1 marginal | 62 % | borderline |
| 800 Hz | ±1 | 8 | 3 clear + 0 marginal | 47 % | avoid |
| 1000 Hz | ±1 | 9 | 0 clear + 3 marginal | 69 % | borderline |
| 1250 Hz | ±1 | 8 | 0 clear + 3 marginal | 82 % | borderline |
| 1600 Hz | ±1 | 8 | 1 clear + 0 marginal | 76 % | setup-dependent |
| 2000 Hz | ±1 | 8 | 0 clear + 0 marginal | 77 % | holds |
| 2500 Hz | ±1 | 8 | 0 clear + 1 marginal | 67 % | borderline |

- Avoid: 315, 400, 800 Hz. Clean in all five: 2000 Hz. Borderline: 630, 1000, 1250, 2500 Hz. Setup-dependent: 250, 500, 1600 Hz.
- Pure tones are not qualified in any band. 3–5 kHz never usable (sphere); 5–6.4 kHz indicative; below 257 Hz not measured.
- Marginal = within ±0.09 dB of the limit (the last config vs its rerun scatter). "avoid/depends/holds" thresholds are ours, not from a standard.
