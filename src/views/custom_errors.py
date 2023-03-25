"""Custom Error Routes"""

from flask import Blueprint, abort, render_template

custom_error = Blueprint("custom_error", __name__, template_folder="./templates")


@custom_error.route("/500")
def error500():
    abort(500)


@custom_error.errorhandler(404)
def not_found(e):
    return (
        render_template(
            "/pages/error.html", e="The page you are looking for does not exist!"
        ),
        404,
    )


@custom_error.errorhandler(400)
def bad_requests(e):
    return (
        render_template(
            "/pages/error.html",
            e="The browser (or proxy) sent a request that this server could not understand.",
        ),
        400,
    )


@custom_error.errorhandler(500)
def internal_error(error):
    return (
        render_template(
            "/pages/error.html", e="There has been an internal server error!"
        ),
        500,
    )
