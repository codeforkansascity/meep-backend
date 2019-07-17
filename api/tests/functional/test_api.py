import json

from flask import current_app
import pytest

from app import create_app
from models import Location, Project, ProjectType, db


def test_get_locations_list(app):
    """
    GIVEN a Flask application
    WHEN the '/locations' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:

            # insert a location into the database
        location_1 = Location(address='123 test street', city='Kansas City',
            state='MO', zip_code=66213, latitude='39.123432', longitude='-83.123456')

        location_2 = Location(address='456 test way', city='Kansas City',
            state='KS', zip_code=66210, latitude='39.654321', longitude='-83.654321')

        db.session.add(location_1)
        db.session.add(location_2)
        db.session.commit()

        response = client.get('/locations')
        assert response.status_code == 200
        data = response.get_json()
        resp_locations = data.get('locations')
        assert resp_locations is not None
        assert json.dumps(resp_locations) == (
        '[{"id": "1", "address": "123 test street", "city": "Kansas City", "state": "MO", "zipCode": 66213, "latitude": 39.123432, "longitude": -83.123456}, {"id": "2", "address": "456 test way", "city": "Kansas City", "state": "KS", "zipCode": 66210, "latitude": 39.654321, "longitude": -83.654321}]')


def test_get_location_by_id(app):
    pass

def test_post_location(app):
    pass

def test_put_location(app):
    pass

def test_delete_location(app):
    pass

def test_get_project_list(app):
    pass

def test_get_project_by_id(app):
    pass

def test_post_project(app):
    pass

def test_put_project(app):
    pass

def test_delete_project(app):
    pass

def test_get_project_type_list(app):
    pass

def test_get_project_type_by_id(app):
    pass

def test_post_project_type(app):
    pass

def test_put_project_type(app):
    pass

def test_delete_project_type(app):
    pass
