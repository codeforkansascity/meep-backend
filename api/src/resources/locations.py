from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, fields
from geoalchemy2 import functions

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


class LocationMapComponent(BaseListAPI):
    base = LocationAPI

    def get(self):
        locations = Location.query.all()
        data = []
        for location in locations:
            # Get lat long info for the location
            coords = location.coords
            # This to be populated later for polygons and other shapes
            LatLongArray = []
            LatLongCenter = {'lat': coords.get('latitude'), 'long': coords.get('longitude')}

            # Do a query to get more info about the project using the project id
            thisProject = Project.query.filter_by(id = location.project_id).first()

            # find the project type:
            thisProjectType = ProjectType.query.filter_by(id = thisProject.project_type_id).first()

            # Compile the information into format needed
            data.append({
                'points': LatLongArray,
                'project_name': thisProject.name,
                'center': LatLongCenter,
                'project_id': location.project_id,
                'project_type': thisProjectType.type_name 
            })
        return jsonify(data)

api.add_resource(LocationMapComponent, '/locationMap', '/locationMap/')
