"""app/api/v1/endpoints/auth.py – /auth routes"""
from __future__ import annotations

from fastapi import APIRouter, status

from app.core.dependencies import SessionDep
from app.schemas.user import RefreshRequest, TokenResponse, UserCreate, UserLogin
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, session: SessionDep) -> TokenResponse:
    """Register a new user and return JWT tokens."""
    return await AuthService(session).register(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, session: SessionDep) -> TokenResponse:
    """Authenticate and return JWT tokens."""
    return await AuthService(session).login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, session: SessionDep) -> TokenResponse:
    """Exchange a refresh token for a new token pair."""
    return await AuthService(session).refresh(data.refresh_token)
