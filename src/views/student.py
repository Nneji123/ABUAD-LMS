"""Student Page Routes"""


import os
import sys
import shutil
from datetime import datetime


import cv2
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

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
    matric = current_user.matric_number
    dept = current_user.department
    name = current_user.username

    names = name.upper()
    matric = matric.upper()
    dept = dept.title()
    filename = f"{names}-{str(matric)}-{dept}.jpg".replace("/", " ")
    mypath = f"./templates/static/profile_pics/{filename}"
    profile_pic = None
    if not os.path.exists(mypath):
        profile_pic = url_for("static", filename=f"profile_pics/generic_profile.png")
    else:
        profile_pic = url_for("static", filename=f"profile_pics/{filename}")

    return render_template("/pages/student.html", date=date, profile_pic=profile_pic)


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
def take_pictures(name):
    dt_str = str(current_user.created_at)
    dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    date = dt_obj.strftime("%A, %d %B %Y")

    if request.method == "POST":
        try:
            data_uri = request.json["data_uri"]
            matric = current_user.matric_number
            dept = current_user.department

            names = name.upper()
            matric = matric.upper()
            dept = dept.title()

            if data_uri is not None:
                filename = f"{names}-{str(matric)}-{dept}.jpg".replace("/", " ")
                img_pil = base64_to_image(data_uri)
                mypath = f"./templates/static/profile_pics/{filename}"
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


@student.route("/student/upload_profile_picture", methods=["POST"])
@login_required
def upload_profile_picture():
    file = request.files["file"]
    if file.filename == "":
        flash("Error! No file selected", "danger")
    matric = current_user.matric_number
    dept = current_user.department
    name = current_user.username

    names = name.upper()
    matric = matric.upper()
    dept = dept.title()

    file_name = secure_filename(file.filename)
    file_extension = os.path.splitext(file_name)[-1].lower()

    if file_extension not in [".jpeg", ".jpg", ".png"]:
        flash(
            "Invalid filetype uploaded! Please only upload jpeg, jpg or png file formats!",
            "danger",
        )
        return redirect(url_for("student.show"))

    filename = f"{names}-{str(matric)}-{dept}.jpg".replace("/", " ")
    mypath = f"./templates/static/profile_pics/{filename}"

    if os.path.exists(mypath):
        os.remove(mypath)
        print("file deleted!")

    file.save(mypath)
    flash("File uploaded successfully!", "success")
    return redirect(url_for("student.show"))


def check_and_copy_file(src_folder, dst_folder, filename):
    src_path = os.path.join(src_folder, filename)
    dst_path = os.path.join(dst_folder, filename)

    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        return True
    else:
        return False


@student.route("/student/register/<course_code>", methods=["POST", "GET"])
@login_required
def register_course_student(course_code):
    matric = current_user.matric_number
    dept = current_user.department
    name = current_user.username

    names = name.upper()
    matric = matric.upper()
    dept = dept.title()
    filename = f"{names}-{str(matric)}-{dept}.jpg".replace("/", " ")
    mypath = f"./templates/static/profile_pics/{filename}"
    course_path = f"./templates/static/courses/{course_code}/registered_faces"
    if not os.path.exists(mypath):
        flash(
            "Please set your profile picture before registering for a course!", "danger"
        )
        return redirect(url_for("student.show"))

    check_and_copy_file(
        src_folder=f"./templates/static/profile_pics",
        dst_folder=course_path,
        filename=filename,
    )
    if True:
        flash(f"Successfully registered for COE {course_code}!", "success")
        return redirect(url_for("student.show"))
    else:
        flash("Error!", "danger")
        return redirect(url_for("student.show"))


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
