from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

# === USERS ===
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    gender = Column(String)
    goal = Column(String)

    # challenges polje uklonjeno
    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    subscribed_plans = relationship("UserTrainerPlan", back_populates="user", cascade="all, delete-orphan")

# === TRAINERS ===
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

    plans = relationship("TrainerPlan", back_populates="trainer", cascade="all, delete-orphan")
    notifications = relationship("TrainerNotification", back_populates="trainer", cascade="all, delete-orphan")

# === TRAINER PLANS ===
class TrainerPlan(Base):
    __tablename__ = "trainer_plans"
    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    plan_name = Column(String, nullable=False)
    description = Column(String)
    level = Column(String)
    goal = Column(String)
    category_id = Column(Integer)

    trainer = relationship("Trainer", back_populates="plans")
    subscribers = relationship("UserTrainerPlan", back_populates="trainer_plan", cascade="all, delete-orphan")

    workouts = relationship(
        "Workout",
        secondary="trainer_plan_workouts",
        back_populates="trainer_plans"
    )

# === PLAN-VJEŽBE RELACIJA ===
class TrainerPlanWorkout(Base):
    __tablename__ = "trainer_plan_workouts"

    id = Column(Integer, primary_key=True, index=True)
    trainer_plan_id = Column(Integer, ForeignKey("trainer_plans.id"))
    workout_id = Column(Integer, ForeignKey("workouts.id"))

# === VJEŽBE ===
class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    repetitions = Column(Integer)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    image_filename = Column(String, nullable=True)

    trainer_plans = relationship(
        "TrainerPlan",
        secondary="trainer_plan_workouts",
        back_populates="workouts"
    )

# === USER <-> PLAN RELACIJA ===
class UserTrainerPlan(Base):
    __tablename__ = "user_trainer_plan"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trainer_plan_id = Column(Integer, ForeignKey("trainer_plans.id"))
    subscribed_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="subscribed_plans")
    trainer_plan = relationship("TrainerPlan", back_populates="subscribers")

# === MOTIVACIJA ===
class MotivationalMessage(Base):
    __tablename__ = "motivational_messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    display_date = Column(Date)

# === PROGRESS ===
class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    created_at = Column(DateTime, default=func.now())
    actual_result = Column(Text, nullable=True)

    user = relationship("User", back_populates="progress")

# === NOTIFIKACIJE ===
class TrainerNotification(Base):
    __tablename__ = "trainer_notifications"

    id = Column(Integer, primary_key=True, index=True)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    trainer = relationship("Trainer", back_populates="notifications")