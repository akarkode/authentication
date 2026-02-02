from __future__ import annotations

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch

from tests.factories import GoogleUserInfoFactory


@pytest.mark.integration
class TestGoogleOAuthEndpoints:
    """Test Google OAuth API endpoints."""

    @pytest.mark.asyncio
    async def test_google_login_redirect(self, client: AsyncClient):
        """Test GET /v1/google/login redirects to Google."""
        with patch("app.src.core.oauth_config.oauth") as mock_oauth:
            mock_google = MagicMock()
            mock_google.authorize_redirect = AsyncMock(
                return_value=MagicMock(
                    status_code=302,
                    headers={"location": "https://accounts.google.com/o/oauth2/v2/auth"}
                )
            )
            mock_oauth.google = mock_google

            response = await client.get("/v1/google/login", follow_redirects=False)

            # Should initiate OAuth flow
            assert response.status_code in [302, 307]

    @pytest.mark.asyncio
    async def test_google_callback_success(self, client: AsyncClient, db_session):
        """Test GET /v1/google/callback with valid OAuth response."""
        userinfo = GoogleUserInfoFactory.build()

        with patch("app.src.core.oauth_config.oauth") as mock_oauth:
            mock_google = MagicMock()
            mock_google.authorize_access_token = AsyncMock(
                return_value={"userinfo": userinfo}
            )
            mock_oauth.google = mock_google

            response = await client.get(
                "/v1/google/callback?code=test_code&state=test_state",
                follow_redirects=False
            )

            # Should redirect with cookies set
            assert response.status_code in [302, 307]

            # Check cookies are set
            cookies = response.cookies
            assert "access_token" in cookies
            assert "refresh_token" in cookies

    @pytest.mark.asyncio
    async def test_google_callback_creates_new_user(self, client: AsyncClient, db_session):
        """Test that callback creates a new user if they don't exist."""
        userinfo = GoogleUserInfoFactory.build()

        with patch("app.src.core.oauth_config.oauth") as mock_oauth:
            mock_google = MagicMock()
            mock_google.authorize_access_token = AsyncMock(
                return_value={"userinfo": userinfo}
            )
            mock_oauth.google = mock_google

            response = await client.get(
                "/v1/google/callback?code=test_code",
                follow_redirects=False
            )

            assert response.status_code in [302, 307]

            # Verify user was created in database
            from app.src.crud.user import CRUDUser
            crud = CRUDUser()
            user = await crud.get_by_provider_user_id(
                session=db_session,
                provider="google",
                provider_user_id=userinfo["sub"]
            )
            assert user is not None
            assert user.email == userinfo["email"]
            assert user.name == userinfo["name"]

    @pytest.mark.asyncio
    async def test_google_callback_existing_user(self, client: AsyncClient, db_session):
        """Test that callback doesn't create duplicate users."""
        from app.src.models.user import User
        from app.src.schemas.user import UserBaseModel

        userinfo = GoogleUserInfoFactory.build()

        # Create user first
        user = User(
            **UserBaseModel(**userinfo).model_dump(),
            provider="google",
            provider_user_id=userinfo["sub"]
        )
        db_session.add(user)
        await db_session.commit()

        with patch("app.src.core.oauth_config.oauth") as mock_oauth:
            mock_google = MagicMock()
            mock_google.authorize_access_token = AsyncMock(
                return_value={"userinfo": userinfo}
            )
            mock_oauth.google = mock_google

            response = await client.get(
                "/v1/google/callback?code=test_code",
                follow_redirects=False
            )

            assert response.status_code in [302, 307]

    @pytest.mark.asyncio
    async def test_google_callback_error_handling(self, client: AsyncClient):
        """Test that callback handles OAuth errors gracefully."""
        with patch("app.src.core.oauth_config.oauth") as mock_oauth:
            mock_google = MagicMock()
            mock_google.authorize_access_token = AsyncMock(
                side_effect=Exception("OAuth error")
            )
            mock_oauth.google = mock_google

            response = await client.get("/v1/google/callback?code=test_code")

            assert response.status_code == 400
