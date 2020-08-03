from psycopg2 import connect

from model import Location


class DatabaseManager:
    def __init__(self, host, user, pwd, db, locations_table, port=5432):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.locations_table = locations_table
        self.connect()

    def connect(self, db=None):
        if db is None:
            db = self.db

        try:
            self.connection = connect(dbname=db, user=self.user,
                password=self.pwd, host=self.host, port=self.port)
        except Exception as e:
            raise e

    def select_location_columns(self):
        sql = '''
            SELECT *
            FROM {}
            LIMIT 0
        '''.format(self.locations_table)
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                column_names = {desc[0] for desc in cursor.description}
            except Exception as e:
                self.connection.close()
                raise e

    def validate_columns(self, *expected_columns):
        expected_columns = list(expected_columns)
        actual_columns = self.select_location_columns()
        invalid_columns = [c for c in expected_columns if c not in actual_columns]
        if invalid_columns:
            msg = 'Unexpected column names: {}.'.format(', '.join(invalid_columns))
            raise Exception(msg)

    def select_all_locations(self):
        expected_columns = ['id', 'address', 'city', 'state', 'zip_code', 'location']
        # self.validate_columns(*expected_columns)

        sql = '''
            SELECT id, address, city, state
            FROM {}
            WHERE address IS NOT NULL
            AND city IS NOT NULL
            AND state IS NOT NULL
            AND (
                location IS NULL
                OR zip_code IS NULL
            )
        '''.format(self.locations_table)

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                return [Location(*(*row, None, None, None)) for row in cursor]
            except Exception as e:
                self.connection.close()
                raise e

    def update_location(self, location):
        self.bulk_update_locations([location])

    def bulk_update_locations(self, locations):
        expected_columns = ['id', 'address', 'city', 'state', 'zip_code', 'location']
        # self.validate_columns(expected_columns)

        sql = '''
            UPDATE {}
            SET address = %s,
            city = %s,
            state = %s,
            zip_code = %s,
            location = ST_POINT(%s, %s)
            WHERE id = %s
        '''.format(self.locations_table)

        with self.connection.cursor() as cursor:
            for location in locations:
                try:
                    cursor.execute(sql, [location.address, location.city, location.state,
                        location.zip_code, location.longitude, location.latitude, location.id])
                except Exception as e:
                    self.connection.close()
                    raise e
            self.connection.commit()
        return 1
