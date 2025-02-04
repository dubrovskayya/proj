from sqlalchemy import Column, PrimaryKeyConstraint, Integer, String, Float, Date, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# define the base class for declarative models
Base = declarative_base()


# define table models
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    gender = Column(String(1), nullable=False)

    __table_args__ = (CheckConstraint(gender.in_(["M", "F"]), name="check_gender"),)


class SleepInfo(Base):
    __tablename__ = 'sleep_info'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    duration = Column(Float, nullable=False)
    interruptions = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'date'),
    )


class StepsInfo(Base):
    __tablename__ = 'steps_info'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    number_of_steps = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'date'),
    )


class WorkoutTypesInfo(Base):
    __tablename__ = 'workout_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    kcal_per_minute = Column(Float, nullable=False)


class WorkoutInfo(Base):
    __tablename__ = 'workout_info'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    duration = Column(Float, nullable=False)
    workout_type = Column(String(20), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'date'),
    )


class NutritionInfo(Base):
    __tablename__ = 'nutrition_info'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    consumed_calories = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'date'),
    )


class CalculatedInfo(Base):
    __tablename__ = 'calculated_info'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    burnt_calories = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'date'),
    )


class LoginInfo(Base):
    __tablename__ = 'login_info'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'username'),
    )
