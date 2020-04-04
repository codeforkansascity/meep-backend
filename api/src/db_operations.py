"""
basic operations for creating and dropping tables, resetting the database,
and seeding with data for development

to run as a script from the command line you need to enter 2 arguments: a command and a config. E.g.:

python db_operations.py drop test

python db_operations.py create dev

python db_operations.py seed dev

python db_operations.py reset test

Currently only dev and test configs work
"""
import sys

from models import *
from app import create_app


def reset(config='dev'):
    drop_tables(config)
    create_tables(config)
    seed_db(config)


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
        # roles
        user = Role(role_name='user')
        admin = Role(role_name='admin')

        # users
        u1 = User(password_hash='bad password', email='greg@gmail.com')
        u1.role = user
        u2 = User(password_hash='another bad password', email='jane@gmail.com')
        u2.role = user
        u3 = User(password_hash='iu3o24hyiurhdskjfhirewufhe',
                  email='admin@yahoo.com')
        u3.role = admin
        u4 = User(password_hash='xckvjxcv98743mcvx32mnrewryfds',
                  email='ecokid@hotmail.com')

        for user in u1, u2, u3, u4:
            db.session.add(user)

        # project types
        building = ProjectType(type_name='Building')
        vehicle_transportation = ProjectType(
            type_name='Vehicle Transportation')
        infrastructure_transportation = ProjectType(
            type_name='Infrastructure Transportation')
        for pt in building, vehicle_transportation, infrastructure_transportation:
            db.session.add(pt)

        # projects
        p1 = Project(name='Black Hills Energy- KS', year=2013,
                     gge_reduced=1995, ghg_reduced=2.5845225, type=building)
        p2 = Project(name='Central States Beverage Company', year=2012,
                     gge_reduced=2891.461077, ghg_reduced=1.133452742,
                     type=building)
        p3 = Project(name='City of Kansas City Missouri - CNG Shuttle',
                     year=2017, gge_reduced=269133.3, ghg_reduced=226.6102386,
                     type=infrastructure_transportation)
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


if __name__ == '__main__':
    cmd = sys.argv[1]
    config = sys.argv[2]
    if config != 'dev' and config != 'test':
        print("Unknown config: Enter dev or test as 2nd argument")
    elif cmd == 'drop':
        drop_tables(config)
    elif cmd == 'create':
        create_tables(config)
    elif cmd == 'seed':
        seed_db(config)
    elif cmd == 'reset':
        reset(config)
    else:
        print('Unknown command. Use drop, create, or seed for 1st argument \
               and either dev or test for 2nd argument')
