import os
from datetime import datetime

import cv2
import pandas as pd
from flask import (Blueprint, Response, flash, redirect, render_template,
                   request, url_for)
from flask_login import LoginManager, current_user, login_required
from PIL import Image
from werkzeug.utils import secure_filename

from constants import *
from utils import gen, gen_frames, get_total_attendance

lecturer = Blueprint("lecturer", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(lecturer)


@lecturer.route("/lecturer", methods=["GET"])
@login_required
def show():
    return render_template("/main_pages/lecturer.html")


@lecturer.route("/upload/<course_code>", methods=["POST"])
@login_required
def upload_file(course_code):
    file = request.files["file"]
    if file.filename == "":
        flash("Error! No file selected")

    file_name = secure_filename(file.filename)
    file_extension = os.path.splitext(file_name)[-1].lower()
    file_names, file_extensions = os.path.splitext(file_name)
    new_file_name = f"{str(course_code)}-{file_names}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}{file_extensions}"
    # course_code = file_names
    print(new_file_name)
    print(file_extension)
    print(file_extensions)

    if not any(course_code in valid_code for valid_code in VALID_COURSE_CODES):
        return "Error: Invalid course code"

    file_type = ""
    if "assignment" in file_name.lower() and file_extension in ASSIGNMENT_EXTENSIONS:
        file_type = "assignment"
    elif file_extension in DOC_EXTENSIONS:
        file_type = "document"
    elif file_extension in VIDEO_EXTENSIONS:
        file_type = "video"
    else:
        flash("Error! Invalid filetype")

    # save the file to the desired location
    os.makedirs(f"./frontend/static/courses/{course_code}/{file_type}", exist_ok=True)
    file.save(f"./frontend/static/courses/{course_code}/{file_type}/{new_file_name}")
    flash("File uploaded successfully!")
    return redirect(url_for("lecturer.show"))


@lecturer.route("/lecturer/record_attendance/<course_code>")
@login_required
def record_attendance(course_code):
    course = course_code
    return render_template(f"/main_pages/record_attendance.html", course=course)


@lecturer.route("/detect_face_feed/<course_code>")
@login_required
def detect_face_feed(course_code):
    return Response(
        gen(file_path=f"./frontend/static/courses/{course_code}/attendance"),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


#### Registering Students
@lecturer.route("/register_students")
@login_required
def index():
    return render_template("/main_pages/register.html")


@lecturer.route("/video_feed")
# @login_required
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@lecturer.route("/register_student", methods=["POST", "GET"])
@login_required
def tasks():
    global switch, camera
    if request.method == "POST":
        names = request.form.get("name")
        matric = request.form.get("matric")
        dept = request.form.get("dept")
        print(names, matric, dept)
        if request.form.get("click") == "Capture":
            global capture
            capture = 1
            camera = cv2.VideoCapture(0)
            m, img = camera.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            filenamess = f"{names}-{str(matric)}-{dept}.jpg".replace("/", " ")
            im_pil.save(f"./registered_faces/{filenamess}")
            flash("Registered Student Successfully!")
            print("done")
    elif request.method == "GET":
        return render_template("/main_pages/register.html")
    return render_template("/main_pages/register.html")


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
        file_path = f"./frontend/static/courses/{course_code}/attendance/{filename}"
        
        if os.path.exists(file_path):
            text = f"Attendance Report for COE {course_code}"
            df = pd.read_csv(file_path)
            if df is not None:
                html_table = df.to_html(index=False)
            else:
                html_table = "No attendance data available."
            return render_template(
                "/main_pages/attendance.html",
                html_table=html_table,
                text=text,
                course=course
            )
        else:
            return render_template(
                "/main_pages/attendance.html",
                text="No attendance data available for this date",
                course = course
            )
    else:
            # return render_template("/main_pages/attendance_date.html")
        text = f"Attendance Report for COE {course_code}"
        df = get_total_attendance(f"./frontend/static/courses/{course_code}/attendance")
        if df is not None:
            html_table = df.to_html(index=False)
        else:
            html_table = "No attendance data available."
        return render_template(
            "/main_pages/attendance.html", html_table=html_table, text=text, course=course
        )


