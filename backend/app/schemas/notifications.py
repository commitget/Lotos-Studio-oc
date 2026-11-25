from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    type: str
    title: str
    message: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationTemplateCreate(BaseModel):
    name: str
    subject: Optional[str] = None
    body: str
    type: str


class NotificationTemplateResponse(BaseModel):
    id: str
    name: str
    subject: Optional[str] = None
    body: str
    type: str
    created_at: datetime

    class Config:
        from_attributes = True
