from __future__ import annotations

import jwt
from fastapi import HTTPException, Depends
from datetime import timedelta, datetime, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.src.core.config import settings
from app.src.schemas.user import UserBaseModel

class TokenService:
    def __init__(self):
        self.algorithm = settings.ALGORITHM
        self.secret_key = settings.SECRET_KEY

    def generate_access_token(self, payload: dict, expires: timedelta = timedelta(minutes=15)):
        payload["type"] = "access"
        payload["exp"] = datetime.now(timezone.utc) + expires
        return jwt.encode(payload=payload, key=self.secret_key, algorithm=self.algorithm)
    
    def generate_refresh_token(self, payload: dict, expires: timedelta = timedelta(hours=24)):
        payload["type"] = "refresh"
        payload["exp"] = datetime.now(timezone.utc) + expires
        return jwt.encode(payload=payload, key=self.secret_key, algorithm=self.algorithm)


class AuthService:
    def __init__(self):
        self.algorithm = settings.ALGORITHM
        self.secret_key = settings.SECRET_KEY

    async def _decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_signature": True}
            )
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

    async def require_access_token(
        self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> UserBaseModel:
        payload = await self._decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid access token")
        return UserBaseModel(**payload)

    async def require_refresh_token(
        self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> UserBaseModel:
        payload = await self._decode_token(credentials.credentials)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return UserBaseModel(**payload)