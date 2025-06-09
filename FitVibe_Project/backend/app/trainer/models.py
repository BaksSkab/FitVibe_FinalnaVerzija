from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)

    bio = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    achievements = Column(Text, nullable=True)
    instagram_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)

    notifications = relationship("TrainerNotification", back_populates="trainer", cascade="all, delete-orphan")
     
class TrainerPlan(Base):
    __tablename__ = "trainer_plans"

    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    plan_name = Column(String, nullable=False)
    description = Column(String)
    level = Column(String)
    goal = Column(String)
    category_id = Column(Integer)
    
class TrainerPlanWorkout(Base):
    __tablename__ = "trainer_plan_workouts"

    id = Column(Integer, primary_key=True, index=True)
    trainer_plan_id = Column(Integer, ForeignKey("trainer_plans.id"))
    workout_id = Column(Integer, ForeignKey("workouts.id"))


class UserTrainerPlan(Base):
    __tablename__ = "user_trainer_plan"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trainer_plan_id = Column(Integer, ForeignKey("trainer_plans.id"))
    joined_at = Column(DateTime)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    gender = Column(String)
    password = Column(String)
    goal = Column(String)
    phone = Column(String)
    
class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    repetitions = Column(Integer)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    image_filename = Column(String, nullable=True)


class TrainerNotification(Base):
    __tablename__ = "trainer_notifications"

    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    trainer = relationship("Trainer", back_populates="notifications") 
