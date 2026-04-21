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
        for _ in range(goal.max_iterations):
            if state.total_spend_usd + goal.iteration_cost_usd > goal.budget_usd:
                break
            state.iteration += 1
            routing = self.task_router.select_model(goal.task_type)
            metric = min(0.55 + (0.1 * state.iteration), 0.95)
            failure = "insufficient_data_diversity" if metric < 0.7 else "model_capacity_limit"
            strategy = self.support_agent.suggest(failure)
            self.domain_agent.validate_strategy(strategy)
            state.best_metric = max(state.best_metric, metric)
            state.total_spend_usd += goal.iteration_cost_usd
            state.history.append(
                {
                    "iteration": state.iteration,
                    "model": routing["selected"],
                    "metric": metric,
                    "failure_mode": failure,
                    "improvement": strategy,
                    "conflicts": conflicts,
                }
            )
            if state.best_metric >= goal.target_metric:
                break
        return state
