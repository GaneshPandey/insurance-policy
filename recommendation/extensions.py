from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate


db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)
