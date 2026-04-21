from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login() -> None:
    response = client.post("/api/auth/login", json={"email": "demo@agentforge.ai", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()
