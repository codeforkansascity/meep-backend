from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def page_not_found(e):
    return {'page not found': str(e)}, 404

@errors.app_errorhandler(500)
def internal_server_error(e):
    return {'internal server error': str(e)}, 500
