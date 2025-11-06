from fastapi.testclient import TestClient

from app.main import app


def test_trace_header_present():
    client = TestClient(app)
    r = client.get("/overview")
    assert "X-Trace-Id" in r.headers and len(r.headers["X-Trace-Id"]) > 0
