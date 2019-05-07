from flask import Flask
from config import config
from models import db


def create_app(config_name='dev'):
    app = Flask(__name__, instance_relative_config=True)
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
