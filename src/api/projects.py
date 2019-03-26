from flask import Blueprint
from ..app import db
from ..models import Project
from . import api


@api.route('/projects/')
def get_projects():
    pass


@api.route('/project/<int:id>')
def get_project(id):
    pass


@api.route('/projects/', methods=['POST'])
def new_project():
    pass


@api.route('/projects/<int:id>', methods=['PUT'])
def edit_project(id):
    pass
