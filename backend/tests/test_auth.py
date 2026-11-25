"""Auth module unit and integration tests"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
from app.core.database import init_db, SessionLocal
from app.core.models import User, UserProfile, UserSettings, Session as UserSessionModel, ChangeLog
from app.core.security import hash_password, generate_salt


@pytest.fixture(scope="module")
def client():
    init_db()
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_db():
    db = SessionLocal()
    try:
        test_emails = [
            "test_auth@test.com", "test_auth2@test.com",
            "test_refresh@test.com", "test_me@test.com",
            "mp_user@test.com",
        ]
        # Disable FK checks to allow deletion
        db.execute(text("PRAGMA foreign_keys=OFF"))
        db.query(ChangeLog).filter(
            ChangeLog.user_id.in_(
                db.query(User.id).filter(User.email.in_(test_emails)).subquery()
            )
        ).delete(synchronize_session='fetch')
        db.query(UserSessionModel).filter(
            UserSessionModel.user_id.in_(
                db.query(User.id).filter(User.email.in_(test_emails)).subquery()
            )
        ).delete(synchronize_session='fetch')
        db.query(UserProfile).filter(
            UserProfile.user_id.in_(
                db.query(User.id).filter(User.email.in_(test_emails)).subquery()
            )
        ).delete(synchronize_session='fetch')
        db.query(UserSettings).filter(
            UserSettings.user_id.in_(
                db.query(User.id).filter(User.email.in_(test_emails)).subquery()
            )
        ).delete(synchronize_session='fetch')
        db.query(User).filter(User.email.in_(test_emails)).delete(synchronize_session='fetch')
        db.execute(text("PRAGMA foreign_keys=ON"))
        db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()


class TestRegistration:
    def test_register_success(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test_auth@test.com",
                "username": "testauth",
                "password": "TestPass123!",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_register_duplicate_email(self, client):
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test_auth@test.com",
                "username": "testauth",
                "password": "TestPass123!",
            },
        )
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test_auth@test.com",
                "username": "testauth2",
                "password": "TestPass123!",
            },
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_register_short_password(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test_short@test.com",
                "username": "shortpw",
                "password": "123",
            },
        )
        assert response.status_code == 422


class TestLogin:
    def test_login_success(self, client):
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test_auth2@test.com",
                "username": "testauth2",
                "password": "TestPass123!",
            },
        )
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test_auth2@test.com",
                "password": "TestPass123!",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_wrong_password(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test_auth2@test.com",
                "password": "WrongPass123!",
            },
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@test.com",
                "password": "TestPass123!",
            },
        )
        assert response.status_code == 401


class TestTokenRefresh:
    def test_refresh_token(self, client):
        reg_resp = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test_refresh@test.com",
                "username": "testrefresh",
                "password": "TestPass123!",
            },
        )
        assert reg_resp.status_code == 201, f"Register failed: {reg_resp.text}"
        reg = reg_resp.json()

        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": reg["refresh_token"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_refresh_invalid_token(self, client):
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token_here"},
        )
        assert response.status_code == 401


class TestMeEndpoint:
    def test_get_me(self, client):
        reg_resp = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test_me@test.com",
                "username": "testmeuser",
                "password": "TestPass123!",
            },
        )
        assert reg_resp.status_code == 201, f"Register failed: {reg_resp.text}"
        reg = reg_resp.json()

        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {reg['access_token']}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test_me@test.com"
        assert data["username"] == "testmeuser"

    def test_get_me_unauthorized(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
