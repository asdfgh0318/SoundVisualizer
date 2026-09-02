from pathlib import Path

from server.api.schemas import Key
from server.store.paths import data_root, key_dir


def _first_measured_at(key_dir_: Path) -> str | None:
    """Timestamp of the key's earliest measurement, or None if it has none.

    Measurement directory names start with the capture time
    (`2026-07-24T15-52-33-283322__acoustic__...`), so the earliest is just the
    minimum name — no files are opened.
    """
    md = key_dir_ / "measurements"
    if not md.is_dir():
        return None
    stamps = [e.name.split("__", 1)[0] for e in md.iterdir() if e.is_dir()]
    return min(stamps) if stamps else None


def list_keys() -> list[Key]:
    """Keys oldest-measurement first, so the list reads as a campaign timeline.

    Directory order is alphabetical, which interleaves sessions and buries the
    set you just captured in the middle. Keys with no measurements yet sort
    last — they are slots waiting to be filled, not history.
    """
    root = data_root()
    if not root.exists():
        return []
    rows: list[tuple[int, str, Key]] = []
    for d in root.iterdir():
        if not d.is_dir():
            continue
        kf = d / "key.json"
        if not kf.exists():
            continue
        first = _first_measured_at(d)
        rows.append((1 if first is None else 0, first or d.name, Key.model_validate_json(kf.read_text())))
    rows.sort(key=lambda r: (r[0], r[1]))
    return [r[2] for r in rows]


def get_key(slug: str) -> Key | None:
    kf = key_dir(slug) / "key.json"
    if not kf.exists():
        return None
    return Key.model_validate_json(kf.read_text())


def create_key(key: Key) -> Key:
    d = key_dir(key.slug)
    d.mkdir(parents=True, exist_ok=True)
    (d / "measurements").mkdir(exist_ok=True)
    (d / "key.json").write_text(key.model_dump_json(indent=2))
    return key
