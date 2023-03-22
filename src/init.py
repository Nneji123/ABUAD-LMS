"""
This script contains functions to initialize and populate the database for the application.

Functions:

    create_new_user: create a new user of the given type with the given attributes
    make_dirs: create directories for storing static files for each course
    main: initialize the database and create some example users (admin, lecturer and student)
"""


import os
from typing import Union

from dotenv import load_dotenv
from configurations.models import Admins, Lecturers, Students
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db
from constants import *

load_dotenv()


def create_new_user(type_of_user: str, **kwargs: Union[str, bool]) -> None:
    """Create a new user of the given type with the given attributes."""
    if type_of_user not in {"student", "lecturer", "admin"}:
        raise ValueError(f"Invalid user type: {type_of_user}")

    hashed_password = generate_password_hash(kwargs.pop("password"), method="sha256")

    try:
        if type_of_user == "student":
            user = Students(password=hashed_password, **kwargs)
            print("Added new student to the database!")
        elif type_of_user == "lecturer":
            user = Lecturers(password=hashed_password, **kwargs)
            print("Added new lecturer to the database!")
        else:
            user = Admins(password=hashed_password, **kwargs)
            print("Added new admin to the database!")

        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("User already exists.")
    finally:
        db.session.close()
        print("Database session closed.")


def make_dirs():
    # loop through the list of strings
    for courses in VALID_COURSE_CODES:
        for dir in TYPES:
            # create a new directory for each string
            os.makedirs(f"../templates/static/courses/{courses}/{dir}", exist_ok=True)
    print("Done")


def main():
    make_dirs()
    db.create_all()
    create_new_user(
        type_of_user="lecturer",
        username="OGUNLADE",
        email="ogunlade@gmail.com",
        password="password",
        role="lecturer",
    )
    create_new_user(
        type_of_user="student",
        username="NNEJI IFEANYI DANIEL",
        email="ifeanyinneji777@gmail.com",
        password="password",
        matric_number="19 ENG02 077",
        role="student",
    )
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    ADMIN_ROLE = os.getenv("ADMIN_ROLE")
    create_new_user(
        type_of_user="admin",
        username=ADMIN_USERNAME,
        password=ADMIN_PASSWORD,
        role=ADMIN_ROLE,
    )


if __name__ == "__main__":
    main()
