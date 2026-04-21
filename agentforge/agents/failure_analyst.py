class FailureAnalyst:
    def analyze(self, metric: float) -> dict[str, str]:
        if metric < 0.7:
            issue = "insufficient_data_diversity"
        elif metric < 0.85:
            issue = "model_capacity_limit"
        else:
            issue = "minor_edge_case_failures"
        return {"top_failure_mode": issue}
