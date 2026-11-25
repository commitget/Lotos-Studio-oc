from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PlaceCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    file_url: Optional[str] = None
    image_url: Optional[str] = None


class PlaceResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    tags: Optional[list] = None
    file_url: Optional[str] = None
    image_url: Optional[str] = None
    is_published: bool
    author_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    file_url: Optional[str] = None


class ModuleResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    tags: Optional[list] = None
    file_url: Optional[str] = None
    is_published: bool
    author_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: str
    user_id: str
    product_type: str
    product_id: str
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
