from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from pathlib import Path
import os
from routers import auth

from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError(f"DATABASE_URL nije pronađen! Provjereni path: {env_path}")



engine = create_engine(DATABASE_URL)


Base = declarative_base()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}

@app.get("/test_connection")
def test_connection(db: Session = Depends(get_db)):
    try:
        
        result = db.execute("SELECT 1").fetchall()
        return {"message": "Database connection is successful!", "result": result}
    except Exception as e:
        return {"message": "Database connection failed", "error": str(e)}
