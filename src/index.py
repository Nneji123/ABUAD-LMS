from flask import Blueprint, redirect, url_for
from flask_admin import expose
from flask_login import logout_user

from models import MyAdminIndexView

index = Blueprint("index", __name__, template_folder="./templates")


@index.route("/", methods=["GET"])
def show():
    return redirect("login")


class CustomIndexView(MyAdminIndexView):
    @expose("/logout")
    def logout(self):
        logout_user()
        return redirect(url_for("login.show"))
