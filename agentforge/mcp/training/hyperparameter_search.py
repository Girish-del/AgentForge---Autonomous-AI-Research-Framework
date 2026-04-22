def hyperparameter_search(task_type: str) -> dict[str, str | float]:
    return {
        "task_type": task_type,
        "optimizer": "adamw",
        "learning_rate": 0.0003,
        "batch_size": 32.0,
    }

