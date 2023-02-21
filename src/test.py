import csv
import os
import pandas as pd

def count_name_in_files(directory_path):
    student_attendance = {}

    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    name = row["Name"]
                    matric_number = row["Matric Number"]
                    department = row["Department"]

                    if name not in student_attendance:
                        student_attendance[name] = {
                            "Matric Number": matric_number,
                            "Department": department,
                            "Attendance": 0
                        }

                    student_attendance[name]["Attendance"] += 1

    data = []
    for name, attendance_data in student_attendance.items():
        total_classes = len(os.listdir(directory_path))
        attendance_percentage = attendance_data["Attendance"] / total_classes * 100
        data.append({
            "Name": name,
            "Matric Number": attendance_data["Matric Number"],
            "Department": attendance_data["Department"],
            "Attendance Percentage": attendance_percentage
        })

    df = pd.DataFrame(data, columns=["Name", "Matric Number", "Department", "Attendance Percentage"])
    df.set_index("Name", inplace=True)
    df.to_csv("total_attendance.csv")
    return df


print(count_name_in_files("./frontend/static/courses/501/attendance"))