from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.db.models import Project
from pydantic import BaseModel

router = APIRouter(prefix="/projects", tags=["projects"])

class ProjectCreate(BaseModel):
    name: str
    path: str

class ProjectOut(BaseModel):
    id: int
    name: str
    path: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    existing = db.query(Project).filter(Project.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Project already exists.")
    proj = Project(name=payload.name, path=payload.path)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@router.get("/", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()