from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.dependencies import get_current_user, get_db
from datetime import date, datetime

router = APIRouter()

# === USER PROFILE ===
@router.get("/profile", response_model=schemas.User)
def get_user_profile(user: models.User = Depends(get_current_user)):
    return user

@router.put("/profile", response_model=schemas.User)
def update_user_profile(update_data: schemas.UserBase, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    user.first_name = update_data.first_name
    user.last_name = update_data.last_name
    user.phone = update_data.phone
    user.gender = update_data.gender
    user.goal = update_data.goal
    db.commit()
    db.refresh(user)
    return user

# === MOTIVATIONAL MESSAGE ===
@router.get("/motivational-message", response_model=schemas.MotivationalMessage)
def get_motivational_message(db: Session = Depends(get_db)):
    today = date.today()
    message = (
        db.query(models.MotivationalMessage)
        .filter(models.MotivationalMessage.display_date == today)
        .first()
    )
    if message:
        return message
    fallback = db.query(models.MotivationalMessage).first()
    if fallback:
        return fallback
    return {"content": "Stay strong and focused today!"}

# === USER PROGRESS ===
@router.get("/my-progress", response_model=list[schemas.Progress])
def get_user_progress(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return db.query(models.Progress).filter(models.Progress.user_id == user.id).all()

# === ALL PLANS ===
@router.get("/plans", response_model=list[schemas.TrainerPlan])
def get_all_plans(db: Session = Depends(get_db)):
    return db.query(models.TrainerPlan).all()

# === SUBSCRIBE TO PLAN ===
@router.post("/plans/{trainer_plan_id}/subscribe")
def subscribe_to_plan(trainer_plan_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    existing = db.query(models.UserTrainerPlan).filter_by(user_id=user.id, trainer_plan_id=trainer_plan_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already subscribed.")
    subscription = models.UserTrainerPlan(user_id=user.id, trainer_plan_id=trainer_plan_id)
    db.add(subscription)
    db.commit()
    return {"message": "Successfully subscribed to plan."}

# === USER'S SUBSCRIBED PLANS ===
@router.get("/my-plans", response_model=list[schemas.UserTrainerPlanOut])
def get_user_plans(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # Koristimo joinedload da bismo dobili i podatke o treneru i vježbama uz plan
    plans = (
        db.query(models.UserTrainerPlan)
        .options(
            joinedload(models.UserTrainerPlan.trainer_plan)
            .joinedload(models.TrainerPlan.trainer),   # učitavamo trenera
            joinedload(models.UserTrainerPlan.trainer_plan)
            .joinedload(models.TrainerPlan.workouts)   # ako trebaš vježbe
        )
        .filter(models.UserTrainerPlan.user_id == user.id)
        .all()
    )
    # Debug print (možeš obrisati poslije)
    print(f"User {user.id} plans with trainer info: {plans}")
    return plans

# === UNSUBSCRIBE FROM PLAN ===
@router.delete("/my-plans/{trainer_plan_id}")
def unsubscribe_from_plan(trainer_plan_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    subscription = db.query(models.UserTrainerPlan).filter_by(user_id=user.id, trainer_plan_id=trainer_plan_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    db.delete(subscription)
    db.commit()
    return {"message": "Successfully unsubscribed from plan."}

# === ADD PROGRESS ===
@router.post("/progress")
def add_progress(
    workout_id: int = Body(...),
    actual_result: str = Body(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    new_progress = models.Progress(
        user_id=user.id,
        workout_id=workout_id,
        actual_result=actual_result,
        created_at=datetime.utcnow()
    )
    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    return {"message": "Progress added successfully", "progress_id": new_progress.id}
