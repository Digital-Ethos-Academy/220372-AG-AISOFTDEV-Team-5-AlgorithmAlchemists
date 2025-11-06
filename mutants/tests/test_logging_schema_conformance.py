import json
from pathlib import Path

from fastapi.testclient import TestClient
from jsonschema import validate

from app.main import app

SCHEMA_PATH = Path("schemas/audit-log-entry.schema.json")
AUDIT_PATH = Path("logs/audit.jsonl")


def test_fr11b_audit_log_schema_conformance():
    # ensure health call writes a log line
    if AUDIT_PATH.exists():
        AUDIT_PATH.unlink()
    client = TestClient(app)
    r = client.get("/health", headers={"X-Trace-Id": "trace-test-123"})
    assert r.status_code == 200
    assert AUDIT_PATH.exists()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    last = json.loads(AUDIT_PATH.read_text(encoding="utf-8").strip().splitlines()[-1])
    # Validate against JSON Schema
    validate(instance=last, schema=schema)
    # Specific field assertions
    assert last["trace_id"] == "trace-test-123"
    assert last["status_code"] == 200
    assert last["latency_ms"] >= 0
