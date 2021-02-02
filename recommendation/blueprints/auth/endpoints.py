from flask_restx import Namespace, Resource
from recommendation.blueprints.user.models import User

auth_ns = Namespace(name="auth", validate=True)


@auth_ns.route("/login", endpoint="auth_login")
class LoginUser(Resource):
    def get(self):
        user = User.query.filter().first()
        return (
            "This is a test auth namespace called user endpoint, {} {}".format(
                user.username, user.email
            )
        )
