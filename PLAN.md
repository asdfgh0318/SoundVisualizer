# Plan — SoundVisualizer refactor

Living plan. See [CLAUDE.md](CLAUDE.md) for project context and locked decisions. Original scope in [2.md](2.md).

## Architecture

```
┌──────────────────┐  HTTP/WS  ┌─────────────────────────────────────────┐
│  Laptop browser  │ ────────► │  Laptop (dev) → RPi 5 (production)       │
│  React + Vite    │           │  Python 3.12 + FastAPI + asyncio        │
│  Plotly.js + ZS  │           │  ├─ Tyto 1585 (Paweł's MSP serial)      │
└──────────────────┘           │  ├─ NOR-145 (Paweł's WS+FTP) [later]    │
                               │  ├─ 6× UMIK-2 (sounddevice + udev)      │
                               │  ├─ Cutoff watchdog                     │
                               │  ├─ Capture-run orchestrator            │
                               │  └─ Filesystem DB: JSON+WAV per meas    │
                               └─────────────────────────────────────────┘
```

## Data store

```
data/
  <motor>__<propeller>__<shroud>__<notes>/    # key dir, fields sluggified
    key.json                                  # {motor, propeller, shroud, notes}
    measurements/
      2026-05-12T09-39-48-105828__acoustic__top__mic-8100001/
        meta.json    # {type:"acoustic", t_start, t_end, mic_serial,
                     #  elevation_deg, azimuth_deg:null, sample_rate,
                     #  calibration_file_id, pwm_setpoint, half}
        audio.wav
      2026-05-12T09-39-48-105828__performance/
        meta.json    # {type:"performance", t_start, t_end, pwm_setpoint}
        telemetry.csv
      2026-...__norsonic/             # later, when NOR arrives
        meta.json
        norsonic.txt
        norsonic.json   # parsed report
```

Each capture step writes one performance row + N acoustic rows (one per UMIK-2) + optionally one NOR row, sharing identical `t_start`/`t_end` so they're joinable. `azimuth_deg` is fixed `null` in MVP (slot reserved for future asymmetric-object work).

## Phases

Order chosen so the existing browser-only app kept working as a reference until phase 2 cut it over.

| # | Phase | Status | Deliverable |
|---|-------|--------|-------------|
| 0 | Repo split | ✅ Done | `server/` directory scaffolding. Paweł's six modules copied verbatim into `server/vendor/pawel/`. |
| 1 | Server skeleton + DB | ✅ Done | FastAPI app, `data/` filesystem store, OpenAPI types, Pydantic schemas. |
| 4 | UMIK-2 capture | ✅ Done | `sounddevice` multi-stream, REW-format cal parser, server-side trigger-onset sync, udev rule generator. |
| 3 | Tyto integration | ✅ Done | Paweł's `msp.py`/`thrust_stand.py` wired up. Calibration constants moved to `config.toml`. **Cutoff watchdog** added (all 8 channels). Live telemetry over `/tyto/ws/telemetry`. |
| 2 | Frontend rebuild | ✅ Done | Legacy Web Audio + spinorama stripped. New Setup page: manual USB-path picker, mic list with add/delete, per-mic cal upload, cutoff-trigger config UI, live Tyto status, audio device list filtered to `(hw:…)` only. |
| 5 | Capture wizard | ✅ Done | Motor/propeller/shroud/notes form → PWM ramp with **live SVG visualization** → review → safety modal → top half (live progress + Tyto telemetry WS) → reconfigure modal → bottom half → done. Top-only / bottom-only checkboxes. **Recording duration is per-step** (`recording_ms`, no separate field). **"Run fake capture (no hardware)" button** bypasses Tyto and synthesizes realistic drone-noise data. |
| 7 | Results — FFT tab | ✅ Done | Per-PWM-point page with performance header strip + scrollable per-mic FFT rows. Settings popover for window/size/overlap. |
| 8 | Results — Polar tab | ✅ Done | SPL-vs-elevation polar plot. 180°/360° toggle. **Top+bottom merge** combines sibling captures at same PWM. Right rail: range + 1/3-octave + octave columns with snap-to. |
| 9 | Results — Custom tab | ✅ Done | Plotly port of Paweł's Bokeh viz. X/Y scatter with column pickers (PWM/thrust/torque/current/voltage/RPM/temp/SPL-in-band). Clicking a point snaps the FFT and Polar tabs to that PWM step via shared sidebar selection. |
| 6 | Norsonic | ⏳ Deferred | Waiting on NOR-145 delivery. Paweł's `norsonic*.py` already vendored, dormant. Setup page shows deferred placeholder. |
| 10 | RPi packaging | ✅ Done & deployed | Raspberry Pi **5** (delivered; replaced the planned RPi 4), running **Debian 13 Trixie** → **system Python 3.13**, so no pyenv/compile (all deps have aarch64 wheels). Native systemd + venv: `deploy/soundvis.service`, `python -m server` entrypoint reading `[server]` host/port from config, FastAPI-served prod bundle on :8000. Deploy from the laptop with `scripts/deploy_to_pi.sh <user>@<host>` (builds bundle locally + ships it → no Node on the Pi, good for small SD cards); `scripts/setup_rpi.sh` is the on-device installer (dist-aware). Live at `http://jama.local:8000` (hostname `jama`). Setup docs in `deploy/README.md`. The old VL805 firmware-bandwidth caveat is gone — the Pi 5's RP1 chip has real USB 3.0. 48 kHz stays (locked decision for the drone band, not a bandwidth workaround). |

## Post-MVP enhancements delivered

These were not in the original 2.md scope but came up during development:

- **Realistic drone-noise synthesis** for `/dev/seed` and `/dev/fake_capture`: BPF + 11 harmonics + LF spreaded hump (around BPF) + HF broadband (1.5–5 kHz center). Elevation-dependent directivity per component (strong on BPF/harmonics, medium on LF, weak on HF). Matches the standard propeller-noise spectrum textbook breakdown.
- **Fake capture runs through the full wizard.** "Run fake capture (no hardware)" goes through safety modal → simulated progress in the RunningView (animated step-by-step phase transitions over ~5 seconds per half) → reconfigure modal → bottom half → done — exactly the same UX as a real capture, just with synthetic data underneath. Useful for testing the wizard flow and exercising Results tools without the rig.
- **Savable mic presets.** Setup → Microphones has a presets bar: server-stored named snapshots of the mic list (count + serials + top/bottom elevations + calibration assignments). USB device indices intentionally *not* in the preset since they shift per machine/boot. Endpoints `GET/POST/DELETE /setup-presets`. Stored as `data/setup-presets/<uuid>.json`.
- **PWM-point merge with compatibility check.** `/keys/{slug}/pwm_points` returns merged points grouped by PWM µs. Top + bottom captures at the same PWM collapse to one sidebar entry (chip `T+B`) when their performance summaries agree within the configured tolerances. Incompatible captures stay as separate entries with `TOP only` / `BOTTOM only` chips. Multiple compatible captures show explicit composition (`2T + 1B`). Sidebar cards expand to reveal underlying captures with timestamps; clicking one drills the FFT/Polar/Custom tabs into that single half. The merged `acoustic` list dedupes by elevation so the 0° mic doesn't appear twice — drill-down preserves the per-capture mic list. Tolerances live at `data/compat-tolerances.json` with sane per-channel absolute + relative defaults, editable on the Setup page. Endpoints `GET/PUT /compat-tolerances`.
- **Audio device filter** — only ALSA `(hw:…)` real devices shown (drops PulseAudio/PipeWire/SRC-plugin virtual entries). On macOS/Windows the filter is disabled (no equivalent virtual layer).
- **Refresh button** on the Results PWM-point sidebar to re-fetch from server after generating new data.
- **Idiot-proof Quick start in README** — step-by-step from `git clone` to fake-capture rendered in Results, with troubleshooting table for common gotchas.
- **Psychoacoustics tab** — per-mic table with loudness (sone), sharpness (acum), roughness (asper), fluctuation strength (vacil, currently 0 — see report), and Psychoacoustic Annoyance (PA) for the selected PWM point. Computed server-side via `mosqito` (ISO 532-1 loudness, DIN 45692 sharpness, Daniel-Weber roughness) with PA from the Zwicker formula. Results cached in `psychoacoustics.json` next to each `audio.wav` so first-render cost (~1 s/mic) is amortized. Math reference: `docs/psychoacoustics_report.{tex,pdf}` (also PL translation in `psychoacoustics_report_pl.{tex,pdf}`).
- **Live per-mic input-level meter** (Setup) — a "🎤 Listen" toggle per mic row opens a WebSocket (`/devices/audio/{index}/level`) streaming RMS/peak dBFS at ~15 Hz, shown as a level bar with peak-hold. Lets you tap a mic and see which device responds — the only way to tell UMIK-2s apart since they all report USB serial `00000`. One listener at a time (a device can't be opened twice).
- **Tyto zero/tare** — "Zero stand" button (Setup) samples the at-rest load-cell baseline (`POST /tyto/zero`, idle-only) and subtracts it from thrust/torque/current in both live telemetry and the recorded `telemetry.csv`; clear restores raw. The load cell reads a non-zero resting offset (~4.6 N on our unit) that would otherwise contaminate every measurement.

## Open questions

- **Multi-mic udev naming** — UMIK-2s report USB serial `00000`, so `scripts/generate_udev.py`'s serial-based rules collide for >1 mic. Needs port-path-based rules (which hub port → stable ALSA name). Deferred until the full 6-mic arc is wired so the real hub topology can be read. Single-mic naming works today.

## Notes

- **Don't reimplement Paweł's Tyto protocol from scratch** — license is granted, his `msp.py` is the reference implementation. Calibration constants are *overridden at runtime* (see `server/core/calibration_override.py`) rather than edited in the vendored module.
- **Trigger-onset sync moves server-side** — UMIK-2s cannot be hardware-clock-locked. JS implementation was the reference for the Python port; legacy JS file is gone now.
- **Calibration constants** in `thrust_stand.py` (`HINGE_DISTANCE`, `CAL_POLES`, `CAL_*`) are correct for this user's specific 1585 unit. Exposed via `config.toml` for per-host overrides.
