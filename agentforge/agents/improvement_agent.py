class ImprovementAgent:
    def propose(self, failure_mode: str) -> dict[str, str]:
        strategy_map = {
            "insufficient_data_diversity": "augment_data_with_hard_negatives",
            "model_capacity_limit": "swap_to_larger_backbone",
            "minor_edge_case_failures": "targeted_finetune",
        }
        strategy = strategy_map.get(failure_mode, "targeted_finetune")
        return {"strategy": strategy}
