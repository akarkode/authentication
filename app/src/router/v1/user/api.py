from __future__ import annotations

from fastapi import Depends
from fastapi import APIRouter
from app.src.core.security import AuthService

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me")
async def user_me(authentication: dict = Depends(AuthService().require_access_token)):
    return authentication