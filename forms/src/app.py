import os

from flask import Flask
from forms import forms_blueprint

app = Flask(__name__)

app.config['API_DOMAIN'] = os.environ.get('API_DOMAIN', 'http://localhost/api')

app.register_blueprint(forms_blueprint)
app.register_blueprint(login_blueprint)

@forms_blueprint.route("/index", methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/ping')
"""Endpoint to test if the app is running"""
def ping():
    return <h1>'pong'</h1>
