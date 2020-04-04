from functools import partial, reduce
from collections import defaultdict, namedtuple

from geoalchemy2 import functions
from sqlalchemy import func

from models import db, Project, ProjectType, Location

LocationMarkerNT = namedtuple(
    'LocationMarkerNT',
    [
        'points',
        'project_name',
        'center',
        'project_ids',
        'project_types',
        'ghg_reduced',
        'gge_reduced'
    ]
)


class LocationMarker(LocationMarkerNT):
    @property
    def json(self):
        return {
            'points': [p.json for p in self.points],
            'project_name': self.project_name,
            'center': self.center.json if self.center is not None else None,
            'project_ids': self.project_ids,
            'project_types': self.project_types,
            'gge_reduced': self.gge_reduced,
            'ghg_reduced': self.ghg_reduced
        }


LatLngNT = namedtuple(
    'LatLngNT',
    [
        'lat',
        'lng'
    ]
)


class LatLng(LatLngNT):
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


def get_location_markers():
    projects = Project.query.all()
    projects_by_name = group_projects_by_name(projects)
    projects_agg = [aggregate_project_group(name, group)
                    for (name, group) in projects_by_name.items()]
    return [lm.json for lm in projects_agg]


def group_projects_by_name(projects):
    grouped = defaultdict(list)
    for project in projects:
        grouped[project.name].append(project)
    return grouped


def aggregate_project_group(name, group):
    agg_project = reduce(
        lambda agg, next_resource: {
            'gge_reduced': agg['gge_reduced'] + next_resource.gge_reduced,
            'ghg_reduced': agg['ghg_reduced'] + next_resource.ghg_reduced,
            'project_types': set(agg['project_types'] | {next_resource.type.type_name}) if next_resource.type else agg[
                'project_types'],
            'project_ids': set(agg['project_ids'] | {next_resource.id}) if next_resource.id else agg['project_ids'],
            'points': agg['points'] | {
                LatLng(
                    lat=loc.coords['latitude'],
                    lng=loc.coords['longitude']
                ) for loc in next_resource.locations if loc.location is not None}
        },
        group,
        {
            'gge_reduced': 0,
            'ghg_reduced': 0,
            'project_types': set([]),
            'project_ids': set([]),
            'points': set([])
        }
    )
    agg_project['project_types'] = list(agg_project['project_types'])
    agg_project['project_ids'] = list(agg_project['project_ids'])
    agg_project['points'] = list(agg_project['points'])
    agg_project['project_name'] = name

    agg_project['center'] = compute_centroid(agg_project['points'])
    return LocationMarker(**agg_project)


def compute_centroid(points):
    points = list(points)
    if len(points) == 0:
        return None
    try:
        lat = sum(p.lat for p in points)
        lat /= len([p for p in points])
        lng = sum(p.lng for p in points)
        lng /= len([p for p in points])
        return LatLng(lat=lat, lng=lng)
    except ZeroDivisionError as e:
        return None
