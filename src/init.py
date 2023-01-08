import os

import sqlite3
from app import db
from werkzeug.security import generate_password_hash


# create a function to make new directories from a list of strings
TYPES = ["video", "assignment", "documents"]
VALID_COURSE_CODES = ["501", "503", "515", "507", "511", "505", "519"]


def create_new_user(username, email, password, role):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    hashed_password = generate_password_hash(password, method="sha256")
    cur.execute(
        "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
        (username, email, hashed_password, role),
    )
    conn.commit()
    conn.close()
    print("Database Executed Successfully!")


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
    create_new_user("test", "test@gmail.com", "password", "student")
    create_new_user("test2", "test2@gmail.com", "password", "lecturer")


if __name__ == "__main__":
    main()
