from flask_sqlalchemy import SQLAlchemy, Model

# see flask_sqlalchemy docs for details on how the library works
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/
# also, the plain sqlalchemy docs
# https://www.sqlalchemy.org/

# Model base class is defined in app.py, and is imported in db.
from src.app import db


# base class shared by all models. Needed to instantiate SQLAlchemy object.
class BaseModel(Model):
    @property
    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # TODO: make this a property instead of a getter method
    @classmethod
    def get_columns(cls):
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
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    # Many to one relationship with role
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    role = db.relationship('Role', backref=db.backref('users', lazy='select'))

    def __init__(self, email):
        self.email = email


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
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    project = db.relationship('Project', backref='locations')

    def __repr__(self):
        return 'Location(address={self.address}, city={self.city}, '\
               'state={self.state}, zip_code={self.zip_code}, '\
               'latitude={self.latitude}, longitude={self.longitude}, '\
               'project_id={self.project_id})'.format(self=self)
