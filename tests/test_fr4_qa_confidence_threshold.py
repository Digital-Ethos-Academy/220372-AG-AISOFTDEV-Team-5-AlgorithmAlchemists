from fastapi.testclient import TestClient
from app.main import app
from jsonschema import validate
import json

with open("schemas/qa.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr4_qa_confidence_threshold():
    resp = client.post("/qa", params={"question": "Who owns the API?"})
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert data["confidence"] >= 0.85
