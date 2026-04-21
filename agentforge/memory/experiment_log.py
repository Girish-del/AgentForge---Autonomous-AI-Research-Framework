from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class ExperimentLog:
    events: list[dict[str, Any]] = field(default_factory=list)

    def add_event(self, event_type: str, payload: dict[str, Any]) -> None:
        self.events.append(
            {
                "event_type": event_type,
                "payload": payload,
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )
