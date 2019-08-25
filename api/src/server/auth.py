import re

from flask import Blueprint, request, jsonify, make_response, current_app

from models import db, User, BlacklistedAuthToken

auth_blueprint = Blueprint('api_auth', __name__)

@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    user_data = request.get_json()
    user = User.query.filter_by(email=user_data.get('email')).first()
    if user:
        return make_response(
            jsonify({
                'status': 'failure',
                'message': 'User already exists. Please log in.'
            })), 202

    user = User(
        email=user_data.get('email'),
        password=user_data.get('password'))
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(
        expiration_seconds=int(current_app.config.get('TOKEN_EXPIRATION', 10)))

    return make_response(jsonify({
        'status': 'success',
        'message': 'Successfully created user.',
        'auth_token': user.encode_auth_token().decode()
    })), 201


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    user_data = request.get_json()
    email = user_data.get('email')
    password = user_data.get('password')
    try:
        User.validate_email(email)
    except AssertionError:
        return make_response(jsonify({
            'status': 'failure',
            'message': "Invalid email address. Please register or try again."
        })), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return make_response(jsonify({
            'status': 'failure',
            'message': "User not found. Please register or try again."
        })), 404
    try:
        user.validate_password(password)
    except AssertionError:
        return "Invalid password. Please try again."
    auth_token = user.encode_auth_token()
    # return json web token
    response = make_response(jsonify({
        'status': 'success',
        'message': 'Login successful',
        'auth_token': auth_token.decode()
    }))
    return response, 200


@auth_blueprint.route('/auth/status', methods=['GET'])
def user_status():
    authorization_header = request.headers.get('Authorization', '')
    match = re.search(r'^Bearer\s(.+)$', authorization_header)
    auth_token = match.group(1) if match else ''
    if auth_token:
        user_id = User.decode_auth_token(auth_token)
        if not isinstance(user_id, str):
            user = User.query.filter_by(id=user_id).first()
            response_data = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'role': user.role.role_name if user.role else None
                }
            }
            status_code = 200
        else:
            response_data = {
                'status': 'failure',
                'message': user_id
            }
            status_code = 401
    else:
        response_data = {
            'status': 'failure',
            'message': 'Invalid auth token.'
        }
        status_code = 401
    return make_response(jsonify(response_data)), status_code


@auth_blueprint.route('/auth/logout', methods=['POST'])
def logout_user():
    auth_header = request.headers.get('Authorization', '')
    match = re.search(r'^Bearer (.+)$', auth_header)
    auth_token = match.group(1) if match else ''
    user_id = User.decode_auth_token(auth_token)
    if isinstance(user_id, str): # if error decoding token, user_id is a string with the error message
        status_code = 401 if 'blacklist' in user_id.lower() else 400
        return make_response(jsonify({
            'status': 'failure',
            'message': user_id
        })), status_code
    # blacklist the token
    try:
        blacklisted_token = BlacklistedAuthToken(auth_token)
        db.session.add(blacklisted_token)
        db.session.commit()
        return make_response(jsonify({
            'status': 'success',
            'message': 'User logged out.'
        })), 200
    except Exception:
        return make_response(jsonify({
            'status': 'failure',
            'message': 'Internal server error'
        })), 500
