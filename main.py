import os
from src import create_app, db
from src.models import User, Role, Project, Location, ProjectType
# from flask_migrate import Migrate

app = create_app(os.get_env('FLASK_CONFIG') or 'default')
# migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Project=Project,
                Location=Location, ProjectType=ProjectType)
