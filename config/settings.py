from datetime import timedelta

DEBUG = True
LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

SERVER_NAME = 'localhost:8000'
SECRET_KEY = 'dev-secret-key'

# SQLAlchemy.
db_uri = 'postgresql://devuser:devpassword@postgres:5432/recommendation'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)
