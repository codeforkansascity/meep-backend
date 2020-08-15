import asyncio

def test_geocode_api(geocode_api, location_no_coords):
    location = asyncio.run(
        geocode_api.geocode_location(location_no_coords)
    )

    assert location.city == location_no_coords.city
    assert location.address == location_no_coords.address
    assert location.state == location_no_coords.state
    assert location.zip_code == 111111
    assert location.location == 'POINT(-97.3432 39.2343)'

def test_geocode_api_run(geocode_api):
    locations = geocode_api.run()