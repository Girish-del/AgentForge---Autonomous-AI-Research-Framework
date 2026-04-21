class IntentParser:
    def parse(self, statement: str) -> dict[str, str]:
        text = statement.lower()
        task_type = "agent_planning"
        if "tool" in text or "function" in text:
            task_type = "agent_tool_use"
        elif "memory" in text or "retrieve" in text:
            task_type = "agent_memory"
        elif "multi-agent" in text or "collaborat" in text:
            task_type = "agent_collaboration"
        elif "eval" in text or "benchmark" in text:
            task_type = "agent_evaluation"
        return {"task_type": task_type}
