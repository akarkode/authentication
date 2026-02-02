from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.src.schemas.user import UserBaseModel, UserCreate


@pytest.mark.unit
class TestUserSchemas:
    """Test user Pydantic schemas."""

    def test_user_base_model_valid(self):
        """Test UserBaseModel with valid data."""
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "picture": "https://example.com/photo.jpg"
        }
        user = UserBaseModel(**data)

        assert user.name == data["name"]
        assert user.email == data["email"]
        assert user.picture == data["picture"]

    def test_user_base_model_optional_picture(self):
        """Test UserBaseModel with optional picture."""
        data = {
            "name": "Test User",
            "email": "test@example.com"
        }
        user = UserBaseModel(**data)

        assert user.name == data["name"]
        assert user.email == data["email"]
        assert user.picture is None

    def test_user_base_model_invalid_email(self):
        """Test UserBaseModel with invalid email."""
        data = {
            "name": "Test User",
            "email": "not-an-email"
        }

        # Note: Email validation requires pydantic[email] to be installed
        # which is in the dependencies
        with pytest.raises(ValidationError):
            UserBaseModel(**data)

    def test_user_base_model_missing_required(self):
        """Test UserBaseModel with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserBaseModel(name="Test User")

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("email",) for error in errors)

    def test_user_create_valid(self):
        """Test UserCreate with valid data."""
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "picture": "https://example.com/photo.jpg",
            "provider": "google",
            "provider_user_id": "12345"
        }
        user = UserCreate(**data)

        assert user.name == data["name"]
        assert user.provider == data["provider"]
        assert user.provider_user_id == data["provider_user_id"]

    def test_user_create_missing_provider(self):
        """Test UserCreate with missing provider fields."""
        data = {
            "name": "Test User",
            "email": "test@example.com"
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("provider",) for error in errors)
        assert any(error["loc"] == ("provider_user_id",) for error in errors)
