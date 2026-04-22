from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class TraceRecorder:
    traces: list[dict[str, Any]] = field(default_factory=list)

    def emit(self, name: str, payload: dict[str, Any]) -> None:
        self.traces.append(
            {
                "name": name,
                "payload": payload,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )

