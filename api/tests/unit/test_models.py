from app import create_app
from models import User, Role, Project, db, ProjectType, Location


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check if the object is instantiated correctly
    """
    assert new_user.email == "evan@aol.com"
    assert new_user.password_hash == "1289rhth"
    assert new_user.id == 42
    assert new_user.json == {
        "email": "evan@aol.com",
        "id": 42,
        "password_hash": "1289rhth",
        "role_id": None,
    }


def test_new_role(new_role):
    """
    GIVEN a Role model
    WHEN a new Role is created
    THEN check if the object is instantiated correctly
    """
    assert new_role.role_name == "admin"
    assert new_role.id == 42
    assert new_role.json == {"id": 42, "role_name": "admin"}


def test_user_role(new_user, new_role):
    """
    GIVEN a User and Role model
    WHEN a Role is associated with a User model
    THEN check if the objects are associated correctly
    """
    new_user.role_id = new_role.id
    new_user.role = new_role
    assert new_user.role_id == 42
    assert new_user.role.id == 42
    assert new_user.role.role_name == "admin"
    assert new_user.role.json == {"id": 42, "role_name": "admin"}


def test_new_project(new_project):
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check if the object is instantiated correctly
    """
    assert new_project.id == 42
    assert new_project.name == "someTestName"
    assert new_project.description == "testDescription"
    assert new_project.photo_url == "www.google.com"
    assert new_project.website_url == "www.aol.com"
    assert new_project.year == 1999
    assert new_project.gge_reduced == 1.234
    assert new_project.ghg_reduced == 2.234
    assert new_project.json == {
        "description": "testDescription",
        "gge_reduced": 1.234,
        "ghg_reduced": 2.234,
        "id": 42,
        "name": "someTestName",
        "photo_url": "www.google.com",
        "project_type_id": None,
        "website_url": "www.aol.com",
        "year": 1999,
    }


def test_new_projectType(new_projectType):
    """
    GIVEN a ProjectType model
    WHEN a new ProjectType is created
    THEN check if the object is instantiated correctly
    """
    assert new_projectType.id == 42
    assert new_projectType.type_name == "typeName"
    assert new_projectType.json == {"id": 42, "type_name": "typeName"}


def test_project_type(new_project, new_projectType):
    """
    GIVEN a Project and ProjectType model
    WHEN a ProjectType is associated with a Project model
    THEN check if the objects are associated correctly
    """
    new_project.project_type_id = new_projectType.id
    new_project.type = new_projectType
    assert new_project.project_type_id == 42
    assert new_project.type.id == 42
    assert new_project.type.type_name == "typeName"
    assert new_project.type.json == {"id": 42, "type_name": "typeName"}


def test_new_location(new_location):
    """
    GIVEN a Location model
    WHEN a new Location is created
    THEN check if the object is instantiated corectly
    """
    assert new_location.id == 42
    assert new_location.address == "1 Infinite Loop"
    assert new_location.city == "Cupertino"
    assert new_location.state == "CA"
    assert new_location.zip_code == 95014
    assert new_location.location == "POINT(-94.668954 38.992762)"
    assert new_location.json == {
        "address": "1 Infinite Loop",
        "city": "Cupertino",
        "id": 42,
        "location": "POINT(-94.668954 38.992762)",
        "project_id": None,
        "state": "CA",
        "zip_code": 95014,
    }


def test_location_project(new_location, new_project):
    """
    GIVEN a Location and Project model
    WHEN a Project is associated with a Location model
    THEN check if the objects are associated correctly
    """
    new_location.project_id = new_project.id
    new_location.project = new_project
    assert new_location.project_id == 42
    assert new_location.project.id == 42
    assert new_location.project.name == "someTestName"
    assert new_location.project.description == "testDescription"
    assert new_location.project.photo_url == "www.google.com"
    assert new_location.project.website_url == "www.aol.com"
    assert new_location.project.year == 1999
    assert new_location.project.gge_reduced == 1.234
    assert new_location.project.ghg_reduced == 2.234
    assert new_location.project.json == {
        "description": "testDescription",
        "gge_reduced": 1.234,
        "ghg_reduced": 2.234,
        "id": 42,
        "name": "someTestName",
        "photo_url": "www.google.com",
        "project_type_id": None,
        "website_url": "www.aol.com",
        "year": 1999,
    }
