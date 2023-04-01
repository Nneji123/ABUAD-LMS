"""Login Route"""

import sys
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user

sys.path.append("..")

from configurations.models import Admins, Lecturers, Students, db
from utils import validate_abuad_email, validate_matric_number

login = Blueprint("login", __name__)

login_manager = LoginManager()
login_manager.init_app(login)


@login.route("/login", methods=["GET", "POST"])
def show():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        user = None
        if role == "student":
            if validate_matric_number(username):
                user = Students.query.filter_by(matric_number=username).first()
            else:
                flash("Invalid Matric Number!", "danger")
                return render_template("/pages/login.html")
        elif role == "lecturer":
            if validate_abuad_email(username):
                user = Lecturers.query.filter_by(email=username).first()
            else:
                flash("Invalid ABUAD Email!", "danger")
                return render_template("/pages/login.html")

        if not user:
            flash("This user is not authorized to view this page!", "danger")
            return render_template("/pages/login.html")

        if user.is_active == False:
            flash("Your account has been deactivated !", "danger")
            return render_template("/pages/login.html")

        if not user.check_password(password):
            flash("Incorrect password!", "danger")
            return render_template("/pages/login.html")

        login_user(user)
        user.last_logged_in_at = datetime.utcnow()
        db.session.commit()
        if role == "student":
            return redirect(url_for("student.show"))
        elif role == "lecturer":
            return redirect(url_for("lecturer.show"))

    return render_template("/pages/login.html")


@login.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    if request.method != "POST":
        return render_template("/pages/login_admin.html")
    username = request.form["username"]
    password = request.form["password"]

    user = Admins.query.filter_by(username=username).first()

    if not user:
        flash("This user is not authorized to view this page!", "danger")
        return render_template("/pages/login_admin.html")

    if user.is_active == False:
        flash("Your account has been deactivated!", "danger")
        return render_template("/pages/login_admin.html")

    if not user.check_password(password):
        flash("Incorrect password!", "danger")
        return render_template("/pages/login_admin.html")

    login_user(user)
    user.last_logged_in_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for("admin.index"))
