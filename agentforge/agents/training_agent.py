class TrainingAgent:
    def train(self, dataset_id: str, model_name: str) -> dict[str, str]:
        run_id = f"train-{dataset_id}-{model_name}".replace("_", "-")
        return {"run_id": run_id, "checkpoint": f"{run_id}/checkpoint.pt"}
