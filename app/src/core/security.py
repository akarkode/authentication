from __future__ import annotations

import jwt
from datetime import timedelta, datetime, timezone
from app.src.core.config import settings

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
    
    def validate_access_token(self, token: str):
        userinfo = jwt.decode(jwt=token, key=self.secret_key, algorithms=self.algorithm, verify=True)
        if userinfo.get("type") != "access":
            raise
        return userinfo
    
    def validate_refresh_token(self, token: str):
        userinfo = jwt.decode(jwt=token, key=self.secret_key, algorithms=self.algorithm, verify=True)
        if userinfo.get("type") != "refresh":
            raise
        return userinfo