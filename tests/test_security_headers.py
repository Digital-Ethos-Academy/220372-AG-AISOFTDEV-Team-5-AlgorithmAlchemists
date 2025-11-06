from fastapi.testclient import TestClient
from app.main import app

def test_security_headers_present():
    client = TestClient(app)
    r = client.get("/overview")
    for header in [
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Referrer-Policy",
        "Permissions-Policy",
        "Content-Security-Policy",
    ]:
        assert header in r.headers
