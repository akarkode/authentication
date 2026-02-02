from __future__ import annotations

from uuid import uuid4
from datetime import datetime
from faker import Faker

fake = Faker()


class UserFactory:
    """Factory for creating test user data."""

    @staticmethod
    def build(**kwargs) -> dict:
        """Build user data without persisting to database."""
        defaults = {
            "id": uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "picture": fake.image_url(),
            "provider": "google",
            "provider_user_id": fake.uuid4(),
            "created_at": datetime.utcnow(),
            "updated_at": None,
        }
        defaults.update(kwargs)
        return defaults

    @staticmethod
    def build_create_schema(**kwargs) -> dict:
        """Build user creation schema data."""
        defaults = {
            "name": fake.name(),
            "email": fake.email(),
            "picture": fake.image_url(),
            "provider": "google",
            "provider_user_id": fake.uuid4(),
        }
        defaults.update(kwargs)
        return defaults


class GoogleUserInfoFactory:
    """Factory for creating Google OAuth userinfo responses."""

    @staticmethod
    def build(**kwargs) -> dict:
        """Build Google userinfo response."""
        defaults = {
            "sub": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "picture": fake.image_url(),
            "email_verified": True,
        }
        defaults.update(kwargs)
        return defaults
