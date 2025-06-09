from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime

class TrainerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str | None = None

class TrainerOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)

class TrainerPlanOut(BaseModel):
    id: int
    plan_name: str
    description: str
    level: str
    goal: str
    category_id: int

    model_config = ConfigDict(from_attributes=True)

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    gender: str
    goal: str
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)

class WorkoutOut(BaseModel):
    id: int
    title: str
    description: str
    repetitions: int
    trainer_id: int
    image_filename: str | None = None

    model_config = ConfigDict(from_attributes=True)

class TrainerPlanCreate(BaseModel):
    plan_name: str
    description: str
    level: str
    goal: str
    category_id: int
    workout_ids: List[int]

class TrainerPlanDetail(BaseModel):
    id: int
    plan_name: str
    description: str
    level: str
    goal: str
    category_id: int
    workouts: List[WorkoutOut]

    model_config = ConfigDict(from_attributes=True)

class WorkoutCreate(BaseModel):
    title: str
    description: str
    repetitions: int

class WorkoutIDsInPlan(BaseModel):
    workout_ids: List[int]


class TrainerProfileUpdate(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    bio: str | None = None
    education: str | None = None
    achievements: str | None = None
    instagram_url: str | None = None
    linkedin_url: str | None = None
    profile_image_url: str | None = None  # ako koristiš ovo

    model_config = ConfigDict(from_attributes=True)

class TrainerProfileOut(TrainerProfileUpdate):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  

class NotificationBase(BaseModel):
    message: str

class NotificationCreate(NotificationBase):
    pass  

class NotificationOut(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True