from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Body
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app import database


from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

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

@router.post("/login/user")
def login_user(form_data: schemas.LoginData, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    access_token = create_access_token(data={"sub": user.email, "role": "user", "id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "first_name": user.first_name
    }


@router.post("/login/trainer")
def login_trainer(form_data: schemas.LoginData, db: Session = Depends(get_db)):
    trainer = db.query(models.Trainer).filter(models.Trainer.email == form_data.email).first()
    if not trainer or not verify_password(form_data.password, trainer.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    access_token = create_access_token(data={"sub": trainer.email, "role": "trainer", "id": trainer.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "trainer_id": trainer.id,
        "first_name": trainer.first_name
    }


@router.post("/login/admin")
def login_admin(form_data: schemas.LoginData, db: Session = Depends(get_db)):
    

    admin = db.query(models.Admin).filter(models.Admin.email == form_data.email).first()
    if not admin or not verify_password(form_data.password, admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    access_token = create_access_token(data={"sub": admin.email, "role": "admin", "id": admin.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin_id": admin.id,
        "full_name": admin.full_name
    }






