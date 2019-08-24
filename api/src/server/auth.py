from flask import Blueprint, request, jsonify, make_response, current_app

from models import db, User

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
        'auth_token': User.decode_auth_token(auth_token)
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


@auth_blueprint.route('/auth/logout', methods=['POST'])
def logout_user():
    pass
