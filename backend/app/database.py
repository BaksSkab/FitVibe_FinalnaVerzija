from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Učitavanje .env fajla
load_dotenv()

# Tvoj URL za povezivanje sa bazom
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:hWKbuxTYfWZRTrYaSUrxiqwqaYkofyPx@metro.proxy.rlwy.net:30907/railway")

# Kreiranje SQLAlchemy engine-a
engine = create_engine(DATABASE_URL)

# Kreiranje sesije
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kreiranje baze
Base = declarative_base()

# Funkcija za dobijanje sesije
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
