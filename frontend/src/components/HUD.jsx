import { NavLink } from "react-router-dom";

import { xpProgressInLevel } from "../services/gamification";

function HUD({ state, gold = 0, navItems = [] }) {
  const { level, into, span, progress } = xpProgressInLevel(state.xp || 0);
  const fillPercent = Math.round(progress * 100);

  return (
    <header className="hud" aria-label="Player heads-up display">
      <div className="hud__brand">
        <div className="hud__crystal" aria-hidden="true">
          <span className="hud__crystal-mark">AF</span>
        </div>
        <div className="hud__title">
          <h1>AgentForge Lab</h1>
          <small>Autonomous Research Console</small>
        </div>
      </div>

      <div className="hud__center">
        <div className="level-chip" title={`${into} / ${span} XP into Level ${level}`}>
          <span>Lv</span>
          <span className="level-chip__num">{level}</span>
        </div>
        <div
          className="xp-bar"
          role="progressbar"
          aria-valuenow={fillPercent}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label="Experience progress to next level"
        >
          <div className="xp-bar__fill" style={{ width: `${fillPercent}%` }} />
        </div>
        <span className="xp-text">
          {into}/{span} XP
        </span>
      </div>

      <div className="hud__stats">
        <span className="stat-chip stat-chip--gold" title="Total experiments completed">
          <span className="stat-chip__icon" aria-hidden="true">⚗️</span>
          {state.totalRuns || 0} runs
        </span>
        <span
          className="stat-chip stat-chip--streak"
          title={`Best streak: ${state.bestStreak || 0}`}
        >
          <span className="stat-chip__icon" aria-hidden="true">🔥</span>
          {state.currentStreak || 0} streak
        </span>
        <span className="stat-chip" title="Lab credits available">
          <span className="stat-chip__icon" aria-hidden="true">💠</span>
          ${gold.toLocaleString()}
        </span>
        {navItems.length > 0 && (
          <nav className="hud__nav" aria-label="Primary">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) => (isActive ? "active" : "")}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        )}
      </div>
    </header>
  );
}

export default HUD;
