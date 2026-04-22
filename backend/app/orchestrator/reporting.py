from typing import Any


def generate_research_report(
    statement: str,
    history: list[dict[str, Any]],
    best_metric: float,
    stop_reason: str,
) -> dict[str, Any]:
    iterations = len(history)
    latest = history[-1] if history else {}
    return {
        "title": "AgentForge Research Report",
        "goal": statement,
        "iterations": iterations,
        "best_metric": best_metric,
        "stop_reason": stop_reason,
        "final_model": latest.get("model_change", {}).get("new_model", "unknown"),
        "top_failure_mode": latest.get("failure_mode", "unknown"),
    }

