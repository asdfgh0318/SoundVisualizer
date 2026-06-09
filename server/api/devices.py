import asyncio
import contextlib
import logging

import numpy as np
import sounddevice as sd
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from server.core.audio_devices import AudioDeviceInfo, list_input_devices

log = logging.getLogger(__name__)

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/audio")
def get_audio_devices() -> list[AudioDeviceInfo]:
    return list_input_devices()


@router.websocket("/audio/{index}/level")
async def audio_level_ws(ws: WebSocket, index: int) -> None:
    """Stream live input level (RMS + peak dBFS) for one device at ~15 Hz.

    Used by the Setup page "Listen" toggle to identify which physical UMIK-2 is
    which — they all report USB serial 00000, so tapping a mic and watching its
    bar move is the only way to tell them apart. Refuses while a capture is in
    progress, since the device can't be opened twice.
    """
    orch = getattr(ws.app.state, "capture_orchestrator", None)
    if orch is not None and orch.is_running():
        await ws.close(code=1011, reason="capture in progress")
        return

    await ws.accept()

    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=8)

    def enqueue(frame: dict) -> None:  # runs on the event loop
        if queue.full():
            with contextlib.suppress(asyncio.QueueEmpty):
                queue.get_nowait()  # drop oldest so the latest level always lands
        queue.put_nowait(frame)

    def callback(indata, _frames, _time, status) -> None:  # runs on PortAudio thread
        x = indata[:, 0].astype(np.float64)
        rms = float(np.sqrt(np.mean(x * x))) + 1e-12
        peak = float(np.max(np.abs(x))) + 1e-12
        frame = {
            "rms_dbfs": 20.0 * np.log10(rms),
            "peak_dbfs": 20.0 * np.log10(peak),
            "overflow": bool(status.input_overflow) if status else False,
        }
        # Hand off to the loop thread; RuntimeError if the loop is already gone.
        with contextlib.suppress(RuntimeError):
            loop.call_soon_threadsafe(enqueue, frame)

    try:
        sr = int(sd.query_devices(index)["default_samplerate"])
    except Exception as e:
        await ws.send_json({"error": f"device {index}: {e}"})
        await ws.close()
        return

    blocksize = max(256, sr // 15)  # ~15 updates/sec

    try:
        stream = sd.InputStream(
            device=index, channels=1, samplerate=sr, blocksize=blocksize, callback=callback
        )
        stream.start()
    except Exception as e:
        log.warning("audio level stream failed for device %s: %s", index, e)
        await ws.send_json({"error": str(e)})
        await ws.close()
        return

    try:
        while True:
            frame = await queue.get()
            await ws.send_json(frame)
    except WebSocketDisconnect:
        pass
    except asyncio.CancelledError:
        raise
    finally:
        stream.stop()
        stream.close()
