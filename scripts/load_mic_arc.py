#!/usr/bin/env python3
"""Load the UMIK-2 mic-arc into a running SoundVisualizer instance.

Given a folder of miniDSP UMIK-2 calibration `.txt` files (downloaded from
minidsp.com — that download is Cloudflare-gated so it must be done in a real
browser), this:

  1. uploads each arc mic's calibration file to SoundVis  (POST /calibrations),
  2. creates a setup preset mapping serial → elevation → calibration_file_id
     so the whole arc loads on the Setup page in one click.

The arc map (serial ↔ elevation) is the single source of truth in ARC below —
keep it in sync with docs/mic_arc.md.

Usage:
  python scripts/load_mic_arc.py --dir ~/Pobrane
  python scripts/load_mic_arc.py --dir ~/Downloads --base-url http://jama.local:8000
  python scripts/load_mic_arc.py --dir ~/Pobrane --ninety   # use the _90deg cal files

Cal-file choice: by default the on-axis file (`<serial>.txt`) is used — correct
when each arc mic points AT the source (the DUT). Pass --ninety only if the
mics are mounted perpendicular to the source.
"""

import argparse
import json
import mimetypes
import sys
import urllib.request
import uuid
from pathlib import Path

# (elevation_deg, numeric serial for the cal filename). Top-down; -90 unknown.
ARC: list[tuple[float, str]] = [
    (90.0, "8111897"),
    (72.0, "8111892"),
    (54.0, "8108901"),
    (36.0, "8108893"),
    (18.0, "8112321"),
    (0.0, "8108897"),
    (-18.0, "8112310"),
    (-36.0, "8108900"),
    (-54.0, "8108903"),
    (-72.0, "8111896"),
    # (-90.0, "????"),  # fill in once that mic's serial is read
]


def _multipart(file_path: Path) -> tuple[bytes, str]:
    boundary = f"----svarc{uuid.uuid4().hex}"
    ctype = mimetypes.guess_type(file_path.name)[0] or "text/plain"
    pre = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode()
    post = f"\r\n--{boundary}--\r\n".encode()
    body = pre + file_path.read_bytes() + post
    return body, f"multipart/form-data; boundary={boundary}"


def _post_multipart(url: str, file_path: Path) -> dict:
    body, ctype = _multipart(file_path)
    req = urllib.request.Request(url, data=body, headers={"Content-Type": ctype}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def _post_json(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def find_cal_file(cal_dir: Path, serial: str, ninety: bool) -> Path | None:
    """miniDSP files are named <serial>.txt (on-axis) and <serial>_90deg.txt.
    Match loosely on the numeric serial so dashed/spaced variants still resolve."""
    want_suffix = "_90deg" if ninety else ""
    candidates = []
    for p in cal_dir.glob("*.txt"):
        stem = p.stem
        digits = "".join(c for c in stem if c.isdigit())
        is_ninety = stem.lower().endswith("_90deg")
        if serial in digits and is_ninety == ninety:
            candidates.append(p)
    if candidates:
        # Prefer exact stem match.
        exact = [p for p in candidates if p.stem == f"{serial}{want_suffix}"]
        return exact[0] if exact else candidates[0]
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="folder containing the downloaded cal .txt files")
    ap.add_argument("--base-url", default="http://jama.local:8000", help="SoundVis base URL")
    ap.add_argument("--ninety", action="store_true", help="use the _90deg cal files")
    ap.add_argument("--name", default="Arc 11-mic 18° (top-down)", help="preset name")
    ap.add_argument("--dry-run", action="store_true", help="report only; no uploads")
    args = ap.parse_args()

    cal_dir = Path(args.dir).expanduser()
    if not cal_dir.is_dir():
        print(f"error: {cal_dir} is not a directory", file=sys.stderr)
        return 1
    base = args.base_url.rstrip("/")

    mics = []
    missing = []
    for elev, serial in ARC:
        f = find_cal_file(cal_dir, serial, args.ninety)
        tag = f"{elev:+.0f}° serial {serial}"
        if f is None:
            missing.append((elev, serial))
            print(f"  MISSING  {tag}: no {'_90deg ' if args.ninety else ''}cal file in {cal_dir}")
            continue
        if args.dry_run:
            print(f"  would upload {tag}: {f.name}")
            mics.append({"serial": serial, "elevation_deg": elev, "calibration_file_id": serial})
            continue
        try:
            summ = _post_multipart(f"{base}/calibrations?serial={serial}", f)
            cal_id = summ["id"]
            print(f"  uploaded {tag}: {f.name} -> cal id {cal_id} ({summ.get('n_points')} pts)")
            mics.append({"serial": serial, "elevation_deg": elev, "calibration_file_id": cal_id})
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR    {tag}: upload failed: {e}", file=sys.stderr)

    if missing:
        print(f"\n{len(missing)} cal file(s) not found — download them first (see instructions).")
    if not mics:
        print("no mics resolved; nothing to do.", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"\n[dry-run] would create preset {args.name!r} with {len(mics)} mics")
        return 0

    preset = _post_json(f"{base}/setup-presets", {"name": args.name, "mics": mics})
    print(f"\ncreated preset {preset['name']!r} (id {preset['id']}) with {len(mics)} mics")
    print("→ load it on the Setup page: Microphones → presets bar → pick it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
