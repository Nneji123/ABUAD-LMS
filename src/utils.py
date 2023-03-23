"""
The code is a facial recognition attendance system that uses OpenCV, face_recognition and other libraries to recognize faces in real-time, match them to pre-registered faces, and save attendance records to a CSV file.

The script contains two functions:

    `save_attendance` - This function saves the attendance data to a CSV file. It takes in an input string of the format: "Name-Matric Number-Department" and saves it to a CSV file with the current date as its name. If there is already an existing attendance record for that student on that day, it will not save another one.

    `gen` - This function generates the video feed. It takes in a file path as an argument and uses that to save the attendance data. If no file path is given, it defaults to using 'attendance_data/attendance_data.csv'.

Parameters:

    attendance_str (str): Pass in the string that was captured from the camera.
    location (str): Specify the location of the attendance file.
    file_path (str): Save the attendance in a csv file.
    course (str): The name of the course to get registered faces.

Returns:

    False if the name and date are already in the file.

Note:

    Before running the script, make sure to create the attendance_data directory in the same location as the script, and a subdirectory called registered_faces within the courses directory.




"""

import base64
import csv
import os
from datetime import datetime

import css_inline
import cv2
import face_recognition
import numpy as np
import pandas as pd
from flask import render_template
from flask_mail import Message
from flask_socketio import emit

from configurations.extensions import email, socketio
from constants import *


def send_mail(to, template, subject, link, username, **kwargs):
    """
    The send_mail_flask function is used to send an email from the Flask app.
    It takes in a recipient, template, subject and link as its parameters. It also takes in optional arguments that can be passed into the function.

    :param to: Specify the recipient of the email
    :param template: Specify the html template that will be used to send the email
    :param subject: Set the subject of the email
    :param link: Create a unique link for each user
    :param username: Populate the username field in the email template
    :param **kwargs: Pass in any additional variables that are needed to be rendered in the email template
    :return: The html of the email that is being sent
    """
    if os.getenv("SERVER_MODE") == "DEV":
        sender = os.getenv("DEV_SENDER_EMAIL")
    elif os.getenv("SERVER_MODE") == "PROD":
        sender = os.getenv("PROD_SENDER_EMAIL")
    msg = Message(subject=subject, sender=sender, recipients=[to])
    html = render_template(template, username=username, link=link, **kwargs)
    inlined = css_inline.inline(html)
    msg.html = inlined
    email.send(msg)


def base64_to_image(base64_string):
    """
    The base64_to_image function accepts a base64 encoded string and returns an image.
    The function extracts the base64 binary data from the input string, decodes it, converts
    the bytes to numpy array, and then decodes the numpy array as an image using OpenCV.

    :param base64_string: Pass the base64 encoded image string to the function
    :return: An image
    """
    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


@socketio.on("connect")
def test_connect():
    """
    The test_connect function is used to test the connection between the client and server.
    It sends a message to the client letting it know that it has successfully connected.

    :return: A 'connected' string
    """
    print("Connected")
    emit("my response", {"data": "Connected"})


@socketio.on("image")
def capture_face(image):
    """
    The receive_image function takes in an image from the webcam, converts it to grayscale, and then emits
    the processed image back to the client.


    :param image: Pass the image data to the receive_image function
    :return: The image that was received from the client
    """
    # Decode the base64-encoded image data
    image = base64_to_image(image)
    frame = image
    # detect faces
    face_locations = face_recognition.face_locations(frame)
    if len(face_locations) > 0:
        # draw bounding boxes around the faces
        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            text = "Capture Face!"
            cv2.putText(
                frame, text, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )
    gray = frame
    frame_resized = cv2.resize(gray, (640, 360))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    processed_img_data = base64.b64encode(frame_encoded).decode()
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    emit("processed_image", processed_img_data)


def save_attendance(attendance_str: str, location: str):
    """
    The save_attendance function saves the attendance data to a CSV file.
    It takes in an input string of the format: &quot;Name-Matric Number-Department&quot; and saves it to a CSV file with the current date as its name.
    If there is already an existing attendance record for that student on that day, it will not save another one.

    :param attendance_str: str: Pass in the string that was captured from the camera
    :param location: str: Specify the location of the attendance file
    :return: False if the name and date are already in the file
    """
    # Split the input string into parts
    parts = attendance_str.split("-")
    name = parts[0]
    matric_number = parts[1]
    department = parts[2]
    # Get the current date and time
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    date_string = now.strftime("%Y-%m-%d")
    filename = f"{date_string}-attendance.csv".capitalize()
    # check if the file already exists
    if os.path.exists(f"{location}/{filename}"):
        # print("True")
        with open(f"{location}/{filename}", "r") as attendance_file:
            attendance_reader = csv.reader(attendance_file)
            # Check if the name and date is already in the file
            for row in attendance_reader:
                if name == row[0] and current_date == row[3]:
                    # print(f'Attendance for {name} on {current_date} already recorded')
                    return False
    else:
        # print("False")
        # Write the headers
        with open(f"{location}/{filename}", "w", newline="") as attendance_file:
            attendance_writer = csv.writer(
                attendance_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            attendance_writer.writerow(
                ["Name", "Matric Number", "Department", "Date", "Time"]
            )
    # Write the attendance data
    with open(f"{location}/{filename}", "a", newline="") as attendance_file:
        attendance_writer = csv.writer(
            attendance_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        attendance_writer.writerow(
            [name, matric_number, department, current_date, current_time]
        )


def encoding_img(IMAGE_FILES):
    encodeList = []
    for img in IMAGE_FILES:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except Exception as e:
            e = "error"
    return encodeList


@socketio.on("images")
def record_face(images, course):
    """
    The receive_image function takes in an image from the webcam, converts it to grayscale, and then emits
    the processed image back to the client.
    :param image: Pass the image data to the receive_image function
    :return: The image that was received from the client
    """
    file_path = f"./templates/static/courses/{course}/attendance"
    # Decode the base64-encoded image data
    image = base64_to_image(images)
    # print("These are the gotten information: ", image, course, file_path)
    frame = image
    # detect faces
    IMAGE_FILES = []
    filename = []
    dir_path = f"./templates/static/courses/{course}/registered_faces"

    for imagess in os.listdir(dir_path):
        img_path = os.path.join(dir_path, imagess)
        img_path = face_recognition.load_image_file(
            img_path
        )  # reading image and append to list
        IMAGE_FILES.append(img_path)
        filename.append(imagess.split(".", 1)[0])

    encodeListknown = encoding_img(IMAGE_FILES)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Iterate through each face found in the current frame
    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):
        # See if the face is a match for any of the known faces
        matches = face_recognition.compare_faces(encodeListknown, face_encoding)
        name = "This Student is not registered"

        # If a match was found in known_face_encodings, use the name of the first one that matches
        if True in matches:
            first_match_index = matches.index(True)
            name = filename[first_match_index]
            name = (
                f"{name}"
                if save_attendance(name, file_path) != False
                else "Attendance already recorded"
            )

            # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(
            frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
        )
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    gray = frame
    frame_resized = cv2.resize(gray, (640, 360))
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    processed_img_data = base64.b64encode(frame_encoded).decode()
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data
    emit("recorded_image", processed_img_data)


def count_name_in_files(directory_path, name):
    """
    The count_name_in_files function counts the number of times a name appears in all csv files in a directory.
    It returns the percentage of files that contain the name and whether or not they are eligible to write exams for this course.

    :param directory_path: Specify the path of the directory that contains all csv files
    :param name: Pass the name of the student whose attendance is to be checked
    :return: A string that tells you how many times the name appears in the files
    """
    count = 0
    num_files = 0

    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.endswith(".csv"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, newline="") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if row and row[0] == name:
                            count += 1
                num_files += 1

    if num_files == 0:
        return "No attendance data available for this course!"

    percentage = count / num_files * 100
    eligibility = "eligible" if percentage >= 70 else "not eligible"
    # \nYou are {eligibility} to write exams for this course!"
    message = f"{name}'s Attendance for this course is {percentage}%"
    return message


def get_total_attendance(directory_path):
    """
    The get_total_attendance function calculates the total attendance of all students in a given directory.
    It returns a pandas dataframe with the following columns: Name, Matric Number, Department and Attendance Percentage.
    The function takes one argument - directory_path which is the path to the folder containing all csv files.

    :param directory_path: Specify the path to the directory containing all of the attendance csv files
    :return: A dataframe with the attendance percentage of each student
    """
    student_attendance = {}

    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    name = row["Name"]
                    matric_number = row["Matric Number"]
                    department = row["Department"]

                    if name not in student_attendance:
                        student_attendance[name] = {
                            "Matric Number": matric_number,
                            "Department": department,
                            "Attendance": 0,
                        }

                    student_attendance[name]["Attendance"] += 1

    data = []
    for name, attendance_data in student_attendance.items():
        total_classes = len(os.listdir(directory_path))
        attendance_percentage = attendance_data["Attendance"] / total_classes * 100
        data.append(
            {
                "Name": name,
                "Matric Number": attendance_data["Matric Number"],
                "Department": attendance_data["Department"],
                "Attendance Percentage": attendance_percentage,
            }
        )

    df = pd.DataFrame(
        data, columns=["Name", "Matric Number", "Department", "Attendance Percentage"]
    )
    return df
