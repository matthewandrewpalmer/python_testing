import json
import uuid
import redis
from flask import Flask, render_template, request, escape, make_response
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)


REDIS_HOST = 'redis'


# Simple Hello world
@app.route('/hello')
def hello_world():
    return 'Hello, World!'


# Gets name argument from url like ?name=Bob
@app.route('/world')
def get_name():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


# Cookie Example: Connecting to redis
@app.route("/user")
def get_user_session():
    user_id = request.cookies.get('user_id')
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    total = 0

    if user_id is not None:  # We have received a cookie
        try:
            total = int(bytes.decode(r.get(user_id))) + 1
        except TypeError:
            print('Cookie received is invalid')

        print(f'Cookie Received: {total}')
        r.set(user_id, str(total))

    response = make_response(str(total))
    if user_id is None:
        print("No Cookie Received")
        user_id = str(uuid.uuid4())
        print(f'set a new cookie: {user_id}')
        response.set_cookie('user_id', user_id)
        r.set(user_id, str(total))

    return response


# =========================================   Login and Authentication Website ==================================

@app.route("/")
def home():
    # Get cookie from request
    user_session = request.cookies.get('user_session')
    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)

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


@app.route('/users/<user_id>')
def get_user_id(user_id):
    user = get_user(user_id)
    if user is None:
        return f'User {user_id} not found'
    return user


def get_user(user_id):
    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
    return r.get(user_id)


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html', msg='Please Login')


@app.route('/login', methods=['POST'])
def login():
    # Get Username and password from Form
    user_name = request.form['username']
    password = request.form['password']
    print(f'Received username {user_name}')
    print(f'Received password {password}')

    # Connect to redis and get password for redis
    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
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
                render_template('home.html', msg=f'You are now logged in: {user_name}', user=user_name,
                                logged_in=True), 200)

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


@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html', msg='Please Signup')


@app.route('/register', methods=['POST'])
def register():
    # Get Username and password from Form
    user_name = request.form['username']
    hashed_password = pbkdf2_sha256.hash(request.form['password'])
    print(f'Received username {user_name}')

    # Connect to redis and store username and password
    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
    db_user = r.get(user_name)
    if db_user is None:
        print('New User, creating account')

        r.set(str(user_name), json.dumps({'username': user_name, 'password': hashed_password}))

        # redirect to /login page
        return render_template('login.html', msg=f'Account created with username: {user_name}, please login')
    else:
        print(f'User: {user_name} already exist')
        return render_template('register.html', msg=f'The Username: {user_name} is already in use')


@app.route('/logout', methods=['GET'])
def logout():
    user_session = request.cookies.get('user_session')
    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)

    if user_session != '':
        r.delete(user_session)

    message = 'You have Now been logged out'
    user = 'guest'
    response = make_response(render_template("home.html", msg=message, user=user, logged_in=False))

    response.set_cookie(key='user_session', value='', max_age=None)
    return response


@app.route('/secure', methods=['GET'])
def secure_page():
    # Get cookie from request
    user_session = request.cookies.get('user_session')

    if user_session is None or user_session == '':
        print("No Cookie Received")
        message = 'You need to be logged in to see this Secure Page'
        return render_template("login.html", msg=message, user='Guest', logged_in=False)
    elif user_session is not None:  # We have received a cookie
        return render_template("secure.html", msg='You are logged in', user='User', logged_in=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # app.run()
