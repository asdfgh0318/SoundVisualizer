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


# A calibrator driving the mic at 94 dB SPL is 1 Pa rms — the reference level the
# UMIK Sens Factor is quoted against (it records the dBFS the mic reports there).
CALIBRATOR_REFERENCE_SPL_DB = 94.0


def is_absolute_spl(cal: UmikCalibration) -> bool:
    """Whether `cal` can convert dBFS to absolute dB SPL (needs a Sens Factor)."""
    return cal.sens_factor_db is not None


def apply_calibration_to_spectrum(
    freq_hz: np.ndarray,
    mag_db: np.ndarray,
    cal: UmikCalibration,
) -> np.ndarray:
    """Add the UMIK-2 calibration correction to a magnitude spectrum.

    Linear interpolation of `cal.gain_db` over `freq_hz`. Bins outside the
    calibration's frequency range clamp to the boundary values.

    With a Sens Factor present the constant `94 - sens_factor_db` is added too,
    turning dBFS into absolute dB SPL. Adding a level offset to a per-Hz density
    is correct here: it passes through the downstream band integration unchanged.
    AGain is deliberately *not* added — the Sens Factor already accounts for the
    mic's internal gain; AGain only records which analog-gain setting it is valid
    at. Without a Sens Factor only the response curve is applied and the result
    stays dBFS-relative (see `is_absolute_spl`).
    """
    correction = np.interp(
        freq_hz,
        cal.freq_hz,
        cal.gain_db,
        left=float(cal.gain_db[0]),
        right=float(cal.gain_db[-1]),
    )
    if cal.sens_factor_db is not None:
        correction = correction + (CALIBRATOR_REFERENCE_SPL_DB - cal.sens_factor_db)
    return mag_db + correction
