from fastapi import APIRouter

from server.api.schemas import CompatibilityTolerances
from server.store import compat_tolerances as store

router = APIRouter(prefix="/compat-tolerances", tags=["compat-tolerances"])


@router.get("", response_model=CompatibilityTolerances)
def get_tolerances() -> CompatibilityTolerances:
    return store.load_tolerances()


@router.put("", response_model=CompatibilityTolerances)
def put_tolerances(body: CompatibilityTolerances) -> CompatibilityTolerances:
    store.save_tolerances(body)
    return body
