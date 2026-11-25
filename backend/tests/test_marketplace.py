"""Marketplace module integration tests"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import init_db


@pytest.fixture(scope="module")
def client():
    init_db()
    with TestClient(app) as c:
        yield c


def get_user_token(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "mp_user@test.com",
            "username": "mpuser",
            "password": "TestPass123!",
        },
    )
    if response.status_code == 201:
        return response.json()["access_token"]
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "mp_user@test.com", "password": "TestPass123!"},
    )
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None


def get_admin_token(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@lotusstudio.dev", "password": "Admin123!"},
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


class TestPlaces:
    def test_list_places_empty(self, client):
        response = client.get("/api/v1/marketplace/places")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_place(self, client):
        token = get_user_token(client)
        response = client.post(
            "/api/v1/marketplace/places",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Test Place",
                "description": "A test Roblox place",
                "price": 49.99,
                "category": "obby",
                "tags": ["obby", "fun"],
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Place"
        assert data["price"] == 49.99


class TestOrders:
    def test_create_order(self, client):
        token = get_user_token(client)
        response = client.post(
            "/api/v1/marketplace/orders?product_type=place&product_id=test123&amount=29.99",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["product_type"] == "place"

    def test_list_orders(self, client):
        token = get_user_token(client)
        response = client.get(
            "/api/v1/marketplace/orders",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)
