import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from session_manager import UserSession, add_user
from models import LoginInfo
from db_session import get_session

load_dotenv()

# create an instance of the Flask app and initialize the database session
app = Flask(__name__)
app.secret_key = os.getenv('APP_KEY')
db_session = get_session()


# route for the login page
# verifies the username and password, then redirects to the home page or prompts to try again
@app.route('/', methods=["GET", "POST"])
def start():
    return render_template('start_page.html')


# route for login page, checks login and password and redirects to home page or asks to try again
@app.route('/signin', methods=["GET", "POST"])
def sign_in():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        # DB query to check login and password hash
        user = db_session.query(LoginInfo).filter(LoginInfo.username == username).first()
        if user and user.user_id and check_password_hash(user.password, password):
            # save the user id in the session if authentication is successful
            session['user_id'] = user.user_id
            return redirect(url_for('home'))
        else:
            return render_template('sign_in_page.html', message='Incorrect username or password, try again')
    return render_template('sign_in_page.html')


# route for the registration page
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        filled_form = request.form.to_dict()
        # get the id of the created user if the adding function was successful
        user_id = add_user(filled_form)
        if user_id:
            session['user_id'] = user_id
            return redirect(url_for('home'))
        else:
            return render_template('register_page.html', message='Something went wrong, check the entered data')
    return render_template('register_page.html')


# route for the home page
@app.route('/home', methods=["GET", "POST"])
def home():
    # retrieve the user id from the session
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('sign_in'))
    # create a UserSession instance to manage session data
    new_session = UserSession(user_id, db_session)
    # calcuate current statistics
    statistics = new_session.calculate_statistics()
    if request.method == 'POST':
        filled_from = request.form.to_dict()
        successful_insert = new_session.process_form(filled_from)

        # alert if the date was invalid or duplicated
        if not successful_insert:
            return render_template('home.html', result=statistics,
                                   message='You cannot add data for an already filled or future date')

        # recalculate statistics after inserting new data
        statistics = new_session.calculate_statistics()
        return render_template('home.html', result=statistics)
    return render_template('home.html', result=statistics)
