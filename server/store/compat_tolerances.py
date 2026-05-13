from pathlib import Path

from server.api.schemas import CompatibilityTolerances
from server.store.paths import data_root


def _file() -> Path:
    return data_root() / "compat-tolerances.json"


def load_tolerances() -> CompatibilityTolerances:
    p = _file()
    if not p.exists():
        return CompatibilityTolerances()
    return CompatibilityTolerances.model_validate_json(p.read_text())


def save_tolerances(t: CompatibilityTolerances) -> None:
    p = _file()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t.model_dump_json(indent=2))
