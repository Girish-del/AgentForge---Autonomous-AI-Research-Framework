from fastapi import APIRouter, Request
from app.services.database import get_database_service

router = APIRouter(tags=["health"])


@router.get("/health")
def health(request: Request) -> dict[str, str]:
    db_health = get_database_service(request.app).health()
    return {"status": "ok", **db_health}
