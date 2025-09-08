from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from app.src.database.session import get_async_session

router = APIRouter(prefix="/google", tags=["Authentication"])

@router.post("/login")
async def sign_in(request: Request):
    pass