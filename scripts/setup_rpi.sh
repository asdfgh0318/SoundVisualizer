#!/usr/bin/env bash
# Production install for SoundVisualizer on a Raspberry Pi 5 (64-bit Raspberry
# Pi OS / Debian). Idempotent — safe to re-run after a `git pull`.
#
# Verified on a Pi 5 running Debian 13 (Trixie), which ships Python 3.13 — so we
# use the system interpreter directly (no pyenv, no CPython compile). Any system
# Python >= 3.12 works; the project requires >= 3.12.
#
# Frontend: the React bundle (dist/) is dist-aware. If dist/ already exists
# (e.g. built on a dev machine and rsync'd over — recommended for small SD
# cards, see deploy/README.md), it's used as-is. Otherwise the script installs
# Node and builds it on-device.
#
# What it does:
#   1. apt deps (PortAudio, avahi/mDNS, git, python venv).
#   2. .venv with system Python >= 3.12, pip install -e . (all wheels on aarch64).
#   3. Ensures dist/ exists (uses a shipped one, or builds on-device).
#   4. config.toml from example; best-effort UMIK-2 udev rules.
#   5. Installs + enables the systemd unit so the server starts on boot.
#
# Run from the repo root on the Pi:  bash scripts/setup_rpi.sh

set -euo pipefail
cd "$(dirname "$0")/.."

GREEN='\033[1;32m'; YELLOW='\033[1;33m'; RED='\033[1;31m'; NC='\033[0m'
step() { printf "\n${GREEN}==>${NC} %s\n" "$*"; }
warn() { printf "${YELLOW}WARN:${NC} %s\n" "$*"; }
fail() { printf "${RED}FAIL:${NC} %s\n" "$*"; exit 1; }

RUN_USER="$(id -un)"
RUN_GROUP="$(id -gn)"
INSTALL_DIR="$(pwd)"

[ "$RUN_USER" = "root" ] && fail "Run as the normal user (e.g. 'jama'), not root. The script uses sudo where needed."

# --- platform sanity -------------------------------------------------------
step "Platform check"
ARCH="$(uname -m)"
case "$ARCH" in
  aarch64) ;;
  *) warn "Expected aarch64 (64-bit Pi OS); got '$ARCH'. Continuing, but wheels may not match." ;;
esac
if grep -qi raspberry /proc/device-tree/model 2>/dev/null; then
  printf "    %s\n" "$(tr -d '\0' < /proc/device-tree/model)"
else
  warn "This doesn't look like a Raspberry Pi. The script still works on any Debian/aarch64 host."
fi

# --- apt dependencies ------------------------------------------------------
# PortAudio (sounddevice), avahi (mDNS <hostname>.local), git, venv. No CPython
# build toolchain — we use the system interpreter.
step "Installing apt packages (sudo)"
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  libportaudio2 \
  avahi-daemon \
  git curl ca-certificates \
  python3-venv python3-dev

# --- system Python >= 3.12 -------------------------------------------------
step "Checking system Python"
PYVER="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
printf "    python3 = %s\n" "$PYVER"
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)'; then
  fail "Need Python >= 3.12; system has $PYVER. On Debian 12 (Bookworm, ships 3.11) either upgrade to a Trixie-based image or install 3.12+ via pyenv, then point this script's venv at it."
fi

# --- Python venv + server install ------------------------------------------
step "Creating .venv with system Python $PYVER"
python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
step "Installing server (pip install -e .) — numpy/scipy/mosqito/matplotlib from wheels"
.venv/bin/pip install -e .

# --- frontend bundle (dist-aware) ------------------------------------------
if [ -f dist/index.html ]; then
  step "Using existing dist/ bundle (shipped from a dev machine)"
else
  step "No dist/ found — building the React bundle on-device"
  if command -v node >/dev/null 2>&1 && [ "$(node -v | sed 's/v\([0-9]*\).*/\1/')" -ge 20 ] 2>/dev/null; then
    printf "    node = %s\n" "$(node -v)"
  else
    step "Installing Node 22 via NodeSource (sudo)"
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y nodejs
  fi
  VITE_API_BASE="" npm ci
  VITE_API_BASE="" npm run build
  [ -f dist/index.html ] || fail "npm run build did not produce dist/index.html."
fi

# --- config.toml -----------------------------------------------------------
if [ ! -f config.toml ]; then
  step "Creating config.toml from example (edit to enable the Tyto stand)"
  cp config.example.toml config.toml
else
  step "config.toml already present — leaving it untouched"
fi

# --- udev rules for stable UMIK-2 names (best-effort) ----------------------
step "Generating UMIK-2 udev rules"
if .venv/bin/python scripts/generate_udev.py > /tmp/99-umik2.rules 2>/dev/null && [ -s /tmp/99-umik2.rules ]; then
  sudo cp /tmp/99-umik2.rules /etc/udev/rules.d/99-umik2.rules
  sudo udevadm control --reload || true
  sudo udevadm trigger || true
else
  warn "No UMIK-2 mics detected yet — re-run scripts/generate_udev.py once they're plugged in."
fi

# --- systemd unit ----------------------------------------------------------
# The committed unit is a template (User=pi, paths under %h/SoundVisualizer).
# Substitute the actual install user/group and absolute repo path so it works
# regardless of who runs this or where the repo was cloned.
step "Installing systemd unit (sudo)"
sed -e "s/^User=.*/User=${RUN_USER}/" \
    -e "s/^Group=.*/Group=${RUN_GROUP}/" \
    -e "s#^WorkingDirectory=.*#WorkingDirectory=${INSTALL_DIR}#" \
    -e "s#^Environment=SOUNDVIS_STATIC=.*#Environment=SOUNDVIS_STATIC=${INSTALL_DIR}/dist#" \
    -e "s#^ExecStart=.*#ExecStart=${INSTALL_DIR}/.venv/bin/python -m server#" \
    deploy/soundvis.service > /tmp/soundvis.service
sudo cp /tmp/soundvis.service /etc/systemd/system/soundvis.service
sudo systemctl daemon-reload
sudo systemctl enable soundvis.service
sudo systemctl restart soundvis.service

# --- done ------------------------------------------------------------------
sleep 2
HOSTNAME_NOW="$(hostname)"
step "Done."
printf "\n"
printf "  Service:   ${GREEN}systemctl status soundvis${NC}\n"
printf "  Logs:      ${GREEN}journalctl -u soundvis -f${NC}\n"
printf "  URL (LAN): ${GREEN}http://%s.local:8000${NC}  (or http://<pi-ip>:8000)\n" "$HOSTNAME_NOW"
printf "\n"
if curl -fs -m 5 http://localhost:8000/health >/dev/null 2>&1; then
  printf "  Health check: ${GREEN}OK${NC}\n"
else
  warn "Health check didn't respond yet — check: journalctl -u soundvis -e"
fi
