from fastapi.testclient import TestClient

from app.main import app


def test_fr10_internal_runtime_metrics_snapshot_structure():
    client = TestClient(app)
    # warm up with a health call so aggregator has at least one entry
    client.get("/health")
    resp = client.get("/internal/runtime-metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert "uptime_seconds" in data
    assert "endpoints" in data
    assert "/health" in data["endpoints"]
    entry = data["endpoints"]["/health"]
    assert set(entry.keys()) == {"count", "avg_ms", "p95_ms"}
    assert entry["count"] >= 1
