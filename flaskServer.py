import uuid
import redis
from flask import Flask, render_template, request, escape, make_response

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route("/")
def get_home():
    return render_template("index.html", msg='')


@app.route('/world')
def get_name():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route("/user")
def get_user_session():
    user_id = request.cookies.get('user_id')
    r = redis.Redis(host='localhost', port=6379, db=0)
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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Get Username and password from Form
        user_name = request.form['username']
        password = request.form['password']
        print(f'Received username {user_name}')
        print(f'Received password {password}')

        # Connect to redis and get password for redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        db_password = r.get(user_name)

        if db_password is None:
            # user not in redis
            return render_template('login.html', msg=f'Tried to login with user: {user_name} but no user was found.')
        elif db_password is not None:
            # If user found in redis
            if password == bytes.decode(db_password):
                # if submitted password match redis password
                return render_template('login.html', msg=f'You are now logged in: {user_name}')
            else:
                # Password Incorrect
                return render_template('login.html', msg=f'Password Incorrect for user: {user_name}')
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Get Username and password from Form
        user_name = request.form['username']
        password = request.form['password']
        print(f'Received username {user_name}')

        # Connect to redis and store username and password
        r = redis.Redis(host='localhost', port=6379, db=0)
        db_user = r.get(user_name)
        if db_user is None:
            print('New User, creating account')
            r.set(str(user_name), str(password))

            # redirect to /login page
            return render_template('login.html', msg=f'Account created with username: {user_name}, please login')
        else:
            print('User already exist')
            return render_template('register.html', msg='Username already in use')
    elif request.method == 'GET':
        return render_template('register.html', msg='Please Signup')


app.run()
