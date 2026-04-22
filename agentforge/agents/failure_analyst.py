class FailureAnalyst:
    def analyze(self, metric: float) -> dict[str, str]:
        from agentforge.mcp.evaluation.failure_clustering import failure_clustering

        return failure_clustering(metric)
