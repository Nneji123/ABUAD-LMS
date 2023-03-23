from flask import Flask
import pytest

import sys

sys.path.append("..")
from app import create_app

name = Flask(__name__)

name = create_app(name)


def test_login_student():
    client = name.test_client()

    # Send a POST request to the login route with form data
    response_student = client.post(
        "/login",
        data={"username": "19/ENG02/077", "password": "password", "role": "student"},
    )

    # Check that the response is a redirect to the student route
    assert response_student.status_code == 302
    assert response_student.headers["Location"] == "http://localhost/student"


def test_login_lecturer():
    client = name.test_client()

    # Send a POST request to the login route with form data
    response_lecturer = client.post(
        "/login",
        data={
            "username": "Afolabi Gbadamosi",
            "password": "password",
            "role": "lecturer",
        },
    )

    # Check that the response is a redirect to the student route
    assert response_lecturer.status_code == 302
    assert response_lecturer.headers["Location"] == "http://localhost/lecturer"


def test_login_admin():
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
    client = name.test_client()

    response = client.get("/")

    # Check that the response is a redirect to the student route
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/login"
