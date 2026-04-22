def generate_synthetic(goal_statement: str, count: int = 100) -> dict[str, str | int]:
    return {
        "generator": "vlm-synthetic-stub",
        "samples_generated": count,
        "status": "completed",
        "notes": f"Synthetic data generated for: {goal_statement}",
    }

