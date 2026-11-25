from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.core.models import (
    User, UserProfile, ChangeLog, Place, Module, Game, Order,
    Payment, Subscription, BetaAccess, Feedback, BugReport, SupportTicket
)
from app.schemas.admin import AdminUserUpdate, ChangeLogResponse, AdminStats
from app.schemas.auth import UserResponse
from app.schemas.marketplace import PlaceResponse
from app.schemas.support import SupportCreate, SupportResponse, SupportStatusUpdate
from app.api.deps import get_admin_user, get_super_admin, get_current_user

router = APIRouter()


@router.get("/stats", response_model=AdminStats)
async def get_stats(admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_orders = db.query(Order).count()
    total_places = db.query(Place).count()
    total_games = db.query(Game).count()
    total_payments = db.query(func.sum(Payment.amount)).filter(Payment.status == "completed").scalar() or 0
    active_subscriptions = db.query(Subscription).filter(Subscription.status == "active").count()
    recent_logins = db.query(ChangeLog).filter(
        ChangeLog.action == "login",
        ChangeLog.created_at >= datetime.now(timezone.utc) - timedelta(hours=24)
    ).count()

    return AdminStats(
        total_users=total_users,
        total_orders=total_orders,
        total_places=total_places,
        total_games=total_games,
        total_payments=total_payments,
        active_subscriptions=active_subscriptions,
        recent_logins=recent_logins,
    )


@router.get("/users", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 50, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, update: AdminUserUpdate, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in update.model_dump(exclude_none=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, admin: User = Depends(get_super_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


@router.get("/changelogs", response_model=List[ChangeLogResponse])
async def list_changelogs(skip: int = 0, limit: int = 50, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(ChangeLog).order_by(ChangeLog.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/places", response_model=List[PlaceResponse])
async def list_all_places(skip: int = 0, limit: int = 50, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(Place).order_by(Place.created_at.desc()).offset(skip).limit(limit).all()


@router.put("/places/{place_id}/publish")
async def toggle_place_publish(place_id: str, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    place.is_published = not place.is_published
    db.commit()
    return {"detail": f"Place {'published' if place.is_published else 'unpublished'}"}


@router.post("/db/reset")
async def reset_database(admin: User = Depends(get_super_admin), db: Session = Depends(get_db)):
    meta = db.get_bind().metadata
    for table in reversed(meta.sorted_tables):
        db.execute(table.delete())
    db.commit()
    return {"detail": "Database reset completed"}


@router.get("/support", response_model=List[SupportResponse])
async def list_support_tickets(admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).all()


@router.put("/support/{ticket_id}", response_model=SupportResponse)
async def update_ticket_status(ticket_id: str, update: SupportStatusUpdate, admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.status = update.status
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/audit/summary")
async def audit_summary(admin: User = Depends(get_admin_user), db: Session = Depends(get_db)):
    logs = db.query(ChangeLog).order_by(ChangeLog.created_at.desc()).limit(100).all()
    actions = {}
    for log in logs:
        actions[log.action] = actions.get(log.action, 0) + 1
    return {
        "total_logs": db.query(ChangeLog).count(),
        "recent_actions": actions,
        "recent_logs": [
            {"action": l.action, "entity": l.entity_type, "time": l.created_at.isoformat()}
            for l in logs[:20]
        ]
    }
