"""
This script contains functions to initialize and populate the database for the application.

Functions:

    create_new_user: create a new user of the given type with the given attributes
    make_dirs: create directories for storing static files for each course
    main: initialize the database and create some example users (admin, lecturer and student)
"""


import os
import random
from typing import Union

from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db
from configurations.models import Admins, Lecturers, Students
from constants import *

load_dotenv()


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def create_new_user(type_of_user: str, **kwargs: Union[str, bool]) -> None:
    """Create a new user of the given type with the given attributes."""
    if type_of_user not in {"student", "lecturer", "admin"}:
        raise ValueError(f"Invalid user type: {type_of_user}")

    hashed_password = generate_password_hash(kwargs.pop("password"), method="sha256")

    try:
        if type_of_user == "student":
            user = Students(password=hashed_password, **kwargs)
            # print("Added new student to the database!")
        elif type_of_user == "lecturer":
            user = Lecturers(password=hashed_password, **kwargs)
            # print("Added new lecturer to the database!")
        else:
            user = Admins(password=hashed_password, **kwargs)
            # print("Added new admin to the database!")

        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        # print("User already exists.")
    finally:
        db.session.close()
        # print("Database session closed.")


def make_dirs():
    # loop through the list of strings
    for courses in VALID_COURSE_CODES:
        for dir in TYPES:
            # create a new directory for each string
            os.makedirs(f"./templates/static/courses/{courses}/{dir}", exist_ok=True)


def create_dummy_users():
    for i in range(20):
        # generate a random first and last name for the user
        first_name = random.choice(nigerian_first_names)
        last_name = random.choice(nigerian_last_names)
        full_name = f"{first_name} {last_name}"

        if i % 2 == 0:
            # create a new lecturer
            create_new_user(
                type_of_user="lecturer",
                username=full_name,
                email=f"{last_name.lower()}.{first_name.lower()}@abuad.com",
                password="password",
                role="lecturer",
            )
        else:
            # create a new student
            # matric_number = f"{random.choice(['18', '19'])}/ENG{random.randint(1, 8):02d}/{random.randint(1, 20):03d}"
            matric_number = (
                f"{random.choice(['18', '19'])}/ENG02/{random.randint(1, 20):03d}"
            )

            create_new_user(
                type_of_user="student",
                username=full_name,
                email=f"{last_name.lower()}.{first_name.lower()}@gmail.com",
                password="password",
                matric_number=matric_number,
                department="Computer Engineering",
                role="student",
            )


def create_admin():
    create_new_user(
        type_of_user="student",
        username="Nneji Ifeanyi Daniel",
        email=f"ifeanyinneji777@gmail.com",
        password="password",
        matric_number="19/ENG02/077",
        department="Computer Engineering",
        role="student",
    )
    create_new_user(
        type_of_user="admin",
        username=ADMIN_USERNAME,
        password=ADMIN_PASSWORD,
        role="admin",
    )


if __name__ == "__main__":
    db.create_all()
    print("Created Database!")
    create_admin()
    print("Created Admin!")
    create_dummy_users()
    ("Print created Users!")
    make_dirs()
    print("Created Directories")
    print("APPLICATION SETUP COMPLETE!..")
