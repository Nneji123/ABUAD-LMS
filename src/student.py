import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required

from constants import COURSES_INFO
from utils import count_name_in_files

student = Blueprint("student", __name__, template_folder="./templates")
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
    course_name = course_info.get("course_name")
    info = course_info.get("info")
    doc_dir = course_info.get("doc_dir", "")
    doc_exts = course_info.get("doc_exts", ())
    attendance_path = f"./templates/static/courses/{course_code}/attendance"
    attendance_record = count_name_in_files(attendance_path, student_name)

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
        "/main_pages/COE.html",
        info=info,
        course_name=course_name,
        videos=videos,
        docs=docs,
        course=course_code,
        student=student_name,
        attendance=attendance_record,
    )
