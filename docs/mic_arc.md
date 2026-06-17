# Microphone arc — serial ↔ elevation map

Physical UMIK-2 arrangement on the vertical directivity arc. 11 positions at
18° intervals from +90° (overhead) to −90° (below). Elevation 0° is the prop
plane. All 11 serials known.

| Elevation | UMIK-2 serial | Cal filename (on-axis) |
|----------:|:--------------|:-----------------------|
| **+90°**  | 811-1897      | `8111897.txt` |
| **+72°**  | 811-1892      | `8111892.txt` |
| **+54°**  | 810-8901      | `8108901.txt` |
| **+36°**  | 810-8893      | `8108893.txt` |
| **+18°**  | 811-2321      | `8112321.txt` |
| **0°**    | 810-8897      | `8108897.txt` |
| **−18°**  | 811-2310      | `8112310.txt` |
| **−36°**  | 810-8900      | `8108900.txt` |
| **−54°**  | 810-8903      | `8108903.txt` |
| **−72°**  | 811-1896      | `8111896.txt` |
| **−90°**  | 810-8904      | `8108904.txt` |

Notes:
- Order was given top-down (+90 → −90); all 11 serials recorded.
- USB device index (`hw:N`) is intentionally **not** recorded here — it shifts per boot/port. Map physical mic → device at capture time with the Setup page's 🎤 Listen meter.
- **Calibration files**: miniDSP UMIK-2 per-serial `.txt` (REW format). Each serial yields two files: `<serial>.txt` (on-axis / 0°) and `<serial>_90deg.txt`. Use the **on-axis** file — the arc mics point at the source. Download is Cloudflare-gated, so it must be done in a real browser (see below); `scripts/load_mic_arc.py` then uploads them + builds a Setup preset.
- This arc map is mirrored in `scripts/load_mic_arc.py` (the `ARC` list) — keep both in sync.

## Loading into SoundVisualizer

1. In a normal browser tab, open <https://www.minidsp.com/products/acoustic-measurement/umik-2> → **Unique Calibration File Download**. Enter each serial (with dash, e.g. `810-8897`), submit; it downloads `<serial>.txt` + `<serial>_90deg.txt`.
   Serials: `811-1897 811-1892 810-8901 810-8893 811-2321 810-8897 811-2310 810-8900 810-8903 811-1896 810-8904`
2. From the laptop: `python3 scripts/load_mic_arc.py --dir ~/Pobrane` (or wherever they downloaded). Add `--dry-run` first to preview.
   This uploads each cal file to the Pi and creates a Setup preset **"11-mic preset"**.
3. On the Setup page → Microphones → presets bar → load that preset. Then assign each physical mic to its USB device with the 🎤 Listen meter.
