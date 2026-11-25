"""Security module tests"""

import pytest
from app.core.security import (
    hash_password, verify_password, generate_salt,
    create_access_token, create_refresh_token, decode_token,
    generate_totp_secret, verify_totp, sanitize_input,
)


class TestPasswordHashing:
    def test_hash_and_verify(self):
        salt = generate_salt()
        password = "TestPassword123!"
        hashed = hash_password(password, salt)
        assert hashed != password
        assert verify_password(password, hashed, salt) is True

    def test_wrong_password(self):
        salt = generate_salt()
        hashed = hash_password("CorrectPass123!", salt)
        assert verify_password("WrongPass123!", hashed, salt) is False

    def test_different_salts(self):
        password = "SamePassword"
        salt1 = generate_salt()
        salt2 = generate_salt()
        hash1 = hash_password(password, salt1)
        hash2 = hash_password(password, salt2)
        assert hash1 != hash2


class TestJWT:
    def test_create_access_token(self):
        token = create_access_token({"sub": "user123", "role": "admin"})
        assert token is not None
        payload = decode_token(token)
        assert payload["sub"] == "user123"
        assert payload["role"] == "admin"
        assert payload["type"] == "access"

    def test_create_refresh_token(self):
        token = create_refresh_token({"sub": "user123"})
        payload = decode_token(token)
        assert payload["sub"] == "user123"
        assert payload["type"] == "refresh"

    def test_expired_token(self):
        from datetime import timedelta
        token = create_access_token({"sub": "test"}, expires_delta=timedelta(seconds=-1))
        payload = decode_token(token)
        assert payload is None

    def test_invalid_token(self):
        payload = decode_token("invalid.token.here")
        assert payload is None


class TestTOTP:
    def test_generate_secret(self):
        secret = generate_totp_secret()
        assert len(secret) > 10
        assert isinstance(secret, str)

    def test_verify_valid_code(self):
        secret = generate_totp_secret()
        import pyotp
        totp = pyotp.TOTP(secret)
        code = totp.now()
        assert verify_totp(secret, code) is True

    def test_verify_invalid_code(self):
        secret = generate_totp_secret()
        assert verify_totp(secret, "000000") is False


class TestSanitizeInput:
    def test_remove_html(self):
        result = sanitize_input("<script>alert('xss')</script>")
        assert "script" in result
        assert "alert" in result
        assert "xss" in result
        assert sanitize_input("Hello World") == "Hello World"
        assert sanitize_input("  spaced  ") == "spaced"
        assert sanitize_input("normal text") == "normal text"
