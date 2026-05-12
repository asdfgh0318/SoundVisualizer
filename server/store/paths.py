import os
import re
from pathlib import Path


def data_root() -> Path:
    return Path(os.environ.get("SOUNDVIS_DATA", "./data"))


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unset"


def key_slug(motor: str, propeller: str, shroud: str, notes: str) -> str:
    return "__".join(slugify(p) for p in (motor, propeller, shroud, notes))


def key_dir(slug: str) -> Path:
    return data_root() / slug


def measurements_dir(slug: str) -> Path:
    return key_dir(slug) / "measurements"


def measurement_dir(slug: str, meas_id: str) -> Path:
    return measurements_dir(slug) / meas_id
