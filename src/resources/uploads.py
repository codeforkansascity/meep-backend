from flask import Blueprint
from flask_restful import Api, Resource, fields, reqparse
from .base import BaseAPI, BaseListAPI
# from models import User, Role
import pandas as pd

from app import db

api_uploads_blueprint = Blueprint('api_uploads', __name__)
api = Api(api_uploads_blueprint)

'''
defining a list api resource entails subclassing BaseListAPI and referring
to the base API resource it is built on
'''

# Uploads api should probably only have put and post requests allowed...

class UploadAPI(Resource):  #
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()  # for input validation
        # for col in self.model.get_columns():
        #     parser.add_argument(col)
        # self.parser = parser

        self.TODOS = {
        'todo1': {'task': 'build an API'},
        'todo2': {'task': '?????'},
        'todo3': {'task': 'profit!'},
        }

    def get(self):

        return self.TODOS

    def post(self):
        self.parser.add_argument('file')
        args = self.parser.parse_args()
        # args['file']
        print(args)

        ######
        df = pd.read_csv(args['file'])

        print(df.head)
        print(df.columns)
        print(df['project'][0])
        #######

        todo_id = int(max(self.TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        # self.TODOS[todo_id] = {'task': args['file']}
        self.TODOS[todo_id] = {'task': df['project'][0]}

        return df['project'][0], 200

    def delete(self, id):
        # # the same ideas from the put method apply here
        # resource = self.model.query.get(id)
        # db.session.delete(resource)
        # db.session.commit()
        return 200


api.add_resource(UploadAPI, '/uploads', endpoint='upload')  #'/uploads/<int:id>'
