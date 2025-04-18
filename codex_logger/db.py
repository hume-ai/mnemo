import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()

# Default to SQLite, resolve relative paths to project root
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./codex_logger.db')
if DATABASE_URL.startswith('sqlite:///') and not DATABASE_URL.startswith('sqlite:////'):
    rel = DATABASE_URL[len('sqlite:///'):]
    base = os.getcwd()
    abs_path = os.path.abspath(os.path.join(base, rel))
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    DATABASE_URL = f'sqlite:///{abs_path}'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    path = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sessions = relationship('Session', back_populates='project')

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship('Project', back_populates='sessions')
    interactions = relationship('Interaction', back_populates='session')

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    prompt = Column(Text, nullable=False)
    chain_of_thought = Column(Text)
    response = Column(Text, nullable=False)
    model = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session = relationship('Session', back_populates='interactions')

def init_db():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)