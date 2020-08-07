import os, json, sys, asyncio
from .service import Location
from sqlalchemy import or_
from geoalchemy2 import Geometry
from .client import GoogleGeocodingClient
from typing import List
from .service import Location, db, Session, queries

def get_all_locations(session):
    session = Session()
    return 

class GeocodingApi:
    def __init__(self, apikey):
        self.client = GoogleGeocodingClient(apikey)

    async def geocode_location(self, location: Location):
        assert isinstance(location, Location)
        '''We modify the instance, but leave it up to the caller to create
        a session and commit the change.

        This allows for bulk updates on a single commit.
        '''

        r = await self.client._geocode_async(
            location.address, 
            location.city, 
            location.state
        )

        if r['longitude'] and r['latitude']:
            location.location = f'POINT({r.longitude},{r.latitude})'
        location.address = r['address'] 
        location.city = r['city'] 
        location.state = r['state'] 
        location.zip_code = r['zip_code']
        return location

    async def geocode_locations(self, locations: List[Location]):
        tasks = (self.geocode_location(loc) for loc in locations)
        return await asyncio.gather(*tasks)

    def run(self):
        session = Session()
        locations = session.query(Location).filter(
                Location.address != None,
                Location.city != None,
                Location.state != None,
                or_(Location.location != None, Location.zip_code == None)
            ).all()
        locations = asyncio.run(self.geocode_locations(locations))
        session.commit()