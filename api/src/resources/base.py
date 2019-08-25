from app import db
from flask_restful import Resource, reqparse, marshal, fields

'''There are two base classes for resources. The first is BaseAPI, and has GET,
PUT, AND DELETE HTTP methods attached to it. The second is BaseListAPI, which
has a GET method for lists of records, and a POST method for a single record.
The reason the methods were organized into resources in this manner is that
all of the methods attached to the BaseAPI object take an id parameter, while
the methods registered with the BaseListAPI object take no url parameters.

To define an api class, just subclass BaseAPI and provide model and output_fields
as class attributes
'''


class BaseAPI(Resource):
    """Base resource class. Treat this as an abstract base class and do not
    instantiate it. If the methods provided do not suit your purposes for a
    given resource, such as if you need to add a query string, you can override
    them by defining a function with the same name in a subclass.

    Attributes:

        parser :

        model : A sqlalchemy model used to reference data fields and
        issue queries. This must be specified in the base class.

        output_fields : a dictionary specifying the shape of the data returned
        by the method. Must be defined in a subclass. See the flask-restful
        documentation for details on how these work.
    """
    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser()  # for input validation
        for col in self.model.get_columns():
            parser.add_argument(col)
        self.parser = parser

    def get(self, id):
        # get an instance of a SQLAlchemy model for the json attribute
        resource = self.model.query.get(id)
        # marshal ensures that the json provided as the first argument takes
        # the format defined in output_fields
        return marshal(resource.json, self.output_fields), 200

    def put(self, id):
        args = self.parser.parse_args()
        resource = self.model.query.get(id) # get instance of model
        for k, v in args.items():
            if v is not None:
                setattr(resource, k, v)  # since we don't know the class we
                # are working with, use setattr
        db.session.commit()  # db is the sqlalchemy instance
        return 200

    def delete(self, id):
        # the same ideas from the put method apply here
        resource = self.model.query.get(id)
        db.session.delete(resource)
        db.session.commit()
        return 200


class BaseListAPI(Resource):
    """Base class for lists of resources.  As with BaseAPI, treat this as an
    abstract base class and do not directly instantiate it.

    attributes:

        base: A subclass of BaseAPI. This essentially tells the get method
        the class of objects to populate a list with. This must be specified
        when defining a subclass.

        parser: RequestParser object for input validation.
        Is automatically created on instantiation.
    """
    def __init__(self):
        super().__init__()
        parser = reqparse.RequestParser()
        for col in self.base.model.get_columns():
            parser.add_argument(col)
        self.parser = parser

    @property
    def output_fields(self):
        """builds the template for output data automatically from output_fields
        of the output_fields attribute of base
        """
        output_fields = dict([])
        output_fields[self.base.model.__tablename__] = (
            fields.List(fields.Nested(self.base.output_fields))
        )
        return output_fields

    def post(self):
        """body of the post request is an object whose attribute names
        mirror the column names of the underlying model
        """
        args = self.parser.parse_args()
        attrs = self.base.model.get_columns()
        new_resource = self.base.model(**{attr: args.get(attr) for attr in attrs})
        db.session.add(new_resource)
        db.session.commit()
        return 200

    def get(self):
        """return a list of the given resource."""
        resources = self.base.model.query.all()
        json = dict([])
        json[self.base.model.__tablename__] = (
            [resource.json for resource in resources]
        )
        return marshal(json, self.output_fields), 200
