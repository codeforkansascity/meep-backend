from models import db, User, Role, Project, ProjectType, Location


def test_insert_user(app, new_user):
    """
    GIVEN a Flask application and a User model
    WHEN a new user is added to the database
    THEN check if that user and its correct attributes are returned from
    the database
    """
    db.session.add(new_user)
    db.session.commit()
    selected_user = User.query.filter_by(email="evan@aol.com").first()
    assert selected_user is new_user
    assert selected_user.password_hash == "1289rhth"
    assert selected_user.email == "evan@aol.com"


def test_update_user(app):
    """
    GIVEN a Flask application
    WHEN an existing user is updated
    THEN check if the updated user is correctly returned from the database
    """
    selected_user = User.query.filter_by(email="evan@aol.com").first()
    assert selected_user.email == "evan@aol.com"
    selected_user.email = "evan@geocities.com"
    db.session.commit()
    selected_user = User.query.filter_by(id=selected_user.id).first()
    assert selected_user.email == "evan@geocities.com"


def test_delete_user(app):
    """
    GIVEN a Flask application
    WHEN an existing user is deleted from the database
    THEN check if that user is actually deleted from the database
    """
    selected_user = User.query.filter_by(email="evan@geocities.com").first()
    assert selected_user.email == "evan@geocities.com"
    db.session.delete(selected_user)
    db.session.commit()
    selected_user = User.query.filter_by(id=selected_user.id).first()
    assert selected_user is None
    selected_user = User.query.filter_by(email="evan@geocities.com").first()
    assert selected_user is None


def test_insert_project(app, new_project):
    """
    GIVEN a Flask application and a Project model
    WHEN a new project is added to the database
    THEN check if that project and its correct attributes are returned from
    the database
    """
    db.session.add(new_project)
    db.session.commit()
    selected_project = Project.query.filter_by(name="someTestName").first()
    assert selected_project is new_project
    assert selected_project.name == "someTestName"
    assert selected_project.description == "testDescription"
    assert selected_project.photo_url == "www.google.com"
    assert selected_project.website_url == "www.aol.com"
    assert selected_project.year == 1999
    assert selected_project.gge_reduced == 1.234
    assert selected_project.ghg_reduced == 2.234


def test_update_project(app):
    """
    GIVEN a Flask application
    WHEN an existing project is updated
    THEN check if the updated project is correctly returned from the database
    """
    selected_project = Project.query.filter_by(name="someTestName").first()
    assert selected_project.description == "testDescription"
    selected_project.description = "updatedDescription"
    db.session.commit()
    selected_project = Project.query.filter_by(id=selected_project.id).first()
    assert selected_project.description == "updatedDescription"


def test_delete_project(app):
    """
    GIVEN a Flask application
    WHEN an existing project is deleted from the database
    THEN check if that project is actually deleted from the database
    """
    selected_project = Project.query.filter_by(name="someTestName").first()
    assert selected_project.name == "someTestName"
    db.session.delete(selected_project)
    db.session.commit()
    selected_project = Project.query.filter_by(id=selected_project.id).first()
    assert selected_project is None
    selected_project = Project.query.filter_by(name="someTestName").first()
    assert selected_project is None


def test_insert_projectType(app, new_projectType):
    """
    GIVEN a Flask application and a ProjectType model
    WHEN a new project type is added to the database
    THEN check if that project type and its correct attributes are returned
    from the database
    """
    db.session.add(new_projectType)
    db.session.commit()
    selected_projectType = ProjectType.query.filter_by(
        type_name="typeName"
    ).first()
    assert selected_projectType is new_projectType
    assert selected_projectType.type_name == "typeName"


def test_update_projectType(app):
    """
    GIVEN a Flask application
    WHEN an existing project type is updated
    THEN check if the updated project type is correctly returned from the
    database
    """
    selected_projectType = ProjectType.query.filter_by(
        type_name="typeName"
    ).first()
    assert selected_projectType.type_name == "typeName"
    selected_projectType.type_name = "updatedTypeName"
    db.session.commit()
    selected_projectType = ProjectType.query.filter_by(
        id=selected_projectType.id
    ).first()
    assert selected_projectType.type_name == "updatedTypeName"


def test_delete_projectType(app):
    """
    GIVEN a Flask application
    WHEN an existing projectType is deleted from the database
    THEN check if that projectType is actually deleted from the database
    """
    selected_projectType = ProjectType.query.filter_by(
        type_name="updatedTypeName"
    ).first()
    assert selected_projectType.type_name == "updatedTypeName"
    db.session.delete(selected_projectType)
    db.session.commit()
    selected_projectType = ProjectType.query.filter_by(
        id=selected_projectType.id
    ).first()
    assert selected_projectType is None
    selected_projectType = ProjectType.query.filter_by(
        type_name="updatedTypeName"
    ).first()
    assert selected_projectType is None


def test_insert_location(app, new_location):
    """
    GIVEN a Flask application and a Location model
    WHEN a new location is added to the database
    THEN check if that location and its correct attributes are returned from
    the database
    """
    db.session.add(new_location)
    db.session.commit()
    selected_location = Location.query.filter_by(
        address="1 Infinite Loop"
    ).first()
    assert selected_location is new_location
    assert selected_location.address == "1 Infinite Loop"
    assert selected_location.city == "Cupertino"
    assert selected_location.state == "CA"
    assert selected_location.zip_code == 95014
    coords = selected_location.coords
    assert coords.get("latitude") == 38.992762
    assert coords.get("longitude") == -94.668954


def test_get_location_coordinates(app):
    """
    GIVEN a Flask application
    WHEN an existing location's location attribute is queried
    THEN check if that location's coordinates are correctly returned from the
    database and that an unspecifed location correctly returns None for its
    coordinates
    """
    selected_location = Location.query.filter_by(
        address="1 Infinite Loop"
    ).first()
    coords = selected_location.coords
    assert coords.get("latitude") == 38.992762
    assert coords.get("longitude") == -94.668954
    bad_location = Location(location=None)
    bad_coords = bad_location.coords
    assert bad_coords.get("latitude") is None
    assert bad_coords.get("longitude") is None


def test_update_location(app):
    """
    GIVEN a Flask application
    WHEN an existing location is updated
    THEN check if the updated location is correctly returned from the database
    """
    selected_location = Location.query.filter_by(
        address="1 Infinite Loop"
    ).first()
    assert selected_location.state == "CA"
    selected_location.state = "CO"
    db.session.commit()
    selected_location = Location.query.filter_by(
        id=selected_location.id
    ).first()
    assert selected_location.state == "CO"


def test_delete_location(app):
    """
    GIVEN a Flask application
    WHEN an existing location is deleted from the database
    THEN check if that location is actually deleted from the database
    """
    selected_location = Location.query.filter_by(
        address="1 Infinite Loop"
    ).first()
    assert selected_location.address == "1 Infinite Loop"
    db.session.delete(selected_location)
    db.session.commit()
    selected_location = Location.query.filter_by(
        id=selected_location.id
    ).first()
    assert selected_location is None
    selected_location = Location.query.filter_by(
        address="1 Infinite Loop"
    ).first()
    assert selected_location is None
