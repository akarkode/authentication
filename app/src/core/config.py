from __future__ import annotations

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = ""
    REDIRECT_URL: str = ""
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    GOOGLE_CLIENT_ID: str = ""
    REDIRECT_RESPONSE: str = ""
    SESSION_SECRET_KEY: str = ""
    COOKIE_IS_SECURE: bool = False
    GOOGLE_CLIENT_SECRET: str = ""
    CORS_ORIGINS: str = "*"

    @property
    def is_development(self) -> bool:
        return self.ENV.lower() in ["local", "dev", "development"]

    @property
    def allowed_origins(self) -> list[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

settings = Settings(_env_file='.env')