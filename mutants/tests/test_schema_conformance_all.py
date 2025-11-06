import json
import pathlib

from fastapi.testclient import TestClient
from jsonschema import validate

from app.main import app

client = TestClient(app)

SCHEMA_DIR = pathlib.Path('schemas')

ENDPOINT_SCHEMAS = [
    ("/overview", "overview.schema.json"),
    ("/org", "org.schema.json"),
    ("/roles?query=test", "roles.schema.json"),
    ("/metrics", "metrics.schema.json"),
    ("/gaps", "gaps.schema.json"),
    ("/quiz", "quiz.schema.json"),
]

POST_ENDPOINTS = [
    ("/qa", {"question": "Who owns API?"}, "qa.schema.json"),
    ("/recommendation", {"user_id": "demo-user"}, "recommendation.schema.json"),
]

# Fallback and quiz submit have dedicated existing tests; here we ensure baseline schema coverage.

def load_schema(name: str):
    with open(SCHEMA_DIR / name) as f:
        return json.load(f)


def test_get_schemas_conform():
    for url, schema_file in ENDPOINT_SCHEMAS:
        schema = load_schema(schema_file)
        resp = client.get(url)
        assert resp.status_code == 200, f"GET {url} failed: {resp.text}"
        validate(instance=resp.json(), schema=schema)


def test_post_schemas_conform():
    for url, payload, schema_file in POST_ENDPOINTS:
        schema = load_schema(schema_file)
        resp = client.post(url, params=payload)
        assert resp.status_code == 200, f"POST {url} failed: {resp.text}"
        validate(instance=resp.json(), schema=schema)
