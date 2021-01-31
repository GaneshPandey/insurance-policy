from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


debug_toolbar = DebugToolbarExtension()
db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
