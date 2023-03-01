<p align="center">
  <img src="./src/templates/static/img/logo.png" alt="ABUAD LMS Logo", width="120", height="120">
</p>
<h1 align="center">ABUAD LMS (Learning Management System)</h1>
<div align="center">

[![Language](https://img.shields.io/badge/Python-darkblue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Framework](https://img.shields.io/badge/Flask-darkgreen.svg?style=flat&logo=flask&logoColor=white)](https://github.com/Nneji123/abuad-lms)
[![HTML](https://img.shields.io/badge/HTML-black.svg?style=flat&logo=html5&logoColor=white)](https://github.com/Nneji123/abuad-lms)
[![CSS](https://img.shields.io/badge/CSS-blue.svg?style=flat&logo=css3&logoColor=white)](https://github.com/Nneji123/abuad-lms)
[![Javascript](https://img.shields.io/badge/Javascript-yellow.svg?style=flat&logo=javascript&logoColor=white)](https://github.com/Nneji123/abuad-lms)
[![Postgres](https://img.shields.io/badge/Postgres-darkblue.svg?style=flat&logo=postgres&logoColor=white)](https://github.com/Nneji123/abuad-lms)
![hosted](https://img.shields.io/badge/Railway-430098?style=flat&logo=railway&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white)
[![Gitpod](https://img.shields.io/badge/Gitpod-orange?style=flat&logo=gitpod&logoColor=white)](https://gitpod.io/#https://github.com/Nneji123/abuad-lms)
![reposize](https://img.shields.io/github/repo-size/Nneji123/abuad-lms)

</div>

> ABUAD LMS (Learning Management System) is a web application that is designed to provide students and teachers with access to high-quality educational resources, facilitate online learning, and foster collaboration and communication within the ABUAD community. It is a part of the ABUAD Smart School Environment Project carried out by [Ifeanyi Nneji](https://github.com/Nneji123) and [Ogunkuade Ayobamidele](https://github.com/devXcant).


> Visit the [ABUAD Smart School Environment](https://github.com/Nneji123/ABUAD-SMART-SCHOOL-ENVIRONMENT) Repository to learn more details about other aspects of the project.

# :bookmark_tabs: Table Of Contents
- [:bookmark\_tabs: Table Of Contents](#bookmark_tabs-table-of-contents)
- [:wave: Introduction](#wave-introduction)
- [:bulb: Motivation](#bulb-motivation)
- [:star2: Features](#star2-features)
- [:file\_folder: Repository Structure](#file_folder-repository-structure)
- [:wrench: Tools Used](#wrench-tools-used)
- [:chart\_with\_upwards\_trend: Flowchart](#chart_with_upwards_trend-flowchart)
- [:bar\_chart: Use Case Diagram](#bar_chart-use-case-diagram)
- [:camera: Screenshots](#camera-screenshots)
- [:movie\_camera: Demo Videos](#movie_camera-demo-videos)
- [:rocket: How to Run ABUAD LMS](#rocket-how-to-run-abuad-lms)
  - [:whale: How to run in Docker and Docker Compose](#whale-how-to-run-in-docker-and-docker-compose)
- [:cloud: Deployment](#cloud-deployment)
- [:book: References](#book-references)
- [:page\_with\_curl: License](#page_with_curl-license)


# :wave: Introduction
ABUAD LMS (Abuad Learning Management System) is a part of the Abuad Smart School Environment. ABUAD LMS is an innovative digital platform that has been developed to support learning and teaching at Afe Babalola University Ado-Ekiti (ABUAD) in Nigeria. This platform is designed to enhance the educational experience of students and teachers alike, by providing them with access to a wide range of digital tools and resources that can be used to support teaching and learning activities.

# :bulb: Motivation

The development of the ABUAD LMS was driven by the need to create a more effective and efficient learning environment that leverages digital technology. With the ABUAD LMS, students and teachers can collaborate and communicate more effectively, and learning can take place anytime, anywhere. The platform provides lecturers with an easy-to-use interface for uploading course content, such as videos, documents, and assignments, which can be accessed by students on demand.



# :star2: Features 
The ABUAD LMS is an innovative digital platform that offers a wide range of features for both students and lecturers. Here are some of the key features of the ABUAD LMS:

For Students:

- Access to Course Documents: Students can easily access all the course documents uploaded by their lecturers, including lecture notes, slides, and other supplementary materials.
- View Assignments: Students can view all the assignments given by their lecturers, including due dates and instructions.
- View Attendance Records: Students can view their attendance records for each course, including the dates they attended and the number of hours.
- View Lecture Videos: Students can watch lecture videos uploaded by their lecturers, which can be accessed on demand.

For Lecturers:

- Upload Course Documents: Lecturers can upload course materials, such as lecture notes, slides, and other supplementary materials, to the ABUAD LMS for their students to access.
- Upload Lecture Videos: Lecturers can upload videos of their lectures to the ABUAD LMS, which can be accessed by their students on demand.
- Record Attendance: Lecturers can record attendance using the state-of-the-art **facial recognition system**, which eliminates the need for manual attendance taking.
- View Attendance Records: Lecturers can view the attendance records for each course they teach, which can help them keep track of student attendance and monitor progress.

For Admins:

In addition to the features available to students and lecturers, the ABUAD LMS also offers a range of features for administrators, which include:

- Manage Users: Administrators can manage users of the ABUAD LMS, including students and lecturers, by adding new users, updating user information, and removing users who are no longer part of the ABUAD community.
- Course Management: Administrators can manage courses offered by the university, including creating new courses, updating course information, and removing courses that are no longer offered.
- Monitor Attendance: Administrators can monitor attendance records for all courses and students, helping to ensure that students are attending classes regularly and meeting attendance requirements.
- System Maintenance: Administrators can perform system maintenance tasks, such as backing up data, updating software, and troubleshooting issues that arise with the ABUAD LMS.

# :file_folder: Repository Structure
```
|-- Dockerfile
|-- LICENSE.md
|-- README.md
|-- docker-compose.yml
|-- instance
|-- render.yaml
|-- requirements.txt
|-- screens
`-- src
    |-- app.py
    |-- config.py
    |-- constants.py
    |-- database.db
    |-- index.py
    |-- init.py
    |-- instance
    |-- lecturer.py
    |-- login.py
    |-- logout.py
    |-- models.py
    |-- saved_model
    |   |-- deploy.prototxt.txt
    |   `-- res10_300x300_ssd_iter_140000.caffemodel
    |-- student.py
    |-- templates
    |   |-- admin
    |   |   `-- index.html
    |   |-- pages
    |   |   |-- attendance.html
    |   |   |-- coe.html
    |   |   |-- course_base.html
    |   |   |-- error.html
    |   |   |-- lecturer.html
    |   |   |-- login.html
    |   |   |-- record_attendance.html
    |   |   |-- register.html
    |   |   `-- student.html
    |   |-- reset_password
    |   |   |-- base.html
    |   |   |-- email.html
    |   |   |-- index.html
    |   |   `-- reset.html
    |   `-- static
    |       |-- courses
    |       |   `-- logo.png
    |       |-- main.css
    |       `-- style.css
    `-- utils.py
```

# :wrench: Tools Used 
 Some of the key tools used in the development of ABUAD LMS are:

1. HTML: HTML was used to develop the structure and content of the web pages in ABUAD LMS.

2. CSS: CSS was used to style the web pages and enhance the visual appeal of ABUAD LMS.

3. JavaScript: JavaScript was used to add dynamic behavior to the web pages and provide a better user experience.

4. Datatables: Datatables is a plugin used in ABUAD LMS to enable the display of data in a tabular format with advanced features such as searching, filtering, and sorting.

5. Bootstrap: Bootstrap is a front-end framework used in ABUAD LMS to ensure a responsive design and improve the overall look and feel of the application.

6. Python: Python is a programming language used in the development of ABUAD LMS.

7. Flask: Flask is a micro web framework used in ABUAD LMS to develop the web application.

8. Postgres: Postgres is an open-source relational database management system used in ABUAD LMS to store and manage data.

9. SQLite: SQLite is a lightweight relational database management system used in ABUAD LMS for development and testing purposes.

10. Flask_Admin: Flask_Admin is a plugin used in ABUAD LMS to provide a user-friendly interface for managing the database.

11. Flask_Mail: Flask_Mail is a plugin used in ABUAD LMS to enable email functionality such as reset password features.

12. Facial Recognition with Dlib: This is used in the facial recognition attendance system.


# :chart_with_upwards_trend: Flowchart
<p align="center">
  <img src="./screens/flowchart.png" alt="Flow Chart", width="700", height="">
</p>

# :bar_chart: Use Case Diagram
<p align="center">
  <img src="./screens/usecasediagram.png" alt="Use Case Diagram", width="500", height="500">
</p>

# :camera: Screenshots
<details>
<summary><strong>Lecturer Page Screenshots</strong></summary>
<br> 

| Screenshot                                                      | Description                                      |
| --------------------------------------------------------------- | ------------------------------------------------ |
| ![Lecturer Dashboard](./screens/lecturer/lecturer_screens0.png) | The lecturer homepage and dashboard              |
| ![Course Materials](./screens/lecturer/lecturer_screens1.png)   | Available list of courses.                       |
| ![Attendance Records](./screens/lecturer/lecturer_screens2.png) | Successful File Upload Pop Up Message.           |
| ![Upload Assignment](./screens/lecturer/lecturer_screens3.png)  | Register Student Page.                           |
| ![View Assignments](./screens/lecturer/lecturer_screens4.png)   | Facial Recognition Attendance Page.              |
| ![Discussion Forum](./screens/lecturer/lecturer_screens5.png)   | Attendance Report Page.                          |
| ![Grades Management](./screens/lecturer/lecturer_screens6.png)  | Search for Attendance record by particular date. |
</details>


<details>
<summary><strong>Student Page Screenshots</strong></summary>
<br>

| Screenshot                                                       | Description                                    |
| ---------------------------------------------------------------- | ---------------------------------------------- |
| ![Student Dashboard](./screens/student/student_screens0.png)     | Student Homepage                               |
| ![Course Materials](./screens/student/student_screens1.png)      | List of courses available to students.         |
| ![Assignment Submission](./screens/student/student_screens2.png) | Course Homepage                                |
| ![Grades](./screens/student/student_screens3.png)                | List of course documents.                      |
| ![Attendance Record](./screens/lecturer/lecturer_screens4.png)   | View Course Document with built in PDF Viewer. |
| ![Announcements](./screens/student/student_screens5.png)         | List of available videos for the course.       |
| ![Course Schedule](./screens/student/student_screens6.png)       | Play videos with built in video player.        |
| ![Account Settings](./screens/student/student_screens7.png)      | View attendance record for course.             |
</details>

<details>
<summary><strong>Admin Page Screenshots</strong></summary>
<br>


| Screenshot                                                     | Description                    |
| -------------------------------------------------------------- | ------------------------------ |
| ![Admin Dashboard](./screens/admin/admin_screens0.png)         | Admin dashboard.               |
| ![User Management](./screens/admin/admin_screens1.png)         | View registered Students.      |
| ![Course Management](./screens/admin/admin_screens2.png)       | View registered Lecturers.     |
| ![Attendance Monitoring](./screens/admin/admin_screens3.png)   | View registered admins.        |
| ![Announcement Management](./screens/admin/admin_screens4.png) | Create new students/lecturers. |
| ![System Settings](./screens/admin/admin_screens5.png)         | Edit and update user details.  |
</details>


<details>
<summary><strong>Password Reset Screenshots</strong></summary>
<br>

| Screenshot                                                                | Description                              |
| ------------------------------------------------------------------------- | ---------------------------------------- |
| ![Password Reset Request](./screens/password/Screenshot%20(387).png)      | Reset password page.                     |
| ![Password Reset Email](./screens/password/Screenshot%20(388).png)        | Password reset email sent successfully.  |
| ![Password Reset Form](./screens/password/Screenshot%20(389).png)         | Received email page.                     |
| ![Password Reset Confirmation](./screens/password/Screenshot%20(390).png) | Reset password button.                   |
| ![Password Reset Error](./screens/password/Screenshot%20(391).png)        | Change password page.                    |
| ![Password Reset Success](./screens/password/Screenshot%20(392).png)      | Successful password change notification. |
</details>


# :movie_camera: Demo Videos
# :rocket: How to Run ABUAD LMS 

To run the ABUAD LMS application using Python, follow these steps:

1. Clone the repository to your computer.
```  
git clone https://github.com/Nneji123/ABUAD-LMS.git
cd ABUAD-LMS
```

1. Create and activate your virtual environment. For Windows users, you can activate your environment by running the following command in your terminal:

```bash
python -m venv env
source env\Scripts\activate
```

3. Set the environment variables required for the application. Create a file named `.env` or edit the `.env.example` and add the following environment variables:

```bash
# DATABASE AND SERVER CONFIG
POSTGRES = "postgresql://postgres:password@url:port/database" # POST SERVER
SQLITE = "sqlite:///../database.db" # LOCATION OF SQLITE DATABASE
SERVER_NAME="http://127.0.0.1:3000" # CHANGE THIS TO YOUR PRODUCTION SERVER LINK
SERVER_MODE="DEV" # CHANGE TO `PROD` TO ENABLE PRODUCTION READY SETTINGS
SERIAL="secret" # FOR GENERATING EMAIL HASHCODE

# ADMIN DETAILS
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
ADMIN_ROLE = "admin"
IS_ADMIN = True

# DEV SERVER CONFIG
DEV_MAIL_SERVER="sandbox.smtp.mailtrap.io"
DEV_MAIL_PORT=2525
DEV_MAIL_USERNAME=""
DEV_MAIL_PASSWORD=""
DEV_SECRET_KEY=""
DEV_SENDER_EMAIL="" # SHOULD BE THE SAME AS DEV_MAIL_USERNAME

# PROD SERVER CONFIG
PROD_MAIL_SERVER= "smtp.gmail.com"
PROD_MAIL_PORT= 465
PROD_MAIL_USERNAME= ""
PROD_MAIL_PASSWORD= ""
PORD_SECRET_KEY=""
PROD_SENDER_EMAIL=""
```

Note that you should replace the values of the environment variables with your own server and database settings, as well as your own email credentials.

4. Install the required Python packages by running the following command in your terminal:


> `pip install -r requirements.txt`

5. Change your directory to the src directory:
> cd src

6. Initialize the local database by running the following command in your terminal:

> `python init.py`

7. Finally, run the application by running the following command in your terminal:

> `python app.py`
Once the application is running, you can visit it in your web browser by going to http://localhost:3000/.



## :whale: How to run in Docker and Docker Compose
To run the application using Docker, follow these steps:

1. Make sure Docker is installed on your machine.
2. Clone the project repository and navigate to the project directory.
3. Create a file called `.env` in the project root directory and add the required environment variables.
4. Build the Docker image using the following command: 
   
   `docker build -t abuad-lms .`
5. Run the Docker container using the following command: `docker run --env-file .env -p 3000:3000 abuad-lms`


To run the application using Docker Compose, follow these steps:

1. Make sure Docker and Docker Compose are installed on your machine.
2. Clone the project repository and navigate to the project directory.
3. Create a file called .env in the project root directory and add the required environment variables.
4. Build and start the Docker container using the following command: `docker-compose up --build`

These steps will start the application in a Docker container, which can be accessed by visiting http://localhost:3000 in a web browser.


# :cloud: Deployment
To deploy the application using the Railway or Render button, follow these steps:

1. Click on the Railway or Render button in the repository to open the deployment platform.

<div align="center">

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/Fr7c3B?referralCode=ZYOf2M)
[![Deploy on Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

</div>



2. Sign up or log in to the deployment platform.
3. Connect your GitHub account to the deployment platform.
4. Choose the repository where the application code is located.
5. Configure the deployment settings, such as the name of the application, the deployment region, and the deployment type (e.g., Docker container or static site).
6. Deploy the application by clicking on the "Deploy" button.
7. Wait for the deployment process to finish. Once it's done, the application will be available at the URL provided by the deployment platform.

> Note that the specific steps and options may vary depending on the deployment platform used. It's recommended to check the documentation and tutorials provided by the platform for more detailed instructions on how to deploy the application.
# :book: References
References:

1. Abuad LMS. (2023). Retrieved from https://github.com/abuad/lms
2. Face Recognition Library. (2023). Retrieved from https://github.com/ageitgey/face_recognition
3. Flask. (2023). Retrieved from https://flask.palletsprojects.com/en/2.1.x/
4. Flask-Admin. (2023). Retrieved from https://flask-admin.readthedocs.io/en/latest/
5. SQLAlchemy. (2023). Retrieved from https://www.sqlalchemy.org/
6. Bootstrap. (2023). Retrieved from https://getbootstrap.com/
7. OpenCV. (2023). Retrieved from https://opencv.org/
8. Akinremi, F. (2020). Building a Simple Flask Web Application with Docker and Kubernetes. Medium. Retrieved from https://medium.com/analytics-vidhya/building-a-simple-flask-web-application-with-docker-and-kubernetes-58439b0c7d3a
# :page_with_curl: License
[MIT](./LICENSE.md)

