from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.src.router.v1.api import router
from app.src.core.config import settings

app = FastAPI(
    title="Authentication Service",
    description="OAuth 2.0 Authentication Service with Google integration",
    version="0.1.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    openapi_url="/openapi.json" if settings.is_development else None,
    debug=settings.is_development,
)

app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

if not settings.is_development:
    app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

templates = Jinja2Templates(directory="app/src/templates")


@app.get("/", response_class=HTMLResponse, include_in_schema=settings.is_development)
async def get_development_ui(request: Request):
    if not settings.is_development:
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Not Found",
                "message": "This endpoint is only available in development environment."
            }
        )
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"env": settings.ENV}
    )


@app.get("/health", tags=["Health"])
async def get_health_status():
    return {
        "status": "healthy",
        "service": "authentication-service",
        "environment": settings.ENV,
        "version": "0.1.0"
    }