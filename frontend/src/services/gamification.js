// Local-only progression layer. Lives in localStorage so progress survives reloads.
// Backend is unaware of any of this — it stays a pure UX flourish.

const STORAGE_KEY = "agentforge_lab_v1";

const DEFAULT_STATE = {
  xp: 0,
  totalRuns: 0,
  targetReachedRuns: 0,
  currentStreak: 0,
  bestStreak: 0,
  unlockedAchievements: [],
};

export const ACHIEVEMENTS = [
  {
    id: "first_forge",
    name: "First Forge",
    description: "Run your first experiment",
    icon: "⚡",
    test: (s) => s.totalRuns >= 1,
  },
  {
    id: "target_reached",
    name: "Target Reached",
    description: "Hit your goal metric in a run",
    icon: "🎯",
    test: (s) => s.targetReachedRuns >= 1,
  },
  {
    id: "triple_threat",
    name: "Triple Threat",
    description: "Three target-reached runs in a row",
    icon: "🔥",
    test: (s) => s.bestStreak >= 3,
  },
  {
    id: "penny_pincher",
    name: "Penny Pincher",
    description: "Finish a run under 50% of budget",
    icon: "💎",
    test: (s) => s.bestBudgetRatio !== undefined && s.bestBudgetRatio <= 0.5,
  },
  {
    id: "mad_scientist",
    name: "Mad Scientist",
    description: "Complete 10 total experiments",
    icon: "🧪",
    test: (s) => s.totalRuns >= 10,
  },
  {
    id: "marathon_runner",
    name: "Marathon Runner",
    description: "Run an experiment with 10+ iterations",
    icon: "🏃",
    test: (s) => (s.maxIterationsRun || 0) >= 10,
  },
  {
    id: "pivot_master",
    name: "Pivot Master",
    description: "Workflow change in 3+ iterations of one run",
    icon: "🔀",
    test: (s) => (s.maxWorkflowChanges || 0) >= 3,
  },
];

const safeRead = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...DEFAULT_STATE };
    return { ...DEFAULT_STATE, ...JSON.parse(raw) };
  } catch {
    return { ...DEFAULT_STATE };
  }
};

const safeWrite = (state) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    /* ignore quota errors — progression is best-effort */
  }
};

export const loadState = () => safeRead();

export const resetState = () => {
  safeWrite({ ...DEFAULT_STATE });
  return { ...DEFAULT_STATE };
};

// Level curve — gentle ramp early, slower later. L1 needs ~50 XP, L5 ~1250 XP.
export const levelFromXp = (xp) => Math.max(1, Math.floor(Math.sqrt(xp / 50)) + 1);

export const xpForLevel = (level) => Math.pow(level - 1, 2) * 50;

export const xpProgressInLevel = (xp) => {
  const level = levelFromXp(xp);
  const floor = xpForLevel(level);
  const ceiling = xpForLevel(level + 1);
  const span = ceiling - floor || 1;
  const progress = Math.min(1, Math.max(0, (xp - floor) / span));
  return { level, floor, ceiling, progress, into: xp - floor, span };
};

const computeUnlockedAchievements = (state) =>
  ACHIEVEMENTS.filter((a) => a.test(state)).map((a) => a.id);

// Apply the result of a successful run. Returns { state, gained, newAchievements }.
export const applyRunResult = ({ result, target_metric, budget_usd }) => {
  const previous = safeRead();
  const iterations = result?.iterations || 0;
  const reachedTarget = (result?.best_metric || 0) >= target_metric;
  const totalSpend = result?.total_spend_usd || 0;
  const budgetRatio = budget_usd > 0 ? totalSpend / budget_usd : 1;

  const workflowChanges = (result?.history || []).filter(
    (entry) => entry?.workflow_change?.next_workflow,
  ).length;

  let xpGain = iterations * 25;
  if (reachedTarget) xpGain += 100;

  const nextStreak = reachedTarget ? previous.currentStreak + 1 : 0;
  if (reachedTarget && nextStreak >= 2) xpGain += 25 * nextStreak;

  const next = {
    ...previous,
    xp: previous.xp + xpGain,
    totalRuns: previous.totalRuns + 1,
    targetReachedRuns: previous.targetReachedRuns + (reachedTarget ? 1 : 0),
    currentStreak: nextStreak,
    bestStreak: Math.max(previous.bestStreak, nextStreak),
    bestBudgetRatio: Math.min(previous.bestBudgetRatio ?? 1, budgetRatio),
    maxIterationsRun: Math.max(previous.maxIterationsRun || 0, iterations),
    maxWorkflowChanges: Math.max(previous.maxWorkflowChanges || 0, workflowChanges),
  };

  const previousIds = new Set(previous.unlockedAchievements || []);
  const unlocked = computeUnlockedAchievements(next);
  const newAchievements = unlocked
    .filter((id) => !previousIds.has(id))
    .map((id) => ACHIEVEMENTS.find((a) => a.id === id));

  next.unlockedAchievements = unlocked;
  safeWrite(next);

  return {
    state: next,
    gained: xpGain,
    reachedTarget,
    newAchievements,
  };
};

export const tierForMetric = (metric) => {
  if (metric >= 0.85) return "gold";
  if (metric >= 0.7) return "silver";
  return "bronze";
};
