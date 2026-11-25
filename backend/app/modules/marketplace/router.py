from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.models import Place, Module, Service, Order, Review, ChangeLog
from app.schemas.marketplace import PlaceCreate, PlaceResponse, ModuleCreate, ModuleResponse, OrderResponse
from app.api.deps import get_current_user
from app.core.models import User

router = APIRouter()


@router.get("/places", response_model=List[PlaceResponse])
async def list_places(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    places = db.query(Place).filter(Place.is_published == True).offset(skip).limit(limit).all()
    return places


@router.get("/places/{place_id}", response_model=PlaceResponse)
async def get_place(place_id: str, db: Session = Depends(get_db)):
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.post("/places", response_model=PlaceResponse, status_code=201)
async def create_place(place: PlaceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_place = Place(**place.model_dump(), author_id=current_user.id)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


@router.get("/modules", response_model=List[ModuleCreate])
async def list_modules(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Module).filter(Module.is_published == True).offset(skip).limit(limit).all()


@router.post("/modules", response_model=ModuleCreate, status_code=201)
async def create_module(module: ModuleCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_module = Module(**module.model_dump(), author_id=current_user.id)
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module


@router.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(product_type: str, product_id: str, amount: float, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = Order(user_id=current_user.id, product_type=product_type, product_id=product_id, amount=amount)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/orders", response_model=List[OrderResponse])
async def list_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()
