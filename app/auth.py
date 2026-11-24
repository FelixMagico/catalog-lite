from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from .extensions import db
from .models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if len(username) < 3 or len(password) < 6:
            flash("Username di almeno 3 caratteri e password di almeno 6.")
        elif User.query.filter_by(username=username).first():
            flash("Username già in uso.")
        else:
            user = User(username=username)  # il ruolo è "user" di default
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Registrazione completata, ora puoi accedere.")
            return redirect(url_for("auth.login"))
    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username", "")).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user)
            return redirect(url_for("main.index"))
        flash("Username o password errati.")
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
