
# FitVibe - Upute za pokretanje

## Backend pokretanje (FastAPI)

1. Otvori terminal i uđi u backend folder:
```
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
2. Pokreni server:
```
uvicorn app.main:app --reload
```
Aplikacija će raditi na: http://localhost:8001

---

## Frontend pokretanje (React)

1. Otvori drugi terminal, uđi u frontend folder:
```
cd frontend
npm install
npm start
```
Aplikacija će biti dostupna na: http://localhost:3000

---

## Baza podataka

1. Pokreni `fitvibe_schema.sql` u SQLite da kreiraš tabele.
2. Pokreni `fitvibe_admin_trainer_seed.sql` da dodaš admina i trenera.

Admin Email: admin@fitvibe.com / Password: 12345  
Trainer Email: trainer@fitvibe.com / Password: 12345

Sve spremno! 🚀
