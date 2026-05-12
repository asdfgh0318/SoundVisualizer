import sounddevice as sd
from pydantic import BaseModel


class AudioDeviceInfo(BaseModel):
    index: int
    name: str
    hostapi: str
    max_input_channels: int
    default_samplerate: float


def list_input_devices() -> list[AudioDeviceInfo]:
    """Real hardware inputs only — filters out ALSA virtual plugins (default,
    pulse, pipewire, samplerate, etc.) by keeping only devices whose name
    contains '(hw:' which is the canonical ALSA hardware marker."""
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()
    return [
        AudioDeviceInfo(
            index=i,
            name=d["name"],
            hostapi=hostapis[d["hostapi"]]["name"],
            max_input_channels=d["max_input_channels"],
            default_samplerate=d["default_samplerate"],
        )
        for i, d in enumerate(devices)
        if d["max_input_channels"] > 0 and "(hw:" in d["name"]
    ]
