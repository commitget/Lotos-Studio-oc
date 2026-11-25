from typing import Any, Dict, List, Optional, TypeVar, Generic, Type
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: str) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, skip: int = 0, limit: int = 100, order_by: str = "created_at", order_dir: str = "desc") -> List[ModelType]:
        order_fn = desc if order_dir == "desc" else asc
        return self.db.query(self.model).order_by(order_fn(getattr(self.model, order_by))).offset(skip).limit(limit).all()

    def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: str, **kwargs) -> Optional[ModelType]:
        obj = self.get(id)
        if not obj:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id: str) -> bool:
        obj = self.get(id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def count(self) -> int:
        return self.db.query(self.model).count()

    def filter_by(self, **kwargs) -> List[ModelType]:
        return self.db.query(self.model).filter_by(**kwargs).all()
