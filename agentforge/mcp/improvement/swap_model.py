def swap_model(current_model: str, fallback_model: str) -> dict[str, str]:
    next_model = fallback_model if current_model != fallback_model else current_model
    return {"previous_model": current_model, "next_model": next_model}

