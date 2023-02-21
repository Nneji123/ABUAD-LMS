import os 
import csv

import csv
import os

def count_name_in_files(directory_path, name):
    count = 0
    num_files = 0
    
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename.endswith('.csv'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if row and row[0] == name:
                            count += 1
                num_files += 1
    
    if num_files == 0:
        return 0
        
    message = f"{name}'s Attendance for this course is " + f"{str(count / num_files * 100)}% \nYou are eligible to write your exam!"
    
    return message




print(count_name_in_files("./frontend/static/attendance/", "NNEJI IFEANYI DANIEL"))