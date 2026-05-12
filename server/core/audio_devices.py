import sys

import sounddevice as sd
from pydantic import BaseModel


class AudioDeviceInfo(BaseModel):
    index: int
    name: str
    hostapi: str
    max_input_channels: int
    default_samplerate: float


def list_input_devices() -> list[AudioDeviceInfo]:
    """List input audio devices.

    On Linux, filters to ALSA `(hw:…)` hardware devices to drop the proliferation
    of virtual ALSA plugins (default, pulse, pipewire, samplerate, speex, …).
    On macOS and Windows the underlying audio frameworks (CoreAudio, WASAPI/MME)
    don't have the same plugin layer, so we return all input devices.
    """
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()
    is_linux = sys.platform.startswith("linux")

    def keep(d: dict) -> bool:
        if d["max_input_channels"] <= 0:
            return False
        return not (is_linux and "(hw:" not in d["name"])

    return [
        AudioDeviceInfo(
            index=i,
            name=d["name"],
            hostapi=hostapis[d["hostapi"]]["name"],
            max_input_channels=d["max_input_channels"],
            default_samplerate=d["default_samplerate"],
        )
        for i, d in enumerate(devices)
        if keep(d)
    ]
