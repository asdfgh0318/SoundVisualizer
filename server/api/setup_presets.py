from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from server.api.schemas import MicPresetEntry, SetupPreset
from server.store import setup_presets as store

router = APIRouter(prefix="/setup-presets", tags=["setup-presets"])


class CreatePresetRequest(BaseModel):
    name: str
    mics: list[MicPresetEntry]


@router.get("", response_model=list[SetupPreset])
def list_presets() -> list[SetupPreset]:
    return store.list_presets()


@router.post("", response_model=SetupPreset, status_code=201)
def create_preset(body: CreatePresetRequest) -> SetupPreset:
    name = body.name.strip()
    if not name:
        raise HTTPException(400, "name required")
    return store.create_preset(name, body.mics)


@router.get("/{preset_id}", response_model=SetupPreset)
def get_preset(preset_id: str) -> SetupPreset:
    p = store.get_preset(preset_id)
    if p is None:
        raise HTTPException(404, f"preset {preset_id!r} not found")
    return p


@router.delete("/{preset_id}", status_code=204)
def delete_preset(preset_id: str) -> None:
    if not store.delete_preset(preset_id):
        raise HTTPException(404, f"preset {preset_id!r} not found")
