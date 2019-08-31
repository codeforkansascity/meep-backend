import time

from passlib.hash import pbkdf2_sha256 as hasher
import jwt

from app import create_app
from models import User, Role, Project, db, ProjectType, Location


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check if email is defined correctly
    """
    assert new_user.email == 'evan@aol.com'
    assert hasher.verify('1289rhth', new_user.password)

def test_encode_user_auth_token(app, new_user):
    encoded_token = new_user.encode_auth_token()
    assert isinstance(encoded_token, bytes)
    decoded_token = jwt.decode(encoded_token, key=app.config.get('PRIVATE_KEY'), algorithms='HS256')
    assert decoded_token.get('sub') == new_user.id


def test_decode_user_auth_token(new_user):
    encoded_token = new_user.encode_auth_token()
    decoded_token = new_user.decode_auth_token(encoded_token)
    assert decoded_token == new_user.id


def test_decode_user_auth_token_invalid_token(new_user):
    encoded_token = new_user.encode_auth_token()
    decoded_token = new_user.decode_auth_token('let-me-in')
    assert decoded_token == 'Token invalid. Please try again.'


def test_decode_user_auth_token_expiration(new_user):
    encoded_token = new_user.encode_auth_token(expiration_seconds=1)
    time.sleep(2)
    decoded_token = new_user.decode_auth_token(encoded_token)
    assert decoded_token == 'Token signature has expired. Please log in again.'



def test_new_role(new_role):
    """
    GIVEN a Role model
    WHEN a new Role is created
    THEN check if role_name is defined correctly
    """
    assert new_role.role_name == "admin"

def test_new_project(new_project):
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check if their fields are defined correctly
    """
    assert new_project.name == "testName"
    assert new_project.description == "testDescription"
    assert new_project.photo_url == "www.google.com"
    assert new_project.website_url == "www.aol.com"
    assert new_project.year == 1999
    assert new_project.gge_reduced == 1.234
    assert new_project.ghg_reduced == 2.234

def test_insert_location(app):
    location = Location(address='123 testing way')
    db.session.add(location)
    db.session.commit()
    assert location is not None

def test_select_location(app):
    location = Location(address='456 test drive', state='CA')
    db.session.add(location)
    db.session.commit()
    selected_location = Location.query.filter_by(state='CA').first()
    assert selected_location.address == '456 test drive'

def test_update_location(app):
    location = Location(address='789 test road', state='CA')
    db.session.add(location)
    db.session.commit()
    selected_location = Location.query.filter_by(address='789 test road').first()
    assert selected_location.state == 'CA'
    selected_location.state = 'CO'
    db.session.commit()
    selected_location = Location.query.filter_by(address='789 test road').first()
    assert selected_location.state == 'CO'

def test_get_location_coordinates(app):
    location = Location(location='POINT(-94.782234 38.880684)')
    coords = location.coords
    assert coords.get('latitude') == 38.880684
    assert coords.get('longitude') == -94.782234

    bad_location = Location(location=None)
    bad_coords = bad_location.coords
    assert bad_coords.get('latitude') == None
    assert bad_coords.get('longitude') == None
