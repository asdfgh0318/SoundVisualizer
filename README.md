# SoundVisualizer

Drone-propeller noise directivity measurement tool. Drives a Tyto Robotics 1585 thrust stand through a PWM ramp while recording audio from 6 miniDSP UMIK-2 microphones arranged on a vertical arc, then renders per-mic FFTs, elevation-polar SPL plots, and linked X/Y scatter views of derived quantities (SPL vs thrust, etc.).

For project context, architecture, and the phased plan, see [`CLAUDE.md`](CLAUDE.md) and [`PLAN.md`](PLAN.md). Original scope: [`2.md`](2.md).

## Architecture

```
┌──────────────────┐  HTTP + WS  ┌──────────────────────────────────────────┐
│  Laptop browser  │ ──────────► │  Laptop (now) → RPi 4 (later)            │
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
| **Setup** | Lists detected ALSA `(hw:…)` audio devices · per-mic configuration (USB device + serial + top/bottom elevations + optional UMIK-2 calibration file) · safety cutoffs (8 channels with tickbox + threshold + direction) · live Tyto connection status. |
| **Capture** | Wizard: motor/propeller/shroud/notes form → editable PWM ramp with **live SVG visualization** → review summary → safety modal → top-half capture (live progress + Tyto telemetry over WS) → reconfigure-mics modal → bottom-half capture → done summary. Top-only / bottom-only checkboxes for partial reruns. **"Run fake capture (no hardware)"** button bypasses Tyto entirely and synthesizes drone-noise WAVs for results-tool dev. |
| **Results — FFT** | Per-PWM-point page with performance header (PWM/thrust/torque/current/voltage/RPM/temp), scrollable per-mic FFT rows on a log-x axis. Settings popover for window/size/overlap. |
| **Results — Polar** | Polar SPL-vs-elevation plot. 180°/360° render toggle. **Top+bottom merge** combines sibling captures at the same PWM into a single full-sphere view. Right rail: freq-band selector (manual range + 1/3-octave + octave snap-to). |
| **Results — Custom** | Plotly port of Paweł's Bokeh viz: X/Y scatter with column pickers (PWM / thrust / torque / current / voltage / RPM / temp / SPL-in-band) where each measurement point is clickable. Clicking a point also re-points the FFT and Polar tabs to that PWM step. |

## Quick start

Walks a colleague from "fresh laptop" to "app running with fake data" in ~5 minutes. No hardware needed.

### 1. Check prerequisites

You need three things on PATH:

| Tool | Check with | Install if missing |
|---|---|---|
| **Git** | `git --version` | Linux `sudo apt install git` · macOS `xcode-select --install` · Windows [git-scm.com](https://git-scm.com) |
| **Python 3.12+** | `python3.12 --version` (Linux/macOS) or `python --version` (Windows) | Linux `sudo apt install python3.12 python3.12-venv` · macOS `brew install python@3.12` · Windows `winget install Python.Python.3.12` |
| **Node 22+** | `node --version` | Linux/macOS: install [nvm](https://github.com/nvm-sh/nvm), then `nvm install 22` · Windows `winget install OpenJS.NodeJS.LTS` |

**Linux extra:** `sudo apt install libportaudio2` — needed for audio device enumeration.

Hardware integration (Tyto serial protocol, ALSA udev rules, multi-mic capture pinning) is Linux-tested only. Frontend dev, fake captures, and all Results tabs work fully on macOS and Windows.

### 2. Clone

```bash
git clone https://github.com/asdfgh0318/SoundVisualizer.git
cd SoundVisualizer
```

### 3. One-shot setup

```bash
bash scripts/setup.sh           # Linux / macOS / WSL
.\scripts\setup.ps1             # Windows PowerShell
```

The script: detects your OS, warns about missing system packages, creates `.venv/`, installs Python + npm deps, runs the pytest suite (68 tests should pass), and builds the production bundle. Ends with `Setup complete!` and the run commands.

### 4. Start the services

**Terminal 1 — backend:**
```bash
.venv/bin/uvicorn server.main:app --reload --port 8000           # Linux/macOS
.venv\Scripts\uvicorn.exe server.main:app --reload --port 8000   # Windows
```
You should see `Uvicorn running on http://127.0.0.1:8000`.

**Terminal 2 — frontend:**
```bash
npm run dev
```
You should see `VITE … ready` and `Local: http://localhost:5173/`.

### 5. Open the app

Navigate to **http://localhost:5173**. You'll land on the **Setup** page. Tyto status will read "Not connected" — that's expected with no hardware.

### 6. Try a fake capture (no hardware required)

1. Click **Capture** in the nav.
2. Fill in: Motor `Demo Motor` · Propeller `5x4` · Shroud `none` · Notes `first-test`.
3. The PWM ramp comes pre-filled with 3 steps (1200 / 1500 / 1800 µs). Leave it.
4. Click **Continue → Review** → **✦ Run fake capture (no hardware)**.
5. Confirm the safety modal ("no motor will spin"). Wait ~5 s for top half, then click the reconfigure modal to continue to bottom half.
6. Land on the **Done** summary.

Now click **Results** and pick your `demo-motor__5x4__none__first-test` key. You should see:

- **Sidebar:** 3 merged PWM points (each tagged `T+B`). Click `▸ 2 captures` to drill into a specific half.
- **FFT tab:** one row per unique elevation, showing the synthesized blade-pass tone + harmonics + broadband.
- **Polar tab:** directivity bubble that grows with PWM. Try the **1k Hz** or **2k Hz** 1/3-octave preset.
- **Custom tab:** X = Thrust, Y = SPL band → 3 dots on a curve. Click one to drill into its FFT.

You're set. To work with real hardware later, see **[With real hardware](#with-real-hardware)** below.

### Common gotchas

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

### Manual install (skip the script)

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
npm install
.venv/bin/pytest server/tests/    # 68 tests should pass
npm run build                      # type-check + bundle
```

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

**Tests:** pytest (58 passing) covering FFT, calibration, trigger-sync alignment, cutoff watchdog, config loading, capture orchestrator with a fake stand, results endpoints. Lint via ruff.

## Acknowledgements

The Tyto Robotics MSP serial protocol and the Norsonic NOR-145 WebSocket+FTP control code were reverse-engineered by **Paweł Sadowski** in his [ars_noise_measurement](https://git.swarozyn.pl/mtj/ars_noise_measurement.git) repo and reused here with permission. See `server/vendor/pawel/README.md` for the per-file attribution.
