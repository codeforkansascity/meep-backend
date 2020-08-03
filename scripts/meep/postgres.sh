#!/bin/bash
docker container run \
 --rm \
 --name meep_postgres \
 --network meep_net \
 -e POSTGRES_USER=meep \
 -e POSTGRES_PASSWORD=password \
 -e POSTGRES_DB=meep_api \
 -d \
 -v meep_data:/var/lib/postgresql/data \
  metroenergy/meep-db:0.0.2
