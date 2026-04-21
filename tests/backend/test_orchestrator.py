from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_orchestrator_run() -> None:
    response = client.post(
        "/api/orchestrator/run",
        json={
            "statement": "Improve pick and place success rate by 20%",
            "budget_usd": 50,
            "max_iterations": 2,
            "target_metric": 0.7,
            "task_type": "image_classification",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["iterations"] >= 1
    assert "history" in body
