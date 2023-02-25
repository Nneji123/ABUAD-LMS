import uuid

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Students(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)
    matric_number = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(10))

    def check_password(self, password):
        return check_password_hash(self.password, password)



class Lecturers(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String(10))

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Admins(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String(10))
    is_admin = db.Column(db.Boolean, default=True)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)    
    
    

class StudentsView(ModelView):
    column_searchable_list = ['username', 'email', 'matric_number']
    column_filters = ['username', 'email', 'matric_number']
    column_exclude_list = ['password']
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = generate_password_hash(model.password, method="sha256")
        return super(StudentsView, self).on_model_change(form, model, is_created)


class LecturersView(ModelView):
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email']
    column_exclude_list = ['password']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = generate_password_hash(model.password, method="sha256")
        return super(StudentsView, self).on_model_change(form, model, is_created)

class AdminsView(ModelView):
    column_searchable_list = ['username']
    column_filters = ['username']
    column_exclude_list = ['password']
    form_excluded_columns = ['id']
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = generate_password_hash(model.password, method="sha256")
        return super(AdminsView, self).on_model_change(form, model, is_created)
    
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    