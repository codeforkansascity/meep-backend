import os

from flask import Flask
from forms import forms_blueprint
from login import login_blueprint


def create_app():
    app = Flask(__name__)

    app.config['API_DOMAIN'] = os.environ.get('API_DOMAIN', 'http://localhost/api')

    app.register_blueprint(forms_blueprint)
    app.register_blueprint(login_blueprint)

    @forms_blueprint.route("/index", methods=["GET"])
    def index():
        return render_template('index.html')

    @app.route('/ping')
    def ping():
        """Endpoint to test if the app is running"""
        return '<h1>pong</h1>'

    return app
