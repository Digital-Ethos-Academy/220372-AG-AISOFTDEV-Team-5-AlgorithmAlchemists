from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_config_health_structure():
    resp = client.get("/config/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "providers" in data
    providers = data["providers"]
    # Expect all provider keys present and values are booleans
    expected = {"openai", "anthropic", "huggingface", "tavily", "google"}
    assert set(providers.keys()) == expected
    assert all(isinstance(v, bool) for v in providers.values())
    # Ensure we never leak actual key material (strings)
    assert not any(isinstance(v, str) for v in providers.values())
    assert "missing_required" in data
