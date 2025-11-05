from fastapi.testclient import TestClient
from app.main import app
from jsonschema import validate
import json

with open("schemas/roles.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr3_roles_lookup_exact():
    resp = client.get("/roles", params={"query": "Team 1"})
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert any(m["score"] == 1.0 for m in data["matches"])  # exact match scored high

def test_fr3_roles_lookup_fuzzy():
    resp = client.get("/roles", params={"query": "API"})
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert len(data["matches"]) > 0
