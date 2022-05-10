from flask import Flask
import subprocess
import os
import hashlib
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():

    # This gets the device HWID
    if 'nt' in os.name:
        hwidr = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
    else:
        hwidr = subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())

    id = "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"
    softid = id.encode(encoding = 'UTF-8')
    hwid = hwidr.encode(encoding = 'UTF-8')

    # This Generates a safe and Device Unique Key to protect the cookies
    hscr = hashlib.sha3_512(softid + hwid)
    hsc = hscr.hexdigest()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = hsc
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from.views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app