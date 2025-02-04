from datetime import date
from models import *
from db_session import get_session
from sqlalchemy import and_
from analytics import *
from werkzeug.security import generate_password_hash

session = get_session()


# class to manage the session for a specific user
class UserSession:
    def __init__(self, user_id, session):
        self.user_id = user_id
        self.session = session

    # add a new entry to a given table model
    def add_table_entry(self, table_model, **kwargs):
        self.session.add(table_model(user_id=self.user_id, **kwargs))

    # distribute form data into corresponding tables
    def distribute_form_data(self, selected_date, sleep_duration, sleep_interruptions, number_of_steps,
                             workout_duration, workout_type, consumed_kcal):
        # check if data for this date already exists or if the date is in the future
        existence_check = self.session.query(SleepInfo.user_id).filter(
            and_(SleepInfo.user_id == self.user_id, SleepInfo.date == selected_date)).first()
        if existence_check or selected_date > date.today().isoformat():
            return False

        self.add_table_entry(SleepInfo,
                             date=selected_date,
                             duration=sleep_duration,
                             interruptions=sleep_interruptions
                             )

        self.add_table_entry(StepsInfo,
                             date=selected_date,
                             number_of_steps=number_of_steps
                             )

        self.add_table_entry(WorkoutInfo,
                             date=selected_date,
                             duration=workout_duration,
                             workout_type=workout_type
                             )

        self.add_table_entry(NutritionInfo,
                             date=selected_date,
                             consumed_calories=consumed_kcal)

        steps_burnt_kcal = 0.04 * int(number_of_steps)
        workout_calories_per_min = session.query(WorkoutTypesInfo.kcal_per_minute).filter_by(name=workout_type).scalar()
        workout_burnt_kcal = workout_calories_per_min * float(workout_duration)

        self.add_table_entry(CalculatedInfo,
                             date=selected_date,
                             burnt_calories=steps_burnt_kcal + workout_burnt_kcal)
        session.commit()
        return True

    # passes data from the database to the statistics functions and returns calculated statistics
    def calculate_statistics(self):
        # make DB queries and convert the received data into a list
        sleep_duration_list = self.session.query(SleepInfo.duration).filter(SleepInfo.user_id == self.user_id).all()
        if len(sleep_duration_list) == 0:  # check if at least one entry for this user exists
            return {'Info': 'Please fill out the form at least once to see the statistics.'}
        sleep_durations = [row[0] for row in sleep_duration_list]
        sleep_interruptions_list = self.session.query(SleepInfo.interruptions).filter(
            SleepInfo.user_id == self.user_id).all()
        sleep_interruptions = [row[0] for row in sleep_interruptions_list]
        consumed_kcal_list = self.session.query(NutritionInfo.consumed_calories).filter(
            NutritionInfo.user_id == self.user_id).all()
        consumed_kcal = [row[0] for row in consumed_kcal_list]
        burnt_kcal_list = self.session.query(CalculatedInfo.burnt_calories).filter(
            CalculatedInfo.user_id == self.user_id).all()
        burnt_kcal = [row[0] for row in burnt_kcal_list]

        # obtain data about the user
        user = self.session.query(User).filter(User.id == self.user_id).scalar()
        weight = user.weight
        height = user.height
        gender = user.gender
        age = user.age

        # get results of analytical functions and combine them into one dictionary
        sleep_result = sleep_analysis(sleep_durations, sleep_interruptions)
        activity_result = activity_analysis(burnt_kcal, consumed_kcal, gender, weight, height, age)
        result = {**sleep_result, **activity_result}
        return result

    # change weight if the user entered a new one
    def change_weight(self, new_weight):
        self.session.query(User).filter(User.id == self.user_id).update({"weight": new_weight})
        session.commit()

    # extract data from the form and pass it to the distribution function
    def process_form(self, form):
        # check if the new weight field was filled
        new_weight = form.get("new_weight")
        if new_weight:
            self.change_weight(float(new_weight))

        successful_insert = self.distribute_form_data(form["selected_date"], form["sleep_duration"],
                                                      form["interruptions"], form["number_of_steps"],
                                                      form["workout_duration"], form["workout_type"],
                                                      form["consumed_calories"])
        # returns True if the insertion was successful or False otherwise
        return successful_insert


# add new user based on the data from the registration form
def add_user(form):
    new_user = User(name=form["username"], age=form["age"], height=form["height"], weight=form["weight"],
                    gender=form["gender"])
    session.add(new_user)

    session.flush()# lets to get a new id without commit

    new_user_login = LoginInfo(user_id=new_user.id, username=form["username"],
                               password=generate_password_hash(form["password"]))
    session.add(new_user_login)
    session.commit()
    return new_user.id
