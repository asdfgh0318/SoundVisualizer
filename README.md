# SoundVisualizer

Drone-propeller noise directivity measurement tool. Drives a Tyto Robotics 1585 thrust stand through a PWM ramp while recording audio from 6 miniDSP UMIK-2 microphones arranged on a vertical arc, then renders per-mic FFTs, elevation-polar SPL plots, and linked X/Y scatter views of derived quantities (SPL vs thrust, etc.).

For project context, architecture, and the phased plan, see [`CLAUDE.md`](CLAUDE.md) and [`PLAN.md`](PLAN.md). Original scope: [`2.md`](2.md).

## Architecture

```
┌──────────────────┐  HTTP + WS  ┌──────────────────────────────────────────┐
│  Laptop browser  │ ──────────► │  Laptop (dev) → RPi 5 (production)       │
│  React + Vite    │             │  Python 3.12 + FastAPI + asyncio         │
│  Plotly.js + ZS  │             │  ├─ Tyto 1585 (Paweł's MSP serial code)  │
└──────────────────┘             │  ├─ NOR-145 (Paweł's WS+FTP) [phase 6]   │
                                 │  ├─ 6× UMIK-2 (sounddevice + udev)       │
                                 │  ├─ Cutoff-trigger watchdog              │
                                 │  ├─ Capture-run orchestrator             │
                                 │  └─ Filesystem JSON+WAV measurement store│
                                 └──────────────────────────────────────────┘
```

Browser and server are decoupled. The server owns the hardware and the data on disk; the browser is a stateless thin client over REST + WebSocket.

## Pages

| Page | What it does |
|------|--------------|
| **Setup** | Lists detected ALSA `(hw:…)` audio devices · per-mic configuration (USB device + serial + single absolute elevation (free-text degrees in −90…+90, decimals OK) + optional UMIK-2 calibration file) · safety cutoffs (8 channels with tickbox + threshold + direction) · live Tyto connection status. |
| **🌳 Research tree** | Header link (when running on the Pi or on a host with the [`duct-research-tree`](https://github.com/asdfgh0318/duct-research-tree) editor on `:8123`) opens the tree editor in a new tab. Capture wizard surfaces an optional **Linked research-tree node** picker — pick a node, the key fields autofill from its geometry, and on a successful capture the SoundVis Results URL is pushed back into that node (status flips to *in-progress*). Configured under `[research_tree]` in `config.toml`. |
| **Capture** | Wizard: motor/propeller/shroud/notes form → editable PWM ramp with **live SVG visualization** → review summary → safety modal → **single-pass capture** (all mics record simultaneously; live progress + Tyto telemetry over WS) → done summary. **"Run fake capture (no hardware)"** button bypasses Tyto entirely and synthesizes drone-noise WAVs for results-tool dev. (Two-pass — physically remount mics between halves — is supported by the backend but not surfaced in the wizard yet.) |
| **Results — FFT** | Per-PWM-point page with performance header (PWM/thrust/torque/current/voltage/RPM/temp), scrollable per-mic FFT rows on a log-x axis. Settings popover for window/size/overlap. **Compare-configs overlay**: a series picker (config → PWM point → add) overlays additional measurements on top of the current one, matched by elevation — so each mic-position row shows one labelled, colored line per series. Cross-key (compare different propellers/shrouds) and cross-PWM; selection is transient and **shared with the Polar tab**. Warns when mixing calibrated (dB SPL) and uncalibrated (dBFS) series. |
| **Results — Polar** | Polar SPL-vs-elevation plot. 180°/360° render toggle. **Top+bottom merge** combines sibling captures at the same PWM into a single full-sphere view. Right rail: freq-band selector (manual range + 1/3-octave + octave snap-to). **Compare-configs overlay**: shares the FFT tab's series selection — each series becomes its own directivity curve, overlaid and color-matched. |
| **Results — Custom** | Plotly port of Paweł's Bokeh viz: X/Y scatter with column pickers (PWM / thrust / torque / current / voltage / RPM / temp / SPL-in-band) where each measurement point is clickable. Clicking a point also re-points the FFT and Polar tabs to that PWM step. |

## Quick start — pick your path

If you **just want to click around the UI**, use **path A** (Docker).
If you want to **edit the code, run tests, or work with real hardware**, use **path B** (dev environment).

---

### Path A — Demo only (Docker, no install)

For colleagues / reviewers / anyone evaluating the app. One command, ~5 minutes the first time, no Python or Node on your machine.

**Prereqs:** Docker (Desktop on macOS/Windows, `sudo apt install docker.io docker-compose-v2` on Linux).

```bash
git clone https://github.com/asdfgh0318/SoundVisualizer.git
cd SoundVisualizer
docker compose up                  # first build ~3-5 min, ~680 MB image
```

Open **http://localhost:8000**. You'll land on the **Setup** page — Tyto status shows "Not connected" and audio devices are empty; that's expected (the demo image intentionally has no hardware passthrough).

To populate test data:
1. Click **Capture** → fill in Motor `Demo` · Propeller `5x4` (others optional).
2. **Continue → Review → ✦ Run fake capture (no hardware)**.
3. Confirm the safety modal ("no motor will spin"). Wait ~5 s per half.
4. Go to **Results** — pick your key. Sidebar shows merged PWM points; the four tabs (FFT / Polar / Custom / Psychoacoustics) all work against the synthesized drone-noise data.

Captured data persists in `./data/` between restarts. To reset, `rm -rf data/`. To stop, `Ctrl+C` or `docker compose down`.

**Don't follow the Path B steps below if you just want to demo** — they install Python, Node, and PortAudio system-wide which you don't need.

---

### Path B — Dev environment (edit code, run tests, real hardware)

#### B.1 Prerequisites

| Tool | Check with | Install if missing |
|---|---|---|
| **Git** | `git --version` | Linux `sudo apt install git` · macOS `xcode-select --install` · Windows [git-scm.com](https://git-scm.com) |
| **Python 3.12+** | `python3.12 --version` (Linux/macOS) or `python --version` (Windows) | Linux `sudo apt install python3.12 python3.12-venv` · macOS `brew install python@3.12` · Windows `winget install Python.Python.3.12` |
| **Node 22+** | `node --version` | Linux/macOS: install [nvm](https://github.com/nvm-sh/nvm), then `nvm install 22` · Windows `winget install OpenJS.NodeJS.LTS` |

**Linux extra:** `sudo apt install libportaudio2` — needed for audio device enumeration.

Hardware integration (Tyto serial protocol, ALSA udev rules, multi-mic capture pinning) is Linux-tested only. The Results tabs work fully on all OSes.

#### B.2 Clone + one-shot setup

```bash
git clone https://github.com/asdfgh0318/SoundVisualizer.git
cd SoundVisualizer
bash scripts/setup.sh           # Linux / macOS / WSL
.\scripts\setup.ps1             # Windows PowerShell
```

The script: detects your OS, warns about missing system packages, creates `.venv/`, installs Python + npm deps, runs the pytest suite (76 tests should pass), builds the production bundle. Ends with `Setup complete!`.

#### B.3 Start the services (two terminals)

**Terminal 1 — backend:**
```bash
.venv/bin/uvicorn server.main:app --reload --port 8000           # Linux/macOS
.venv\Scripts\uvicorn.exe server.main:app --reload --port 8000   # Windows
```

**Terminal 2 — frontend (Vite dev with HMR):**
```bash
npm run dev
```

#### B.4 Open the app

**http://localhost:5173** — the Vite dev server proxies API calls to `:8000`. Setup page loads; Tyto shows "Not connected".

The fake-capture flow is the same as Path A above.

#### Manual install (skip the script)

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
npm install
.venv/bin/pytest server/tests/    # 76 tests should pass
npm run build                      # type-check + bundle
```

#### Common gotchas

| Symptom | Fix |
|---|---|
| `bash: scripts/setup.sh: Permission denied` | `chmod +x scripts/setup.sh` |
| Setup says `python3.12: command not found` but `python --version` shows 3.12+ | The script auto-fallbacks to `python` — re-run, it'll work |
| Backend logs `OSError: PortAudio library not found` on Linux | `sudo apt install libportaudio2` |
| Browser shows "Network Error" / red banners | Backend isn't running — check Terminal 1 |
| Setup page shows zero audio devices (Linux) | No real mics plugged in; the filter only shows ALSA `hw:…` devices. Fake capture still works. |
| Fake capture button is disabled | Fill in **Motor** + **Propeller** at minimum |
| `npm run dev` is slow / OOM | `node -v` should be 22+; older Node may misbehave |

For team workflow (branches, PRs, issues, the maintenance directive), see [CLAUDE.md](CLAUDE.md) → "Maintenance — standing instructions".

## With real hardware

1. Plug 6× UMIK-2 into a powered USB-2 hub. Each will appear as a new `(hw:N,0)` device in the Setup page audio device list.
2. Generate udev rules so ALSA card names are stable across reboots:
   ```bash
   .venv/bin/python scripts/generate_udev.py | sudo tee /etc/udev/rules.d/99-umik2.rules
   sudo udevadm control --reload && sudo udevadm trigger
   ```
3. Upload each mic's UMIK-2 calibration `.txt` file (Setup → "UMIK-2 calibration files"). Serial is auto-detected from the file header.
4. Plug the Tyto 1585 USB serial cable. Find the device with `ls /dev/ttyACM* /dev/ttyUSB*`.
5. Copy and edit the config:
   ```bash
   cp config.example.toml config.toml
   # In config.toml: set tyto.enabled = true and tyto.tty = "/dev/ttyACM0"
   ```
6. Restart the server. The Setup page should now show **Tyto stand · Connected, armed**.
7. Configure safety cutoffs in Setup (current, voltage, RPM, thrust, torque, temps) and **Push to Tyto**.
8. Add 5–6 mics on the Setup page — one row per UMIK-2, picking the matching USB device, serial, top and bottom elevations, and cal file.
9. Go to **Capture**, fill out motor/propeller/shroud/notes + PWM ramp + half selection → **Continue → Review → Start capture**.

## Deploy to a Raspberry Pi 5 (production rig)

The production target runs the same `server/` code as a `systemd` service on a
Raspberry Pi 5, serving the API + bundled UI on `http://soundvis.local:8000`.
One command on a fresh Pi:

```bash
git clone https://github.com/asdfgh0318/SoundVisualizer.git
cd SoundVisualizer
bash scripts/setup_rpi.sh
```

Full bring-up (PD supply, powered USB hub, mDNS, Tyto enable, operating the
service): **[`deploy/README.md`](deploy/README.md)**.

## Data layout

```
data/
  <motor>__<propeller>__<shroud>__<notes>/    # key dir, fields sluggified
    key.json                                  # { motor, propeller, shroud, notes }
    measurements/
      2026-05-12T09-39-48-105828__acoustic__top__mic-8100001/
        meta.json    # type, t_start, t_end, mic_serial, elevation_deg, half,
                     # pwm_setpoint, sample_rate, calibration_file_id
        audio.wav    # float32 IEEE_FLOAT, 48 kHz
      2026-05-12T09-39-48-105828__performance/
        meta.json    # type, t_start, t_end, pwm_setpoint
        telemetry.csv  # t_offset_s,thrust_n,torque_nm,current_a,voltage_v,rpm,
                       # temp0_c,temp1_c,temp2_c,vibration
```

One performance + N acoustic measurements per PWM step share the same `t_start`, which is how the Results page groups them into "PWM points".

## Tech stack

**Server:** Python 3.12 · FastAPI · uvicorn · `sounddevice` (PortAudio) · `pyserial-asyncio` · `numpy` · `scipy` (Welch PSD, filters) · `aiofiles` · `aioftp` + `websockets` (Norsonic, later).

**Client:** React 19 · Vite 7 · TypeScript · Tailwind 4 · Zustand 5 · Plotly.js (`plotly.js-dist-min`).

**Tests:** pytest (76 passing) covering FFT, calibration, trigger-sync alignment, cutoff watchdog, config loading, capture orchestrator with a fake stand, results endpoints, psychoacoustics. Lint via ruff.

## Acknowledgements

The Tyto Robotics MSP serial protocol and the Norsonic NOR-145 WebSocket+FTP control code were reverse-engineered by **Paweł Sadowski** in his [ars_noise_measurement](https://git.swarozyn.pl/mtj/ars_noise_measurement.git) repo and reused here with permission. See `server/vendor/pawel/README.md` for the per-file attribution.

Psychoacoustic metrics (loudness, sharpness, roughness, fluctuation strength, PA) are computed via [**MOSQITO**](https://github.com/Eomys/MoSQITo) by Green Forge Coop (BSD-licensed, ISO/DIN-compliant). If you publish results derived from this pipeline, please cite:

> Green Forge Coop. *MOSQITO* [Computer software]. https://doi.org/10.5281/zenodo.5284054

Use the *Cite this repository* button on the MOSQITO GitHub page for a release-specific citation.
