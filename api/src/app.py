from functools import wraps
import re

from flask import Flask, request, make_response, jsonify, url_for

from config import config
from models import db, User
from server.auth import get_auth_token_from_header, login_user, register_user

def create_app(config_name='dev'):
    """App factory method for initializing flask extensions and registering
    blueprints. See http://flask.pocoo.org/docs/1.0/patterns/appfactories/
    for info on this pattern.
    Later can implement other configs like test and prod.
    """
    app = Flask(__name__, instance_relative_config=True)

    # config data defined in config.py
    app.config.from_object(config[config_name])

    assert app.config.get('PRIVATE_KEY') is not None

    with app.app_context():
        # initialize extensions
        db.init_app(app)
        from resources.locations import api_locations_blueprint
        from resources.projects import api_projects_blueprint
        from resources.users import api_users_blueprint
        from server.auth import auth_blueprint

        # register blueprints
        app.register_blueprint(api_locations_blueprint)
        app.register_blueprint(api_projects_blueprint)
        app.register_blueprint(api_users_blueprint)
        app.register_blueprint(auth_blueprint)

        @app.route('/ping')
        def ping():
            return "<h1>Hellos from MEEP!</h1>"

        if app.config.get('REQUIRE_AUTH_TOKEN'):
            for view in app.view_functions:
                if view not in ('register_user', 'login_user'):
                    app.view_functions[view] = require_auth(app.view_functions[view])

        return app

def require_auth(view):
    @wraps(view)
    def new_view(*args, **kwargs):
        auth_token = get_auth_token_from_header(request)
        decoded = User.decode_auth_token(auth_token)
        if isinstance(decoded, str): #decode_auth_token returns strings with error messages for invalid tokens
            return make_response(jsonify(dict(
                message=decoded,
                status='Unauthorized token. Register or login.',
                urls=dict(
                    register=request.url_root[:-1] + url_for('api_auth.register_user'),
                    login=request.url_root[:-1] + url_for('api_auth.login_user'),
                    current=request.url
                )
            ))), 401
        return view(*args, **kwargs)

    return new_view
