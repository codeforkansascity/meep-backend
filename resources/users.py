from flask import Blueprint
from flask_restful import Api, fields
from resources.base import BaseAPI, BaseListAPI
from models import User, Role

api_users_blueprint = Blueprint('api_users', __name__)
api = Api(api_users_blueprint)

'''
defining a list api resource entails subclassing BaseListAPI and referring
to the base API resource it is built on
'''


class UserAPI(BaseAPI):
    model = User
    output_fields = {
        'id': fields.Integer,
        'email': fields.String
    }


api.add_resource(UserAPI, '/users/<int:id>', endpoint='user')


class UserListAPI(BaseListAPI):
    base = UserAPI


api.add_resource(UserListAPI, '/users', endpoint='user_list')


class RoleAPI(BaseAPI):
    model = Role
    output_fields = {
        'id': fields.Integer,
        'role': fields.String(attribute='role_name')
    }


api.add_resource(RoleAPI, '/roles/<int:id>', endpoint='role')


class RoleListAPI(BaseListAPI):
    base = RoleAPI


api.add_resource(RoleListAPI, '/roles', endpoint='role_list')