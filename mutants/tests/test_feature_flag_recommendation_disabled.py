import os
from fastapi.testclient import TestClient
from app.main import app

def test_recommendation_disabled(monkeypatch):
    monkeypatch.setenv("REC_DISABLE", "1")  # 1 disables recommendation (is_enabled returns False)
    client = TestClient(app)
    resp = client.post("/recommendation", params={"user_id": "demo"})
    assert resp.status_code == 503
    body = resp.json()
    assert body["error_code"] == "HTTP_503"
    assert "disabled" in body["message"].lower()
