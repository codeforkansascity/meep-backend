from functools import partial, reduce
from collections import defaultdict, namedtuple

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, fields
from geoalchemy2 import functions
from sqlalchemy import func

from .base import BaseAPI, BaseListAPI
from models import db, Project, ProjectType, Location
from services.location_marker import get_location_markers


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

    def get(self, resource_id):
        location = self.model.query.get(resource_id)
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
    base = LocationAPI()
    model = Location

    def get(self):
        locations = self.model.query.all()
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
    base = LocationAPI()
    model = Location
    """Given a location, return the associated project"""
    def get(self, resource_id):
        location = self.model.query.get(resource_id)
        return location.project.json


api.add_resource(LocationProjectAPI, '/locations/<int:id>/project', endpoint='location_project')


class LocationMarkerAPI(BaseListAPI):
    base = LocationAPI()

    def get(self):
        return jsonify({
            'locationMarkers': get_location_markers()
        })


api.add_resource(LocationMarkerAPI, '/location-markers', '/location-markers/')
