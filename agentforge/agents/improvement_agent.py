class ImprovementAgent:
    def propose(self, failure_mode: str, current_model: str, fallback_model: str) -> dict[str, str]:
        from agentforge.mcp.improvement.apply_augmentation import apply_augmentation
        from agentforge.mcp.improvement.propose_fix import propose_fix
        from agentforge.mcp.improvement.swap_model import swap_model

        proposed = propose_fix(failure_mode)
        augmentation = apply_augmentation(proposed["strategy"])
        swap = swap_model(current_model, fallback_model)
        return {
            "strategy": proposed["strategy"],
            "augmentation_status": augmentation["status"],
            "next_model": swap["next_model"],
        }
