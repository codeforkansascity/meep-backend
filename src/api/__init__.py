from flask import Blueprint

api = Blueprint('api', __name__)

from . import projects
# from . import users
# other routes etc.
