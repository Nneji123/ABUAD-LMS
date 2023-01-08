import datetime
import os
from io import BytesIO

import numpy as np
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


@lecturer.route("/lecturer", methods=["GET"])
@login_required
def show():
    return render_template("lecturer.html")


@lecturer.route("/upload", methods=["POST"])
@login_required
def upload_video():
    # Get the file from the POST request
    file = request.files["file"]
    # Check if the file is not empty
    if file.filename != "":
        # Save the file to the desired location
        # get the file name in the form of a string
        ass_file = str(file.filename)

        print(ass_file.lower())

        file_name = str(file.filename)
        # get the file extension
        file_extension = file_name.split(".")[-1]
        file_names, file_extensions = os.path.splitext(file.filename)
        # construct the new file name with the current datetime and the original file name
        new_file_name = f"{file_names}-{now}{file_extensions}"
        print(new_file_name)
        
        course_code = str(file.filename)#.split("-")[0]
        print(course_code)

        # check the file type
        if "assignment" in file_name.lower() and file_extension in [
            "mp4",
            "avi",
            "mov",
            "wmv",
            "flv",
            "mkv",
            "doc",
            "docx",
            "pdf",
            "txt",
            "ppt",
            "pptx",
            "xls",
            "xlsx",
            ".csv",
        ]:
            file_type = "assignment"
        elif file_extension in [
            "doc",
            "docx",
            "pdf",
            "txt",
            "ppt",
            "pptx",
            "xls",
            "xlsx",
        ]:
            file_type = "documents"
        elif file_extension in ["mp4", "avi", "mov", "wmv", "flv", "mkv"]:
            file_type = "video"

        # check if the file name contains "assignment"

        if course_code in VALID_COURSE_CODES:
            # save the file to the desired location
            file.save(f"./frontend/static/courses/{course_code}/{file_type}/{new_file_name}")
            flash("File uploaded successfully!")
            return redirect(url_for("lecturer.show"))
        
        else:
            return "Error: Invalid file type"
        
    else:
        return "No file selected!"