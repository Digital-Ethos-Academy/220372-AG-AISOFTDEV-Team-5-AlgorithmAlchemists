import json

from fastapi.testclient import TestClient
from jsonschema import validate

from app.main import app

with open("schemas/recommendation.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr5_recommendation_scoring():
    resp = client.post("/recommendation", params={"user_id": "U123"})
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert data["confidence"] >= 0.75
    assert len(data["explanation_breakdown"]) == 3
