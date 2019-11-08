import csv
import io

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, fields, reqparse

from app import db
from .base import BaseAPI, BaseListAPI
from models import Project, ProjectType


api_projects_blueprint = Blueprint("api_projects", __name__)
api = Api(api_projects_blueprint)

"""
defining a list api resource entails subclassing BaseListAPI and referring
to the base API resource it is built on
"""


class ProjectAPI(BaseAPI):
    model = Project
    output_fields = {
        "id": fields.Integer,
        "name": fields.String,
        "description": fields.String,
        "photoUrl": fields.String(attribute="photo_url"),
        "websiteUrl": fields.String(attribute="website_url"),
        "year": fields.Integer,
        "ggeReduced": fields.Float(attribute="gge_reduced"),
        "ghgReduced": fields.Float(attribute="ghg_reduced"),
    }


api.add_resource(ProjectAPI, "/projects/<int:id>", endpoint="project")


class ProjectListAPI(BaseListAPI):
    base = ProjectAPI


api.add_resource(ProjectListAPI, "/projects", endpoint="project_list")


class ProjectTypeAPI(BaseAPI):
    model = ProjectType
    output_fields = {
        "id": fields.Integer,
        "typeName": fields.String(attribute="type_name"),
    }


api.add_resource(
    ProjectTypeAPI, "/project-types/<int:id>", endpoint="project_type"
)


class ProjectTypeListAPI(BaseListAPI):
    base = ProjectTypeAPI


api.add_resource(
    ProjectTypeListAPI, "/project-types", endpoint="project_type_list"
)


class ProjectTypeListProjectsAPI(Resource):
    """Return all projects with a given project type"""

    def get(self, id):
        project_type = ProjectType.query.get(id)
        projects = project_type.projects
        return {"projects": [project.json for project in projects]}


api.add_resource(
    ProjectTypeListProjectsAPI,
    "/project-types/<int:id>/projects",
    endpoint="project_type_project_list",
)


class ProjectLocationsAPI(Resource):
    """Return all locations associated with a given project"""

    def get(self, id):
        project = Project.query.get(id)
        return {"locations": [loc.json for loc in project.locations]}


api.add_resource(
    ProjectLocationsAPI,
    "/projects/<int:id>/locations",
    endpoint="project_locations",
)


class ProjectUploadAPI(Resource):
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()  # for input validation
        self.parser.add_argument("file")  # TODO: where should this add be?

    def post(self):
        """
        Test this endpoint using curl or the requests library
        ex: using curl enter the following in a command prompt:
        curl -X POST -F file=@"local_filepath" http://localhost:8001/uploads

        check that projects were added to the database by going to the /projects endpoint
        """
        # Pull in arguments from the post request
        file = request.files["file"]

        # TODO: add error handling or settings to specify which file extensions are allowed
        # TODO: add error handling, gives error if trying to add the same project with the same name again. Need to handle that error
        # sqlite3.IntegrityError: UNIQUE constraint failed: projects.name

        # convert the incoming file object to a file stream object in the proper mode and encoding setting
        file.stream.seek(0)  # seek to the beginning of the file
        contents = file.stream.read().decode(
            "utf-8"
        )  # write contents to a string
        csvfile = io.StringIO(
            contents
        )  # open the string as a filestream so we can use csv package tools

        # use csv package to import the csv
        # create a Project object for each row and add it to the database
        reader = csv.DictReader(csvfile)
        for row in reader:
            # for each row, we will add it to the database
            project = Project(
                name=row["name"],
                description=row["description"],
                photo_url=row["photo_url"],
                website_url=row["website_url"],
                year=row["year"],
                ghg_reduced=row["ghg_reduced"],
                gge_reduced=row["gge_reduced"],
            )
            db.session.add(project)
        db.session.commit()

        return 200

    # TODO: add delete and pull requests??


api.add_resource(
    ProjectUploadAPI, "/projects/upload/csv", endpoint="project_uploads"
)


class ProjectDetailAPI(Resource):
    def get(self, id):
        project = Project.query.filter_by(id=id).first()
        return jsonify(dict(
            img = project.photo_url,
            project_name = project.name,
            details = project.description,
            project_type = project.type.type_name if project.type else None,
            date = str(project.year),
            emissions_data = {
                'gge_reduced': project.gge_reduced,
                'ghg_reduced': project.ghg_reduced
            }
        ))


api.add_resource(
    ProjectDetailAPI,
    "/projects/<int:id>/detail",
    endpoint="project_detail",
)


class ProjectSummaryAPI(Resource):
    def get(self, id):
        project = Project.query.filter_by(id=id).first()
        return jsonify(dict(
            img = project.photo_url,
            project_name = project.name,
            project_details = project.description,
            date = str(project.year)
        ))

api.add_resource(
    ProjectSummaryAPI,
    "/projects/<int:id>/summary",
    endpoint="project_summary",
)
