from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from app.core.models import UserRole


class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class ChangeLogResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    changes: Optional[Any] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AdminStats(BaseModel):
    total_users: int
    total_orders: int
    total_places: int
    total_games: int
    total_payments: float
    active_subscriptions: int
    recent_logins: int
