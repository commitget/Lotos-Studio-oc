"""Admin module integration tests"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db
from app.core.models import User, UserRole
from app.core.security import hash_password, generate_salt


@pytest.fixture(scope="module")
def client():
    init_db()
    with TestClient(app) as c:
        yield c


def get_admin_token(client):
    # Admin is seeded on startup: admin@lotusstudio.dev / Admin123!
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@lotusstudio.dev", "password": "Admin123!"},
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


class TestAdminStats:
    def test_stats_requires_admin(self, client):
        response = client.get("/api/v1/admin/stats")
        assert response.status_code == 401

    def test_stats_as_admin(self, client):
        token = get_admin_token(client)
        assert token, "Admin login failed"
        response = client.get(
            "/api/v1/admin/stats",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_orders" in data
        assert "total_places" in data


class TestAdminUsers:
    def test_list_users(self, client):
        token = get_admin_token(client)
        response = client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        users = response.json()
        assert len(users) >= 1
        assert any(u["email"] == "admin@lotusstudio.dev" for u in users)

    def test_get_user(self, client):
        token = get_admin_token(client)
        users = client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        if users:
            response = client.get(
                f"/api/v1/admin/users/{users[0]['id']}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert response.status_code == 200

    def test_update_user(self, client):
        token = get_admin_token(client)
        users = client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        if users:
            user_id = users[0]["id"]
            response = client.put(
                f"/api/v1/admin/users/{user_id}",
                headers={"Authorization": f"Bearer {token}"},
                json={"is_verified": True},
            )
            assert response.status_code == 200
            assert response.json()["is_verified"] == True


class TestAdminChangelogs:
    def test_list_changelogs(self, client):
        token = get_admin_token(client)
        response = client.get(
            "/api/v1/admin/changelogs",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        logs = response.json()
        assert isinstance(logs, list)


class TestAdminAudit:
    def test_audit_summary(self, client):
        token = get_admin_token(client)
        response = client.get(
            "/api/v1/admin/audit/summary",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_logs" in data
        assert "recent_actions" in data
        assert "recent_logs" in data
