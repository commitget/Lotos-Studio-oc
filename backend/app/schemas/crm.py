from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClientCreate(BaseModel):
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None


class ClientResponse(BaseModel):
    id: str
    user_id: str
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    client_id: str
    title: str
    description: Optional[str] = None
    budget: Optional[float] = None
    deadline: Optional[datetime] = None


class ProjectResponse(BaseModel):
    id: str
    client_id: str
    title: str
    description: Optional[str] = None
    status: str
    budget: Optional[float] = None
    deadline: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    project_id: str
    title: str
    description: Optional[str] = None
    assignee_id: Optional[str] = None
    priority: Optional[str] = "medium"


class TaskResponse(BaseModel):
    id: str
    project_id: str
    title: str
    description: Optional[str] = None
    assignee_id: Optional[str] = None
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
