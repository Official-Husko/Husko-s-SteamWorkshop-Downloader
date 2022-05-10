from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/register", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password-confirm")

        if password != password_confirm:
            flash("Confirm Password does not match Password!", category="soft-error")
        elif len(password) <= 4:
            flash("Password must be at least 4 characters long!", category="soft-error")
        else:
            flash("Account Created successfully", category="success")
            #add to db

    return render_template("register.html")