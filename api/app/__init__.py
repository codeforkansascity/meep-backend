from flask import Flask, jsonify
from datetime import datetime
# from .config import config
from app.models import db
from flask_cors import CORS

def create_app(config_name='dev'):
    """App factory method for initializing flask extensions and registering
    blueprints. See http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    for info on this pattern.
    Later can implement other configs like test and prod.
    """
    app = Flask(__name__, instance_relative_config=True)

    # config data defined in config.py
    # app.config.from_object(config[config_name])
    app.config.from_envvar('APP_SETTINGS')
    # get db string
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://{}:{}@{}/{}'.format(
        *[app.config[o] for o in ('PG_USER','PG_PASS', 'PG_HOSTNAME', 'PG_DBNAME')]
    )
    with app.app_context():
        # initialize extensions
        db.init_app(app)
        CORS(app)
        from .resources.locations import api_locations_blueprint
        from .resources.projects import api_projects_blueprint
        from .resources.users import api_users_blueprint
        from .forms import forms_blueprint

        # register blueprints
        app.register_blueprint(api_locations_blueprint)
        app.register_blueprint(api_projects_blueprint)
        app.register_blueprint(api_users_blueprint)
        app.register_blueprint(forms_blueprint)

        app.config['UPTIME'] = datetime.now()

        @app.route('/ping')
        def ping():
            return jsonify({
                "success": True, 
                "name": f"meep-server-{app.config['ENV']}", 
                "uptime": app.config['UPTIME'],
                "duration": str((datetime.now() - app.config['UPTIME']))
            })

        return app
