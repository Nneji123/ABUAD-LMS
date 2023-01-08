import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# conn = sqlite3.connect('database.db')

def create_new_student(username, email, password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # username = "ifeanyi"
    # email = "ify@gmail.com"
    # password = "linda321"
    hashed_password = generate_password_hash(password, method="sha256")
    cur.execute("INSERT INTO students (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()
    conn.close()
    print("Database Executed Successfully!")
    
def create_new_lecturer(username, email, password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # username = "ifeanyi"
    # email = "ify@gmail.com"
    # password = "linda321"
    hashed_password = generate_password_hash(password, method="sha256")
    cur.execute("INSERT INTO lecturers (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()
    conn.close()
    print("Database Executed Successfully!")
    
def create_new_user(username, email, password, role):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    # username = "ifeanyi"
    # email = "ify@gmail.com"
    # password = "linda321"
    hashed_password = generate_password_hash(password, method="sha256")
    cur.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", (username, email, hashed_password, role))
    conn.commit()
    conn.close()
    print("Database Executed Successfully!")
    
from app import db

def main():
    db.create_all()
    create_new_user("test", "test@gmail.com", "linda321", "student")
    # create_new_student("ifeanyi2", "ifeanyinneji77@gmail.com", "linda321")
    create_new_user("test2", "test2@gmail.com", "linda321", "lecturer")
    
if __name__ == "__main__":
    main()


