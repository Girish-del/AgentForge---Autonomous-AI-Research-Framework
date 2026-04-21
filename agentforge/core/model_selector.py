MODEL_MATRIX: dict[str, tuple[str, str]] = {
    "image_classification": ("vit_base_patch16_224", "resnet50"),
    "object_detection": ("yolov9", "faster_rcnn"),
    "language_understanding": ("claude_sonnet", "gpt_4o_mini"),
    "vision_language": ("gemini_1_5_pro", "gpt_4v"),
    "trajectory_prediction": ("trajectory_transformer", "lstm"),
}


def select_model(task_type: str, prefer_open_source: bool = True) -> dict[str, str]:
    if task_type not in MODEL_MATRIX:
        raise ValueError(f"Unknown task_type: {task_type}")
    preferred, fallback = MODEL_MATRIX[task_type]
    selected = preferred
    if prefer_open_source and preferred.startswith(("claude", "gpt", "gemini")):
        selected = fallback
    return {"selected": selected, "fallback": fallback}
