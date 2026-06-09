# Deploying to a Raspberry Pi 5

Production target for the rig. The Pi runs the **same** `server/` code as the
laptop — only the host moves. One `systemd` service serves both the API and the
prebuilt React bundle on port 8000, reachable on the LAN at
`http://<hostname>.local:8000` (our unit is `jama`, so `http://jama.local:8000`).

> The browser-only demo path (`docker compose up`) is unrelated to this and
> stays as-is for hardware-free UI testing. This document is the **real rig**.

## What the Pi actually runs

Our Pi 5 runs **Debian 13 (Trixie)**, which ships **Python 3.13**. The project
requires Python ≥ 3.12, so we use the **system interpreter directly — no pyenv,
no CPython compile.** All Python deps (numpy, scipy, mosqito, matplotlib …)
install from prebuilt aarch64 wheels.

> On an older **Bookworm** image (Python 3.11) the system interpreter is too old.
> Either flash a Trixie-based image, or install 3.12+ via pyenv and point the
> venv at it — `setup_rpi.sh` fails fast with a clear message in that case.

## Hardware checklist

| Item | Why it matters |
|------|----------------|
| **Raspberry Pi 5** (4 GB+), 64-bit Pi OS (Debian 13 Trixie) | Target platform. RP1 I/O chip has real USB 3.0 — no VL805 bandwidth bug, unlike the Pi 4. |
| **5V / 5A USB-C PD supply** (official 27 W) | Without PD negotiation the Pi 5 caps downstream USB at 600 mA and warns. |
| **Powered USB hub** for the 6× UMIK-2 | Bus-powered mics + a passive hub will brown out. Always power the hub. |
| SD card 8 GB+ (16 GB+ comfortable) | The venv is ~400 MB. On a small card, build the bundle on a dev machine and ship it (below) so the Pi never needs Node. |

## Recommended: deploy from a dev machine

Build the React bundle on your laptop and ship the repo + `dist/` to the Pi.
The Pi never installs Node — best for small SD cards. One command from the repo
root on the laptop:

```bash
scripts/deploy_to_pi.sh jama@jama.local      # or jama@<pi-ip>
```

It builds `dist/` locally, rsyncs the source + bundle to `~/SoundVisualizer` on
the Pi, then runs `scripts/setup_rpi.sh` there. Re-runnable: rsync only sends
changed files. Auth uses your normal ssh (set up a key, or get prompted).

## Alternative: install directly on the Pi

```bash
# On the Pi, as the normal user (e.g. 'jama'), NOT root:
git clone https://github.com/asdfgh0318/SoundVisualizer.git
cd SoundVisualizer
bash scripts/setup_rpi.sh
```

What `setup_rpi.sh` does (idempotent — safe to re-run after `git pull`):

1. **apt deps** — PortAudio, avahi (mDNS), git, `python3-venv`.
2. **`.venv` + `pip install -e .`** with the system Python (≥ 3.12 required).
3. **Frontend (dist-aware)** — if `dist/` is already present (shipped from a dev
   machine) it's used as-is; otherwise the script installs Node 22 and builds it
   on-device.
4. **`config.toml`** from the example (if not already present).
5. **udev rules** for stable UMIK-2 ALSA names (best-effort; re-run once mics are
   plugged in if none were detected).
6. **systemd unit** installed, enabled, started — then a local health check.

## mDNS — reaching it at `<hostname>.local`

avahi (installed by the script) advertises the Pi at `http://<hostname>.local:8000`.
Our unit's hostname is `jama`, so it's **http://jama.local:8000**. macOS/Linux
resolve `.local` out of the box; Windows needs Bonjour. If `.local` won't
resolve, use the Pi's IP directly (`http://<pi-ip>:8000`).

To rename it (optional — e.g. to `soundvis.local`):

```bash
sudo hostnamectl set-hostname soundvis
sudo systemctl restart avahi-daemon
```

## Enabling the Tyto stand

```bash
ls /dev/ttyACM* /dev/ttyUSB*        # find the stand's serial device
nano config.toml                    # set tyto.enabled = true and tyto.tty = "/dev/ttyACM0"
sudo systemctl restart soundvis
```

`config.toml` is gitignored and survives `git pull` + re-running the installer.
The `[server]` section there controls the bind host/port the service uses.

## Operating the service

```bash
systemctl status soundvis           # is it up?
journalctl -u soundvis -f           # live logs
sudo systemctl restart soundvis     # after editing config.toml
sudo systemctl stop soundvis        # take it down
```

The unit runs as the install user in the `audio` + `dialout` groups (ALSA mics +
USB serial), restarts on failure, and starts on boot.

## Updating to a new version

From the laptop (recommended):

```bash
scripts/deploy_to_pi.sh jama@jama.local
```

Or on the Pi directly:

```bash
cd ~/SoundVisualizer && git pull && bash scripts/setup_rpi.sh
```

Re-runs are fast — the venv exists, so it's just `pip` (changed deps), the
bundle, and a service restart.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `setup_rpi.sh` fails the Python check | System Python is < 3.12 (Bookworm ships 3.11). Flash a Trixie image, or install 3.12+ via pyenv and point the venv at it. |
| Service is `active` but browser can't reach `<hostname>.local` | Same LAN? Try the Pi's IP directly: `http://<pi-ip>:8000`. Windows needs Bonjour for `.local`. |
| Setup page shows zero audio devices | Mics on a **powered** hub? `arecord -l` should list `card N: UMIK-2…`. Re-run `scripts/generate_udev.py` after plugging in. |
| `journalctl` shows `PortAudio library not found` | `sudo apt install libportaudio2` (the installer does this; check it ran). |
| Tyto shows "Not connected" | `tyto.enabled = true` and correct `tty` in `config.toml`? User in `dialout` group? `sudo systemctl restart soundvis` after edits. |
| USB undervoltage warnings in `dmesg` | Not using the 5V/5A PD supply, or mics drawing from a passive hub. |
