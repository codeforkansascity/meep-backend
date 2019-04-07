from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

# globally accessible database connection
db = SQLAlchemy()
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
