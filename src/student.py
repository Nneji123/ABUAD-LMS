import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required
from werkzeug.utils import secure_filename

from models import Users, db

student = Blueprint("student", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(student)

COURSES_INFO = {
    "501": {
        "doc_dir": "501/documents",
        "doc_exts": (".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".py", ".java", ".c", ".cpp", ".h"),
        "video_dir": "501/video",
        "video_ext": ".mp4"
    },
    "503": {
        "doc_dir": "503/documents",
        "doc_exts": (".doc",),
        "video_dir": "503/video",
        "video_ext": ".mp4"
    },
    "507": {
        "doc_dir": "507/documents",
        "doc_exts": (".doc",),
        "video_dir": "507/video",
        "video_ext": ".mp4"
    }
}


@student.route("/student", methods=["GET"])
# @login_required
def show():
    return render_template("/main_pages/student.html")



@student.route("/<course_code>/documents", methods=["GET", "POST"])
def list_docs(course_code):
    course_info = COURSES_INFO.get(course_code, {})
    doc_dir = course_info.get("doc_dir")
    doc_exts = course_info.get("doc_exts", ())
    files = [f for f in os.listdir(f"./frontend/static/courses/{doc_dir}") if f.endswith(doc_exts)]
    return render_template(f"/course_pages/{course_code}.html", files=files)

@student.route("/<course_code>/videos", methods=["GET", "POST"])
def list_videos(course_code):
    course_info = COURSES_INFO.get(course_code, {})
    video_dir = course_info.get("video_dir")
    video_ext = course_info.get("video_ext", ".mp4")
    videos = [f for f in os.listdir(f"./frontend/static/courses/{video_dir}") if f.endswith(video_ext)]
    if videos is None:
        return render_template(f"/course_pages/{course_code}.html")
    else:
        return render_template(f"/course_pages/{course_code}.html", videos=videos)

@student.route("/student/<course_code>", methods=["GET", "POST"])
def get_page(course_code):
    return render_template(f"/course_pages/{course_code}.html")
