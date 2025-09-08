from __future__ import annotations

from fastapi import FastAPI
from app.src.router.google.api import router as google

app = FastAPI(title="Authentication Service")
app.include_router(google, prefix="/auth")