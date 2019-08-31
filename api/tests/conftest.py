import pytest
from app import create_app
from models import User, Role, Project, db, ProjectType
from db_operations import reset


@pytest.fixture(scope='function')
def new_user():
    user = User('evan@aol.com', '1289rhth')
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
        ghg_reduced=2.234
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
        address="7510 Floyd St",
        city="Overland Park",
        state="KS",
        zip_code=66204,
        location='POINT(-94.668954 38.992762)',
        project_id=1
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
