from pathlib import Path
import csv
from collections import namedtuple
from ..models import Location, Project, ProjectType
from ..services import db
from sqlalchemy import and_

column_names = [
    "Project_ID",
    "Project_Year",
    "Project_Owner",
    "Project_Type",
    "Fleet_or_Station",
    "Project_Funder",
    "Project_Description",
    "GHG_Reduced", # tons
    "GGE_Reduced", # gallons
    "Address",
    "City",
    "State",
    "Zip",
    "Latitude",
    "Longitude",
    "blank_1",
    "blank_2",
    "blank_3",
    "blank_4",
    "blank_5",
    "blank_6"
]

CsvRow = namedtuple('CsvRow', column_names)

def prep_cell(cell):
    return cell.strip()

def read_csv(stream):
    for i, row in enumerate(csv.reader(stream)):
        if i == 0: continue
        yield CsvRow(*[prep_cell(cell) for cell in row])

def load_from_file(local_file):
    
    project_names = db.session.query(ProjectType.type_name).all()
    print('project types', project_names)
    project_types = set(project_names)

    for row in read_csv(open(local_file, 'r')):
        location = Location(
            address=row.Address,
            city=row.City,
            state=row.State,
            zip_code=row.Zip
        )
        location.set_xy(row.Longitude, row.Latitude)

        project = Project(
            name=row.Project_Owner,
            description=row.Project_Description,
            year=int(row.Project_Year),
            fleet_or_station=row.Fleet_or_Station,
            funder=row.Project_Funder,
            ghg_reduced=float(row.GHG_Reduced.replace(',', '')),
            gge_reduced=float(row.GGE_Reduced.replace(',', ''))
        )

        if row.Project_ID != 'TBD':
            project.id = row.Project_ID

        if not row.Project_Type in project_types:

            '''Is this second check unnecessary?
            '''
            proj_type = db.session\
                    .query(ProjectType)\
                    .filter(ProjectType.type_name==row.Project_Type)

            if not db.session.query(proj_type.exists()).scalar():
                project_type = ProjectType(type_name=row.Project_Type)
                db.session.add(project_type)
                db.session.flush()
                db.session.refresh(project_type)
                project.project_type_id = project_type.id
                project_types |= set([project_type.type_name])

        
        curr_project = db.session.query(Project)\
                .filter(
                    and_(
                        Project.year==project.year, 
                        Project.name==project.name
                    )
                )

        if not db.session.query(curr_project.exists()).scalar():
            db.session.add(project)
            db.session.commit()

        db.session.flush()
        db.session.refresh(project)

        location.project_id = project.id 

        db.session.add(location)
        db.session.commit()
