def label_with_vlm(dataset_id: str) -> dict[str, str]:
    return {
        "dataset_id": dataset_id,
        "labeler": "gemini-vision-stub",
        "status": "labeled",
    }

