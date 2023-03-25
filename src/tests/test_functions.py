"""Functional Tests"""

import base64
import sys
from unittest.mock import Mock, patch

import numpy as np
import pytest
from flask import Flask
from flask_mail import Message

sys.path.append("..")

from app import create_app
from utils import (base64_to_image, count_name_in_files, send_mail,
                   validate_matric_number)


def test_validate_matric_number():
    # Valid matric number
    assert validate_matric_number("18/ABC12/345") == True
    assert validate_matric_number("19/XYZ23/456") == True
    assert validate_matric_number("22/GHI45/678") == True

    # Invalid matric number
    assert validate_matric_number("20ss/abc12/345") == False
    assert validate_matric_number("21/XYZ23/") == False
    assert validate_matric_number("23/GHI45/6789") == False


@pytest.fixture()
def mock_email():
    with patch("flask_mail.Message.send") as mock_send:
        yield mock_send


def test_send_mail():
    to = "test@example.com"
    template = "test_template.html"
    subject = "Test Subject"
    link = "https://example.com/test_link"
    username = "Test User"
    kwargs = {"variable1": "value1", "variable2": "value2"}
    expected_html = "<html><body>Test HTML</body></html>"
    from flask import Flask

    name = Flask(__name__, template_folder="./templates")
    with create_app(name).app_context():
        with patch(
            "configurations.extensions.email.render_template",
            return_value=expected_html,
        ):
            html = send_mail(to, template, subject, link, username, **kwargs)
            assert html == None


@pytest.fixture
def test_base64_string():
    with open("test_image.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return f"data:image/jpeg;base64,{encoded_string.decode('utf-8')}"


def test_base64_to_image(test_base64_string):
    image = base64_to_image(test_base64_string)
    assert isinstance(image, np.ndarray)
    assert image.shape[2] == 3  # RGB image
    assert image.dtype == np.uint8


def test_count_names_in_files():
    assert (
        count_name_in_files("./templates/static/courses/", "Unknown")
        == "No attendance data available for this course!"
    )

    assert (
        count_name_in_files("test_files", "James")
        == "No attendance data available for this course!"
    )
    assert (
        count_name_in_files("test_files", "John")
        == "No attendance data available for this course!"
    )
    assert (
        count_name_in_files("invalid_directory_path", "John")
        == "No attendance data available for this course!"
    )
    assert (
        count_name_in_files("test_files", "")
        == "No attendance data available for this course!"
    )
    assert (
        count_name_in_files("test_files", 123)
        == "No attendance data available for this course!"
    )
