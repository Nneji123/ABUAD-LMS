from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from models import Users, db

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

        user = Users.query.filter_by(username=username).first()
        print(user)
        roles = user.role

        if (roles == "student" and roling == "student") and user:
            check_password_hash(user.password, password)
            login_user(user)
            return redirect(url_for("student.show"))
        elif (roles == "lecturer" and roling == "lecturer") and user:
            check_password_hash(user.password, password)
            login_user(user)
            return redirect(url_for("lecturer.show"))
        elif (roles == "admin" and roling == "admin") and user.is_admin == True:
            check_password_hash(user.password, password)
            login_user(user)
            return redirect(url_for("admin.show"))

        else:
            return redirect(
                url_for("login.show") + "?error=incorrect-password-unauthorized"
            )
    #     else:
    #         return redirect(url_for("login.show") + "?error=user-not-found")
    else:
        return render_template("/main_pages/login.html")
