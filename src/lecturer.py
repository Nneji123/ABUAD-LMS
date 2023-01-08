import datetime
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required
from werkzeug.utils import secure_filename

from models import Users, db

lecturer = Blueprint("lecturer", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(lecturer)

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M-%S")
VALID_COURSE_CODES = ["501", "503", "515", "507", "511", "505", "519"]
VIDEO_EXTENSIONS = [
    "mp4",
    "mkv",
    "avi",
    "mov",
    "flv",
    "wmv",
    "webm",
    "mpeg",
    "mpg",
    "m4v",
    "3gp",
    "3g2",
    "f4v",
    "f4p",
    "f4a",
    "f4b",
]
DOC_EXTENSIONS = [
    "pdf",
    "docx",
    "doc",
    "csv",
]
ASSIGNMENT_EXTENSIONS = [
    "pdf",
    "docx",
    "doc",
    "csv",
    "txt",
    "pptx",
    "ppt",
    "xlsx",
    "xls",
    "zip",
    "rar",
    "7z",
    "tar",
    "gz",
    "bz2",
    "xz",
    "iso",
    "mp4",
    "mkv",
    "avi",
    "mov",
    "flv",
    "wmv",
    "webm",
    "mpeg",
    "mpg",
    "m4v",
    "3gp",
    "3g2",
    "f4v",
    "f4p",
    "f4a",
    "f4b",
]


@lecturer.route("/lecturer", methods=["GET"])
@login_required
def show():
    return render_template("lecturer.html")


@lecturer.route("/upload", methods=["POST"])
@login_required
def upload_video():
    file = request.files["file"]
    if file.filename != "":
        file_name = str(file.filename)
        file_extension = file_name.split(".")[-1]
        file_names, file_extensions = os.path.splitext(file.filename)
        new_file_name = f"{file_names}-{now}{file_extensions}"
        course_code = file_names
        print(course_code)

        if any(course_code in VALID_COURSE_CODES for course_code in VALID_COURSE_CODES):
            for course_code in VALID_COURSE_CODES:
                if course_code in file_name:
                    if (
                        "assignment" in file_name.lower()
                        and file_extension in ASSIGNMENT_EXTENSIONS
                    ):
                        print("assignment")
                        file_type = "assignment"
                        file.save(
                            f"./frontend/static/courses/{course_code}/assignment/{new_file_name}"
                        )
                        flash("File uploaded successfully!")
                        return redirect(url_for("lecturer.show"))
                    elif (
                        "assignment" not in course_code
                        and file_extension in DOC_EXTENSIONS
                    ):
                        file_type = "documents"
                    elif (
                        "assignment" not in course_code
                        and file_extension in VIDEO_EXTENSIONS
                    ):

                        file_type = "video"

                    # save the file to the desired location
                    file.save(
                        f"./frontend/static/courses/{course_code}/{file_type}/{new_file_name}"
                    )
                    flash("File uploaded successfully!")
                    return redirect(url_for("lecturer.show"))
        else:
            return "Error: Invalid file type"
    else:
        return "No file selected!"
