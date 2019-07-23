import json

import pytest

from models import Location, db

def test_post_location(app):
    with app.test_client() as client:
        res = client.post(
            '/locations',
            json={
                'address': "123 test way",
                'city': "Kansas City",
                'state': "MO"
            }
        )

        [loc] = Location.query.all()
        assert res.status_code == 201
        assert loc.id == 1
        assert loc.address == "123 test way"
        assert loc.city == "Kansas City"
        assert loc.state == 'MO'
        assert loc.zip_code == None



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

    location_1 = Location(address='123 test street', city='Kansas City',
        state='MO', zip_code=66213, latitude='39.123432', longitude='-83.123456')
    db.session.add(location_1)
    db.session.commit()
    with app.test_client() as client:
        response = client.get('/locations/1')
        data = response.get_json()

    assert response.status_code == 200
    assert data.get('address') == '123 test street'
    assert data.get('city') == 'Kansas City'
    assert data.get('state') == 'MO'
    # attributes are camel cased
    assert data.get('zipCode') == 66213
    assert data.get('latitude') == 39.123432
    assert data.get('longitude') == -83.123456

def test_put_location(app):
    location = Location(address='123 test street', city='Kansas City',
        state='MO', zip_code=66213, latitude='39.123452', longitude='-83.123456')
    db.session.add(location)
    db.session.commit()
    del location
    with app.test_client() as client:
        response = client.put('/locations/1', json={'address': '456 testing way'})
    assert response.status_code == 200
    [location_copy, *_] = Location.query.all()
    assert location_copy.address == '456 testing way'
    assert location_copy.city == 'Kansas City'


def test_delete_location(app):
    location_1 = Location(address='123 test street', city='Kansas City',
        state='MO', zip_code=66213, latitude='39.123452', longitude='-83.123456')
    location_2 = Location(address='456 test way', city='Kansas City',
        state='KS', zip_code=66210, latitude='39.654321', longitude='-83.654321')
    db.session.add(location_1)
    db.session.add(location_2)
    db.session.commit()
    del location_1
    del location_2
    with app.test_client() as client:
        response = client.delete('/locations/1')
    assert response.status_code == 200
    [location_2_copy] = Location.query.all()
    assert location_2_copy.address == '456 test way'
    assert location_2_copy.city == 'Kansas City'
    assert location_2_copy.state == 'KS'
    assert location_2_copy.zip_code == 66210
    assert location_2_copy.latitude == 39.654321
    assert location_2_copy.longitude == -83.654321
