from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Body
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app import database


from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.models import User, Trainer, Admin
from app.schemas import LoginData


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


SECRET_KEY = "b60fc9f20ad54217892305ef62b946c9b2db1e94f3424a349a6d0251d9abf709"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# ---------------- Registracija ----------------
@router.post("/register/user", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        email=user.email,
        gender=user.gender,
        goal=user.goal,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
 


@router.post("/register/trainer", response_model=schemas.Trainer)
def register_trainer(trainer: schemas.TrainerCreate, db: Session = Depends(get_db)):
    db_trainer = db.query(models.Trainer).filter(models.Trainer.email == trainer.email).first()
    if db_trainer:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(trainer.password)
    db_trainer = models.Trainer(
        first_name=trainer.first_name,
        last_name=trainer.last_name,
        phone=trainer.phone,
        email=trainer.email,
        password=hashed_password
    )
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer

# ---------------- Login ----------------

@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    # 1. Pokušaj kao user
    user = db.query(User).filter(User.email == data.email).first()
    if user and verify_password(data.password, user.password):  # ✅ ispravno polje
        token = create_access_token({"sub": user.email, "role": "user"})
        return {
            "access_token": token,
            "first_name": user.first_name,
            "role": "user",
            "user_id": user.id
        }

    # 2. Pokušaj kao trainer
    trainer = db.query(Trainer).filter(Trainer.email == data.email).first()
    if trainer and verify_password(data.password, trainer.password):  # ✅
        token = create_access_token({"sub": trainer.email, "role": "trainer"})
        return {
            "access_token": token,
            "first_name": trainer.first_name,
            "role": "trainer",
            "trainer_id": trainer.id
        }

    # 3. Pokušaj kao admin
    admin = db.query(Admin).filter(Admin.email == data.email).first()
    if admin and verify_password(data.password, admin.password):  # ✅
        token = create_access_token({"sub": admin.email, "role": "admin"})
        return {
            "access_token": token,
            "first_name": admin.full_name,
            "role": "admin",
            "admin_id": admin.id
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/reset-password")
def reset_password(email: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.password = get_password_hash(new_password)
        db.commit()
        return {"msg": "Password updated"}
    trainer = db.query(Trainer).filter(Trainer.email == email).first()
    if trainer:
        trainer.password = get_password_hash(new_password)
        db.commit()
        return {"msg": "Password updated"}
    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin:
        admin.password = get_password_hash(new_password)
        db.commit()
        return {"msg": "Password updated"}

    raise HTTPException(status_code=404, detail="Email not found")
