from fastapi import FastAPI

from agentforge.api.schemas import GoalRequest, RunResponse
from agentforge.core.agent_loop import AgentLoop
from agentforge.core.types import ResearchGoal

app = FastAPI(title="AgentForge API", version="0.1.0")
agent_loop = AgentLoop()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/research/run", response_model=RunResponse)
def run_research(goal: GoalRequest) -> RunResponse:
    result = agent_loop.run(
        ResearchGoal(
            statement=goal.statement,
            budget_usd=goal.budget_usd,
            max_iterations=goal.max_iterations,
            target_metric=goal.target_metric,
            task_type=goal.task_type,
        )
    )
    return RunResponse(
        iterations=result.iteration,
        best_metric=result.best_metric,
        total_spend_usd=result.total_spend_usd,
        history=result.history,
    )
