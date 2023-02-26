import os
import random
import string

import sqlalchemy
from dotenv import load_dotenv
from flask import Flask, render_template, abort, request, redirect, url_for, flash
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail, Message

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

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'beratbozkurt1999@gmail.com'
app.config['MAIL_PASSWORD'] = '[password]'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
posta = Mail(app)

db.init_app(app)
app.app_context().push()

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(lecturer)
app.register_blueprint(student)
# app.register_blueprint(password_reset)


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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    mail = db.Column(db.String(120))
    password = db.Column(db.String(80))
    hashCode = db.Column(db.String(120))

@app.route('/forgot_password',methods=["POST","GET"])
def index():
    if request.method=="POST":
        mail = request.form['mail']
        check = User.query.filter_by(mail=mail).first()

        if check:
            hashCode = ''.join(random.choices(string.ascii_letters + string.digits, k=24))
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'berat@github.com', recipients = [mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hashCode
            posta.send(msg)
            return '''
                <form action="/forgot_password" method="post">
                    <small>enter the email address of the account you forgot your password</small> <br>
                    <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return '''
            <form action="/forgot_password" method="post">
                <small>enter the email address of the account you forgot your password</small> <br>
                <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
                <input type="submit" value="Submit">
            </form>
        '''
    
@app.route("/forgot_password/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = User.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('yanlış girdin')
                return '''
                    <form method="post">
                        <small>enter your new password</small> <br>
                        <input type="password" name="passw" id="passw" placeholder="password"> <br>
                        <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                        <input type="submit" value="Submit">
                    </form>
                '''
        else:
            return '''
                <form method="post">
                    <small>enter your new password</small> <br>
                    <input type="password" name="passw" id="passw" placeholder="password"> <br>
                    <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return render_template('/')

@app.route('/createUser')
def createUser():
    newUser = User(username='',mail='beratbozkurt1999@gmail.com',password='123456')
    db.session.add(newUser)
    db.session.commit()
    db.create_all()
    return "Created user"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True, threaded=True)
