from __future__ import annotations

import logging
from fastapi import Depends
from fastapi import Request
from fastapi import Response
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models.user import User
from app.src.crud.user import CRUDUser
from app.src.core.config import settings
from app.src.core.oauth_config import oauth
from app.src.core.security import TokenService
from app.src.schemas.user import UserBaseModel
from app.src.database.session import get_async_session


router = APIRouter(prefix="/auth/v1/google", tags=["Authentication"])
logger = logging.getLogger(__name__)
token_service = TokenService()
crud_user = CRUDUser()


@router.get("/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.REDIRECT_URL)

@router.get("/callback")
async def callback(request: Request, response: Response, session: AsyncSession = Depends(get_async_session)):
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token["userinfo"]
        user = await crud_user.get_by_provider_user_id(session=session, provider="google", provider_user_id=userinfo["sub"])
        if not user:
            await crud_user.create(session=session, user=User(**UserBaseModel(**userinfo).model_dump(), provider="google", provider_user_id=userinfo["sub"]))
        response.set_cookie("access_token", token_service.generate_access_token(payload=UserBaseModel(**userinfo).model_dump()), httponly=True, secure=True, samesite="strict", max_age=900)
        response.set_cookie("refresh_token", token_service.generate_refresh_token(payload=UserBaseModel(**userinfo).model_dump()), httponly=True, secure=True, samesite="strict", max_age=86400)
        return RedirectResponse("/")
    except Exception as error:
        logger.error(error)
        raise HTTPException(400)