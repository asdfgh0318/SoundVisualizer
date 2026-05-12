from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from server.api.schemas import AcousticMeasurementMeta, MeasurementHalf
from server.core.capture import MicCaptureSpec, capture_simultaneous
from server.core.trigger_sync import align_captures
from server.core.wav import write_wav_float32
from server.store import keys as keys_store
from server.store import measurements as meas_store
from server.store.paths import measurement_dir

router = APIRouter(prefix="/capture", tags=["capture"])


class MicSpecIn(BaseModel):
    serial: str
    device_index: int
    elevation_deg: float
    half: MeasurementHalf
    calibration_file_id: str | None = None


class TriggerSyncIn(BaseModel):
    enabled: bool = True
    threshold_db: float = -40.0
    block_size: int = 128
    preroll_samples: int = 480  # ~10ms at 48 kHz


class AcousticCaptureRequest(BaseModel):
    key_slug: str
    duration_seconds: Annotated[float, Field(ge=0.1, le=120.0)] = 5.0
    sample_rate: int = 48000
    pwm_setpoint: int | None = None
    mics: list[MicSpecIn]
    trigger: TriggerSyncIn = TriggerSyncIn()


class AcousticCaptureResponse(BaseModel):
    measurement_ids: list[str]


@router.post("/acoustic", response_model=AcousticCaptureResponse, status_code=201)
def capture_acoustic(req: AcousticCaptureRequest) -> AcousticCaptureResponse:
    if not keys_store.get_key(req.key_slug):
        raise HTTPException(404, f"Key {req.key_slug!r} not found")
    if not req.mics:
        raise HTTPException(400, "no mics specified")

    specs = [
        MicCaptureSpec(serial=m.serial, device_index=m.device_index, sample_rate=req.sample_rate)
        for m in req.mics
    ]

    t_start = datetime.now(UTC)
    results = capture_simultaneous(specs, req.duration_seconds)
    t_end = datetime.now(UTC)

    audios = [r.audio for r in results]
    if req.trigger.enabled:
        audios = align_captures(
            audios,
            threshold_db=req.trigger.threshold_db,
            block_size=req.trigger.block_size,
            preroll_samples=req.trigger.preroll_samples,
        )

    measurement_ids: list[str] = []
    for mic, audio in zip(req.mics, audios, strict=True):
        meta = AcousticMeasurementMeta(
            t_start=t_start,
            t_end=t_end,
            pwm_setpoint=req.pwm_setpoint,
            mic_serial=mic.serial,
            elevation_deg=mic.elevation_deg,
            half=mic.half,
            sample_rate=req.sample_rate,
            calibration_file_id=mic.calibration_file_id,
        )
        saved = meas_store.create_measurement(req.key_slug, meta)
        write_wav_float32(
            measurement_dir(req.key_slug, saved.id) / "audio.wav", audio, req.sample_rate
        )
        measurement_ids.append(saved.id)

    return AcousticCaptureResponse(measurement_ids=measurement_ids)
