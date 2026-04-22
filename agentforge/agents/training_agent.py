class TrainingAgent:
    def train(self, dataset_id: str, model_name: str, iteration: int, task_type: str) -> dict[str, str]:
        from agentforge.mcp.training.hyperparameter_search import hyperparameter_search
        from agentforge.mcp.training.launch_training import launch_training

        params = hyperparameter_search(task_type)
        run = launch_training(dataset_id, model_name, iteration)
        run["hparams"] = (
            f'optimizer={params["optimizer"]},lr={params["learning_rate"]},batch={int(params["batch_size"])}'
        )
        return run
