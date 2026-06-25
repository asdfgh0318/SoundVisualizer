#!/usr/bin/env bash
# Mirror ~/SoundVisualizer/data/ into a sibling git repo and push to GitHub.
#
# Run unattended via systemd timer (deploy/soundvis-backup.timer). Pulls in any
# new measurement dirs since the last run, commits with a timestamp, pushes.
# Idempotent: a no-data-change run just exits with "nothing to commit".
#
# Auth: a dedicated ed25519 deploy key (~/.ssh/id_soundvis_data) gated to the
# private SoundVisualizer-data repo via the "github-data" SSH alias.

set -euo pipefail

SRC="${SOUNDVIS_DATA:-$HOME/SoundVisualizer/data}"
DST_DIR="${SOUNDVIS_BACKUP_DIR:-$HOME/SoundVisualizer-data}"
REMOTE="${SOUNDVIS_BACKUP_REMOTE:-github-data:asdfgh0318/SoundVisualizer-data.git}"
BRANCH=main

if [ ! -d "$SRC" ]; then
  echo "no source data dir at $SRC — nothing to back up"
  exit 0
fi

# First-time bootstrap of the destination repo.
if [ ! -d "$DST_DIR/.git" ]; then
  echo "bootstrapping $DST_DIR"
  mkdir -p "$DST_DIR"
  cd "$DST_DIR"
  git init -q -b "$BRANCH"
  git remote add origin "$REMOTE"
  # Try to fetch in case the repo already has history from elsewhere.
  if git ls-remote --heads origin "$BRANCH" 2>/dev/null | grep -q "$BRANCH"; then
    git fetch -q origin "$BRANCH"
    git reset -q --hard "origin/$BRANCH"
  fi
fi

cd "$DST_DIR"

# Mirror data/ from the live tree. --delete so removed runs don't accumulate.
# Exclude any partial / in-progress writes (live captures still being written
# would otherwise produce noisy half-WAV commits).
rsync -a --delete \
  --exclude '.tmp/' --exclude '*.tmp' \
  "$SRC/" data/

git add -A data/

# A bare snapshot README so the repo isn't completely empty on first push.
[ -f README.md ] || cat > README.md <<EOF
# SoundVisualizer-data

Auto-pushed measurement backups from the live SoundVisualizer rig on jama.
Push cadence: every 15 min via systemd timer. See setup_rpi.sh on the main
SoundVisualizer repo for the backup pipeline.
EOF
git add README.md

if git diff --cached --quiet; then
  echo "nothing changed — skipping commit"
  exit 0
fi

git -c user.email="soundvis-data@jama" -c user.name="SoundVis backup" \
  commit -q -m "auto-backup $(date -u +%Y-%m-%dT%H:%M:%SZ)"
git push -q origin "$BRANCH"
echo "pushed $(git rev-parse --short HEAD)"
