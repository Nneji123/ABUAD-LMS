"""
This module defines a Flask Blueprint for handling user logout functionality. 
It includes a route for logging out the current user and redirecting them to the login page with a success message. 
The Blueprint requires users to be logged in to access the logout page, which is enforced using the login_required decorator provided by Flask-Login.

"""


from flask import Blueprint, redirect, url_for
from flask_login import LoginManager, login_required, logout_user

logout = Blueprint("logout", __name__, template_folder="./templates")
login_manager = LoginManager()
login_manager.init_app(logout)


@logout.route("/logout")
@login_required
def show():
    logout_user()
    return redirect(url_for("login.show") + "?success=logged-out")
