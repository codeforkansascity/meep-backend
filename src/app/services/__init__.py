from ..models import db, Location

class Queries:
    '''Store static query strings -- this way we only read from disk once.
    '''
    queries = [
        ('location_marker_query', 'src/app/services/sql/get_location_markers.sql')
    ]

    def __init__(self):
        for prop, location in self.queries:
            setattr(self, prop, open(location, 'r').read())

queries = Queries()