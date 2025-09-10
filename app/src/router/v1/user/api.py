from __future__ import annotations

from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from app.src.schemas.user import UserBaseModel
from app.src.core.security import TokenService

router = APIRouter(prefix="/user", tags=["User"])
token = TokenService()
security = HTTPBearer()


@router.get("/me")
async def user_me(authentication: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return UserBaseModel(**token.validate_access_token(token=authentication.credentials))
    except Exception:
        raise HTTPException(401)