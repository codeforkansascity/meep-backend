from models import *
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with

from models import db, Project, ProjectType, Location

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

parser = reqparse.RequestParser()

parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('photo_url')
parser.add_argument('website_url')
parser.add_argument('year')
parser.add_argument('gge_reduced')
parser.add_argument('ghg_reduced')

parser.add_argument('project_type')

project_fields = {
    'name': fields.String,
    'description': fields.String,
    'photoUrl': fields.String(attribute='photo_url'),
    'websiteUrl': fields.String(attribute='website_url'),
    'year': fields.Integer,
    'ggeReduced': fields.Float(attribute='gge_reduced'),
    'ghgReduced': fields.Float(attribute='ghg_reduced')
}

project_list_fields = {'projects': fields.List(fields.Nested(project_fields))}

class ProjectAPI(Resource):

    @marshal_with(project_fields)
    def get(self, id):
        project = Project.query.get(id)
        return project.json

    def put(self, id):
        args = parser.parse_args()
        project = Project.query.get(id)
        for k, v in args.items():
            if v is not None or "null":
                setattr(project, k, v)
        db.session.add(project)
        db.session.commit()

    def delete(self, id):
        pass

class ProjectListAPI(Resource):
    def post(self):
        args = parser.parse_args()

        new_project = Project(
            name=args['name'], description=args['description'],
            photo_url=args['photo_url'], website_url=args['website_url'],
            year=args['year'], gge_reduced=args['gge_reduced'],
            ghg_reduced=args['ghg_reduced']
        )

        new_project.type = ProjectType(type_name=args['project_type'])
        db.session.add(new_project)
        db.session.commit()

    @marshal_with(project_list_fields)
    def get(self):
        projects = Project.query.all()
        return {'projects': [project.json for project in projects]}



api.add_resource(ProjectAPI, '/projects/<int:id>', endpoint='project')
api.add_resource(ProjectListAPI, '/projects', endpoint='project_list')
