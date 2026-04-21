class ConflictDetector:
    def detect(self, budget_usd: float, max_iterations: int, iteration_cost_usd: float) -> list[str]:
        conflicts: list[str] = []
        if (max_iterations * iteration_cost_usd) > budget_usd:
            conflicts.append("budget may stop run before max_iterations")
        return conflicts
