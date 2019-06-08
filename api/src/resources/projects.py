from flask import Blueprint
from flask_restful import Api, Resource, fields
from .base import BaseAPI, BaseListAPI
from models import Project, ProjectType

api_projects_blueprint = Blueprint('api_projects', __name__)
api = Api(api_projects_blueprint)

'''
defining a list api resource entails subclassing BaseListAPI and referring
to the base API resource it is built on
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


api.add_resource(ProjectAPI, '/projects/<int:id>', endpoint='project')


class ProjectListAPI(BaseListAPI):
    base = ProjectAPI


api.add_resource(ProjectListAPI, '/projects', endpoint='project_list')


class ProjectTypeAPI(BaseAPI):
    model = ProjectType
    output_fields = {
        'id': fields.Integer,
        'typeName': fields.String(attribute='type_name')
    }


api.add_resource(ProjectTypeAPI, '/project-types/<int:id>', endpoint='project_type')


class ProjectTypeListAPI(BaseListAPI):
    base = ProjectTypeAPI


api.add_resource(ProjectTypeListAPI, '/project-types', endpoint='project_type_list')


class ProjectTypeListProjectsAPI(Resource):
    """Return all projects with a given project type"""
    def get(self, id):
        project_type = ProjectType.query.get(id)
        projects = project_type.projects
        return {'projects': [project.json for project in projects]}


api.add_resource(ProjectTypeListProjectsAPI, '/project-types/<int:id>/projects', endpoint='project_type_project_list')


class ProjectLocationsAPI(Resource):
    """Return all locations associated with a given project"""
    def get(self, id):
        project = Project.query.get(id)
        return {'locations': [loc.json for loc in project.locations]}


api.add_resource(ProjectLocationsAPI, '/projects/<int:id>/locations', endpoint='project_locations')
