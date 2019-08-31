# see flask_sqlalchemy docs for details on how the library works
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/
# also, the plain sqlalchemy docs
# https://www.sqlalchemy.org/

from datetime import datetime, timedelta
import json
import re

from flask import current_app
from flask_sqlalchemy import SQLAlchemy, Model
from geoalchemy2 import Geometry
from passlib.hash import pbkdf2_sha256 as hasher
from sqlalchemy import func
import jwt




class BaseModel(Model):
    """Base class shared by all models to implement common attributes and methods.
    Needed to instantiate SQLAlchemy object.
    TODO: find a way to move this to models.py without breaking the app
    """

    @property
    def json(self):
        """return json representation of model"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_columns(cls):
        # TODO: make this a property instead of a getter method
        return [c.name for c in cls().__table__.columns]


# globally accessible database connection
db = SQLAlchemy(model_class=BaseModel)

class User(db.Model):
    """A user of the application.
    By convention, all foreign key Columns must end in '_id'
    This will ensure that the parser object in resource.py will work correctly.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    # Many to one relationship with role
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    role = db.relationship('Role', backref=db.backref('users', lazy='select'))
    # TODO: write better email regex
    email_regex = re.compile(r'\w+@\w+\.\w+')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        email = kwargs.get('email')
        if not email:
            raise ValueError('email is required')
        password = kwargs.get('password')
        if not password:
            raise ValueError('password is required')
        self.password = hasher.hash(password)

    def __repr__(self):
        return "User(email={!r})".format(self.email)

    @classmethod
    def validate_email(cls, email):
        assert cls.email_regex.match(email)

    def validate_password(self, password):
        assert hasher.verify(password, self.password)

    def encode_auth_token(self, expiration_seconds=None):
        if expiration_seconds is None:
            expiration_seconds = current_app.config.get('TOKEN_EXPIRATION')
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=expiration_seconds, days=0),
            'iat': datetime.utcnow(),
            'sub': self.id
        }
        return jwt.encode(
            payload,
            current_app.config.get('PRIVATE_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        if isinstance(auth_token, bytes):
            auth_token = auth_token.decode()
        try:
            private_key = current_app.config.get('PRIVATE_KEY')
            decoded_token = jwt.decode(auth_token, private_key, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return 'Token signature has expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Token invalid. Please try again.'
        # check that the token has not been blacklisted
        if BlacklistedAuthToken.is_token_blacklisted(auth_token):
            return 'Token blacklisted. Please login again.'
        return decoded_token['sub']

class Role(db.Model):
    """User role for privileges."""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), nullable=False, unique=True)
    # TODO: Add fields for privileges


class Project(db.Model):
    """An MEC project."""
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(250))
    photo_url = db.Column(db.String(250))
    website_url = db.Column(db.String(250))
    year = db.Column(db.Integer)
    gge_reduced = db.Column(db.Float)
    ghg_reduced = db.Column(db.Float)
    # Many to one relationship with project types
    project_type_id = db.Column(db.Integer, db.ForeignKey('project_types.id'))

    type = db.relationship('ProjectType',
                           backref=db.backref('projects', lazy='select'))

    def __repr__(self):
        return f'Project(name={self.name}, description={self.description}, photo_url={self.photo_url}, website_url={self.website_url}, year={self.year}, ghg_reduced={self.ghg_reduced}, gge_reduced={self.gge_reduced})'


class ProjectType(db.Model):
    """Different categories of projects. I.e. building, vehicle transportation,
    infrastructure transportation, etc. This could potentially be moved into
    a column in the project model, if no new fields are added in the future.
    """
    __tablename__ = 'project_types'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(30), nullable=False, unique=True)

    def __repr__(self):
        return f'ProjectType(type_name={self.type_name})'


class Location(db.Model):
    """Model for spatial data."""
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.Integer)
    location = db.Column(Geometry(geometry_type='POINT'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    project = db.relationship('Project', backref='locations')

    def __repr__(self):
        return 'Location(address={self.address}, city={self.city}, '\
               'state={self.state}, zip_code={self.zip_code}, '\
               'location={self.location}, '\
               'project_id={self.project_id})'.format(self=self)

    @property
    def coords(self):
        try:
            geojson = json.loads(
                db.session.scalar(func.ST_AsGeoJSON(self.location))
            )
            assert geojson.get('type') == 'Point'
        except (TypeError, AssertionError):
            return {'longitude': None, 'latitude': None}

        return dict(zip(('longitude', 'latitude'), geojson.get('coordinates')))


class BlacklistedAuthToken(db.Model):
    __tablename__ = 'blacklisted_auth_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return "BlacklistedAuthToken(token={!r})".format(self.token)

    @classmethod
    def blacklist(cls, token):
        db.session.add(cls(token=token))
        db.session.commit()

    @classmethod
    def is_token_blacklisted(cls, token):
        return cls.query.filter_by(token=token).first() is not None
