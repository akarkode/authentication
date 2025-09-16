from __future__ import annotations

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALGORITHM: str = "HS256"
    SECRET_KEY: str = ""
    REDIRECT_URL: str = ""
    DATABASE_URL: str = ""
    GOOGLE_CLIENT_ID: str = ""
    REDIRECT_RESPONSE: str = ""
    SESSION_SECRET_KEY: str = ""
    COOKIE_IS_SECURE: bool = False
    GOOGLE_CLIENT_SECRET: str = ""

settings = Settings(_env_file='.env')