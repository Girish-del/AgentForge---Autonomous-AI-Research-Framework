import { useEffect, useState } from "react";

import Spinner from "../components/Spinner";
import apiClient from "../services/apiClient";

const toPercent = (value) => `${(Number(value || 0) * 100).toFixed(1)}%`;
const toCurrency = (value) => `$${Number(value || 0).toFixed(2)}`;

function DashboardPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    statement: "Improve AI agent task completion rate by 20%",
    budget_usd: 100,
    max_iterations: 3,
    target_metric: 0.8,
    task_type: "agent_planning",
  });

  const loadHistory = async () => {
    try {
      const response = await apiClient.get("/orchestrator/runs", { params: { limit: 8 } });
      setHistory(response.data);
    } catch {
      setHistory([]);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const updateField = (field, value) => {
    setForm((previous) => ({ ...previous, [field]: value }));
  };

  const runResearch = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const response = await apiClient.post("/orchestrator/run", form);
      setResult(response.data);
      await loadHistory();
    } catch {
      setError("Could not run experiment. Please verify backend connectivity.");
    } finally {
      setLoading(false);
    }
  };

  const runStatus =
    result && result.best_metric >= form.target_metric ? "Target Reached" : "In Progress";

  return (
    <section className="dashboard-grid">
      <article className="panel">
        <h2>Experiment Runner</h2>
        <p>Configure a goal and trigger an autonomous research loop.</p>
        <form className="form-grid" onSubmit={runResearch}>
          <label>
            Goal Statement
            <textarea
              value={form.statement}
              onChange={(event) => updateField("statement", event.target.value)}
              rows={3}
              required
            />
          </label>
          <label>
            Budget (USD)
            <input
              type="number"
              step="1"
              min="1"
              value={form.budget_usd}
              onChange={(event) => updateField("budget_usd", Number(event.target.value))}
              required
            />
          </label>
          <label>
            Max Iterations
            <input
              type="number"
              min="1"
              max="20"
              value={form.max_iterations}
              onChange={(event) => updateField("max_iterations", Number(event.target.value))}
              required
            />
          </label>
          <label>
            Target Metric (0-1)
            <input
              type="number"
              step="0.01"
              min="0"
              max="1"
              value={form.target_metric}
              onChange={(event) => updateField("target_metric", Number(event.target.value))}
              required
            />
          </label>
          <label>
            Task Type
            <select value={form.task_type} onChange={(event) => updateField("task_type", event.target.value)}>
              <option value="agent_planning">Agent Planning</option>
              <option value="agent_tool_use">Agent Tool Use</option>
              <option value="agent_memory">Agent Memory</option>
              <option value="agent_collaboration">Agent Collaboration</option>
              <option value="agent_evaluation">Agent Evaluation</option>
            </select>
          </label>
          <button type="submit">Run Experiment</button>
        </form>
        {loading && <Spinner />}
        {error && <p className="error">{error}</p>}
      </article>

      <article className="panel">
        <h3>Latest Result</h3>
        {!result ? (
          <p className="muted">No run yet.</p>
        ) : (
          <div className="result-report">
            <div className="result-header">
              <h4>Experiment Report</h4>
              <span className={`badge ${result.best_metric >= form.target_metric ? "badge-success" : "badge-warn"}`}>
                {runStatus}
              </span>
            </div>

            <div className="metric-grid">
              <div className="metric-card">
                <span>Best Metric</span>
                <strong>{toPercent(result.best_metric)}</strong>
              </div>
              <div className="metric-card">
                <span>Target Metric</span>
                <strong>{toPercent(form.target_metric)}</strong>
              </div>
              <div className="metric-card">
                <span>Iterations</span>
                <strong>{result.iterations}</strong>
              </div>
              <div className="metric-card">
                <span>Total Spend</span>
                <strong>{toCurrency(result.total_spend_usd)}</strong>
              </div>
            </div>

            <div className="table-wrap">
              <table className="result-table">
                <thead>
                  <tr>
                    <th>Iteration</th>
                    <th>Metric</th>
                    <th>Failure Mode</th>
                    <th>Model Change</th>
                    <th>Workflow</th>
                    <th>Rerun</th>
                  </tr>
                </thead>
                <tbody>
                  {result.history.map((entry) => (
                    <tr key={entry.iteration}>
                      <td>{entry.iteration}</td>
                      <td>{toPercent(entry.metric)}</td>
                      <td>{entry.failure_mode || "-"}</td>
                      <td>
                        {entry.model_change
                          ? `${entry.model_change.previous_model} -> ${entry.model_change.new_model}`
                          : "-"}
                      </td>
                      <td>{entry.active_workflow || entry.workflow_change?.next_workflow || "-"}</td>
                      <td>{entry.rerun_experiment ? "Yes" : "No"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </article>

      <article className="panel history-panel">
        <h3>Saved Runs (PostgreSQL)</h3>
        {history.length === 0 ? (
          <p className="muted">No database records found. Start Postgres and run an experiment.</p>
        ) : (
          <ul className="history-list">
            {history.map((item) => (
              <li key={item.id}>
                <strong>{item.statement}</strong>
                <span>
                  Metric: {item.best_metric} | Iterations: {item.iterations} | Spend: ${item.total_spend_usd}
                </span>
                <small>{new Date(item.created_at).toLocaleString()}</small>
              </li>
            ))}
          </ul>
        )}
      </article>
    </section>
  );
}

export default DashboardPage;
