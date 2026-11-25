from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.core.models import User, UserProfile, UserSettings, Session as UserSession, ChangeLog
from app.core.security import (
    generate_salt, hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
    generate_totp_secret, verify_totp, generate_totp_qrcode, sanitize_input
)
from app.repositories.base import BaseRepository
from app.core.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = BaseRepository(User, db)

    def register(self, email: str, username: str, password: str) -> User:
        existing = self.user_repo.filter_by(email=email)
        if existing:
            raise ValueError("Email already registered")
        existing = self.user_repo.filter_by(username=username)
        if existing:
            raise ValueError("Username already taken")

        salt = generate_salt()
        hashed = hash_password(password, salt)

        user = self.user_repo.create(
            email=sanitize_input(email),
            username=sanitize_input(username),
            hashed_password=hashed,
            salt=salt,
        )
        profile = UserProfile(user_id=user.id)
        self.db.add(profile)
        settings = UserSettings(user_id=user.id)
        self.db.add(settings)
        log = ChangeLog(
            user_id=user.id,
            action="register",
            entity_type="user",
            entity_id=user.id,
        )
        self.db.add(log)
        self.db.commit()

        return user

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.filter_by(email=email)
        if not user:
            return None
        user = user[0]
        if not verify_password(password, user.hashed_password, user.salt):
            return None
        if not user.is_active:
            return None
        return user

    def create_tokens(self, user: User) -> dict:
        access_token = create_access_token({"sub": user.id, "role": user.role.value})
        refresh_token = create_refresh_token({"sub": user.id})
        return {"access_token": access_token, "refresh_token": refresh_token}

    def save_session(self, user_id: str, refresh_token: str, ip: str = None, ua: str = None) -> UserSession:
        session = UserSession(
            user_id=user_id,
            refresh_token=refresh_token,
            ip_address=ip,
            user_agent=ua,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def refresh_tokens(self, refresh_token: str) -> Optional[dict]:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")
        user = self.user_repo.get(user_id)
        if not user or not user.is_active:
            return None

        sessions = self.user_repo.db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.refresh_token == refresh_token,
            UserSession.is_active == True,
        ).all()

        if not sessions:
            return None

        return self.create_tokens(user)

    def enable_2fa(self, user: User) -> dict:
        secret = generate_totp_secret()
        user.totp_secret = secret
        self.db.commit()
        qrcode = generate_totp_qrcode(secret, user.email)
        uri = f"otpauth://totp/{settings.TOTP_ISSUER}:{user.email}?secret={secret}&issuer={settings.TOTP_ISSUER}"
        return {"secret": secret, "qrcode": qrcode, "uri": uri}

    def verify_2fa(self, user: User, code: str) -> bool:
        if not user.totp_secret:
            return False
        return verify_totp(user.totp_secret, code)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.user_repo.get(user_id)
