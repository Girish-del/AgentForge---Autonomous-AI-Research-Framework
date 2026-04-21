# AgentForge - Autonomous AI Research Framework

AgentForge is a production-oriented multi-agent research orchestration platform.  
It accepts high-level research goals, routes them through an orchestrator pipeline, runs iterative improvement loops, and exposes results through a FastAPI backend + React frontend with a complete HTML/CSS user interface.

## Architecture

Full Mermaid diagram: `docs/architecture.mmd`

```text
┌──────────────────────────────────────────────────────────────┐
│                     React Frontend (Vite)                   │
│     Login / Register / Dashboard / Experiment Trigger       │
└──────────────────────────┬───────────────────────────────────┘
                           │  REST API (JSON)
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│                                                              │
│  ┌──────────┐  ┌──────────────────────────────────────────┐  │
│  │  Auth    │  │            Orchestrator Pipeline         │  │
│  │  (JWT)   │  │                                          │  │
│  └──────────┘  │ Intent Parser → Task Router → Conflict   │  │
│                │ Detector → Loop Executor                 │  │
│                └──────────┬──────────────┬───────────────┘  │
│                           │              │                   │
│                     ┌─────▼──────┐ ┌─────▼────────────┐     │
│                     │ Support    │ │ Domain Agent      │     │
│                     │ Agent      │ │ (pluggable)       │     │
│                     └─────┬──────┘ └─────┬────────────┘     │
│                           └──────┬───────┘                   │
│                                  ▼                           │
│                     ┌────────────────────────┐               │
│                     │ Shared Memory Layer    │               │
│                     │ • FAISS store          │               │
│                     │ • Embedding service    │               │
│                     └────────────────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, semantic HTML, custom CSS, React Router, Axios |
| Backend | Python 3.11+, FastAPI, Uvicorn |
| AI / ML | FAISS (`faiss-cpu`), Sentence-Transformers (planned runtime integration) |
| Auth | JWT-ready service scaffold |
| Data | PostgreSQL (run history persisted from `/api/orchestrator/run`) |
| Deployment | Docker and Docker Compose |
| CI | GitHub Actions |
| Formatting | Black config in `pyproject.toml` |

## Project Structure

```text
├── frontend/
│   ├── src/
│   │   ├── pages/          # Login, Register, Dashboard
│   │   ├── services/       # Axios API client
│   │   └── components/     # Spinner, reusable UI
│   ├── package.json
│   └── Dockerfile
├── backend/
│   ├── app/
│   │   ├── routers/        # auth, orchestrator, health
│   │   ├── services/       # database, auth, LLM wrapper
│   │   ├── orchestrator/   # intent parser, task router, conflict detector, pipeline
│   │   ├── memory/         # FAISS store, embedding service
│   │   ├── agents/         # support agent, domain agent
│   │   └── models/         # schemas and domain models
│   ├── requirements.txt
│   └── Dockerfile
├── tests/
│   └── backend/            # pytest API tests
├── docs/
│   ├── architecture.mmd
│   ├── PROJECT_PLAN.txt
│   └── BUILD_PARTS_GUIDE.md
├── eval/
├── .github/workflows/ci.yml
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 20+ / npm 10+
- Git
- Docker and Docker Compose (optional, recommended for full stack)

### 1) Clone repository

```bash
git clone <your-repo-url>
cd "AgentForge - Autonomous AI Research Framework"
```

### 2) Configure environment variables

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

### 3) Run backend

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies and run API:

```bash
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000
```

Backend API: `http://localhost:8000`  
Swagger: `http://localhost:8000/docs`

### 4) Run frontend (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:5173`

### 4.1) Verify PostgreSQL persistence

The backend now creates and uses a `run_history` table automatically at startup.  
If PostgreSQL is unavailable, the API still runs and reports database status in health checks.

Quick local option (Docker only for DB):

```bash
docker compose up -d postgres
```

Then run backend + frontend normally. Each dashboard experiment is saved in PostgreSQL and rendered in the "Saved Runs" panel.

### 5) Docker alternative

```bash
docker compose up --build
```

Services:
- Frontend -> `http://localhost:5173`
- Backend -> `http://localhost:8000`
- PostgreSQL -> `localhost:5432`

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `BACKEND_PORT` | Exposed backend port | `8000` |
| `FRONTEND_PORT` | Exposed frontend port | `5173` |
| `DATABASE_URL` | Postgres connection URL | `postgresql://agentforge:agentforge@postgres:5432/agentforge` |
| `JWT_SECRET` | JWT signing secret | `replace-this-in-production` |
| `VITE_API_BASE_URL` | Frontend API base URL | `http://localhost:8000/api` |

Never commit `.env`. Keep secrets local.

## API Endpoints (Current)

- `GET /api/health`
- `POST /api/auth/login`
- `POST /api/orchestrator/run`
- `GET /api/orchestrator/runs?limit=10`

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

CI executes on every push and pull request via `.github/workflows/ci.yml`.

## Authentication Flow (Current)

1. Open frontend app.
2. Use Login page to call `/api/auth/login`.
3. Backend returns `access_token` (development token scaffold).
4. Dashboard can trigger `/api/orchestrator/run`.
5. Successful runs are persisted to PostgreSQL and available from `/api/orchestrator/runs`.

## Orchestration Loop (Current)

The pipeline currently executes a foundation loop:

1. Parse intent from goal statement
2. Detect planning conflicts (budget vs iteration settings)
3. Route task to model selection logic
4. For each iteration, autonomously:
   - collect agent telemetry/task data
   - train and evaluate a model/workflow candidate
   - identify failure modes
   - propose and validate an improvement strategy
   - change model/workflow when needed
   - rerun the experiment with updated settings
5. Run iterative improvement loop until:
   - target metric reached, or
   - budget exhausted, or
   - max iterations reached
6. Return structured run history with per-iteration actions

## Roadmap

- Harden JWT auth and role-based access control
- Persist run history in PostgreSQL
- Add real FAISS + Sentence-Transformer indexing path
- Expand evaluation harness under `eval/`
- Add observability and production deployment manifests

