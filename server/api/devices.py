from fastapi import APIRouter

from server.core.audio_devices import AudioDeviceInfo, list_input_devices

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/audio")
def get_audio_devices() -> list[AudioDeviceInfo]:
    return list_input_devices()
