def test_locations_list(test_client):
    """
    GIVEN a Flask application
    WHEN the '/locations' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/locations')
    assert response.status_code == 200
    assert b"Black Hills" in response.data
    assert b"2891.461077" in response.data
    assert b"2017" in response.data
    assert b"1.276533264" in response.data

def test_location(test_client):
    """
    GIVEN a Flask application
    WHEN the '/locations/2' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/locations/2')
    assert response.status_code == 200
    assert b"14220 Wyandotte St" in response.data
    assert b"Kansas City" in response.data
    assert b"MO" in response.data
    assert b"64145" in response.data
    assert b"38.8705357" in response.data
    assert b"-94.6095686" in response.data