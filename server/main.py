import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api import (
    calibration,
    capture,
    capture_run,
    dev,
    devices,
    keys,
    measurements,
    results,
)
from server.api import thrust_stand as tyto_api
from server.core.calibration_override import apply_calibration_config
from server.core.capture_orchestrator import CaptureOrchestrator
from server.core.config import load_config
from server.core.thrust_stand_service import ThrustStandService

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = load_config()
    apply_calibration_config(config.tyto.calibration)

    if config.tyto.enabled:
        try:
            app.state.thrust_stand = await ThrustStandService.start(config)
            log.info("Tyto stand connected on %s", config.tyto.tty)
        except Exception as e:
            log.warning("Tyto stand failed to start: %s — continuing without it", e)
            app.state.thrust_stand = None
    else:
        app.state.thrust_stand = None

    app.state.capture_orchestrator = CaptureOrchestrator(
        poll_period_seconds=config.tyto.poll_period_seconds
    )

    try:
        yield
    finally:
        orch = getattr(app.state, "capture_orchestrator", None)
        if orch is not None and orch.is_running():
            await orch.abort()
        svc = getattr(app.state, "thrust_stand", None)
        if svc is not None:
            await svc.stop()


app = FastAPI(title="SoundVisualizer Server", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(keys.router)
app.include_router(measurements.router)
app.include_router(devices.router)
app.include_router(calibration.router)
app.include_router(capture.router)
app.include_router(capture_run.router)
app.include_router(results.router)
app.include_router(tyto_api.router)
app.include_router(dev.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
