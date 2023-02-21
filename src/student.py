import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required
from werkzeug.utils import secure_filename

from constants import COURSES_INFO
# from models import Users, db
from utils import count_name_in_files

student = Blueprint("student", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(student)


# @login_required
@student.route("/student", methods=["GET"])
def show():
    return render_template("/main_pages/student.html")


# @login_required
@student.route("/<course_code>/documents", methods=["GET", "POST"])
def list_docs(course_code):
    course_info = COURSES_INFO.get(course_code, {})
    doc_dir = course_info.get("doc_dir")
    doc_exts = course_info.get("doc_exts", ())
    files = [
        f
        for f in os.listdir(f"./frontend/static/courses/{doc_dir}")
        if f.endswith(doc_exts)
    ]
    return render_template(f"/course_pages/{course_code}.html", files=files)


@student.route("/<course_code>/videos", methods=["GET", "POST"])
# @login_required
def list_videos(course_code):
    course_info = COURSES_INFO.get(course_code, {})
    video_dir = course_info.get("video_dir")
    video_ext = course_info.get("video_ext", ".mp4")
    videos = [
        f
        for f in os.listdir(f"./frontend/static/courses/{video_dir}")
        if f.endswith(video_ext)
    ]
    if videos is None:
        return render_template(f"/course_pages/{course_code}.html")
    else:
        return render_template(f"/course_pages/{course_code}.html", videos=videos)


@student.route("/student/<course_code>", methods=["GET", "POST"])
# @login_required
def get_page(course_code):
    return render_template(f"/course_pages/{course_code}.html")


@student.route("/attendance/<course_code>/<student_name>")
def show_attendance(course_code, student_name):
    student_name = current_user.username
    # Define the path to the directory containing the attendance CSV files for this course
    dir_path = f"./frontend/static/attendance/{course_code}"

    # Use count_name_in_files to count the number of times the student's name appears in all CSV files in the directory
    count = count_name_in_files(dir_path, student_name)

    # Calculate the percentage of classes the student attended
    # num_classes = len(os.listdir(dir_path))
    # percent_attendance = count / num_classes * 100 if num_classes > 0 else 0

    # Render the HTML template and pass the attendance data
    return render_template(
        f"/course_pages/{course_code}.html",
        course=course_code,
        student=student_name,
        attendance=count,
    )
