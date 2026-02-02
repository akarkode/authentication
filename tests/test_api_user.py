from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.src.core.security import TokenService
from tests.factories import UserFactory


@pytest.mark.integration
class TestUserEndpoints:
    """Test user API endpoints."""

    @pytest.mark.asyncio
    async def test_get_user_me_success(self, client: AsyncClient):
        """Test GET /v1/user/me with valid access token."""
        token_service = TokenService()
        user_data = UserFactory.build_create_schema()

        access_token = token_service.generate_access_token({
            "name": user_data["name"],
            "email": user_data["email"],
            "picture": user_data["picture"],
        })

        response = await client.get(
            "/v1/user/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]

    @pytest.mark.asyncio
    async def test_get_user_me_no_token(self, client: AsyncClient):
        """Test GET /v1/user/me without token returns 403."""
        response = await client.get("/v1/user/me")

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_user_me_invalid_token(self, client: AsyncClient):
        """Test GET /v1/user/me with invalid token returns 401."""
        response = await client.get(
            "/v1/user/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_user_me_refresh_token_rejected(self, client: AsyncClient):
        """Test GET /v1/user/me with refresh token instead of access token."""
        token_service = TokenService()
        user_data = UserFactory.build_create_schema()

        # Use refresh token instead of access token
        refresh_token = token_service.generate_refresh_token({
            "name": user_data["name"],
            "email": user_data["email"],
            "picture": user_data["picture"],
        })

        response = await client.get(
            "/v1/user/me",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )

        assert response.status_code == 401
        assert "Invalid access token" in response.json()["detail"]
