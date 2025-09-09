from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class UserBaseModel(BaseModel):
    name: str
    email: str
    picture: Optional[str] = None

class UserCreate(UserBaseModel):
    provider: str
    provider_user_id: str