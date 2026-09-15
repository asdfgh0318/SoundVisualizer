"""Thin CLI over the library — every command only wires argv to a library call.

    python -m calibrator devices
    python -m calibrator capture 810-8897 [--out DIR] [--freqs 200,1000] [--amplitude 1.0]
    python -m calibrator process --ref 810-8897 [--dir DIR]
"""

import argparse
import sys
from datetime import date
from pathlib import Path

from .core import (
    CalibratorError,
    acquire_speaker,
    acquire_umik,
    assert_mic_ok,
    assert_speaker_ok,
)
from .postprocess import relative_curves, write_rew_curve
from .session import capture_capsule


def _today_dir() -> Path:
    return Path("calibrator/sessions") / date.today().isoformat()


def cmd_devices(_args: argparse.Namespace) -> int:
    try:
        m = acquire_umik()
        print(f"mic:     {m.name}  (card {m.card_id})")
        assert_mic_ok(m)
        print("mic gate: PASS")
    except CalibratorError as e:
        print(f"mic:     {e}")
    try:
        s = acquire_speaker()
        print(f"speaker: {s.name}  (card {s.card_id})")
        assert_speaker_ok(s)
        print("speaker gate: PASS")
    except CalibratorError as e:
        print(f"speaker: {e}")
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    m = acquire_umik()
    s = acquire_speaker()
    freqs = [float(f) for f in args.freqs.split(",")] if args.freqs else None
    out = capture_capsule(m, s, args.label, args.out, freqs=freqs, amplitude=args.amplitude)
    print(f"\ncurve saved: {out}")
    return 0


def cmd_process(args: argparse.Namespace) -> int:
    res = relative_curves(args.dir, args.ref)
    if res["reference_drift_db"]:
        worst = max(res["reference_drift_db"].values())
        print(f"reference bracket drift: worst {worst:+.2f} dB")
        if worst > 2.0:
            print("WARNING: drift above 2 dB — treat this session's curves with suspicion")
    for label, c in res["curves"].items():
        path = write_rew_curve(
            Path(args.dir) / f"{label}_relative.txt",
            c["freqs"], c["diff_db"],
            comment=f"{label} relative to {res['reference']}",
        )
        print(
            f"{label}: {len(c['freqs'])} freqs, "
            f"diff {min(c['diff_db']):+.2f}..{max(c['diff_db']):+.2f} dB "
            f"(shape spread {max(c['diff_db']) - min(c['diff_db']):.2f} dB), "
            f"skipped {c['skipped']} -> {path}"
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="calibrator",
                                description="single-mic substitution calibration")
    sub = p.add_subparsers(dest="command", required=True)

    dev = sub.add_parser("devices", help="show mic/speaker and gate status")
    dev.set_defaults(func=cmd_devices)

    cap = sub.add_parser("capture", help="record one capsule's full curve")
    cap.add_argument("label", help="capsule label (read it off the capsule)")
    cap.add_argument("--out", type=Path, default=_today_dir(),
                     help="session dir (default: calibrator/sessions/<today>)")
    cap.add_argument("--freqs", help="comma-separated override, e.g. 200,1000,16000")
    cap.add_argument("--amplitude", type=float, default=1.0)
    cap.set_defaults(func=cmd_capture)

    proc = sub.add_parser("process", help="difference curves vs the reference")
    proc.add_argument("--ref", required=True, help="reference label")
    proc.add_argument("--dir", type=Path, default=_today_dir(),
                      help="session dir (default: calibrator/sessions/<today>)")
    proc.set_defaults(func=cmd_process)

    args = p.parse_args(argv)
    try:
        return args.func(args)
    except CalibratorError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
