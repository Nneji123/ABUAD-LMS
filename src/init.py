import os
from typing import Union

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db
from constants import *
from models import Admins, Lecturers, Students


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
            os.makedirs(f"./frontend/static/courses/{courses}/{dir}", exist_ok=True)
    print("Done")


def main():
    make_dirs()
    db.create_all()
    # create_new_user("test", "test@gmail.com", "password", "student", False)
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
    create_new_user(
        type_of_user="admin",
        username="admin",
        password="admin",
        role="admin",
        is_admin=True,
    )


if __name__ == "__main__":
    main()
