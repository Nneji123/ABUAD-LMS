"""Lecturer Page Routes and Functions"""

import os
import sys
from datetime import datetime

import pandas as pd
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import LoginManager, current_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

sys.path.append("..")

from configurations.models import Announcements, Lecturers, db
from constants import *
from utils import get_total_attendance

lecturer = Blueprint("lecturer", __name__)
login_manager = LoginManager()
login_manager.init_app(lecturer)


@lecturer.route("/lecturer", methods=["GET"])
@login_required
def show():
    dt_str = str(current_user.created_at)
    dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    date = dt_obj.strftime("%A, %d %B %Y")
    name = current_user.username
    email = current_user.email
    filename = f"{name}-{email}.jpg".replace("/", " ")
    mypath = f"./templates/static/profile_pics/{filename}"
    profile_pic = None
    if not os.path.exists(mypath):
        profile_pic = url_for("static", filename=f"profile_pics/generic_profile.png")
    else:
        profile_pic = url_for("static", filename=f"profile_pics/{filename}")

    return render_template("/pages/lecturer.html", date=date, profile_pic=profile_pic)


@login_required
@lecturer.route("/lecturer/change_password", methods=["GET", "POST"])
def change_password_lecturer():
    if request.method == "POST":
        user = Lecturers.query.filter_by(username=current_user.username).first()
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
                        url_for("lecturer.show") + "?success=change-password-succesful"
                    )
                else:
                    flash("Your password does not match please try again!", "danger")
                    return redirect(
                        url_for("lecturer.show") + "?error=password-does-not-match"
                    )
            else:
                flash("Your old password is incorrect! Please try again", "danger")
                return redirect(url_for("lecturer.show") + "?error=password-incorrect")
        else:
            flash("User does not exist!", "danger")
            return redirect(url_for("lecturer.show") + "?error=user-does-not-exist")
    else:
        return redirect(url_for("lecturer.show"))


@lecturer.route("/lecturer/upload_profile_picture", methods=["POST"])
@login_required
def upload_profile_picture_lecturer():
    file = request.files["file"]
    if file.filename == "":
        flash("Error! No file selected", "danger")
    name = current_user.username
    email = current_user.email
    filename = f"{name}-{email}.jpg".replace("/", " ")
    mypath = f"./templates/static/profile_pics/{filename}"

    file_name = secure_filename(file.filename)
    file_extension = os.path.splitext(file_name)[-1].lower()

    if file_extension not in [".jpeg", ".jpg", ".png"]:
        flash(
            "Invalid filetype uploaded! Please only upload jpeg, jpg or png file formats!",
            "danger",
        )
        return redirect(url_for("lecturer.show"))

    mypath = f"./templates/static/profile_pics/{filename}"

    if os.path.exists(mypath):
        os.remove(mypath)
        print("file deleted!")

    file.save(mypath)
    flash("Profile Picture Uploaded Successfully!", "success")
    return redirect(url_for("lecturer.show"))


@lecturer.route("/upload/<course_code>", methods=["POST"])
@login_required
def upload_file(course_code):
    file = request.files[f"file_{course_code}"]
    if file.filename == "":
        flash("Error! No file selected", "danger")

    file_name = secure_filename(file.filename)
    file_extension = os.path.splitext(file_name)[-1].lower()
    file_names, file_extensions = os.path.splitext(file_name)
    new_file_name = f"{str(course_code)}-{file_names}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}{file_extensions.lower()}"

    if not any(course_code in valid_code for valid_code in VALID_COURSE_CODES):
        return "Error: Invalid course code"

    file_type = ""
    expected_extensions = []
    if "assignment" in file_name.lower() and file_extension in ASSIGNMENT_EXTENSIONS:
        file_type = "assignment"
        expected_extensions = ASSIGNMENT_EXTENSIONS
    elif file_extension in DOC_EXTENSIONS:
        file_type = "documents"
        expected_extensions = DOC_EXTENSIONS
    elif file_extension in VIDEO_EXTENSIONS:
        file_type = "video"
        expected_extensions = VIDEO_EXTENSIONS
    else:
        flash("Error! Invalid filetype", "danger")

    if file_extension not in expected_extensions:
        # flash(f"Error! Invalid file extension for {file_type}", "danger")
        return redirect(url_for("lecturer.show"))

    # save the file to the desired location
    os.makedirs(f"./templates/static/courses/{course_code}/{file_type}", exist_ok=True)
    file.save(f"./templates/static/courses/{course_code}/{file_type}/{new_file_name}")
    flash("File uploaded successfully!", "success")
    return redirect(url_for("lecturer.show"))


@lecturer.route("/lecturer/record_attendance/<course_code>")
@login_required
def record_attendance(course_code):
    course = course_code
    return render_template(f"/pages/record_attendance.html", course=course)


# View Attendance Records
@lecturer.route("/lecturer/view_attendance/<course_code>", methods=["POST", "GET"])
@login_required
def attendance(course_code):
    course = course_code
    if request.method == "POST":
        year = request.form.get("year")
        month = request.form.get("month")
        day = request.form.get("day")
        date = f"{year}-{month}-{day}"
        # search for the attendance file for that date
        filename = f"{date}-attendance.csv"
        file_path = f"./templates/static/courses/{course_code}/attendance/{filename}"

        if os.path.exists(file_path):
            text = f"Attendance Report for COE {course_code}"
            df = pd.read_csv(file_path)
            if df is not None:
                html_table = df.to_html(index=False)
            else:
                html_table = "No attendance data available."
            return render_template(
                "/pages/attendance.html",
                html_table=html_table,
                text=text,
                course=course,
            )
        else:
            return render_template(
                "/pages/attendance.html",
                text="No attendance data available for this date",
                html_table="No attendance data available.",
                course=course,
            )
    else:
        # return render_template("/pages/attendance_date.html")
        text = f"Attendance Report for COE {course_code}"
        df = get_total_attendance(
            f"./templates/static/courses/{course_code}/attendance"
        )
        if df is not None:
            html_table = df.to_html(index=False)
        else:
            html_table = "No attendance data available."
        return render_template(
            "/pages/attendance.html",
            html_table=html_table,
            text=text,
            course=course,
        )


@lecturer.route("/lecturer/view_registered_students/<course>", methods=["POST", "GET"])
@login_required
def get_images(course):
    # specify the directory path where the images are stored
    path = f"./templates/static/courses/{course}/registered_faces"

    # initialize an empty list to store the image details
    image_list = []

    # loop through each file in the directory
    for filename in os.listdir(path):
        if filename.endswith(".jpg"):
            # split the filename by space
            components = filename.split("-")
            name = components[0].strip()
            matricnumber = components[1].strip()
            department = components[-1].split(".")[0].strip()

            # create a dictionary to store the image details
            image_dict = {
                "name": name,
                "matricnumber": matricnumber.replace(" ", "/"),
                "department": department,
                "filename": url_for(
                    "static", filename=f"courses/{course}/registered_faces/{filename}"
                ),
            }

            # add the image dictionary to the image list
            image_list.append(image_dict)
    if image_list == []:
        # return the image details as JSON
        return jsonify("No students registered for this course!")
    else:
        return jsonify(images=image_list)


@lecturer.route("/lecturer/view_students/<course>")
@login_required
def view_students(course):
    return render_template(f"/pages/view_students.html", course=course)


@lecturer.route("/lecturer/make_announcement/<course>", methods=["GET", "POST"])
@login_required
def make_announcement(course):
    if request.method == "POST":
        name = current_user.username
        email = current_user.email
        filename = f"{name}-{email}.jpg".replace("/", " ")
        mypath = f"./templates/static/profile_pics/{filename}"
        profile_pic = None
        if not os.path.exists(mypath):
            profile_pic = url_for(
                "static", filename=f"profile_pics/generic_profile.png"
            )
        else:
            profile_pic = url_for("static", filename=f"profile_pics/{filename}")
        title = request.form["announcementTitle"]
        message = request.form["announcementText"]
        announcement = Announcements(
            lecturer_id=current_user.id,
            profile_pic=str(profile_pic),
            message=message,
            title=title,
            course_code=course,
        )
        try:
            db.session.add(announcement)
            db.session.commit()
            flash("Announcement posted successfully!", "success")
            return redirect(url_for("lecturer.show"))
        except IntegrityError as e:
            flash("Error occured! Please try again later!", "danger")
            db.session.rollback()
            return redirect(url_for("lecturer.show"))
        finally:
            db.session.close()

    return redirect(url_for("lecturer.show"))
