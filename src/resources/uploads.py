from flask import Blueprint
from flask_restful import Api, fields
from .base import BaseAPI, BaseListAPI
from models import User, Role

api_uploads_blueprint = Blueprint('api_uploads', __name__)
api = Api(api_uploads_blueprint)

'''
defining a list api resource entails subclassing BaseListAPI and referring
to the base API resource it is built on
'''


class UploadAPI(BaseAPI):
    # model = User
    model = BaseModel
    output_fields = {
        'id': 'upload test'
    }
    print('made it to uploads api')


api.add_resource(UploadAPI, '/uploads', endpoint='upload')  #'/uploads/<int:id>'


class UserListAPI(BaseListAPI):
    base = UploadAPI

