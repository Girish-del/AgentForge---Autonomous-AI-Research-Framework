// Static metadata for the seven agents in the AgentForge research loop.
// Order matches the orchestrator pipeline (collect -> select -> train -> ... -> report).

export const AGENTS = [
  {
    id: "collect",
    name: "Scout",
    role: "Data Collection",
    icon: "🛰",
    description: "Pulls datasets, runs sims, synthesizes examples.",
  },
  {
    id: "select",
    name: "Oracle",
    role: "Model Selection",
    icon: "🔮",
    description: "Routes the task to the best model family.",
  },
  {
    id: "train",
    name: "Forge",
    role: "Training",
    icon: "🔥",
    description: "Tunes weights and runs the training loop.",
  },
  {
    id: "evaluate",
    name: "Auditor",
    role: "Evaluation",
    icon: "📊",
    description: "Benchmarks the model against eval suites.",
  },
  {
    id: "analyze",
    name: "Detective",
    role: "Failure Analysis",
    icon: "🔍",
    description: "Clusters failures, surfaces root causes.",
  },
  {
    id: "improve",
    name: "Architect",
    role: "Improvement",
    icon: "🛠",
    description: "Proposes augmentations, model swaps, fixes.",
  },
  {
    id: "report",
    name: "Scribe",
    role: "Reporting",
    icon: "📜",
    description: "Compiles the run into a structured report.",
  },
];

export const TASK_TYPES = [
  { id: "agent_planning", label: "Agent Planning", icon: "🧠" },
  { id: "agent_tool_use", label: "Tool Use", icon: "🛠" },
  { id: "agent_memory", label: "Memory", icon: "🧬" },
  { id: "agent_collaboration", label: "Collaboration", icon: "🤝" },
  { id: "agent_evaluation", label: "Evaluation", icon: "🧪" },
  { id: "image_classification", label: "Image Class.", icon: "🖼" },
  { id: "object_detection", label: "Object Det.", icon: "🎯" },
  { id: "language_understanding", label: "Lang. Understand.", icon: "💬" },
  { id: "vision_language", label: "Vision+Lang.", icon: "👁" },
  { id: "trajectory_prediction", label: "Trajectory", icon: "📈" },
  { id: "low_latency_inference", label: "Low-Latency", icon: "⚡" },
  { id: "generative_data", label: "Generative", icon: "🎨" },
];
