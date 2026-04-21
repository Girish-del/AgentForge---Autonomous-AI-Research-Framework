# AgentForge Build Parts Guide

This guide explains how the project is built in parts using a production-ready monorepo layout.

## Structure Baseline (Current)

Top-level layout:

- `frontend/` - React app (Vite)
- `backend/` - FastAPI app and AI orchestration logic
- `tests/backend/` - backend tests
- `docs/` - architecture and planning docs
- `eval/` - evaluation scripts placeholder
- `.github/workflows/` - CI
- `docker-compose.yml` - local stack orchestration
- `.env.example` - environment template

## Part 1 - Production Skeleton (Current)

### Frontend files

- `frontend/src/pages/` - `LoginPage`, `RegisterPage`, `DashboardPage`
- `frontend/src/services/apiClient.js` - Axios API client
- `frontend/src/components/Spinner.jsx` - reusable loading UI
- `frontend/package.json`, `frontend/vite.config.js`, `frontend/Dockerfile`, `frontend/index.html`

### Backend files

- `backend/app/routers/` - `auth`, `orchestrator`, `health`
- `backend/app/services/` - `database`, `llm_wrapper`, `auth_service`
- `backend/app/orchestrator/` - `intent_parser`, `task_router`, `conflict_detector`, `pipeline`
- `backend/app/memory/` - `faiss_store`, `embeddings`
- `backend/app/agents/` - `support_agent`, `domain_agent`
- `backend/app/models/` - `schemas`, domain dataclasses
- `backend/app/main.py` - FastAPI app wiring
- `backend/requirements.txt`, `backend/Dockerfile`

### Platform files

- `.github/workflows/ci.yml` - backend test + frontend build jobs
- `docker-compose.yml` - frontend + backend + postgres
- `docs/architecture.mmd` and `docs/PROJECT_PLAN.txt`

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
