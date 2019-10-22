docker container exec -it meep_postgres \
psql -h localhost -p 5432 -d meep_api -U meep --password
