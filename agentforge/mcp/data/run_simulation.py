def run_simulation(goal_statement: str) -> dict[str, str | int]:
    from agentforge.robotics.ros_connector import ROSGazeboConnector

    connector = ROSGazeboConnector()
    rollout = connector.run_rollout(goal_statement, episodes=20)
    return {
        "sim_id": str(rollout["engine"]),
        "episodes": int(rollout["episodes"]),
        "status": str(rollout["status"]),
        "notes": str(rollout["notes"]),
    }

