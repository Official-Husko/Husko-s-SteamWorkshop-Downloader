from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_updates = db.Column(db.Boolean(True))
    proxies = db.Column(db.Boolean(True))
    random_agent = db.Column(db.Boolean(True))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class UserMods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mod_id = db.Column(db.String())
    mod_name = db.Column(db.String())
    mod_added = db.Column(db.DateTime(timezone=True), default=func.now())
    mod_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class UserGames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String())
    game_id = db.Column(db.String())
    game_path = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    games = db.relationship("UserGames")
    mods = db.relationship("UserMods")