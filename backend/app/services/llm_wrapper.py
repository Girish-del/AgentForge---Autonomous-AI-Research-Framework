class LLMWrapper:
    """Stub LLM adapter to keep provider logic centralized."""

    def summarize(self, text: str) -> str:
        return f"Summary: {text[:100]}"
