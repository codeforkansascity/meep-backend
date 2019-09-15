

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

    selected_location = Location.query.filter_by(address="1 Infinite Loop").first()
    coords = selected_location.coords
    assert new_location.address == "1 Infinite Loop"
    assert new_location.city == "Cupertino"
    assert new_location.state == "CA"
    assert new_location.zip_code == 95014
    assert coords.get("latitude") == 38.992762
    assert coords.get("longitude") == -94.668954


def test_update_location(app):
    """
    GIVEN a Flask application
    WHEN an existing location is updated
    THEN check if the updated location is correctly returned from the database
    """
    selected_location = Location.query.filter_by(address="1 Infinite Loop").first()
    assert selected_location.state == "CA"
    selected_location.state = "CO"
    db.session.commit()
    selected_location = Location.query.filter_by(address="1 Infinite Loop").first()
    assert selected_location.state == "CO"


def test_get_location_coordinates(app):
    """
    GIVEN a Flask application
    WHEN an existing location's location is queried
    THEN check if that location's coordinates are correctly returned from the
    database and that an unspecifed location correctly correctly returns None
    for its coordinates
    """
    selected_location = Location.query.filter_by(address="1 Infinite Loop").first()
    assert selected_location.location == 'POINT(-94.668954 38.992762)'
    bad_location = Location(location=None)
    bad_coords = bad_location.coords
    assert bad_coords.get("latitude") is None
    assert bad_coords.get("longitude") is None
