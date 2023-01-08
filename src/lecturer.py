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

        file_name = str(file.filename)
        # get the file extension
        file_extension = file_name.split(".")[-1]
        file_names, file_extensions = os.path.splitext(file.filename)
        # construct the new file name with the current datetime and the original file name
        new_file_name = f"{file_names}-{now}{file_extensions}"

        # check the file type
        if "assignment" in ass_file.lower() and file_extension in [
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

        else:
            return "Error: Invalid file type"

        # check if the file name contains "assignment"

        if "501" in file_name:
            # save the file to the desired location
            file.save(f"./frontend/static/courses/501/{file_type}/{new_file_name}")
            flash("File uploaded successfully!")
            return redirect(url_for("lecturer.show"))

        elif "503" in file_name:
            file.save(f"./frontend/static/courses/503/{file_type}/{new_file_name}")
            flash("File uploaded successfully!")
            return redirect(url_for("lecturer.show"))

        elif "515" in file_name:
            file.save(f"./frontend/static/courses/515/{file_type}/{new_file_name}")
            flash("File uploaded successfully!")
            return redirect(url_for("lecturer.show"))

        elif "507" in file_name:
            file.save(f"./frontend/static/courses/507/{file_type}/{new_file_name}")
            flash("File uploaded successfully!")
            return redirect(url_for("lecturer.show"))

        elif "511" in file_name:
            file.save(f"./frontend/static/courses/511/{file_type}/{new_file_name}")
            flash("File uploaded successfully!")
            return redirect(url_for("lecturer.show"))

        elif "505" in file_name:
            file.save(f"./frontend/static/courses/505/{file_type}/{new_file_name}")
            flash("File uploaded successfully!")
            return redirect(url_for("lecturer.show"))

        elif "519" in file_name:
            file.save(f"./frontend/static/courses/519/{file_type}/{new_file_name}")

            flash("File uploaded successfully!")
            return redirect(url_for("lecturer.show"))
    return "No file selected!"
