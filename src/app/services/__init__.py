from ..models import db, Location
from pathlib import Path

class Queries:
    '''Store static query strings -- this way we only read from disk once.
    '''
    queries = [
        ('location_marker_query', '../sql/get_location_markers.sql')
    ]

    def __init__(self):
        for prop, location in self.queries:
            file = Path(__file__, location).resolve()
            setattr(self, prop, open(file, 'r').read())


queries = Queries()