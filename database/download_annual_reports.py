import os
import re
from pprint import pprint

import pandas as pd
import requests

import sqlalchemy as sa

#shamelessly copied from stack overflow
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={ 'id' : id }, stream=True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


ids = {
    'locations': '1-jn_oDi7zjP-R1NZlM7hLl1o7ZsYKxgB',
    'projects': '19eAtW6hcA3yE0WYK-cOr0UQG_AFaxNT2'
}


def download_to_json(sheet):
    id = ids.get(sheet)
    if id is None:
        raise ValueError('invalid sheet')
    if 'temp' not in os.listdir():
        os.mkdir('temp')
    try:
        filename = f'./temp/{sheet}.csv'
        download_file_from_google_drive(id, filename)
        with open(filename, 'r') as f:
            lines = f.readlines()

    finally:
        os.remove(filename)
        os.rmdir('temp')

    columns, *data = (line.strip().split(',') for line in lines)
    objects = [dict(zip(columns, row)) for row in data]
    return objects


def format_location(location):
    location = dict((k, None) if not location[k] else (k, location[k]) for k in location)
    del location['id']
    address = location.get('address')
    location['address'] = address.strip() if address else None

    city = location.get('city')
    location['city'] = city.strip() if city else None

    latitude = format_latitude(location['latitude'])
    longitude = format_longitude(location['longitude'])
    if latitude and longitude:
        location['location'] = 'POINT({!s} {!s})'.format(latitude, longitude)
    else:
        return None

    del location['latitude']
    del location['longitude']

    location['zip_code'] = int(location['zip_code'].split('.')[0]) if location['zip_code'] else None
    location['state'] = state_abbreviations.get(location['state'])

    return location

lat_regex = re.compile(r'''(\d{1,2}).+(\d{1,2})\'(\d{1,2}\.\d{1,2})\"\"([NS])"''')

def format_latitude(lat):
    if not isinstance(lat, str):
        return None
    m = lat_regex.search(lat)
    if m:
        degrees = float(m.group(1))
        minutes = float(m.group(2)) / 60
        seconds = float(m.group(3)) / 60**2
        decimal = degrees + minutes + seconds
        return decimal if m.group(4) == 'N' else -decimal

lng_regex = re.compile(r'''(\d{1,2}).+(\d{1,2})\'(\d{1,2}\.\d{1,2})\"\"([EW])"''')

def format_longitude(long):
    if not isinstance(long, str):
        return None
    m = lng_regex.search(long)
    if m:
        degrees = float(m.group(1))
        minutes = float(m.group(2)) / 60
        seconds = float(m.group(3)) / 60**2
        decimal = degrees + minutes + seconds
        return decimal if m.group(4) == 'E' else -decimal

state_abbreviations = {
    ' MO"': 'MO',
    'Kansas': 'KS',
    'Missouri': 'MO',
    'Nebraska': 'NE'
}

def create_sqlalchemy_engine(connection_string=None):
    if connection_string is None:
        connection_string = os.environ.get('DEV_DATABASE_URL')
        if connection_string is None:
            raise ValueError('No connection string')
    return sa.create_engine(connection_string)



def bulk_insert(engine, table, values):
    connection = engine.connect()
    connection.execute(
        table.insert(),
        values
    )

def insert_locations_08_09_2019(connection_url):
    metadata = sa.MetaData()
    engine = create_sqlalchemy_engine(connection_url)
    locations_table = sa.Table('locations', metadata, autoload=True, autoload_with=engine)
    locations = download_to_json('locations')
    formatted = [format_location(loc) for loc in locations]
    filtered = filter(lambda loc: loc is not None, formatted)
    filtered = filter(lambda loc: loc.get('address') is not None, filtered)
    pprint(list(filtered))
    bulk_insert(locations_table, list(filtered))
