import sys

from app import db
from models import *
from app import create_app

def reset():
    drop_tables()
    create_tables()
    seed_db()

def drop_tables():
    app = create_app('dev')
    with app.app_context():
        db.drop_all()

def create_tables():
    app = create_app('dev')
    with app.app_context():
        db.create_all()

def seed_db():
    app = create_app('dev')
    with app.app_context():
        #roles
        user = Role(role_name = 'user')
        admin = Role(role_name = 'admin')

        #users
        u1 = User(password_hash='bad password', email='greg@gmail.com')
        u1.role = user
        u2 = User(password_hash='another bad password', email='jane@gmail.com')
        u2.role = user
        u3 = User(password_hash='iu3o24hyiurhdskjfhirewufhe', email='admin@yahoo.com')
        u3.role = admin
        u4 = User(password_hash='xckvjxcv98743mcvx32mnrewryfds', email='ecokid@hotmail.com')

        for user in u1, u2, u3, u4:
            db.session.add(user)

        #project types
        building = ProjectType(type_name='Building')
        vehicle_transportation = ProjectType(type_name='Vehicle Transportation')
        infastructure_transportation = ProjectType(type_name='Infastructure Transportation')
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
        p1.locations.append(Location(address='601 N Iowa St', city='Lawrence', state='KS', zip_code=66044, latitude=38.9930314, longitude=-95.2632409))
        p2.locations.append(Location(address='14220 Wyandotte St', city='Kansas City', state='MO', zip_code=64145, latitude=38.8705357, longitude=-94.6095686))
        p3.locations.extend([
            Location(address='W 75th St & Wornall Rd', city='Kansas City', state='MO', zip_code=64114, latitude=38.9924194, longitude=-94.5965102),
            Location(address='On 63rd & Brookside', city='Kansas City', state='MO', zip_code=64113, latitude=39.0131619, longitude=-94.5921776),
            Location(address='On 63rd at Cherry Westbound', city='Kansas City', state='MO', zip_code=64110, latitude=39.0146112, longitude=-94.5955968),
            Location(address='On 63rd at Paseo Westbound', city='Kansas City', state='MO', zip_code=64110, latitude=39.0142199, longitude=-94.5758463),
            Location(address='On Brookside at 59th SB', city='Kansas City', state='MO', zip_code=64113, latitude=39.0180454, longitude=-94.5919601),
            Location(address='On Brookside at 55th SB', city='Kansas City', state='MO', zip_code=64113, latitude=39.0227138, longitude=-94.5935497),
            Location(address='On Brookside at 51st SB', city='Kansas City', state='MO', zip_code=64112, latitude=39.0338538, longitude=-94.585571)
        ])
        p4.locations.append(Location(address='100 NW Vivion Rd', city='Kansas City', state='MO', zip_code=64118, latitude=39.1650181, longitude=-94.6187879))
        p5.locations.extend([
            Location(address='8400 E Truman Rd', city='Kansas City', state='MO', zip_code=64126, latitude=39.112502, longitude=-94.5194595),
            Location(address='4121 N Kentucky Ave', city='Kansas City', state='MO', zip_code=64161, latitude=39.1128102, longitude=-94.7304727)
        ])
        p6.locations.append(Location(address='3451-3599 W Luke St', city='Lincoln', state='NE', zip_code=68524, latitude=40.8502301, longitude=-96.7688027))
        p7.locations.append(Location(address='1101 Riverside Dr', city='Jefferson City', state='MO', zip_code=65101, latitude=38.57268, longitude=-92.1573004))
        p8.locations.extend([
            Location(address='2005 W 9th St', city='Lawrence', state='KS', zip_code=66044, latitude=38.781587, longitude=-95.3452984),
            Location(address='2518 E Logan St', city='Ottowa', state='KS', zip_code=66067, latitude=38.781587, longitude=-95.3452984),
            Location(address='1500 E 23rd St', city='Lawrence', state='KS', zip_code=66044, latitude=38.912997, longitude=-95.2525864),
        ])

        for project in p1, p2, p3, p4, p5, p6, p7, p8:
            db.session.add(project)

        db.session.commit()

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'drop':
        drop_tables()
    elif cmd == 'create':
        create_tables()
    elif cmd == 'seed':
        seed_db()
    elif cmd == 'reset':
        reset()
    else:
        print('Unknown command. Use drop, create, or seed.')
