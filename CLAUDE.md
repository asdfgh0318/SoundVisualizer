# SoundVisualizer

Drone-noise directivity measurement tool. Captures audio from up to 6 miniDSP UMIK-2 mics arranged on a vertical arc plus thrust/torque/current telemetry from a Tyto Robotics 1585 stand, computes per-mic FFT and elevation-polar SPL plots, optionally adds Norsonic NOR-145 SLM data.

## Status

**Refactor MVP is built.** Phases 0/1/2/3/4/5/7/8/9/10 of [PLAN.md](PLAN.md) are complete. Server + frontend run end-to-end against either real hardware (when `tyto.enabled = true` in `config.toml`) or against synthesised "fake capture" data for results-tool development without the rig.

Remaining phases:
- **Phase 6 — Norsonic NOR-145**: hardware pending delivery. Paweł's `norsonic*.py` is vendored and dormant in `server/vendor/pawel/`.

Production deployment (Phase 10) targets a **Raspberry Pi 5** (running Raspberry Pi OS (Debian 13 trixie base), hostname `sound-viz`, reachable at `sound-viz.local:8000`; user `pi`, password `dupa`). Deploy from the laptop with `scripts/deploy_to_pi.sh pi@sound-viz.local` (builds the bundle locally, ships it, runs `scripts/setup_rpi.sh` on the Pi). Native systemd (`deploy/soundvis.service`), **system Python 3.13** (Trixie ships it; all deps have aarch64 wheels, so no pyenv/compile), FastAPI-served bundle on :8000. See [deploy/README.md](deploy/README.md). The instance is live. (Reflashed 2026-07-22 after a second SD-card death — previous identity was hostname `jama`, user `jama`. The laptop SSH aliases `jama` / `soundvis-pi` / `sound-viz` all point at the new identity.) **Immutable-rootfs design (live since 2026-07-24):** the SD card is partitioned `boot 512M | rootfs 4.5G | data 2.4G (ext4, LABEL=data)`. The rootfs runs under **overlayroot** (`overlayroot=tmpfs:recurse=0` in `/boot/firmware/cmdline.txt`) — all rootfs writes go to RAM and vanish on reboot, so SD corruption (which killed two cards) is impossible. The **data partition is the only persistent storage**: mounted at `/home/pi/data`, with `~/SoundVisualizer/data → /home/pi/data/measurements`, `~/SoundVisualizer-data → /home/pi/data/backup-repo`, and `~/SoundVisualizer/config.toml → /home/pi/data/config.toml` symlinks — so measurements, the GitHub backup clone, AND the server config (incl. Tyto calibration) survive reboots and are editable without the overlay ceremony. Swap is zram-only (`/etc/rpi/swap.conf.d/99-zram-only.conf`; the 2G `/var/swap` file was removed to fit the shrunk rootfs).
  - **To change anything persistent** (packages, udev, config.toml, systemd units): `sudo raspi-config nonint do_overlayfs 1` + reboot (disables overlay, rootfs rw), make the change, re-enable + reboot.
  - **CRITICAL gotcha:** re-enabling overlay via raspi-config writes plain `overlayroot=tmpfs` — you MUST re-append `:recurse=0` in `/boot/firmware/cmdline.txt` afterwards, or overlayroot will stack a RAM overlay over the data partition too (mounts it ro underneath → measurements silently become ephemeral). The boot partition stays writable, so this edit needs no overlay toggle.
  - Cutoffs + tare are runtime state and reset every boot regardless of overlay — re-push cutoffs before any powered run.

Reference docs: [PLAN.md](PLAN.md) · [2.md](2.md) (original scope) · [1.md](1.md) (kickoff) · [docs/overview.html](docs/overview.html).

## Hardware

| Device | Status | Notes |
|--------|--------|-------|
| 6× UMIK-2 USB mics | Available | Plug into laptop USB hub. Setup page filters audio devices to ALSA `(hw:…)` only. |
| Tyto Robotics 1585 thrust stand | Available | USB serial, driven via Paweł's MSP protocol code. |
| Norsonic NOR-145 SLM | Pending delivery | WiFi when delivered; phase 6. |
| Raspberry Pi 5 | Available, **deployed & live** | Raspberry Pi OS (Debian 13 trixie base), hostname `sound-viz` → `http://sound-viz.local:8000`. Native systemd service running on system Python 3.13. Deploy/update from the laptop via `scripts/deploy_to_pi.sh pi@sound-viz.local`. SSH alias `ssh jama` (passwordless key; also `ssh sound-viz`). (Replaced the originally-planned RPi 4; the Pi 5's RP1 chip has real USB 3.0, so no VL805 bandwidth workaround.) **Integration-tested on the Pi** with 4× UMIK-2 + Tyto: mics enumerate + capture, Tyto on `/dev/ttyUSB0` connects + streams telemetry + cutoff watchdog + full capture run + tare all verified. UMIK-2s report USB serial `00000`, so `generate_udev.py` names them by **USB port path** (`umik_3_1_4_1`…) and the device picker shows that `alsa_card_id`; the live level meter is the physical-identify tool. Temps unused. ESC/battery not yet connected (no powered/prop run done). **Power lesson:** run mics off a self-powered USB hub — hanging everything off the Pi's ports once brown-outed it and corrupted the SD card (recovered by reflash + `setup_rpi.sh`). |

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

Tests: `.venv/bin/pytest server/tests/` (101 passing). Lint: `.venv/bin/ruff check server/ scripts/`.

Demo via Docker (no install needed): `docker compose up` → http://localhost:8000. Multi-stage Dockerfile bundles the React build into FastAPI's static mount; no hardware passthrough.

## Locked decisions

- **No azimuth measurement.** Tested objects are rotationally symmetric around the vertical axis. Elevation is the only varying spatial dimension. The 360° polar plot is a cosmetic mirror of the measured arc.
- **Single-pass capture is the default.** Each mic has one absolute elevation (−90…+90°) and all configured mics record simultaneously in one run; `MeasurementHalf.FULL` labels the resulting measurements. The backend still accepts `half="top"`/`"bottom"` (legacy + future two-pass clients), so existing two-pass data renders unchanged; the wizard just doesn't drive that flow today.
- **Filesystem JSON+WAV store**, no SQL. Keys are `motor__propeller__shroud__notes` directories under `data/`. Per-measurement layout: `meta.json` + `audio.wav` (acoustic) or `telemetry.csv` (performance) or `norsonic.{txt,json}` (NOR data — later).
- **Tyto serial port: use the stable by-id path**, not `/dev/ttyUSBn`. A replug re-enumerates the FTDI to a new node while the running service keeps the dead handle — the poll loop stalls silently (`connected: true` stays stale, telemetry stops, and PWM stops being transmitted since it rides on each poll). `config.toml` uses `tty = "/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_D30F775I-if00-port0"`. Symptom to recognise: "Tyto not outputting PWM" + empty `/tyto/ws/telemetry`.
- **Thrust calibration verified against a 200.0 g reference (2026-07-24):** Paweł's `cal_thrust` read 4.3% low on our rig; corrected iteratively to `cal_thrust = -1.0019910071` (final check: 200.30 g read for a 200.00 g weight, +0.15%). Lives in `[tyto.calibration]` of the Pi's `config.toml` (on the data partition). Method: tare empty → place reference weight → read absolute; iterate the scale factor.
- **Paweł Sadowski's [ars_noise_measurement](https://git.swarozyn.pl/mtj/ars_noise_measurement.git) code is ours** to copy/edit (full permission, 2026-05-06). Vendored in `server/vendor/pawel/` (`msp.py`, `async_serial.py`, `thrust_stand.py` for Tyto; `norsonic*.py` for NOR-145). Calibration constants in `thrust_stand.py` are *overridden at runtime* from `config.toml` via `server/core/calibration_override.py`.
- **Cutoff triggers:** all eight (current, voltage, RPM, thrust, torque, temp0, temp1, temp2) — each tickbox-enabled with a numeric threshold and an above/below direction. Server-side watchdog reads `PollResponse` at ~33 Hz and slams `mot_pwm = 1000` on any trip; latched until reset.
- **Auto-tare per run:** the orchestrator re-zeros the stand once at the top of every capture run, while the motor is still at idle (PWM=1000). Eliminates load-cell drift bleeding into thrust/torque/current readings. Not re-taring between PWM steps — that'd force a spool-down/up per step and isn't worth the wear/time. Manual `POST /tyto/zero` still works for ad-hoc taring outside of a run.
- **Tyto serial auto-reconnect:** the FT231X USB link drops and re-enumerates on its own (seen on the rig, 2026-07-27). The service treats "poll raised" *or* "no sample within 1 s" as a dead link, tears it down and reopens `config.tyto.tty` with escalating backoff (0.5/1/2/5 s, forever). PWM always comes back at **1000** — a reconnect never resumes a live throttle. Tare offsets, cutoff config and the trip latch survive. `GET /tyto/status` reports live state via `link_state` (`absent` = not configured, `connected`, `reconnecting`) and the telemetry WS emits a `{connected: false, link_error}` frame on the drop. A capture run in flight is **failed** (not silently continued) — without the poll stream there's no telemetry, no PWM transmission and no cutoff watchdog. Because `MSPSlave.open_connection` blocks the event loop forever waiting for the board's `Ready` banner, the open handshake lives in `thrust_stand_service.open_stand` (bounded, run in a thread) instead of the vendored one.
- **Multi-tree research-tree integration:** SoundVis supports any number of [research-tree](https://github.com/asdfgh0318/duct-research-tree)-style editors as companion services. Configured via repeated `[[research_trees]]` tables in `config.toml`. On the Pi: [`duct-research-tree`](https://github.com/asdfgh0318/duct-research-tree) on `:8123` (single-duct work), [`drone-paczek-research-tree`](https://github.com/asdfgh0318/drone-paczek-research-tree) on `:8124` (parcel-drone material studies). Node IDs are unique across trees by prefix (`p1-*` for duct, `dp1-*` for drone-paczek), which is how the backend routes a capture-completion push to the right tree. The legacy singular `[research_tree]` table still loads (folds into a one-entry list). Adding more trees later: clone the repo, append a `[[research_trees]]` entry + a systemd unit (see `scripts/setup_rpi.sh`'s `RESEARCH_TREES` array).
- **Measurement-data backup to GitHub:** the Pi mirrors `~/SoundVisualizer/data/` to the private repo [`asdfgh0318/SoundVisualizer-data`](https://github.com/asdfgh0318/SoundVisualizer-data) every 15 min via `soundvis-backup.timer` → `scripts/backup_data.sh`. Auth is a per-repo SSH deploy key on the Pi (`~/.ssh/id_soundvis_data`) gated through the `Host github-data` SSH alias. Introduced after losing all measurements to a corrupted SD card on 2026-06-25 — one SD failure should never again take data with it. `setup_rpi.sh` installs the timer; the deploy key has to be created + registered with the repo by hand on first deploy.
- **FFT defaults:** Hann window, 4096 size, 50% overlap, log-x 20 Hz–24 kHz, dBSPL after UMIK calibration applied (dBFS fallback if no cal file uploaded). Welch PSD via `scipy.signal.welch`.
- **Absolute dB SPL conversion:** `SPL = level_dBFS - sens_factor_db + 94`. The UMIK Sens Factor is the dBFS the mic reports when driven by a 94 dB SPL (1 Pa) calibrator, quoted under REW's convention that a full-scale sine is **−3.01 dBFS**, not 0 — which our Welch `scaling="density"` + band integration already reproduces, so no ±3.01 fudge anywhere. **AGain is deliberately not added**: the Sens Factor already accounts for the mic's internal gain, AGain only records which analog-gain setting it is valid at. A cal file with a response curve but **no** Sens Factor cannot give absolute levels — `FFTResponse.calibrated` then stays `true` (cal applied) while `absolute_spl` is `false`, and the UI labels those axes `dBFS`, never `dB SPL`.
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
