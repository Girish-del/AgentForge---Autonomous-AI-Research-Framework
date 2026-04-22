from agentforge.agents.data_agent import DataAgent
from agentforge.agents.eval_agent import EvalAgent
from agentforge.agents.failure_analyst import FailureAnalyst
from agentforge.agents.improvement_agent import ImprovementAgent
from agentforge.agents.training_agent import TrainingAgent
from agentforge.core.reporting import generate_research_report
from agentforge.core.model_selector import select_model
from agentforge.core.orchestrator import Orchestrator
from agentforge.core.types import LoopState, ResearchGoal
from agentforge.mcp.memory.retrieve_similar import retrieve_similar
from agentforge.mcp.memory.store_experiment import store_experiment
from agentforge.mcp.memory.update_skill_library import update_skill_library
from agentforge.memory.experiment_log import ExperimentLog
from agentforge.observability.tracer import TraceRecorder


class AgentLoop:
    def __init__(self) -> None:
        self.orchestrator = Orchestrator()
        self.data_agent = DataAgent()
        self.training_agent = TrainingAgent()
        self.eval_agent = EvalAgent()
        self.failure_analyst = FailureAnalyst()
        self.improvement_agent = ImprovementAgent()

    def run(self, goal: ResearchGoal) -> LoopState:
        log = ExperimentLog()
        tracer = TraceRecorder()
        state = LoopState()
        plan = self.orchestrator.plan(goal)
        prior_context = retrieve_similar(goal.statement)
        log.add_event(
            "plan_created",
            {
                "tasks": [task.id for task in plan],
                "budget_usd": goal.budget_usd,
                "max_iterations": goal.max_iterations,
                "prior_matches": len(prior_context["matches"]),
            },
        )
        tracer.emit("plan_created", {"task_count": len(plan), "goal": goal.statement})

        dataset = {"dataset_id": ""}

        while state.iteration < goal.max_iterations:
            if (state.total_spend_usd + goal.iteration_cost_usd) > goal.budget_usd:
                state.stop_reason = "budget_exhausted"
                log.add_event(
                    "budget_guard_stop",
                    {
                        "iteration": state.iteration,
                        "spend": state.total_spend_usd,
                        "budget": goal.budget_usd,
                    },
                )
                break

            state.iteration += 1
            tracer.emit("iteration_started", {"iteration": state.iteration})
            routing = {"selected": "", "fallback": "", "task_type": goal.task_type}
            trained = {"run_id": "", "checkpoint": ""}
            eval_result = {"primary_metric": 0.0, "latency_ms": 0.0}
            analysis = {"top_failure_mode": ""}
            improvement = {"strategy": "", "next_model": "", "augmentation_status": "skipped"}

            for task in plan:
                if task.id == "collect":
                    dataset = self.data_agent.collect(goal.statement, goal.dataset_hint)
                elif task.id == "select":
                    routing = select_model(goal.task_type)
                elif task.id == "train":
                    trained = self.training_agent.train(
                        dataset["dataset_id"],
                        routing["selected"],
                        state.iteration,
                        routing["task_type"],
                    )
                elif task.id == "evaluate":
                    eval_result = self.eval_agent.evaluate(trained["run_id"], state.iteration)
                elif task.id == "analyze":
                    analysis = self.failure_analyst.analyze(eval_result["primary_metric"])
                elif task.id == "improve":
                    improvement = self.improvement_agent.propose(
                        analysis["top_failure_mode"],
                        routing["selected"],
                        routing["fallback"],
                    )

            state.best_metric = max(state.best_metric, eval_result["primary_metric"])
            state.total_spend_usd += goal.iteration_cost_usd
            history_entry = {
                "iteration": state.iteration,
                "model": routing["selected"],
                "next_model": improvement["next_model"],
                "dataset": dataset["dataset_id"],
                "metric": eval_result["primary_metric"],
                "latency_ms": eval_result["latency_ms"],
                "failure_mode": analysis["top_failure_mode"],
                "improvement": improvement["strategy"],
                "augmentation_status": improvement["augmentation_status"],
                "checkpoint": trained["checkpoint"],
            }
            state.history.append(history_entry)
            state.checkpoints.append(
                {
                    "iteration": state.iteration,
                    "run_id": trained["run_id"],
                    "checkpoint": trained["checkpoint"],
                }
            )
            store_experiment(history_entry)
            log.add_event("iteration_complete", history_entry)
            tracer.emit("iteration_completed", history_entry)

            if state.best_metric >= goal.target_metric:
                state.stop_reason = "target_reached"
                update_skill_library("targeted_finetune")
                log.add_event("target_reached", {"best_metric": state.best_metric})
                tracer.emit("target_reached", {"best_metric": state.best_metric})
                break

        if state.stop_reason == "max_iterations_reached" and state.iteration >= goal.max_iterations:
            log.add_event("max_iterations_stop", {"iteration": state.iteration})
            tracer.emit("max_iterations_stop", {"iteration": state.iteration})

        state.report = generate_research_report(
            statement=goal.statement,
            history=state.history,
            best_metric=state.best_metric,
            stop_reason=state.stop_reason,
        )
        state.traces = tracer.traces

        return state
