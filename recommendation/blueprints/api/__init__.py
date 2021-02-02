from flask import Blueprint
from flask_restx import Api

from recommendation.blueprints.auth.endpoints import auth_ns

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {
    "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(
    api_bp,
    version="0.1",
    title="Insurance recommendation API",
    description="Insurance recommendation API Documentaion",
    doc="/doc",
    # authorizations=authorizations,
)

api.add_namespace(auth_ns, path="/auth")

print("Inside API bulueprint", auth_ns)
