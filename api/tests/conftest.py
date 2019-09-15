import pytest
from app import create_app
from models import User, Role, Project, db, ProjectType, Location
from db_operations import reset


@pytest.fixture(scope='function')
def new_user():
    user = User('evan@aol.com', '1289rhth')
    user.id = 42
    return user


@pytest.fixture(scope='function')
def new_role():
    role = Role(role_name="admin", id=42)
    role.id = 42
    return role


@pytest.fixture(scope='function')
def new_project():
    project = Project(
        id=42,
        name="someTestName",
        description="testDescription",
        photo_url="www.google.com",
        website_url="www.aol.com",
        year=1999,
        gge_reduced=1.234,
        ghg_reduced=2.234
    )
    return project

@pytest.fixture(scope='function')
def another_project():
    project = Project(
        id=43,
        name="anotherTestName",
        description="anotherDescription",
        photo_url="www.yahoo.com",
        website_url="www.myspace.com",
        year=2000,
        gge_reduced=3.234,
        ghg_reduced=4.234,
    )
    return project


@pytest.fixture(scope='function')
def new_projectType():
    projectType = ProjectType(
        id=42,
        type_name="typeName"
    )
    return projectType


@pytest.fixture(scope='function')
def new_location():
    location = Location(
        id=42,
        address="1 Infinite Loop",
        city="Cupertino",
        state="CA",
        zip_code=95014,
        location='POINT(-94.668954 38.992762)'
    )
    return location

@pytest.fixture(scope='function')
def another_location():
    location = Location(
        address="456 test way",
        city="Kansas City",
        state="KS",
        zip_code=66210,
        location='POINT(-83.654321 39.654321)',
    )
    return location


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
