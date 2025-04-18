import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Default to SQLite file; allow overriding with DATABASE_URL in .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./codex_logger.db")
# If using a relative SQLite path, resolve it against the project root (two levels up)
if DATABASE_URL.startswith("sqlite:///") and not DATABASE_URL.startswith("sqlite:////"):
    # strip the sqlite:/// prefix to get the relative path
    rel_path = DATABASE_URL[len("sqlite:///"):]
    # project root is two directories above this file
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    abs_path = os.path.join(base_dir, rel_path)
    # ensure parent directory exists
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    DATABASE_URL = f"sqlite:///{abs_path}"

engine = create_engine(
     DATABASE_URL, connect_args={"check_same_thread": False}
 )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()