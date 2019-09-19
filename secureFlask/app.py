# __init__.py
import redis
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'auth.login_form'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    r = redis.Redis(host='localhost', port=6379, db=1)
    user = r.get(user_id)
    user_name = bytes.decode(user['username'])
    print(f'Got user {user_name}')
    return

# blueprint for non-auth parts of app
from main_pages import main as main_blueprint

app.register_blueprint(main_blueprint)

from auth_pages import auth as main_blueprint

app.register_blueprint(main_blueprint)





app.run()
