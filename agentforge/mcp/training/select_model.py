MODEL_SELECTOR_MATRIX: dict[str, tuple[str, str]] = {
    "image_classification": ("vit_base_patch16", "resnet50"),
    "object_detection": ("yolo_v9", "faster_rcnn"),
    "language_understanding": ("claude_sonnet", "gpt_4o_mini"),
    "vision_language": ("gemini_1_5_pro", "gpt_4v"),
    "trajectory_prediction": ("trajectory_transformer", "lstm"),
    "low_latency_inference": ("quantized_onnx", "torchscript"),
    "generative_data": ("sdxl", "dalle_3"),
}


def select_model(task_type: str, prefer_open_source: bool = True) -> dict[str, str]:
    if task_type not in MODEL_SELECTOR_MATRIX:
        task_type = "language_understanding"
    preferred, fallback = MODEL_SELECTOR_MATRIX[task_type]
    selected = preferred
    if prefer_open_source and preferred in {"claude_sonnet", "gpt_4o_mini", "gemini_1_5_pro", "gpt_4v", "dalle_3"}:
        selected = fallback
    return {"selected": selected, "fallback": fallback, "task_type": task_type}

