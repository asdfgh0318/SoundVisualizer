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

### Prerequisites

| Platform | What you need |
|----------|---------------|
| **Linux** (Debian/Ubuntu) | `python3.12` + `python3.12-venv` · Node 22 (e.g. via `nvm` — `.nvmrc` is pinned) · `sudo apt install libportaudio2` |
| **macOS** | `brew install python@3.12 node portaudio` |
| **Windows** | Python 3.12 (python.org or `winget install Python.Python.3.12`) · Node 22 (nodejs.org or `winget install OpenJS.NodeJS.LTS`). Use PowerShell, not cmd. |

Hardware integration (Tyto Robotics serial protocol, ALSA udev rules, multi-mic capture pinning) is **Linux-tested only**. Frontend dev, fake captures, and the Results tabs (FFT/Polar/Custom) work fully on macOS and Windows.

### One-shot setup script

```bash
# Linux / macOS / WSL
git clone https://github.com/asdfgh0318/SoundVisualizer.git
cd SoundVisualizer
bash scripts/setup.sh
```

```powershell
# Windows PowerShell
git clone https://github.com/asdfgh0318/SoundVisualizer.git
cd SoundVisualizer
.\scripts\setup.ps1
```

The script: detects platform · checks prereqs (warns about missing PortAudio etc.) · creates the Python venv · installs server + frontend deps · runs the pytest suite · builds the frontend bundle. About 60 seconds on a warm cache.

### Run it

```bash
# Backend (terminal 1)
.venv/bin/uvicorn server.main:app --reload --port 8000          # Linux/macOS
.venv\Scripts\uvicorn.exe server.main:app --reload --port 8000  # Windows

# Frontend (terminal 2)
npm run dev          # → http://localhost:5173

# Populate demo data without any hardware
curl -X POST http://localhost:8000/dev/seed
# Or use the Capture form's "Run fake capture (no hardware)" button
```

### Manual install (skip the script)

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"
npm install
.venv/bin/pytest server/tests/    # 63 tests should pass
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
