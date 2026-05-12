import uuid
from datetime import UTC, datetime
from pathlib import Path

from server.api.schemas import MicPresetEntry, SetupPreset
from server.store.paths import data_root


def _presets_dir() -> Path:
    return data_root() / "setup-presets"


def list_presets() -> list[SetupPreset]:
    d = _presets_dir()
    if not d.exists():
        return []
    out: list[SetupPreset] = []
    for f in sorted(d.glob("*.json")):
        out.append(SetupPreset.model_validate_json(f.read_text()))
    # most recent first
    out.sort(key=lambda p: p.created_at, reverse=True)
    return out


def get_preset(preset_id: str) -> SetupPreset | None:
    p = _presets_dir() / f"{preset_id}.json"
    if not p.exists():
        return None
    return SetupPreset.model_validate_json(p.read_text())


def create_preset(name: str, mics: list[MicPresetEntry]) -> SetupPreset:
    d = _presets_dir()
    d.mkdir(parents=True, exist_ok=True)
    preset = SetupPreset(
        id=uuid.uuid4().hex,
        name=name,
        created_at=datetime.now(UTC),
        mics=mics,
    )
    (d / f"{preset.id}.json").write_text(preset.model_dump_json(indent=2))
    return preset


def delete_preset(preset_id: str) -> bool:
    p = _presets_dir() / f"{preset_id}.json"
    if not p.exists():
        return False
    p.unlink()
    return True
