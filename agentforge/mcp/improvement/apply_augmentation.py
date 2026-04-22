def apply_augmentation(strategy: str) -> dict[str, str]:
    return {
        "strategy": strategy,
        "status": "applied",
        "augmentation_pipeline": "standard_hard_negative_mixer",
    }

