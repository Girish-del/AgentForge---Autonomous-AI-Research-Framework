from typing import Literal

from pydantic import BaseModel, Field


class GoalRequest(BaseModel):
    statement: str = Field(min_length=5)
    budget_usd: float = Field(default=100.0, ge=1.0)
    max_iterations: int = Field(default=3, ge=1, le=20)
    target_metric: float = Field(default=0.9, ge=0.0, le=1.0)
    task_type: Literal[
        "image_classification",
        "object_detection",
        "language_understanding",
        "vision_language",
        "trajectory_prediction",
    ] = Field(default="image_classification")


class RunResponse(BaseModel):
    iterations: int
    best_metric: float
    total_spend_usd: float
    history: list[dict]
