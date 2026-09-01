import asyncio
import contextlib
import logging

import numpy as np
import sounddevice as sd
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from server.core.audio_devices import AudioDeviceInfo, list_input_devices
from server.core.calibration import CALIBRATOR_REFERENCE_SPL_DB
from server.store.calibration import get_calibration

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


class LevelsMicSpec(BaseModel):
    """One mic to monitor: which device, where on the arc, and how to calibrate it."""

    serial: str
    device_index: int
    elevation_deg: float
    calibration_file_id: str | None = None


class LevelsRequest(BaseModel):
    mics: list[LevelsMicSpec]


@router.websocket("/audio/levels")
async def audio_levels_ws(ws: WebSocket) -> None:
    """Stream broadband level for several mics at once, for the live polar readout.

    Send a `{"mics": [...]}` frame first, then receive `{"levels": [...]}` at ~10 Hz.

    Each mic's level is scalar-calibrated to dB SPL when its cal file carries a Sens
    Factor (`SPL = dBFS - sens + 94`), matching the FFT path's convention. The
    per-frequency response curve is deliberately NOT applied — that needs an FIR
    filter on the time signal, and this is a broadband RMS. Mics without a Sens
    Factor stay dBFS and are flagged `absolute: false`.

    Opens every requested device, so it refuses while a capture is running for the
    same reason the single-mic meter does: a device cannot be opened twice.
    """
    orch = getattr(ws.app.state, "capture_orchestrator", None)
    if orch is not None and orch.is_running():
        await ws.close(code=1011, reason="capture in progress")
        return

    await ws.accept()

    try:
        req = LevelsRequest.model_validate(await ws.receive_json())
    except Exception as e:
        await ws.send_json({"error": f"bad request: {e}"})
        await ws.close()
        return
    if not req.mics:
        await ws.send_json({"error": "no mics specified"})
        await ws.close()
        return

    # Scalar SPL offset per mic, resolved once up front.
    offsets: list[float | None] = []
    for m in req.mics:
        off = None
        if m.calibration_file_id:
            cal = get_calibration(m.calibration_file_id)
            if cal is not None and cal.sens_factor_db is not None:
                off = CALIBRATOR_REFERENCE_SPL_DB - cal.sens_factor_db
        offsets.append(off)

    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=4)
    latest: list[float | None] = [None] * len(req.mics)

    def enqueue() -> None:  # runs on the event loop
        frame = {
            "levels": [
                {
                    "serial": m.serial,
                    "elevation_deg": m.elevation_deg,
                    "level_db": latest[i],
                    "absolute": offsets[i] is not None,
                }
                for i, m in enumerate(req.mics)
            ]
        }
        if queue.full():
            with contextlib.suppress(asyncio.QueueEmpty):
                queue.get_nowait()  # drop oldest so the latest reading always lands
        queue.put_nowait(frame)

    def make_callback(i: int):
        def cb(indata, _frames, _time, _status) -> None:  # PortAudio thread
            x = indata[:, 0].astype(np.float64)
            rms = float(np.sqrt(np.mean(x * x))) + 1e-12
            db = 20.0 * np.log10(rms)
            off = offsets[i]
            latest[i] = db + off if off is not None else db
            if i == 0:  # one mic drives the frame rate; the rest just update `latest`
                with contextlib.suppress(RuntimeError):
                    loop.call_soon_threadsafe(enqueue)

        return cb

    streams: list[sd.InputStream] = []
    try:
        for i, m in enumerate(req.mics):
            sr = int(sd.query_devices(m.device_index)["default_samplerate"])
            streams.append(
                sd.InputStream(
                    device=m.device_index,
                    channels=1,
                    samplerate=sr,
                    blocksize=max(256, sr // 10),  # ~10 updates/sec
                    callback=make_callback(i),
                )
            )
        for st in streams:
            st.start()
    except Exception as e:
        log.warning("live levels stream failed: %s", e)
        for st in streams:  # release whatever opened before the failure
            with contextlib.suppress(Exception):
                st.stop()
            with contextlib.suppress(Exception):
                st.close()
        with contextlib.suppress(Exception):
            await ws.send_json({"error": str(e)})
            await ws.close()
        return

    try:
        while True:
            await ws.send_json(await queue.get())
    except WebSocketDisconnect:
        pass
    except asyncio.CancelledError:
        raise
    finally:
        for st in streams:
            with contextlib.suppress(Exception):
                st.stop()
            with contextlib.suppress(Exception):
                st.close()
