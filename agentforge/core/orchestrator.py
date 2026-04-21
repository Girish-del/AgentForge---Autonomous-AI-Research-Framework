from agentforge.core.types import PlannedTask, ResearchGoal, TaskType


class Orchestrator:
    """Turns high-level goals into a deterministic task plan."""

    def plan(self, goal: ResearchGoal) -> list[PlannedTask]:
        return [
            PlannedTask(
                id="collect",
                task_type=TaskType.COLLECT,
                description=f"Collect data for goal: {goal.statement}",
            ),
            PlannedTask(
                id="select",
                task_type=TaskType.SELECT,
                description="Select best model family",
                depends_on=["collect"],
            ),
            PlannedTask(
                id="train",
                task_type=TaskType.TRAIN,
                description="Train selected model",
                depends_on=["select"],
            ),
            PlannedTask(
                id="evaluate",
                task_type=TaskType.EVALUATE,
                description="Evaluate model performance",
                depends_on=["train"],
            ),
            PlannedTask(
                id="analyze",
                task_type=TaskType.ANALYZE,
                description="Analyze failure patterns",
                depends_on=["evaluate"],
            ),
            PlannedTask(
                id="improve",
                task_type=TaskType.IMPROVE,
                description="Propose and apply improvements",
                depends_on=["analyze"],
            ),
            PlannedTask(
                id="report",
                task_type=TaskType.REPORT,
                description="Generate experiment report",
                depends_on=["improve"],
            ),
        ]
