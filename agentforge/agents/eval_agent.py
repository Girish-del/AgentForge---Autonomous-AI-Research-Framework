class EvalAgent:
    def evaluate(self, run_id: str, iteration: int) -> dict[str, float]:
        from agentforge.mcp.evaluation.compute_metrics import compute_metrics
        from agentforge.mcp.evaluation.run_eval_suite import run_eval_suite

        suite = run_eval_suite(run_id, iteration)
        metrics = compute_metrics(float(suite["primary_metric"]))
        return {
            "primary_metric": float(suite["primary_metric"]),
            "latency_ms": float(suite["latency_ms"]),
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1": metrics["f1"],
        }
