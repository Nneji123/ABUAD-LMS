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


import csv
import os
from datetime import datetime

import cv2
import face_recognition
import numpy as np
import pandas as pd

from constants import *


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


def record_face_attendance(file_path, course):
    """
    The record_attendance function is a generator that yields the byte stream of images captured by the webcam.

    :param file_path: Save the attendance in a csv file
    :param course: Specify the course folder to save attendance in
    :return: A generator object, which is iterable
    """
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

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    while True:
        # Grab a single frame of video

        ret, frame = video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations)

        # Iterate through each face found in the current frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for any of the known faces
            matches = face_recognition.compare_faces(
                encodeListknown, face_encoding)
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
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

        frame = cv2.imencode(".jpg", frame)[1].tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    video_capture.release()


def capture_face():
    """
    The capture_face function is a generator function that captures frames from the camera, encodes them into
    a JPEG format, and returns the encoded frame. The function also yields each encoded frame as it is captured.

    :return: A generator object that yields the frame by frame data from a camera
    """
    global out, capture, rec_frame, frame
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if success:
            # detect faces
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) > 0:
                # draw bounding boxes around the faces
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35),
                                  (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    text = "Capture Face!"
                    cv2.putText(frame, text, (left + 6, bottom - 6),
                                font, 1.0, (255, 255, 255), 1)
            try:
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
            except Exception as e:
                pass
        else:
            pass

    camera.release()


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
        attendance_percentage = attendance_data["Attendance"] / \
            total_classes * 100
        data.append(
            {
                "Name": name,
                "Matric Number": attendance_data["Matric Number"],
                "Department": attendance_data["Department"],
                "Attendance Percentage": attendance_percentage,
            }
        )

    df = pd.DataFrame(
        data, columns=["Name", "Matric Number",
                       "Department", "Attendance Percentage"]
    )
    return df
