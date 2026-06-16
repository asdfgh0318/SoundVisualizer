"""Research-tree integration (Phase C+D).

Browses the linked duct-research-tree editor (typically running on the same Pi
at :8123) and pushes measurement results back to a picked node on capture
completion. All HTTP calls go through aiohttp-free stdlib `urllib.request` to
avoid pulling another runtime dep — the data we exchange is tiny.

The integration is **opt-in** via `config.toml`:

    [research_tree]
    enabled = true
    base_url = "http://localhost:8123"

When `enabled = false` the `/research-tree/*` endpoints respond 503 and the
orchestrator skip-no-op on completion — no behavior change for users who
don't run the tree.
"""

import json
import logging
import urllib.error
import urllib.request
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from server.core.config import ResearchTreeConfig, load_config

log = logging.getLogger(__name__)

router = APIRouter(prefix="/research-tree", tags=["research-tree"])


class ResearchTreeNode(BaseModel):
    """Subset of a duct-research-tree node surfaced to the SoundVis frontend."""

    id: str
    phaseId: str
    title: str
    description: str = ""
    type: str
    status: str
    parents: list[str] = []
    geometry: dict[str, Any] = {}
    soundVisualizerLink: str = ""
    notes: str = ""


class ResearchTreeNodesResponse(BaseModel):
    enabled: bool
    base_url: str
    phases: list[dict[str, Any]] = []
    nodes: list[ResearchTreeNode] = []


def _cfg(req: Request) -> ResearchTreeConfig:
    """Read the latest config for each call — cheap, and lets the user toggle
    the integration without restarting just for the picker to refresh."""
    cfg = getattr(req.app.state, "config", None) or load_config()
    return cfg.research_tree


@router.get("/nodes", response_model=ResearchTreeNodesResponse)
def list_nodes(req: Request) -> ResearchTreeNodesResponse:
    rt = _cfg(req)
    if not rt.enabled:
        return ResearchTreeNodesResponse(enabled=False, base_url=rt.base_url)
    try:
        with urllib.request.urlopen(f"{rt.base_url}/data.json", timeout=5) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise HTTPException(503, f"research-tree unreachable at {rt.base_url}: {e}") from e
    except json.JSONDecodeError as e:
        raise HTTPException(502, f"research-tree returned non-JSON: {e}") from e

    raw_nodes = data.get("nodes") or []
    nodes = [ResearchTreeNode.model_validate(n) for n in raw_nodes]
    return ResearchTreeNodesResponse(
        enabled=True,
        base_url=rt.base_url,
        phases=data.get("phases") or [],
        nodes=nodes,
    )


def push_node_update(rt: ResearchTreeConfig, node_id: str, fields: dict[str, Any]) -> None:
    """Best-effort POST to research-tree's loopback writer. Never raises — the
    capture run already succeeded; failure to update the tree shouldn't fail
    the user-visible operation. Logs the outcome."""
    if not rt.enabled:
        return
    url = f"{rt.base_url}/api/node/{node_id}"
    body = json.dumps(fields).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read())
        log.info("research-tree: updated node %s -> %s", node_id, payload.get("changed", {}))
    except urllib.error.HTTPError as e:
        log.warning("research-tree: node %s update HTTP %s: %s", node_id, e.code, e.read()[:200])
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
        log.warning("research-tree: node %s update failed: %s", node_id, e)
