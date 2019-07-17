import pytest
from app import create_app
from models import User, Role, Project, db, ProjectType


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
        latitude=38.992762,
        longitude=-94668954,
        project_id=1
    )
    return location


@pytest.fixture(scope='session')
def test_client():
    flask_app = create_app(config_name='test')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


# @pytest.fixture(scope='module')
# def init_database():
#     # Create the database and the database table
#     db.create_all()
#
#     # Insert user data
#     app = create_app('dev')
#     with app.app_context():
#         # project types
#         building = ProjectType(type_name='Building')
#         vehicle_transportation = ProjectType(type_name='Vehicle Transportation')
#         infastructure_transportation = ProjectType(type_name='Infastructure Transportation')
#         for pt in building, vehicle_transportation, infastructure_transportation:
#             db.session.add(pt)
#
#     yield db  # this is where the testing happens!
#
#     db.drop_all()