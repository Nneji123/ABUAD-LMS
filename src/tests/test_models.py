import sys
from datetime import datetime, timedelta

import pytest
from werkzeug.security import generate_password_hash

sys.path.append("..")

from app import create_app, db
from configurations.models import Admins, Announcements, Lecturers, Students
from utils import (base64_to_image, count_name_in_files, send_mail,
                   validate_matric_number)


@pytest.fixture(scope="module")
def new_announcement():
    lecturer = Lecturers(
        username="test_lecturer",
        email="test_lecturer@abuad.com",
        password="password",
        role="lecturer",
    )
    db.session.add(lecturer)
    db.session.commit()

    announcement = Announcements(lecturer_id=lecturer.id, message="Test announcement")
    return announcement


def test_announcement_creation(new_announcement):
    assert new_announcement.id is not None
    assert new_announcement.lecturer_id is not None
    assert new_announcement.message == "Test announcement"
    assert new_announcement.created_at is not None


def test_time_diff_property(new_announcement):
    # Set created_at to 3 days ago
    new_announcement.created_at = datetime.utcnow() - timedelta(days=3)
    assert new_announcement.time_diff == "Posted 3 days ago"

    # Set created_at to yesterday
    new_announcement.created_at = datetime.utcnow() - timedelta(days=1)
    assert new_announcement.time_diff == "Posted yesterday"

    # Set created_at to today
    new_announcement.created_at = datetime.utcnow()
    assert new_announcement.time_diff == "Posted today"


def test_student_creation():
    password = generate_password_hash("password", method="sha256")
    student = Students(
        username="john_doe",
        email="john_doe@example.com",
        password=password,
        matric_number="MAT123456",
        department="Computer Science",
        role="student",
    )
    db.session.add(student)
    db.session.commit()
    assert student.id is not None


def test_lecturer_creation():
    password = generate_password_hash("password", method="sha256")

    lecturer = Lecturers(
        username="jane_doe",
        email="jane_doe@example.com",
        password=password,
        role="lecturer",
    )
    db.session.add(lecturer)
    db.session.commit()
    assert lecturer.id is not None


def test_check_password():
    password = generate_password_hash("password", method="sha256")

    student = Students(
        username="john_doe",
        email="john_doe@example.com",
        password=password,
        matric_number="19/ENG06/098",
        department="Computer Engineering",
        role="student",
    )
    db.session.add(student)
    db.session.commit()
    assert student.check_password("password") == True
