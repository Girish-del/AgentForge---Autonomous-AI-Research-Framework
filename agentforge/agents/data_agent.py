class DataAgent:
    def collect(self, goal_statement: str) -> dict[str, str]:
        return {
            "dataset_id": "synthetic-foundation-dataset-v1",
            "source": "stub",
            "notes": f"Prepared starter dataset for: {goal_statement}",
        }
