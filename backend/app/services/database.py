import json
import os
from typing import Any

from psycopg import connect
from psycopg.rows import dict_row
from psycopg.types.json import Json
from starlette.applications import Starlette


class DatabaseService:
    """Lightweight PostgreSQL service for run history persistence."""

    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL", "")
        self._connection_error: str | None = None
        self.connected = False

    def connect(self) -> None:
        if not self.database_url:
            self._connection_error = "DATABASE_URL is not configured."
            self.connected = False
            return
        try:
            with connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS run_history (
                            id BIGSERIAL PRIMARY KEY,
                            statement TEXT NOT NULL,
                            task_type TEXT NOT NULL,
                            target_metric DOUBLE PRECISION NOT NULL,
                            best_metric DOUBLE PRECISION NOT NULL,
                            iterations INTEGER NOT NULL,
                            total_spend_usd DOUBLE PRECISION NOT NULL,
                            history JSONB NOT NULL,
                            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                        );
                        """
                    )
                conn.commit()
            self.connected = True
            self._connection_error = None
        except Exception as exc:
            self.connected = False
            self._connection_error = str(exc)

    def save_run(self, payload: dict[str, Any]) -> None:
        if not self.connected:
            return
        with connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO run_history (
                        statement,
                        task_type,
                        target_metric,
                        best_metric,
                        iterations,
                        total_spend_usd,
                        history
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        payload["statement"],
                        payload["task_type"],
                        payload["target_metric"],
                        payload["best_metric"],
                        payload["iterations"],
                        payload["total_spend_usd"],
                        Json(payload["history"]),
                    ),
                )
            conn.commit()

    def get_runs(self, limit: int = 10) -> list[dict[str, Any]]:
        if not self.connected:
            return []
        with connect(self.database_url, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        statement,
                        task_type,
                        target_metric,
                        best_metric,
                        iterations,
                        total_spend_usd,
                        history,
                        created_at
                    FROM run_history
                    ORDER BY created_at DESC
                    LIMIT %s;
                    """,
                    (limit,),
                )
                rows = cur.fetchall()

        return [
            {
                **row,
                "created_at": row["created_at"].isoformat(),
                "history": row["history"] if isinstance(row["history"], list) else json.loads(row["history"]),
            }
            for row in rows
        ]

    def health(self) -> dict[str, str]:
        if self.connected:
            return {"database": "connected"}
        if self._connection_error:
            return {"database": "disconnected", "reason": self._connection_error}
        return {"database": "disconnected"}


def get_database_service(app: Starlette) -> DatabaseService:
    service = getattr(app.state, "database_service", None)
    if service is None:
        service = DatabaseService()
        service.connect()
        app.state.database_service = service
    return service
