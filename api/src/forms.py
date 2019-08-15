from flask import render_template, Blueprint, request, redirect, url_for
from sqlalchemy import func
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
        project_name = request.args.get('projectName')
        project_types = ProjectType.query.all()

        query = Project.query
        if project_name:
            query = query.filter(func.lower(Project.name).startswith(project_name.lower()))
        projects = query.all()
        return render_template('projects.html', project_types=project_types, projects=projects)
    elif request.method == 'POST':
        form = request.form
        new_project = Project(
            name=form.get('project_name'),
            description=form.get('project_description'),
            photo_url=form.get('project_photo_url'),
            website_url=form.get('project_website_url'),
            year=form.get('project_year'),
            gge_reduced=form.get('project_gge_reduced'),
            ghg_reduced=form.get('project_ghg_reduced'),
        )
        project_type_name = form.get('project_type_name')
        if project_type_name:
            project_type = ProjectType.query.filter_by(type_name=project_type_name).first()
            new_project.type = project_type
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('forms.projects_form'), code=303)
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
