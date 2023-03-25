"""Logout Route"""


from flask import Blueprint, redirect, url_for
from flask_login import LoginManager, login_required, logout_user

logout = Blueprint("logout", __name__)
login_manager = LoginManager()
login_manager.init_app(logout)


@logout.route("/logout")
@login_required
def show():
    logout_user()
    return redirect(url_for("login.show") + "?success=logged-out")
