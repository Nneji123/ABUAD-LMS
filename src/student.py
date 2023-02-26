import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required

from constants import COURSES_INFO
from utils import count_name_in_files

student = Blueprint("student", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(student)


@login_required
@student.route("/student", methods=["GET"])
def show():
    return render_template("/main_pages/student.html")


@student.route("/student/<course_code>")
@login_required
def get_page(course_code):
    student_name = current_user.username
    course_info = COURSES_INFO.get(course_code, {})
    video_dir = course_info.get("video_dir", "")
    video_ext = course_info.get("video_ext", ".mp4")
    doc_dir = course_info.get("doc_dir", "")
    doc_exts = course_info.get("doc_exts", ())
    attendance_path = f"./frontend/static/courses/{course_code}/attendance"
    attendance_record = count_name_in_files(attendance_path, student_name)

    videos = [
        f
        for f in os.listdir(f"./frontend/static/courses/{video_dir}")
        if f.endswith(video_ext)
    ]
    docs = [
        f
        for f in os.listdir(f"./frontend/static/courses/{doc_dir}")
        if f.endswith(doc_exts)
    ]

    return render_template(
        f"/course_pages/{course_code}.html",
        videos=videos,
        docs=docs,
        course=course_code,
        student=student_name,
        attendance=attendance_record,
    )
