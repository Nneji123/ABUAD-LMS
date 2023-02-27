"""
This module defines a Flask blueprint for the student pages in the course management system. The blueprint allows students to view course documents, watch videos, and see their attendance record.

The `student` blueprint is created with a template folder at './templates'. The blueprint is protected with the `@login_required` decorator from Flask-Login, which ensures that only logged-in users can access the student pages. 

The `show` function is mapped to the '/student' route and returns the student homepage template, which displays a list of available courses.

The `get_page` function is mapped to the '/student/<course_code>' route, where `course_code` is the unique identifier for the course. This function retrieves the course information from `COURSES_INFO`, a dictionary containing course-specific data, such as video and document directories, file extensions, and attendance records. The function then uses this data to generate a course-specific page template, which displays the course name, a list of available documents and videos, and the student's attendance record.

The function `count_name_in_files` is used to count the number of times the student's username appears in the attendance file for the course. The function `os.listdir` is used to retrieve a list of available video and document files in the specified directories.

The course page template is rendered using the `render_template` function from Flask. The template displays the course name, course information, videos and documents available for the course, the student's attendance record, and a link to return to the student homepage.

This blueprint assumes that course information is stored in `COURSES_INFO` as a dictionary with the course code as the key and a dictionary containing course-specific information as the value.

"""


import os

from flask import Blueprint, render_template
from flask_login import LoginManager, current_user, login_required

from constants import COURSES_INFO
from utils import count_name_in_files

student = Blueprint("student", __name__, template_folder="./templates")
login_manager = LoginManager()
login_manager.init_app(student)


@login_required
@student.route("/student", methods=["GET"])
def show():
    return render_template("/pages/student.html")


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
        "/pages/coe.html",
        info=info,
        course_name=course_name,
        videos=videos,
        docs=docs,
        course=course_code,
        student=student_name,
        attendance=attendance_record,
    )
