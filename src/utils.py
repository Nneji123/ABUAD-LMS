import datetime
import os
import csv
import face_recognition
import numpy as np
import cv2


global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0


#Load pretrained face detection model    
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

def gen():
    global capture,  out, face
    IMAGE_FILES = []
    filename = []
    dir_path = './shots'

    for imagess in os.listdir(dir_path):
        img_path = os.path.join(dir_path, imagess)
        img_path = face_recognition.load_image_file(img_path)  # reading image and append to list
        IMAGE_FILES.append(img_path)
        filename.append(imagess.split(".", 1)[0])

    def encoding_img(IMAGE_FILES):
        encodeList = []
        for img in IMAGE_FILES:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            except Exception as e:
                print(e)
        return encodeList

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



    encodeListknown = encoding_img(IMAGE_FILES)

    cap = cv2.VideoCapture(0)

    while True: 
        success, img = cap.read()
        imgc = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        # converting image to RGB from BGR
        imgc = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        fasescurrent = face_recognition.face_locations(imgc)
        encode_fasescurrent = face_recognition.face_encodings(imgc, fasescurrent)

        # faceloc- one by one it grab one face location from fasescurrent
        # than encodeFace grab encoding from encode_fasescurrent
        # we want them all in same loop so we are using zip
        for encodeFace, faceloc in zip(encode_fasescurrent, fasescurrent):
            matches_face = face_recognition.compare_faces(encodeListknown, encodeFace)
            face_distence = face_recognition.face_distance(encodeListknown, encodeFace)
            # print(face_distence)
            # finding minimum distence index that will return best match
            matchindex = np.argmin(face_distence)

            if matches_face[matchindex]:
                name = filename[matchindex].upper()
                # print(name)
                y1, x2, y2, x1 = faceloc
                # multiply locations by 4 because we above we reduced our webcam input image by 0.25
                # y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), 2, cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                save_attendance(name)  # taking name for attendence function above

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27:
            break


def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame, frame
    while True:
        camera = cv2.VideoCapture(0)
        success, frame = camera.read() 
        if success:   
            if(capture):
                capture=0    
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass 
        else:
            pass