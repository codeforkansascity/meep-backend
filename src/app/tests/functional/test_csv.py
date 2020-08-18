from ..conftest import create_app, Location, Project, ProjectType,\
    db, load_from_file

from pathlib import Path

def test_load_csv(app):
    load_from_file(Path('staging/data/test.csv').resolve())