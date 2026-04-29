# AgentForge — Autonomous AI Research Framework
### GitHub Repository: `agentforge-research`

> An autonomous agentic AI framework that closes the loop between data collection, model training, evaluation, failure analysis, and iterative improvement — purpose-built for robotics and agent research.

---

## 1. Vision & Goals

AgentForge is a self-driving research platform. Given a high-level research goal (e.g., "improve pick-and-place success rate by 20%"), it autonomously:

- Collects or synthesizes relevant data
- Selects and trains the best model/VLM for the task
- Evaluates results with rigorous metrics
- Identifies failure modes using introspective agents
- Proposes and implements fixes — new architectures, augmentation strategies, or workflow changes
- Reruns experiments until convergence or budget exhaustion

The system is **model-agnostic**, **skill-composable**, and **fully observable** via a live dashboard.

---

## 2. Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR                            │
│         (Goal Parser → Task Planner → Agent Dispatcher)         │
└────────────┬────────────────────────────────────────────────────┘
             │
     ┌───────▼────────────────────────────────────────────┐
     │                  AGENT LOOP CORE                   │
     │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
     │  │  Collect │→ │  Train   │→ │    Evaluate      │ │
     │  └──────────┘  └──────────┘  └────────┬─────────┘ │
     │       ↑                               │            │
     │  ┌────┴────────────────────────┐      │            │
     │  │   Improve / Rerun           │ ←────┘            │
     │  │  (model swap, augment, fix) │                   │
     │  └─────────────────────────────┘                   │
     └────────────────────────────────────────────────────┘
             │
     ┌───────▼───────────────────┐
     │     TOOL / MCP LAYER      │
     │  - Data tools             │
     │  - Training runners       │
     │  - Eval harnesses         │
     │  - Model registry         │
     │  - Memory / RAG store     │
     └───────────────────────────┘
             │
     ┌───────▼───────────────────┐
     │   OBSERVABILITY LAYER     │
     │  Dashboard · Logs · Audit │
     └───────────────────────────┘
```

---

## 3. System Components

### 3.1 Orchestrator Agent
- **Role**: Accepts high-level research goals, decomposes them into sub-tasks, and dispatches specialized agents.
- **Tech**: LangGraph or custom DAG runner; backed by Claude Sonnet / GPT-4o as the reasoning backbone.
- **Key behaviors**: Goal clarification, loop budget management, early stopping, progress checkpointing.

### 3.2 Data Collection Agent
- **Role**: Autonomously gathers training/evaluation data from simulation, the web, or internal datasets.
- **Sources**: ROS/Gazebo simulation rollouts, HuggingFace datasets, web scraping via browser tools, synthetic data generation via VLMs (GPT-4V, Gemini Vision).
- **MCP Tools**: `fetch_dataset`, `run_simulation`, `generate_synthetic`, `label_with_vlm`.

### 3.3 Training Agent
- **Role**: Selects appropriate model architecture, configures hyperparameters, kicks off training runs.
- **Supported model types**: CNNs, Transformers, ViTs, LLMs (fine-tuning), VLMs, diffusion-based data generators.
- **Routing logic**: Uses a Model Selector sub-agent that reasons about task type (perception vs. planning vs. NLP) and picks the right model family.
- **Runners**: Local GPU (PyTorch), remote (Modal, RunPod), or HuggingFace AutoTrain.

### 3.4 Evaluation Agent
- **Role**: Runs the trained model against benchmarks and structured eval suites.
- **Outputs**: Per-class metrics, confusion matrices, latency profiles, robustness reports.
- **Eval harnesses**: `lm-evaluation-harness` for LLMs, custom robotics eval loops via ROS.
- **MCP Tools**: `run_eval_suite`, `compute_metrics`, `generate_report`.

### 3.5 Failure Mode Analyst Agent
- **Role**: Introspects eval results to identify *why* failures occur — not just where.
- **Methods**: Attention map analysis, embedding cluster inspection, error-pattern clustering (UMAP + KMeans), prompted VLM critique of failure cases.
- **Output**: Structured failure taxonomy fed back to the Improvement Agent.

### 3.6 Improvement Agent
- **Role**: Given a failure taxonomy, proposes concrete fixes and implements them.
- **Strategies**: Data augmentation, architecture swap, prompt re-engineering, fine-tuning on hard negatives, workflow restructuring.
- **Decision making**: Scores strategies by expected gain vs. compute cost; picks the Pareto-optimal action.

### 3.7 Memory & Knowledge Store
- **Short-term**: Conversation/agent state stored in-context.
- **Long-term**: PostgreSQL + pgvector (RAG) for experiment history, model cards, and lessons learned.
- **Skill library**: Reusable tool wrappers stored as MCP skills; agent can load new skills at runtime.

---

## 4. Technology Stack

The right column marks what is **shipping** in the current codebase versus what is
**aspirational** (planned for later phases).

| Layer | Technology | Status |
|---|---|---|
| **Agent Orchestration** | Custom Python DAG (deterministic) — LangGraph deferred | ✅ DAG / 🔜 LangGraph |
| **LLM Backbone** | Claude 3.5 Sonnet (reasoning), GPT-4o (fallback) | 🔜 Provider wrapper stub only (`LLMWrapper`) |
| **VLM Support** | Gemini 1.5 Pro Vision, LLaVA, GPT-4V | 🔜 Listed in `MODEL_MATRIX` only |
| **Tool/Skill Layer** | MCP (Model Context Protocol) | ✅ Scaffold under `agentforge/mcp/` |
| **Training Framework** | PyTorch, HuggingFace Transformers, Accelerate | 🔜 Stubbed |
| **Robotics Sim** | ROS 2, Gazebo, Isaac Sim | 🔜 `agentforge/robotics/ros_connector.py` stub |
| **Vector DB / RAG** | PostgreSQL 16 + pgvector | ⚠️ pgvector image provisioned, no `vector` columns yet |
| **Eval Harness** | lm-evaluation-harness, custom eval runners | 🔜 `eval/` is a placeholder |
| **Experiment Tracking** | MLflow or Weights & Biases | 🔜 Not wired |
| **Workflow Scheduling** | Prefect or Temporal | 🔜 Not wired |
| **Observability** | OpenTelemetry, Grafana, custom dashboard (React) | ⚠️ Custom dashboard ✅, OTel/Grafana 🔜 |
| **API Layer** | FastAPI (Python) | ✅ Two FastAPI apps: `backend/app/` and `agentforge/api/` |
| **Containerization** | Docker, Docker Compose | ✅ Implemented |
| **CI/CD** | GitHub Actions | ✅ Backend pytest + frontend `npm run build` |
| **Frontend Dashboard** | React 18 + Vite + plain JSX + custom CSS (gamified UI) — TypeScript / Tailwind deferred | ✅ Implemented (no TS/Tailwind yet) |
| **Frontend gamification** | XP / levels / achievements / streaks via `localStorage` | ✅ Implemented |

---

## 5. MCP Tools & Skills Catalog

```
agentforge/
└── mcp/
    ├── data/
    │   ├── fetch_dataset.py         # Pull from HF, Roboflow, etc.
    │   ├── run_simulation.py        # Trigger ROS/Gazebo rollout
    │   └── generate_synthetic.py   # VLM-assisted data synthesis
    ├── training/
    │   ├── select_model.py          # Model routing logic
    │   ├── launch_training.py       # PyTorch / HF Trainer wrapper
    │   └── hyperparameter_search.py # Optuna-based HPO
    ├── evaluation/
    │   ├── run_eval_suite.py        # Benchmarks + custom evals
    │   ├── compute_metrics.py       # Precision, recall, F1, AUC
    │   └── failure_clustering.py   # UMAP + KMeans on embeddings
    ├── improvement/
    │   ├── propose_fix.py           # Structured fix generation
    │   ├── apply_augmentation.py   # Auto data aug pipelines
    │   └── swap_model.py           # Hot-swap architecture
    └── memory/
        ├── store_experiment.py      # pgvector experiment log
        ├── retrieve_similar.py      # RAG over past experiments
        └── update_skill_library.py # Add new MCP tools dynamically
```

---

## 6. Agentic Loop — Step by Step

```
1. INPUT        → User defines research goal + constraints (budget, time, dataset)
2. PLAN         → Orchestrator decomposes goal into DAG of sub-tasks
3. COLLECT      → Data Agent gathers/generates datasets
4. SELECT       → Model Selector reasons about best architecture + backbone
5. TRAIN        → Training Agent launches and monitors training run
6. EVALUATE     → Eval Agent runs full benchmark suite
7. ANALYZE      → Failure Analyst clusters and categorizes failure modes
8. IMPROVE      → Improvement Agent proposes + applies top-ranked fix strategy
9. RERUN        → Loop back to TRAIN with updated config
10. CONVERGE    → Stop when metric target met OR budget exhausted
11. REPORT      → Auto-generate research summary with experiment lineage
```

---

## 7. Model Selection Strategy

The Model Selector sub-agent uses a decision matrix:

| Task Type | Preferred Model | Fallback |
|---|---|---|
| Image classification | ViT / ResNet | CNN |
| Object detection | YOLO v9 / RT-DETR | Faster RCNN |
| Language understanding | Claude Sonnet | GPT-4o-mini |
| Vision + Language | Gemini 1.5 Pro | GPT-4V |
| Trajectory prediction | Transformer (traj) | LSTM |
| Low-latency inference | Quantized ONNX | TorchScript |
| Generative data | Stable Diffusion XL | DALL-E 3 |

Routing factors: task modality, latency budget, context length, cost per token, open vs. closed source requirement.

---

## 8. Observability & Dashboard

A live React dashboard provides:

- **Experiment timeline**: DAG visualization of every agent action taken
- **Metric trends**: Loss curves, accuracy, F1 across all runs
- **Failure heatmaps**: Per-class failure rates across iterations
- **Agent chat log**: Transparency into every agent decision
- **Model registry**: All trained checkpoints with metadata
- **Cost tracker**: Token usage + compute spend per experiment

---

## 9. Repository Structure

The project ships as a monorepo. The plan-aligned package lives at `agentforge/`,
the user-facing API + UI live at `backend/app/` and `frontend/`, and tests are
shared.

```
.
├── frontend/                   # React 18 + Vite gamified UI
├── backend/                    # User-facing FastAPI service
│   └── app/
│       ├── routers/            # auth, orchestrator, health
│       ├── services/           # database (Postgres), auth, llm wrapper
│       ├── orchestrator/       # intent parser, task router, conflict
│       │                       # detector, pipeline, reporting, tracing
│       ├── memory/             # FAISS store + embedding stubs
│       ├── agents/             # support_agent, domain_agent
│       └── models/             # schemas, domain dataclasses
├── agentforge/                 # Comprehensive plan scaffold
│   ├── core/                   # orchestrator, agent_loop, model_selector
│   ├── agents/                 # data, training, eval, failure_analyst,
│   │                           # improvement
│   ├── mcp/                    # data, training, evaluation, improvement,
│   │                           # memory tool stubs
│   ├── memory/                 # vector_store, experiment_log
│   ├── observability/          # tracer
│   ├── robotics/               # ros_connector stub
│   └── api/                    # standalone FastAPI exposing /research/run
├── tests/backend/              # Pytest suite
├── docs/                       # architecture.mmd, BUILD_PARTS_GUIDE.md,
│                               # PROJECT_PLAN.txt
├── eval/                       # placeholder for Phase 4
├── docker-compose.yml          # frontend + backend + pgvector image
├── pyproject.toml
├── Plan.md (this file)
├── Project.md
└── Readme.md
```

---

## 10. Milestones & Phases

### Phase 1 — Foundation (Weeks 1–3) ✅ Mostly done
- ✅ Orchestrator + basic DAG runner (`agentforge/core/orchestrator.py`,
  `backend/app/orchestrator/pipeline.py`)
- ⚠️ Data Collection Agent — stub at `agentforge/agents/data_agent.py`
  (no HF / simulation calls yet)
- 🔜 Manual training runner (PyTorch)
- 🔜 MLflow experiment tracking
- ✅ Basic REST API (`backend/app/main.py` + `agentforge/api/main.py`)
- ✅ PostgreSQL run-history persistence

### Phase 2 — Autonomy Core (Weeks 4–7) — In progress
- ✅ Full agent loop scaffold (collect → select → train → evaluate → analyze →
  improve → report) in both `backend/app/orchestrator/pipeline.py` and
  `agentforge/core/agent_loop.py`
- ✅ MCP tool catalog scaffold under `agentforge/mcp/`
- ✅ Model Selector sub-agent (`agentforge/mcp/training/select_model.py`,
  `backend/app/orchestrator/task_router.py`)
- 🔜 Real pgvector memory store (currently a Python list in `FaissStore`)
- 🔜 LangGraph integration
- 🔜 Real LLM provider wiring (currently `LLMWrapper` stub)

### Phase 3 — Robotics Integration (Weeks 8–11) — Stubbed
- ⚠️ ROS 2 / Gazebo simulation connector — `agentforge/robotics/ros_connector.py`
- 🔜 VLM-based failure analysis (visual inputs)
- 🔜 Synthetic data generation pipeline
- 🔜 Real robot eval harness

### Phase 4 — Observability & Polish (Weeks 12–14) — UI partially done
- ✅ Gamified React dashboard (XP, levels, agent crew, quest log,
  achievements, run library)
- ⚠️ Trace recorder writes to memory only (`TraceRecorder`)
- 🔜 OpenTelemetry tracing + Grafana
- 🔜 Auto-generated research report output (current report is a structured dict)
- 🔜 Multi-goal parallel experiment runs
- 🔜 Public benchmark eval suite

---

## 11. Key Design Principles

1. **Every agent action is logged and reversible** — full audit trail.
2. **No hardcoded models** — everything routes through the Model Selector.
3. **Skills are composable** — agents can load new MCP tools at runtime without restarts.
4. **Fail fast, learn fast** — failures are first-class data, not exceptions.
5. **Human-in-the-loop optional** — supports fully autonomous mode OR approval gates at any step.
6. **Open by default** — prefer open-source models; closed APIs are opt-in.

---

*Generated for AgentForge Research — April 2026. Status annotations updated April 2026
to reflect the current monorepo state. The status legend: ✅ shipping, ⚠️ partial /
stub, 🔜 not yet started.*