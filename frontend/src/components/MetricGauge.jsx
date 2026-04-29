const RADIUS = 70;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

function MetricGauge({ value = 0, target = 0.9 }) {
  const safeValue = Math.max(0, Math.min(1, value));
  const offset = CIRCUMFERENCE * (1 - safeValue);
  const reached = safeValue >= target;

  return (
    <div className="gauge" role="img" aria-label={`Best metric ${(safeValue * 100).toFixed(1)} percent`}>
      <div className="gauge__ring">
        <svg viewBox="0 0 168 168">
          <defs>
            <linearGradient id="gauge-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#00ffe1" />
              <stop offset="60%" stopColor="#7dffe9" />
              <stop offset="100%" stopColor="#ff2b9d" />
            </linearGradient>
          </defs>
          <circle className="gauge__track" cx="84" cy="84" r={RADIUS} />
          <circle
            className="gauge__progress"
            cx="84"
            cy="84"
            r={RADIUS}
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={offset}
          />
        </svg>
        <div className="gauge__center">
          <span className="gauge__value">{(safeValue * 100).toFixed(1)}%</span>
          <span className="gauge__label">Best Metric</span>
        </div>
      </div>
      <div className="gauge__sub">
        <span className="gauge__sub-target">
          Target {(target * 100).toFixed(0)}%
        </span>
        {reached ? (
          <span className="metric-pill metric-pill--target">🎯 Target reached</span>
        ) : (
          <span className="metric-pill metric-pill--metric">In progress</span>
        )}
      </div>
    </div>
  );
}

export default MetricGauge;
