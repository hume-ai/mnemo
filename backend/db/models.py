from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from backend.db.database import Base
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    path = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("Session", back_populates="project")

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="sessions")
    interactions = relationship("Interaction", back_populates="session")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    prompt = Column(Text, nullable=False)
    chain_of_thought = Column(Text)
    response = Column(Text, nullable=False)
    model = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="interactions")