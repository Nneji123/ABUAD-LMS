from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from models import Students, Lecturers, Admins, db

login = Blueprint(
    "login", __name__, template_folder="./frontend", static_folder="./frontend"
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
            return render_template("/main_pages/login.html")

        if not check_password_hash(user.password, password):
            flash("Incorrect password!")
            return render_template("/main_pages/login.html")

        login_user(user)

        if role == "student":
            return redirect(url_for("student.show"))
        elif role == "lecturer":
            return redirect(url_for("lecturer.show"))
        elif role == "admin":
            return redirect(url_for("admin.show_users"))

    return render_template("/main_pages/login.html")
