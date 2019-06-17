#!/bin/bash
docker container run --rm --name "meep-db" -p 25432:5432 -d -t \
-v $(pwd)/scripts:/scripts \
-v $(pwd)/data_cleaning/processed:/data \
meep-db;
