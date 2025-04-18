from fastapi import FastAPI
from backend.db.database import engine, Base
from backend.api.routers import projects, sessions, interactions

Base.metadata.create_all(bind=engine)
app = FastAPI(title="codex-logger API")
"""
Enable CORS so that the frontend (http://localhost:3000) can access the API during development.
"""
from fastapi.middleware.cors import CORSMiddleware
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(sessions.router)
app.include_router(interactions.router)