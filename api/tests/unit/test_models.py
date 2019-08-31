from app import create_app
from models import User, Role, Project, db, ProjectType, Location


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check if email is defined correctly
    """
    assert new_user.id == 456
    assert new_user.email == 'evan@aol.com'
    assert new_user.password_hash == '1289rhth'
    assert new_user.role_id == 2
    assert new_user.role.role_name == 'user'


def test_new_role(new_role):
    """
    GIVEN a Role model
    WHEN a new Role is created
    THEN check if role_name is defined correctly
    """
    assert new_role.id == 8
    assert new_role.role_name == "admin"


def test_new_project(new_project):
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check if their fields are defined correctly
    """
    assert new_project.id == 1
    assert new_project.name == "testName"
    assert new_project.description == "testDescription"
    assert new_project.photo_url == "www.google.com"
    assert new_project.website_url == "www.aol.com"
    assert new_project.year == 1999
    assert new_project.gge_reduced == 1.234
    assert new_project.ghg_reduced == 2.234
    assert new_project.project_type_id == 3
    assert new_project.type.id == 3
    assert new_project.type.type_name == "someType"


def test_new_projectType(new_projectType):
    assert new_projectType.id == 9
    assert new_projectType.type_name == "typeName"


def test_new_location(new_location):
    assert new_location.id == 5
    assert new_location.address == "1 Infinite Loop"
    assert new_location.city == "Cupertino"
    assert new_location.state == "CA"
    assert new_location.zip_code == 95014
    assert new_location.latitude == 38.992762
    assert new_location.longitude == -94668954
    assert new_location.project_id == 2
    assert new_location.project.id == 2
    assert new_location.project.name == "testName"
    assert new_location.project.description == "testDescription"
    assert new_location.project.photo_url == "www.google.com"
    assert new_location.project.website_url == "www.aol.com"
    assert new_location.project.year == 1999
    assert new_location.project.gge_reduced == 1.234
    assert new_location.project.ghg_reduced == 2.234
    assert new_location.project.project_type_id == 3
    assert new_location.project.type.id == 3
    assert new_location.project.type.type_name == "someType"


def test_insert_location(app):
    location = Location(address='123 testing way')
    db.session.add(location)
    db.session.commit()
    assert location is not None


def test_select_location(app):
    location = Location(address='456 test drive', state='CA')
    db.session.add(location)
    db.session.commit()
    selected_location = Location.query.filter_by(state='CA').first()
    assert selected_location.address == '456 test drive'


def test_update_location(app):
    location = Location(address='789 test road', state='CA')
    db.session.add(location)
    db.session.commit()
    selected_location = Location.query.filter_by(address='789 test road').first()
    assert selected_location.state == 'CA'
    selected_location.state = 'CO'
    db.session.commit()
    selected_location = Location.query.filter_by(address='789 test road').first()
    assert selected_location.state == 'CO'