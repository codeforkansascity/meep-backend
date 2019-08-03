from flask import Blueprint, request
from flask_restful import Api, Resource, fields, reqparse
from models import db, Project
import csv
import io
from app import db

api_uploads_blueprint = Blueprint('api_uploads', __name__)
api = Api(api_uploads_blueprint)


# TODO: Uploads api should probably only have put and post requests allowed...

class UploadAPI(Resource):  
    def __init__(self):
        super().__init__()
        self.parser = reqparse.RequestParser()  # for input validation
        self.parser.add_argument('file')   # TODO: where should this add be?
    
    def post(self):
        """
        Test this endpoint using curl or the requests library
        ex: using curl enter the following in a command prompt:
        curl -X POST -F file=@"local_filepath" http://localhost:8001/uploads

        check that projects were added to the database by going to the /projects endpoint
        """
        # Pull in arguments from the post request
        file = request.files['file']

        # TODO: add error handling or settings to specify which file extensions are allowed
        # TODO: add error handling, gives error if trying to add the same project with the same name again. Need to handle that error
            #sqlite3.IntegrityError: UNIQUE constraint failed: projects.name

        # convert the incoming file object to a file stream object in the proper mode and encoding setting
        file.stream.seek(0) # seek to the beginning of the file
        contents = file.stream.read().decode('utf-8')   # write contents to a string
        csvfile = io.StringIO(contents)  # open the string as a filestream so we can use csv package tools
       
        # use csv package to import the csv
        # create a Project object for each row and add it to the database
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            print(row['name'])
            #for each row, we will add it to the database
            project = Project(name=row['name'], 
                description=row['description'], 
                photo_url=row['photo_url'], 
                website_url=row['website_url'], 
                year=row['year'], 
                ghg_reduced=row['ghg_reduced'], 
                gge_reduced=row['gge_reduced'])
            db.session.add(project)
        db.session.commit()

        return 200

    # TODO: add delete and pull requests??

api.add_resource(UploadAPI, '/projects/upload/csv', endpoint='upload')
