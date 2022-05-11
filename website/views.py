from flask import Blueprint, render_template
from flask_login import current_user, login_required

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home():
    return render_template("base.html", user=current_user)

@views.route("/games")
@login_required
def games():
    return render_template("games.html", user=current_user)

@views.route("/downloader")
@login_required
def downloader():
    return render_template("downloader.html", user=current_user)

@views.route("/settings")
@login_required
def settings():
    return render_template("settings.html", user=current_user)