class EmbeddingService:
    """Sentence-transformer abstraction layer."""

    def embed(self, text: str) -> list[float]:
        # Placeholder deterministic embedding.
        return [float((ord(c) % 10) / 10) for c in text[:16]]
