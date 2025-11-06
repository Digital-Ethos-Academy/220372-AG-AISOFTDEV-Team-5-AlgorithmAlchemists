from fastapi.testclient import TestClient

from app.main import app


def test_fr4_qa_fallback_low_confidence():
    client = TestClient(app)
    resp = client.post('/qa', params={'question': 'unknown token phrase'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['confidence'] < 0.85
    assert data['escalation'] == 'Consult Mentor'
