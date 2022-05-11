from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category="success")
                session['username'] = request.form['username']
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password, try again.", category="soft-error")
        else:
            flash("User does not exist.", category="soft-error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password-confirm")

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username is taken, please choose a different one", category="soft-error")
        elif password != password_confirm:
            flash("Confirm Password does not match Password!", category="soft-error")
        elif len(password) <= 4:
            flash("Password must be at least 4 characters long!", category="soft-error")
        else:
            new_user = User(username=username, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(username=username).first()
            session['username'] = request.form['username']
            login_user(user, remember=True)
            flash("Account Created successfully", category="success")
            return redirect(url_for("views.home"))

    return render_template("register.html", user=current_user)