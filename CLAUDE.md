# SoundVisualizer

Drone-noise directivity measurement tool. Captures audio from up to 6 miniDSP UMIK-2 mics arranged on a vertical arc plus thrust/torque/current telemetry from a Tyto Robotics 1585 stand, computes per-mic FFT and elevation-polar SPL plots, optionally adds Norsonic NOR-145 SLM data.

## Status

**Refactor MVP is built.** Phases 0/1/2/3/4/5/7/8/9/10 of [PLAN.md](PLAN.md) are complete. Server + frontend run end-to-end against either real hardware (when `tyto.enabled = true` in `config.toml`) or against synthesised "fake capture" data for results-tool development without the rig.

Remaining phases:
- **Phase 6 — Norsonic NOR-145**: hardware pending delivery. Paweł's `norsonic*.py` is vendored and dormant in `server/vendor/pawel/`.

Production deployment (Phase 10) targets a **Raspberry Pi 5** (running Debian 13 Trixie, hostname `jama`, reachable at `jama.local:8000`). Deploy from the laptop with `scripts/deploy_to_pi.sh jama@jama.local` (builds the bundle locally, ships it, runs `scripts/setup_rpi.sh` on the Pi). Native systemd (`deploy/soundvis.service`), **system Python 3.13** (Trixie ships it; all deps have aarch64 wheels, so no pyenv/compile), FastAPI-served bundle on :8000. See [deploy/README.md](deploy/README.md). The instance is live.

Reference docs: [PLAN.md](PLAN.md) · [2.md](2.md) (original scope) · [1.md](1.md) (kickoff) · [docs/overview.html](docs/overview.html).

## Hardware

| Device | Status | Notes |
|--------|--------|-------|
| 6× UMIK-2 USB mics | Available | Plug into laptop USB hub. Setup page filters audio devices to ALSA `(hw:…)` only. |
| Tyto Robotics 1585 thrust stand | Available | USB serial, driven via Paweł's MSP protocol code. |
| Norsonic NOR-145 SLM | Pending delivery | WiFi when delivered; phase 6. |
| Raspberry Pi 5 | Available, **deployed & live** | Debian 13 Trixie, hostname `jama` → `http://jama.local:8000`. Native systemd service running on system Python 3.13. Deploy/update from the laptop via `scripts/deploy_to_pi.sh jama@jama.local`. SSH alias `ssh jama` (passwordless key). (Replaced the originally-planned RPi 4; the Pi 5's RP1 chip has real USB 3.0, so no VL805 bandwidth workaround.) **Integration-tested on the Pi:** 1× UMIK-2 enumerates + captures, Tyto on `/dev/ttyUSB0` connects + streams telemetry + cutoff watchdog + a full capture run all verified. Note: UMIK-2s report USB serial `00000` (so multi-mic udev naming needs port-paths, not serials); temps unused; ESC/battery not yet connected (no powered/prop run done). |

Laptop is Linux (kernel 6.8). Same Python server runs on the RPi 5 with no code change — only the host moves.

## Running it

```bash
# Backend
.venv/bin/uvicorn server.main:app --reload --port 8000

# Frontend (separate terminal)
npm run dev
# → http://localhost:5173

# Populate demo data without hardware
curl -X POST http://localhost:8000/dev/seed
# Or use the Capture form's "Run fake capture (no hardware)" button
```

Tests: `.venv/bin/pytest server/tests/` (76 passing). Lint: `.venv/bin/ruff check server/ scripts/`.

Demo via Docker (no install needed): `docker compose up` → http://localhost:8000. Multi-stage Dockerfile bundles the React build into FastAPI's static mount; no hardware passthrough.

## Locked decisions

- **No azimuth measurement.** Tested objects are rotationally symmetric around the vertical axis. Elevation is the only varying spatial dimension. The 360° polar plot is a cosmetic mirror of the measured arc.
- **6 mics, 2 physical configurations** ("top half" / "bottom half"), both user-defined per-mic in Setup. The user manually re-mounts mics between top and bottom captures. No hardcoded "0° stays fixed" or paired-mic assumption — pairing is whatever the user enters.
- **Filesystem JSON+WAV store**, no SQL. Keys are `motor__propeller__shroud__notes` directories under `data/`. Per-measurement layout: `meta.json` + `audio.wav` (acoustic) or `telemetry.csv` (performance) or `norsonic.{txt,json}` (NOR data — later).
- **Paweł Sadowski's [ars_noise_measurement](https://git.swarozyn.pl/mtj/ars_noise_measurement.git) code is ours** to copy/edit (full permission, 2026-05-06). Vendored in `server/vendor/pawel/` (`msp.py`, `async_serial.py`, `thrust_stand.py` for Tyto; `norsonic*.py` for NOR-145). Calibration constants in `thrust_stand.py` are *overridden at runtime* from `config.toml` via `server/core/calibration_override.py`.
- **Cutoff triggers:** all eight (current, voltage, RPM, thrust, torque, temp0, temp1, temp2) — each tickbox-enabled with a numeric threshold and an above/below direction. Server-side watchdog reads `PollResponse` at ~33 Hz and slams `mot_pwm = 1000` on any trip; latched until reset.
- **FFT defaults:** Hann window, 4096 size, 50% overlap, log-x 20 Hz–24 kHz, dBSPL after UMIK calibration applied (dBFS fallback if no cal file uploaded). Welch PSD via `scipy.signal.welch`.
- **Sample rate:** 48 kHz (RPi 4 USB bandwidth makes 96 kHz unsafe with 6 mics; sufficient for drone-noise band 100 Hz–20 kHz).
- **PWM step model:** each step carries its own `recording_ms` (the audio capture duration at that PWM). Total recording per half is `sum(step.recording_ms)`. Stabilization time is automatic (server `stabilize_rpm` waits for RPM to settle within tolerance).

## Tech stack

**Server (`server/`):** Python 3.12 + FastAPI + asyncio. `sounddevice` (PortAudio) for UMIK-2 capture · `pyserial-asyncio` for Tyto MSP · `aioftp` + `websockets` for Norsonic (later) · `numpy` + `scipy` for FFT/Welch/calibration · `aiofiles` for the measurement store · `mosqito` for psychoacoustic SQM/PA computation.

**Client (`src/`):** React 19 + Vite 7 + TypeScript + Tailwind 4 + Zustand 5 + Plotly.js.

**Third-party attribution:** Psychoacoustic metrics are computed with [MOSQITO](https://github.com/Eomys/MoSQITo) (Green Forge Coop, BSD). When publishing results derived from those metrics, cite: *Green Forge Coop. MOSQITO [Computer software]. https://doi.org/10.5281/zenodo.5284054* (use GitHub's "Cite this repository" button for the release-pinned form).

## Conventions

- Don't add comments unless the *why* is non-obvious. No docstring bloat.
- Don't pre-build for hypothetical features. MVP target is laptop + UMIKs + Tyto; Norsonic and RPi packaging are deferred phases — don't write code for them now.
- `server/vendor/pawel/` is treated as upstream — modifications limited to package-relative import fixes (see `server/vendor/pawel/README.md`). Calibration overrides happen in `server/core/calibration_override.py`, not in the vendored module.
- Server-side trigger-onset sync is the chosen mic-alignment strategy — UMIK-2s cannot be hardware-clock-locked.
- For UI changes, dev server is `npm run dev` (frontend) + `uvicorn server.main:app --reload` (backend on `:8000`).
- The `/dev/seed` and `/dev/fake_capture` endpoints synthesize realistic propeller noise (BPF + harmonics + LF spreaded + HF broadband, with elevation-dependent directivity) so the Results tools can be developed and demoed without the rig.

## Maintenance — standing instructions

The user has standing approval to do the following at natural break points (e.g. after finishing a phase, fixing a bug that crossed several files, adding a feature, or whenever docs and code drift):

**1. Keep the following five files coherent with the current state of the code:**

| File | Should reflect |
|------|----------------|
| `CLAUDE.md` (this file) | Status banner, hardware availability, locked decisions, conventions, **anything you wish a fresh Claude session would know** |
| `PLAN.md` | Phase table with ✅/⏳ status, post-MVP enhancements list, open questions |
| `README.md` | What the project is, page surfaces, quick start, real-hardware bring-up, data layout, attribution |
| `server/README.md` | Module layout, route inventory, conventions, test count |
| `docs/overview.html` | Status pill, phase badges, hardware availability table |

When code lands that adds a feature, changes a schema, or completes/defers a phase, also update whichever of the five docs above is now stale. The user does *not* want to be asked each time — just do it as part of the same edit batch.

**2. Commit + push to GitHub.** The remote is `origin → https://github.com/asdfgh0318/SoundVisualizer.git`. After a coherent chunk of work + updated docs:
- Stage the specific files (not blanket `git add .` — review what changed first).
- Write a concise commit message describing the *why*, not just *what*.
- `git push origin main` to the remote.
- Skip commits when the change is purely exploratory (no code/doc change), or when the working tree is already pristine.

The standard Anthropic safety rules still apply: don't commit secrets, don't `--no-verify`, don't force-push to `main`, don't amend the initial commit. Treat `data/` and `config.toml` as gitignored (already configured).

**3. Track future work as GitHub issues.** Before starting non-trivial new work (a feature, a bug fix that spans files, a phase, an experiment), create a GitHub issue describing it:
- `gh issue create --title "..." --body "..."` (auth via `gh auth status`).
- One issue per logical unit. Include scope, what's in/out, and acceptance criteria.
- Reference the issue in the relevant commit messages (`closes #N`) so GitHub auto-links them and closes the issue on merge to `main`.
- Quick bug fixes, doc tweaks, and small one-off changes don't need an issue.

**4. Rebuild the demo Docker image after every code-touching commit.** The demo image bakes the React bundle in at build time (`COPY --from=frontend-build /app/dist /app/static`), so old images serve stale UI. After pushing a commit that touches `src/`, `server/`, `package*.json`, `pyproject.toml`, `index.html`, `vite.config.ts`, `tsconfig*.json`, `Dockerfile`, or `config.example.toml`:
- `sudo docker compose build` (rebuilds Stage 1 / Stage 2 with current source).
- Verify the rebuild succeeded; you don't need to start the container unless the user asks.
- Skip the rebuild for docs-only commits (CLAUDE.md, PLAN.md, README.md, docs/), commits touching only `.gitignore` / `.dockerignore` exclusions, or test-only commits in `server/tests/` that don't change runtime behaviour.
- The image is local-only (no registry push). Anyone cloning the repo gets a fresh build on their first `docker compose up`, so this step is for *your* local demo to stay current — not a release artifact.
