from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.models import Payment, Invoice, Subscription, User
from app.schemas.billing import PaymentResponse, InvoiceResponse, SubscriptionCreate, SubscriptionResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/payments", response_model=List[PaymentResponse])
async def list_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Payment).filter(Payment.user_id == current_user.id).order_by(Payment.created_at.desc()).all()


@router.get("/invoices", response_model=List[InvoiceResponse])
async def list_invoices(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Invoice).filter(Invoice.user_id == current_user.id).order_by(Invoice.created_at.desc()).all()


@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=201)
async def create_subscription(sub: SubscriptionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subscription = Subscription(user_id=current_user.id, plan=sub.plan, price=sub.price, expires_at=sub.expires_at)
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


@router.get("/subscriptions", response_model=List[SubscriptionResponse])
async def list_subscriptions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Subscription).filter(Subscription.user_id == current_user.id).order_by(Subscription.created_at.desc()).all()


@router.get("/subscriptions/active", response_model=List[SubscriptionResponse])
async def active_subscriptions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Subscription).filter(Subscription.user_id == current_user.id, Subscription.status == "active").all()
