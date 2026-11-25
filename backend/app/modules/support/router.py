from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import SupportTicket, User
from app.schemas.support import SupportCreate, SupportResponse
from app.api.deps import get_current_user
from typing import List

router = APIRouter()


@router.post("/tickets", response_model=SupportResponse, status_code=201)
async def create_ticket(ticket: SupportCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_ticket = SupportTicket(**ticket.model_dump(), user_id=current_user.id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@router.get("/tickets", response_model=List[SupportResponse])
async def list_my_tickets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SupportTicket).filter(SupportTicket.user_id == current_user.id).order_by(SupportTicket.created_at.desc()).all()
