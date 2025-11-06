from fastapi.testclient import TestClient
from app.main import app


def test_fr8_gaps_simulation_contains_gap():
    client = TestClient(app)
    resp = client.get('/gaps')
    assert resp.status_code == 200
    data = resp.json()
    assert data['summary']['gap_count'] == 1
    assert len(data['gaps']) == 1
    gap = data['gaps'][0]
    assert gap['team_id'] == 'T5'
    assert gap['type'] == 'missing_mission'
