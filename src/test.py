# import csv
# import os
# from datetime import datetime


# def save_attendance(attendance_str):
#     # Split the input string into parts
#     parts = attendance_str.split("-")
#     name = parts[0]
#     matric_number = parts[1]
#     department = parts[2]
#     # Get the current date and time
#     now = datetime.now()
#     current_date = now.strftime("%Y-%m-%d")
#     current_time = now.strftime("%H:%M:%S")
#     # check if the file already exists
#     if os.path.exists("attendance.csv"):
#         with open("attendance.csv", 'r') as attendance_file:
#             attendance_reader = csv.reader(attendance_file)
#             # Check if the name and date is already in the file
#             for row in attendance_reader:
#                 if name == row[0] and current_date == row[3]:
#                     print(f'Attendance for {name} on {current_date} already recorded')
#                     return
#     else:
#         # Write the headers
#         with open("attendance.csv", 'w', newline='') as attendance_file:
#             attendance_writer = csv.writer(attendance_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             attendance_writer.writerow(["Name", "Matric Number", "Department", "Date", "Time"])
#     # Write the attendance data
#     with open("attendance.csv", 'a', newline='') as attendance_file:
#         attendance_writer = csv.writer(attendance_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         attendance_writer.writerow([name, matric_number, department, current_date, current_time])


# save_attendance("Nneji Ifeanyi Daniel-19 ENG02 077-Computer Engineering")

import numpy as np

inputs = [2.0, 3.0]
weights = [[0.2, -0.5], [-0.26, -0.27]]
bias = [2.0, 0.5]

output = np.dot(weights, inputs)# + bias
print(output)
