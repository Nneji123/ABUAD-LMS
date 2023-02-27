"""
This module contains a Flask blueprint for handling user authentication and login. 
It provides a login page where users can enter their username, password, and role (student, lecturer, or admin). Upon successful login, the user is redirected to the appropriate page based on their role. 
If the user is not authorized or enters incorrect login credentials, an error message is displayed.

"""


from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user

from models import Admins, Lecturers, Students

login = Blueprint(
    "login", __name__, template_folder="./templates", static_folder="./templates"
)

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
            user = Students.query.filter_by(username=username).first()
        elif role == "lecturer":
            user = Lecturers.query.filter_by(username=username).first()
        elif role == "admin":
            user = Admins.query.filter_by(username=username).first()

        if not user:
            flash("This user is not authorized to view this page!")
            return render_template("/pages/login.html")

        if not user.check_password(password):
            flash("Incorrect password!")
            return render_template("/pages/login.html")

        login_user(user)

        if role == "student":
            return redirect(url_for("student.show"))
        elif role == "lecturer":
            return redirect(url_for("lecturer.show"))
        elif role == "admin":
            return redirect(url_for("admin.index"))

    return render_template("/pages/login.html")
