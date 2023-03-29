"""Student Page Routes"""


import os
import sys
from datetime import datetime


import cv2
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from werkzeug.security import generate_password_hash

sys.path.append("..")

from constants import COURSES_INFO
from configurations.models import Students
from configurations.extensions import db
from utils import count_name_in_files, base64_to_image

student = Blueprint("student", __name__)
login_manager = LoginManager()
login_manager.init_app(student)


@login_required
@student.route("/student", methods=["GET"])
def show():
    dt_str = str(current_user.created_at)
    dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    date = dt_obj.strftime("%A, %d %B %Y")
    return render_template("/pages/student.html", date=date)


@login_required
@student.route("/student/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        user = Students.query.filter_by(username=current_user.username).first()
        if user:
            old_password = request.form["old_password"]
            if user.check_password(old_password):
                new_password = request.form["new_password"]
                confirm_password = request.form["confirm_new_password"]
                if new_password == confirm_password:
                    user.password = generate_password_hash(
                        new_password, method="sha256"
                    )
                    db.session.commit()
                    flash("Password Changed Successfully", "success")
                    return redirect(
                        url_for("student.show") + "?success=change-password-succesful"
                    )
                else:
                    flash("Your password does not match please try again!", "danger")
                    return redirect(
                        url_for("student.show") + "?error=password-does-not-match"
                    )
            else:
                flash("Your old password is incorrect! Please try again", "danger")
                return redirect(url_for("student.show") + "?error=password-incorrect")
        else:
            flash("User does not exist!", "danger")
            return redirect(url_for("student.show") + "?error=user-does-not-exist")
    else:
        return redirect(url_for("student.show"))


@student.route("/student/take_picture/<name>", methods=["POST", "GET"])
@login_required
def take_picture(name):
    print("Entering take_picture function")
    dt_str = str(current_user.created_at)
    dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    date = dt_obj.strftime("%A, %d %B %Y")

    if request.method == "POST":
        print("Request method is POST")
        try:
            data_uri = request.json["data_uri"]
            # name = current_user.username
            matric = current_user.matric_number
            dept = current_user.department

            print(f"data_uri: {data_uri}")
            names = name.upper()
            matric = matric.upper()
            dept = dept.title()

            if data_uri is not None:
                filename = f"{names}-{str(matric)}-{dept}.jpg".replace("/", " ")
                img_pil = base64_to_image(data_uri)
                mypath = f"./templates/static/courses/profile_pics/{filename}"

                if os.path.exists(mypath):
                    flash("This student is already registered!", "danger")
                    print("This student is already registered!")
                else:
                    cv2.imwrite(mypath, img_pil)
                    print("Student registered successfully")
                    flash("Student registered successfully!", "success")

            else:
                print("data_uri is None")

        except TypeError as e:
            print(f"Error: {e}")

    elif request.method == "GET":
        print("Request method is GET")

    else:
        print("Unknown request method")

    return render_template("/pages/student.html", date=date)


@student.route("/student/<course_code>")
@login_required
def get_page(course_code):
    student_name = current_user.username
    course_info = COURSES_INFO.get(course_code, {})
    video_dir = course_info.get("video_dir", "")
    video_ext = course_info.get("video_ext", ".mp4")
    course_name = course_info.get("course_name")
    info = course_info.get("info")
    doc_dir = course_info.get("doc_dir", "")
    doc_exts = course_info.get("doc_exts", ())
    attendance_path = f"./templates/static/courses/{course_code}/attendance"
    attendance_record = count_name_in_files(attendance_path, student_name.upper())

    videos = [
        f
        for f in os.listdir(f"./templates/static/courses/{video_dir}")
        if f.endswith(video_ext)
    ]
    docs = [
        f
        for f in os.listdir(f"./templates/static/courses/{doc_dir}")
        if f.endswith(doc_exts)
    ]

    return render_template(
        "/pages/coe.html",
        info=info,
        course_name=course_name,
        videos=videos,
        docs=docs,
        course=course_code,
        student=student_name,
        attendance=attendance_record,
    )
