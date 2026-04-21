from agentforge.agents.data_agent import DataAgent
from agentforge.agents.eval_agent import EvalAgent
from agentforge.agents.failure_analyst import FailureAnalyst
from agentforge.agents.improvement_agent import ImprovementAgent
from agentforge.agents.training_agent import TrainingAgent
from agentforge.core.model_selector import select_model
from agentforge.core.orchestrator import Orchestrator
from agentforge.core.types import LoopState, ResearchGoal
from agentforge.memory.experiment_log import ExperimentLog


class AgentLoop:
    def __init__(self) -> None:
        self.orchestrator = Orchestrator()
        self.data_agent = DataAgent()
        self.training_agent = TrainingAgent()
        self.eval_agent = EvalAgent()
        self.failure_analyst = FailureAnalyst()
        self.improvement_agent = ImprovementAgent()
        self.log = ExperimentLog()

    def run(self, goal: ResearchGoal) -> LoopState:
        state = LoopState()
        plan = self.orchestrator.plan(goal)
        self.log.add_event("plan_created", {"tasks": [task.id for task in plan]})

        dataset = {}

        while state.iteration < goal.max_iterations:
            if (state.total_spend_usd + goal.iteration_cost_usd) > goal.budget_usd:
                self.log.add_event(
                    "budget_guard_stop",
                    {
                        "iteration": state.iteration,
                        "spend": state.total_spend_usd,
                        "budget": goal.budget_usd,
                    },
                )
                break

            state.iteration += 1
            routing = {"selected": "", "fallback": ""}
            trained = {"run_id": "", "checkpoint": ""}
            eval_result = {"primary_metric": 0.0, "latency_ms": 0.0}
            analysis = {"top_failure_mode": ""}
            improvement = {"strategy": ""}

            for task in plan:
                if task.id == "collect":
                    dataset = self.data_agent.collect(goal.statement)
                elif task.id == "select":
                    routing = select_model(goal.task_type)
                elif task.id == "train":
                    trained = self.training_agent.train(dataset["dataset_id"], routing["selected"])
                elif task.id == "evaluate":
                    eval_result = self.eval_agent.evaluate(trained["run_id"], state.iteration)
                elif task.id == "analyze":
                    analysis = self.failure_analyst.analyze(eval_result["primary_metric"])
                elif task.id == "improve":
                    improvement = self.improvement_agent.propose(analysis["top_failure_mode"])

            state.best_metric = max(state.best_metric, eval_result["primary_metric"])
            state.total_spend_usd += goal.iteration_cost_usd
            state.history.append(
                {
                    "iteration": state.iteration,
                    "model": routing["selected"],
                    "metric": eval_result["primary_metric"],
                    "failure_mode": analysis["top_failure_mode"],
                    "improvement": improvement["strategy"],
                }
            )
            self.log.add_event("iteration_complete", state.history[-1])

            if state.best_metric >= goal.target_metric:
                self.log.add_event("target_reached", {"best_metric": state.best_metric})
                break

        return state
