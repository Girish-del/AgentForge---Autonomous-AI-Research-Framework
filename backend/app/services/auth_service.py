from app.models.schemas import AuthResponse


class AuthService:
    def login(self, email: str, password: str) -> AuthResponse:
        if not email or not password:
            raise ValueError("Invalid credentials")
        return AuthResponse(access_token="dev-token")
