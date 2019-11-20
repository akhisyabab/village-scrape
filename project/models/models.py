import datetime

from functools import wraps
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from project import db, bcrypt

from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(128), nullable=True)
    username = db.Column(db.String(128), nullable=False, unique=True,)
    password = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=True)
    register_on = db.Column(db.DateTime, nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    role = db.Column(db.String, default='user')
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = password
        self.phone = None
        self.address = None
        self.register_on = datetime.datetime.now()
        self.is_confirmed = False
        self.role = role
        self.authenticated = False
        self.bank_name = None
        self.bank_number = None

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def __repr__(self):
        return '<title {}'.format(self.name)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


class Datasource(db.Model):
    __tablename__ = 'datasources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_name = db.Column(db.String(128), nullable=True)
    site_url = db.Column(db.String(128), nullable=True )

    def __init__(self, site_name, site_url):
        self.site_name = site_name
        self.site_url = site_url

    @classmethod
    def find_by_site_name(cls, site_name):
        return cls.query.filter_by(site_name=site_name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def __repr__(self):
        return '<title {}'.format(self.site_name)

    def to_json(self):
        return {
            'id': self.id,
            'site_name': self.site_name,
            'site_url': self.site_url
        }


class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
