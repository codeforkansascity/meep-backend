from flask import render_template, Blueprint, request
from models import db, Project, ProjectType, Location

forms_blueprint = Blueprint('forms', __name__)

@forms_blueprint.route('/forms/project-types', methods=['GET', 'POST'])
def project_types_form():
    if request.method == 'GET':
        project_types = ProjectType.query.all()
        return render_template('project_types.html', project_types=project_types)
    elif request.method == 'POST':
        pass
    else:
        # raise method not found error
        pass


@forms_blueprint.route('/forms/projects', methods=['GET', 'POST'])
def projects_form():
    if request.method == 'GET':
        project_types = ProjectType.query.all()
        projects = Project.query.all()
        return render_template('projects.html', project_types=project_types, projects=projects)
    elif request.method == 'POST':
        pass
    else:
        # raise method not found error
        pass


@forms_blueprint.route('/forms/projects/<int:project_id>', methods=['GET', 'PUT'])
def locations_form(project_id):
    if request.method == 'GET':
        project_types = ProjectType.query.all()
        project = Project.query.get(project_id)
        return render_template('project_detail.html', project=project, project_types=project_types)
    elif request.method == 'PUT':
        pass
    else:
        # raise method not found error
        pass


@forms_blueprint.route('/forms/roles', methods=['GET', 'POST'])
def roles_form():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    else:
        # raise method not found error
        pass


@forms_blueprint.route('/forms/users', methods=['GET', 'POST'])
def users_form():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    else:
        # raise method not found error
        pass
