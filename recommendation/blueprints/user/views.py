from flask import Blueprint

user = Blueprint("user", __name__, url_prefix="/api/v1/user")


@user.route("/", methods=["GET", "POST"])
def index():
    return "this is a index route"


@user.route("/user", methods=["GET"])
def user_view():
    return "Another user view"
