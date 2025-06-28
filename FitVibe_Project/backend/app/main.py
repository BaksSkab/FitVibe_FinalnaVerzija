from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from pathlib import Path
import os
from app.routers import auth
from app.trainer.routes import router as trainer_router
from fastapi.staticfiles import StaticFiles
from app.models import User, Trainer, Admin


# Učitavanje .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError(f"DATABASE_URL nije pronađen! Provjereni path: {env_path}")

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# FastAPI aplikacija
app = FastAPI()

# CORS podešavanja
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uključivanje ruta
app.include_router(auth.router)
app.include_router(trainer_router, prefix="/trainer", tags=["Trainer"])


# Statika
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dependency za bazu
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

# Root ruta
@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}

# Test konekcije
@app.get("/test_connection")
def test_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchall()
        return {
            "message": "Database connection is successful!",
            "result": [tuple(row) for row in result]
        }
    except Exception as e:
        return {"message": "Database connection failed", "error": str(e)}
