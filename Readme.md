# AgentForge — Autonomous AI Research Framework

AgentForge is a multi-agent research orchestration platform. You give it a high-level
research goal, and a pipeline of specialized agents iteratively collects data, picks a
model, trains, evaluates, analyzes failures, proposes improvements, and reruns until a
target metric is reached or the budget is exhausted.

The repository ships a **gamified React UI**, two FastAPI backends (`backend/app/` for
the user-facing API and `agentforge/api/` for the comprehensive plan scaffold),
PostgreSQL persistence for run history, and a Docker-Compose stack for the full local
loop.

## Architecture

Full Mermaid diagram: [`docs/architecture.mmd`](docs/architecture.mmd).

```text
┌────────────────────────────────────────────────────────────────┐
│            Frontend — React 18 + Vite (gamified UI)            │
│  Login · Register · Dashboard · HUD · Quest log · Achievements │
└──────────────────────────┬─────────────────────────────────────┘
                           │  REST API (JSON)
                           ▼
┌────────────────────────────────────────────────────────────────┐
│             Backend (1) — backend/app · FastAPI                │
│  Auth · Health · Orchestrator pipeline · Run-history (Postgres)│
│                                                                │
│   Intent Parser → Task Router → Conflict Detector              │
│   → Iterative Loop (Support / Domain agents) → Reporting       │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│         Backend (2) — agentforge/ · Comprehensive scaffold     │
│  Orchestrator · Agent loop · Model selector · MCP tool catalog │
│  data/ training/ evaluation/ improvement/ memory/ robotics/    │
└────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology | Status |
|---|---|---|
| Frontend | React 18, Vite, plain JSX, custom CSS, React Router, Axios | ✅ Implemented |
| Frontend gamification | XP, levels, streaks, achievements, quest log (localStorage) | ✅ Implemented |
| Backend (primary) | Python 3.11+, FastAPI, Uvicorn (`backend/app/`) | ✅ Implemented |
| Backend (scaffold) | FastAPI app at `agentforge/api/` exposing `/research/run` | ✅ Scaffold |
| Auth | Dev-only `/api/auth/login` returning a fixed token | ⚠️ Stub — JWT hardening on roadmap |
| Persistence | PostgreSQL `run_history` table created at startup | ✅ Implemented |
| Vector store | `pgvector/pgvector:pg16` image provisioned in compose | ⚠️ Image only — no `vector` columns yet |
| Memory layer | `FaissStore` (Python list) + `EmbeddingService` (placeholder) | ⚠️ Stub |
| LLM wrapper | `LLMWrapper` summarize stub | ⚠️ Stub |
| MCP tool catalog | `agentforge/mcp/{data,training,evaluation,improvement,memory}` | ✅ Scaffold |
| Robotics connector | `agentforge/robotics/ros_connector.py` | ⚠️ Phase-3 stub |
| Tests | Pytest (3 backend tests) | ✅ Implemented |
| CI | GitHub Actions: backend tests + frontend build | ✅ Implemented |
| Containerization | Docker + Docker Compose (frontend, backend, postgres) | ✅ Implemented |
| Formatting | Black, line-length 100 (`pyproject.toml`) | ✅ Configured |

> Tailwind, TypeScript, LangGraph, MLflow, and OpenTelemetry appear in `Plan.md` as
> aspirational targets. They are **not** yet wired into the running system.

## Project Structure

```text
.
├── frontend/                      # React 18 + Vite gamified UI
│   ├── src/
│   │   ├── components/            # HUD, AgentCard, MetricGauge, QuestLog,
│   │   │                          # AchievementToast, StarField, Spinner
│   │   ├── pages/                 # LoginPage, RegisterPage, DashboardPage
│   │   ├── services/              # apiClient.js, gamification.js, agents.js
│   │   ├── App.jsx, main.jsx, styles.css
│   │   └── ...
│   ├── package.json, vite.config.js, Dockerfile, index.html
├── backend/                       # User-facing FastAPI app
│   ├── app/
│   │   ├── routers/               # auth, orchestrator, health
│   │   ├── services/              # database, auth_service, llm_wrapper
│   │   ├── orchestrator/          # intent_parser, task_router,
│   │   │                          # conflict_detector, pipeline, reporting,
│   │   │                          # tracing
│   │   ├── memory/                # faiss_store, embeddings (stubs)
│   │   ├── agents/                # support_agent, domain_agent
│   │   └── models/                # schemas, domain dataclasses
│   ├── requirements.txt, Dockerfile
├── agentforge/                    # Comprehensive plan scaffold (separate FastAPI)
│   ├── core/                      # orchestrator, agent_loop, model_selector,
│   │                              # reporting, types
│   ├── agents/                    # data_agent, training_agent, eval_agent,
│   │                              # failure_analyst, improvement_agent
│   ├── mcp/                       # data, training, evaluation, improvement, memory
│   ├── memory/                    # vector_store, experiment_log
│   ├── observability/             # tracer
│   ├── robotics/                  # ros_connector (stub)
│   └── api/                       # main.py exposing POST /research/run
├── tests/backend/                 # pytest suite (health, auth, orchestrator)
├── docs/                          # architecture.mmd, BUILD_PARTS_GUIDE.md,
│                                  # PROJECT_PLAN.txt
├── eval/                          # placeholder — Phase 4
├── .github/workflows/ci.yml
├── docker-compose.yml             # frontend + backend + postgres (pgvector image)
├── pyproject.toml
├── .env.example
├── Plan.md                        # Comprehensive plan (vision)
├── Project.md                     # ELI5 description
├── AgentForge_Comprehensive_Plan.docx
└── Readme.md                      # this file
```

## The Gamified UI

The dashboard is built as a research-lab game console rather than a generic admin panel.
The intent: keep the dense iteration data legible while making the loop feel rewarding to
operate.

- **HUD** at the top: Level chip, XP bar (animated shimmer), total runs, current streak,
  budget chip.
- **Quest Console** (left panel): goal textarea framed as a "Goal Transmission", numeric
  inputs for budget and max iterations, a target-metric range slider with neon track,
  and a 12-tile task-type picker with icons. The big primary button reads "Initiate Quest".
- **Lab Grid** (center panel): seven agent cards (Scout, Oracle, Forge, Auditor,
  Detective, Architect, Scribe) mapping 1:1 to the orchestrator pipeline stages
  (`collect → select → train → evaluate → analyze → improve → report`). Cards
  pulse when active and turn green on completion.
- **Mission Stats** (right panel): SVG ring gauge (cyan-to-magenta gradient) for best
  metric vs target, plus stat tiles for iterations, spend, final model, and stop reason.
- **Quest Log**: per-iteration cards with metric pills, model swap, workflow, and a
  per-iteration `+XP` reward pill.
- **Achievements**: 7 unlockable badges (`First Forge`, `Target Reached`,
  `Triple Threat`, `Penny Pincher`, `Mad Scientist`, `Marathon Runner`,
  `Pivot Master`). Locked badges are dimmed; unlocked ones glow gold.
- **Run Library**: saved runs from PostgreSQL rendered as cards with bronze/silver/gold
  tier badges based on `best_metric`.
- **Toast stack**: top-right slide-in notifications for `+XP gained` and unlocked
  achievements.

The gamification state lives entirely in `localStorage` under the key `agentforge_lab_v1`
and is independent from the backend. Clearing your browser storage resets your level.

Color tokens (defined in `frontend/src/styles.css` as CSS custom properties):

| Token | Hex | Use |
|---|---|---|
| `--plasma` | `#00ffe1` | Primary cyan accents, focus rings, gauges |
| `--magenta` | `#ff2b9d` | Secondary accent, gradients, highlights |
| `--xp-gold` | `#ffd166` | Level/XP, achievements, gold tier |
| `--success` | `#38f583` | Done states, target reached |
| `--danger` | `#ff5d6c` | Error banners, streak chip |

Fonts: **Orbitron** (display, numerics, agent IDs) + **Inter** (body, forms), loaded from
Google Fonts in `frontend/index.html`.

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 20+ / npm 10+
- Git
- Docker and Docker Compose (optional, recommended for full stack with PostgreSQL)

### 1. Clone repository

```bash
git clone <your-repo-url>
cd "AgentForge - Autonomous AI Research Framework"
```

### 2. Configure environment variables

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

### 3. Run backend

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and run the user-facing API:

```bash
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000
```

- Backend: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

### 3a. (Optional) Run the comprehensive-plan scaffold separately

The `agentforge/` package ships its own FastAPI app at `agentforge/api/main.py`. It is
**not** mounted by `backend/app/main.py`; it runs as a separate service.

```bash
uvicorn agentforge.api.main:app --reload --port 8001
```

- Endpoint: `POST http://localhost:8001/research/run`
- Health: `GET http://localhost:8001/health`

### 4. Run frontend (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

### 4.1. PostgreSQL persistence

The user-facing backend creates and uses a `run_history` table automatically at startup.
If PostgreSQL is unavailable the API still runs and reports database status in
`/api/health`.

Quick local option (Docker for the DB only):

```bash
docker compose up -d postgres
```

Then run backend + frontend normally. Each dashboard experiment is saved in PostgreSQL
and surfaced in the **Run Library** panel.

### 5. Docker alternative (full stack)

```bash
docker compose up --build
```

Services:

- Frontend → `http://localhost:5173`
- Backend → `http://localhost:8000`
- PostgreSQL → `localhost:5432` (image: `pgvector/pgvector:pg16`)

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `BACKEND_PORT` | Exposed backend port | `8000` |
| `FRONTEND_PORT` | Exposed frontend port | `5173` |
| `DATABASE_URL` | Postgres connection URL | `postgresql://agentforge:agentforge@postgres:5432/agentforge` |
| `JWT_SECRET` | JWT signing secret (reserved — JWT validation not yet active) | `replace-this-in-production` |
| `VITE_API_BASE_URL` | Frontend API base URL | `http://localhost:8000/api` |

Never commit `.env`. Keep secrets local.

## API Endpoints

### `backend/app/` — user-facing API (port 8000)

- `GET /api/health` → `{status, database, ...}`
- `POST /api/auth/login` → `{access_token, token_type}` (dev token; any non-empty
  email + password succeeds)
- `POST /api/orchestrator/run` → runs the pipeline and persists the run
- `GET /api/orchestrator/runs?limit=10` → newest persisted runs

### `agentforge/api/` — comprehensive scaffold (port 8001 if run separately)

- `GET /health`
- `POST /research/run` → richer response contract with `checkpoints`, `report`,
  `traces`, and `history`

## Running Tests

From project root:

```bash
pytest tests/backend -v
```

Current backend test suite:

| File | Covers |
|---|---|
| `test_health.py` | health endpoint |
| `test_auth.py` | login flow endpoint |
| `test_orchestrator.py` | orchestrator run endpoint |

CI executes on every push and pull request via `.github/workflows/ci.yml` (backend
pytest + frontend `npm run build`).

Verify the frontend builds locally:

```bash
cd frontend
npm run build
```

## Authentication Flow (current)

1. Open the frontend app at `http://localhost:5173`.
2. The Login page calls `POST /api/auth/login`. The dev backend returns
   `{ "access_token": "dev-token", "token_type": "bearer" }` for any non-empty payload.
3. Frontend stores the token in `sessionStorage` and routes you to the dashboard.
4. Dashboard interactions hit `/api/orchestrator/run` and `/api/orchestrator/runs`.
5. Successful runs are persisted to PostgreSQL when reachable.

> **Register page status:** the form exists in the UI as a profile-creation flow but no
> backend register endpoint is wired yet. The page makes that explicit when you submit.

## Orchestration Loop (current)

The pipeline currently executes a foundation loop (`backend/app/orchestrator/pipeline.py`):

1. Parse intent from the goal statement (heuristic keyword matcher).
2. Detect planning conflicts (budget vs iteration cost).
3. Route the task to model selection logic (`MODEL_MATRIX`).
4. For each iteration, autonomously:
   - synthesize agent telemetry / task data
   - simulate train + evaluate (deterministic curve)
   - identify a failure mode
   - propose and validate a strategy via support + domain agents
   - swap model on later iterations
   - rerun the experiment with updated settings
5. Stop when:
   - target metric reached, or
   - budget exhausted, or
   - max iterations reached.
6. Return structured run history with per-iteration actions, traces, and a final report.

The `agentforge/core/agent_loop.py` package mirrors the same loop with the
plan-aligned agent set (DataAgent, TrainingAgent, EvalAgent, FailureAnalyst,
ImprovementAgent) and writes through to MCP tool stubs.

## Comprehensive Plan Alignment (April 2026)

The `agentforge/` package mirrors the comprehensive plan scaffold:

- Full research task DAG in `agentforge/core/orchestrator.py`
- Iterative `collect → select → train → evaluate → analyze → improve` loop in
  `agentforge/core/agent_loop.py`
- Model selector decision matrix aligned with the plan in
  `agentforge/mcp/training/select_model.py`
- MCP tool catalog scaffold:
  - `data/` — `fetch_dataset`, `run_simulation`, `generate_synthetic`, `label_with_vlm`
  - `training/` — `select_model`, `launch_training`, `hyperparameter_search`
  - `evaluation/` — `run_eval_suite`, `compute_metrics`, `failure_clustering`
  - `improvement/` — `propose_fix`, `apply_augmentation`, `swap_model`
  - `memory/` — `store_experiment`, `retrieve_similar`, `update_skill_library`
- Rich response contract for `POST /research/run` with checkpoints and stop reasons.
- Phase-3 stub for robotics simulation in `agentforge/robotics/ros_connector.py`.
- Phase-4 stub for observability tracing + report generation in both the
  `agentforge/` and `backend/app/orchestrator/` packages.

## Roadmap

Done:

- ✅ Production monorepo skeleton (frontend + backend + tests + CI + Docker)
- ✅ User-facing FastAPI service with health, auth, orchestrator endpoints
- ✅ PostgreSQL `run_history` persistence + UI surfacing
- ✅ Comprehensive plan scaffold under `agentforge/`
- ✅ Gamified React UI (XP, levels, achievements, agent crew, quest log)

In progress / next:

- Harden JWT auth (real signing + RBAC roles)
- Real FAISS + Sentence-Transformer indexing path (replace stubs)
- Wire `agentforge/api/` into the main backend or expose it via a shared gateway
- Add `pgvector` columns and retrieval APIs over `run_history`
- Expand the evaluation harness under `eval/`
- Add OpenTelemetry tracing and production deployment manifests
- Implement `POST /api/auth/register` to back the Forge Profile UI
