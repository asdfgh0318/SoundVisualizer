import asyncio

from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect

from server.api.schemas import CaptureRunStatus
from server.core.capture_orchestrator import CaptureHalfRunRequest, CaptureOrchestrator

router = APIRouter(prefix="/capture/run", tags=["capture-run"])


def _orchestrator(req: Request) -> CaptureOrchestrator:
    orch = getattr(req.app.state, "capture_orchestrator", None)
    if orch is None:
        raise HTTPException(503, "Capture orchestrator not initialized")
    return orch


@router.get("", response_model=CaptureRunStatus)
def get_status(req: Request) -> CaptureRunStatus:
    return _orchestrator(req).get_status()


@router.post("", response_model=CaptureRunStatus, status_code=202)
async def start_run(req: Request, body: CaptureHalfRunRequest) -> CaptureRunStatus:
    orch = _orchestrator(req)
    stand = getattr(req.app.state, "thrust_stand", None)
    if stand is None:
        raise HTTPException(503, "Tyto stand not connected (config.tyto.enabled = false)")
    try:
        return await orch.start_run(stand, body)
    except RuntimeError as e:
        raise HTTPException(409, str(e)) from e
    except ValueError as e:
        raise HTTPException(400, str(e)) from e


@router.delete("", status_code=204)
async def abort_run(req: Request) -> None:
    await _orchestrator(req).abort()


@router.websocket("/ws")
async def status_ws(ws: WebSocket) -> None:
    orch = getattr(ws.app.state, "capture_orchestrator", None)
    if orch is None:
        await ws.close(code=1011, reason="orchestrator not initialized")
        return
    await ws.accept()
    queue = orch.subscribe()
    try:
        await ws.send_json(orch.get_status().model_dump(mode="json"))
        while True:
            status = await queue.get()
            await ws.send_json(status.model_dump(mode="json"))
    except WebSocketDisconnect:
        pass
    except asyncio.CancelledError:
        raise
    finally:
        orch.unsubscribe(queue)
