import datetime
import os

from flask import Blueprint, flash, redirect, render_template, request, url_for, Response
from flask_login import LoginManager, login_required
from PIL import Image
import cv2

from utils import gen, gen_frames

lecturer = Blueprint("lecturer", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(lecturer)

global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0


#Load pretrained face detection model    
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')


now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M-%S")
VALID_COURSE_CODES = ["501", "503", "515", "507", "511", "505", "519"]
VIDEO_EXTENSIONS = [
    "mp4",
    "mkv",
    "avi",
    "mov",
    "flv",
    "wmv",
    "webm",
    "mpeg",
    "mpg",
    "m4v",
    "3gp",
    "3g2",
    "f4v",
    "f4p",
    "f4a",
    "f4b",
]
DOC_EXTENSIONS = [
    "pdf",
    "docx",
    "doc",
    "csv",
]
ASSIGNMENT_EXTENSIONS = [
    "pdf",
    "docx",
    "doc",
    "csv",
    "txt",
    "pptx",
    "ppt",
    "xlsx",
    "xls",
    "zip",
    "rar",
    "7z",
    "tar",
    "gz",
    "bz2",
    "xz",
    "iso",
    "mp4",
    "mkv",
    "avi",
    "mov",
    "flv",
    "wmv",
    "webm",
    "mpeg",
    "mpg",
    "m4v",
    "3gp",
    "3g2",
    "f4v",
    "f4p",
    "f4a",
    "f4b",
]
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@lecturer.route("/lecturer", methods=["GET"])
# @login_required
def show():
    return render_template("lecturer.html")


@lecturer.route("/upload", methods=["POST"])
@login_required
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



### Take Attendance
@lecturer.route('/recognition')
def take_attendance():
    return render_template('takeattendance.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@lecturer.route('/detect_face_feed')
def video_feeds():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




#### Registering Students


@lecturer.route('/register_students')
def index():
    return render_template('registerattendance.html')
    
    
@lecturer.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@lecturer.route('/register_student',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        names = request.form.get('name')
        matric = request.form.get('matric')
        dept = request.form.get('dept')
        print(names,matric,dept)
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
            camera = cv2.VideoCapture(0)
            m, img = camera.read()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            filenamess = f"{names}-{str(matric)}-{dept}.jpg".replace("/", " ")
            im_pil.save(f"./shots/{filenamess}")
            print("done")
        elif request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                switch=1
                          
    elif request.method=='GET':
        return render_template('registerattendance.html')
    return render_template('registerattendance.html')



