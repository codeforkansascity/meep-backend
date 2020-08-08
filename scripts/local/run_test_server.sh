#!/bin/sh
source $(pipenv --venv)/bin/activate
export APP_SETTINGS=env.test.cfg
export FLASK_APP="src/app:create_app()"
export FLASK_ENV=test
python src/db_operations.py reset test
flask run