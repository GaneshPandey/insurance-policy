from datetime import timedelta

DEBUG = True
TESTING = False
LOG_LEVEL = "DEBUG"  # CRITICAL / ERROR / WARNING / INFO / DEBUG

SERVER_NAME = "localhost:8000"
SECRET_KEY = "dev-secret-key"

# SQLAlchemy.
db_uri = "postgresql://recommendation:recommendationpass123@postgres:5432/recommendation"
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

# User.
SEED_ADMIN_ROLE = "admin"
SEED_ADMIN_EMAIL = "dev@local.host"
SEED_ADMIN_PASSWORD = "devpassword"
SEED_ADMIN_FIRST_NAME = "Ganesh"
SEED_ADMIN_LAST_NAME = "Pandey"
SEED_ADMIN_USERNAME = "noones"

# bcrypt configuration settings
# make sure to change accordingly on production settings
BCRYPT_LOG_ROUNDS = 4
TOKEN_EXPIRE_HOURS = 0
TOKEN_EXPIRE_MINUTES = 5
PRESERVE_CONTEXT_ON_EXCEPTION = False
