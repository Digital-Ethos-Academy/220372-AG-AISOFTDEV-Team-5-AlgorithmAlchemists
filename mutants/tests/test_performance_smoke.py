import time
from statistics import mean

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

ENDPOINTS = [
    ("GET", "/overview", {}),
    ("GET", "/org", {}),
    ("GET", "/roles", {"params": {"query": "Team"}}),
    ("POST", "/qa", {"params": {"question": "Who owns API?"}}),
    ("POST", "/recommendation", {"params": {"user_id": "u1"}}),
    ("GET", "/quiz", {}),
    ("GET", "/metrics", {}),
]


def call(method: str, path: str, kwargs: dict):
    m = method.lower()
    return getattr(client, m)(path, **kwargs)


def test_performance_smoke():
    durations = []
    for _ in range(3):  # small sample per endpoint
        for method, path, kw in ENDPOINTS:
            start = time.time()
            resp = call(method, path, kw)
            assert resp.status_code == 200, f"{path} failed: {resp.status_code} {resp.text}" 
            durations.append((path, (time.time() - start) * 1000))
    avg_ms = mean(d for _, d in durations)
    # Soft target to ensure no gross regression; PRD p95 < 500ms, here avg << 200ms expected
    assert avg_ms < 200, f"Average latency {avg_ms:.2f}ms exceeds threshold"
