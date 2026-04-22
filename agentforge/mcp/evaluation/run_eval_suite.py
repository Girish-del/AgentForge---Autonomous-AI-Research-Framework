def run_eval_suite(run_id: str, iteration: int) -> dict[str, str | float]:
    metric = min(0.55 + (0.1 * iteration), 0.96)
    return {
        "run_id": run_id,
        "primary_metric": metric,
        "latency_ms": 25.0 + iteration,
        "status": "completed",
    }

