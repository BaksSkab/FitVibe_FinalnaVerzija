from sqlalchemy.orm import Session
from app import models, schemas
from datetime import date

def update_user_profile(db: Session, user: models.User, update_data: schemas.UserBase):
    for attr, value in update_data.dict().items():
        setattr(user, attr, value)
    db.commit()
    db.refresh(user)
    return user

def get_today_motivation(db: Session):
    return db.query(models.MotivationalMessage).filter(models.MotivationalMessage.display_date == date.today()).first()

def get_all_challenges(db: Session):
    return db.query(models.Challenge).all()

def join_challenge(db: Session, user_id: int, challenge_id: int):
    exists = db.query(models.UserChallenge).filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if exists:
        return {"message": "Already joined"}
    new = models.UserChallenge(user_id=user_id, challenge_id=challenge_id)
    db.add(new)
    db.commit()
    return {"message": "Joined challenge"}

def get_user_challenges(db: Session, user_id: int):
    return db.query(models.UserChallenge).filter_by(user_id=user_id).all()

def get_user_progress(db: Session, user_id: int):
    return db.query(models.Progress).filter_by(user_id=user_id).all()

def add_progress(db: Session, user_id: int, progress_data: schemas.ProgressCreate):
    progress = models.Progress(**progress_data.dict(), user_id=user_id)
    db.add(progress)
    db.commit()
    return {"message": "Progress added"}

def get_all_plans(db: Session):
    return db.query(models.TrainerPlan).all()

def subscribe_user_to_plan(db: Session, user_id: int, plan_id: int):
    # TODO: napravi tabelu za povezivanje user-plan ako još ne postoji
    return {"message": f"User {user_id} subscribed to plan {plan_id}"}

def get_user_plans(db: Session, user_id: int):
    # TODO: povuci sve planove na koje je user prijavljen
    return []
