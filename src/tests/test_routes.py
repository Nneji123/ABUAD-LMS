"""Application Route Tests"""

import sys

import pytest
from flask import Flask

sys.path.append("..")
from app import create_app


def test_login_student():
    name = Flask(__name__)

    name = create_app(name)

    client = name.test_client()

    # Send a POST request to the login route with form data
    response_student = client.post(
        "/login",
        data={"username": "19/ENG02/077", "password": "password", "role": "student"},
    )

    # Check that the response is a redirect to the student route
    assert response_student.status_code == 302
    assert response_student.headers["Location"] == "http://localhost/student"


def test_student():
    name = Flask(__name__)

    name = create_app(name)

    client = name.test_client()

    # Send a POST request to the login route with form data
    response_student = client.post(
        "/login",
        data={"username": "19/ENG02/077", "password": "password", "role": "student"},
    )

    response_student = client.get("/students/501")
    # Check that the response is a redirect to the student route
    assert response_student.status_code == 404


def test_login_lecturer():
    name = Flask(__name__)

    name = create_app(name)

    client = name.test_client()

    # Send a POST request to the login route with form data
    response_lecturer = client.post(
        "/login",
        data={
            "username": "Adebayo Adigun",
            "password": "password",
            "role": "lecturer",
        },
    )

    # Check that the response is a redirect to the student route
    assert response_lecturer.status_code == 302
    assert response_lecturer.headers["Location"] == "http://localhost/lecturer"


def test_reset_password_lecturer():
    name = Flask(__name__, template_folder="../templates")

    name = create_app(name)

    client = name.test_client()

    response_lecturer = client.get("reset_password")
    assert response_lecturer.status_code == 200

    # Send a POST request to the login route with form data
    response_lecturer = client.post(
        "/reset_password",
        data={"mail": "ifeanyinneji777@gmail.com"},
    )

    # Check that the response is a redirect to the student route
    assert response_lecturer.status_code == 200


def test_login_admin():
    name = Flask(__name__)

    name = create_app(name)

    client = name.test_client()

    # Send a POST request to the login route with form data
    response_admin = client.post(
        "/login",
        data={"username": "admin", "password": "admin", "role": "admin"},
    )

    # Check that the response is a redirect to the student route
    assert response_admin.status_code == 302
    assert response_admin.headers["Location"] == "http://localhost/admin/"


def test_logout():
    name = Flask(__name__)

    name = create_app(name)

    client = name.test_client()

    # Send a POST request to the login route with form data
    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin", "role": "admin"},
    )
    # Act: Access the logout route.
    response = client.get("/logout")

    # Assert: Check that the user is redirected to the login page.
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/login?success=logged-out"


def test_index():
    name = Flask(__name__)

    name = create_app(name)

    client = name.test_client()

    response = client.get("/")

    # Check that the response is a redirect to the student route
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/login"


def test_lecturer_record_attendance_route():
    name = Flask(__name__, template_folder="../templates")
    name = create_app(name)
    client = name.test_client()
    response_lecturer = client.post(
        "/login",
        data={
            "username": "Afolabi Gbadamosi",
            "password": "password",
            "role": "lecturer",
        },
    )
    response_lecturer = client.get("/lecturer/record_attendance/501")
    assert response_lecturer.status_code == 200


def test_lecturer_view_student_route():
    name = Flask(__name__, template_folder="../templates")
    name = create_app(name)
    client = name.test_client()
    response_lecturer = client.post(
        "/login",
        data={
            "username": "Afolabi Gbadamosi",
            "password": "password",
            "role": "lecturer",
        },
    )
    response_lecturer = client.get("/lecturer/view_students/501")
    assert response_lecturer.status_code == 200


def test_lecturer_register_student_route():
    name = Flask(__name__, template_folder="../templates")
    name = create_app(name)
    client = name.test_client()
    response_lecturer = client.post(
        "/login",
        data={
            "username": "Afolabi Gbadamosi",
            "password": "password",
            "role": "lecturer",
        },
    )
    response_lecturer = client.get("/lecturer/register_students/501")
    assert response_lecturer.status_code == 404
