from flask import Flask
import subprocess
from os import path, name
import hashlib
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from time import time
import secrets

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():

    # This gets the device HWID
    if 'nt' in name:
        hwidr = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
    else:
        hwidr = subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())

    hwid = hwidr.encode(encoding = 'UTF-8')
    cte = str(time()).encode(encoding = 'UTF-8')
    sc = secrets.token_hex(16).encode(encoding = 'UTF-8')

    # This Generates a safe and Device Unique Key to protect the cookies
    hscr = hashlib.sha3_512(hwid + cte + sc)
    hsc = hscr.hexdigest()

    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = hsc
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, UserGames, UserMods

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)