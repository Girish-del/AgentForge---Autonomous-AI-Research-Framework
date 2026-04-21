from app.agents.domain_agent import DomainAgent
from app.agents.support_agent import SupportAgent
from app.models.domain import LoopState, PlannedTask, ResearchGoal, TaskType
from app.orchestrator.conflict_detector import ConflictDetector
from app.orchestrator.intent_parser import IntentParser
from app.orchestrator.task_router import TaskRouter


class Pipeline:
    def __init__(self) -> None:
        self.intent_parser = IntentParser()
        self.task_router = TaskRouter()
        self.conflict_detector = ConflictDetector()
        self.support_agent = SupportAgent()
        self.domain_agent = DomainAgent()

    def plan(self, goal: ResearchGoal) -> list[PlannedTask]:
        return [
            PlannedTask("collect", TaskType.COLLECT, "Collect data"),
            PlannedTask("select", TaskType.SELECT, "Select model", ["collect"]),
            PlannedTask("train", TaskType.TRAIN, "Train model", ["select"]),
            PlannedTask("evaluate", TaskType.EVALUATE, "Evaluate model", ["train"]),
            PlannedTask("analyze", TaskType.ANALYZE, "Analyze failures", ["evaluate"]),
            PlannedTask("improve", TaskType.IMPROVE, "Improve strategy", ["analyze"]),
            PlannedTask("report", TaskType.REPORT, "Generate report", ["improve"]),
        ]

    def run(self, goal: ResearchGoal) -> LoopState:
        inferred = self.intent_parser.parse(goal.statement)
        goal.task_type = goal.task_type or inferred["task_type"]
        conflicts = self.conflict_detector.detect(goal.budget_usd, goal.max_iterations, goal.iteration_cost_usd)

        state = LoopState()
        active_workflow = "baseline_workflow"
        for _ in range(goal.max_iterations):
            if state.total_spend_usd + goal.iteration_cost_usd > goal.budget_usd:
                break
            state.iteration += 1
            routing = self.task_router.select_model(goal.task_type)
            data_summary = self._collect_data(goal, state.iteration)
            metric = self._train_and_evaluate(state.iteration)
            failure = "insufficient_agent_tool_reliability" if metric < 0.7 else "agent_reasoning_drift"
            strategy = self.support_agent.suggest(failure)
            self.domain_agent.validate_strategy(strategy)
            workflow_update = self._update_workflow(failure, state.iteration)
            model_switch = routing["fallback"] if state.iteration > 1 else routing["selected"]
            rerun_triggered = state.iteration < goal.max_iterations
            state.best_metric = max(state.best_metric, metric)
            state.total_spend_usd += goal.iteration_cost_usd
            active_workflow = workflow_update["next_workflow"]
            state.history.append(
                {
                    "iteration": state.iteration,
                    "data_collection": data_summary,
                    "training_status": "completed",
                    "evaluation_result": {"metric": metric, "target_metric": goal.target_metric},
                    "metric": metric,
                    "failure_mode": failure,
                    "improvement": strategy,
                    "model_change": {
                        "previous_model": routing["selected"],
                        "new_model": model_switch,
                    },
                    "workflow_change": workflow_update,
                    "rerun_experiment": rerun_triggered,
                    "active_workflow": active_workflow,
                    "conflicts": conflicts,
                }
            )
            if state.best_metric >= goal.target_metric:
                break
        return state

    def _collect_data(self, goal: ResearchGoal, iteration: int) -> dict[str, str | int]:
        return {
            "source": "agent_telemetry_and_task_logs",
            "task_type": goal.task_type,
            "samples_collected": 100 + (iteration * 20),
        }

    def _train_and_evaluate(self, iteration: int) -> float:
        return min(0.55 + (0.1 * iteration), 0.95)

    def _update_workflow(self, failure_mode: str, iteration: int) -> dict[str, str]:
        next_workflow = "tool_reliability_workflow" if "tool" in failure_mode else "reasoning_stability_workflow"
        return {
            "reason": failure_mode,
            "next_workflow": f"{next_workflow}_v{iteration}",
        }
