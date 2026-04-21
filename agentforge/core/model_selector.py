MODEL_MATRIX: dict[str, tuple[str, str]] = {
    "agent_planning": ("claude_opus_planner", "gpt_4o_planner"),
    "agent_tool_use": ("gpt_4o_toolformer", "claude_sonnet_tools"),
    "agent_memory": ("claude_sonnet_memory", "gpt_4o_mini_memory"),
    "agent_collaboration": ("claude_multi_agent", "gpt_swarm"),
    "agent_evaluation": ("deepseek_eval_runner", "claude_eval"),
}


def select_model(task_type: str, prefer_open_source: bool = True) -> dict[str, str]:
    if task_type not in MODEL_MATRIX:
        raise ValueError(f"Unknown task_type: {task_type}")
    preferred, fallback = MODEL_MATRIX[task_type]
    selected = preferred
    if prefer_open_source and preferred.startswith(("claude", "gpt", "gemini")):
        selected = fallback
    return {"selected": selected, "fallback": fallback}
