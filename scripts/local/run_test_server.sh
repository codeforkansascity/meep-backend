#!/usr/bin/env bash

# shellcheck disable=SC1090
source "$(pipenv --venv)/bin/activate"
export APP_SETTINGS=env.test.cfg
export FLASK_APP="src/app:create_app()"
export FLASK_ENV=test

DATA_TYPE=$1
PROJECT_COUNT=${2:-5}

if [ "$DATA_TYPE" == 'rand' ] || [ "$DATA_TYPE" == 'random' ]; then
    python src/db_operations.py clear test
    python src/db_operations.py seed_rand test "$PROJECT_COUNT"
elif [ "$DATA_TYPE" == 'last' ]; then
    echo "Running server with previous state..."
else
    python src/db_operations.py reset test
fi
flask run
