from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.models import Notification, NotificationTemplate, User, ChangeLog
from app.schemas.notifications import NotificationResponse, NotificationTemplateCreate, NotificationTemplateResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == current_user.id).order_by(Notification.created_at.desc()).limit(50).all()


@router.get("/unread", response_model=List[NotificationResponse])
async def unread_notifications(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == current_user.id, Notification.is_read == False).all()


@router.post("/{notification_id}/read")
async def mark_read(notification_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user.id).first()
    if notif:
        notif.is_read = True
        db.commit()
    return {"detail": "Marked as read"}


@router.post("/read-all")
async def mark_all_read(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Notification).filter(Notification.user_id == current_user.id, Notification.is_read == False).update({"is_read": True})
    db.commit()
    return {"detail": "All marked as read"}


@router.get("/templates", response_model=List[NotificationTemplateResponse])
async def list_templates(db: Session = Depends(get_db)):
    return db.query(NotificationTemplate).all()


@router.post("/templates", response_model=NotificationTemplateResponse, status_code=201)
async def create_template(template: NotificationTemplateCreate, db: Session = Depends(get_db)):
    db_template = NotificationTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template
