from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.models import Game, BetaAccess, Feedback, BugReport, User, ChangeLog
from app.schemas.betatesting import (
    GameCreate, GameResponse, BetaAccessCreate, BetaAccessResponse,
    FeedbackCreate, FeedbackResponse, BugReportCreate, BugReportResponse
)
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/games", response_model=List[GameResponse])
async def list_games(db: Session = Depends(get_db)):
    return db.query(Game).filter(Game.is_active == True).all()


@router.post("/games", response_model=GameResponse, status_code=201)
async def create_game(game: GameCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_game = Game(**game.model_dump(), author_id=current_user.id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


@router.get("/games/{game_id}", response_model=GameResponse)
async def get_game(game_id: str, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.post("/access", response_model=BetaAccessResponse, status_code=201)
async def purchase_beta_access(access: BetaAccessCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == access.game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    beta = BetaAccess(game_id=access.game_id, user_id=current_user.id, price=access.price, expires_at=access.expires_at)
    db.add(beta)
    db.commit()
    db.refresh(beta)
    return beta


@router.get("/my-access", response_model=List[BetaAccessResponse])
async def my_beta_access(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(BetaAccess).filter(BetaAccess.user_id == current_user.id).all()


@router.post("/feedback", response_model=FeedbackResponse, status_code=201)
async def submit_feedback(feedback: FeedbackCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_feedback = Feedback(**feedback.model_dump(), user_id=current_user.id)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


@router.post("/bugs", response_model=BugReportResponse, status_code=201)
async def report_bug(bug: BugReportCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_bug = BugReport(**bug.model_dump(), user_id=current_user.id)
    db.add(db_bug)
    db.commit()
    db.refresh(db_bug)
    return db_bug


@router.get("/bugs/{game_id}", response_model=List[BugReportResponse])
async def game_bugs(game_id: str, db: Session = Depends(get_db)):
    return db.query(BugReport).filter(BugReport.game_id == game_id).order_by(BugReport.created_at.desc()).all()
