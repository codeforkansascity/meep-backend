from models import *
from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from sqlalchemy import and_

from models import db, Project, ProjectType, Location

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


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
        output_fields[self.base.model.__tablename__] = (
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
        # import pdb; pdb.set_trace()
        resources = self.base.model.query.all()
        json = dict([])
        json[self.base.model.__tablename__] = (
            [resource.json for resource in resources]
        )
        return marshal(json, self.output_fields), 200


class ProjectAPI(BaseAPI):
    model = Project
    output_fields = {
        'id': fields.Integer,
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


class LocationProjectAPI(Resource):

    def get(self, id):
        location = Location.query.get(id)
        return location.project.json


class ProjectTypeAPI(BaseAPI):
    model = ProjectType
    output_fields = {
        'id': fields.Integer,
        'typeName': fields.String(attribute='type_name')
    }


class ProjectTypeListAPI(BaseListAPI):
    base = ProjectTypeAPI


class ProjectTypeListProjectsAPI(Resource):
    def get(self, id):
        project_type = ProjectType.query.get(id)
        projects = project_type.projects
        return {'projects': [project.json for project in projects]}


class ProjectLocationsAPI(Resource):
    def get(self, id):
        project = Project.query.get(id)
        return {'locations': [loc.json for loc in project.locations]}


class UserAPI(BaseAPI):
    model = User
    output_fields = {
        'id': fields.Integer,
        'email': fields.String
    }


class UserListAPI(BaseListAPI):
    base = UserAPI


class RoleAPI(BaseAPI):
    model = Role
    output_fields = {
        'id': fields.Integer,
        'role': fields.String(attribute='role_name')
    }

class RoleListAPI(BaseListAPI):
    base = RoleAPI


api.add_resource(ProjectAPI, '/projects/<int:id>', endpoint='project')
api.add_resource(ProjectListAPI, '/projects', endpoint='project_list')
api.add_resource(LocationAPI, '/locations/<int:id>', endpoint='location')
api.add_resource(LocationListAPI, '/locations', '/locations/')
api.add_resource(UserAPI, '/users/<int:id>', endpoint='user')
api.add_resource(UserListAPI, '/users', endpoint='user_list')
api.add_resource(RoleAPI, '/roles/<int:id>', endpoint='role')
api.add_resource(RoleListAPI, '/roles', endpoint='role_list')
api.add_resource(ProjectTypeAPI, '/project-types/<int:id>', endpoint='project_type')
api.add_resource(ProjectTypeListAPI, '/project-types', endpoint='project_type_list')

api.add_resource(LocationProjectAPI, '/locations/<int:id>/project', endpoint='location_project')
api.add_resource(ProjectTypeListProjectsAPI, '/project-types/<int:id>/projects', endpoint='project_type_project_list')
api.add_resource(ProjectLocationsAPI, '/projects/<int:id>/locations', endpoint='project_locations')
