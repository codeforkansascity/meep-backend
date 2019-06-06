#!/bin/bash
docker container run --rm --name "meep-db" -p 25432:5432 -d -t \
-v scripts:/scripts \
-v xlsx:/xlsx \
meep-db;
