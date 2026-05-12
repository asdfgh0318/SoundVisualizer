# Plan — SoundVisualizer refactor

Living plan. See [CLAUDE.md](CLAUDE.md) for project context and locked decisions. Original scope in [2.md](2.md).

## Architecture

```
┌──────────────────┐  HTTP/WS  ┌─────────────────────────────────────────┐
│  Laptop browser  │ ────────► │  Laptop (now) → RPi 4 (later)           │
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
| 10 | RPi packaging | ⏳ Deferred | Waiting on RPi 4 delivery. Systemd unit, mDNS `soundvis.local`, FastAPI-served prod bundle, udev rules. README will document fresh-Pi setup (powered USB-2 hub, VL805 firmware update for bandwidth bug, 48 kHz cap). |

## Post-MVP enhancements delivered

These were not in the original 2.md scope but came up during development:

- **Realistic drone-noise synthesis** for `/dev/seed` and `/dev/fake_capture`: BPF + 11 harmonics + LF spreaded hump (around BPF) + HF broadband (1.5–5 kHz center). Elevation-dependent directivity per component (strong on BPF/harmonics, medium on LF, weak on HF). Matches the standard propeller-noise spectrum textbook breakdown.
- **Audio device filter** — only ALSA `(hw:…)` real devices shown (drops PulseAudio/PipeWire/SRC-plugin virtual entries).
- **Polar top+bottom merge** — when the sidebar-selected PWM point has a sibling capture at the same PWM µs but opposite half, the polar tab can combine both mic sets into a single -90°→+90° plot. Toggled by a checkbox; defaults on when sibling exists.
- **Refresh button** on the Results PWM-point sidebar to re-fetch from server after generating new data.

## Open questions

(none — all blockers cleared 2026-05-06)

## Notes

- **Don't reimplement Paweł's Tyto protocol from scratch** — license is granted, his `msp.py` is the reference implementation. Calibration constants are *overridden at runtime* (see `server/core/calibration_override.py`) rather than edited in the vendored module.
- **Trigger-onset sync moves server-side** — UMIK-2s cannot be hardware-clock-locked. JS implementation was the reference for the Python port; legacy JS file is gone now.
- **Calibration constants** in `thrust_stand.py` (`HINGE_DISTANCE`, `CAL_POLES`, `CAL_*`) are correct for this user's specific 1585 unit. Exposed via `config.toml` for per-host overrides.
