from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class LoginData(BaseModel):
    email: str
    password: str

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

class AdminBase(BaseModel):
    email: str
    full_name: str  # dodano

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int

    class Config:
        orm_mode = True


class TrainerBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str

class TrainerCreate(TrainerBase):
    password: str

class Trainer(TrainerBase):
    id: int

    class Config:
        orm_mode = True


class WorkoutBase(BaseModel):
    title: str
    description: str
    repetitions: Optional[int] = None

class WorkoutCreate(WorkoutBase):
    trainer_id: int

class Workout(WorkoutBase):
    id: int

    class Config:
        orm_mode = True

class ChallengeBase(BaseModel):
    name: str
    description: str
    duration_days: int

class ChallengeCreate(ChallengeBase):
    pass

class Challenge(ChallengeBase):
    id: int

    class Config:
        orm_mode = True

class UserChallengeBase(BaseModel):
    user_id: int
    challenge_id: int
    progress: Optional[int] = 0

class UserChallengeCreate(UserChallengeBase):
    pass

class UserChallenge(UserChallengeBase):
    id: int

    class Config:
        orm_mode = True

class MotivationalMessageBase(BaseModel):
    content: str
    display_date: date

class MotivationalMessageCreate(MotivationalMessageBase):
    pass

class MotivationalMessage(MotivationalMessageBase):
    id: int

    class Config:
        orm_mode = True

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

class TrainerPlanBase(BaseModel):
    trainer_id: int
    plan_name: str
    description: Optional[str] = None

class TrainerPlanCreate(TrainerPlanBase):
    pass

class TrainerPlan(TrainerPlanBase):
    id: int

    class Config:
        orm_mode = True

class PasswordChangeRequest(BaseModel):
    email: str
    old_password: str
    new_password: str
