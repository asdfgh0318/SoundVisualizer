from fastapi import APIRouter, HTTPException

from server.api.schemas import MeasurementMeta
from server.store import keys as keys_store
from server.store import measurements as store

router = APIRouter(prefix="/keys/{slug}/measurements", tags=["measurements"])


def _require_key(slug: str) -> None:
    if not keys_store.get_key(slug):
        raise HTTPException(404, f"Key {slug!r} not found")


@router.get("")
def list_measurements(slug: str) -> list[MeasurementMeta]:
    _require_key(slug)
    return store.list_measurements(slug)


@router.post("", status_code=201)
def create_measurement(slug: str, meta: MeasurementMeta) -> MeasurementMeta:
    _require_key(slug)
    return store.create_measurement(slug, meta)


@router.get("/{meas_id}")
def get_measurement(slug: str, meas_id: str) -> MeasurementMeta:
    _require_key(slug)
    m = store.get_measurement(slug, meas_id)
    if not m:
        raise HTTPException(404, f"Measurement {meas_id!r} not found")
    return m
