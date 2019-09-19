# auth.py
import json
import uuid
import redis
from passlib.hash import pbkdf2_sha256
from flask import Blueprint, request, render_template, make_response, redirect, url_for

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html', msg='Please Login')


@auth.route('/login', methods=['POST'])
def login_post():
    # Get Username and password from Form
    user_name = request.form['username']
    password = request.form['password']
    print(f'Received username {user_name}')
    print(f'Received password {password}')

    # Connect to redis and get password for redis
    r = redis.Redis(host='localhost', port=6379, db=1)
    user_data = r.get(user_name)

    if user_data is None:
        # If user session not in Redis
        return render_template('login.html', msg=f'Tried to login with user: {user_name} but no user was found.')
    elif user_data is not None:
        # If user found in redis
        user = json.loads(bytes.decode(user_data))
        if pbkdf2_sha256.verify(password, user['password']):
            # if submitted password match Redis password

            # Load Homepage
            response = make_response(
                redirect(url_for('main.index')))

            # render_template('home.html', msg=f'You are now logged in: {user_name}', user=user_name,
            #                 logged_in=True), 200)

            # Create new uuid to track session
            user_session = str(uuid.uuid4())
            print(f'Set a new cookie: {user_session}')
            # Create Cookie which expires in 1 minute (max_age in seconds)
            response.set_cookie(key='user_session', value=user_session, max_age=60)

            # Store the uuid with username in redis
            r.set(str(user_session), user_name)

            return response
        else:
            # Password Incorrect
            return render_template('login.html', msg=f'Password Incorrect for user: {user_name}')


@auth.route('/signup')
def signup():
    return 'Signup'


@auth.route('/logout')
def logout():
    return 'Logout'
