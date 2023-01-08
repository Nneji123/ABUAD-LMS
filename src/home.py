# from io import BytesIO

# import numpy as np
# import os
# from flask import Blueprint, redirect, render_template, request, url_for, flash
# from flask_login import LoginManager, current_user, login_required
# from models import Users, db
# from werkzeug.utils import secure_filename

# home = Blueprint("home", __name__, template_folder="./frontend")
# login_manager = LoginManager()
# login_manager.init_app(home)


# @home.route("/home", methods=["GET"])
# @login_required
# def show():
#     return render_template("home.html")


# @home.route("/upload", methods=["POST"])
# @login_required
# def upload_video():
#     # Get the file from the POST request
#     file = request.files['file']
#     # Check if the file is not empty
#     if file.filename != '':
#         # Save the file to the desired location
#         # get the file name in the form of a string
#         file_name = str(file.filename)
#         if '501' in file_name:
#             # save the file to the desired location
#             file.save(f"static/courses/501/{file.filename}")
#             flash('Video uploaded successfully!')
#             return redirect(url_for("home.show"))

#         elif '503' in file_name:
#             file.save(f"static/courses/503/{file.filename}")
#             return 'Video saved successfully!'
        
#         elif '515' in file_name:
#             file.save(f"static/courses/515/{file.filename}")
#             return 'Video saved successfully!'
        
#         elif '507' in file_name:
#             file.save(f"static/courses/507/{file.filename}")
#             return 'Video saved successfully!'
        
#         elif '511' in file_name:
#             file.save(f"static/courses/511/{file.filename}")
#             return 'Video saved successfully!'
        
#         elif '505' in file_name:
#             file.save(f"static/courses/505/{file.filename}")
#             return 'Video saved successfully!'
        
#         elif '519' in file_name:
#             file.save(f"static/courses/519/{file.filename}")
            
#             return 'Video saved successfully!'
#         # file.save(secure_filename(f".static/courses/file.filename))
#         # return 'Video saved successfully!'
#     return 'No file selected!'

#     return render_template("home", e = "course uploaded successfully")
