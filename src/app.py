import os

import sqlalchemy
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_admin import Admin

from configurations.config import configs
from configurations.extensions import db, email, login_manager, socketio
from configurations.models import (
    Admins,
    AdminsView,
    Lecturers,
    LecturersView,
    Students,
    StudentsView,
)
from views.custom_errors import custom_error
from views.index import CustomIndexView, index
from views.lecturer import lecturer
from views.login import login
from views.logout import logout
from views.reset_password import reset_passwords
from views.student import student

load_dotenv()


SERVER_MODE = os.getenv("SERVER_MODE")


def create_app(app):
    if SERVER_MODE in configs:
        app.config.update(configs[SERVER_MODE])
    else:
        raise ValueError(f"Unknown server mode: {SERVER_MODE}")
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    login_manager.init_app(app)
    db.init_app(app)
    email.init_app(app)
    socketio.init_app(app)
    create_admin_views(app)
    app.app_context().push()
    return None


def create_admin_views(app):
    admin = Admin(
        app, name="ABUAD", template_mode="bootstrap4", index_view=CustomIndexView()
    )
    admin.add_view(StudentsView(Students, db.session))
    admin.add_view(LecturersView(Lecturers, db.session))
    admin.add_view(AdminsView(Admins, db.session))

    return admin


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(index)
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(lecturer)
    app.register_blueprint(student)
    app.register_blueprint(custom_error)
    app.register_blueprint(reset_passwords)
    return None


@login_manager.user_loader
def load_user(user_id):
    students = Students.query.filter_by(id=user_id).first()
    lecturers = Lecturers.query.filter_by(id=user_id).first()
    admins = Admins.query.filter_by(id=user_id).first()
    try:
        if students:
            return students
        elif lecturers:
            return lecturers
        elif admins:
            return admins
        else:
            return None
    except sqlalchemy.exc.OperationalError as e:
        return render_template("error.html", e="Database not found")


app = Flask(__name__, static_folder="./templates/static")

app = create_app(app)

if __name__ == "__main__":
    socketio.run(
        app,
        port=5000,
        debug=configs[SERVER_MODE]["DEBUG"],
        host="0.0.0.0",
    )
