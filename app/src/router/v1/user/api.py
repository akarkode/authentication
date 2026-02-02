from __future__ import annotations

from fastapi import Depends, APIRouter
from app.src.core.security import AuthService

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me")
async def get_current_user(
    authenticated_user: dict = Depends(AuthService().require_access_token)
):
    return authenticated_user