from fastapi import APIRouter, Depends, HTTPException
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Admin
from app.admin.schemas import AdminLogin
from app.admin.services import authenticate_admin
from app.routers.auth import create_access_token
from app.models import User
from app.admin.schemas import UserOut
from app.schemas import UserOut, UserBase
from app.admin.schemas import UserUpdate
from typing import List
from app.models import Workout
from app.admin.schemas import WorkoutCreate, WorkoutOut
from app.models import MotivationalMessage
from app.admin.schemas import MessageCreate, MessageOut
from app.models import Challenge
from app.admin.schemas import ChallengeCreate, ChallengeOut
from app.admin.schemas import CategoryOut
from app.models import PlanCategory
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.security import create_access_token  


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login")
def admin_login(data: AdminLogin, db: Session = Depends(get_db)):
    admin = authenticate_admin(data.email, data.password, db)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": admin.email, "role": "admin"})
    return {"access_token": token, "token_type": "bearer"}


def authenticate_admin(email: str, password: str, db: Session):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        return None

    if not pwd_context.verify(password, admin.password):
        return None

    return admin

    
@router.get("/users", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in data.dict().items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user  

@router.get("/workouts", response_model=List[WorkoutOut])
def get_all_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).all()

@router.post("/workouts", response_model=WorkoutOut)
def create_workout(data: WorkoutCreate, db: Session = Depends(get_db)):
    workout = Workout(**data.dict())
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

@router.delete("/workouts/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()
    return

@router.put("/workouts/{workout_id}", response_model=WorkoutOut)
def update_workout(workout_id: int, data: WorkoutCreate, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    for field, value in data.dict().items():
        setattr(workout, field, value)
    
    db.commit()
    db.refresh(workout)
    return workout


@router.get("/messages", response_model=List[MessageOut])
def get_messages(db: Session = Depends(get_db)):
    return db.query(MotivationalMessage).order_by(MotivationalMessage.display_date.desc()).all()

@router.post("/messages", response_model=MessageOut)
def create_message(data: MessageCreate, db: Session = Depends(get_db)):
    message = MotivationalMessage(**data.dict())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.put("/messages/{message_id}", response_model=MessageOut)
def update_message(message_id: int, data: MessageCreate, db: Session = Depends(get_db)):
    message = db.query(MotivationalMessage).filter(MotivationalMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    for field, value in data.dict().items():
        setattr(message, field, value)
    db.commit()
    db.refresh(message)
    return message


@router.delete("/messages/{message_id}", status_code=204)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(MotivationalMessage).filter(MotivationalMessage.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()

from app.models import Challenge
from app.admin.schemas import ChallengeCreate, ChallengeOut


@router.get("/challenges", response_model=List[ChallengeOut])
def get_challenges(db: Session = Depends(get_db)):
    return db.query(Challenge).order_by(Challenge.id.desc()).all()


@router.post("/challenges", response_model=ChallengeOut)
def create_challenge(data: ChallengeCreate, db: Session = Depends(get_db)):
    challenge = Challenge(**data.dict())
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


@router.put("/challenges/{challenge_id}", response_model=ChallengeOut)
def update_challenge(challenge_id: int, data: ChallengeCreate, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    for field, value in data.dict().items():
        setattr(challenge, field, value)
    db.commit()
    db.refresh(challenge)
    return challenge


@router.delete("/challenges/{challenge_id}", status_code=204)
def delete_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    db.delete(challenge)
    db.commit()


@router.get("/categories", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(PlanCategory).all()

