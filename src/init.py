import os
import sqlalchemy

from werkzeug.security import generate_password_hash

from app import db
from models import Students, Lecturers, Admins

# create a function to make new directories from a list of strings
TYPES = ["video", "assignment", "documents"]
VALID_COURSE_CODES = ["501", "503", "515", "507", "511", "505", "519"]


def create_new_user(
    type_of_user: str = "",
    username: str = "",
    email: str = "",
    password: str = "",
    matric_number: str = "",
    role: str = "",
    is_admin: bool = False,
):
    hashed_password = generate_password_hash(password, method="sha256")
    if type_of_user == "student":
        try:
            new_user = Students(
                username=username,
                email=email,
                password=hashed_password,
                matric_number=matric_number,
                role=role,
            )
            print("Added new Student to the Database!")
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            print("User Already Exists")

        finally:
            db.session.close()
            print("Reverted Database")
    elif type_of_user == "lecturer":
        try:
            new_user = Lecturers(
                username=username,
                email=email,
                password=hashed_password,
                role=role,
            )
            print("Added new Lecturer to the Database!")
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            print("User Already Exists")

        finally:
            db.session.close()
            print("Reverted Database")
    elif type_of_user == "admin":
        try:
            new_user = Admins(
                username=username,
                password=hashed_password,
                role=role,
                is_admin=is_admin,
            )
            print("Added new Admin to the Database!")
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            print("User Already Exists")

        finally:
            db.session.close()
            print("Reverted Database")
    else:
        print("Please input the type of user!\n1.Student\n2.Lecturer\n3.Admin ")


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
        type_of_user="admin", username="admin", password="admin", role="admin", is_admin=True
    )


if __name__ == "__main__":
    main()
