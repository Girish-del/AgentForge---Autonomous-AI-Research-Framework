class VectorStore:
    """Phase-1 placeholder for pgvector-backed memory."""

    def __init__(self) -> None:
        self._connected = False

    def connect(self) -> None:
        self._connected = True

    def is_connected(self) -> bool:
        return self._connected
