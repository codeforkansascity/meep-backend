from flask import Flask
from src.config import config
from src.models import db

# for some reason doing this import makes models accessible to create_app
# TODO: see if app can be instantiated without this import
# from models import User, Role, Project, ProjectType, Location


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
        from src.resources.locations import api_locations_blueprint
        from src.resources.projects import api_projects_blueprint
        from src.resources.users import api_users_blueprint

        # register blueprints
        app.register_blueprint(api_locations_blueprint)
        app.register_blueprint(api_projects_blueprint)
        app.register_blueprint(api_users_blueprint)

        return app
