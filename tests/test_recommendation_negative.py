from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recommendation_invalid_user():
    """Test recommendation endpoint with an invalid user ID."""
    resp = client.post("/recommendation", params={"user_id": "invalid-user"})
    assert resp.status_code == 404
    data = resp.json()
    assert data["error_code"] == "USER_NOT_FOUND"
    assert "message" in data

def test_recommendation_no_candidates():
    """Test recommendation endpoint when no candidates are available."""
    # Use a tenant with no seeded teams to force empty candidate list
    resp = client.post(
        "/recommendation",
        params={"user_id": "demo-user-no-candidates"},
        headers={"X-Tenant-Id": "empty"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["confidence"] == 0.0
    assert data["selected_team_id"] is None