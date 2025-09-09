from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.models.user import User


class CRUDUser:
    def __init__(self):
        pass
    
    async def create(self, session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_provider_user_id(self, session: AsyncSession, provider: str, provider_user_id:str) -> User|None:
        stmt = select(User).where(User.provider==provider, User.provider_user_id==provider_user_id).limit(1)
        user = await session.execute(stmt)
        return user.scalar_one_or_none()
        