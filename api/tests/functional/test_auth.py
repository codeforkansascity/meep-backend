import time
from functools import partial

import pytest
from flask import current_app

from app import create_app, require_auth
from models import db, User, BlacklistedAuthToken

def test_register_existing_user(app):
    existing_user = create_user('iexist@gmail.com')
    with app.test_client() as client:
        response, _ = register_user(client, 'iexist@gmail.com', 'password')
        assert response.status_code == 202
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == 'User already exists. Please log in.'

def test_register_new_user(app):
    with app.test_client() as client:
        response, auth_token = register_user(client, 'idonotexistyet@gmail.com')
        assert response.status_code == 201
        response_data = response.get_json()
        assert response_data.get('status') == 'success'
        assert response_data.get('message') == 'Successfully created user.'
        assert auth_token is not None
        assert isinstance(auth_token.encode(), bytes)
        user = User.query.filter_by(email="idonotexistyet@gmail.com").first()
        assert user
        assert user.encode_auth_token() == auth_token.encode()

def test_login(app, new_user):
    db.session.add(new_user)
    db.session.commit()
    with app.test_client() as client:
        response, _ = login_user(client, new_user.email, password='1289rhth')
        assert response.status_code == 200
        response_data = response.get_json()
        assert response_data.get('status') == 'success'
        assert response_data.get('message') == 'Login successful'
        auth_token = response_data.get('auth_token')
        assert auth_token is not None
        assert auth_token.encode() == new_user.encode_auth_token()

def test_nonregistered_user_login(app):
    with app.test_client() as client:
        response, _ = login_user(client, 'hackeremail@gmail.com', password='12345')
        assert response.status_code == 404
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == "User not found. Please register or try again."

def test_invalid_email_login(app):
    with app.test_client() as client:
        response, _ = login_user(client, 'i.do.what.i.want')
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == "Invalid email address. Please register or try again."

def test_user_auth_status(app):
    registration_data = dict(
        email='user@gmail.com',
        password='password'
    )
    with app.test_client() as client:
        _, auth_token = register_user(client, 'user@gmail.com')
        response = get_auth_status(client, auth_token)
        assert response.status_code == 200
        response_data = response.get_json()
        assert response_data.get('status') == 'success'
        assert response_data.get('data') is not None
        assert response_data.get('data').get('email') == 'user@gmail.com'
        assert response_data.get('data').get('admin') is None

def test_user_auth_invalid_token(app):
    registration_data = dict(
        email='user@gmail.com',
        password='password'
    )
    with app.test_client() as client:
        _, auth_token = register_user(client, 'user@gmail.com')
        response = get_auth_status(client, 'thiscannotpossiblyberight')
        assert response.status_code == 401
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == 'Token invalid. Please try again.'

def test_user_auth_no_authorization_header(app):
    with app.test_client() as client:
        _, auth_token = register_user(client, 'user@gmail.com')
        response = client.get('/auth/status', headers=dict())
        assert response.status_code == 401
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == 'Invalid auth token.'

def test_logout_user(app):
    with app.test_client() as client:
        _, auth_token = register_user(client, 'superuser@hotmail.com')
        login_resp, _ = login_user(client, 'superuser@hotmail.com')
        assert login_resp.status_code == 200
        assert login_resp.get_json().get('message') == 'Login successful'

        response = logout_user(client, auth_token)
        assert response.status_code == 200
        response_data = response.get_json()
        assert response_data.get('status') == 'success'
        assert response_data.get('message') == 'User logged out.'
        # assert data.get('email') == 'superuser@hotmail.com'

        # check that blacklisted token has been added to the database
        bad_token = BlacklistedAuthToken.query.filter_by(token=auth_token).first()
        assert bad_token is not None

def test_invalid_logout(app):
    with app.test_client() as client:
        _, auth_token = register_user(client, 'bestuser@gmail.com')
        login_response, _ = login_user(client, 'bestuser@gmail.com')
        assert login_response.status_code == 200
        status_response = get_auth_status(client, auth_token)
        assert status_response.status_code == 200
        assert status_response.get_json().get('status') == 'success'

        time.sleep(2) # ensure auth token expires
        response = logout_user(client, auth_token)
        assert response.status_code == 400
        assert response.get_json().get('status') == 'failure'
        assert response.get_json().get('message') == 'Token signature has expired. Please log in again.'


def test_user_status_with_blacklisted_token(app):
    with app.test_client() as client:
        _, bad_token = register_user(client, 'superduperuser@gmail.com')
        assert bad_token
        login_resp, _ = login_user(client, 'superduperuser@gmail.com')
        assert login_resp.status_code == 200
        # blacklist users auth token
        db.session.add(BlacklistedAuthToken(token=bad_token))
        db.session.commit()
        # check user status with blacklisted token
        response = get_auth_status(client, bad_token)
        assert response.status_code == 401
        assert response.get_json().get('status') == 'failure'
        assert response.get_json().get('message') == 'Token blacklisted. Please login again.'


def test_logout_with_blacklisted_token(app):
    with app.test_client() as client:
        register_res, bad_token = register_user(client, 'superuser@gmail.com')
        assert register_res.status_code == 201
        assert bad_token is not None
        login_resp, _ = login_user(client, 'superuser@gmail.com')
        assert login_resp.status_code == 200
        BlacklistedAuthToken.blacklist(bad_token)
        response = logout_user(client, bad_token)
        assert response.status_code == 401
        assert response.get_json().get('status') == 'failure'
        assert response.get_json().get('message') == 'Token blacklisted. Please login again.'

def create_user(email):
    user = User(email=email, password='password')
    db.session.add(user)
    db.session.commit()

def register_user(client, email, password='password'):
    response = client.post('/auth/register',
        json=dict(email=email, password=password))
    auth_token = response.get_json().get('auth_token')
    return response, auth_token

def login_user(client, email, password='password'):
    response = client.post('/auth/login',
        json=dict(email=email, password=password))
    auth_token = response.get_json().get('auth_token')
    return response, auth_token

def get_auth_status(client, auth_token):
    return client.get('/auth/status',
        headers={
            'Authorization': f'Bearer {auth_token}'
        })

def logout_user(client, auth_token):
    return client.post('/auth/logout',
        headers=dict(Authorization=f'Bearer {auth_token}'))

def test_route_authorization(app):
    assert 'ping' in app.view_functions
    app.view_functions['ping'] = require_auth(app.view_functions['ping'])
    with app.test_client() as client:
        register_user(client, 'someuser@gmail.com')
        _, auth_token = login_user(client, 'someuser@gmail.com')
        success_response = client.get('/ping',
            headers={'Authorization': f'Bearer {auth_token}'})
        assert success_response.status_code == 200
        logout_user(client, auth_token)
        blacklisted_response = client.get('/ping',
            headers={'Authorization': f'Bearer {auth_token}'})
        assert blacklisted_response.status_code == 401
        res_data = blacklisted_response.get_json()
        assert res_data.get('status') == 'Unauthorized token. Register or login.'
        assert res_data.get('message') == 'Token blacklisted. Please login again.'
        urls = res_data.get('urls')
        assert urls.get('current').split('/')[-1] == 'ping'
        assert urls.get('login').split('/')[-2:] == ['auth', 'login']
        assert urls.get('register').split('/')[-2:] == ['auth', 'register']

        # test route using an invalid token
        unauthorized_response = client.get('/ping',
            headers={'Authorization': 'Bearer jabberwocky'})
        assert unauthorized_response.status_code == 401
        res_data = unauthorized_response.get_json()
        assert res_data.get('message') == 'Token invalid. Please try again.'
