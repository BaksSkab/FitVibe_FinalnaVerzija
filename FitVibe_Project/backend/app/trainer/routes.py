from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.trainer import services, models, schemas
from app.dependencies import get_db
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_current_trainer
from app.trainer.services import update_trainer_profile
from app.trainer.models import Trainer
import os
import shutil

router = APIRouter()

@router.get("/test")
def test_trainer_route():
    return {"message": "Trainer route is working!"}

@router.get("/plans", response_model=List[schemas.TrainerPlanOut])
def get_trainer_plans(
    db: Session = Depends(get_db),
    trainer = Depends(get_current_trainer)
):
    return services.get_trainer_plans(db, trainer.id)

@router.get("/workouts", response_model=List[schemas.WorkoutOut])
def get_all_workouts(db: Session = Depends(get_db)):
    return services.get_all_workouts(db)


from fastapi import Form

@router.post("/workouts")
def create_workout_with_image(
    title: str = Form(...),
    description: str = Form(...),
    repetitions: int = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    trainer=Depends(get_current_trainer)
):
    image_url = None
    if image:
        upload_dir = "app/static/workout_images"
        os.makedirs(upload_dir, exist_ok=True)

        filename = f"workout_{trainer.id}_{image.filename}"
        filepath = os.path.join(upload_dir, filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_url = f"/static/workout_images/{filename}"

    workout = models.Workout(
        title=title,
        description=description,
        repetitions=repetitions,
        image_filename=filename,
        trainer_id=trainer.id
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


@router.post("/plans", response_model=schemas.TrainerPlanOut)
def create_plan(
    plan_data: schemas.TrainerPlanCreate,
    db: Session = Depends(get_db),
    trainer = Depends(get_current_trainer)
):
    return services.create_trainer_plan(db, plan_data, trainer.id)

@router.get("/plans/{plan_id}", response_model=schemas.TrainerPlanDetail)
def get_plan_detail(plan_id: int, db: Session = Depends(get_db), trainer=Depends(get_current_trainer)):
    result = services.get_plan_with_workouts(db, plan_id)
    if not result:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan, workouts = result
    return schemas.TrainerPlanDetail(
        id=plan.id,
        plan_name=plan.plan_name,
        description=plan.description,
        level=plan.level,
        goal=plan.goal,
        category_id=plan.category_id,
        workouts=[schemas.WorkoutOut.model_validate(w) for w in workouts]  # konverzija
    )

@router.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db), trainer=Depends(get_current_trainer)):
    return services.delete_trainer_plan(db, plan_id, trainer.id)

@router.delete("/plans/{plan_id}/workouts/{workout_id}")
def remove_workout_from_plan(plan_id: int, workout_id: int, db: Session = Depends(get_db), trainer=Depends(get_current_trainer)):
    return services.remove_workout_from_plan(db, plan_id, workout_id)

@router.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db), trainer=Depends(get_current_trainer)):
    return services.delete_workout(db, workout_id)

@router.post("/plans/{plan_id}/workouts")
def add_workouts_to_plan(
    plan_id: int,
    workout_ids: List[int],
    db: Session = Depends(get_db),
    trainer=Depends(get_current_trainer)
):
    return services.add_workouts_to_existing_plan(db, trainer.id, plan_id, workout_ids)

@router.post("/plans/{plan_id}/add_workouts")
def add_workouts_to_plan(
    plan_id: int,
    payload: schemas.WorkoutIDsInPlan,
    db: Session = Depends(get_db),
    trainer=Depends(get_current_trainer)
):
    return services.add_workouts_to_existing_plan(
        db=db,
        trainer_id=trainer.id,
        plan_id=plan_id,
        workout_ids=payload.workout_ids
    )

@router.get("/profile", response_model=schemas.TrainerProfileOut)
def get_profile(
    db: Session = Depends(get_db),
    trainer=Depends(get_current_trainer),
):
    refreshed = db.query(Trainer).filter(Trainer.id == trainer.id).first()
    return refreshed



@router.put("/profile", response_model=schemas.TrainerProfileOut)
def update_profile(
    profile_data: schemas.TrainerProfileUpdate,
    db: Session = Depends(get_db),
    trainer: models.Trainer = Depends(get_current_trainer),
):
    updated_trainer = update_trainer_profile(db, trainer.id, profile_data)
    if not updated_trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return updated_trainer

@router.post("/profile/upload_image")
def upload_profile_image(
    file: UploadFile = File(...),
    trainer=Depends(get_current_trainer),
):
    upload_dir = "app/static/profile_images"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"trainer_{trainer.id}.jpg"
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    trainer.profile_image_url = f"/static/profile_images/{filename}"
    db = next(get_db()) 
    db.add(trainer)
    db.commit()

    return {"message": "Image uploaded successfully", "image_url": trainer.profile_image}

@router.get("/plans/{plan_id}/users", response_model=List[schemas.UserOut])
def get_users_for_trainer_plan(plan_id: int, db: Session = Depends(get_db), trainer=Depends(get_current_trainer)):
    plan = db.query(models.TrainerPlan).filter_by(id=plan_id, trainer_id=trainer.id).first()
    if not plan:
        raise HTTPException(status_code=403, detail="You don't have access to this plan.")

    return services.get_users_for_plan(db, plan_id)

@router.get("/plans/{plan_id}/user_count")
def get_user_count_for_plan(plan_id: int, db: Session = Depends(get_db), trainer=Depends(get_current_trainer)):
    count = (
        db.query(models.UserTrainerPlan)
        .filter(models.UserTrainerPlan.trainer_plan_id == plan_id)
        .count()
    )
    return {"plan_id": plan_id, "user_count": count}

@router.delete("/plans/{plan_id}/users/{user_id}")
def remove_user_from_plan(
    plan_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    trainer=Depends(get_current_trainer)
):

    relation = (
        db.query(models.UserTrainerPlan)
        .filter_by(trainer_plan_id=plan_id, user_id=user_id)
        .first()
    )
    if not relation:
        raise HTTPException(status_code=404, detail="The user is not signed in to this plan.")

    db.delete(relation)
    db.commit()
    return {"message": "The user has been removed from the plan."}

@router.get("/notifications", response_model=List[schemas.NotificationOut])
def get_trainer_notifications(
    db: Session = Depends(get_db),
    trainer=Depends(get_current_trainer)
):
    return services.get_notifications(db, trainer.id)

@router.post("/notifications")
def create_notification_for_trainer(
    payload: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    trainer=Depends(get_current_trainer)
):
    return services.create_notification(db, trainer.id, payload.message)

@router.put("/notifications/{notification_id}/read", response_model=schemas.NotificationOut)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    trainer=Depends(get_current_trainer)
):
    return services.mark_notification_as_read(db, notification_id)
