# Deploying to a Raspberry Pi 5

Production target for the rig. The Pi runs the **same** `server/` code as the
laptop — only the host moves. One `systemd` service serves both the API and the
prebuilt React bundle on port 8000, reachable on the LAN at
`http://soundvis.local:8000`.

> The browser-only demo path (`docker compose up`) is unrelated to this and
> stays as-is for hardware-free UI testing. This document is the **real rig**.

## Hardware checklist

| Item | Why it matters |
|------|----------------|
| **Raspberry Pi 5** (4 GB+), 64-bit Pi OS **Bookworm** | Target platform. RP1 I/O chip has real USB 3.0 — no VL805 bandwidth bug, unlike the Pi 4. |
| **5V / 5A USB-C PD supply** (official 27 W) | Without PD negotiation the Pi 5 caps downstream USB at 600 mA and warns. |
| **Powered USB hub** for the 6× UMIK-2 | Bus-powered mics + a passive hub will brown out. Always power the hub. |
| SD card 16 GB+ (or NVMe HAT) | pyenv compiles CPython 3.12 from source; needs headroom + a few GB free. |

## One-shot install

```bash
# On the Pi, as the normal user (e.g. 'pi'), NOT root:
git clone https://github.com/asdfgh0318/SoundVisualizer.git
cd SoundVisualizer
bash scripts/setup_rpi.sh
```

What the script does (idempotent — safe to re-run after `git pull`):

1. **apt deps** — PortAudio, avahi (mDNS), Node 22 (NodeSource), and the CPython
   build-dependency set.
2. **pyenv + CPython 3.12** — Bookworm ships Python 3.11, but the project
   requires 3.12 and `deadsnakes` is Ubuntu-only, so we compile 3.12 via pyenv.
   **This step takes ~15–25 min the first time** (one-time; cached after).
3. **`.venv` + `pip install -e .`** with the 3.12 interpreter.
4. **`npm ci && npm run build`** → `dist/` (same-origin bundle; `VITE_API_BASE=""`).
5. **udev rules** for stable UMIK-2 ALSA names (best-effort; re-run once mics are
   plugged in if none were detected).
6. **systemd unit** installed, enabled, started.

When it finishes it prints the service status commands and the LAN URL.

## mDNS — reaching it at `soundvis.local`

Set the hostname once so any laptop on the same network resolves it:

```bash
sudo hostnamectl set-hostname soundvis
sudo systemctl restart avahi-daemon
```

Then browse to **http://soundvis.local:8000** from the laptop. (avahi is
installed by the script; macOS/Linux resolve `.local` out of the box, Windows
via Bonjour.)

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

```bash
cd ~/SoundVisualizer
git pull
bash scripts/setup_rpi.sh           # rebuilds venv + bundle, restarts the service
```

pyenv/3.12 is already cached, so re-runs are fast (just `pip`, `npm build`, restart).

## Troubleshooting

| Symptom | Fix |
|---|---|
| `setup_rpi.sh` aborts during `pyenv install` | A build dep is missing — re-run; the apt step installs them. Check `~/.pyenv/versions` for a half-built dir and `pyenv uninstall 3.12.7` before retrying. |
| Service is `active` but browser can't reach `soundvis.local` | Same LAN? Hostname set + avahi restarted? Try the Pi's IP directly: `http://<pi-ip>:8000`. |
| Setup page shows zero audio devices | Mics on a **powered** hub? `arecord -l` should list `card N: UMIK-2…`. Re-run `scripts/generate_udev.py` after plugging in. |
| `journalctl` shows `PortAudio library not found` | `sudo apt install libportaudio2` (the installer does this; check it ran). |
| Tyto shows "Not connected" | `tyto.enabled = true` and correct `tty` in `config.toml`? User in `dialout` group? `sudo systemctl restart soundvis` after edits. |
| USB undervoltage warnings in `dmesg` | Not using the 5V/5A PD supply, or mics drawing from a passive hub. |
