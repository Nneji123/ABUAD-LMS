import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required
from werkzeug.utils import secure_filename

from models import Users, db

student = Blueprint("student", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(student)


@student.route("/student", methods=["GET"])
@login_required
def show():
    return render_template("student.html")


@student.route("/neuralnetworks", methods=["GET", "POST"])
# @login_required
def neuralnetworks():
    return render_template("neural_networks.html")


@student.route("/cad", methods=["GET", "POST"])
@login_required
def cad():
    return render_template("cad.html")


# get a list of files in the courses folder and pass it to the template
@student.route("/neuralnetworks/documents", methods=["GET", "POST"])
# @login_required
def list_docs_neuralnetworks():
    # Get a list of files from the directory
    files = [
        f
        for f in os.listdir("frontend/static/courses/501/documents")
        if f.endswith(
            (
                ".doc",
                ".docx",
                ".xls",
                ".xlsx",
                ".ppt",
                ".pptx",
                ".pdf",
                ".py",
                ".java",
                ".c",
                ".cpp",
                ".h",
            )
        )
    ]
    # Render the HTML template and pass the list of files
    return render_template("neural_networks.html", files=files)


@student.route("/neuralnetworks/videos", methods=["GET", "POST"])
# @login_required
def list_videos_neuralnetworks():
    # Get a list of videos from the directory
    videos = [
        f
        for f in os.listdir("./frontend/static/courses/501/video")
        if f.endswith(".mp4")
    ]
    # Render the HTML template and pass the list of videos
    return render_template("neural_networks.html", videos=videos)


@student.route("/cad/documents", methods=["GET", "POST"])
@login_required
def list_docs_cad():
    # Get a list of files from the directory
    files = [
        f
        for f in os.listdir("./frontend/static/courses/503/documents")
        if f.endswith(".doc")
    ]
    print(files)
    # files = flash(files)
    # Render the HTML template and pass the list of files
    return render_template("cad.html", files=files)


@student.route("/cad/videos", methods=["GET", "POST"])
@login_required
def list_videos_cad():
    # Get a list of videos from the directory
    videos = [
        f
        for f in os.listdir("./frontend/static/courses/503/video")
        if f.endswith(".mp4")
    ]
    # Render the HTML template and pass the list of videos
    return render_template("cad.html", videos=videos)

