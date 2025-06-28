from sqlalchemy.orm import Session
from app.trainer import models, schemas
from typing import List
from app.trainer.models import TrainerNotification
from fastapi import HTTPException

def get_trainer_plans(db: Session, trainer_id: int):
    return db.query(models.TrainerPlan).filter(models.TrainerPlan.trainer_id == trainer_id).all()

def get_users_for_plan(db: Session, plan_id: int):
    return (
        db.query(models.User)
        .join(models.UserTrainerPlan, models.User.id == models.UserTrainerPlan.user_id)
        .filter(models.UserTrainerPlan.trainer_plan_id == plan_id)
        .all()
    )
    
def get_all_workouts(db: Session):
    return db.query(models.Workout).all()

def create_trainer_plan(db: Session, plan_data: schemas.TrainerPlanCreate, trainer_id: int):
    new_plan = models.TrainerPlan(
        plan_name=plan_data.plan_name,
        description=plan_data.description,
        level=plan_data.level,
        goal=plan_data.goal,
        category_id=plan_data.category_id,
        trainer_id=trainer_id
    )
    db.add(new_plan)
    db.commit()
    message = f"New plan created: {new_plan.plan_name}"
    notification = TrainerNotification(trainer_id=trainer_id, message=message)
    db.add(notification)
    db.commit()

    db.refresh(new_plan)

    for workout_id in plan_data.workout_ids:
        link = models.TrainerPlanWorkout(
            trainer_plan_id=new_plan.id,
            workout_id=workout_id
        )
        db.add(link)

    db.commit()
    return new_plan

def get_plan_with_workouts(db: Session, plan_id: int):
    plan = db.query(models.TrainerPlan).filter(models.TrainerPlan.id == plan_id).first()
    if not plan:
        return None

    workouts = (
        db.query(models.Workout)
        .join(models.TrainerPlanWorkout, models.Workout.id == models.TrainerPlanWorkout.workout_id)
        .filter(models.TrainerPlanWorkout.trainer_plan_id == plan_id)
        .all()
    )

    return plan, workouts

def delete_trainer_plan(db: Session, plan_id: int, trainer_id: int):
    plan = db.query(models.TrainerPlan).filter_by(id=plan_id, trainer_id=trainer_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")

    db.query(models.TrainerPlanWorkout).filter_by(trainer_plan_id=plan_id).delete() # brisanje veze sa vjezbama

    db.delete(plan)
    db.commit()
    message = f"Plan '{plan.plan_name}' has been deleted."
    notification = TrainerNotification(trainer_id=trainer_id, message=message)
    db.add(notification)
    db.commit()



def create_workout(db: Session, workout_data: schemas.WorkoutCreate, trainer_id: int):
    new_workout = models.Workout(
        title=workout_data.title,
        description=workout_data.description,
        repetitions=workout_data.repetitions,
        trainer_id=trainer_id
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    message = f"Added new workout: {new_workout.title}"
    notification = TrainerNotification(trainer_id=trainer_id, message=message)
    db.add(notification)
    db.commit()

    return new_workout

def remove_workout_from_plan(db: Session, plan_id: int, workout_id: int):
    link = db.query(models.TrainerPlanWorkout).filter_by(
        trainer_plan_id=plan_id,
        workout_id=workout_id
    ).first()
    if link:
        db.delete(link)
        db.commit()
    message = f"Workout {workout_id} has been removed from the plan {plan_id}."
    plan = db.query(models.TrainerPlan).filter_by(id=plan_id).first()
    if plan:
        notification = TrainerNotification(trainer_id=plan.trainer_id, message=message)
        db.add(notification)
        db.commit()


def delete_workout(db: Session, workout_id: int):
    db.query(models.TrainerPlanWorkout).filter_by(workout_id=workout_id).delete()
    workout = db.query(models.Workout).filter_by(id=workout_id).first()
    if workout:
        db.delete(workout)
        db.commit()
    message = f"Workout '{workout.title}' has been removed from the base."
    notification = TrainerNotification(trainer_id=workout.trainer_id, message=message)
    db.add(notification)
    db.commit()


def add_workouts_to_existing_plan(db: Session, trainer_id: int, plan_id: int, workout_ids: List[int]):
    plan = db.query(models.TrainerPlan).filter_by(id=plan_id, trainer_id=trainer_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found or does not belong to this trainer.")

    existing_ids = {
        tw.workout_id
        for tw in db.query(models.TrainerPlanWorkout)
        .filter(models.TrainerPlanWorkout.trainer_plan_id == plan_id)
        .all()
    }

    new_links = [
        models.TrainerPlanWorkout(trainer_plan_id=plan_id, workout_id=w_id)
        for w_id in workout_ids if w_id not in existing_ids
    ]

    db.add_all(new_links)
    db.commit()
    message = f"{len(new_links)} workouts added to the plan '{plan.plan_name}'"
    notification = TrainerNotification(trainer_id=trainer_id, message=message)
    db.add(notification)
    db.commit()


def get_trainer_profile(db: Session, trainer_id: int):
    trainer = db.query(models.Trainer).filter(models.Trainer.id == trainer_id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer


def update_trainer_profile(db: Session, trainer_id: int, profile_data: schemas.TrainerProfileUpdate):
    trainer = db.query(models.Trainer).filter(models.Trainer.id == trainer_id).first()
    if not trainer:
        return None

    trainer.first_name = profile_data.first_name
    trainer.last_name = profile_data.last_name
    trainer.phone = profile_data.phone
    trainer.bio = profile_data.bio
    trainer.education = profile_data.education
    trainer.achievements = profile_data.achievements
    trainer.instagram_url = profile_data.instagram_url
    trainer.linkedin_url = profile_data.linkedin_url
    trainer.profile_image_url = profile_data.profile_image_url

    db.commit()
    db.refresh(trainer)
    return trainer


def create_notification(db: Session, trainer_id: int, message: str):
    notification = models.TrainerNotification(
        trainer_id=trainer_id,
        message=message
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_notifications(db: Session, trainer_id: int):
    return (
        db.query(models.TrainerNotification)
        .filter(models.TrainerNotification.trainer_id == trainer_id)
        .order_by(models.TrainerNotification.created_at.desc())
        .all()
    )

def mark_notification_as_read(db: Session, notification_id: int):
    notification = db.query(models.TrainerNotification).filter_by(id=notification_id).first()
    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)
    return notification

def user_join_plan(db: Session, user_id: int, plan_id: int):
    existing = db.query(models.UserTrainerPlan).filter_by(user_id=user_id, trainer_plan_id=plan_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You are already signed up for the plan.")

    user_plan = models.UserTrainerPlan(user_id=user_id, trainer_plan_id=plan_id)
    db.add(user_plan)

    plan = db.query(models.TrainerPlan).filter_by(id=plan_id).first()
    trainer_id = plan.trainer_id

    user = db.query(models.User).filter_by(id=user_id).first()
    message = f"{user.first_name} signed up for your plan: {plan.plan_name}"

    notification = TrainerNotification(
        trainer_id=trainer_id,
        message=message
    )
    db.add(notification)

    db.commit()
