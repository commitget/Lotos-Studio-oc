from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.models import Client, Project, Task, Contract, User, ChangeLog
from app.schemas.crm import ClientCreate, ClientResponse, ProjectCreate, ProjectResponse, TaskCreate, TaskResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/clients", response_model=List[ClientResponse])
async def list_clients(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Client).filter(Client.user_id == current_user.id).all()


@router.post("/clients", response_model=ClientResponse, status_code=201)
async def create_client(client: ClientCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_client = Client(**client.model_dump(), user_id=current_user.id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Project).join(Client).filter(Client.user_id == current_user.id).all()


@router.post("/projects", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == project.client_id, Client.user_id == current_user.id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    project = db.query(Project).join(Client).filter(
        Project.id == task.project_id,
        Client.user_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Task).join(Project).join(Client).filter(Client.user_id == current_user.id).all()
