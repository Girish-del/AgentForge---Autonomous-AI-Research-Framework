class EvalAgent:
    def evaluate(self, run_id: str, iteration: int) -> dict[str, float]:
        # Deterministic baseline progression for Phase 1.
        metric = min(0.55 + (0.1 * iteration), 0.95)
        return {"primary_metric": metric, "latency_ms": 25.0 + iteration}
