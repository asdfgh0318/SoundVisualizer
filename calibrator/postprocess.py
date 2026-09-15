"""Turn session captures into calibration curves.

Everything here is relative: the reference capsule defines zero, its repeated
runs (the bracket) average out source drift, and every other capsule's curve
is its level minus the reference's at each frequency. Folding the difference
into a factory REW file is gain += diff (the pipeline SUBTRACTS gain, so a
capsule measuring D dB hot needs D added); the Sens Factor header is kept
verbatim — the absolute anchor comes from a real 94 dB calibrator later.
"""

import json
from pathlib import Path

import numpy as np

from .core import CalibratorError


def _runs(base: Path, label: str) -> list[Path]:
    runs = [d for d in sorted(base.glob(f"{label}__*")) if d.is_dir()]
    if (base / label).is_dir():
        runs.insert(0, base / label)
    return runs


def _levels(run: Path) -> dict[float, float]:
    data = json.loads((run / "levels.json").read_text())
    return {r["freq"]: r["level_dbfs"] for r in data if "level_dbfs" in r}


def relative_curves(session_dir: str | Path, reference_label: str) -> dict:
    """{curves: {label: {freqs, diff_db, skipped}}, reference levels and drift}.

    diff_db = capsule level - reference level at each frequency they share.
    Reference drift (max-min across the bracket runs, per frequency) is
    reported so a drifted session is visible before anyone trusts the curves.
    """
    base = Path(session_dir)
    ref_runs = _runs(base, reference_label)
    if not ref_runs:
        raise CalibratorError(f"no reference runs labelled '{reference_label}' in {base}")
    ref = [_levels(r) for r in ref_runs]
    freqs = sorted(set.intersection(*(set(r) for r in ref)))
    reference_levels = {f: float(np.mean([r[f] for r in ref])) for f in freqs}
    drift = {}
    if len(ref) > 1:
        drift = {f: float(max(r[f] for r in ref) - min(r[f] for r in ref)) for f in freqs}

    curves: dict[str, dict] = {}
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        if d.name == reference_label or d.name.startswith(f"{reference_label}__"):
            continue
        lv = _levels(d)
        common = [f for f in freqs if f in lv]
        curves[d.name] = {
            "freqs": common,
            "diff_db": [lv[f] - reference_levels[f] for f in common],
            "skipped": sorted(set(lv) - set(common)),
        }
    return {
        "reference": reference_label,
        "reference_levels": reference_levels,
        "reference_drift_db": drift,
        "curves": curves,
    }


def write_rew_curve(path: str | Path, freqs, gain_db, comment: str = "") -> Path:
    """REW-compatible curve file ('*' comments + 'freq gain' rows)."""
    path = Path(path)
    lines = [f"* {comment}".rstrip()]
    lines += [f"{f:g}  {g:+.2f}" for f, g in zip(freqs, gain_db, strict=False)]
    path.write_text("\n".join(lines) + "\n")
    return path


def merge_curve(factory_path: str | Path, freqs, diff_db, out_path: str | Path) -> Path:
    """Fold a measured difference into a factory REW calibration file.

    Rows before the first freq/gain pair (Sens Factor, AGain, SERNO, comments)
    are copied verbatim; the response curve becomes factory gain + interpolated
    difference. Interpolation clamps at the ends of the measured range.
    """
    header: list[str] = []
    rows: list[tuple[float, float]] = []
    for line in Path(factory_path).read_text().splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            f, g = (float(v) for v in s.replace(",", " ").split()[:2])
        except ValueError:
            if not rows:
                header.append(line)
            continue
        rows.append((f, g))
    if not rows:
        raise CalibratorError(f"no freq/gain rows in {factory_path}")

    xs = np.asarray(freqs, dtype=float)
    ds = np.asarray(diff_db, dtype=float)
    order = np.argsort(xs)
    xs, ds = xs[order], ds[order]

    out = Path(out_path)
    with out.open("w") as fh:
        for line in header:
            fh.write(line + "\n")
        for f, g in rows:
            fh.write(f"{f:g}  {g + float(np.interp(f, xs, ds)):+.4f}\n")
    return out
