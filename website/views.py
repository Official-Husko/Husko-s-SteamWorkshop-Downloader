from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from . import db
from .models import User, UserGames
import requests as rq

views = Blueprint("views", __name__)

@views.route("/")
def blank():
    return render_template("base.html", user=current_user)

@views.route("/home")
@login_required
def home():
    return render_template("base.html", user=current_user)

@views.route("/games", methods=["GET", "POST"])
@login_required
def games():
    if request.method == "POST":
        game_id = request.form.get("game_id")
        game_name = request.form.get("game_name")
        game_path = request.form.get("game_path")

        game = UserGames.query.filter_by(game_id=game_id, user_id=current_user.id).first()
        if game:
            flash("Game was already added!", category="error")
        elif game_id == "" or game_name == "" or game_path == "":
            flash("Please fill out all fields.", category="error")
        else:
            new_game = UserGames(game_id=game_id, game_name=game_name, game_path=game_path, user_id=current_user.id)
            db.session.add(new_game)
            db.session.commit()

            # Retrieve image directly
            request_image = rq.get(f"https://cdn.akamai.steamstatic.com/steam/apps/{game_id}/header.jpg")
            if request_image.status_code == 200:
                open(f"website/static/headers/{game_id}.jpg", 'wb').write(request_image.content)
            else:
                pass


            flash("Game Added Successfully!", category="success")
            return redirect(url_for("views.games"))

    return render_template("games.html", user=current_user)

@views.route("/downloader")
@login_required
def downloader():
    return render_template("downloader.html", user=current_user)

@views.route("/settings")
@login_required
def settings():
    return render_template("settings.html", user=current_user)