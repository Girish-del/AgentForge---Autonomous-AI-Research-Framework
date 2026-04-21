class DatabaseService:
    """Database abstraction for app services."""

    def __init__(self) -> None:
        self.connected = False

    def connect(self) -> None:
        self.connected = True

    def health(self) -> dict[str, str]:
        return {"database": "connected" if self.connected else "disconnected"}
