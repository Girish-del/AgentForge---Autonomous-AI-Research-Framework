# AgentForge Build Parts Guide

This guide explains how the project is built in parts using a production-ready monorepo layout.

## Structure Baseline (Current)

Top-level layout:

- `frontend/` - React 18 + Vite gamified UI
- `backend/` - User-facing FastAPI app and AI orchestration logic
- `agentforge/` - Comprehensive plan scaffold (separate FastAPI + agents + MCP tools)
- `tests/backend/` - backend tests
- `docs/` - architecture and planning docs (`architecture.mmd`, `PROJECT_PLAN.txt`,
  this file)
- `eval/` - evaluation scripts placeholder
- `.github/workflows/` - CI
- `docker-compose.yml` - local stack orchestration
- `.env.example` - environment template
- `Plan.md`, `Project.md`, `AgentForge_Comprehensive_Plan.docx` - planning artifacts

## Part 1 - Production Skeleton (Current)

### Frontend files

- `frontend/src/pages/` - `LoginPage`, `RegisterPage`, `DashboardPage`
- `frontend/src/components/` - `HUD`, `AgentCard`, `MetricGauge`, `QuestLog`,
  `AchievementToast`, `StarField`, `Spinner`
- `frontend/src/services/` - `apiClient.js` (Axios), `gamification.js` (XP/levels/
  achievements via localStorage), `agents.js` (agent + task-type metadata)
- `frontend/src/styles.css` - design tokens + gamified visual language
- `frontend/package.json`, `frontend/vite.config.js`, `frontend/Dockerfile`,
  `frontend/index.html` (Orbitron + Inter fonts, SVG favicon)

### Backend files (`backend/app/`)

- `backend/app/routers/` - `auth`, `orchestrator`, `health`
- `backend/app/services/` - `database`, `llm_wrapper`, `auth_service`
- `backend/app/orchestrator/` - `intent_parser`, `task_router`, `conflict_detector`,
  `pipeline`, `reporting`, `tracing`
- `backend/app/memory/` - `faiss_store`, `embeddings` (stubs)
- `backend/app/agents/` - `support_agent`, `domain_agent`
- `backend/app/models/` - `schemas`, domain dataclasses
- `backend/app/main.py` - FastAPI app wiring
- `backend/requirements.txt`, `backend/Dockerfile`

### Platform files

- `.github/workflows/ci.yml` - backend test + frontend build jobs
- `docker-compose.yml` - frontend + backend + postgres (`pgvector/pgvector:pg16` image)
- `docs/architecture.mmd` and `docs/PROJECT_PLAN.txt`

## Part 1.5 - Comprehensive Plan Scaffold (Current)

A second package, `agentforge/`, mirrors the structure described in `Plan.md`. It is
**not** mounted into `backend/app/main.py`; it ships as a standalone FastAPI app.

- `agentforge/core/` - `orchestrator`, `agent_loop`, `model_selector`, `reporting`, `types`
- `agentforge/agents/` - `data_agent`, `training_agent`, `eval_agent`, `failure_analyst`,
  `improvement_agent`
- `agentforge/mcp/` - tool catalog under `data/`, `training/`, `evaluation/`,
  `improvement/`, `memory/`
- `agentforge/memory/` - `vector_store`, `experiment_log`
- `agentforge/observability/` - `tracer`
- `agentforge/robotics/` - `ros_connector` (Phase 3 stub)
- `agentforge/api/` - `main.py` exposing `POST /research/run` and `GET /health`

Run it on its own port:

```bash
uvicorn agentforge.api.main:app --reload --port 8001
```

## Part 1.6 - Gamified Frontend (Current)

The dashboard is intentionally not a generic admin panel. It is built as a research-lab
game console while keeping all the dense iteration data legible.

- **HUD** with level, XP bar, run count, streak, and budget chip
- **Quest Console** for goal entry and parameter tuning (range slider for target,
  task-type pill grid)
- **Lab Grid** with seven agent cards (Scout, Oracle, Forge, Auditor, Detective,
  Architect, Scribe) that activate sequentially during a run
- **Mission Stats** SVG ring gauge (cyan→magenta gradient) for best metric vs target
- **Quest Log** rendering iteration history with per-iteration `+XP` pills
- **Achievements** panel showing 7 unlockable badges
- **Run Library** with bronze/silver/gold tier badges sourced from PostgreSQL
- **Toast stack** for XP gains and achievement unlocks

Gamification state persists in `localStorage` under `agentforge_lab_v1`. The backend is
unaware of any of it.

## Part 2 - API Hardening

Planned additions:

- JWT validation middleware and role model
- structured error handling and request IDs
- config management with strict environment validation
- input/output contract tests for all routers

## Part 3 - Autonomous Core

Planned additions:

- full collect -> train -> evaluate -> improve pipeline state machine
- persistent experiment/event log in PostgreSQL
- richer conflict resolution, retries, and checkpointing

## Part 4 - Memory + Evaluation

Planned additions:

- real FAISS + sentence-transformer indexing
- retrieval APIs for prior experiments
- `eval/` scripts for regression benchmarking and scorecards

## Part 5 - Observability + Release

Planned additions:

- OpenTelemetry traces and dashboards
- release workflow, image tagging, and deployment manifests
- scale/performance tests for orchestrator and API
