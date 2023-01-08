import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

conn = sqlite3.connect('database.db')
cur = conn.cursor()
username = "ify"
email = "ify@gmail.com"
password = "ify"
hashed_password = generate_password_hash(password, method="sha256")
role = "student"
id = 2
cur.execute("INSERT INTO users (id, username, email, password, role) VALUES (?, ?, ?, ?, ?)", (id, username, email, hashed_password, role))
cur.close()
print("Database Executed Successfully!")