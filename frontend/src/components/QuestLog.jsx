const formatPercent = (value) => `${(Number(value || 0) * 100).toFixed(1)}%`;

const formatModelChange = (entry) => {
  const change = entry.model_change;
  if (!change) return null;
  if (change.previous_model === change.new_model) return change.new_model;
  return `${change.previous_model} → ${change.new_model}`;
};

function QuestLog({ history = [], target = 0.9 }) {
  if (!history.length) {
    return (
      <div className="empty-state">
        <span className="empty-state__icon" aria-hidden="true">📜</span>
        <p>No quests logged yet. Initiate one to populate the journal.</p>
      </div>
    );
  }

  return (
    <ul className="quest-log" aria-label="Iteration history">
      {history.map((entry) => {
        const reached = (entry.metric || 0) >= target;
        const xpGain = 25 + (reached ? 100 : 0);
        const modelText = formatModelChange(entry) || "—";
        const failure = entry.failure_mode
          ? entry.failure_mode.replace(/_/g, " ")
          : "no failures detected";

        return (
          <li key={entry.iteration} className="quest-log__item">
            <span className="quest-log__num" aria-hidden="true">
              {entry.iteration}
            </span>
            <div className="quest-log__body">
              <span className="quest-log__title">Iteration {entry.iteration}</span>
              <p className="quest-log__detail">
                Failure mode: <strong>{failure}</strong>. Model: <strong>{modelText}</strong>.
                {entry.workflow_change?.next_workflow ? (
                  <>
                    {" "}Workflow: <strong>{entry.workflow_change.next_workflow}</strong>.
                  </>
                ) : null}
              </p>
            </div>
            <div className="quest-log__metrics">
              <span className={`metric-pill ${reached ? "metric-pill--target" : "metric-pill--metric"}`}>
                {formatPercent(entry.metric)}
              </span>
              <span className="metric-pill metric-pill--xp">+{xpGain} XP</span>
            </div>
          </li>
        );
      })}
    </ul>
  );
}

export default QuestLog;
