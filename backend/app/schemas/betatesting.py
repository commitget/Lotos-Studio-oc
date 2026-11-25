from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GameCreate(BaseModel):
    title: str
    description: Optional[str] = None
    roblox_game_id: Optional[str] = None
    image_url: Optional[str] = None


class GameResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    roblox_game_id: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    author_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BetaAccessCreate(BaseModel):
    game_id: str
    price: float
    expires_at: Optional[datetime] = None


class BetaAccessResponse(BaseModel):
    id: str
    game_id: str
    user_id: str
    price: float
    is_active: bool
    expires_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    game_id: str
    text: str
    rating: Optional[int] = None


class FeedbackResponse(BaseModel):
    id: str
    game_id: str
    user_id: str
    text: str
    rating: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BugReportCreate(BaseModel):
    game_id: str
    title: str
    description: str
    severity: Optional[str] = "low"


class BugReportResponse(BaseModel):
    id: str
    game_id: str
    user_id: str
    title: str
    description: str
    severity: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
