import os

import sqlalchemy
from dotenv import load_dotenv
from flask import Flask, render_template, abort
from flask_admin import Admin
from flask_login import LoginManager

from index import index, CustomIndexView
from lecturer import lecturer
from login import login
from logout import logout
from models import Admins, Lecturers, Students, db, StudentsView, LecturersView, AdminsView
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
app.config["LOGIN_DISABLED"] = os.getenv("LOGIN_DISABLED")
db.init_app(app)
app.app_context().push()

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(lecturer)
app.register_blueprint(student)

admin = Admin(app, name='ABUAD', template_mode='bootstrap3', index_view=CustomIndexView())
admin.add_view(StudentsView(Students, db.session))
admin.add_view(LecturersView(Lecturers, db.session))
admin.add_view(AdminsView(Admins, db.session))


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
    except (sqlalchemy.exc.OperationalError) as e:
        return render_template("error.html", e="Database not found")


@app.route('/500')
def error500():
    abort(500)

@app.errorhandler(404)
def not_found(e):
    return render_template("/main_pages/error.html", e="The page you are looking for does not exist!"),404

@app.errorhandler(400)    
def bad_requests(e):
    return render_template("/main_pages/error.html", e="The browser (or proxy) sent a request that this server could not understand."), 400

@app.errorhandler(500)
def internal_error(error):
    return render_template("/main_pages/error.html", e="There has been an internal server error!"), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True, threaded=True)
