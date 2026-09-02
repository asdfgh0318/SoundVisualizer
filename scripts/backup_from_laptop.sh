#!/usr/bin/env bash
# Back up the Pi's measurements to GitHub, driven from the laptop.
#
# Why here and not on the Pi: the Pi's data partition (2.3 GB) cannot hold a git
# mirror of the measurements. A mirror is measurements x2 - working copy plus
# objects - and WAVs do not compress, so it filled the partition mid-session on
# 2026-09-02. The laptop has the disk; the Pi keeps only the live files.
#
# Flow: rsync Pi:/home/pi/data/measurements -> local clone of SoundVisualizer-data
#       -> commit if anything changed -> push.
#
# Additive on purpose: NO --delete. Pruning old campaigns off the Pi to free space
# must never remove them from the backup. Removing something from the backup is a
# deliberate act done by hand in the clone.
#
# Exits 0 quietly when the Pi is unreachable so a timer can poll it.
#
# Run: scripts/backup_from_laptop.sh          (or via the user timer, every 15 min)
# Env: PI_HOST (default 10.42.0.245), SOUNDVIS_DATA_CLONE (default ../SoundVisualizer-data)

set -euo pipefail

PI_HOST="${PI_HOST:-10.42.0.245}"
PI_USER="${PI_USER:-pi}"
PI_KEY="${PI_KEY:-$HOME/.ssh/id_ed25519}"
PI_SRC="/home/pi/data/measurements/"
CLONE="${SOUNDVIS_DATA_CLONE:-$(cd "$(dirname "$0")/../.." && pwd)/SoundVisualizer-data}"
BRANCH=main

SSH="ssh -o ConnectTimeout=8 -o BatchMode=yes -o StrictHostKeyChecking=accept-new -i $PI_KEY"

if [ ! -d "$CLONE/.git" ]; then
  echo "no clone at $CLONE - clone asdfgh0318/SoundVisualizer-data there first" >&2
  exit 1
fi

# One run at a time: the timer and a manual run can coincide, and two commits
# in the same clone collide on git's index.lock. Second comer just leaves.
exec 9>"$CLONE/.backup.lock"
if ! flock -n 9; then
  echo "$(date +%H:%M) another backup run is in progress - skipping"
  exit 0
fi

if ! $SSH "$PI_USER@$PI_HOST" true 2>/dev/null; then
  echo "$(date +%H:%M) pi unreachable at $PI_HOST - skipping"
  exit 0
fi

# Do not snapshot a capture in flight: its WAVs are still being written.
state=$(curl -s -m 5 "http://$PI_HOST:8000/capture/run" 2>/dev/null \
        | python3 -c 'import json,sys; print(json.load(sys.stdin).get("state",""))' 2>/dev/null || true)
case "$state" in
  running|starting|stabilizing|recording|writing)
    echo "$(date +%H:%M) capture in progress ($state) - skipping"; exit 0 ;;
esac

cd "$CLONE"
git pull -q --ff-only origin "$BRANCH" 2>/dev/null || true

rsync -a --exclude 'setup-presets/' -e "$SSH" "$PI_USER@$PI_HOST:$PI_SRC" data/

git add -A data/
if git diff --cached --quiet; then
  echo "$(date +%H:%M) nothing changed"
  exit 0
fi

added=$(git diff --cached --name-only --diff-filter=A | grep -c '/meta.json$' || true)
git commit -q -m "backup $(date -u +%Y-%m-%dT%H:%M:%SZ) from laptop (${added} new measurements)"
git push -q origin "$BRANCH"
echo "$(date +%H:%M) pushed $(git rev-parse --short HEAD) - ${added} new measurements"
