from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class UserMods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mod_name = db.Column(db.String(1024))
    mod_id = db.Column(db.String(1024))
    mod_added = db.Column(db.DateTime(timezone=True), default=func.now())
    mod_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class UserGames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(1024))
    game_id = db.Column(db.String(1024))
    game_path = db.Column(db.String(65536))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1024), unique=True)
    password = db.Column(db.String(4096))
    games = db.relationship("UserGames")
    mods = db.relationship("UserMods")