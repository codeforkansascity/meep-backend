import json
from operator import itemgetter

from flask import current_app
import pytest
from sqlalchemy import func

from app import create_app
from models import Location, Project, ProjectType, db


def test_get_locations_list(app):
    """
    GIVEN a Flask application
    WHEN the '/locations' page is requested (GET)
    THEN check the response is valid
    """

    # insert a location into the database
    location_1 = Location(address='123 test street', city='Kansas City',
        state='MO', zip_code=66213, location='POINT(-83.123456 39.123432)')

    location_2 = Location(address='456 test way', city='Kansas City',
        state='KS', zip_code=66210, location='POINT(-83.654321 39.654321)')

    db.session.add(location_1)
    db.session.add(location_2)
    db.session.commit()
    with app.test_client() as client:
        response = client.get('/locations')
        assert response.status_code == 200
        data = response.get_json()
        resp_locations = sorted(data.get('locations'), key=itemgetter('address'))
        assert resp_locations is not None

        test_location1 = {"id": resp_locations[0].get("id"), "address": "123 test street", "city": "Kansas City", "state": "MO", "zipCode": 66213, "longitude": -83.123456, "latitude": 39.123432 }
        test_location2 = {"id": resp_locations[1].get("id"), "address": "456 test way", "city": "Kansas City", "state": "KS", "zipCode": 66210, "longitude": -83.654321, "latitude": 39.654321 }
        assert resp_locations == [test_location1, test_location2]


def test_get_location_by_id(app):
    location = Location(address='123 test street', city='Kansas City',
        state='MO', zip_code=66213, location='POINT(-83.123456 39.123432)')
    db.session.add(location)
    db.session.commit()
    id = db.session.scalar(func.max(Location.id))
    with app.test_client() as client:
        response = client.get(f'/locations/{id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            'address': '123 test street',
            'city': 'Kansas City',
            'state': 'MO',
            'zipCode': 66213,
            'latitude': 39.123432,
            'longitude': -83.123456
        }


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
