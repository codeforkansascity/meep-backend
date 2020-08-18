from ..conftest import Project, db, ProjectType, Location

def test_new_project(new_project):
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check if the object is instantiated correctly
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
    """
    GIVEN a ProjectType model
    WHEN a new ProjectType is created
    THEN check if the object is instantiated correctly
    """
    assert new_projectType.id == 9
    assert new_projectType.type_name == "typeName"




def test_new_location(new_location):
    """
    GIVEN a Location model
    WHEN a new Location is created
    THEN check if the object is instantiated correctly
    """
    assert new_location.id == 5000
    assert new_location.address == "1 Infinite Loop"
    assert new_location.city == "Cupertino"
    assert new_location.state == "CA"
    assert new_location.zip_code == 95014
    assert new_location.location == "POINT(-94.668954 38.992762)"
    assert new_location.project_id == 79
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


def test_insert_location(app, new_location):
    """
    GIVEN a Flask application and a Location model
    WHEN a new location is added to the database
    THEN check if that location and its correct attributes are returned from
    the database
    """

    # insert locations into the database
    db.session.add(new_location)
    db.session.commit()

    selected_location = Location.query.filter_by(id=5).first()
    coords = selected_location.coords
    assert new_location.id == 5000
    assert new_location.address == "1 Infinite Loop"
    assert new_location.city == "Cupertino"
    assert new_location.state == "CA"
    assert new_location.zip_code == 95014
    assert coords.get("latitude") == 38.992762
    assert coords.get("longitude") == -94.668954
    assert new_location.project_id == 79
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


def test_update_location(app):
    """
    GIVEN a Flask application
    WHEN an existing location is updated
    THEN check if the updated location is correctly returned from the database
    """
    selected_location = Location.query.filter_by(id=5).first()
    assert selected_location.state == "CA"
    selected_location.state = "CO"
    db.session.commit()
    selected_location = Location.query.filter_by(id=5).first()
    assert selected_location.state == "CO"


def test_get_location_coordinates(app):
    """
    GIVEN a Flask application
    WHEN an existing location's location is queried
    THEN check if that location's coordinates are correctly returned from the
    database and that an unspecifed location correctly correctly returns None
    for its coordinates
    """
    selected_location = Location.query.filter_by(id=5).first()
    coords = selected_location.coords
    assert coords.get("latitude") == 38.992762
    assert coords.get("longitude") == -94.668954

    bad_location = Location(location=None)
    bad_coords = bad_location.coords
    assert bad_coords.get("latitude") is None
    assert bad_coords.get("longitude") is None
