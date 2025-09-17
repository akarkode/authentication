from __future__ import annotations

import logging
from fastapi import Depends
from fastapi import Request
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


router = APIRouter(prefix="/google", tags=["Authentication"])
logger = logging.getLogger(__name__)
token_service = TokenService()
crud_user = CRUDUser()


@router.get("/login")
async def login(request: Request):
    print(f"{settings.GOOGLE_CLIENT_ID}|")
    print(f"{settings.GOOGLE_CLIENT_SECRET}|")
    print(f"{settings.REDIRECT_RESPONSE}|")
    print(f"{settings.REDIRECT_URL}|")
    return await oauth.google.authorize_redirect(request, settings.REDIRECT_URL)

@router.get("/callback")
async def callback(request: Request, session: AsyncSession = Depends(get_async_session)):
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token["userinfo"]
        if not await crud_user.get_by_provider_user_id(session=session, provider="google", provider_user_id=userinfo["sub"]):
            await crud_user.create(session=session, user=User(**UserBaseModel(**userinfo).model_dump(), provider="google", provider_user_id=userinfo["sub"]))

        redirect = RedirectResponse(settings.REDIRECT_RESPONSE)
        redirect.set_cookie(
            key="access_token", 
            secure=settings.COOKIE_IS_SECURE, 
            max_age=900,
            httponly=False, # Change this to True if you want to use HttpOnly cookie session
            samesite="strict", 
            value=token_service.generate_access_token(payload=UserBaseModel(**userinfo).model_dump()), 
        )
        redirect.set_cookie(
            key="refresh_token", 
            secure=settings.COOKIE_IS_SECURE, 
            max_age=86400,
            httponly=False, # Change this to True if you want to use HttpOnly cookie session 
            samesite="strict", 
            value=token_service.generate_refresh_token(payload=UserBaseModel(**userinfo).model_dump()), 
        )
        return redirect
    except Exception as error:
        logger.error(error)
        raise HTTPException(400)