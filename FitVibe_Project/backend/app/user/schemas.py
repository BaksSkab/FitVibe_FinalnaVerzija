from pydantic import BaseModel
from typing import Optional

class TrainerInfo(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class TrainerPlanOut(BaseModel):
    id: int
    plan_name: str
    description: Optional[str]
    level: Optional[str]
    goal: Optional[str]
    trainer: TrainerInfo

    class Config:
        orm_mode = True

class UserTrainerPlanOut(BaseModel):
    id: int
    trainer_plan: TrainerPlanOut

    class Config:
        orm_mode = True
