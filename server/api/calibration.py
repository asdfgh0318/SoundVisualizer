from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from server.core.calibration import parse_umik_calibration
from server.store import calibration as store
from server.store.calibration import CalibrationSummary

router = APIRouter(prefix="/calibrations", tags=["calibrations"])


@router.get("")
def list_calibrations() -> list[CalibrationSummary]:
    return store.list_calibrations()


@router.post("", status_code=201)
async def upload_calibration(
    file: Annotated[UploadFile, File()],
    serial: str | None = None,
) -> CalibrationSummary:
    text = (await file.read()).decode("utf-8", errors="replace")
    try:
        parsed = parse_umik_calibration(text)
    except ValueError as e:
        raise HTTPException(400, f"failed to parse calibration: {e}") from e
    use_serial = serial or parsed.serial
    if not use_serial:
        raise HTTPException(400, "serial not provided in query and not found in file header")
    return store.save_calibration(use_serial, text, parsed)
