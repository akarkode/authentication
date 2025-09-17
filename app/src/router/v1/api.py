from __future__ import annotations

from fastapi import APIRouter
from app.src.router.v1.user.api import router as user
from app.src.router.v1.google.api import router as google

router = APIRouter(prefix="/api/auth/v1")
router.include_router(router=user)
router.include_router(router=google)