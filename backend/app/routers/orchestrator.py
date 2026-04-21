from fastapi import APIRouter

from app.models.domain import ResearchGoal
from app.models.schemas import GoalRequest, RunResponse
from app.orchestrator.pipeline import Pipeline

router = APIRouter(tags=["orchestrator"])
pipeline = Pipeline()


@router.post("/orchestrator/run", response_model=RunResponse)
def run_pipeline(payload: GoalRequest) -> RunResponse:
    result = pipeline.run(
        ResearchGoal(
            statement=payload.statement,
            budget_usd=payload.budget_usd,
            max_iterations=payload.max_iterations,
            target_metric=payload.target_metric,
            task_type=payload.task_type,
        )
    )
    return RunResponse(
        iterations=result.iteration,
        best_metric=result.best_metric,
        total_spend_usd=result.total_spend_usd,
        history=result.history,
    )
