import pytest
from app import create_app
from models import User, Role, Project, db, ProjectType, Location
from db_operations import reset


@pytest.fixture(scope='function')
def new_user():
    user = User('evan@aol.com', '1289rhth')
    user.id = 456
    user.role_id = 2
    user.role = Role(id=2, role_name="user")
    return user


@pytest.fixture(scope='function')
def new_role():
    role = Role(id=8, role_name="admin")
    return role


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


@pytest.fixture(scope='session')
def app():
    app = create_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
