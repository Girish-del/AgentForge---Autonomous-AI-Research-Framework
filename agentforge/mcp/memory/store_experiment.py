from datetime import UTC, datetime
from typing import Any


def store_experiment(entry: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(entry)
    enriched["stored_at"] = datetime.now(UTC).isoformat()
    enriched["storage"] = "pgvector_stub"
    return enriched

