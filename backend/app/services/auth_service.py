"""
app/services/auth_service.py
─────────────────────────────
Authentication business logic:
  - register: create user, hash password, return tokens
  - login: verify credentials, return tokens
  - refresh: validate refresh token, return new access token
"""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserCreate, UserLogin
from jose import JWTError


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserRepository(session)

    async def register(self, data: UserCreate) -> TokenResponse:
        if await self._repo.get_by_email(data.email):
            raise ConflictException(f"Email '{data.email}' is already registered")

        user = await self._repo.create(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            age=data.age,
            goals=data.goals,
        )
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def login(self, data: UserLogin) -> TokenResponse:
        user = await self._repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedException("Account is inactive")

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise UnauthorizedException("Invalid token type")
            user_id: str = payload["sub"]
        except (JWTError, KeyError):
            raise UnauthorizedException("Invalid or expired refresh token")

        from uuid import UUID
        user = await self._repo.get_by_id(UUID(user_id))
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive")

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )
