import json
import uuid
import redis
from flask_login import login_required, current_user
from passlib.hash import pbkdf2_sha256
from flask import Blueprint, request, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    # Get cookie from request
    user_session = request.cookies.get('user_session')
    r = redis.Redis(host='localhost', port=6379, db=1)

    if user_session is not None:  # We have received a cookie
        try:
            user = bytes.decode(r.get(user_session))
            print(f'Cookie Received from user: {user}')
            return render_template("home.html", msg=f'Hello {user}', user=user, logged_in=True)
        except TypeError:
            print('Cookie received is invalid')
            return render_template("home.html", msg='Login session could not be validated, please log in again',
                                   user='Guest', logged_in=True)

    elif user_session is None:
        print("No Cookie Received")
        return render_template("home.html", msg='Hello Guest', user='Guest', logged_in=False)


#
# @main.route('/profile')
# def profile():
#     return 'Profile'

# Simple Hello world
@main.route('/hello')
@login_required
def hello_world():
    return 'Hello, World!'


@main.route('/secure', methods=['GET'])
@login_required
def secure_page():
    # Get cookie from request
    # user_session = request.cookies.get('user_session')

    return render_template("secure.html", msg=f'You are logged in as {current_user.name}', user=current_user.name,
                           logged_in=True)
