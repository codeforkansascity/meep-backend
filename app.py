from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model

from config import config

# base class shared by all models. Needed to instantiate SQLAlchemy object.
class BaseModel(Model):
    @property
    def json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    #TODO: make this a property instead of a getter method
    @classmethod
    def get_columns(cls):
        return [c.name for c in cls().__table__.columns]

# globally accessible database connection
db = SQLAlchemy(model_class=BaseModel)


from models import User, Role, Project, ProjectType, Location


def create_app(config_name='dev'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    with app.app_context():
        # initialize extensions
        db.init_app(app)
        from resources import api_blueprint

        # register blueprints
        app.register_blueprint(api_blueprint)

        return app
