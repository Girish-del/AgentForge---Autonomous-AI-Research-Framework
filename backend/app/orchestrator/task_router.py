MODEL_MATRIX: dict[str, tuple[str, str]] = {
    "agent_planning": ("claude_opus_planner", "gpt_4o_planner"),
    "agent_tool_use": ("gpt_4o_toolformer", "claude_sonnet_tools"),
    "agent_memory": ("claude_sonnet_memory", "gpt_4o_mini_memory"),
    "agent_collaboration": ("claude_multi_agent", "gpt_swarm"),
    "agent_evaluation": ("deepseek_eval_runner", "claude_eval"),
    "image_classification": ("vit_base_patch16", "resnet50"),
    "object_detection": ("yolo_v9", "faster_rcnn"),
    "language_understanding": ("claude_sonnet", "gpt_4o_mini"),
    "vision_language": ("gemini_1_5_pro", "gpt_4v"),
    "trajectory_prediction": ("trajectory_transformer", "lstm"),
    "low_latency_inference": ("quantized_onnx", "torchscript"),
    "generative_data": ("sdxl", "dalle_3"),
}


class TaskRouter:
    def select_model(self, task_type: str, prefer_open_source: bool = True) -> dict[str, str]:
        if task_type not in MODEL_MATRIX:
            task_type = "language_understanding"
        preferred, fallback = MODEL_MATRIX[task_type]
        selected = fallback if prefer_open_source and preferred.startswith(("claude", "gpt", "gemini")) else preferred
        return {"selected": selected, "fallback": fallback, "task_type": task_type}
