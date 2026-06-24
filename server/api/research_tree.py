"""Research-tree integration (Phase C+D, multi-tree).

Aggregates nodes from one or more research-tree editor services (each is a
duct-research-tree-style `serve.py` process running on this host or LAN) and
pushes capture results back to a picked node on capture completion. All HTTP
calls go through stdlib `urllib.request` to avoid pulling another runtime dep —
the data we exchange is tiny.

The integration is **opt-in** via `config.toml`. Multiple trees:

    [[research_trees]]
    name = "duct"
    enabled = true
    base_url = "http://localhost:8123"

    [[research_trees]]
    name = "drone-paczek"
    enabled = true
    base_url = "http://localhost:8124"

Legacy `[research_tree]` (singular) is still accepted — it folds into a single
`name="default"` entry.

Routing: node IDs are unique across trees by prefix (e.g. `p1-*` vs `dp1-*`),
so a push is routed by finding which tree's `data.json` contains the id. The
look-up runs once per push and is best-effort: failures are logged, never
propagated, because the capture run already succeeded by the time we push.
"""

import json
import logging
import urllib.error
import urllib.request
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from server.core.config import Config, ResearchTreeConfig, load_config

log = logging.getLogger(__name__)

router = APIRouter(prefix="/research-tree", tags=["research-tree"])


class ResearchTreePhase(BaseModel):
    """A phase scoped to one tree (tagged with `treeKey` so the picker can group)."""

    id: str
    title: str
    color: str = ""
    treeKey: str


class ResearchTreeNode(BaseModel):
    """A node scoped to one tree (tagged with `treeKey` so the picker can group)."""

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
    treeKey: str


class ResearchTreeRef(BaseModel):
    """Front-end surface for one configured tree (used for header links etc.)."""

    name: str
    base_url: str


class ResearchTreeNodesResponse(BaseModel):
    enabled: bool
    trees: list[ResearchTreeRef] = []
    phases: list[ResearchTreePhase] = []
    nodes: list[ResearchTreeNode] = []


def _config(req: Request) -> Config:
    """Read the latest config for each call — cheap, and lets the user toggle
    a tree without restarting just for the picker to refresh."""
    return getattr(req.app.state, "config", None) or load_config()


def _fetch_tree(rt: ResearchTreeConfig) -> dict | None:
    """Fetch a single tree's data.json. Returns None on failure (logged)."""
    try:
        with urllib.request.urlopen(f"{rt.base_url}/data.json", timeout=5) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        log.warning("research-tree %r unreachable at %s: %s", rt.name, rt.base_url, e)
        return None
    except json.JSONDecodeError as e:
        log.warning("research-tree %r returned non-JSON: %s", rt.name, e)
        return None


@router.get("/nodes", response_model=ResearchTreeNodesResponse)
def list_nodes(req: Request) -> ResearchTreeNodesResponse:
    """Aggregate phases + nodes from every enabled tree, tagging each with its
    `treeKey`. When zero trees are enabled, returns `enabled=false` (the picker
    UI then hides itself). When at least one tree is configured but ALL of them
    fail to fetch, raises 503 so the UI can surface the error."""
    cfg = _config(req)
    enabled_trees = [t for t in cfg.research_trees if t.enabled]
    if not enabled_trees:
        return ResearchTreeNodesResponse(enabled=False)

    phases: list[ResearchTreePhase] = []
    nodes: list[ResearchTreeNode] = []
    refs: list[ResearchTreeRef] = []
    failures: list[str] = []
    for rt in enabled_trees:
        refs.append(ResearchTreeRef(name=rt.name, base_url=rt.base_url))
        data = _fetch_tree(rt)
        if data is None:
            failures.append(rt.name)
            continue
        for p in data.get("phases") or []:
            phases.append(ResearchTreePhase.model_validate({**p, "treeKey": rt.name}))
        for n in data.get("nodes") or []:
            nodes.append(ResearchTreeNode.model_validate({**n, "treeKey": rt.name}))

    # All enabled trees failed → surface the error (picker will say "unreachable").
    if failures and not nodes:
        raise HTTPException(
            503, f"research-tree unreachable: {', '.join(failures)}"
        )
    return ResearchTreeNodesResponse(
        enabled=True, trees=refs, phases=phases, nodes=nodes
    )


def _find_tree_for_node(
    trees: list[ResearchTreeConfig], node_id: str
) -> ResearchTreeConfig | None:
    """Look up which configured (enabled) tree owns the given node id.

    Fetches each tree's data.json on demand. Returns the first match.
    Returns None if no tree claims the id (or all fetches failed)."""
    for rt in trees:
        if not rt.enabled:
            continue
        data = _fetch_tree(rt)
        if data is None:
            continue
        if any(n.get("id") == node_id for n in data.get("nodes") or []):
            return rt
    return None


def push_node_update(
    trees: list[ResearchTreeConfig], node_id: str, fields: dict[str, Any]
) -> None:
    """Best-effort POST to the owning tree's loopback writer. Never raises —
    the capture run already succeeded; failure to update the tree shouldn't
    fail the user-visible operation. Logs the outcome."""
    rt = _find_tree_for_node(trees, node_id)
    if rt is None:
        log.warning(
            "research-tree: no enabled tree claims node %r — skipping push", node_id
        )
        return
    url = f"{rt.base_url}/api/node/{node_id}"
    body = json.dumps(fields).encode("utf-8")
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read())
        log.info(
            "research-tree[%s]: updated node %s -> %s",
            rt.name, node_id, payload.get("changed", {}),
        )
    except urllib.error.HTTPError as e:
        log.warning(
            "research-tree[%s]: node %s update HTTP %s: %s",
            rt.name, node_id, e.code, e.read()[:200],
        )
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
        log.warning("research-tree[%s]: node %s update failed: %s", rt.name, node_id, e)
