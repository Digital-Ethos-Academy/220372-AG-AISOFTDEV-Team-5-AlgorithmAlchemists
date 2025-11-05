from fastapi.testclient import TestClient
from app.main import app
from jsonschema import validate
import json

with open("schemas/overview.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr1_overview_success():
    resp = client.get("/overview")
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert data["team_count"] >= 1
    assert len(data["mission"]) >= 10
