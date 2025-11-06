import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app


AUDIT_FILE = Path("logs/audit.jsonl")
client = TestClient(app)


def test_audit_log_entry_health_endpoint(tmp_path):
    # Ensure clean slate
    if AUDIT_FILE.exists():
        AUDIT_FILE.unlink()
    trace_id = "test-trace-123"
    resp = client.get("/health", headers={"X-Trace-Id": trace_id})
    assert resp.status_code == 200
    assert AUDIT_FILE.exists(), "Audit file not created"
    lines = AUDIT_FILE.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 1
    entry = json.loads(lines[-1])
    # Required keys
    for k in [
        "ts",
        "trace_id",
        "user_id",
        "method",
        "path",
        "status_code",
        "latency_ms",
        "confidence",
    ]:
        assert k in entry, f"Missing key {k} in audit entry"
    assert entry["trace_id"] == trace_id
    assert entry["method"] == "GET"
    assert entry["path"] == "/health"
    assert isinstance(entry["latency_ms"], (int, float)) and entry["latency_ms"] >= 0
    # Confidence may be None (not a recommendation/qa path)
    assert entry["confidence"] is None
