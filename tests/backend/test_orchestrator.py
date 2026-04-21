from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_orchestrator_run() -> None:
    response = client.post(
        "/api/orchestrator/run",
        json={
            "statement": "Improve AI agent planning accuracy by 20%",
            "budget_usd": 50,
            "max_iterations": 2,
            "target_metric": 0.7,
            "task_type": "agent_planning",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["iterations"] >= 1
    assert "history" in body
    first_entry = body["history"][0]
    assert "data_collection" in first_entry
    assert first_entry["training_status"] == "completed"
    assert "evaluation_result" in first_entry
    assert "failure_mode" in first_entry
    assert "improvement" in first_entry
    assert "model_change" in first_entry
    assert "workflow_change" in first_entry
    assert "rerun_experiment" in first_entry
