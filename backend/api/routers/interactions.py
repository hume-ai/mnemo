from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.db.models import Interaction
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/interactions", tags=["interactions"])

class InteractionCreate(BaseModel):
    session_id: int
    prompt: str
    chain_of_thought: Optional[str] = None
    response: str
    model: str

class InteractionOut(BaseModel):
    id: int
    session_id: int
    prompt: str
    chain_of_thought: Optional[str]
    response: str
    model: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InteractionOut)
def create_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    inter = Interaction(**payload.dict())
    db.add(inter)
    db.commit()
    db.refresh(inter)
    return inter

@router.get("/{session_id}", response_model=list[InteractionOut])
def list_interactions(session_id: int, db: Session = Depends(get_db)):
    return db.query(Interaction).filter(Interaction.session_id == session_id).all()