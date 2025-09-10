from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.src.router.v1.api import router
from app.src.core.config import settings

app = FastAPI(title="Authentication Service")
app.include_router(router=router)
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

templates = Jinja2Templates(directory="app/src/templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")