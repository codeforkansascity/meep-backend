import json
from operator import itemgetter

from flask import current_app
import pytest
from sqlalchemy import func

from app import create_app
from models import Location, Project, ProjectType, db


def test_get_projects_list(app, new_project, another_project):
    """
    GIVEN a Flask application and two projects added to the database
    WHEN the '/api/projects' page is requested (GET)
    THEN check the response is correct
    """
    db.session.add(new_project)
    db.session.add(another_project)
    db.session.commit()

    with app.test_client() as client:
        response = client.get("/projects")
        assert response.status_code == 200
        data = response.get_json()
        resp_projects = sorted(data.get("projects"), key=itemgetter("id"))
        test_new_project = {
            "id": resp_projects[0].get("id"),
            "name": "someTestName",
            "description": "testDescription",
            "photoUrl": "www.google.com",
            "websiteUrl": "www.aol.com",
            "year": 1999,
            "ggeReduced": 1.234,
            "ghgReduced": 2.234,
        }
        test_another_project = {
            "id": resp_projects[1].get("id"),
            "name": "anotherTestName",
            "description": "anotherDescription",
            "photoUrl": "www.yahoo.com",
            "websiteUrl": "www.myspace.com",
            "year": 2000,
            "ggeReduced": 3.234,
            "ghgReduced": 4.234,
        }
        assert resp_projects is not None
        assert resp_projects == [test_new_project, test_another_project]


def test_get_project_by_id(app, new_project):
    """
    GIVEN a Flask application and a project added to the database
    WHEN the '/api/projects/{id}' page is requested (GET)
    THEN check the response is correct
    """
    with app.test_client() as client:
        response = client.get(f"/projects/{new_project.id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "description": "testDescription",
            "ggeReduced": 1.234,
            "ghgReduced": 2.234,
            "name": "someTestName",
            "photoUrl": "www.google.com",
            "websiteUrl": "www.aol.com",
            "year": 1999,
        }


def test_post_project(app):
    pass


def test_put_project(app):
    pass


def test_delete_project(app):
    pass


def test_get_locations_list(app, new_location, another_location):
    """
    GIVEN a Flask application and two locations added to the database
    WHEN the '/api/locations' page is requested (GET)
    THEN check the response is correct
    """
    with app.test_client() as client:
        db.session.add(new_location)
        db.session.add(another_location)
        db.session.commit()
        response = client.get("/locations")
        assert response.status_code == 200
        data = response.get_json()
        resp_locations = sorted(
            data.get("locations"), key=itemgetter("address")
        )
        assert resp_locations is not None
        test_new_location = {
            "id": resp_locations[0].get("id"),
            "address": "1 Infinite Loop",
            "city": "Cupertino",
            "state": "CA",
            "zipCode": 95014,
            "longitude": -94.668954,
            "latitude": 38.992762,
        }
        test_another_location = {
            "id": resp_locations[1].get("id"),
            "address": "456 test way",
            "city": "Kansas City",
            "state": "KS",
            "zipCode": 66210,
            "longitude": -83.654321,
            "latitude": 39.654321,
        }
        assert resp_locations == [test_new_location, test_another_location]


def test_get_location_by_id(app, new_location):
    """
    GIVEN a Flask application and a location added to the database
    WHEN the '/api/locations/{id}' page is requested (GET)
    THEN check the response is correct
    """
    with app.test_client() as client:
        response = client.get(f"/locations/{new_location.id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "address": "1 Infinite Loop",
            "city": "Cupertino",
            "state": "CA",
            "zipCode": 95014,
            "latitude": 38.992762,
            "longitude": -94.668954,
        }


def test_post_location(app):
    pass


def test_put_location(app):
    pass


def test_delete_location(app):
    pass
