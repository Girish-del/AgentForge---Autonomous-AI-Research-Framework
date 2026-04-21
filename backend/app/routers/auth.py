from fastapi import APIRouter, HTTPException

from app.models.schemas import AuthResponse, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])
auth_service = AuthService()


@router.post("/auth/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    try:
        return auth_service.login(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
