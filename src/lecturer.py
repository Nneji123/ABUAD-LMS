"""
This module contains the code for the lecturer's view of the web application. It includes functionalities such as uploading files, recording attendance, registering students, and viewing attendance records.

The lecturer blueprint is registered with the login manager to ensure that the pages are only accessible by authenticated users.

This module uses Flask for the web framework, OpenCV for video processing, and Pandas and PIL for data handling and image processing, respectively.

It includes the following functions:

    show: Renders the lecturer homepage.
    upload_file: Uploads files to the application's file system.
    record_attendance: Renders the page for recording attendance and provides a video feed for the facial recognition.
    detect_face_feed: Generates a video feed for the facial recognition.
    index: Renders the page for registering students.
    video_feed: Provides a video feed for the webcam.
    tasks: Saves the images of registered students in the application's file system.
    attendance: Renders the page for viewing attendance records.
"""


import os
from datetime import datetime

import cv2
import pandas as pd
from flask import (
    Blueprint,
    Response,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import LoginManager, login_required
from PIL import Image
from werkzeug.utils import secure_filename

from constants import *
from utils import (
    get_total_attendance,
    base64_to_image,
)

lecturer = Blueprint("lecturer", __name__, template_folder="./templates")
login_manager = LoginManager()
login_manager.init_app(lecturer)


@lecturer.route("/lecturer", methods=["GET"])
@login_required
def show():
    return render_template("/pages/lecturer.html")


@lecturer.route("/upload/<course_code>", methods=["POST"])
@login_required
def upload_file(course_code):
    file = request.files[f"file_{course_code}"]
    if file.filename == "":
        flash("Error! No file selected", "danger")

    file_name = secure_filename(file.filename)
    file_extension = os.path.splitext(file_name)[-1].lower()
    file_names, file_extensions = os.path.splitext(file_name)
    new_file_name = f"{str(course_code)}-{file_names}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}{file_extensions.lower()}"

    if not any(course_code in valid_code for valid_code in VALID_COURSE_CODES):
        return "Error: Invalid course code"

    file_type = ""
    expected_extensions = []
    if "assignment" in file_name.lower() and file_extension in ASSIGNMENT_EXTENSIONS:
        file_type = "assignment"
        expected_extensions = ASSIGNMENT_EXTENSIONS
    elif file_extension in DOC_EXTENSIONS:
        file_type = "documents"
        expected_extensions = DOC_EXTENSIONS
    elif file_extension in VIDEO_EXTENSIONS:
        file_type = "video"
        expected_extensions = VIDEO_EXTENSIONS
    else:
        flash("Error! Invalid filetype", "danger")

    if file_extension not in expected_extensions:
        # flash(f"Error! Invalid file extension for {file_type}", "danger")
        return redirect(url_for("lecturer.show"))

    # save the file to the desired location
    os.makedirs(f"./templates/static/courses/{course_code}/{file_type}", exist_ok=True)
    file.save(f"./templates/static/courses/{course_code}/{file_type}/{new_file_name}")
    flash("File uploaded successfully!", "success")
    return redirect(url_for("lecturer.show"))


@lecturer.route("/lecturer/record_attendance/<course_code>")
@login_required
def record_attendance(course_code):
    course = course_code
    return render_template(f"/pages/record_attendance.html", course=course)


# Registering Students
@lecturer.route("/register_students/<course_code>")
@login_required
def index():
    return render_template("/pages/register.html")


@lecturer.route("/register_student/<course_code>", methods=["POST", "GET"])
@login_required
def tasks(course_code):
    if request.method == "POST":
        try:
            data_uri = request.json["data_uri"]
            names = request.json["name"]
            matric = request.json["matric"]
            dept = request.json["dept"]

            names = names.upper()
            matric = matric.upper()
            dept = dept.title()
            if data_uri is not None:
                filenamess = f"{names}-{str(matric)}-{dept}.jpg".replace("/", " ")
                img_pil = base64_to_image(data_uri)
                mypath = f"./templates/static/courses/{course_code}/registered_faces/{filenamess}"
                if os.path.exists(mypath):
                    flash("This student is already registered!", "danger")
                    print("True")
                    return render_template(
                        "/pages/register.html", course_code=course_code
                    )

                else:
                    cv2.imwrite(
                        mypath,
                        img_pil,
                    )
                    print("Done!")
                    flash("Student registered successfully!", "success")
                    return render_template(
                        "/pages/register.html", course_code=course_code
                    )

            else:
                return render_template("/pages/register.html", course_code=course_code)
        except TypeError as e:
            return render_template("/pages/register.html", course_code=course_code)
    elif request.method == "GET":
        return render_template("/pages/register.html", course_code=course_code)
    return render_template("/pages/register.html", course_code=course_code)


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
        file_path = f"./templates/static/courses/{course_code}/attendance/{filename}"

        if os.path.exists(file_path):
            text = f"Attendance Report for COE {course_code}"
            df = pd.read_csv(file_path)
            if df is not None:
                html_table = df.to_html(index=False)
            else:
                html_table = "No attendance data available."
            return render_template(
                "/pages/attendance.html",
                html_table=html_table,
                text=text,
                course=course,
            )
        else:
            return render_template(
                "/pages/attendance.html",
                text="No attendance data available for this date",
                html_table="No attendance data available.",
                course=course,
            )
    else:
        # return render_template("/pages/attendance_date.html")
        text = f"Attendance Report for COE {course_code}"
        df = get_total_attendance(
            f"./templates/static/courses/{course_code}/attendance"
        )
        if df is not None:
            html_table = df.to_html(index=False)
        else:
            html_table = "No attendance data available."
        return render_template(
            "/pages/attendance.html",
            html_table=html_table,
            text=text,
            course=course,
        )


@lecturer.route("/lecturer/view_registered_students/<course>", methods=["POST", "GET"])
@login_required
def get_images(course):
    # specify the directory path where the images are stored
    path = f"./templates/static/courses/{course}/registered_faces"

    # initialize an empty list to store the image details
    image_list = []

    # loop through each file in the directory
    for filename in os.listdir(path):
        if filename.endswith(".jpg"):
            # split the filename by space
            components = filename.split("-")
            name = components[0].strip()
            matricnumber = components[1].strip()
            department = components[-1].split(".")[0].strip()

            # create a dictionary to store the image details
            image_dict = {
                "name": name,
                "matricnumber": matricnumber.replace(" ", "/"),
                "department": department,
                "filename": url_for(
                    "static", filename=f"courses/{course}/registered_faces/{filename}"
                ),
            }

            # add the image dictionary to the image list
            image_list.append(image_dict)
    if image_list == []:
        # return the image details as JSON
        return jsonify("No students registered for this course!")
    else:
        return jsonify(images=image_list)


@lecturer.route("/lecturer/view_students/<course>")
@login_required
def view_students(course):
    return render_template(f"/pages/view_students.html", course=course)


@lecturer.route("/lecturer/view_students/delete_student/<course>", methods=["POST"])
@login_required
def delete_image(course):
    # get the filename from the request
    name = request.form["name"]
    matricnumber = request.form["matricnumber"]
    department = request.form["department"]

    filename = f"{name}-{matricnumber}-{department}.jpg".replace("/", " ")
    directory = os.path.join("./templates/static/courses", course, "attendance")

    # loop through all CSV files in the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check if the file is a CSV file
            if file.endswith(".csv"):
                # get the path to the CSV file
                path = os.path.join(root, file)

                # read the CSV file into a DataFrame
                df = pd.read_csv(path)

                # check if the student's name is in the DataFrame
                if name in df["Name"].values:
                    # delete the row containing the student's name
                    df = df[df["Name"] != name]

                    # write the updated DataFrame back to the CSV file
                    df.to_csv(path, index=False)

    # get the path to the image file
    path = f"./templates/static/courses/{course}/registered_faces/{filename}"
    # delete the image file
    try:
        os.remove(path)
        flash("Deleted Successfully", "success")
    except FileNotFoundError as e:
        print(e)
        flash("No files found!", "danger")

    return redirect(url_for("lecturer.view_students", course=course))


@lecturer.route(
    "/lecturer/view_students/edit_filename/<course>", methods=["POST", "GET"]
)
@login_required
def edit_filename(course):
    # get the old name, matric number, and department from the request
    old_name = request.form["old_name"]
    old_matricnumber = request.form["old_matricnumber"]
    old_department = request.form["old_department"]

    # get the new name, matric number, and department from the request
    new_name = request.form["name"].upper()
    new_matricnumber = request.form["matricnumber"].replace("/", " ").upper()
    new_department = request.form["department"].title()

    if new_name == "":
        new_name = old_name

    if new_department == "":
        new_department = old_department

    if new_matricnumber == "":
        new_matricnumber = old_matricnumber

    # replace any forward slashes with spaces in the new name, matric number, and department
    new_name = new_name.replace("/", " ")
    new_department = new_department.replace("/", " ")

    # set the new filename based on the new name, matric number, and department
    new_filename = f"{new_name}-{new_matricnumber}-{new_department}.jpg".replace(
        "/", " "
    )

    # check if the new filename already exists, and return an error message if it does
    if os.path.exists(
        os.path.join(
            "./templates/static/courses", course, "registered_faces", new_filename
        )
    ):
        flash("A student with that name and matric number already exists!", "danger")
        return render_template(f"/pages/view_students.html", course=course)

    directory = os.path.join("./templates/static/courses", course, "attendance")

    # loop through all CSV files in the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check if the file is a CSV file
            if file.endswith(".csv"):
                # get the path to the CSV file
                path = os.path.join(root, file)

                # read the CSV file into a DataFrame
                df = pd.read_csv(path)
                # check if the student's details are in the DataFrame
                mask = (
                    (df["Name"] == old_name)
                    & (df["Matric Number"] == old_matricnumber)
                    & (df["Department"] == old_department)
                )

                if mask.any():
                    # update the student's details in the DataFrame
                    df.loc[mask, "Name"] = new_name
                    df.loc[mask, "Matric Number"] = new_matricnumber
                    df.loc[mask, "Department"] = new_department

                    # write the updated DataFrame back to the CSV file
                    df.to_csv(path, index=False)

    # get the path to the old image file
    old_filename = f"{old_name}-{old_matricnumber}-{old_department}.jpg".replace(
        "/", " "
    )
    old_path = os.path.join(
        "./templates/static/courses", course, "registered_faces", old_filename
    )

    # get the path to the new image file
    new_path = os.path.join(
        "./templates/static/courses", course, "registered_faces", new_filename
    )

    # rename the old image file to the new image file
    os.rename(old_path, new_path)

    flash("Student details saved successfully!", "success")

    # return the view_students page with the updated course data
    return redirect(url_for("lecturer.view_students", course=course))
