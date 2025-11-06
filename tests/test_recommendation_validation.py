from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_recommendation_confidence_and_determinism():
    resp = client.post("/recommendation", params={"user_id": "demo-user"})
    assert resp.status_code == 200
    data = resp.json()
    # Confidence target per PRD demo >= 0.75 (rule-based yields 1.0 currently)
    assert data["confidence"] >= 0.9
    # Deterministic first team selection (seeded ordering) should be T1
    assert data["selected_team_id"] == "T1"
