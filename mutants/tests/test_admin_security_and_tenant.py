import os
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def setup_module(module):  # noqa: D401
    os.environ['ADMIN_API_KEY'] = 'secret-admin'


def test_admin_unauthorized():
    r = client.get('/admin/teams')
    assert r.status_code == 401


def test_admin_list_authorized():
    r = client.get('/admin/teams', headers={'X-Admin-Token': 'secret-admin'})
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_tenant_isolation_create_and_list():
    # create a team in tenant alpha
    payload = {"id": "TA1", "name": "Alpha Team", "mission": "Alpha", "responsibilities": ["API"], "parent_team_id": None}
    r = client.post('/admin/teams', headers={'X-Admin-Token': 'secret-admin', 'X-Tenant-Id': 'alpha'}, json=payload)
    assert r.status_code == 200, r.text
    # list default tenant should NOT include TA1
    default_list = client.get('/admin/teams', headers={'X-Admin-Token': 'secret-admin'}).json()
    assert all(t['id'] != 'TA1' for t in default_list)
    # list alpha tenant should include TA1
    alpha_list = client.get('/admin/teams', headers={'X-Admin-Token': 'secret-admin', 'X-Tenant-Id': 'alpha'}).json()
    assert any(t['id'] == 'TA1' for t in alpha_list)


def test_recommendation_debug_endpoint():
    r = client.get('/admin/recommendation/debug', params={'user_id': 'u1'}, headers={'X-Admin-Token': 'secret-admin'})
    assert r.status_code == 200
    data = r.json()
    assert 'candidates' in data and len(data['candidates']) >= 1
    # Ensure breakdown keys present
    first = data['candidates'][0]
    assert 'breakdown' in first
