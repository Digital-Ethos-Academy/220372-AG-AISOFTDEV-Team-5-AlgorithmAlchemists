import json

from fastapi.testclient import TestClient
from jsonschema import validate

from app.main import app

with open("schemas/metrics.schema.json") as f:
    SCHEMA = json.load(f)

client = TestClient(app)

def test_fr7_metrics_payload():
    resp = client.get("/metrics")
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SCHEMA)
    assert data["compression_pct"] >= 60
