from flask import Blueprint, request
from flask_restful import Api, Resource, fields
from resources.base import BaseAPI, BaseListAPI
from models import db, Project, ProjectType, Location


api_locations_blueprint = Blueprint('api_locations', __name__)
api = Api(api_locations_blueprint)


class LocationAPI(BaseAPI):
    model = Location
    output_fields = {
        'id': fields.String(),
        'address': fields.String,
        'city': fields.String,
        'state': fields.String,
        'zipCode': fields.Integer(attribute='zip_code'),
        'latitude': fields.Float,
        'longitude': fields.Float
    }


api.add_resource(LocationAPI, '/locations/<int:id>', endpoint='location')


class LocationListAPI(BaseListAPI):
    base = LocationAPI

    def get(self):
        min_year = request.args.get('min-year')
        max_year = request.args.get('max-year')
        project_types = request.args.getlist('project-type')

        if not request.args:
            locs = [loc.json for loc in Project.query.all()]
            return {'locations': locs}

        q = db.session.query(ProjectType, Project, Location)\
            .filter(ProjectType.id == Project.project_type_id)\
            .filter(Project.id == Location.project_id)

        if min_year is not None:
            q = q.filter(Project.year >= min_year)

        if max_year is not None:
            q = q.filter(Project.year <= max_year)

        if project_types:
            q = q.filter(ProjectType.type_name.in_(project_types))

        locs = [loc.json for (type, proj, loc) in q]
        return {'locations': locs}


api.add_resource(LocationListAPI, '/locations', '/locations/')


class LocationProjectAPI(Resource):

    def get(self, id):
        location = Location.query.get(id)
        return location.project.json


api.add_resource(LocationProjectAPI, '/locations/<int:id>/project', endpoint='location_project')