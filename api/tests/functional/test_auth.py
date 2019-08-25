import time

import pytest

from models import db, User, BlacklistedAuthToken

def test_register_existing_user(app):

    existing_user = User(email="iexist@gmail.com", password="password")
    db.session.add(existing_user)
    db.session.commit()
    with app.test_client() as client:
        response = client.post('/auth/register',
            json={
                'email': 'iexist@gmail.com',
                'password': 'password'
            })
        assert response.status_code == 202
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == 'User already exists. Please log in.'


def test_register_new_user(app):
    with app.test_client() as client:
        new_user_data = dict(
            email="idonotexistyet@gmail.com",
            password="password"
        )
        response = client.post('/auth/register',
            json=new_user_data)
        assert response.status_code == 201
        response_data = response.get_json()
        assert response_data.get('status') == 'success'
        assert response_data.get('message') == 'Successfully created user.'
        auth_token = response_data.get('auth_token')
        assert auth_token is not None
        assert isinstance(auth_token.encode(), bytes)
        user = User.query.filter_by(email="idonotexistyet@gmail.com").first()
        assert user
        assert user.encode_auth_token() == auth_token.encode()


def test_login(app, new_user):
    db.session.add(new_user)
    db.session.commit()
    with app.test_client() as client:
        response = client.post('/auth/login',
            json={
                'email': new_user.email,
                'password': '1289rhth'
            })
        assert response.status_code == 200
        response_data = response.get_json()
        assert response_data.get('status') == 'success'
        assert response_data.get('message') == 'Login successful'
        auth_token = response_data.get('auth_token')
        assert auth_token is not None
        assert auth_token.encode() == new_user.encode_auth_token()


def test_nonregistered_user_login(app):
    invalid_login_data = dict(
        email='hackeremail@gmail.com',
        password='12345'
    )
    with app.test_client() as client:
        response = client.post('/auth/login',
            json=invalid_login_data)
        assert response.status_code == 404
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == "User not found. Please register or try again."


def test_invalid_email_login(app):
    invalid_login_data = dict(
        email='i.do.what.i.want',
        password='password'
    )
    with app.test_client() as client:
        response = client.post('/auth/login',
            json=invalid_login_data)
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
        auth_token = client.post('/auth/register', json=registration_data)\
            .get_json()\
            .get('auth_token')
        authorization_header = f"Bearer {auth_token}"

        response = client.get('/auth/status',
            headers=dict(
                Authorization=authorization_header
            ))
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
        auth_token = client.post('/auth/register', json=registration_data)\
            .get_json()\
            .get('auth_token')
        authorization_header = f"Bearer thiscannotpossiblyberight"

        response = client.get('/auth/status',
            headers=dict(
                Authorization=authorization_header
            ))
        assert response.status_code == 401
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == 'Token invalid. Please try again.'

def test_user_auth_no_authorization_header(app):
    registration_data = dict(
        email='user@gmail.com',
        password='password'
    )
    with app.test_client() as client:
        auth_token = client.post('/auth/register', json=registration_data)\
            .get_json()\
            .get('auth_token')
        response = client.get('/auth/status', headers=dict())
        assert response.status_code == 401
        response_data = response.get_json()
        assert response_data.get('status') == 'failure'
        assert response_data.get('message') == 'Invalid auth token.'

def test_logout_user(app):
    with app.test_client() as client:
        # register a new user and get auth token generated
        auth_token = client.post('/auth/register',
            json={
                'email': 'superuser@hotmail.com',
                'password': 'password'
            })\
            .get_json()\
            .get('auth_token')
        # login that user
        login_resp = client.post('/auth/login',
            json={
                'email': 'superuser@hotmail.com',
                'password': 'password'
            })
        assert login_resp.status_code == 200
        assert login_resp.get_json().get('message') == 'Login successful'

        response = client.post('/auth/logout',
            headers={
                'Authorization': f'Bearer {auth_token}'
            })
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
        auth_token = client.post('/auth/register',
            json={
                'email': 'bestuser@gmail.com',
                'password': 'password'
            })\
            .get_json()\
            .get('auth_token')

        login_response = client.post('/auth/login',
            json={
                'email': 'bestuser@gmail.com',
                'password': 'password'
            })
        assert login_response.status_code == 200
        status_response = client.get('/auth/status',
            headers={
                'Authorization': f'Bearer {auth_token}'
            })
        assert status_response.status_code == 200
        assert status_response.get_json().get('status') == 'success'

        time.sleep(2) # ensure auth token expires
        response = client.post('/auth/logout',
            headers={
                'Authorization': f'Bearer {auth_token}'
            })
        assert response.status_code == 400
        assert response.get_json().get('status') == 'failure'
        assert response.get_json().get('message') == 'Token signature has expired. Please log in again.'


def test_user_status_with_blacklisted_token(app):
    with app.test_client() as client:
        # register user
        bad_token = client.post('/auth/register',
            json={
                'email': 'superduperuser@gmail.com',
                'password': 'password'
            }
        )\
        .get_json()\
        .get('auth_token')
        assert bad_token
        # login user
        login_resp = client.post('/auth/login',
            json={
                'email': 'superduperuser@gmail.com',
                'password': 'password'
            })
        assert login_resp.status_code == 200
        # blacklist users auth token
        db.session.add(BlacklistedAuthToken(token=bad_token))
        db.session.commit()
        # check user status with blacklisted token
        response = client.get('/auth/status',
            headers=dict(Authorization=f'Bearer {bad_token}'))
        assert response.status_code == 401
        assert response.get_json().get('status') == 'failure'
        assert response.get_json().get('message') == 'Token blacklisted. Please login again.'

        db.session.delete(User.query.filter_by(email='superduperuser@gmail.com').first())
        db.session.commit()


def test_logout_with_blacklisted_token(app):
    with app.test_client() as client:
        # register user
        register_res = client.post('/auth/register',
            json={
                'email': 'superuser@gmail.com',
                'password': 'password'
            })
        assert register_res.status_code == 201
        bad_token = register_res.get_json().get('auth_token')
        assert bad_token is not None
        # login user
        login_resp = client.post('/auth/login',
            json={
                'email': 'superuser@gmail.com',
                'password': 'password'
            })
        assert login_resp.status_code == 200
        # blacklist users auth token
        db.session.add(BlacklistedAuthToken(token=bad_token))
        db.session.commit()
        # check user status with blacklisted token
        response = client.post('/auth/logout',
            headers=dict(Authorization=f'Bearer {bad_token}'))
        assert response.status_code == 401
        assert response.get_json().get('status') == 'failure'
        assert response.get_json().get('message') == 'Token blacklisted. Please login again.'

        db.session.delete(User.query.filter_by(email='superuser@gmail.com').first())
        db.session.commit()
