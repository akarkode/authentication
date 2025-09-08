from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from app.src.models.user import User

class CRUD:
    def __init__(self):
        pass

    async def create(self, session: AsyncSession, user: User):
        await session.add(user)
        await session.commit()
        await session.refresh(user)
        return user