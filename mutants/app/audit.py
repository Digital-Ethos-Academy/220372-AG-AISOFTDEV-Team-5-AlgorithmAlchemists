"""Audit logging middleware writing JSON lines."""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

AUDIT_FILE = Path("logs/audit.jsonl")

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        trace_id = request.headers.get("X-Trace-Id") or str(uuid.uuid4())
        start = time.time()
        response: Response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)
        # Transform to schema-aligned naming & formatting
        iso_ts = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
        entry = {
            "ts": iso_ts,
            "trace_id": trace_id,
            "user_id": None,  # placeholder; future auth integration
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "latency_ms": duration_ms,
            "confidence": None,
            # Optional agent metadata (populated if headers provided)
            "agent_mode": request.headers.get("X-Agent-Mode"),
            "agent_model": request.headers.get("X-Agent-Model"),
            "agent_tools": request.headers.get("X-Agent-Tools"),
        }
        AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return response