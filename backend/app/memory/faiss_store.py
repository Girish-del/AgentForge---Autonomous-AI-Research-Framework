class FaissStore:
    def __init__(self) -> None:
        self._index: list[list[float]] = []

    def add(self, vector: list[float]) -> int:
        self._index.append(vector)
        return len(self._index) - 1

    def count(self) -> int:
        return len(self._index)
