"""
Mnemos FastAPI Server
Expõe o EvoPalace como API REST — consome qualquer LLM, interface web, ou ferramenta externa.

Instalar:
    pip install fastapi uvicorn

Rodar:
    uvicorn api:app --reload --port 8000

Docs automáticas:
    http://localhost:8000/docs
"""

import os
import sys
import time
import uuid

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import EvoPalace

# ─── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Mnemos API",
    description="Living memory for AI agents — evolves, forgets, and shares like a human brain.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, restringir pro domínio da interface
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Palaces ──────────────────────────────────────────────────────────────────

LOCAL_PATH  = os.getenv("MNEMOS_PATH", "./mnemos_data")
SHARED_PATH = os.getenv("MNEMOS_SHARED_PATH", "./mnemos_shared")
PENDING_PATH = os.path.join(SHARED_PATH, "pending.yaml")
AUDIT_PATH   = os.path.join(SHARED_PATH, "audit.yaml")

os.makedirs(SHARED_PATH, exist_ok=True)

palace = EvoPalace(
    palace_name=os.getenv("MNEMOS_PALACE_NAME", "mnemos"),
    api_key=os.getenv("GOOGLE_API_KEY"),
    persist_path=LOCAL_PATH,
)

shared_palace = EvoPalace(
    palace_name="mnemos_shared",
    api_key=os.getenv("GOOGLE_API_KEY"),
    persist_path=SHARED_PATH,
    forget_threshold=0.1,
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _load_yaml(path: str) -> list:
    if os.path.exists(path):
        with open(path) as f:
            return yaml.safe_load(f) or []
    return []


def _save_yaml(path: str, data: list):
    with open(path, "w") as f:
        yaml.dump(data, f)


def _append_audit(action: str, memory_id: str, by: str, note: str = ""):
    audit = _load_yaml(AUDIT_PATH)
    audit.append({
        "action": action,
        "memory_id": memory_id,
        "by": by,
        "note": note,
        "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    _save_yaml(AUDIT_PATH, audit)


# ─── Schemas ──────────────────────────────────────────────────────────────────

class RememberRequest(BaseModel):
    content: str
    room: str = "general"
    tags: list[str] = []
    importance: float = Field(0.7, ge=0.0, le=1.0)

class RecallRequest(BaseModel):
    query: str
    top_k: int = Field(5, ge=1, le=20)
    room_filter: Optional[str] = None

class ShareRequest(BaseModel):
    content: str
    room: str = "project/general"
    reason: str
    proposed_by: str = "agent"
    importance: float = Field(0.8, ge=0.0, le=1.0)

class ApproveRequest(BaseModel):
    approved_by: str = "human"

class RejectRequest(BaseModel):
    rejected_by: str = "human"
    note: str = ""

class LinkRequest(BaseModel):
    id_a: str
    id_b: str
    relation: str = "related"


# ─── Local memory ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "product": "Mnemos", "version": "0.1.0"}


@app.post("/memory", tags=["Local Memory"])
def remember(req: RememberRequest):
    """Store a new memory."""
    mem = palace.remember(
        content=req.content,
        room=req.room,
        tags=req.tags,
        importance=req.importance,
    )
    return {"id": mem.id, "room": mem.room, "importance": mem.importance}


@app.post("/memory/recall", tags=["Local Memory"])
def recall(req: RecallRequest):
    """Search memories by meaning."""
    results = palace.recall(
        query=req.query,
        top_k=req.top_k,
        room_filter=req.room_filter,
    )
    return {"results": results, "count": len(results)}


@app.post("/memory/link", tags=["Local Memory"])
def link(req: LinkRequest):
    """Connect two memories explicitly."""
    palace.link(req.id_a, req.id_b, req.relation)
    return {"linked": True, "id_a": req.id_a, "id_b": req.id_b, "relation": req.relation}


@app.post("/memory/reorganize", tags=["Local Memory"])
def reorganize():
    """Run PageRank — redistribute importance based on usage."""
    changes = palace.reorganize()
    return {"changes": changes, "updated": len(changes)}


@app.post("/memory/forget", tags=["Local Memory"])
def forget(dry_run: bool = False):
    """Apply Ebbinghaus forgetting curve."""
    result = palace.consolidate(dry_run=dry_run)
    return result


@app.get("/memory/status", tags=["Local Memory"])
def status():
    """Palace overview."""
    return palace.status()


@app.get("/memory/all", tags=["Local Memory"])
def list_all():
    """All memories sorted by importance."""
    return {"memories": palace.list_all()}


@app.get("/memory/map", tags=["Local Memory"])
def palace_map():
    """Palace map for visualization."""
    return palace.get_palace_map()


# ─── Shared memory ────────────────────────────────────────────────────────────

@app.post("/shared/propose", tags=["Shared Memory"])
def propose(req: ShareRequest):
    """Propose a memory to be shared with the team. Requires human approval."""
    pending_id = str(uuid.uuid4())[:8]
    pending = _load_yaml(PENDING_PATH)
    pending.append({
        "id": pending_id,
        "content": req.content,
        "room": req.room,
        "reason": req.reason,
        "proposed_by": req.proposed_by,
        "importance": req.importance,
        "proposed_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    })
    _save_yaml(PENDING_PATH, pending)
    _append_audit("proposed", pending_id, req.proposed_by, req.reason)
    return {"pending_id": pending_id, "status": "pending_approval"}


@app.get("/shared/pending", tags=["Shared Memory"])
def list_pending():
    """List memories waiting for approval."""
    return {"pending": _load_yaml(PENDING_PATH)}


@app.post("/shared/approve/{pending_id}", tags=["Shared Memory"])
def approve(pending_id: str, req: ApproveRequest):
    """Approve a pending memory — makes it available to all team agents."""
    pending = _load_yaml(PENDING_PATH)
    found = next((p for p in pending if p["id"] == pending_id), None)
    if not found:
        raise HTTPException(status_code=404, detail=f"Pending ID '{pending_id}' not found")

    shared_palace.remember(
        content=found["content"],
        room=found["room"],
        importance=found.get("importance", 0.8),
        tags=["shared", f"approved_by:{req.approved_by}"],
    )

    pending = [p for p in pending if p["id"] != pending_id]
    _save_yaml(PENDING_PATH, pending)
    _append_audit("approved", pending_id, req.approved_by)

    return {"status": "approved", "shared": True, "content": found["content"][:100]}


@app.post("/shared/reject/{pending_id}", tags=["Shared Memory"])
def reject(pending_id: str, req: RejectRequest):
    """Reject a pending memory — stays local only."""
    pending = _load_yaml(PENDING_PATH)
    found = next((p for p in pending if p["id"] == pending_id), None)
    if not found:
        raise HTTPException(status_code=404, detail=f"Pending ID '{pending_id}' not found")

    pending = [p for p in pending if p["id"] != pending_id]
    _save_yaml(PENDING_PATH, pending)
    _append_audit("rejected", pending_id, req.rejected_by, req.note)

    return {"status": "rejected", "note": req.note}


@app.post("/shared/recall", tags=["Shared Memory"])
def recall_shared(req: RecallRequest):
    """Search approved team memories."""
    results = shared_palace.recall(query=req.query, top_k=req.top_k)
    return {"results": results, "count": len(results)}


@app.get("/shared/status", tags=["Shared Memory"])
def shared_status():
    """Team shared memory overview."""
    s = shared_palace.status()
    pending = _load_yaml(PENDING_PATH)
    audit = _load_yaml(AUDIT_PATH)
    return {
        **s,
        "pending_count": len(pending),
        "recent_audit": audit[-10:] if audit else [],
    }
