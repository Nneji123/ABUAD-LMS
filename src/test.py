import csv
from datetime import datetime
import os

def save_attendance(attendance_str):
    # Split the input string into parts
    parts = attendance_str.split("-")
    name = parts[0]
    matric_number = parts[1]
    department = parts[2]
    # Get the current date and time
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    # Check if the file already exists
    if not os.path.exists("attendance.csv"):
        # Write the headers
        with open("attendance.csv", 'w', newline='') as attendance_file:
            attendance_writer = csv.writer(attendance_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            attendance_writer.writerow(["Name", "Matric Number", "Department", "Date", "Time"])
    # Write the attendance data
    with open("attendance.csv", 'a', newline='') as attendance_file:
        attendance_writer = csv.writer(attendance_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        attendance_writer.writerow([name, matric_number, department, current_date, current_time])



save_attendance("Nneji Ifeanyi Daniel-19 ENG02 077-Computer Engineering")
