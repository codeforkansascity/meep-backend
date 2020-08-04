from dataclasses import dataclass, field
from ..models import db, Project, ProjectType, Location

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
            'center': LatLng(*self.center).json,
            'project_ids': self.project_ids,
            'project_types': self.project_types,
            'gge_reduced': self.gge_reduced,
            'ghg_reduced': self.ghg_reduced
        }

def get_location_markers():
    with db.engine.connect() as con:
        result = con.execute('''
            with projects_and_types as (
                select 	projects.id, 
                    name, 
                    gge_reduced, 
                    ghg_reduced, 
                    type_name as project_type 
                from 
                projects
                join
                project_types
                on projects.project_type_id = project_types.id
            ), proj_locs as (
                select 	name, 
                    sum(gge_reduced) as gge_reduced, 
                    sum(ghg_reduced) as ghg_reduced, 
                    array_agg(project_type) as project_types, 
                    array_agg(projects_and_types.id) as project_ids, 
                    ST_Collect(location) as points 
                from 
                projects_and_types 
                join 
                locations
                on projects_and_types.id = locations.id
                group by name
            )
            select  ST_AsGeoJSON(points)::json -> 'coordinates' as points,
                    name as project_name, 
                    ST_AsGeoJSON(ST_Centroid(points))::json -> 'coordinates' as center,
                    project_ids, 
                    project_types, 
                    ghg_reduced, 
                    gge_reduced
            from proj_locs;
            ''')
        
        return [LocationMarker(*row).json for row in result.fetchall()]