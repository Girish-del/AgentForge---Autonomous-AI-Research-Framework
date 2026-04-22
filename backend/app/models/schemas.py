from typing import Literal

from pydantic import BaseModel, Field


class GoalRequest(BaseModel):
    statement: str = Field(min_length=5)
    budget_usd: float = Field(default=100.0, ge=1.0)
    max_iterations: int = Field(default=3, ge=1, le=20)
    target_metric: float = Field(default=0.9, ge=0.0, le=1.0)
    task_type: Literal[
        "agent_planning",
        "agent_tool_use",
        "agent_memory",
        "agent_collaboration",
        "agent_evaluation",
        "image_classification",
        "object_detection",
        "language_understanding",
        "vision_language",
        "trajectory_prediction",
        "low_latency_inference",
        "generative_data",
    ] = "language_understanding"


class RunResponse(BaseModel):
    iterations: int
    best_metric: float
    total_spend_usd: float
    stop_reason: str = "max_iterations_reached"
    report: dict = Field(default_factory=dict)
    traces: list[dict] = Field(default_factory=list)
    history: list[dict]


class RunHistoryRecord(BaseModel):
    id: int
    statement: str
    task_type: str
    target_metric: float
    best_metric: float
    iterations: int
    total_spend_usd: float
    history: list[dict]
    created_at: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
