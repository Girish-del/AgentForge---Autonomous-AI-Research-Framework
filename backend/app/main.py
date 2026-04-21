from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.orchestrator import router as orchestrator_router

app = FastAPI(title="AgentForge Backend", version="1.0.0")

app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(orchestrator_router, prefix="/api")
