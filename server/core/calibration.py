"""miniDSP UMIK-2 calibration file parser.

Format (REW-compatible plain text):

    "Sens Factor =-1.7240dB, SERNO: 8100123"
    "AGain=-9.0dB"
    20.000   -0.45
    21.000   -0.43
    ...

Some files omit AGain. Some have a third "phase" column we ignore. Comment lines
start with `*`. Values are whitespace- or comma-separated.
"""

import re
from dataclasses import dataclass

import numpy as np

_SENS_RE = re.compile(r"Sens(?:\s*Factor)?\s*=\s*(-?\d+(?:\.\d+)?)\s*dB", re.IGNORECASE)
_AGAIN_RE = re.compile(r"AGain\s*=\s*(-?\d+(?:\.\d+)?)\s*dB", re.IGNORECASE)
_SERNO_RE = re.compile(r"SERNO\s*:\s*(\w+)", re.IGNORECASE)


@dataclass
class UmikCalibration:
    serial: str | None
    sens_factor_db: float | None
    again_db: float | None
    freq_hz: np.ndarray
    gain_db: np.ndarray


def parse_umik_calibration(text: str) -> UmikCalibration:
    serial: str | None = None
    sens: float | None = None
    again: float | None = None
    rows: list[tuple[float, float]] = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("*"):
            continue

        m = _SENS_RE.search(line)
        if m:
            sens = float(m.group(1))
            sm = _SERNO_RE.search(line)
            if sm:
                serial = sm.group(1)
            # Real UMIK-2 files put AGain on the SAME line as Sens Factor + SERNO
            # (e.g. `Sens Factor =-12dB, AGain =18dB, SERNO: 8108897`), so scan
            # this line for it too before moving on.
            am = _AGAIN_RE.search(line)
            if am:
                again = float(am.group(1))
            continue

        m = _AGAIN_RE.search(line)
        if m:
            again = float(m.group(1))
            continue

        parts = line.replace(",", " ").split()
        if len(parts) >= 2:
            try:
                rows.append((float(parts[0]), float(parts[1])))
            except ValueError:
                continue

    if not rows:
        raise ValueError("no frequency/gain data found in calibration file")

    arr = np.asarray(rows, dtype=np.float64)
    return UmikCalibration(
        serial=serial,
        sens_factor_db=sens,
        again_db=again,
        freq_hz=arr[:, 0],
        gain_db=arr[:, 1],
    )


def apply_calibration_to_spectrum(
    freq_hz: np.ndarray,
    mag_db: np.ndarray,
    cal: UmikCalibration,
) -> np.ndarray:
    """Add the UMIK-2 calibration correction to a magnitude spectrum.

    Linear interpolation of `cal.gain_db` over `freq_hz`. Bins outside the
    calibration's frequency range clamp to the boundary values.
    """
    correction = np.interp(
        freq_hz,
        cal.freq_hz,
        cal.gain_db,
        left=float(cal.gain_db[0]),
        right=float(cal.gain_db[-1]),
    )
    return mag_db + correction
