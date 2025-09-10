from __future__ import annotations

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = ""
    REDIRECT_URL: str = ""
    FRONTEND_URL: str = ""
    DATABASE_URL: str = ""
    JWT_SECRET_KEY: str = ""
    GOOGLE_CLIENT_ID: str = ""
    SESSION_SECRET_KEY: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

settings = Settings(_env_file='.env')