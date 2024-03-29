"""Database Models"""


import uuid
from datetime import datetime

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class Students(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    matric_number = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_logged_in_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    hashCode = db.Column(db.String(120), nullable=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Lecturers(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_logged_in_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    hashCode = db.Column(db.String(120), nullable=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Admins(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_logged_in_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Announcements(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lecturer_id = db.Column(
        db.String(36), db.ForeignKey("lecturers.id"), nullable=False
    )
    profile_pic = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def time_diff(self):
        diff = datetime.utcnow() - self.created_at
        if diff.days == 0:
            return "Posted today"
        elif diff.days == 1:
            return "Posted yesterday"
        else:
            return f"Posted {diff.days} days ago"


class StudentsView(ModelView):
    column_searchable_list = [
        "username",
        "email",
        "matric_number",
        "department",
        "created_at",
        "last_logged_in_at",
    ]
    column_filters = ["username", "email", "matric_number"]
    column_exclude_list = ["password", "hashCode"]

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method="sha256")
        return super(StudentsView, self).on_model_change(form, model, is_created)


class LecturersView(ModelView):
    column_searchable_list = ["username", "email", "created_at", "last_logged_in_at"]
    column_filters = ["username", "email"]
    column_exclude_list = ["password", "hashCode"]

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method="sha256")
        return super(LecturersView, self).on_model_change(form, model, is_created)


class AdminsView(ModelView):
    column_searchable_list = ["username", "created_at", "last_logged_in_at"]
    column_filters = ["username", "created_at", "last_logged_in_at"]
    column_exclude_list = ["password"]
    form_excluded_columns = ["id"]

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method="sha256")
        return super(AdminsView, self).on_model_change(form, model, is_created)


class AnnouncementsView(ModelView):
    column_searchable_list = [
        "lecturer_id",
        "message",
        "title",
        "course_code",
        "created_at",
    ]


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_active
