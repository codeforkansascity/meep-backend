from dataclasses import dataclass, field
from ..models import db, Project, ProjectType, Location
from ..services import queries

@dataclass
class LatLng:
    lat: float = field()
    lng: float = field()

    def __eq__(self, o):
        return self.lat == o.lat and self.lng == o.lng

    def __hash__(self):
        return hash((self.lat, self.lng))

    @property
    def json(self):
        return {
            'lat': self.lat,
            'lng': self.lng
        }

@dataclass
class LocationMarker:
    points: list = field()
    project_name: str = field()
    year: int = field()
    center: list = field()
    project_ids: list = field()
    project_types: list = field()
    ghg_reduced: float = field()
    gge_reduced: float = field()
    
    @property
    def json(self):
        return {
            'points': [LatLng(*pt).json for pt in self.points],
            'project_name': self.project_name,
            'year': self.year,
            'center': LatLng(*self.center).json,
            'project_ids': self.project_ids,
            'project_types': self.project_types,
            'gge_reduced': self.gge_reduced,
            'ghg_reduced': self.ghg_reduced
        }


def get_location_markers():
    with db.engine.connect() as con:
        result = con.execute(queries.location_marker_query)
        return [LocationMarker(*row).json for row in result.fetchall()]