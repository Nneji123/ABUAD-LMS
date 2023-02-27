"""
This file defines a Flask application for the ABUAD e-learning platform. It imports and uses several libraries such as os, css_inline, sqlalchemy, dotenv, Flask, Flask-Admin, Flask-Login, Flask-Mail, and itsdangerous.

The application is configured using the "configs" dictionary imported from the config.py module. The server mode is set using the environment variable "SERVER_MODE", which must be one of the keys in the "configs" dictionary; otherwise, a ValueError will be raised.

The application consists of the following Blueprints:
- index: the landing page for the application.
- login: allows users to log in.
- logout: allows users to log out.
- student: provides access to student-specific pages, such as the dashboard and course materials.
- lecturer: provides access to lecturer-specific pages, such as the dashboard and course management.

The application also defines an Admin instance for managing the database models, with views for the Students, Lecturers, and Admins models.

The application uses Flask-Login to handle user authentication and Flask-Mail for password reset features.

This file also defines several utility functions such as send_mail and error handlers for HTTP errors.
"""


import os

import css_inline
import sqlalchemy
from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadTimeSignature
from werkzeug.security import generate_password_hash

from config import configs
from index import CustomIndexView, index
from lecturer import lecturer
from login import login
from logout import logout
from models import (
    Admins,
    AdminsView,
    Lecturers,
    LecturersView,
    Students,
    StudentsView,
    db,
)
from student import student

load_dotenv()

app = Flask(__name__, static_folder="./templates/static")


SERVER_MODE = os.getenv("SERVER_MODE")
if SERVER_MODE in configs:
    app.config.update(configs[SERVER_MODE])
else:
    raise ValueError(f"Unknown server mode: {SERVER_MODE}")

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
app.app_context().push()

email = Mail(app)

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(lecturer)
app.register_blueprint(student)
serializer = URLSafeTimedSerializer("secret")


admin = Admin(
    app, name="ABUAD", template_mode="bootstrap4", index_view=CustomIndexView()
)
admin.add_view(StudentsView(Students, db.session))
admin.add_view(LecturersView(Lecturers, db.session))
admin.add_view(AdminsView(Admins, db.session))


@login_manager.user_loader
def load_user(user_id):
    students = Students.query.filter_by(id=user_id).first()
    lecturers = Lecturers.query.filter_by(id=user_id).first()
    admins = Admins.query.filter_by(id=user_id).first()
    try:
        if students:
            return students
        elif lecturers:
            return lecturers
        elif admins:
            return admins
        else:
            return None
    except (sqlalchemy.exc.OperationalError) as e:
        return render_template("error.html", e="Database not found")


@app.route("/500")
def error500():
    abort(500)


@app.errorhandler(404)
def not_found(e):
    return (
        render_template(
            "/pages/error.html", e="The page you are looking for does not exist!"
        ),
        404,
    )


@app.errorhandler(400)
def bad_requests(e):
    return (
        render_template(
            "/pages/error.html",
            e="The browser (or proxy) sent a request that this server could not understand.",
        ),
        400,
    )


@app.errorhandler(500)
def internal_error(error):
    return (
        render_template(
            "/pages/error.html", e="There has been an internal server error!"
        ),
        500,
    )


def send_mail(to, template, subject, link, username, **kwargs):
    """
    The send_mail_flask function is used to send an email from the Flask app.
    It takes in a recipient, template, subject and link as its parameters. It also takes in optional arguments that can be passed into the function.

    :param to: Specify the recipient of the email
    :param template: Specify the html template that will be used to send the email
    :param subject: Set the subject of the email
    :param link: Create a unique link for each user
    :param username: Populate the username field in the email template
    :param **kwargs: Pass in any additional variables that are needed to be rendered in the email template
    :return: The html of the email that is being sent
    """
    if os.getenv("SERVER_MODE") == "DEV":
        sender = os.getenv("DEV_SENDER_EMAIL")
    elif os.getenv("SERVER_MODE") == "PROD":
        sender = os.getenv("PROD_SENDER_EMAIL")
    msg = Message(subject=subject, sender=sender, recipients=[to])
    html = render_template(template, username=username, link=link, **kwargs)
    inlined = css_inline.inline(html)
    msg.html = inlined
    email.send(msg)


@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    if request.method == "POST":
        mail = request.form["mail"]

        # check if user exists in students table
        student = Students.query.filter_by(email=mail).first()
        if student:
            username = student.username
        else:
            # check if user exists in lecturers table
            lecturer = Lecturers.query.filter_by(email=mail).first()
            if lecturer:
                username = lecturer.username
            else:
                flash("User does not exist!")
                return render_template("/reset_password/index.html")

        hashCode = serializer.dumps(mail, salt="reset-password")
        if student:
            student.hashCode = hashCode
        else:
            lecturer.hashCode = hashCode
        server = os.getenv("SERVER_NAME")
        link = f"{server}/{hashCode}"
        db.session.commit()
        send_mail(
            to=mail,
            template="/reset_password/email.html",
            subject="Reset Password",
            username=username,
            link=link,
        )

        flash("A password reset link has been sent to your email! Please Check")
        return render_template("/reset_password/index.html")
    else:
        return render_template("/reset_password/index.html")


@app.route("/<string:hashCode>", methods=["GET", "POST"])
def hashcode(hashCode):
    try:
        mail = serializer.loads(hashCode, salt="reset-password", max_age=600)
    except BadTimeSignature:
        flash("The password reset link has expired. Please request a new one.")
        return redirect(url_for("index.show"))

    # check if user exists in students table
    student = Students.query.filter_by(email=mail).first()
    if student:
        check = student
    else:
        # check if user exists in lecturers table
        lecturer = Lecturers.query.filter_by(email=mail).first()
        if lecturer:
            check = lecturer
        else:
            flash("User does not exist!")
            return render_template("/reset_password/base.html")

    if request.method == "POST":
        passw = request.form["passw"]
        cpassw = request.form["cpassw"]
        if passw == cpassw:
            check.password = generate_password_hash(passw, method="sha256")
            check.hashCode = None
            db.session.commit()
            flash("Your Password has been reset successfully!")
            return redirect(url_for("index.show"))
        else:
            flash("Password fields do not match.")
            return render_template("/reset_password/reset.html", hashCode=hashCode)
    else:
        return render_template("/reset_password/reset.html", hashCode=hashCode)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", port=3000, debug=configs[SERVER_MODE]["DEBUG"], threaded=True
    )
