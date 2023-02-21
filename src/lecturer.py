import datetime
import os

import cv2
from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import LoginManager, login_required
from PIL import Image

from constants import *
from utils import gen, gen_frames, get_total_attendance

lecturer = Blueprint("lecturer", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(lecturer)


now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M-%S")


@lecturer.route("/lecturer", methods=["GET"])
# @login_required
def show():
    return render_template("/main_pages/lecturer.html")


@lecturer.route("/upload", methods=["POST"])
# @login_required
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


@lecturer.route("/take_attendance/<course_code>")
# @login_required
def take_attendance(course_code):
    return render_template(f"/attendance_pages/takeattendance_{course_code}.html")


@lecturer.route("/detect_face_feed/<course_code>")
# @login_required
def detect_face_feed(course_code):
    return Response(
        gen(file_path=f"./frontend/static/courses/{course_code}/attendance"),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


#### Registering Students


@lecturer.route("/register_students")
# @login_required
def index():
    return render_template("/main_pages/face_register_attendace.html")


@lecturer.route("/video_feed")
# @login_required
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@lecturer.route("/register_student", methods=["POST", "GET"])
# @login_required
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
            print("done")
        elif request.form.get("stop") == "Stop/Start":

            if switch == 1:
                switch = 0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                switch = 1

    elif request.method == "GET":
        return render_template("/main_pages/face_register_attendance.html")
    return render_template("/main_pages/face_register_attendance.html")


@lecturer.route("/view_attendance/<course_code>")
def attendance(course_code):
    text = f"Attendance Report for COE {course_code}"
    df = get_total_attendance(f"./frontend/static/courses/{course_code}/attendance")
    if df is not None:
        html_table = df.to_html(index=False)
    else:
        html_table = "No attendance data available."
    return render_template("/attendance_pages/attendance.html", html_table=html_table, text=text)
