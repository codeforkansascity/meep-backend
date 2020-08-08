import pytest

from .. import create_app
from ..models import Project, db, ProjectType, Location
from db_operations import reset
from ..services.geocoder.client import GoogleGeocodingClient
from ..services.geocoder.api import GeocodingApi


@pytest.fixture(scope='function')
def new_project():
    project = Project(
        id=1,
        name="testName",
        description="testDescription",
        photo_url="www.google.com",
        website_url="www.aol.com",
        year=1999,
        gge_reduced=1.234,
        ghg_reduced=2.234,
        project_type_id=3,
        type=ProjectType(id=3, type_name="someType")
    )
    return project

@pytest.fixture(scope='function')
def new_projectType():
    projectType = ProjectType(
        id=9,
        type_name="typeName"
    )
    return projectType

@pytest.fixture(scope='function')
def new_location():
    location = Location(
        id=5,
        address="1 Infinite Loop",
        city="Cupertino",
        state="CA",
        zip_code=95014,
        location='POINT(-94.668954 38.992762)',
        project_id=79,
        project=Project(
            id=79,
            name="testName",
            description="testDescription",
            photo_url="www.google.com",
            website_url="www.aol.com",
            year=1999,
            gge_reduced=1.234,
            ghg_reduced=2.234,
            project_type_id=3,
            type=ProjectType(id=3, type_name="someType")
            )
    )
    return location

@pytest.fixture(scope='function')
def location_no_coords():
    location = Location(
        id=8,
        address="1234 Main St",
        city="Kansas City",
        state="KS",
        zip_code=66101,
        location=None,
        project_id=8,
        project=Project(
            id=8,
            name="Something",
            description="AnothertestDescription",
            photo_url="www.google.com/images/2343",
            website_url="www.aol.com/we-still-use-this",
            year=2020,
            gge_reduced=122.234,
            ghg_reduced=2343.234,
            project_type_id=7,
            type=ProjectType(id=7, type_name="someType")
        )
    )
    return location


@pytest.fixture(scope='function')
def geocode_api():
    import asyncio
    class Client(GoogleGeocodingClient):
        async def _geocode_async(self, address, city, state):
            return {
                'address': address,
                'city': city,
                'state': state,
                'zip_code': 111111,
                'latitude': 39.2343,
                'longitude': -97.3432
            }
    
    client = Client('fake_api_key')
    geocode_api = GeocodingApi('fake_api_key')
    geocode_api.client = client
    return geocode_api

@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
