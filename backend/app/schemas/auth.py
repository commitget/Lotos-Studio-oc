from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class Verify2FARequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)


class Enable2FAResponse(BaseModel):
    secret: str
    qrcode: str
    uri: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    role: str
    is_active: bool
    is_verified: bool
    totp_enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True
