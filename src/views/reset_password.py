import os
import sys

from flask import Blueprint, flash, redirect, render_template, request, url_for
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, BadTimeSignature
from werkzeug.security import generate_password_hash

sys.path.append("..")
from configurations.extensions import db
from configurations.models import Lecturers, Students
from utils import send_mail

reset_passwords = Blueprint("reset_passwords", __name__)

serializer = URLSafeTimedSerializer("secret")


@reset_passwords.route("/reset_password", methods=["POST", "GET"])
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
                flash("User does not exist!", "danger")
                return render_template("/reset_password/index.html")

        hashCode = serializer.dumps(mail, salt="reset-password")
        if student:
            student.hashCode = hashCode
        else:
            lecturer.hashCode = hashCode
        server = (
            os.getenv("DEV_SERVER_NAME")
            if os.getenv("SERVER_MODE") == "DEV"
            else os.getenv("PROD_SERVER_NAME")
        )
        print(server)
        link = f"{server}/{hashCode}"
        db.session.commit()
        send_mail(
            to=mail,
            template="/reset_password/email.html",
            subject="Reset Password",
            username=username,
            link=link,
        )

        flash("A password reset link has been sent to your email!", "success")
    return render_template("/reset_password/index.html")


@reset_passwords.route("/<string:hashCode>", methods=["GET", "POST"])
def hashcode(hashCode):
    try:
        mail = serializer.loads(hashCode, salt="reset-password", max_age=600)
    except (BadTimeSignature, BadSignature):
        flash(
            "The password reset link has expired. Please request a new one.", "danger"
        )
        return redirect(url_for("index.show"))

    if student := Students.query.filter_by(email=mail).first():
        check = student
    elif lecturer := Lecturers.query.filter_by(email=mail).first():
        check = lecturer
    else:
        flash("User does not exist!", "danger")
        return render_template("/reset_password/base.html")

    if request.method != "POST":
        return render_template("/reset_password/reset.html", hashCode=hashCode)
    passw = request.form["passw"]
    cpassw = request.form["cpassw"]
    if passw == cpassw:
        check.password = generate_password_hash(passw, method="sha256")
        check.hashCode = None
        db.session.commit()
        flash("Your Password has been reset successfully!", "success")
        return redirect(url_for("index.show"))
    else:
        flash("Password fields do not match.", "danger")
        return render_template("/reset_password/reset.html", hashCode=hashCode)
