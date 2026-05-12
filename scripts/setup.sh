#!/usr/bin/env bash
# First-time setup for SoundVisualizer on a fresh clone.
#
# Creates a Python venv, installs server + frontend dependencies, runs the test
# suite, and builds the frontend bundle. Works on Linux and macOS.
# Windows users: use scripts/setup.ps1 from PowerShell, or run this from WSL.

set -euo pipefail
cd "$(dirname "$0")/.."

GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m'

step() { printf "\n${GREEN}==>${NC} %s\n" "$*"; }
warn() { printf "${YELLOW}WARN:${NC} %s\n" "$*"; }
fail() { printf "${RED}FAIL:${NC} %s\n" "$*"; exit 1; }

UNAME=$(uname -s)
case "$UNAME" in
  Linux*)   PLATFORM=linux ;;
  Darwin*)  PLATFORM=macos ;;
  MINGW*|CYGWIN*|MSYS*) PLATFORM=windows-bash ;;
  *)        PLATFORM=unknown ;;
esac
step "Detected platform: $PLATFORM"

# --- Python 3.12 ---
if command -v python3.12 >/dev/null 2>&1; then
  PYTHON=python3.12
elif command -v python3 >/dev/null 2>&1 && python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" 2>/dev/null; then
  PYTHON=python3
else
  fail "Python 3.12+ not found. Linux: sudo apt install python3.12 python3.12-venv · macOS: brew install python@3.12"
fi
step "Python: $($PYTHON --version)"

# --- nvm + Node 22 (best-effort) ---
if [ -z "${NVM_DIR:-}" ] && [ -d "$HOME/.nvm" ]; then
  export NVM_DIR="$HOME/.nvm"
fi
if [ -n "${NVM_DIR:-}" ] && [ -s "$NVM_DIR/nvm.sh" ]; then
  # shellcheck disable=SC1091
  . "$NVM_DIR/nvm.sh"
  nvm use >/dev/null 2>&1 || nvm install >/dev/null 2>&1 || true
fi
command -v node >/dev/null 2>&1 || fail "node not found. Install Node 22 (nvm or nodejs.org)."
NODE_VER=$(node -v)
step "Node: $NODE_VER"
case "$NODE_VER" in v22.*) ;; *) warn ".nvmrc pins Node 22; you're on $NODE_VER — frontend should still work but is untested." ;; esac

# --- PortAudio (sounddevice runtime dep) ---
case "$PLATFORM" in
  linux)
    if command -v dpkg-query >/dev/null 2>&1; then
      if ! dpkg-query -W -f='${Status}' libportaudio2 2>/dev/null | grep -q "install ok installed"; then
        warn "libportaudio2 is not installed — sounddevice will fail to enumerate audio devices."
        warn "  Install with: sudo apt install libportaudio2"
      fi
    else
      warn "Non-Debian Linux — install PortAudio via your package manager (e.g. dnf install portaudio)."
    fi
    ;;
  macos)
    if command -v brew >/dev/null 2>&1; then
      if ! brew list portaudio >/dev/null 2>&1; then
        warn "portaudio not installed via Homebrew. If sounddevice imports fail at runtime, run: brew install portaudio"
      fi
    fi
    ;;
  windows-bash|unknown)
    warn "PortAudio: sounddevice wheels bundle the library on Windows; if import fails at runtime, install PortAudio separately."
    ;;
esac

# --- Python venv + deps ---
step "Setting up Python venv at .venv/"
if [ ! -d .venv ]; then
  $PYTHON -m venv .venv
fi
.venv/bin/pip install --upgrade pip --quiet
.venv/bin/pip install -e ".[dev]" --quiet

# --- Frontend deps ---
step "Installing frontend dependencies"
npm install --silent

# --- Smoke checks ---
step "Running server test suite"
.venv/bin/pytest server/tests/ -q

step "Building frontend bundle"
npm run build > /dev/null

# --- Done ---
printf "\n${GREEN}Setup complete!${NC}\n\n"
echo "Run the app:"
echo "  Terminal 1:  .venv/bin/uvicorn server.main:app --reload --port 8000"
echo "  Terminal 2:  npm run dev"
echo "  Open:        http://localhost:5173"
echo
echo "Populate demo data without hardware:"
echo "  curl -X POST http://localhost:8000/dev/seed"
echo "  (or use the Capture form's 'Run fake capture' button)"
echo

case "$PLATFORM" in
  macos|windows-bash|unknown)
    printf "${YELLOW}Heads up:${NC} hardware integration (Tyto serial protocol, ALSA udev rules,\n"
    printf "  multi-mic capture quirks) is Linux-tested only. Frontend dev, fake captures,\n"
    printf "  and the Results tabs (FFT/Polar/Custom) work fully on your platform.\n\n"
    ;;
esac
