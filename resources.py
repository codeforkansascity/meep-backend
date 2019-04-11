from models import *
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with

from models import db, Project, ProjectType, Location

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)








# project_fields = {
#     'name': fields.String,
#     'description': fields.String,
#     'photoUrl': fields.String(attribute='photo_url'),
#     'websiteUrl': fields.String(attribute='website_url'),
#     'year': fields.Integer,
#     'ggeReduced': fields.Float(attribute='gge_reduced'),
#     'ghgReduced': fields.Float(attribute='ghg_reduced')
# }

location_fields = {
    'address': fields.String,
    'city': fields.String,
    'state': fields.String,
    'zipCode': fields.Integer(attribute='zip_code'),
    'latitude': fields.Float,
    'longitude': fields.Float
}

# project_list_fields = {'projects': fields.List(fields.Nested(project_fields))}
# location_list_fields = (
#     {'locations': fields.List(fields.Nested(location_fields))}
# )


class BaseAPI(Resource):

    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser()
        for col in self.model.get_columns():
            parser.add_argument(col)
        self.parser = parser

    def get(self, id):
        resource = self.model.query.get(id)
        return marshal(resource.json, self.output_fields), 200

    def put(self, id):
        args = self.parser.parse_args()
        resource = self.model.query.get(id)
        for k, v in args.items():
            if v is not None:
                setattr(resource, k, v)
        db.session.commit()
        return 200

    def delete(self, id):
        resource = self.model.query.get(id)
        db.session.delete(resource)
        db.session.commit()
        return 200


class BaseListAPI(Resource):

    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser()
        for col in self.base.model.get_columns():
            parser.add_argument(col)
        self.parser = parser

    @property
    def output_fields(self):
        output_fields = dict([])
        output_fields[self.base.model.__table__] = (
            fields.List(fields.Nested(self.base.output_fields))
        )
        print(output_fields)
        return output_fields

    def post(self):
        args = self.parser.parse_args()
        attrs = self.base.model.get_columns()
        new_resource = self.base.model(**{attr: args.get(attr) for attr in attrs})
        db.session.add(new_resource)
        db.session.commit()
        return 200

    def get(self):
        resources = self.base.model.query.all()
        json = dict([])
        json[self.base.model.__table__] = (
            [resource.json for resource in resources]
        )
        return marshal(json, self.output_fields), 200



class ProjectAPI(BaseAPI):

    model = Project
    output_fields = {
        'name': fields.String,
        'description': fields.String,
        'photoUrl': fields.String(attribute='photo_url'),
        'websiteUrl': fields.String(attribute='website_url'),
        'year': fields.Integer,
        'ggeReduced': fields.Float(attribute='gge_reduced'),
        'ghgReduced': fields.Float(attribute='ghg_reduced')
    }


class ProjectListAPI(BaseListAPI):

    base = ProjectAPI


# class LocationAPI(Resource):
#
#     @marshal_with(location_fields)
#     def get(self, id):
#         location = Location.query.get(id)
#         return location.json
#
#     def put(self, id):
#         pass
#
#     def delete(self, id):
#         pass
#
#
# class LocationListAPI(Resource):
#
#     def post(self):
#         args = parser.parse_args()
#         attrs = ('address', 'city', 'state', 'zip_code', 'latitude',
#                  'longitude')
#         new_location = Location(**{attr: args.get(attr) for attr in attrs})
#         db.session.add(new_location)
#         db.session.commit()




api.add_resource(ProjectAPI, '/projects/<int:id>', endpoint='project')
api.add_resource(ProjectListAPI, '/projects', endpoint='project_list')
# api.add_resource(LocationAPI, '/locations/<int:id>', endpoint='location')
# api.add_resource(LocationListAPI, '/locations', endpoint='location_list')
