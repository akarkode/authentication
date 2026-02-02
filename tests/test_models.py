from __future__ import annotations

import pytest
from uuid import UUID
from datetime import datetime

from app.src.models.user import User
from tests.factories import UserFactory


@pytest.mark.unit
class TestUserModel:
    """Test User model."""

    @pytest.mark.asyncio
    async def test_create_user(self, db_session):
        """Test creating a user."""
        user_data = UserFactory.build_create_schema()
        user = User(**user_data)

        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.id is not None
        assert isinstance(user.id, UUID)
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert user.provider == user_data["provider"]
        assert user.provider_user_id == user_data["provider_user_id"]
        assert isinstance(user.created_at, datetime)

    @pytest.mark.asyncio
    async def test_user_email_unique(self, db_session):
        """Test that user email must be unique."""
        user_data = UserFactory.build_create_schema(email="duplicate@example.com")

        user1 = User(**user_data)
        db_session.add(user1)
        await db_session.commit()

        # Try to create another user with same email
        user2 = User(**user_data)
        db_session.add(user2)

        with pytest.raises(Exception):  # SQLAlchemy will raise IntegrityError
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_user_with_optional_fields(self, db_session):
        """Test creating a user with optional fields."""
        user_data = UserFactory.build_create_schema()
        user_data["picture"] = None  # Optional field

        user = User(**user_data)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        assert user.id is not None
        assert user.picture is None
        assert user.updated_at is None
