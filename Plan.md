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

| Layer | Technology |
|---|---|
| **Agent Orchestration** | LangGraph, custom Python DAG |
| **LLM Backbone** | Claude 3.5 Sonnet (reasoning), GPT-4o (fallback) |
| **VLM Support** | Gemini 1.5 Pro Vision, LLaVA, GPT-4V |
| **Tool/Skill Layer** | MCP (Model Context Protocol) |
| **Training Framework** | PyTorch, HuggingFace Transformers, Accelerate |
| **Robotics Sim** | ROS 2, Gazebo, Isaac Sim |
| **Vector DB / RAG** | PostgreSQL 16 + pgvector |
| **Eval Harness** | lm-evaluation-harness, custom eval runners |
| **Experiment Tracking** | MLflow or Weights & Biases |
| **Workflow Scheduling** | Prefect or Temporal |
| **Observability** | OpenTelemetry, Grafana, custom dashboard (React) |
| **API Layer** | FastAPI (Python) |
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Frontend Dashboard** | React + TypeScript + Tailwind |

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

```
agentforge-research/
├── core/
│   ├── orchestrator.py         # Main goal-to-DAG planner
│   ├── agent_loop.py           # Collect → Train → Eval → Improve loop
│   └── model_selector.py       # Model routing logic
├── agents/
│   ├── data_agent.py
│   ├── training_agent.py
│   ├── eval_agent.py
│   ├── failure_analyst.py
│   └── improvement_agent.py
├── mcp/                        # All MCP tool definitions
├── memory/
│   ├── vector_store.py         # pgvector integration
│   └── experiment_log.py       # Structured run history
├── dashboard/                  # React frontend
├── api/                        # FastAPI backend
├── tests/                      # Pytest suite
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## 10. Milestones & Phases

### Phase 1 — Foundation (Weeks 1–3)
- Orchestrator + basic DAG runner
- Data Collection Agent (HF datasets + simulation stub)
- Manual training runner (PyTorch)
- MLflow experiment tracking
- Basic REST API

### Phase 2 — Autonomy Core (Weeks 4–7)
- Full agent loop (collect → train → eval → improve)
- MCP tool layer with all core skills
- Model Selector sub-agent
- pgvector memory store
- LangGraph integration

### Phase 3 — Robotics Integration (Weeks 8–11)
- ROS 2 / Gazebo simulation connector
- VLM-based failure analysis (visual inputs)
- Synthetic data generation pipeline
- Real robot eval harness

### Phase 4 — Observability & Polish (Weeks 12–14)
- Full React dashboard
- OpenTelemetry tracing
- Auto-generated research report output
- Multi-goal parallel experiment runs
- Public benchmark eval suite

---

## 11. Key Design Principles

1. **Every agent action is logged and reversible** — full audit trail.
2. **No hardcoded models** — everything routes through the Model Selector.
3. **Skills are composable** — agents can load new MCP tools at runtime without restarts.
4. **Fail fast, learn fast** — failures are first-class data, not exceptions.
5. **Human-in-the-loop optional** — supports fully autonomous mode OR approval gates at any step.
6. **Open by default** — prefer open-source models; closed APIs are opt-in.

---

*Generated for AgentForge Research — April 2026*