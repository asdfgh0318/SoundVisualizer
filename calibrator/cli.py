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
    log_series,
    third_octave,
)
from .postprocess import relative_curves, write_rew_curve
from .rig import capture_rig, discover_umiks, identify_live, load_arc
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
    if args.freqs:
        if args.fmin is not None or args.fmax is not None:
            raise CalibratorError("--freqs and --fmin/--fmax are mutually exclusive")
        freqs = [float(f) for f in args.freqs.split(",")]
    elif args.per_octave:
        freqs = log_series(
            fmin=60.0 if args.fmin is None else args.fmin,
            fmax=16000.0 if args.fmax is None else args.fmax,
            per_octave=args.per_octave,
        )
    elif args.fmin is not None or args.fmax is not None:
        freqs = third_octave(
            fmin=63.0 if args.fmin is None else args.fmin,
            fmax=16000.0 if args.fmax is None else args.fmax,
        )
    else:
        freqs = None
    out = capture_capsule(m, s, args.label, args.out, freqs=freqs, amplitude=args.amplitude)
    print(f"\ncurve saved: {out}")
    return 0


def cmd_rig(args: argparse.Namespace) -> int:
    """Stepped tones through the whole assembled arc — see calibrator/rig.py."""
    arc = load_arc(args.preset)
    s = acquire_speaker()
    assert_speaker_ok(s)
    print(f"speaker: {s.name}")
    print(f"arc: {len(arc)} capsules  " +
          "  ".join(f"{m.position_deg:+.0f}°={m.serial[-4:]}" for m in arc) + "\n")
    if args.freqs:
        freqs = [float(f) for f in args.freqs.split(",")]
    else:
        freqs = log_series(fmin=args.fmin, fmax=args.fmax, per_octave=args.per_octave)
    out = capture_rig(arc, s, args.label, args.out, freqs,
                      amplitude=args.amplitude, capture_s=args.capture_s,
                      save_wavs=args.save_wavs)
    print(f"\nsaved: {out}")
    return 0


def cmd_identify(args: argparse.Namespace) -> int:
    """Live per-capsule meter — tap a mic, see which row jumps."""
    if args.preset:
        arc = load_arc(args.preset)
        print(f"arc: {len(arc)} capsules from {args.preset}")
    else:
        arc = discover_umiks()
        if not arc:
            raise CalibratorError("no UMIK-2 inputs visible to PortAudio — if they are plugged "
                                  "in, PipeWire is holding them; wpctl set-profile <dev> off")
        print(f"{len(arc)} UMIK-2 inputs, by USB port. Positions unknown — tap them in arc "
              f"order and write down which port answers.")
    identify_live(arc, refresh_hz=args.refresh_hz, tap_over_db=args.tap_over_db)
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
    cap.add_argument("--per-octave", type=int, default=None,
                    help="denser log grid (IEC 61260, anchored at 1 kHz) instead of the "
                         "default 1/3-octave list; e.g. 6 = 49 points, 12 = 97 points. "
                         "One grid per session: postprocessing matches exact frequencies.")
    cap.add_argument("--fmin", type=float, default=None,
                     help="lower bound of the tone grid (default: the grid's own, 63/60 Hz)")
    cap.add_argument("--fmax", type=float, default=None,
                     help="upper bound of the tone grid (default: 16000 Hz)")
    cap.add_argument("--amplitude", type=float, default=1.0)
    cap.set_defaults(func=cmd_capture)

    rig = sub.add_parser("rig", help="stepped tones through the whole arc at once")
    rig.add_argument("label", help="what this run is, e.g. full-rig or neighbours-removed")
    rig.add_argument("--preset", type=Path, required=True,
                     help="Setup preset json holding the eleven serials + alsa_card_ids")
    rig.add_argument("--out", type=Path, default=_today_dir(),
                     help="session dir (default: calibrator/sessions/<today>)")
    rig.add_argument("--freqs", help="comma-separated override, e.g. 500,1000,1300")
    rig.add_argument("--per-octave", type=int, default=24,
                     help="log grid density; 24 resolves a 26 cm neighbour comb (default 24)")
    rig.add_argument("--fmin", type=float, default=500.0)
    rig.add_argument("--fmax", type=float, default=4000.0)
    rig.add_argument("--amplitude", type=float, default=0.03)
    rig.add_argument("--capture-s", type=float, default=2.0)
    rig.add_argument("--save-wavs", action="store_true",
                     help="keep the audio as well as the levels (11 files per frequency)")
    rig.set_defaults(func=cmd_rig)

    ident = sub.add_parser("identify",
                           help="live meter over the whole arc — verify which capsule is where")
    ident.add_argument("--preset", type=Path, default=None,
                       help="verify an existing map; omit to just list every UMIK by USB port "
                            "(the preset's identity is a port path, and those do not survive "
                            "a move to another machine or hub)")
    ident.add_argument("--refresh-hz", type=float, default=12.0)
    ident.add_argument("--tap-over-db", type=float, default=12.0,
                       help="how far above its own quiet baseline a channel must jump to be "
                            "flagged as tapped (default 12 dB)")
    ident.set_defaults(func=cmd_identify)

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
