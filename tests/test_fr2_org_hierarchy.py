import json

from fastapi.testclient import TestClient
from jsonschema import validate

from app.main import app

with open("schemas/org.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr2_org_hierarchy():
    resp = client.get("/org")
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert len(data["teams"]) >= 10
    # Ensure hierarchical relation present
    assert any(t.get("parent_team_id") for t in data["teams"])  # At least one child team
