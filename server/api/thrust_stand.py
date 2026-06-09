import asyncio

from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from server.api.schemas import CutoffTriggers

router = APIRouter(prefix="/tyto", tags=["tyto"])


def _service(req: Request):
    svc = getattr(req.app.state, "thrust_stand", None)
    if svc is None:
        raise HTTPException(503, "Tyto stand not connected (config.tyto.enabled = false)")
    return svc


class StatusResponse(BaseModel):
    connected: bool
    pwm_us: int | None = None
    tripped: str | None = None
    tare_thrust_n: float = 0.0
    tare_torque_nm: float = 0.0
    tare_current_a: float = 0.0


class TareResponse(BaseModel):
    tare_thrust_n: float
    tare_torque_nm: float
    tare_current_a: float


class SetPwmRequest(BaseModel):
    pwm_us: int = Field(ge=1000, le=2000)


@router.get("/status", response_model=StatusResponse)
def status(req: Request) -> StatusResponse:
    svc = getattr(req.app.state, "thrust_stand", None)
    if svc is None:
        return StatusResponse(connected=False)
    return StatusResponse(
        connected=True,
        pwm_us=svc.stand.mot_pwm,
        tripped=svc.watchdog.tripped,
        tare_thrust_n=svc.tare.thrust_n,
        tare_torque_nm=svc.tare.torque_nm,
        tare_current_a=svc.tare.current_a,
    )


@router.post("/zero", response_model=TareResponse)
def zero_stand(req: Request) -> TareResponse:
    svc = _service(req)
    try:
        t = svc.zero()
    except RuntimeError as e:
        raise HTTPException(409, str(e)) from e
    return TareResponse(
        tare_thrust_n=t.thrust_n, tare_torque_nm=t.torque_nm, tare_current_a=t.current_a
    )


@router.post("/zero/clear", status_code=204)
def clear_tare(req: Request) -> None:
    _service(req).clear_tare()


@router.post("/pwm", status_code=204)
def set_pwm(req: Request, body: SetPwmRequest) -> None:
    svc = _service(req)
    try:
        svc.set_pwm(body.pwm_us)
    except RuntimeError as e:
        raise HTTPException(409, str(e)) from e


@router.post("/cutoffs", status_code=204)
def set_cutoffs(req: Request, cutoffs: CutoffTriggers) -> None:
    _service(req).update_cutoffs(cutoffs)


@router.post("/reset", status_code=204)
def reset_watchdog(req: Request) -> None:
    _service(req).reset_watchdog()


@router.websocket("/ws/telemetry")
async def telemetry_ws(ws: WebSocket) -> None:
    svc = getattr(ws.app.state, "thrust_stand", None)
    if svc is None:
        await ws.close(code=1011, reason="Tyto stand not connected")
        return
    await ws.accept()
    queue = svc.subscribe()
    try:
        while True:
            msg = await queue.get()
            await ws.send_json(msg)
    except WebSocketDisconnect:
        pass
    except asyncio.CancelledError:
        raise
    finally:
        svc.unsubscribe(queue)
