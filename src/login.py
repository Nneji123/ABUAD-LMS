from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_user
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from models import Admins, Lecturers, Students, db

login = Blueprint(
    "login", __name__, template_folder="./frontend", static_folder="./frontend"
)

login_manager = LoginManager()
login_manager.init_app(login)

serializer = URLSafeTimedSerializer("secret_key")


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

        if not user.check_password(password):
            flash("Incorrect password!")
            return render_template("/main_pages/login.html")

        login_user(user)

        if role == "student":
            return redirect(url_for("student.show"))
        elif role == "lecturer":
            return redirect(url_for("lecturer.show"))
        elif role == "admin":
            return redirect(url_for("admin.index"))

    return render_template("/main_pages/login.html")


@login.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if request.method == "POST":
        email = request.form["email"]
        # search for student with email
        student = Students.query.filter_by(email=email).first()
        # search for admin with email
        admin = Admins.query.filter_by(email=email).first()
        # search for lecturer with email
        lecturer = Lecturers.query.filter_by(email=email).first()
        if student:
            model = "student"
            id = student.id
        elif admin:
            model = "admin"
            id = admin.id
        elif lecturer:
            model = "lecturer"
            id = lecturer.id
        else:
            flash("Email not found")
            return redirect(url_for("login"))
        token = serializer.dumps({"id": id, "model": model}, salt="reset_password")
        if model == "student":
            student.reset_token = token
        elif model == "admin":
            admin.reset_token = token
        elif model == "lecturer":
            lecturer.reset_token = token
        db.session.commit()
        # send email with link to password reset form including token in URL
        flash("Check your email for instructions to reset your password")
        return redirect(url_for("login"))
    render_template("password_pages/base.html")
    return render_template("password_pages/base.html")


@login.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="reset_password", max_age=3600)
    except SignatureExpired:
        flash("The password reset link has expired")
        return redirect(url_for("login"))
    except BadSignature:
        flash("Invalid password reset link")
        return redirect(url_for("login"))
    user = None
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Email not found")
        return redirect(url_for("login"))
    if request.method == "POST":
        password = request.form["password"]
        password_confirmation = request.form["password_confirmation"]
        if password == password_confirmation:
            user.set_password(password)
            user.reset_token = None
            db.session.commit()
            flash("Your password has been reset")
            return redirect(url_for("login"))
        else:
            flash("Passwords do not match")
    return render_template("password_pages/reset_password.html", token=token)
