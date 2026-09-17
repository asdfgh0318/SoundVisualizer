"""Fold the 2026-09-16 substitution measurement into the UMIK cal files.

Nothing is destroyed: the factory files are copied to a dated backup directory
first, and the tool refuses to run if that directory already exists. The session
WAVs and levels.json stay where they are.

Datum: the four capsules whose factory files agree with each other AND with the
measurement (810-8900, 810-8903, 811-1896, 811-2321). Their mean calibrated level
defines zero. That choice adopts whatever absolute error those four share — only a
94 dB calibrator can remove it — but it leaves all eleven mutually consistent,
which is what the arc needs.

Correction goes entirely into gain_db (offset AND shape); every Sens Factor is
kept verbatim, per the session decision.
"""

import json
import re
import shutil
import statistics
import sys
from pathlib import Path

import numpy as np

CAL = Path("/home/adam/ŻYCIE/PRACA/SoundVisualizer-data/data/calibrations")
SESSION = Path("calibrator/sessions/2026-09-16")
BACKUP = CAL / "factory-originals-2026-09-16"

DATUM = ["8108900", "8108903", "8111896", "8112321"]
# serial -> the run(s) to use; the reference has three dense runs, average them
RUNS = {
    "8108904": ["m-810-8904__3", "m-810-8904__4", "m-810-8904__5"],
    "8111896": ["m-811-1896"], "8108903": ["m-810-8903"], "8108900": ["m-810-8900"],
    "8112310": ["m-811-2310"], "8108897": ["m-810-8897"], "8112321": ["m-811-2321"],
    "8108893": ["m-810-8893"], "8111892": ["m-811-1892"], "8108901": ["m-810-8901"],
    "8111897": ["m-811-1897"],
}
# Below this the tone sits near the room's noise floor (62-80 Hz scattered by up to
# 0.7 dB between repeats), so the correction is held flat rather than extrapolated.
LF_TRUST_HZ = 90.0
HF_TRUST_HZ = 16000.0


def read_factory(serial: Path | str):
    text = (CAL / f"{serial}.txt").read_text()
    head = text.splitlines()[0]
    f, g = [], []
    for ln in text.splitlines()[1:]:
        p = ln.split()
        if len(p) >= 2:
            try:
                f.append(float(p[0])); g.append(float(p[1]))
            except ValueError:
                pass
    sens = float(re.search(r"Sens Factor\s*=\s*(-?[\d.]+)", head).group(1))
    return head, np.array(f), np.array(g), sens


def measured(serial):
    """Mean measured level per frequency across this capsule's runs."""
    per = []
    for run in RUNS[serial]:
        rows = json.loads((SESSION / run / "levels.json").read_text())
        per.append({r["freq"]: r["level_dbfs"] for r in rows if "error" not in r})
    freqs = sorted(set().union(*[set(d) for d in per]))
    return {f: statistics.mean([d[f] for d in per if f in d]) for f in freqs}


def main() -> int:
    if BACKUP.exists():
        print(f"refusing to run: {BACKUP} already exists (corrections already applied?)")
        return 1
    BACKUP.mkdir(parents=True)
    for p in sorted(CAL.glob("*.txt")) + sorted(CAL.glob("*.json")):
        shutil.copy2(p, BACKUP / p.name)
    print(f"factory originals copied to {BACKUP}  ({len(list(BACKUP.iterdir()))} files)")

    fac = {s: read_factory(s) for s in RUNS}
    meas = {s: measured(s) for s in RUNS}
    common = sorted(set.intersection(*[set(m) for m in meas.values()]))

    # calibrated level each capsule currently reports, at the measured frequencies
    def calibrated(s):
        head, ff, gg, sens = fac[s]
        return np.array([meas[s][f] - np.interp(f, ff, gg) + 94.0 - sens for f in common])

    datum = np.mean([calibrated(s) for s in DATUM], axis=0)

    report = []
    for s in RUNS:
        head, ff, gg, sens = fac[s]
        delta = calibrated(s) - datum

        # hold the correction flat outside the trusted measured band
        lf = float(np.mean([d for f, d in zip(common, delta) if LF_TRUST_HZ <= f <= 250]))
        hf = float(np.mean([d for f, d in zip(common, delta) if 12000 <= f <= HF_TRUST_HZ]))
        trusted = [(f, d) for f, d in zip(common, delta) if f >= LF_TRUST_HZ]
        tf = np.array([f for f, _ in trusted]); td = np.array([d for _, d in trusted])
        on_grid = np.interp(np.log10(ff), np.log10(tf), td, left=lf, right=hf)

        out = [
            head,
            f'* corrected {__import__("datetime").date.today().isoformat()} from the '
            f"substitution session calibrator/sessions/2026-09-16",
            "* datum = mean of 810-8900, 810-8903, 811-1896, 811-2321 (files consistent "
            "with each other and with measurement)",
            "* Sens Factor above is the FACTORY value, kept verbatim; the whole correction "
            "is in the gain column",
            f"* correction applied: {on_grid.min():+.2f} to {on_grid.max():+.2f} dB, "
            f"{float(np.mean(td)):+.2f} dB mean over {LF_TRUST_HZ:.0f} Hz-16 kHz",
            f"* held flat below {LF_TRUST_HZ:.0f} Hz ({lf:+.2f} dB) and above "
            f"{HF_TRUST_HZ:.0f} Hz ({hf:+.2f} dB) — outside the measured band",
            "* originals in factory-originals-2026-09-16/",
        ]
        out += [f"{f:.3f}\t{g:.4f}" for f, g in zip(ff, gg + on_grid)]
        (CAL / f"{s}.txt").write_text("\n".join(out) + "\n")
        report.append((s, float(np.mean(td)), float(on_grid.min()), float(on_grid.max())))

    print(f"\n{'serial':>9} {'mean':>7} {'min':>7} {'max':>7}")
    for s, m, lo, hi in sorted(report, key=lambda r: -abs(r[1])):
        print(f"{s:>9} {m:+7.2f} {lo:+7.2f} {hi:+7.2f}")
    (CAL / "CORRECTIONS-2026-09-16.csv").write_text(
        "serial,mean_db,min_db,max_db\n"
        + "".join(f"{s},{m:.3f},{lo:.3f},{hi:.3f}\n" for s, m, lo, hi in report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
