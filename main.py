from __future__ import annotations

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.src.router.auth.v1.google.api import router as google

app = FastAPI(title="Authentication Service")
app.add_middleware(SessionMiddleware, secret_key="rahasia")
app.include_router(google)

@app.get("/")
async def main():
    return "successfully"