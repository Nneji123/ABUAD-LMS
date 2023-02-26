from flask import (Blueprint, Response, flash, redirect, render_template,
                   request, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random
import string
from models import db, Students

password_reset = Blueprint("lecturer", __name__, template_folder="./frontend")
# login_manager = LoginManager()
# login_manager.init_app(lecturer)
posta = Mail(password_reset)


@password_reset.route('/forgot_password',methods=["POST","GET"])
def index():
    if request.method=="POST":
        email = request.form['email']
        check = Students.query.filter_by(email=email).first()

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
    
@password_reset.route("/forgot_password/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = Students.query.filter_by(hashCode=hashCode).first()    
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

# @app.route('/createUser')
# def createUser():
#     newUser = User(username='berat',mail='beratbozkurt1999@gmail.com',password='123456')
#     db.session.add(newUser)
#     db.session.commit()
#     return "Created user"
    

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)