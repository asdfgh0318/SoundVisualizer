import re
import sys
from pathlib import Path

import sounddevice as sd
from pydantic import BaseModel


class AudioDeviceInfo(BaseModel):
    index: int
    name: str
    hostapi: str
    max_input_channels: int
    default_samplerate: float
    alsa_card_id: str | None = None  # stable per-port id from udev (e.g. umik_3_1_2)


_HW_RE = re.compile(r"\(hw:(\d+),")


def _alsa_card_id(device_name: str) -> str | None:
    """Map an ALSA device name like 'UMIK-2: USB Audio (hw:3,0)' to the card's
    stable id (/sys/class/sound/card3/id), which our udev rules pin per USB port.
    Lets the UI tell apart UMIK-2s that otherwise share the name + serial."""
    m = _HW_RE.search(device_name)
    if not m:
        return None
    try:
        return Path(f"/sys/class/sound/card{m.group(1)}/id").read_text().strip() or None
    except OSError:
        return None


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
            alsa_card_id=_alsa_card_id(d["name"]) if is_linux else None,
        )
        for i, d in enumerate(devices)
        if keep(d)
    ]
