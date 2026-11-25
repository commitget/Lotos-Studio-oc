from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SupportCreate(BaseModel):
    subject: str
    message: str


class SupportStatusUpdate(BaseModel):
    status: str


class SupportResponse(BaseModel):
    id: str
    user_id: str
    subject: str
    message: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
