from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserProfileResponse(BaseModel):
    id: str
    user_id: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    roblox_username: Optional[str] = None
    roblox_id: Optional[str] = None
    discord_username: Optional[str] = None
    discord_id: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    roblox_username: Optional[str] = None
    roblox_id: Optional[str] = None
    discord_username: Optional[str] = None
    discord_id: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None


class UserSettingsResponse(BaseModel):
    id: str
    user_id: str
    email_notifications: bool
    discord_notifications: bool
    telegram_notifications: bool
    language: str
    theme: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserSettingsUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    discord_notifications: Optional[bool] = None
    telegram_notifications: Optional[bool] = None
    language: Optional[str] = None
    theme: Optional[str] = None
