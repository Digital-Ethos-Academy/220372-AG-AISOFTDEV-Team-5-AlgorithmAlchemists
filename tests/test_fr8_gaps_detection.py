from fastapi.testclient import TestClient
from app.main import app
from jsonschema import validate
import json

with open("schemas/gaps.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr8_gaps_detection():
    resp = client.get("/gaps")
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert data["summary"]["gap_count"] == 0
