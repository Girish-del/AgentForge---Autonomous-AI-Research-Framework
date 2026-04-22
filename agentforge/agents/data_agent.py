class DataAgent:
    def collect(self, goal_statement: str, dataset_hint: str = "auto") -> dict[str, str]:
        from agentforge.mcp.data.fetch_dataset import fetch_dataset
        from agentforge.mcp.data.generate_synthetic import generate_synthetic
        from agentforge.mcp.data.label_with_vlm import label_with_vlm
        from agentforge.mcp.data.run_simulation import run_simulation

        base = fetch_dataset(goal_statement, dataset_hint)
        sim = run_simulation(goal_statement)
        synthetic = generate_synthetic(goal_statement)
        labels = label_with_vlm(base["dataset_id"])
        return {
            "dataset_id": base["dataset_id"],
            "source": f'{base["source"]}+{sim["sim_id"]}',
            "notes": base["notes"],
            "synthetic_samples": str(synthetic["samples_generated"]),
            "labels_status": labels["status"],
        }
