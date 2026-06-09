#!/usr/bin/env bash
# Production install for SoundVisualizer on a Raspberry Pi 5 (Raspberry Pi OS
# Bookworm, 64-bit). Idempotent — safe to re-run after a `git pull`.
#
# What it does:
#   1. Installs apt deps (PortAudio, avahi/mDNS, CPython build deps, Node).
#   2. Installs pyenv + CPython 3.12 (Bookworm ships 3.11; we require 3.12,
#      and deadsnakes is Ubuntu-only, so we compile via pyenv — ~15-25 min once).
#   3. Creates .venv with 3.12, installs the server (pip install -e .).
#   4. Builds the React production bundle into dist/.
#   5. Installs + enables the systemd unit so the server starts on boot.
#
# Run from the repo root on the Pi:  bash scripts/setup_rpi.sh

set -euo pipefail
cd "$(dirname "$0")/.."

GREEN='\033[1;32m'; YELLOW='\033[1;33m'; RED='\033[1;31m'; NC='\033[0m'
step() { printf "\n${GREEN}==>${NC} %s\n" "$*"; }
warn() { printf "${YELLOW}WARN:${NC} %s\n" "$*"; }
fail() { printf "${RED}FAIL:${NC} %s\n" "$*"; exit 1; }

PY_VERSION="3.12.7"
RUN_USER="$(id -un)"
RUN_GROUP="$(id -gn)"

[ "$RUN_USER" = "root" ] && fail "Run as the normal user (e.g. 'pi'), not root. The script uses sudo where needed."

# --- platform sanity -------------------------------------------------------
step "Platform check"
ARCH="$(uname -m)"
case "$ARCH" in
  aarch64) ;;
  *) warn "Expected aarch64 (64-bit Pi OS); got '$ARCH'. Continuing, but wheels may not match." ;;
esac
if ! grep -qi raspberry /proc/device-tree/model 2>/dev/null; then
  warn "This doesn't look like a Raspberry Pi. The script still works on any Debian/aarch64 host."
else
  printf "    %s\n" "$(tr -d '\0' < /proc/device-tree/model)"
fi

# --- apt dependencies ------------------------------------------------------
step "Installing apt packages (sudo)"
sudo apt-get update
# PortAudio (sounddevice), avahi (mDNS soundvis.local), git, and the full
# CPython build-dep set pyenv needs to compile 3.12 from source.
sudo apt-get install -y --no-install-recommends \
  libportaudio2 \
  avahi-daemon \
  git curl ca-certificates \
  build-essential \
  libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
  libffi-dev liblzma-dev libncursesw5-dev tk-dev xz-utils \
  llvm libxml2-dev libxmlsec1-dev

# --- Node 22 (Vite 7 needs Node >=20.19 / >=22.12) -------------------------
NODE_OK=false
if command -v node >/dev/null 2>&1; then
  NODE_MAJOR="$(node -v | sed 's/v\([0-9]*\).*/\1/')"
  if [ "$NODE_MAJOR" -ge 20 ] 2>/dev/null; then NODE_OK=true; fi
fi
if [ "$NODE_OK" = true ]; then
  step "Node present: $(node -v)"
else
  step "Installing Node 22 via NodeSource (sudo)"
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
  sudo apt-get install -y nodejs
fi

# --- pyenv + CPython 3.12 --------------------------------------------------
export PYENV_ROOT="$HOME/.pyenv"
if [ ! -d "$PYENV_ROOT" ]; then
  step "Installing pyenv"
  curl -fsSL https://pyenv.run | bash
else
  step "pyenv already installed"
fi
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

if ! pyenv versions --bare | grep -qx "$PY_VERSION"; then
  step "Compiling CPython $PY_VERSION (this takes ~15-25 min on a Pi 5)"
  pyenv install "$PY_VERSION"
else
  step "CPython $PY_VERSION already built"
fi
pyenv local "$PY_VERSION"   # writes .python-version in the repo

# Add pyenv to the user's shell rc once, so future logins find it.
RC="$HOME/.bashrc"
if ! grep -q 'PYENV_ROOT' "$RC" 2>/dev/null; then
  step "Adding pyenv to $RC"
  {
    echo ''
    echo '# pyenv (added by SoundVisualizer setup_rpi.sh)'
    echo 'export PYENV_ROOT="$HOME/.pyenv"'
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"'
    echo 'eval "$(pyenv init -)"'
  } >> "$RC"
fi

# --- Python venv + server install ------------------------------------------
step "Creating .venv with Python $PY_VERSION"
"$(pyenv which python)" -m venv .venv
.venv/bin/pip install --upgrade pip
step "Installing server (pip install -e .)"
.venv/bin/pip install -e .

# --- frontend production bundle --------------------------------------------
step "Building the React bundle (same-origin: served by FastAPI on :8000)"
VITE_API_BASE="" npm ci
VITE_API_BASE="" npm run build
[ -d dist ] || fail "npm run build did not produce dist/."

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
  sudo udevadm control --reload && sudo udevadm trigger || true
else
  warn "No UMIK-2 mics detected yet — re-run scripts/generate_udev.py once they're plugged in."
fi

# --- systemd unit ----------------------------------------------------------
step "Installing systemd unit (sudo)"
# The committed unit is a template (User=pi, paths under %h/SoundVisualizer).
# Substitute the actual install user/group and absolute repo path so it works
# regardless of who runs this or where the repo was cloned.
INSTALL_DIR="$(pwd)"
sed -e "s/^User=.*/User=${RUN_USER}/" \
    -e "s/^Group=.*/Group=${RUN_GROUP}/" \
    -e "s#^WorkingDirectory=.*#WorkingDirectory=${INSTALL_DIR}#" \
    -e "s#^Environment=SOUNDVIS_STATIC=.*#Environment=SOUNDVIS_STATIC=${INSTALL_DIR}/dist#" \
    -e "s#^ExecStart=.*#ExecStart=${INSTALL_DIR}/.venv/bin/python -m server#" \
    deploy/soundvis.service | sudo tee /etc/systemd/system/soundvis.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable soundvis.service
sudo systemctl restart soundvis.service

# --- mDNS hostname hint ----------------------------------------------------
HOSTNAME_NOW="$(hostname)"
step "Done."
printf "\n"
printf "  Service:   ${GREEN}systemctl status soundvis${NC}\n"
printf "  Logs:      ${GREEN}journalctl -u soundvis -f${NC}\n"
printf "  URL (LAN): ${GREEN}http://%s.local:8000${NC}\n" "$HOSTNAME_NOW"
printf "\n"
if [ "$HOSTNAME_NOW" != "soundvis" ]; then
  warn "Hostname is '$HOSTNAME_NOW'. To reach the rig at http://soundvis.local:8000:"
  printf "      ${YELLOW}sudo hostnamectl set-hostname soundvis && sudo systemctl restart avahi-daemon${NC}\n"
fi
if .venv/bin/python -c "import sounddevice" 2>/dev/null; then
  printf "  sounddevice import OK.\n"
fi
