def fetch_dataset(goal_statement: str, dataset_hint: str = "auto") -> dict[str, str]:
    resolved = dataset_hint if dataset_hint != "auto" else "hf/agentforge-foundation-v1"
    return {
        "dataset_id": resolved,
        "source": "huggingface",
        "notes": f"Fetched dataset for goal: {goal_statement}",
    }

