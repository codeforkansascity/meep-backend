from flask import render_template, Blueprint, request, redirect, url_for
from models import db, Project, ProjectType, Location

forms_blueprint = Blueprint('forms', __name__)

@forms_blueprint.route('/forms/project-types', methods=['GET', 'POST'])
def project_types_form():
    if request.method == 'GET':
        project_types = ProjectType.query.all()
        return render_template('project_types.html', project_types=project_types)
    elif request.method == 'POST':
        type_name = request.form.get('project_type')
        project_type = ProjectType(type_name=type_name)
        db.session.add(project_type)
        db.session.commit()
        return redirect(url_for('forms.project_types_form'), code=303)
    else:
        # raise method not found error
        pass

@forms_blueprint.route('/forms/project-types/<int:type_id>', methods=['POST'])
def delete_project_type(type_id):
    project_type = ProjectType.query.get(type_id)
    db.session.delete(project_type)
    db.session.commit()
    return redirect(url_for('forms.project_types_form'), code=303)

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
