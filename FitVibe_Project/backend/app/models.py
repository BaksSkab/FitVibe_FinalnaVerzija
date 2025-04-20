from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    gender = Column(String)
    password = Column(String, nullable=False)
    goal = Column(String)

class Admin(Base):
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Trainer(Base):
    __tablename__ = 'trainers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

class Workout(Base):
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    repetitions = Column(Integer)
    trainer_id = Column(Integer, ForeignKey('trainers.id'))
    
    trainer = relationship('Trainer', back_populates='workouts')

class Challenge(Base):
    __tablename__ = 'challenges'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    duration_days = Column(Integer, nullable=False)

class UserChallenge(Base):
    __tablename__ = 'user_challenges'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), nullable=False)
    progress = Column(Integer, default=0)
    
    user = relationship('User', back_populates='user_challenges')
    challenge = relationship('Challenge', back_populates='user_challenges')

class MotivationalMessage(Base):
    __tablename__ = 'motivational_messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    display_date = Column(Date, nullable=False)

class Progress(Base):
    __tablename__ = 'progress'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    workout_id = Column(Integer, ForeignKey('workouts.id'), nullable=False)
    actual_result = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship('User', back_populates='progress')
    workout = relationship('Workout', back_populates='progress')

class TrainerPlan(Base):
    __tablename__ = 'trainer_plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    trainer_id = Column(Integer, ForeignKey('trainers.id'), nullable=False)
    plan_name = Column(String, nullable=False)
    description = Column(Text)
    
    trainer = relationship('Trainer', back_populates='trainer_plans')

# Relationships in Trainer class to link with other tables
Trainer.workouts = relationship('Workout', back_populates='trainer')
Trainer.trainer_plans = relationship('TrainerPlan', back_populates='trainer')
User.user_challenges = relationship('UserChallenge', back_populates='user')
Challenge.user_challenges = relationship('UserChallenge', back_populates='challenge')
User.progress = relationship('Progress', back_populates='user')
Workout.progress = relationship('Progress', back_populates='workout')
