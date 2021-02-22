'''
basic operations for creating and dropping tables, resetting the database,
and seeding with data for development

to run as a script from the command line you need to enter 2 arguments: a command and a config. E.g.:

python db_operations.py drop test

python db_operations.py create dev

python db_operations.py seed dev

python db_operations.py reset test

Currently only dev and test configs work
'''
import sys
import urllib
from os import environ
from random import choice, random, randrange, uniform
from time import sleep, time

from string import punctuation

import essential_generators
from geopy import Point
from geopy.geocoders import GoogleV3

from app import create_app
from app.constants import states
from app.models import *


def reset(config='dev'):
    drop_tables(config)
    create_tables(config)
    seed_db(config)


def clear(config='dev'):
    drop_tables(config)
    create_tables(config)


def drop_tables(config='dev'):
    app = create_app(config)
    with app.app_context():
        db.drop_all()


def create_tables(config='dev'):
    app = create_app(config)
    with app.app_context():
        db.create_all()


def seed_db(config='dev'):
    app = create_app(config)
    with app.app_context():

        # project types
        building = ProjectType(type_name='Building')
        vehicle_transportation = ProjectType(
            type_name='Vehicle Transportation')
        infastructure_transportation = ProjectType(
            type_name='Infastructure Transportation')
        for pt in building, vehicle_transportation, infastructure_transportation:
            db.session.add(pt)

        # projects
        p1 = Project(name='Black Hills Energy- KS', year=2013,
                     gge_reduced=1995, ghg_reduced=2.5845225, type=building)
        p2 = Project(name='Central States Beverage Company', year=2012,
                     gge_reduced=2891.461077, ghg_reduced=1.133452742,
                     type=building)
        p3 = Project(name='City of Kansas City Missouri - CNG Shuttle',
                     year=2017, gge_reduced=269133.3, ghg_reduced=226.6102386,
                     type=infastructure_transportation)
        p4 = Project(name='City of Kansas City Missouri - CNG Vans',
                     year=2017, gge_reduced=87652.7, ghg_reduced=113.5540729,
                     type=vehicle_transportation)
        p5 = Project(name='Dart Long-Haul Fleet', year=2015,
                     gge_reduced=720000, ghg_reduced=606.24,
                     type=vehicle_transportation)
        p6 = Project(name='Lincoln Airport Authority -CNG', year=2017,
                     gge_reduced=11970, ghg_reduced=15.507135, type=building)
        p7 = Project(name=' State of Missouri - Propane', year=2017,
                     gge_reduced=903.101, ghg_reduced=1.276533264,
                     type=building)
        p8 = Project(name='Zarco 66 Heavy Duty B20', year=2014,
                     gge_reduced=1093.80128, ghg_reduced=9.578417809,
                     type=vehicle_transportation)

        # locations
        p1.locations.append(Location(address='601 N Iowa St', city='Lawrence', state='KS',
                                     zip_code=66044, location='POINT(38.9930314 -95.2632409)'))
        p2.locations.append(Location(address='14220 Wyandotte St', city='Kansas City', state='MO',
                                     zip_code=64145, location='POINT(38.8705357 -94.6095686)'))
        p3.locations.extend([
            Location(address='W 75th St & Wornall Rd', city='Kansas City', state='MO',
                     zip_code=64114, location='POINT(38.9924194 -94.5965102)'),
            Location(address='On 63rd & Brookside', city='Kansas City', state='MO',
                     zip_code=64113, location='POINT(39.0131619 -94.5921776)'),
            Location(address='On 63rd at Cherry Westbound', city='Kansas City', state='MO',
                     zip_code=64110, location='POINT(39.0146112 -94.5955968)'),
            Location(address='On 63rd at Paseo Westbound', city='Kansas City', state='MO',
                     zip_code=64110, location='POINT(39.0142199 -94.5758463)'),
            Location(address='On Brookside at 59th SB', city='Kansas City', state='MO',
                     zip_code=64113, location='POINT(39.0180454 -94.5919601)'),
            Location(address='On Brookside at 55th SB', city='Kansas City', state='MO',
                     zip_code=64113, location='POINT(39.0227138 -94.5935497)'),
            Location(address='On Brookside at 51st SB', city='Kansas City', state='MO',
                     zip_code=64112, location='POINT(39.0338538 -94.585571)')
        ])
        p4.locations.append(Location(address='100 NW Vivion Rd', city='Kansas City', state='MO',
                                     zip_code=64118, location='POINT(39.1650181 -94.6187879)'))
        p5.locations.extend([
            Location(address='8400 E Truman Rd', city='Kansas City', state='MO',
                     zip_code=64126, location='POINT(39.112502 -94.5194595)'),
            Location(address='4121 N Kentucky Ave', city='Kansas City', state='MO',
                     zip_code=64161, location='POINT(39.1128102 -94.7304727)')
        ])
        p6.locations.append(Location(address='3451-3599 W Luke St', city='Lincoln', state='NE',
                                     zip_code=68524, location='POINT(40.8502301 -96.7688027)'))
        p7.locations.append(Location(address='1101 Riverside Dr', city='Jefferson City', state='MO',
                                     zip_code=65101, location='POINT(38.57268 -92.1573004)'))
        p8.locations.extend([
            Location(address='2005 W 9th St', city='Lawrence', state='KS',
                     zip_code=66044, location='POINT(38.781587 -95.3452984)'),
            Location(address='2518 E Logan St', city='Ottowa', state='KS',
                     zip_code=66067, location='POINT(38.781587 -95.3452984)'),
            Location(address='1500 E 23rd St', city='Lawrence', state='KS',
                     zip_code=66044, location='POINT(38.912997 -95.2525864)'),
        ])

        for project in p1, p2, p3, p4, p5, p6, p7, p8:
            db.session.add(project)

        db.session.commit()


# Generate a seed database from random data rather than a static set like above.
def seed_db_rand(config='dev', count=5):
    app = create_app(config)
    with app.app_context():
        gen = essential_generators.DocumentGenerator()
        # project types
        building = ProjectType(type_name='Building')
        transportation = ProjectType(type_name='Transportation')
        for pt in building, transportation:
            db.session.add(pt)

        for p in range(count):
            # Generate Project Name
            projectName = gen.gen_sentence(
                min_words=1, max_words=3).capitalize().translate(str.maketrans('', '', punctuation))
            # pick project type
            ptype = choice([building, transportation])

            # construct project
            randProject = Project(
                id=p,
                name=projectName,
                description=gen.gen_sentence(),
                photo_url=gen.url(),
                website_url=gen.url(),
                year=randrange(2010, 2020),
                gge_reduced=uniform(500, 500000),
                ghg_reduced=uniform(1, 1000),
                type=ptype
            )
            geolocator = GoogleV3(api_key=environ.get("GOOGLE_API_KEY"))

            # construct location(s) (single for building, possibly more for transportation)
            locationCount = 1 if ptype == building else randrange(1, 5)
            for _ in range(0, locationCount):
                while True:
                    # Select a random point centered around KC (39.0997° N, 94.5786° W)
                    randLat = 39.0997 + uniform(-0.5, 0.5)
                    randLng = -94.5786 + uniform(-0.5, 0.5)
                    randPoint = Point(latitude=randLat, longitude=randLng)
                    t_s = time()
                    randLocation = geolocator.reverse(randPoint)
                    # Ensure location actually has the keys we need.
                    # We can assume it does if street number is present.
                    if randLocation.raw['address_components'][0]['types'][0] == 'street_number':
                        break

                    # Google allows up to 50 requests per second. Wait if we're doing more.
                    t_e = time()
                    if t_e - t_s < 0.02:
                        sleep(1-(t_e - t_s))
                randAddr = randLocation.raw['formatted_address']
                # Split up result into array delimited by commas.
                # 0 and 1 should always be Address and City, trimming to remove the whitespace after comma.
                # Grab the space-delimited State and ZIP from 2 (discard first entry as it's just the space)
                addrList = list(map(str.strip, randAddr.split(
                    ',')[:2])) + randAddr.split(',')[2].split(' ')[1:]
                randProject.locations.append(
                    Location(
                        address=addrList[0],
                        city=addrList[1],
                        state=addrList[2],
                        zip_code=addrList[3],
                        location=f'POINT({randLat} {randLng})'
                    )
                )

            db.session.add(randProject)
        db.session.commit()


if __name__ == '__main__':
    cmd = sys.argv[1]
    config = sys.argv[2]
    project_count = sys.argv[3] if len(sys.argv) > 3 else 5
    if config != 'dev' and config != 'test':
        print("Unknown config: Enter dev or test as 2nd argument")
    elif cmd == 'drop':
        drop_tables(config)
    elif cmd == 'create':
        create_tables(config)
    elif cmd == 'seed':
        seed_db(config)
    elif cmd == 'seed_rand':
        seed_db_rand(config, int(project_count))
    elif cmd == 'reset':
        reset(config)
    elif cmd == 'clear':
        clear(config)
    else:
        print('Unknown command. Use drop, create, or seed for 1st argument \
               and either dev or test for 2nd argument')
