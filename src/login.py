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
        roling = request.form["role"]
        
        if roling == "student":
            studs = Students.query.filter_by(username=username).first()
            if studs:
                roles = studs.role
            else: 
                message = flash("This user is not authorized to view this page!")
                return render_template("/main_pages/login.html", message=message)
        if roling == "lecturer":
            lects = Lecturers.query.filter_by(username=username).first()
            if lects:
                roles = lects.role
                
            else: 
                message = flash("This user is not authorized to view this page!")
                return render_template("/main_pages/login.html", message=message)
        if roling == "admin":
            admins = Admins.query.filter_by(username=username).first()
            if admins:
                roles = admins.role
            else: 
                message = flash("This user is not authorized to view this page!")
                return render_template("/main_pages/login.html", message=message)


        if (roles == "student" and roling == "student") and studs:
            check_password_hash(studs.password, password)
            login_user(studs)
            return redirect(url_for("student.show"))
        elif (roles == "lecturer" and roling == "lecturer") and lects:
            check_password_hash(lects.password, password)
            login_user(lects)
            return redirect(url_for("lecturer.show"))
        elif (roles == "admin" and roling == "admin") and admins:
            check_password_hash(admins.password, password)
            login_user(admins)
            return redirect(url_for("admin.show_users"))

        else:
            return redirect(
                url_for("login.show") + "?error=incorrect-password-unauthorized"
            )
    #     else:
    #         return redirect(url_for("login.show") + "?error=user-not-found")
    else:
        return render_template("/main_pages/login.html")
