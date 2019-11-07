import os
import json
import sys
import asyncio

from model import Location
from geocoder import GoogleGeocodingClient
from db import DatabaseManager


class GeocodingService:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = json.loads(f.read())
        self.client = GoogleGeocodingClient(**config['client'])
        self.db = DatabaseManager(**config['db'])

    async def geocode_location(self, location):
        data = await self.client._geocode_async(location.address, location.city, location.state)
        geocoded_loc = Location(id=location.id, **data)
        return geocoded_loc

    async def geocode_locations(self, locations):
        tasks = (self.geocode_location(loc) for loc in locations)
        return await asyncio.gather(*tasks)

    def run(self):
        locations = self.db.select_all_locations()
        geocoded_locs = asyncio.run(self.geocode_locations(locations))
        self.db.bulk_update_locations((loc for loc in geocoded_locs if loc.latitude and loc.longitude))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        path_to_config = os.environ.get('GEOCODING_SERVICE_CONFIG')
    elif len(sys.argv) == 2:
        path_to_config = sys.argv[1]
    else:
        raise TypeError(f'Invalid number ({len(sys.argv) - 1}) of command line arguments. Expected 0 or 1.')

    service = GeocodingService(path_to_config)
    service.run()
