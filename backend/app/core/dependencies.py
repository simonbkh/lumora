"""
app/core/dependencies.py
────────────────────────
FastAPI dependency-injection helpers for:
  - Database async sessions
  - Authenticated current user (access token)
  - RBAC role guards
"""
from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import RoleEnum, User
from app.repositories.user_repository import UserRepository

# ── Re-export DB session dep ──────────────────────────────────────────────────
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# ── Bearer token extractor ────────────────────────────────────────────────────
_bearer = HTTPBearer(auto_error=True)
BearerDep = Annotated[HTTPAuthorizationCredentials, Depends(_bearer)]


async def get_current_user(
    credentials: BearerDep,
    session: SessionDep,
) -> User:
    """
    Validate the Bearer access token and return the active user.
    Raises 401 on any failure so the reason is not leaked.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise credentials_exception
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    repo = UserRepository(session)
    user = await repo.get_by_id(UUID(user_id))
    if user is None or not user.is_active:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: RoleEnum):
    """
    Factory that returns a dependency enforcing role membership.
    Usage:  Depends(require_roles(RoleEnum.ADMIN))
    """
    async def _guard(current_user: CurrentUserDep) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _guard
