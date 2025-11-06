from fastapi.testclient import TestClient

from app.main import app


def test_error_envelope_structure_recommendation_flag():
    client = TestClient(app)
    # Force flag disabled via header injection not needed; relying on default env (enabled) we expect 200
    resp = client.post("/recommendation", params={"user_id": "demo"})
    if resp.status_code == 503:  # if disabled in environment running tests
        body = resp.json()
        assert set(body.keys()) == {"error_code", "message", "trace_id"}
    else:
        assert resp.status_code == 200
