from datetime import datetime, timezone, timedelta
from collections import OrderedDict

import jwt
from recommendation.extensions import db, bcrypt
from lib.util_sqlalchemy import AwareDateTime
from lib.util_result import Result
from config import settings


class User(db.Model):
    """ "
    User Model
    """

    ROLE = OrderedDict([("member", "Member"), ("admin", "Admin")])

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, index=True)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(*ROLE, name="role_types", native_enum=False))
    active = db.Column(
        "is_active", db.Boolean(), nullable=False, server_default="1"
    )
    # Activity tracking.
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_on = db.Column(AwareDateTime())
    last_sign_in_ip = db.Column(db.String(45))

    def __repr__(self):
        return f"<User username={self.username}>"

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password_hash = User.encrypt_password(kwargs.get("password", ""))

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @classmethod
    def encrypt_password(cls, plain_text_password):
        """
        Hash a plain text password i.e string using bcrypt
        :param plain_text_password:
        :return: str
        """
        log_rounds = settings.BCRYPT_LOG_ROUNDS
        hash_bytes = bcrypt.generate_password_hash(
            plain_text_password, log_rounds
        )
        return hash_bytes.decode("utf-8")

    @password.setter
    def password(self, password):
        self.password_hash = User.encrypt_password(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def encode_access_token(self):
        now = datetime.now(timezone.utc)
        token_age_h = settings.TOKEN_EXPIRE_HOURS
        token_age_m = settings.TOKEN_EXPIRE_MINUTES
        expire = now + timedelta(hours=token_age_h, minutes=token_age_m)
        if settings.TESTING:
            expire = now + timedelta(seconds=5)
        payload = dict(
            exp=expire, iat=now, sub=self.public_id, admin=self.admin
        )
        key = settings.SECRET_KEY
        return jwt.encode(payload, key, algorithm="HS256")

    @staticmethod
    def decode_access_token(access_token):
        if isinstance(access_token, bytes):
            access_token = access_token.decode("ascii")
        if access_token.startswith("Bearer "):
            split = access_token.split("Bearer")
            access_token = split[1].strip()
        try:
            key = settings.SECRET_KEY
            payload = jwt.decode(access_token, key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            error = "Access token expired. Please log in again."
            return Result.Fail(error)
        except jwt.InvalidTokenError:
            error = "Invalid token. Please log in again."
            return Result.Fail(error)

        if BlacklistedToken.check_blacklist(access_token):
            error = "Token blacklisted. Please log in again."
            return Result.Fail(error)
        user_dict = dict(
            token=access_token,
            expires_at=payload["exp"],
        )
        return Result.Ok(user_dict)

    @classmethod
    def find_by_identity(cls, identity):
        """
        Find a user by their e-mail or username.

        :param identity: Email or username
        :type identity: str
        :return: User instance
        """
        return User.query.filter(
            (User.email == identity) | (User.username == identity)
        ).first()

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()

        return self


class BlacklistedToken(db.Model):
    """BlacklistedToken Model for storing JWT tokens."""

    __tablename__ = "token_blacklists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(AwareDateTime())
    expires_at = db.Column(AwareDateTime())

    def __init__(self, token, expires_at):
        self.token = token
        self.expires_at = expires_at

    def __repr__(self):
        return f"<BlacklistToken token={self.token}>"

    @classmethod
    def check_blacklist(cls, token):
        exists = cls.query.filter_by(token=token).first()
        return True if exists else False
