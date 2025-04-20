from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Učitavanje .env fajla
load_dotenv()

# Uzmi podatke iz .env fajla
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Kreiranje URL-a za povezivanje sa bazom
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Kreiranje SQLAlchemy engine-a
engine = create_engine(DATABASE_URL)

# Kreiranje baze
Base = declarative_base()

# Kreiranje FastAPI aplikacije
app = FastAPI()

# Funkcija za dobijanje sesije
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
        # Pokrećemo jednostavan upit da proverimo da li postoji veza sa bazom
        result = db.execute("SELECT 1").fetchall()
        return {"message": "Database connection is successful!", "result": result}
    except Exception as e:
        return {"message": "Database connection failed", "error": str(e)}
