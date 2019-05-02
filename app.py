from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model

from config import config


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

# for some reason doing this import makes models accessible to create_app
# TODO: see if app can be instantiated without this import
from models import User, Role, Project, ProjectType, Location


def create_app(config_name='dev'):
    """App factory method for initializing flask extensions and registering
    blueprints. See http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    for info on this pattern.
    Later can implement other configs like test and prod.
    """
    app = Flask(__name__, instance_relative_config=True)

    # config data defined in config.py
    app.config.from_object(config[config_name])
    with app.app_context():
        # initialize extensions
        db.init_app(app)

        # blueprints defined in resources files
        from resources import api_blueprint
        app.register_blueprint(api_blueprint)

        return app
