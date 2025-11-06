from fastapi.testclient import TestClient
from pathlib import Path
import json
from app.main import app

AUDIT_PATH = Path("logs/audit.jsonl")


def test_fr11_audit_log_write_after_request(tmp_path):
    # Ensure fresh file
    if AUDIT_PATH.exists():
        AUDIT_PATH.unlink()
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert AUDIT_PATH.exists(), "Audit log file should be created"
    lines = AUDIT_PATH.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 1
    last = json.loads(lines[-1])
    # Updated schema-aligned keys
    for key in ["ts", "trace_id", "user_id", "method", "path", "status_code", "latency_ms"]:
        assert key in last
    assert last["path"] == "/health"
    assert last["status_code"] == 200
