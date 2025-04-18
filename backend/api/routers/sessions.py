from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.db.models import Project, Session as DBSession
from pydantic import BaseModel

router = APIRouter(prefix="/sessions", tags=["sessions"])

class SessionCreate(BaseModel):
    project_id: int
    title: str

class SessionOut(BaseModel):
    id: int
    project_id: int
    title: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SessionOut)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    if not db.query(Project).get(payload.project_id):
        raise HTTPException(status_code=404, detail="Project not found.")
    sess = DBSession(project_id=payload.project_id, title=payload.title)
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess

@router.get("/{project_id}", response_model=list[SessionOut])
def list_sessions(project_id: int, db: Session = Depends(get_db)):
    return db.query(DBSession).filter(DBSession.project_id == project_id).all()