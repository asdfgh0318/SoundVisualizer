from server.api.schemas import Key
from server.store.paths import data_root, key_dir


def list_keys() -> list[Key]:
    root = data_root()
    if not root.exists():
        return []
    out: list[Key] = []
    for d in sorted(root.iterdir()):
        if not d.is_dir():
            continue
        kf = d / "key.json"
        if not kf.exists():
            continue
        out.append(Key.model_validate_json(kf.read_text()))
    return out


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
