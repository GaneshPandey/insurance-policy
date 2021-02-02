"""
Global pytest fixtures
"""

import pytest
from config import settings
from recommendation.app import create_app
from recommendation.extensions import db as _db
from recommendation.blueprints.user.models import User


@pytest.fixture(scope="session")
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """
    db_uri = "{0}_test".format(settings.SQLALCHEMY_DATABASE_URI)
    params = {
        "DEBUG": False,
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": db_uri,
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope="session")
def db(app):
    """
    Setup our database, this only gets executed once per session.

    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    _db.drop_all()
    _db.create_all()

    # Create a single user because a lot of tests do not mutate this user.
    # It will result in faster tests.
    params = {
        "role": "admin",
        "email": "admin@local.host",
        "username": "noones",
        "password": "password",
        "first_name": "Ganesh",
        "last_name": "Pandey",
    }

    admin = User(**params)

    _db.session.add(admin)
    _db.session.commit()

    return _db
