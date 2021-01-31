from flask import (
    Blueprint)

user = Blueprint('user', __name__, url_prefix="/api/v1/user")


@user.route('/', methods=['GET', 'POST'])
def index():
    return "this is a index route"
