#!/usr/bin/env bash
# Deploy SoundVisualizer to a Raspberry Pi from a dev machine.
#
# Builds the React bundle here (so the Pi never needs Node — ideal for small SD
# cards), ships the repo + dist/ to the Pi, and runs scripts/setup_rpi.sh there
# to create the venv and install the systemd service.
#
# Usage:
#   scripts/deploy_to_pi.sh <user>@<host>
#   scripts/deploy_to_pi.sh jama@jama.local
#   scripts/deploy_to_pi.sh jama@192.168.190.89
#
# Auth: uses your normal ssh (set up an ssh key, or you'll be prompted per
# connection). No passwords are stored or accepted on the command line.
#
# Re-runnable: rsync only sends changed files; setup_rpi.sh is idempotent.

set -euo pipefail
cd "$(dirname "$0")/.."

GREEN='\033[1;32m'; RED='\033[1;31m'; NC='\033[0m'
step() { printf "\n${GREEN}==>${NC} %s\n" "$*"; }
fail() { printf "${RED}FAIL:${NC} %s\n" "$*"; exit 1; }

TARGET="${1:-}"
[ -n "$TARGET" ] || fail "Usage: scripts/deploy_to_pi.sh <user>@<host>   (e.g. jama@jama.local)"
REMOTE_DIR="SoundVisualizer"   # relative to the remote user's home

command -v rsync >/dev/null || fail "rsync not found on this machine."

# --- build the bundle locally ----------------------------------------------
step "Building the React bundle (VITE_API_BASE='' → same-origin)"
VITE_API_BASE="" npm run build
[ -f dist/index.html ] || fail "npm run build did not produce dist/index.html."

# --- ship repo + dist -------------------------------------------------------
# Source needed on the Pi: server/, scripts/, deploy/, pyproject.toml,
# config.example.toml, and the prebuilt dist/. Skip the heavy/dev-only dirs.
step "Syncing source + bundle to $TARGET:~/$REMOTE_DIR/"
ssh "$TARGET" "mkdir -p ~/$REMOTE_DIR"
rsync -az --delete \
  --exclude '.git' --exclude '.venv' --exclude 'node_modules' \
  --exclude 'data' --exclude 'config.toml' --exclude '__pycache__' \
  --exclude '.pytest_cache' --exclude '.ruff_cache' \
  ./server ./scripts ./deploy ./dist ./pyproject.toml ./config.example.toml \
  "$TARGET:$REMOTE_DIR/"

# --- run the on-device installer -------------------------------------------
step "Running scripts/setup_rpi.sh on $TARGET"
ssh -t "$TARGET" "cd ~/$REMOTE_DIR && bash scripts/setup_rpi.sh"

HOST="${TARGET#*@}"
step "Deployed."
printf "  Open: ${GREEN}http://%s:8000${NC}\n" "$HOST"
