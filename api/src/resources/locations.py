from functools import partial, reduce
from collections import defaultdict, namedtuple

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, fields
from geoalchemy2 import functions
from sqlalchemy import func

from .base import BaseAPI, BaseListAPI
from models import db, Project, ProjectType, Location


api_locations_blueprint = Blueprint('api_locations', __name__)
api = Api(api_locations_blueprint)

'''
defining a list api resource entails subclassing BaseListAPI and referring
to the base API resource it is built on
'''


class LocationAPI(BaseAPI):
    model = Location
    output_fields = {
        'id': fields.String(),
        'address': fields.String,
        'city': fields.String,
        'state': fields.String,
        'zipCode': fields.Integer(attribute='zip_code'),
        'location': fields.String
    }

    def get(self, id):
        location = self.model.query.get(id)
        coords = location.coords
        return jsonify({
            'address': location.address,
            'city': location.city,
            'state': location.state,
            'zipCode': location.zip_code,
            'latitude': coords.get('latitude'),
            'longitude': coords.get('longitude')
        })




api.add_resource(LocationAPI, '/locations/<int:id>', endpoint='location')


class LocationListAPI(BaseListAPI):
    base = LocationAPI

    def get(self):
        locations = Location.query.all()
        data = []
        for location in locations:
            coords = location.coords
            data.append({
                'id': location.id,
                'address': location.address,
                'city': location.city,
                'state': location.state,
                'zipCode': location.zip_code,
                'latitude': coords.get('latitude'),
                'longitude': coords.get('longitude')
            })
        return jsonify({'locations': data})



api.add_resource(LocationListAPI, '/locations', '/locations/')


class LocationProjectAPI(Resource):
    """Given a location, return the associated project"""
    def get(self, id):
        location = Location.query.get(id)
        return location.project.json


api.add_resource(LocationProjectAPI, '/locations/<int:id>/project', endpoint='location_project')


def build_project_year_query(min_year, max_year):
    min_year_query = (Project.year >= min_year) if min_year else None
    max_year_query = (Project.year <= max_year) if max_year else None

    if min_year is not None and max_year is not None:
        year_query = min_year_query & max_year_query
    elif max_year is not None:
        year_query = max_year_query
    elif min_year is not None:
        year_query = min_year_query
    else:
        year_query = None

    return year_query


def query_projects(min_year, max_year, project_types):
    if project_types is None:
        project_types = []
    project_types = list(map(lambda type: type.lower(), project_types))
    project_types = ProjectType.query.filter(
        func.lower(ProjectType.type_name).in_(project_types)).all()
    project_type_ids = [type.id for type in project_types]

    year_query = build_project_year_query(min_year, max_year)

    project_type_query = (Project.project_type_id.in_(project_type_ids))

    projects = Project.query
    if year_query is not None:
        projects = projects.filter(year_query)

    projects = projects.filter(project_type_query)

    projects = projects.all()

    return projects


def compute_centroid(points):
    points = list(points)
    if len(points) == 0:
        return points
    try:
        lat = sum(p.get('lat') for p in points if p.get('lat') is not None)
        lat /= len([p for p in points if p.get('lat') is not None])
        lng = sum(p.get('lng') for p in points if p.get('lng') is not None)
        lng /= len([p for p in points if p.get('lng') is not None])
        return {'lat': lat, 'lng': lng}
    except ZeroDivisionError as e:
        return points[0]

Coord = namedtuple('Coord', ['lat', 'lng'])

def aggregate_projects(projects):
    grouped_by_name = defaultdict(list)
    for project in projects:
        grouped_by_name[project.name.lower()].append(project)
    aggregates = []
    for project_name, group in grouped_by_name.items():
        locations = [project.locations for project in group]
        coords = [[loc.coords for loc in loc_group] for loc_group in locations]
        coords_nt = [list(map(lambda c: Coord(c.get('latitude'), c.get('longitude')), coord_group)) for coord_group in coords]
        points_nt = reduce(
            lambda agg, next: agg | set(next),
            coords_nt,
            set([])
        )
        points = [p._asdict() for p in points_nt]
        center = compute_centroid(points)
        project_ids = [project.id for project in group]
        project_types = list(set(project.type.type_name.lower() for project in group))
        gge_reduced = sum(proj.gge_reduced for proj in group if proj.gge_reduced is not None)
        ghg_reduced = sum(proj.ghg_reduced for proj in group if proj.ghg_reduced is not None)
        aggregates.append({
            'points': points,
            'project_name': project_name,
            'center': center,
            'project_ids': project_ids,
            'project_types': project_types,
            'ghg_reduced': ghg_reduced,
            'gge_reduced': gge_reduced
        })
    return aggregates


class LocationMapComponent(BaseListAPI):
    base = LocationAPI()

    def get(self):
        min_year = request.args.get('minYear')
        if min_year is not None:
            min_year = int(min_year)
        max_year = request.args.get('maxYear')
        if max_year is not None:
            max_year = int(max_year)
        project_types = request.args.getlist('projectType')
        # format project types
        projects = query_projects(min_year, max_year, project_types)
        projects_agg = aggregate_projects(projects)
        return jsonify(projects_agg)


api.add_resource(LocationMapComponent, '/locationMap', '/locationMap/')
