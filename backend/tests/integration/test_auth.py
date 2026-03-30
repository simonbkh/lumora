"""
tests/integration/test_auth.py
──────────────────────────────
HTTP-level integration tests for the authentication endpoints.
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestRegister:
    async def test_register_success(self, client: AsyncClient):
        resp = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "alice@example.com",
                "password": "SecurePass1!",
                "full_name": "Alice",
            },
        )
        assert resp.status_code == 201
        body = resp.json()
        assert "access_token" in body
        assert "refresh_token" in body
        assert body["token_type"] == "bearer"

    async def test_register_duplicate_email(self, client: AsyncClient):
        payload = {"email": "bob@example.com", "password": "SecurePass1!", "full_name": "Bob"}
        await client.post("/api/v1/auth/register", json=payload)
        resp = await client.post("/api/v1/auth/register", json=payload)
        assert resp.status_code == 409


@pytest.mark.asyncio
class TestLogin:
    async def test_login_success(self, client: AsyncClient):
        email, password = "charlie@example.com", "SecurePass1!"
        await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": password, "full_name": "Charlie"},
        )
        resp = await client.post(
            "/api/v1/auth/login", json={"email": email, "password": password}
        )
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    async def test_login_wrong_password(self, client: AsyncClient):
        email = "diana@example.com"
        await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "correct!", "full_name": "Diana"},
        )
        resp = await client.post(
            "/api/v1/auth/login", json={"email": email, "password": "wrongpassword"}
        )
        assert resp.status_code == 401


@pytest.mark.asyncio
class TestProtectedRoute:
    async def test_me_requires_auth(self, client: AsyncClient):
        resp = await client.get("/api/v1/users/me")
        assert resp.status_code == 403  # no bearer header → HTTPBearer rejects

    async def test_me_returns_profile(self, client: AsyncClient):
        email = "eve@example.com"
        reg = await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "SecurePass1!", "full_name": "Eve"},
        )
        token = reg.json()["access_token"]
        resp = await client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == email
