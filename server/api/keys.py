from fastapi import APIRouter, HTTPException

from server.api.schemas import Key
from server.store import keys as store

router = APIRouter(prefix="/keys", tags=["keys"])


@router.get("")
def list_keys() -> list[Key]:
    return store.list_keys()


@router.post("", status_code=201)
def create_key(key: Key) -> Key:
    if store.get_key(key.slug):
        raise HTTPException(409, f"Key {key.slug!r} already exists")
    return store.create_key(key)


@router.get("/{slug}")
def get_key(slug: str) -> Key:
    k = store.get_key(slug)
    if not k:
        raise HTTPException(404, f"Key {slug!r} not found")
    return k
