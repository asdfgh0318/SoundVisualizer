import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from server.api import (
    calibration,
    capture,
    capture_run,
    compat_tolerances,
    dev,
    devices,
    keys,
    measurements,
    research_tree,
    results,
    setup_presets,
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
    app.state.config = config
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

    # Capture-completion hook: push the SoundVis Results URL back into the
    # linked research-tree node, if the run's request carries one. The push
    # is routed to whichever configured tree owns the node id.
    def _on_capture_completed(req, status):
        node_id = getattr(req, "research_tree_node_id", None)
        trees = [t for t in config.research_trees if t.enabled]
        if not node_id or not trees:
            return
        # `public_url` is per-tree (might differ if trees front different
        # SoundVis instances), but in our setup all trees point at the same
        # SoundVis — so the first enabled tree's public_url is the right base.
        base = trees[0].public_url.rstrip("/")
        results_url = (
            f"{base}/results#key={status.key_slug}"
            if base and status.key_slug
            else f"/results#key={status.key_slug}"
        )
        research_tree.push_node_update(
            config.research_trees,
            node_id,
            {"soundVisualizerLink": results_url, "status": "in-progress"},
        )

    app.state.capture_orchestrator = CaptureOrchestrator(
        poll_period_seconds=config.tyto.poll_period_seconds,
        on_completed=_on_capture_completed,
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
app.include_router(setup_presets.router)
app.include_router(research_tree.router)
app.include_router(compat_tolerances.router)
app.include_router(tyto_api.router)
app.include_router(dev.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


# When packaged as a Docker image, the React bundle is served from here so
# port 8000 hosts both the API and the SPA. Registered last so it doesn't
# shadow API routes. A bare StaticFiles mount can't fall back to index.html
# for client-side router paths (e.g. /setup, /capture), so direct loads or
# refreshes of those paths 404. The catch-all below serves the requested
# file when it exists and otherwise returns index.html — standard SPA hosting.
_static_dir = os.environ.get("SOUNDVIS_STATIC")
if _static_dir and Path(_static_dir).is_dir():
    _static_path = Path(_static_dir).resolve()
    _index_html = _static_path / "index.html"

    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str) -> FileResponse:
        if full_path:
            candidate = (_static_path / full_path).resolve()
            try:
                candidate.relative_to(_static_path)
            except ValueError:
                raise HTTPException(status_code=404) from None
            if candidate.is_file():
                return FileResponse(candidate)
        return FileResponse(_index_html)

    log.info("Serving frontend bundle from %s", _static_dir)
