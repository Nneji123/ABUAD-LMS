"""
This module contains a Flask blueprint for handling user authentication and login. 

It provides a login page where users can enter their username, password, and role (student, lecturer, or admin). Upon successful login, the user is redirected to the appropriate page based on their role. 

If the user is not authorized or enters incorrect login credentials, an danger message is displayed.

"""

import sys
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user

sys.path.append("..")

from configurations.models import Admins, Lecturers, Students, db
from utils import validate_matric_number

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
            user = Lecturers.query.filter_by(username=username).first()
        elif role == "admin":
            user = Admins.query.filter_by(username=username).first()

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
        elif role == "admin":
            return redirect(url_for("admin.index"))

    return render_template("/pages/login.html")
