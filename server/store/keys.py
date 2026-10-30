from datetime import UTC, datetime
from pathlib import Path

from server.api.schemas import Key, KeyListing
from server.store.paths import data_root, key_dir


def _stamps(key_dir_: Path) -> list[str]:
    """Capture times of the key's measurements, sorted.

    Measurement directory names start with the UTC capture time
    (`2026-07-24T15-52-33-283322__acoustic__...`), so no files are opened.
    """
    md = key_dir_ / "measurements"
    if not md.is_dir():
        return []
    return sorted(e.name.split("__", 1)[0] for e in md.iterdir() if e.is_dir())


def _stamp_time(stamp: str) -> datetime | None:
    try:
        return datetime.strptime(stamp, "%Y-%m-%dT%H-%M-%S-%f").replace(tzinfo=UTC)
    except ValueError:
        return None


def list_keys() -> list[KeyListing]:
    """Keys oldest-measurement first, so the list reads as a campaign timeline.

    Directory order is alphabetical, which interleaves sessions and buries the
    set you just captured in the middle. Keys with no measurements yet sort
    last — they are slots waiting to be filled, not history.
    """
    root = data_root()
    if not root.exists():
        return []
    rows: list[tuple[int, str, KeyListing]] = []
    for d in root.iterdir():
        if not d.is_dir():
            continue
        kf = d / "key.json"
        if not kf.exists():
            continue
        stamps = _stamps(d)
        key = Key.model_validate_json(kf.read_text())
        listing = KeyListing(
            **key.model_dump(exclude={"slug"}),
            first_measured_at=_stamp_time(stamps[0]) if stamps else None,
            last_measured_at=_stamp_time(stamps[-1]) if stamps else None,
        )
        rows.append((0 if stamps else 1, stamps[0] if stamps else d.name, listing))
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
