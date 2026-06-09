# SoundVisualizer Server

Python 3.12 + FastAPI + asyncio. Drives 6× UMIK-2 + Tyto Robotics 1585 + (later) Norsonic NOR-145. Filesystem JSON+WAV measurement store.

For overall project context see [`../CLAUDE.md`](../CLAUDE.md) and [`../PLAN.md`](../PLAN.md).

## Quick start

```bash
cd /home/adam/ŻYCIE/PRACA/SoundVisualizer
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn server.main:app --reload --port 8000
# → http://localhost:8000/health
# → http://localhost:8000/docs   (OpenAPI / Swagger)
```

Tests: `pytest server/tests/`. Lint: `ruff check server/ scripts/`.

## Layout

```
server/
  main.py            # FastAPI app entry + lifespan (boots Tyto service & orchestrator); SPA fallback when SOUNDVIS_STATIC set
  __main__.py        # `python -m server` — prod entrypoint, reads [server] host/port from config (used by the RPi systemd unit)
  api/               # HTTP + WS route handlers
    keys.py            # /keys CRUD
    measurements.py    # /keys/{slug}/measurements
    devices.py         # /devices/audio (hw-only filter)
    calibration.py     # /calibrations upload + list
    capture.py         # /capture/acoustic (single-shot, no Tyto)
    capture_run.py     # /capture/run (orchestrated PWM-ramp + mics + WS)
    thrust_stand.py    # /tyto/{status,pwm,cutoffs,reset,ws/telemetry}
    results.py         # /keys/{slug}/{pwm_points, .../fft, .../performance_summary, .../psychoacoustics}
    setup_presets.py   # /setup-presets — named mic-list snapshots
    compat_tolerances.py # /compat-tolerances — PWM-point merge tolerances
    dev.py             # /dev/{seed, fake_capture} — synthetic drone-noise data
  core/              # Hardware orchestration + signal processing
    audio_devices.py   # sounddevice device enumeration (hw: only)
    capture.py         # multi-stream capture
    trigger_sync.py    # dBFS onset alignment (port from src/audio/triggerSync.ts)
    wav.py             # float32 WAV read/write via scipy
    fft.py             # Welch PSD → dB
    calibration.py     # REW-format UMIK-2 cal parser + spectrum correction
    cutoff_watchdog.py # Tyto safety latching
    thrust_stand_service.py  # owns the Tyto connection + sample stream
    capture_orchestrator.py  # per-half PWM-ramp capture loop
    calibration_override.py  # applies config.toml to Paweł's vendored constants
    config.py          # Pydantic config loader (config.toml) — [server], [tyto]
    psychoacoustics.py # mosqito loudness/sharpness/roughness + Zwicker PA
  store/             # Filesystem JSON+WAV persistence
    paths.py keys.py measurements.py calibration.py
    setup_presets.py compat_tolerances.py psychoacoustics.py
  vendor/pawel/      # Vendored — Paweł's Tyto MSP + Norsonic protocol code
  tests/             # 76 passing tests
```

## Conventions

- `server/vendor/pawel/` is treated as upstream — modifications limited to package-relative import fixes (documented in `vendor/pawel/README.md`). Calibration overrides happen in `server/core/calibration_override.py`, not inside the vendored module.
- Hardware modules behind narrow interfaces in `core/`. The watchdog wraps the Tyto poll loop, not the other way around. The orchestrator wraps both.
- Type-hint everything Python 3.12-style (`list[str]`, `int | None`, `dict[str, X]`). Pydantic for any data crossing the API boundary.
- No comments unless the *why* is non-obvious. No docstring bloat.

## Endpoints (17 routes)

```
GET  /health
GET  /devices/audio
GET  /calibrations
POST /calibrations             (multipart UMIK-2 .txt upload)
GET  /setup-presets
POST /setup-presets
GET  /setup-presets/{id}
DELETE /setup-presets/{id}
GET  /keys
POST /keys
GET  /keys/{slug}
GET  /keys/{slug}/measurements
POST /keys/{slug}/measurements
GET  /keys/{slug}/measurements/{id}
GET  /keys/{slug}/pwm_points
GET  /keys/{slug}/measurements/{id}/fft
GET  /keys/{slug}/measurements/{id}/performance_summary
POST /capture/acoustic         (single-shot, no Tyto)
POST /capture/run              (orchestrated PWM-ramp capture)
GET  /capture/run
DELETE /capture/run            (abort, slams PWM=1000)
WS   /capture/run/ws           (live capture status stream)
GET  /tyto/status
POST /tyto/pwm
POST /tyto/cutoffs
POST /tyto/reset
WS   /tyto/ws/telemetry        (~33 Hz Tyto poll stream)
POST /dev/seed                 (creates a demo key with synthetic drone-noise data)
POST /dev/fake_capture         (real capture-run body, bypasses hardware)
```
