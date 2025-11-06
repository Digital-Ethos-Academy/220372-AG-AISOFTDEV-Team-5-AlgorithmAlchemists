import json

from fastapi.testclient import TestClient
from jsonschema import validate

from app.main import app

with open("schemas/quiz.schema.json") as f:
    LIST_SCHEMA = json.load(f)
with open("schemas/quiz-submit.schema.json") as f:
    SUBMIT_SCHEMA = json.load(f)

client = TestClient(app)

def test_fr6_quiz_list():
    resp = client.get("/quiz")
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=LIST_SCHEMA)
    assert len(data["questions"]) == 15


def test_fr6_quiz_submit_all_correct():
    answers = [q for q in [f"Q{i}" for i in range(1,16)]]
    resp = client.post("/quiz/submit", params={"answers": ",".join(answers)})
    assert resp.status_code == 200
    data = resp.json()
    validate(instance=data, schema=SUBMIT_SCHEMA)
    assert data["score"] == 15
