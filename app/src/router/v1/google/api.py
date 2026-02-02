from __future__ import annotations

import logging
from fastapi import Depends, Request, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models.user import User
from app.src.crud.user import CRUDUser
from app.src.core.config import settings
from app.src.core.oauth_config import oauth
from app.src.core.security import TokenService
from app.src.schemas.user import UserBaseModel
from app.src.database.session import get_async_session

router = APIRouter(prefix="/google", tags=["Authentication"])
logger = logging.getLogger(__name__)
token_service = TokenService()
crud_user = CRUDUser()


@router.get("/login")
async def initiate_google_oauth(request: Request):
    return await oauth.google.authorize_redirect(request, settings.REDIRECT_URL)


@router.get("/callback")
async def handle_google_oauth_callback(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token["userinfo"]

        existing_user = await crud_user.get_by_provider_user_id(
            session=session,
            provider="google",
            provider_user_id=userinfo["sub"]
        )

        if not existing_user:
            user_data = UserBaseModel(**userinfo).model_dump()
            new_user = User(**user_data, provider="google", provider_user_id=userinfo["sub"])
            await crud_user.create(session=session, user=new_user)

        user_payload = UserBaseModel(**userinfo).model_dump()
        redirect = RedirectResponse(settings.REDIRECT_RESPONSE)

        redirect.set_cookie(
            key="access_token",
            value=token_service.generate_access_token(payload=user_payload),
            secure=settings.COOKIE_IS_SECURE,
            max_age=900,
            httponly=False,
            samesite="strict",
        )

        redirect.set_cookie(
            key="refresh_token",
            value=token_service.generate_refresh_token(payload=user_payload),
            secure=settings.COOKIE_IS_SECURE,
            max_age=86400,
            httponly=False,
            samesite="strict",
        )

        return redirect
    except Exception as error:
        logger.error(error)
        raise HTTPException(400)