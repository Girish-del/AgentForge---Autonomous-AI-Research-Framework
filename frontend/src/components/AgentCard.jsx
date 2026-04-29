function AgentCard({ agent, status }) {
  const cls = ["agent-card"];
  if (status === "active") cls.push("is-active");
  if (status === "done") cls.push("is-done");

  const stateLabel =
    status === "active" ? "Working" : status === "done" ? "Done" : "Idle";

  return (
    <div className={cls.join(" ")} aria-label={`${agent.name} agent — ${stateLabel}`}>
      <div className="agent-card__head">
        <div className="agent-card__icon" aria-hidden="true">
          {agent.icon}
        </div>
        <div className="agent-card__title">
          <span className="agent-card__name">{agent.name}</span>
          <span className="agent-card__role">{agent.role}</span>
        </div>
      </div>
      <span className="agent-card__state">
        <span className="agent-card__state-dot" />
        {stateLabel}
      </span>
      <div className="agent-card__bar" aria-hidden="true">
        <div className="agent-card__bar-fill" />
      </div>
    </div>
  );
}

export default AgentCard;
