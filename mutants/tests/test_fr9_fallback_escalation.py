import json

from fastapi.testclient import TestClient
from jsonschema import validate

from app.main import app

with open("schemas/fallback.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr9_fallback_escalation():
    resp = client.get("/qa/fallback", params={"question": "Unclear query"})
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert data["escalation"] == "Consult Mentor"
