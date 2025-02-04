# the file must be executed once before the first launch of the app
from db_session import engine, get_session
from models import Base
from models import WorkoutTypesInfo

session = get_session()

# create all tables from "models" file
Base.metadata.create_all(engine)

# fill in the workout types table
workouts = [
    WorkoutTypesInfo(name='none', kcal_per_minute=0),
    WorkoutTypesInfo(name='cardio', kcal_per_minute=10),
    WorkoutTypesInfo(name='lifting', kcal_per_minute=8),
    WorkoutTypesInfo(name='yoga', kcal_per_minute=4),
    WorkoutTypesInfo(name='cycling', kcal_per_minute=10),
    WorkoutTypesInfo(name='swimming', kcal_per_minute=12)
]
session.add_all(workouts)
session.commit()
