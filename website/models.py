from enum import unique
from . import db
from flask_login import UserMixin

class UserMods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mod_name = db.Column(db.String(1024))
    mod_id = db.Column(db.String(1024))
    

class UserGames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(1024))
    game_id = db.Column(db.String(1024))
    game_path = db.Column(db.String(65536))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(4096))