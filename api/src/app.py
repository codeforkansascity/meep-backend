from flask import Flask

from config import config
from models import db

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
        from resources.locations import api_locations_blueprint
        from resources.projects import api_projects_blueprint
        from resources.users import api_users_blueprint

        # register blueprints
        app.register_blueprint(api_locations_blueprint)
        app.register_blueprint(api_projects_blueprint)
        app.register_blueprint(api_users_blueprint)

        return app