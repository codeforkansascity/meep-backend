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
        user = User.query.filter_by(email="idonotexistyet@gmail.com").first()
        assert user
