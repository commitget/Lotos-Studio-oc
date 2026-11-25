from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    currency: str
    status: str
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: str
    user_id: str
    payment_id: Optional[str] = None
    amount: float
    status: str
    due_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    plan: str
    price: float
    expires_at: Optional[datetime] = None


class SubscriptionResponse(BaseModel):
    id: str
    user_id: str
    plan: str
    status: str
    price: float
    started_at: datetime
    expires_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
