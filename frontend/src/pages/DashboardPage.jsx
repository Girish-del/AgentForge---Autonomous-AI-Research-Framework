import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import AgentCard from "../components/AgentCard";
import MetricGauge from "../components/MetricGauge";
import QuestLog from "../components/QuestLog";
import Spinner from "../components/Spinner";
import { AGENTS, TASK_TYPES } from "../services/agents";
import apiClient from "../services/apiClient";
import {
  ACHIEVEMENTS,
  applyRunResult,
  loadState,
  tierForMetric,
} from "../services/gamification";

const STOP_REASON_META = {
  target_reached: { label: "Target reached", icon: "🎯", className: "metric-pill--target" },
  budget_exhausted: { label: "Budget exhausted", icon: "💰", className: "metric-pill--metric" },
  max_iterations_reached: { label: "Max iterations", icon: "⏱", className: "metric-pill--metric" },
};

const formatPercent = (value) => `${(Number(value || 0) * 100).toFixed(1)}%`;
const formatCurrency = (value) => `$${Number(value || 0).toFixed(2)}`;

function setRangeProgress(event) {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) return;
  const min = Number(target.min || 0);
  const max = Number(target.max || 100);
  const value = Number(target.value);
  const percent = ((value - min) / (max - min || 1)) * 100;
  target.style.setProperty("--range-progress", `${percent}%`);
}

function DashboardPage({ progress, onProgressUpdate, onToast }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const [activeAgentIndex, setActiveAgentIndex] = useState(-1);
  const agentTickerRef = useRef(null);
  const [form, setForm] = useState({
    statement: "Improve AI agent task completion rate by 20%",
    budget_usd: 100,
    max_iterations: 3,
    target_metric: 0.8,
    task_type: "agent_planning",
  });

  const loadHistory = useCallback(async () => {
    try {
      const response = await apiClient.get("/orchestrator/runs", { params: { limit: 8 } });
      setHistory(response.data);
    } catch {
      setHistory([]);
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  useEffect(
    () => () => {
      if (agentTickerRef.current) clearInterval(agentTickerRef.current);
    },
    [],
  );

  const startAgentTicker = useCallback(() => {
    setActiveAgentIndex(0);
    if (agentTickerRef.current) clearInterval(agentTickerRef.current);
    agentTickerRef.current = setInterval(() => {
      setActiveAgentIndex((prev) => (prev + 1) % AGENTS.length);
    }, 600);
  }, []);

  const stopAgentTicker = useCallback(() => {
    if (agentTickerRef.current) {
      clearInterval(agentTickerRef.current);
      agentTickerRef.current = null;
    }
    setActiveAgentIndex(AGENTS.length);
  }, []);

  const updateField = (field, value) => {
    setForm((previous) => ({ ...previous, [field]: value }));
  };

  const runResearch = async (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    setResult(null);
    startAgentTicker();
    try {
      const response = await apiClient.post("/orchestrator/run", form);
      setResult(response.data);

      const { gained, reachedTarget, newAchievements } = applyRunResult({
        result: response.data,
        target_metric: form.target_metric,
        budget_usd: form.budget_usd,
      });

      onProgressUpdate?.();
      if (gained > 0) {
        onToast?.({
          icon: "✨",
          head: reachedTarget ? "Quest complete" : "Run logged",
          title: `+${gained} XP gained`,
          description: reachedTarget ? "Target metric reached!" : "Keep iterating to hit target.",
        });
      }
      newAchievements?.forEach((achievement) => {
        onToast?.({
          icon: achievement.icon,
          head: "Achievement unlocked",
          title: achievement.name,
          description: achievement.description,
        });
      });

      await loadHistory();
    } catch {
      setError(
        "Could not run experiment. Verify the FastAPI backend is running on port 8000 and the database is reachable.",
      );
    } finally {
      stopAgentTicker();
      setLoading(false);
    }
  };

  const agentStatusFor = (index) => {
    if (loading) {
      if (index === activeAgentIndex % AGENTS.length) return "active";
      return index < activeAgentIndex ? "done" : "idle";
    }
    if (result) return "done";
    return "idle";
  };

  const stopMeta = result
    ? STOP_REASON_META[result.stop_reason] || STOP_REASON_META.max_iterations_reached
    : null;

  const unlocked = useMemo(
    () => new Set(progress?.unlockedAchievements || loadState().unlockedAchievements || []),
    [progress],
  );

  return (
    <div className="dashboard">
      <section className="dashboard__top">
        <article className="panel panel--glow" aria-labelledby="quest-title">
          <h2 className="panel__title" id="quest-title">
            <span className="panel__title-mark" />
            Quest Console
          </h2>
          <p className="muted" style={{ margin: "0 0 1rem", fontSize: "0.88rem" }}>
            Define your research goal and dispatch the loop. Each iteration earns XP.
          </p>
          <form className="form-grid" onSubmit={runResearch}>
            <label>
              Goal Transmission
              <textarea
                value={form.statement}
                onChange={(event) => updateField("statement", event.target.value)}
                rows={3}
                required
              />
            </label>

            <div className="console-stats">
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
            </div>

            <div className="range-row">
              <div className="range-row__head">
                <span>Target Metric</span>
                <span className="range-row__value">{formatPercent(form.target_metric)}</span>
              </div>
              <input
                type="range"
                step="0.05"
                min="0.1"
                max="1"
                value={form.target_metric}
                onChange={(event) => {
                  setRangeProgress(event);
                  updateField("target_metric", Number(event.target.value));
                }}
                onInput={setRangeProgress}
                style={{
                  "--range-progress": `${(form.target_metric - 0.1) / 0.9 * 100}%`,
                }}
              />
            </div>

            <div>
              <div className="range-row__head" style={{ marginBottom: "0.4rem" }}>
                <span>Task Type</span>
                <span className="range-row__value">
                  {TASK_TYPES.find((task) => task.id === form.task_type)?.label}
                </span>
              </div>
              <div className="task-type-grid" role="radiogroup" aria-label="Task type">
                {TASK_TYPES.map((task) => {
                  const active = form.task_type === task.id;
                  return (
                    <button
                      key={task.id}
                      type="button"
                      role="radio"
                      aria-checked={active}
                      className={`task-type-pill ${active ? "is-active" : ""}`}
                      onClick={() => updateField("task_type", task.id)}
                    >
                      <span className="task-type-pill__icon" aria-hidden="true">
                        {task.icon}
                      </span>
                      {task.label}
                    </button>
                  );
                })}
              </div>
            </div>

            <button className="btn-primary" type="submit" disabled={loading}>
              {loading ? "Running…" : "Initiate Quest"}
            </button>
          </form>

          {loading && (
            <div className="banner banner--info" style={{ display: "flex", gap: "0.6rem" }}>
              <Spinner label="Agents engaged" />
              <span>Watch the lab grid for live status.</span>
            </div>
          )}
          {error && <div className="banner banner--error">{error}</div>}
        </article>

        <article className="panel" aria-labelledby="lab-title">
          <h2 className="panel__title" id="lab-title">
            <span className="panel__title-mark" />
            Lab Grid — Agent Crew
          </h2>
          <div className="lab-grid">
            {AGENTS.map((agent, index) => (
              <AgentCard key={agent.id} agent={agent} status={agentStatusFor(index)} />
            ))}
          </div>
          <p className="muted" style={{ marginTop: "0.85rem", fontSize: "0.82rem" }}>
            Each agent maps 1:1 to a stage of the orchestrator pipeline:{" "}
            collect → select → train → evaluate → analyze → improve → report.
          </p>
        </article>

        <article className="panel" aria-labelledby="mission-title">
          <h2 className="panel__title" id="mission-title">
            <span className="panel__title-mark" />
            Mission Stats
          </h2>
          <MetricGauge value={result?.best_metric || 0} target={form.target_metric} />
          <div className="stat-tiles">
            <div className="stat-tile">
              <span className="stat-tile__label">Iterations</span>
              <span className="stat-tile__value">{result?.iterations ?? "—"}</span>
            </div>
            <div className="stat-tile">
              <span className="stat-tile__label">Spend</span>
              <span className="stat-tile__value">
                {result ? formatCurrency(result.total_spend_usd) : "—"}
              </span>
            </div>
            <div className="stat-tile">
              <span className="stat-tile__label">Final Model</span>
              <span className="stat-tile__value" title={result?.report?.final_model}>
                {result?.report?.final_model
                  ? String(result.report.final_model).slice(0, 18)
                  : "—"}
              </span>
            </div>
            <div className="stat-tile">
              <span className="stat-tile__label">Outcome</span>
              <span className="stat-tile__value">
                {stopMeta ? `${stopMeta.icon} ${stopMeta.label}` : "—"}
              </span>
            </div>
          </div>
        </article>
      </section>

      <section className="panel" aria-labelledby="quests-title">
        <h2 className="panel__title" id="quests-title">
          <span className="panel__title-mark" />
          Quest Log
        </h2>
        <QuestLog history={result?.history || []} target={form.target_metric} />
      </section>

      <section className="panel" aria-labelledby="achievements-title">
        <h2 className="panel__title" id="achievements-title">
          <span className="panel__title-mark" />
          Achievements
        </h2>
        <div className="achievement-grid">
          {ACHIEVEMENTS.map((achievement) => {
            const isUnlocked = unlocked.has(achievement.id);
            return (
              <div
                key={achievement.id}
                className={`achievement ${isUnlocked ? "is-unlocked" : ""}`}
                aria-label={`${achievement.name} — ${isUnlocked ? "unlocked" : "locked"}`}
              >
                <div className="achievement__icon" aria-hidden="true">
                  {isUnlocked ? achievement.icon : "🔒"}
                </div>
                <div>
                  <div className="achievement__name">{achievement.name}</div>
                  <div className="achievement__desc">{achievement.description}</div>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <section className="panel" aria-labelledby="library-title">
        <h2 className="panel__title" id="library-title">
          <span className="panel__title-mark" />
          Run Library (PostgreSQL)
        </h2>
        {history.length === 0 ? (
          <div className="empty-state">
            <span className="empty-state__icon" aria-hidden="true">📚</span>
            <p>
              No saved runs yet. Run an experiment with PostgreSQL reachable to populate the
              library.
            </p>
          </div>
        ) : (
          <div className="runs-library">
            {history.map((item) => {
              const tier = tierForMetric(item.best_metric);
              return (
                <div className="run-card" key={item.id}>
                  <div className="run-card__head">
                    <span className="run-card__statement" title={item.statement}>
                      {item.statement}
                    </span>
                    <span className={`tier-badge tier-badge--${tier}`}>{tier}</span>
                  </div>
                  <div className="run-card__meta">
                    <span>
                      <strong>Metric</strong> {formatPercent(item.best_metric)}
                    </span>
                    <span>
                      <strong>Iter.</strong> {item.iterations}
                    </span>
                    <span>
                      <strong>Spend</strong> {formatCurrency(item.total_spend_usd)}
                    </span>
                  </div>
                  <div className="muted" style={{ fontSize: "0.78rem" }}>
                    {new Date(item.created_at).toLocaleString()}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}

export default DashboardPage;
