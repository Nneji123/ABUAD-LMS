import os

import sqlalchemy
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager

from admin import admin
from index import index
from lecturer import lecturer
from login import login
from logout import logout
from models import Users, db
from register import register
from student import student

load_dotenv()


app = Flask(__name__, static_folder="./frontend/static")


POSTGRES = os.getenv("POSTGRES")
SQLITE = os.getenv("SQLITE")
DATABASE_MODE = os.getenv("DATABASE_MODE")


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if DATABASE_MODE == "postgres":
    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLITE


login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(lecturer)
app.register_blueprint(student)
app.register_blueprint(admin)


@login_manager.user_loader
def load_user(user_id):
    try:

        return Users.query.get(int(user_id))  # Lecturers.query.get(int(user_id))
    except (sqlalchemy.exc.OperationalError) as e:
        return render_template("error.html", e="Database not found")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
