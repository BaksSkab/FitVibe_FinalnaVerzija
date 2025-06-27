from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

# === LOGIN ===
class LoginData(BaseModel):
    email: str
    password: str

# === USER ===
class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    gender: Optional[str] = None
    goal: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

# === MOTIVATIONAL MESSAGE ===
class MotivationalMessageBase(BaseModel):
    content: str
    display_date: date

class MotivationalMessageCreate(MotivationalMessageBase):
    pass

class MotivationalMessage(MotivationalMessageBase):
    id: int
    class Config:
        orm_mode = True

# === PROGRESS ===
class ProgressBase(BaseModel):
    user_id: int
    workout_id: int
    actual_result: Optional[str] = None
    created_at: Optional[datetime] = None

class ProgressCreate(ProgressBase):
    pass

class Progress(ProgressBase):
    id: int
    class Config:
        orm_mode = True

# === TRAINER INFO (za prikaz trenera unutar plana) ===
class TrainerInfo(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

# === TRAINER PLAN ===
class TrainerPlanBase(BaseModel):
    trainer_id: int
    plan_name: str
    description: Optional[str] = None
    level: Optional[str] = None
    goal: Optional[str] = None

class TrainerPlan(TrainerPlanBase):
    id: int
    workouts: List = []  # ako trebaš za frontend, možeš kasnije detaljnije tipizirati
    trainer: Optional[TrainerInfo] = None  # uključujemo podatke o treneru

    class Config:
        orm_mode = True

# === USER-TRAINER PLAN (user subscription to plan) ===
class UserTrainerPlanOut(BaseModel):
    id: int
    user_id: int
    trainer_plan_id: int
    subscribed_at: datetime
    trainer_plan: TrainerPlan

    class Config:
        orm_mode = True

# === TRAINER ===
class TrainerBase(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: str

class TrainerCreate(TrainerBase):
    password: str

class Trainer(TrainerBase):
    id: int

    class Config:
        orm_mode = True
