from fastapi import APIRouter, Request

from app.models.domain import ResearchGoal
from app.models.schemas import GoalRequest, RunHistoryRecord, RunResponse
from app.orchestrator.pipeline import Pipeline
from app.services.database import get_database_service

router = APIRouter(tags=["orchestrator"])
pipeline = Pipeline()


@router.post("/orchestrator/run", response_model=RunResponse)
def run_pipeline(payload: GoalRequest, request: Request) -> RunResponse:
    result = pipeline.run(
        ResearchGoal(
            statement=payload.statement,
            budget_usd=payload.budget_usd,
            max_iterations=payload.max_iterations,
            target_metric=payload.target_metric,
            task_type=payload.task_type,
        )
    )
    response = RunResponse(
        iterations=result.iteration,
        best_metric=result.best_metric,
        total_spend_usd=result.total_spend_usd,
        history=result.history,
    )
    try:
        get_database_service(request.app).save_run(
            {
                "statement": payload.statement,
                "task_type": payload.task_type,
                "target_metric": payload.target_metric,
                "best_metric": response.best_metric,
                "iterations": response.iterations,
                "total_spend_usd": response.total_spend_usd,
                "history": response.history,
            }
        )
    except Exception:
        # Database persistence is best-effort; do not fail an otherwise successful pipeline run.
        pass
    return response


@router.get("/orchestrator/runs", response_model=list[RunHistoryRecord])
def get_run_history(request: Request, limit: int = 10) -> list[RunHistoryRecord]:
    records = get_database_service(request.app).get_runs(limit=max(1, min(limit, 50)))
    return [RunHistoryRecord(**record) for record in records]
