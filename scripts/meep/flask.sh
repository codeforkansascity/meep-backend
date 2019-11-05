docker container run \
 --rm \
 --network meep_net \
 -d \
 --name meep_api \
 -e PROD_DATABASE_URL=postgresql://meep:password@meep_postgres:5432/meep_api \
 -e APP_CONFIG=prod \
 -p 18773:8000 \
 metroenergy/meep-api:0.0.3
