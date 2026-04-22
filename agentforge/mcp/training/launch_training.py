def launch_training(dataset_id: str, model_name: str, iteration: int) -> dict[str, str]:
    run_id = f"run-{dataset_id}-{model_name}-it{iteration}".replace("_", "-")
    return {
        "run_id": run_id,
        "checkpoint": f"checkpoints/{run_id}.pt",
        "status": "completed",
    }

