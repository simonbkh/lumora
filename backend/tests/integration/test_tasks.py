"""tests/integration/test_tasks.py – Integration tests for task CRUD."""
from __future__ import annotations

import pytest
from httpx import AsyncClient


async def _register_and_get_token(client: AsyncClient, email: str) -> str:
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "SecurePass1!", "full_name": "Tester"},
    )
    return resp.json()["access_token"]


@pytest.mark.asyncio
class TestTasks:
    async def test_create_and_get_task(self, client: AsyncClient):
        token = await _register_and_get_token(client, "taskuser@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        # Create
        create_resp = await client.post(
            "/api/v1/tasks/",
            json={"title": "Learn FastAPI", "priority": "HIGH"},
            headers=headers,
        )
        assert create_resp.status_code == 201
        task_id = create_resp.json()["id"]

        # Get
        get_resp = await client.get(f"/api/v1/tasks/{task_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "Learn FastAPI"

    async def test_update_task(self, client: AsyncClient):
        token = await _register_and_get_token(client, "taskuser2@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        cr = await client.post(
            "/api/v1/tasks/",
            json={"title": "Old title"},
            headers=headers,
        )
        task_id = cr.json()["id"]
        patch = await client.patch(
            f"/api/v1/tasks/{task_id}",
            json={"title": "New title", "status": "IN_PROGRESS"},
            headers=headers,
        )
        assert patch.status_code == 200
        assert patch.json()["title"] == "New title"
        assert patch.json()["status"] == "IN_PROGRESS"

    async def test_delete_task(self, client: AsyncClient):
        token = await _register_and_get_token(client, "taskuser3@example.com")
        headers = {"Authorization": f"Bearer {token}"}

        cr = await client.post("/api/v1/tasks/", json={"title": "Temp"}, headers=headers)
        task_id = cr.json()["id"]
        del_resp = await client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
        assert del_resp.status_code == 204
