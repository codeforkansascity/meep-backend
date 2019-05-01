from models import *
from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse, fields, marshal, marshal_with
from sqlalchemy import and_

from models import db, Project, ProjectType, Location

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

'''
There are two base classes for resources. The first is BaseAPI, and has GET,
PUT, AND DELETE HTTP methods attached to it. The second is BaseListAPI, which
has a GET method for lists of records, and a POST method for a single record.
The reason the methods were organized into resources in this manner is that
all of the methods attached to the BaseAPI object take an id parameter, while
the methods registered with the BaseListAPI object take no url parameters.
'''

class BaseAPI(Resource):
    '''
    Base resource class. Treat this as an abstract base class and do not
    instantiate it. If the methods provided do not suit your purposes for a
    given resource, such as if you need to add a query string, you can override
    them. By defining a function with the same name in a subclass.

    Attributes:

        parser :

        model : A sqlalchemy model used to reference data fields and
        issue queries. This must be specified in the base class.

        output_fields : a dictionary specifying the shape of the data returned
        by the method. Must be defined in a subclass. See the flask-restful
        documentation for details on how these work.

    '''
    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser() # for input validation
        for col in self.model.get_columns():
            parser.add_argument(col)
        self.parser = parser

    def get(self, id):
        # get an instance of a SQLAlchemy model for the json attribute
        resource = self.model.query.get(id)
        # marshal ensures that the json provided as the first argument takes
        # the format defined in output_fields
        return marshal(resource.json, self.output_fields), 200

    def put(self, id):
        args = self.parser.parse_args()
        resource = self.model.query.get(id) # get instance of model
        for k, v in args.items():
            if v is not None:
                setattr(resource, k, v) # since we don't know the class we
                # are working with, use setattr
        db.session.commit() # db is the sqlalchemy instance
        return 200

    def delete(self, id):
        # the same ideas from the put method apply here
        resource = self.model.query.get(id)
        db.session.delete(resource)
        db.session.commit()
        return 200


class BaseListAPI(Resource):
    '''
    Base class for lists of resources.  As with BaseAPI, treat this as an
    abstract base class and do not directly instantiate it.

    attributes:

        base: A subclass of BaseAPI. This essentially tells the get method
        the class of objects to populate a list with. This must be specified
        when defining a subclass.

        parser: RequestParser object for input validation.
        Is automatically created on instantiation.

    '''
    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser()
        for col in self.base.model.get_columns():
            parser.add_argument(col)
        self.parser = parser

    @property
    def output_fields(self):
        '''
        builds the template for output data automatically from output_fields
        of the output_fields attribute of base
        '''
        output_fields = dict([])
        output_fields[self.base.model.__tablename__] = (
            fields.List(fields.Nested(self.base.output_fields))
        )
        return output_fields

    def post(self):
        '''
        body of the post request is an object whose attribute names
        mirror the column names of the underlying model
        '''
        args = self.parser.parse_args()
        attrs = self.base.model.get_columns()
        new_resource = self.base.model(**{attr: args.get(attr) for attr in attrs})
        db.session.add(new_resource)
        db.session.commit()
        return 200

    def get(self):
        '''
        return a list of the given resource.
        '''
        resources = self.base.model.query.all()
        json = dict([])
        json[self.base.model.__tablename__] = (
            [resource.json for resource in resources]
        )
        return marshal(json, self.output_fields), 200


'''
To define an api class, just subclass BaseAPI and provide model and output_fields
as class attributes
'''
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


'''
defining a list api resource entails subclassing BaseListAPI and refering
to the base API resource it is built on
'''
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
    '''
    overrides inherited get method from BaseListAPI in order to implement
    query string parameters
    '''
        #query string parameters
        min_year = request.args.get('min-year')
        max_year = request.args.get('max-year')
        project_types = request.args.getlist('project-type')

        if not request.args: # if no query string parameters provided
            # return all locations
            locs = [loc.json for loc in Project.query.all()]
            return {'locations': locs}

        # some query parameter was passed, so join project type, project, and
        # location tables, and filter based on non null queries
        q = db.session.query(ProjectType, Project, Location)\
            .filter(ProjectType.id == Project.project_type_id)\
            .filter(Project.id == Location.project_id)

        if min_year is not None:
            q = q.filter(Project.year >= min_year)

        if max_year is not None:
            q = q.filter(Project.year <= max_year)

        if project_types:
            q = q.filter(ProjectType.type_name.in_(project_types))

        # only return location data, even though projects and project types
        # were used in the query
        locs = [loc.json for (type, proj, loc) in q]
        return {'locations': locs}


class LocationProjectAPI(Resource):
    '''
    given a location, return the associated project
    '''
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
    '''
    return all projects with a given project type
    '''
    def get(self, id):
        project_type = ProjectType.query.get(id)
        projects = project_type.projects
        return {'projects': [project.json for project in projects]}


class ProjectLocationsAPI(Resource):
    '''
    return all locations associated with a given project
    '''
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


# define routes and endpoints for the resources
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
