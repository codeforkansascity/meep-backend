from app import db
from flask_restful import Resource, reqparse, marshal, fields


class BaseAPI(Resource):

    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser()
        for col in self.model.get_columns():
            parser.add_argument(col)
        self.parser = parser

    def get(self, id):
        resource = self.model.query.get(id)
        return marshal(resource.json, self.output_fields), 200

    def put(self, id):
        args = self.parser.parse_args()
        resource = self.model.query.get(id)
        for k, v in args.items():
            if v is not None:
                setattr(resource, k, v)
        db.session.commit()
        return 200

    def delete(self, id):
        resource = self.model.query.get(id)
        db.session.delete(resource)
        db.session.commit()
        return 200


class BaseListAPI(Resource):

    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser()
        for col in self.base.model.get_columns():
            parser.add_argument(col)
        self.parser = parser

    @property
    def output_fields(self):
        output_fields = dict([])
        output_fields[self.base.model.__tablename__] = (
            fields.List(fields.Nested(self.base.output_fields))
        )
        print(output_fields)
        return output_fields

    def post(self):
        args = self.parser.parse_args()
        attrs = self.base.model.get_columns()
        new_resource = self.base.model(**{attr: args.get(attr) for attr in attrs})
        db.session.add(new_resource)
        db.session.commit()
        return 200

    def get(self):
        # import pdb; pdb.set_trace()
        resources = self.base.model.query.all()
        json = dict([])
        json[self.base.model.__tablename__] = (
            [resource.json for resource in resources]
        )
        return marshal(json, self.output_fields), 200