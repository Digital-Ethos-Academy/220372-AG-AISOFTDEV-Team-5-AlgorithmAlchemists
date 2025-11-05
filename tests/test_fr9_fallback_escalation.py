from fastapi.testclient import TestClient
from app.main import app
from jsonschema import validate
import json

with open("schemas/fallback.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr9_fallback_escalation():
    resp = client.get("/qa/fallback", params={"question": "Unclear query"})
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert data["escalation"] == "Consult Mentor"
