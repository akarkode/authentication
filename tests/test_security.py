from __future__ import annotations

import pytest
import jwt
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException

from app.src.core.security import TokenService, AuthService
from app.src.core.config import settings


@pytest.mark.unit
class TestTokenService:
    """Test TokenService for JWT generation."""

    def test_generate_access_token(self, valid_jwt_payload):
        """Test access token generation."""
        token_service = TokenService()
        token = token_service.generate_access_token(valid_jwt_payload.copy())

        assert token is not None
        assert isinstance(token, str)

        # Decode and verify
        decoded = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        assert decoded["type"] == "access"
        assert decoded["name"] == valid_jwt_payload["name"]
        assert decoded["email"] == valid_jwt_payload["email"]
        assert "exp" in decoded

    def test_generate_refresh_token(self, valid_jwt_payload):
        """Test refresh token generation."""
        token_service = TokenService()
        token = token_service.generate_refresh_token(valid_jwt_payload.copy())

        assert token is not None
        assert isinstance(token, str)

        # Decode and verify
        decoded = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        assert decoded["type"] == "refresh"
        assert decoded["name"] == valid_jwt_payload["name"]
        assert "exp" in decoded

    def test_access_token_expiration(self, valid_jwt_payload):
        """Test access token has correct expiration."""
        token_service = TokenService()
        custom_expires = timedelta(minutes=30)
        token = token_service.generate_access_token(
            valid_jwt_payload.copy(),
            expires=custom_expires
        )

        decoded = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        expected_time = datetime.now(timezone.utc) + custom_expires

        # Allow 5 second tolerance
        assert abs((exp_time - expected_time).total_seconds()) < 5


@pytest.mark.unit
class TestAuthService:
    """Test AuthService for JWT validation."""

    @pytest.mark.asyncio
    async def test_decode_valid_token(self, valid_jwt_payload):
        """Test decoding a valid token."""
        token_service = TokenService()
        auth_service = AuthService()

        token = token_service.generate_access_token(valid_jwt_payload.copy())
        decoded = await auth_service._decode_token(token)

        assert decoded["name"] == valid_jwt_payload["name"]
        assert decoded["email"] == valid_jwt_payload["email"]
        assert decoded["type"] == "access"

    @pytest.mark.asyncio
    async def test_decode_invalid_token(self):
        """Test decoding an invalid token raises HTTPException."""
        auth_service = AuthService()

        with pytest.raises(HTTPException) as exc_info:
            await auth_service._decode_token("invalid.token.here")

        assert exc_info.value.status_code == 401
        assert "Invalid or expired token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_decode_expired_token(self, valid_jwt_payload):
        """Test decoding an expired token raises HTTPException."""
        token_service = TokenService()
        auth_service = AuthService()

        # Generate token that expires immediately
        token = token_service.generate_access_token(
            valid_jwt_payload.copy(),
            expires=timedelta(seconds=-1)
        )

        with pytest.raises(HTTPException) as exc_info:
            await auth_service._decode_token(token)

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_decode_token_wrong_signature(self, valid_jwt_payload):
        """Test decoding a token with wrong signature raises HTTPException."""
        auth_service = AuthService()

        # Create token with different secret
        token = jwt.encode(
            payload=valid_jwt_payload,
            key="wrong-secret-key",
            algorithm=settings.ALGORITHM
        )

        with pytest.raises(HTTPException) as exc_info:
            await auth_service._decode_token(token)

        assert exc_info.value.status_code == 401
