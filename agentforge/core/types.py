from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskType(str, Enum):
    COLLECT = "collect"
    SELECT = "select"
    TRAIN = "train"
    EVALUATE = "evaluate"
    ANALYZE = "analyze"
    IMPROVE = "improve"
    REPORT = "report"


@dataclass(slots=True)
class ResearchGoal:
    statement: str
    budget_usd: float = 100.0
    max_iterations: int = 3
    target_metric: float = 0.9
    task_type: str = "language_understanding"
    iteration_cost_usd: float = 5.0
    time_budget_minutes: int = 60
    dataset_hint: str = "auto"


@dataclass(slots=True)
class PlannedTask:
    id: str
    task_type: TaskType
    description: str
    depends_on: list[str] = field(default_factory=list)


@dataclass(slots=True)
class LoopState:
    iteration: int = 0
    best_metric: float = 0.0
    total_spend_usd: float = 0.0
    history: list[dict[str, Any]] = field(default_factory=list)
    stop_reason: str = "max_iterations_reached"
    checkpoints: list[dict[str, Any]] = field(default_factory=list)
    report: dict[str, Any] = field(default_factory=dict)
    traces: list[dict[str, Any]] = field(default_factory=list)
