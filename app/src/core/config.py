from __future__ import annotations
from pydantic_settings import BaseSettings
from pydantic import field_validator

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

    @field_validator("*", mode="before")
    def strip_all(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

settings = Settings(_env_file=".env")
