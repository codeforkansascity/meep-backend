import pytest

from models import db, User

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
