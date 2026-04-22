def propose_fix(failure_mode: str) -> dict[str, str]:
    strategy_map = {
        "data_distribution_shift": "augment_data_with_hard_negatives",
        "model_capacity_limit": "swap_to_larger_backbone",
        "rare_edge_cases": "targeted_finetune",
    }
    strategy = strategy_map.get(failure_mode, "targeted_finetune")
    return {"strategy": strategy, "failure_mode": failure_mode}

